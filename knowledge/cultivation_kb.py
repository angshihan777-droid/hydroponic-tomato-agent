from typing import Literal, NotRequired, TypedDict


class CultivationKnowledge(TypedDict):
    """栽培知识库里的卡片结构。"""

    name: str
    field: str
    operator: Literal["contains"]
    value: str
    finding: str
    suggestion: str
    risk: NotRequired[str]


# 栽培知识卡片列表
CULTIVATION_KNOWLEDGE: list[CultivationKnowledge] = [
    # 第一张卡片
    {
        "name": "坐果期管理重点",
        "field": "tomato_stage",
        "operator": "contains",
        "value": "坐果期",
        "finding": "当前处于坐果期，需要重点关注坐果稳定性和果实膨大。",
        "suggestion": "保持水肥和环境稳定，观察是否有落花落果、裂果或膨果不均。",
    },
    # 第二张卡片：叶片发黄观察
    {
        "name": "叶片发黄观察",
        "field": "observation",
        "operator": "contains",
        "value": "叶片发黄",
        "finding": "现场观察到叶片发黄，需要排查根区、水肥和光照因素。",
        "suggestion": "先结合基质湿度、EC 和光照情况判断原因，不要直接盲目加肥。",
    },
]
