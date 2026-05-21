from typing import Literal, NotRequired, TypedDict


class FertigationKnowledge(TypedDict):
    """水肥知识库里的一条知识。"""

    # 知识名称：方便我们知道这条资料讲的是什么。
    name: str

    # 观察字段：这条知识主要看 State 里的哪个字段。
    field: str

    # 比较方式：告诉程序以后怎么判断，但这里不直接执行判断。
    operator: Literal[">", ">=", "contains"]

    # 触发值：比如 6.5、3.0、"过湿"。
    value: float | int | str

    # 命中后的判断：写进水肥报告的“水肥状态”栏目。
    finding: str

    # 命中后的建议：写进水肥报告的“建议”栏目。
    suggestion: str

    # 可选风险：有些知识有风险提醒，有些只有建议。
    risk: NotRequired[str]


# 这里现在只保存“知识数据”，不直接写 if，也不写 lambda。
# 真正的判断动作放到 Agent 里做。
FERTIGATION_KNOWLEDGE: list[FertigationKnowledge] = [
    {
        "name": "pH 偏高",
        "field": "ph",
        "operator": ">",
        "value": 6.5,
        "finding": "pH 偏高",
        "suggestion": "复测营养液和回液 pH，再小幅调整酸度。",
    },
    {
        "name": "EC 偏高",
        "field": "ec",
        "operator": ">",
        "value": 3.0,
        "finding": "EC 偏高",
        "suggestion": "检查营养液浓度、回液 EC 和基质盐分累积情况。",
        "risk": "可能存在营养液浓度偏高或基质盐分累积风险。",
    },
    {
        "name": "基质过湿",
        "field": "substrate_moisture",
        "operator": "contains",
        "value": "过湿",
        "finding": "基质过湿",
        "suggestion": "检查单次灌溉量、灌溉间隔和排液情况。",
        "risk": "基质过湿会增加根区缺氧和烂根风险。",
    },
    {
        "name": "灌溉次数偏多",
        "field": "irrigation_count",
        "operator": ">=",
        "value": 8,
        "finding": "灌溉次数偏多",
        "suggestion": "结合基质湿度和排液率判断是否需要减少灌溉频次。",
    },
]
