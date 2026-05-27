from typing import Literal, NotRequired, TypedDict


class RiskKnowledge(TypedDict):
    name: str
    field: str
    operator: Literal["contains"]
    value: str
    finding: str
    suggestion: str
    risk_level: NotRequired[str]


RISK_KNOWLEDGE: list[RiskKnowledge] = [
    {
        "name": "高湿病害风险",
        "field": "environment_report",
        "operator": "contains",
        "value": "高湿",
        "finding": "环境报告提示高湿相关风险。",
        "suggestion": "优先检查通风和叶面结露情况，必要时复查灰霉等病害迹象。",
        "risk_level": "medium",
    },
    {
        "name": "基质过湿根区风险",
        "field": "fertigation_report",
        "operator": "contains",
        "value": "基质过湿",
        "finding": "水肥报告提示基质过湿，根区缺氧风险上升。",
        "suggestion": "复查灌溉频次、排液情况和根系颜色，避免根区持续缺氧。",
        "risk_level": "medium",
    },
    {
        "name": "叶片发黄复合风险",
        "field": "cultivation_report",
        "operator": "contains",
        "value": "叶片发黄",
        "finding": "栽培报告提示叶片发黄，需要综合排查。",
        "suggestion": "结合基质湿度、EC、pH、光照和根区状态判断原因。",
        "risk_level": "medium",
    },
    {
        "name": "裂果观察风险",
        "field": "observation",
        "operator": "contains",
        "value": "裂果",
        "finding": "现场观察出现裂果迹象。",
        "suggestion": "重点排查水分波动、湿度变化和坐果期管理稳定性。",
        "risk_level": "high",
    },
]
