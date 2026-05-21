from app.state import TomatoState
from knowledge.fertigation_kb import FERTIGATION_KNOWLEDGE, FertigationKnowledge


def format_bullets(items: list[str]) -> str:
    """把字符串列表格式化成 Markdown 项目符号。"""
    return "\n".join(f"- {item}" for item in items)


def knowledge_matches(state: TomatoState, knowledge: FertigationKnowledge) -> bool:
    """判断某条水肥知识是否命中当前 State。

    knowledge 是一条资料规则，state 是现场数据白板。
    """
    field = knowledge["field"]
    operator = knowledge["operator"]
    expected_value = knowledge["value"]
    actual_value = state[field]

    if operator == ">":
        return float(actual_value) > float(expected_value)

    if operator == ">=":
        return float(actual_value) >= float(expected_value)

    if operator == "contains":
        return str(expected_value) in str(actual_value)

    return False


def fertigation_agent(state: TomatoState) -> dict[str, str]:
    """水肥专家：读取 State，查询水肥知识库，生成水肥报告。"""
    # 读取报告需要展示的现场数据。
    ph = state["ph"]
    ec = state["ec"]
    irrigation_count = state["irrigation_count"]
    substrate_moisture = state["substrate_moisture"]
    observation = state["observation"]

    # 查询知识库，筛出当前 State 命中的水肥知识。
    matched_rules = [
        knowledge
        for knowledge in FERTIGATION_KNOWLEDGE
        if knowledge_matches(state, knowledge)
    ]

    # 将命中的知识拆成报告栏目。
    findings = [rule["finding"] for rule in matched_rules]
    suggestions = [rule["suggestion"] for rule in matched_rules]
    risks = [rule["risk"] for rule in matched_rules if "risk" in rule]

    # 没有命中知识时，也要给下游一个明确结论，避免报告空白。
    if not findings:
        findings.append("水肥指标未命中明显异常规则")
        suggestions.append("维持当前水肥策略，并继续观察 pH、EC 和基质湿度变化。")

    # 固定报告格式，方便后续 Risk_Agent 和 Decision_Agent 读取。
    report = f"""水肥状态：
{format_bullets(findings)}

依据：
- pH：{ph}
- EC：{ec}
- 当日灌溉次数：{irrigation_count}
- 基质湿度：{substrate_moisture}
- 现场观察：{observation}

建议：
{format_bullets(suggestions)}

风险：
{format_bullets(risks) if risks else "- 暂无明确水肥风险命中。"}
"""

    # LangGraph 节点返回 dict，用来更新 State 中对应字段。
    return {"fertigation_report": report}
