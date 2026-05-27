from backend.app.state import TomatoState
from backend.knowledge.fertigation_kb import FERTIGATION_KNOWLEDGE, FertigationKnowledge


def format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def knowledge_matches(state: TomatoState, knowledge: FertigationKnowledge) -> bool:
    actual_value = state.get(knowledge["field"], "")
    expected_value = knowledge["value"]
    operator = knowledge["operator"]

    if operator == ">":
        return float(actual_value) > float(expected_value)
    if operator == ">=":
        return float(actual_value) >= float(expected_value)
    if operator == "contains":
        return str(expected_value) in str(actual_value)
    return False


def fertigation_agent(state: TomatoState) -> dict[str, str]:
    matched = [
        knowledge
        for knowledge in FERTIGATION_KNOWLEDGE
        if knowledge_matches(state, knowledge)
    ]
    findings = [item["finding"] for item in matched] or ["水肥指标未命中明显异常规则。"]
    suggestions = [item["suggestion"] for item in matched] or [
        "维持当前水肥策略，并继续观察 pH、EC、排液和基质湿度变化。"
    ]
    risks = [item["risk"] for item in matched if "risk" in item]

    report = f"""水肥状态：
{format_bullets(findings)}

依据：
- pH：{state.get("ph")}
- EC：{state.get("ec")}
- 今日灌溉次数：{state.get("irrigation_count")}
- 基质湿度：{state.get("substrate_moisture")}
- 现场观察：{state.get("observation", "")}

建议：
{format_bullets(suggestions)}

风险：
{format_bullets(risks) if risks else "- 暂无明确水肥风险命中。"}
"""
    return {"fertigation_report": report}
