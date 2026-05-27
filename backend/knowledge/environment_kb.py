from typing import Literal, NotRequired, TypedDict


class EnvironmentKnowledge(TypedDict):
    name: str
    field: str
    operator: Literal[">=", "<=", "contains"]
    value: float | int | str
    finding: str
    suggestion: str
    risk: NotRequired[str]


ENVIRONMENT_KNOWLEDGE: list[EnvironmentKnowledge] = [
    {
        "name": "温度偏高",
        "field": "air_temperature",
        "operator": ">=",
        "value": 30,
        "finding": "空气温度偏高，可能增加植株蒸腾压力。",
        "suggestion": "优先检查通风、遮阴和降温设备，避免高温时段叠加大幅水分波动。",
        "risk": "高温可能增加落花落果、脐腐和萎蔫风险。",
    },
    {
        "name": "湿度偏高",
        "field": "air_humidity",
        "operator": ">=",
        "value": 80,
        "finding": "空气湿度偏高，棚内可能偏闷湿。",
        "suggestion": "加强通风，降低叶面长时间结露，观察灰霉等病害迹象。",
        "risk": "高湿环境会增加灰霉和叶部病害风险。",
    },
    {
        "name": "光照不足",
        "field": "light_hours",
        "operator": "<=",
        "value": 6,
        "finding": "每日光照时长偏少，可能影响光合作用和果实发育。",
        "suggestion": "检查遮阴、棚膜透光和补光条件，必要时优化叶幕管理。",
    },
    {
        "name": "棚内闷湿",
        "field": "observation",
        "operator": "contains",
        "value": "闷湿",
        "finding": "现场观察提示棚内闷湿，空气交换不足。",
        "suggestion": "优先改善空气流通，观察叶面是否结露和病斑扩展。",
        "risk": "闷湿环境容易放大病害风险。",
    },
]
