RAG_EVAL_CASES = [
    {
        "case_id": "case_substrate_wet",
        "query": "基质过湿，排液很少，根区缺氧应该怎么处理？",
        "expected_doc_ids": ["fertigation_substrate_wet"],
    },
    {
        "case_id": "case_ec_high",
        "query": "排液 EC 持续升高，叶缘焦枯，怀疑根区盐分累积",
        "expected_doc_ids": ["fertigation_ec_high", "fertigation_low_drainage"],
    },
    {
        "case_id": "case_ph_high",
        "query": "pH 偏高，新叶黄化，可能是铁锰等微量元素吸收不好",
        "expected_doc_ids": ["fertigation_ph_high", "cultivation_leaf_yellowing"],
    },
    {
        "case_id": "case_high_humidity",
        "query": "棚内湿度高，叶面结露，担心灰霉病",
        "expected_doc_ids": ["environment_high_humidity", "environment_poor_ventilation"],
    },
    {
        "case_id": "case_high_temperature",
        "query": "白天温度太高，番茄萎蔫，坐果下降",
        "expected_doc_ids": ["environment_high_temperature"],
    },
    {
        "case_id": "case_low_light",
        "query": "连续阴雨，光照不足，果实膨大慢",
        "expected_doc_ids": ["environment_low_light"],
    },
    {
        "case_id": "case_blossom_end_rot",
        "query": "果实花端出现褐色凹陷斑块，是不是只要补钙？",
        "expected_doc_ids": ["cultivation_blossom_end_rot"],
    },
    {
        "case_id": "case_fruit_cracking",
        "query": "番茄快成熟时裂果，最近灌水忽多忽少",
        "expected_doc_ids": ["cultivation_fruit_cracking"],
    },
    {
        "case_id": "case_poor_fruit_set",
        "query": "开花很多但是坐果差，落花多，温室又热又湿",
        "expected_doc_ids": ["cultivation_poor_fruit_set", "cultivation_flowering_fruiting"],
    },
]
