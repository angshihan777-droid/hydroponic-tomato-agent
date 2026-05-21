from app.state import TomatoState
from knowledge.environment_kb import ENVIRONMENT_KNOWLEDGE, EnvironmentKnowledge


def format_bullets(items: list[str]) -> str:
    """把字符串列表格式化成 Markdown 项目符号。"""
    return "\n".join(f"- {item}" for item in items)


def knowledge_matches(state: TomatoState, knowledge: EnvironmentKnowledge) -> bool:
    """判断某条环境知识是否命中当前 State。"""
    field = knowledge["field"]
    operator = knowledge["operator"]
    expected_value = knowledge["value"]
    actual_value = state.get(field, "")

    if operator == ">=":
        return float(actual_value) >= float(expected_value)

    if operator == "<=":
        return float(actual_value) <= float(expected_value)

    if operator == "contains":
        return str(expected_value) in str(actual_value)

    return False


def environment_agent(state: TomatoState) -> dict[str, str]:
    """环境专家：读取 State，查询环境知识库，生成环境报告。"""
    air_temperature = state.get("air_temperature", "")
    air_humidity = state.get("air_humidity", "")
    light_hours = state.get("light_hours", "")
    observation = state.get("observation", "")

    # 找出当前环境数据命中的知识卡片。
    matched_knowledge = [
        knowledge
        for knowledge in ENVIRONMENT_KNOWLEDGE
        if knowledge_matches(state, knowledge)
    ]

    findings = [knowledge["finding"] for knowledge in matched_knowledge]
    suggestions = [knowledge["suggestion"] for knowledge in matched_knowledge]
    risks = [knowledge["risk"] for knowledge in matched_knowledge if "risk" in knowledge]

    if not findings:
        findings.append("环境知识库未命中明显异常。")
    if not suggestions:
        suggestions.append("继续记录温度、湿度和光照变化，观察是否出现环境波动。")

    report = f"""环境状态：
{format_bullets(findings)}

依据：
- 空气温度：{air_temperature}
- 空气湿度：{air_humidity}
- 每日光照小时数：{light_hours}
- 现场观察：{observation}

建议：
{format_bullets(suggestions)}

风险：
{format_bullets(risks) if risks else "- 暂无明确环境风险命中。"}
"""
    return {"environment_report": report}
