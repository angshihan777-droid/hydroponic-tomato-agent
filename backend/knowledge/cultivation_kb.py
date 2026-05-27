from typing import Literal, NotRequired, TypedDict


class CultivationKnowledge(TypedDict):
    name: str
    field: str
    operator: Literal["contains"]
    value: str
    finding: str
    suggestion: str
    risk: NotRequired[str]


CULTIVATION_KNOWLEDGE: list[CultivationKnowledge] = [
    {
        "name": "坐果期管理重点",
        "field": "tomato_stage",
        "operator": "contains",
        "value": "坐果期",
        "finding": "当前处于坐果期，需要关注坐果稳定性、果实膨大和水分波动。",
        "suggestion": "保持水肥和环境稳定，重点观察落花落果、裂果和膨果不均。",
    },
    {
        "name": "叶片发黄观察",
        "field": "observation",
        "operator": "contains",
        "value": "叶片发黄",
        "finding": "现场观察到叶片发黄，需要排查根区、水肥、光照和病害因素。",
        "suggestion": "先结合基质湿度、EC、pH 和光照判断原因，不要直接盲目加肥。",
        "risk": "叶片发黄可能由根区缺氧、盐分胁迫、pH 偏高或病害共同造成。",
    },
]
