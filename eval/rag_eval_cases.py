# 模拟 RAG 资料库里的文档片段。
# V4 接入真实检索器后，这里会逐步替换为从知识文档切出来的 chunk。
RAG_DOCUMENTS = [
    {
        "doc_id": "fertigation_substrate_wet",
        "title": "基质过湿",
        "content": "基质过湿会增加根区缺氧和烂根风险，需要检查灌溉量、灌溉间隔和排液情况。",
    },
    {
        "doc_id": "environment_high_humidity",
        "title": "空气湿度偏高",
        "content": "空气湿度偏高会增加灰霉和叶部病害风险，需要加强通风，减少叶面长时间结露。",
    },
]


# RAG 评测题：expected_doc_ids 是标准答案，retrieved_doc_ids 是当前模拟检索结果。
RAG_EVAL_CASES = [
    {
        "case_id": "case_substrate_wet",
        "query": "基质过湿时应该检查什么？",
        "reference_answer": "应检查灌溉量、灌溉间隔和排液情况，并关注根区缺氧和烂根风险。",
        "expected_doc_ids": ["fertigation_substrate_wet"],
        "retrieved_doc_ids": ["fertigation_substrate_wet"],
        "notes": "第一版先手工模拟检索结果，后面再替换成真实检索结果。",
    },
    {
        "case_id": "case_high_humidity",
        "query": "空气湿度偏高时应该怎么办？",
        "reference_answer": "需要加强通风，减少叶面长时间结露，以降低灰霉和叶部病害风险。",
        "expected_doc_ids": ["environment_high_humidity"],
        "retrieved_doc_ids": ["environment_high_humidity"],
        "notes": "第一版先手工模拟检索结果，后面再替换成真实检索结果。",
    },
    {
        "case_id": "case_substrate_wet_with_noise",
        "query": "基质过湿时应该检查什么？",
        "reference_answer": "应检查灌溉量、灌溉间隔和排液情况，并关注根区缺氧和烂根风险。",
        "expected_doc_ids": ["fertigation_substrate_wet"],
        "retrieved_doc_ids": [
            "fertigation_substrate_wet",
            "environment_high_humidity",
        ],
        "notes": "命中正确资料，但夹杂了一条无关资料，用来观察 precision 下降。",
    },
    {
        "case_id": "case_high_humidity_rank_second",
        "query": "空气湿度偏高时应该怎么办？",
        "reference_answer": "需要加强通风，减少叶面长时间结露，以降低灰霉和叶部病害风险。",
        "expected_doc_ids": ["environment_high_humidity"],
        "retrieved_doc_ids": [
            "fertigation_substrate_wet",
            "environment_high_humidity",
        ],
        "notes": "命中正确资料，但正确资料排在第二位，用来观察 mrr 下降。",
    },
    {
        "case_id": "case_substrate_wet_missed",
        "query": "基质过湿时应该检查什么？",
        "reference_answer": "应检查灌溉量、灌溉间隔和排液情况，并关注根区缺氧和烂根风险。",
        "expected_doc_ids": ["fertigation_substrate_wet"],
        "retrieved_doc_ids": ["environment_high_humidity"],
        "notes": "完全没有命中正确资料，用来观察 recall、hit_rate 和 mrr 变为 0。",
    },
]
