from backend.eval.rag_eval_cases import RAG_EVAL_CASES


def calculate_recall(expected_doc_ids: list[str], retrieved_doc_ids: list[str]) -> float:
    expected = set(expected_doc_ids)
    if not expected:
        return 0.0
    return len(expected & set(retrieved_doc_ids)) / len(expected)


def calculate_precision(expected_doc_ids: list[str], retrieved_doc_ids: list[str]) -> float:
    retrieved = set(retrieved_doc_ids)
    if not retrieved:
        return 0.0
    return len(set(expected_doc_ids) & retrieved) / len(retrieved)


def calculate_hit_rate(expected_doc_ids: list[str], retrieved_doc_ids: list[str]) -> float:
    return 1.0 if set(expected_doc_ids) & set(retrieved_doc_ids) else 0.0


def calculate_mrr(expected_doc_ids: list[str], retrieved_doc_ids: list[str]) -> float:
    expected = set(expected_doc_ids)
    for index, doc_id in enumerate(retrieved_doc_ids, start=1):
        if doc_id in expected:
            return 1 / index
    return 0.0


def summarize_metrics(results: list[dict[str, float | str]]) -> dict[str, float]:
    if not results:
        return {"avg_recall": 0.0, "avg_precision": 0.0, "avg_hit_rate": 0.0, "avg_mrr": 0.0}
    return {
        "avg_recall": sum(float(item["recall"]) for item in results) / len(results),
        "avg_precision": sum(float(item["precision"]) for item in results) / len(results),
        "avg_hit_rate": sum(float(item["hit_rate"]) for item in results) / len(results),
        "avg_mrr": sum(float(item["mrr"]) for item in results) / len(results),
    }


def main() -> None:
    print(f"case_count={len(RAG_EVAL_CASES)}")
    for case in RAG_EVAL_CASES:
        print(f'{case["case_id"]}: expected={case["expected_doc_ids"]}')


if __name__ == "__main__":
    main()
