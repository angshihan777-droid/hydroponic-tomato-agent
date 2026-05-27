from backend.eval.check_rag_metrics import (
    calculate_hit_rate,
    calculate_mrr,
    calculate_precision,
    calculate_recall,
    summarize_metrics,
)
from backend.eval.rag_eval_cases import RAG_EVAL_CASES
from backend.retrieval.hybrid_retriever import SearchMode, search_chunks


def evaluate_real_retriever(
    *,
    mode: SearchMode = "hybrid",
    top_k: int = 3,
) -> list[dict[str, float | str]]:
    results: list[dict[str, float | str]] = []
    for case in RAG_EVAL_CASES:
        retrieved_doc_ids = [
            result["chunk"]["doc_id"]
            for result in search_chunks(case["query"], top_k=top_k, mode=mode)
        ]
        expected_doc_ids = case["expected_doc_ids"]
        results.append(
            {
                "case_id": case["case_id"],
                "recall": calculate_recall(expected_doc_ids, retrieved_doc_ids),
                "precision": calculate_precision(expected_doc_ids, retrieved_doc_ids),
                "hit_rate": calculate_hit_rate(expected_doc_ids, retrieved_doc_ids),
                "mrr": calculate_mrr(expected_doc_ids, retrieved_doc_ids),
            }
        )
        if mode == "hybrid":
            print(f'{case["case_id"]}:')
            print(f"  query={case['query']}")
            print(f"  expected={expected_doc_ids}")
            print(f"  retrieved={retrieved_doc_ids}")
            print()
    return results


def main() -> None:
    for mode in ["bm25", "embedding", "hybrid"]:
        results = evaluate_real_retriever(mode=mode, top_k=3)
        summary = summarize_metrics(results)
        print(f"{mode}_retriever_summary:")
        print(f'  case_count={len(results)}')
        print(f'  avg_recall={summary["avg_recall"]:.2f}')
        print(f'  avg_precision={summary["avg_precision"]:.2f}')
        print(f'  avg_hit_rate={summary["avg_hit_rate"]:.2f}')
        print(f'  avg_mrr={summary["avg_mrr"]:.2f}')
        print()


if __name__ == "__main__":
    main()
