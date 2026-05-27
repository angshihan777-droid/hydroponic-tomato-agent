from backend.app.state import TomatoState
from backend.knowledge.environment_kb import ENVIRONMENT_KNOWLEDGE, EnvironmentKnowledge


def format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def knowledge_matches(state: TomatoState, knowledge: EnvironmentKnowledge) -> bool:
    actual_value = state.get(knowledge["field"], "")
    expected_value = knowledge["value"]
    operator = knowledge["operator"]

    if operator == ">=":
        return float(actual_value) >= float(expected_value)
    if operator == "<=":
        return float(actual_value) <= float(expected_value)
    if operator == "contains":
        return str(expected_value) in str(actual_value)
    return False


def environment_agent(state: TomatoState) -> dict[str, str]:
    matched = [
        knowledge
        for knowledge in ENVIRONMENT_KNOWLEDGE
        if knowledge_matches(state, knowledge)
    ]
    findings = [item["finding"] for item in matched] or ["环境知识库未命中明显异常。"]
    suggestions = [item["suggestion"] for item in matched] or [
        "继续记录温度、湿度和光照变化，观察是否出现环境波动。"
    ]
    risks = [item["risk"] for item in matched if "risk" in item]

    report = f"""环境状态：
{format_bullets(findings)}

依据：
- 空气温度：{state.get("air_temperature")}
- 空气湿度：{state.get("air_humidity")}
- 每日光照小时数：{state.get("light_hours")}
- 现场观察：{state.get("observation", "")}

建议：
{format_bullets(suggestions)}

风险：
{format_bullets(risks) if risks else "- 暂无明确环境风险命中。"}
"""
    return {"environment_report": report}
