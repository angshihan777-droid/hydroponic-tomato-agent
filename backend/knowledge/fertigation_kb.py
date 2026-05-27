from typing import Literal, NotRequired, TypedDict


class FertigationKnowledge(TypedDict):
    name: str
    field: str
    operator: Literal[">", ">=", "contains"]
    value: float | int | str
    finding: str
    suggestion: str
    risk: NotRequired[str]


FERTIGATION_KNOWLEDGE: list[FertigationKnowledge] = [
    {
        "name": "pH 偏高",
        "field": "ph",
        "operator": ">",
        "value": 6.5,
        "finding": "pH 偏高，可能影响铁、锰等微量元素有效性。",
        "suggestion": "复测营养液和排液 pH，确认传感器校准后再小幅调整酸度。",
    },
    {
        "name": "EC 偏高",
        "field": "ec",
        "operator": ">",
        "value": 3.0,
        "finding": "EC 偏高，根区可能存在盐分累积。",
        "suggestion": "检查营养液浓度、回液 EC、排液比例和基质盐分累积情况。",
        "risk": "营养液浓度偏高或排液不足会增加吸水困难和盐害风险。",
    },
    {
        "name": "基质过湿",
        "field": "substrate_moisture",
        "operator": "contains",
        "value": "过湿",
        "finding": "基质过湿，根区氧气供应可能不足。",
        "suggestion": "检查单次灌溉量、灌溉间隔、排液比例和排水通畅情况。",
        "risk": "基质过湿会增加根区缺氧和烂根风险。",
    },
    {
        "name": "灌溉次数偏多",
        "field": "irrigation_count",
        "operator": ">=",
        "value": 8,
        "finding": "今日灌溉次数偏多，需要结合基质湿度和排液判断是否过量。",
        "suggestion": "如排液不足或基质持续过湿，应减少频次或降低单次灌溉量。",
    },
]
