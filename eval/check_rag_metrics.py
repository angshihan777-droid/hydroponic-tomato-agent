from eval.rag_eval_cases import RAG_DOCUMENTS, RAG_EVAL_CASES


# Chunk 正文长度的第一版经验阈值，后续可以根据评测结果调整。
MIN_CONTENT_LENGTH = 20
MAX_CONTENT_LENGTH = 300


# 统一计算标准答案、检索结果和命中数量，供多个指标复用。
def get_eval_sets(expected_doc_ids, retrieved_doc_ids):
    expected_set = set(expected_doc_ids)
    retrieved_set = set(retrieved_doc_ids)
    hit_count = len(expected_set & retrieved_set)
    return expected_set, retrieved_set, hit_count


# 计算 Recall（召回率）：标准相关资料中命中了多少。
def calculate_recall(expected_doc_ids, retrieved_doc_ids):
    expected_set, _, hit_count = get_eval_sets(expected_doc_ids, retrieved_doc_ids)

    if not expected_set:
        return 0.0

    return hit_count / len(expected_set)


# 计算 Precision（精确率）：实际返回资料中有多少是正确的。
def calculate_precision(expected_doc_ids, retrieved_doc_ids):
    _, retrieved_set, hit_count = get_eval_sets(expected_doc_ids, retrieved_doc_ids)

    if not retrieved_set:
        return 0.0

    return hit_count / len(retrieved_set)


# 计算 Hit Rate（命中率）：Top K 结果里是否至少命中一条正确资料。
def calculate_hit_rate(expected_doc_ids, retrieved_doc_ids):
    _, _, hit_count = get_eval_sets(expected_doc_ids, retrieved_doc_ids)
    return 1.0 if hit_count > 0 else 0.0


# 计算 MRR（平均倒数排名）：第一条正确资料排得越靠前，分数越高。
def calculate_mrr(expected_doc_ids, retrieved_doc_ids):
    expected_set = set(expected_doc_ids)

    for index, doc_id in enumerate(retrieved_doc_ids):
        if doc_id in expected_set:
            rank = index + 1
            return 1 / rank
    return 0.0


# 汇总单条评测题的所有指标。
def evaluate_case(case):
    expected_doc_ids = case["expected_doc_ids"]
    retrieved_doc_ids = case["retrieved_doc_ids"]

    return {
        "case_id": case["case_id"],
        "recall": calculate_recall(expected_doc_ids, retrieved_doc_ids),
        "precision": calculate_precision(expected_doc_ids, retrieved_doc_ids),
        "hit_rate": calculate_hit_rate(expected_doc_ids, retrieved_doc_ids),
        "mrr": calculate_mrr(expected_doc_ids, retrieved_doc_ids),
    }


def check_chunk_quality(documents):
    """检查资料片段是否具备最基本的 RAG 可用性。"""
    quality_issues = []

    for document in documents:
        doc_id = document.get("doc_id", "")
        title = document.get("title", "")
        content = document.get("content", "")
        label = doc_id or "<missing_doc_id>"

        if not doc_id:
            quality_issues.append(f"{label}: 缺少 doc_id")

        if not title:
            quality_issues.append(f"{label}: 缺少 title")

        if not content:
            quality_issues.append(f"{label}: 缺少 content")
            continue

        content_length = len(content)

        if content_length < MIN_CONTENT_LENGTH:
            quality_issues.append(
                f"{label}: content 太短，当前 {content_length} 字"
            )

        if content_length > MAX_CONTENT_LENGTH:
            quality_issues.append(
                f"{label}: content 太长，当前 {content_length} 字"
            )

    return quality_issues


def summarize_metrics(results):
    """汇总所有评测题的平均指标，帮助判断整体检索质量。"""
    if not results:
        return {
            "avg_recall": 0.0,
            "avg_precision": 0.0,
            "avg_hit_rate": 0.0,
            "avg_mrr": 0.0,
        }

    case_count = len(results)

    return {
        "avg_recall": sum(result["recall"] for result in results) / case_count,
        "avg_precision": (
            sum(result["precision"] for result in results) / case_count
        ),
        "avg_hit_rate": (
            sum(result["hit_rate"] for result in results) / case_count
        ),
        "avg_mrr": sum(result["mrr"] for result in results) / case_count,
    }


def main():
    results = []

    for case in RAG_EVAL_CASES:
        metrics = evaluate_case(case)
        results.append(metrics)
        notes = case.get("notes", "")

        print(
            f'{metrics["case_id"]}:\n'
            f'  recall={metrics["recall"]:.2f}\n'
            f'  precision={metrics["precision"]:.2f}\n'
            f'  hit_rate={metrics["hit_rate"]:.2f}\n'
            f'  mrr={metrics["mrr"]:.2f}\n'
            f'  notes={notes}'
        )
        print()

    summary = summarize_metrics(results)
    print(
        "summary:\n"
        f'  avg_recall={summary["avg_recall"]:.2f}\n'
        f'  avg_precision={summary["avg_precision"]:.2f}\n'
        f'  avg_hit_rate={summary["avg_hit_rate"]:.2f}\n'
        f'  avg_mrr={summary["avg_mrr"]:.2f}'
    )
    print()

    quality_issues = check_chunk_quality(RAG_DOCUMENTS)
    print("chunk_quality:")

    if not quality_issues:
        print("  passed")
        return

    for issue in quality_issues:
        print(f"  {issue}")


if __name__ == "__main__":
    main()
