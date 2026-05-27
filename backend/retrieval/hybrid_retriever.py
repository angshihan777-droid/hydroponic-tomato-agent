from __future__ import annotations

from collections import Counter
from functools import lru_cache
import hashlib
from math import log, sqrt
from pathlib import Path
import os
import re
from typing import Literal, Protocol, TypedDict


DOCS_DIR = Path(__file__).resolve().parents[1] / "knowledge" / "docs"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class RagChunk(TypedDict):
    doc_id: str
    title: str
    content: str
    source: list[str]


class SearchResult(TypedDict):
    chunk: RagChunk
    score: float
    bm25_score: float
    embedding_score: float


SearchMode = Literal["bm25", "embedding", "hybrid"]


class EmbeddingBackend(Protocol):
    name: str

    def encode(self, texts: list[str]) -> list[list[float]]:
        ...


class HashingEmbeddingBackend:
    """Dependency-light local embedding fallback for offline demos and tests."""

    name = "hashing-char-ngram"

    def __init__(self, dimensions: int = 2048) -> None:
        self.dimensions = dimensions

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            vector = [0.0] * self.dimensions
            for ngram in char_ngrams(text):
                vector[stable_hash(ngram) % self.dimensions] += 1.0
            norm = sqrt(sum(value * value for value in vector))
            if norm:
                vector = [value / norm for value in vector]
            vectors.append(vector)
        return vectors


class SentenceTransformerBackend:
    name = "sentence-transformers"

    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return [list(map(float, embedding)) for embedding in embeddings]


def load_markdown_files(docs_dir: Path = DOCS_DIR) -> list[Path]:
    if not docs_dir.exists():
        return []
    return sorted(docs_dir.glob("*.md"))


def extract_sources(content: str) -> list[str]:
    sources: list[str] = []
    for line in content.splitlines():
        for url in re.findall(r"https?://\S+", line):
            sources.append(url.rstrip(").,，。"))
    return sources


def extract_metadata(lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if ":" not in stripped:
            break
        key, value = stripped.split(":", maxsplit=1)
        metadata[key.strip()] = value.strip()
    return metadata


def strip_metadata(lines: list[str]) -> list[str]:
    content_start = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            content_start = index + 1
            continue
        if ":" not in stripped:
            content_start = index
            break
    return lines[content_start:]


def parse_markdown_chunks(file_path: Path) -> list[RagChunk]:
    content = file_path.read_text(encoding="utf-8")
    chunks: list[RagChunk] = []
    current_title: str | None = None
    current_lines: list[str] = []

    def flush_current_chunk() -> None:
        if current_title is None:
            return
        metadata = extract_metadata(current_lines)
        doc_id = metadata.get("chunk_id")
        if not doc_id:
            raise ValueError(f"Missing chunk_id in {file_path}: {current_title}")
        chunk_content = "\n".join(strip_metadata(current_lines)).strip()
        chunks.append(
            {
                "doc_id": doc_id,
                "title": current_title,
                "content": chunk_content,
                "source": extract_sources(chunk_content),
            }
        )

    for line in content.splitlines():
        if line.startswith("## "):
            flush_current_chunk()
            current_title = line.removeprefix("## ").strip()
            current_lines = []
            continue
        if current_title is not None:
            current_lines.append(line)

    flush_current_chunk()
    return chunks


@lru_cache(maxsize=1)
def load_all_chunks() -> tuple[RagChunk, ...]:
    chunks: list[RagChunk] = []
    for file_path in load_markdown_files():
        chunks.extend(parse_markdown_chunks(file_path))
    return tuple(chunks)


def tokenize_terms(text: str) -> list[str]:
    lowered = text.lower()
    ascii_tokens = re.findall(r"[a-z0-9_]+", lowered)
    chinese_chars = [char for char in text if "\u4e00" <= char <= "\u9fff"]
    chinese_bigrams = [
        "".join(chinese_chars[index : index + 2])
        for index in range(len(chinese_chars) - 1)
    ]
    return ascii_tokens + chinese_chars + chinese_bigrams


def char_ngrams(text: str, min_n: int = 2, max_n: int = 4) -> list[str]:
    normalized = re.sub(r"\s+", "", text.lower())
    return [
        normalized[index : index + size]
        for size in range(min_n, max_n + 1)
        for index in range(max(len(normalized) - size + 1, 0))
    ]


def stable_hash(value: str) -> int:
    digest = hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, byteorder="big", signed=False)


def chunk_text(chunk: RagChunk) -> str:
    return f'{chunk["title"]}\n{chunk["content"]}'


def calculate_idf(document_tokens: list[list[str]]) -> dict[str, float]:
    document_count = len(document_tokens)
    document_frequency: Counter[str] = Counter()
    for tokens in document_tokens:
        document_frequency.update(set(tokens))
    return {
        token: log(1 + (document_count - frequency + 0.5) / (frequency + 0.5))
        for token, frequency in document_frequency.items()
    }


def bm25_scores(
    query_tokens: list[str],
    document_tokens: list[list[str]],
    *,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[float]:
    if not document_tokens:
        return []

    idf = calculate_idf(document_tokens)
    avg_doc_length = sum(len(tokens) for tokens in document_tokens) / len(document_tokens)
    query_terms = set(query_tokens)
    scores: list[float] = []

    for tokens in document_tokens:
        term_frequency = Counter(tokens)
        doc_length = len(tokens)
        score = 0.0
        for term in query_terms:
            frequency = term_frequency.get(term, 0)
            if not frequency:
                continue
            denominator = frequency + k1 * (
                1 - b + b * doc_length / max(avg_doc_length, 1)
            )
            score += idf.get(term, 0.0) * frequency * (k1 + 1) / denominator
        scores.append(score)
    return scores


def normalize_scores(scores: list[float]) -> list[float]:
    if not scores:
        return []
    max_score = max(scores)
    if max_score <= 0:
        return [0.0 for _ in scores]
    return [score / max_score for score in scores]


@lru_cache(maxsize=1)
def get_embedding_backend() -> EmbeddingBackend:
    backend = os.getenv("EMBEDDING_BACKEND", "hashing").lower()
    if backend in {"sentence-transformers", "sentence_transformers", "semantic"}:
        try:
            return SentenceTransformerBackend(
                os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
            )
        except Exception:
            return HashingEmbeddingBackend()
    return HashingEmbeddingBackend()


def embedding_scores(query: str, documents: list[str]) -> list[float]:
    if not documents:
        return []
    backend = get_embedding_backend()
    vectors = backend.encode([query, *documents])
    query_vector = vectors[0]
    document_vectors = vectors[1:]
    return [dense_cosine_similarity(query_vector, vector) for vector in document_vectors]


def dense_cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    dot_product = sum(left_value * right_value for left_value, right_value in zip(left, right))
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot_product / (left_norm * right_norm)


def search_chunks(
    query: str,
    top_k: int = 3,
    *,
    mode: SearchMode = "hybrid",
    bm25_weight: float = 0.55,
    embedding_weight: float = 0.45,
) -> list[SearchResult]:
    chunks = list(load_all_chunks())
    query_tokens = tokenize_terms(query)
    document_tokens = [tokenize_terms(chunk_text(chunk)) for chunk in chunks]
    documents = [chunk_text(chunk) for chunk in chunks]

    normalized_bm25_scores = normalize_scores(bm25_scores(query_tokens, document_tokens))
    normalized_embedding_scores = normalize_scores(embedding_scores(query, documents))

    results: list[SearchResult] = []
    for index, chunk in enumerate(chunks):
        bm25_score = normalized_bm25_scores[index]
        semantic_score = normalized_embedding_scores[index]

        if mode == "bm25":
            final_score = bm25_score
        elif mode == "embedding":
            final_score = semantic_score
        else:
            final_score = bm25_weight * bm25_score + embedding_weight * semantic_score

        if final_score <= 0:
            continue

        results.append(
            {
                "chunk": chunk,
                "score": final_score,
                "bm25_score": bm25_score,
                "embedding_score": semantic_score,
            }
        )

    return sorted(results, key=lambda result: result["score"], reverse=True)[:top_k]


def main() -> None:
    chunks = load_all_chunks()
    print(f"chunk_count={len(chunks)}")
    print(f"embedding_backend={get_embedding_backend().name}")
    for chunk in chunks:
        print(f'{chunk["doc_id"]} | {chunk["title"]}')


if __name__ == "__main__":
    main()
