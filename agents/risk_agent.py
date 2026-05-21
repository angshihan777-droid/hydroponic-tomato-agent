from app.state import TomatoState
from knowledge.risk_kb import RISK_KNOWLEDGE, RiskKnowledge


def format_bullets(items: list[str]) -> str:
    """把字符串列表格式化成 Markdown 项目符号。"""
    return "\n".join(f"- {item}" for item in items)


def knowledge_matches(state: TomatoState, knowledge: RiskKnowledge) -> bool:
    """判断某条风险知识是否命中当前 State。"""
    field = knowledge["field"]
    expected_value = knowledge["value"]
    actual_value = state.get(field, "")
    return expected_value in str(actual_value)


# 查找缺失报告
def find_missing_reports(state: TomatoState) -> list[str]:
    """找出风险专家需要但当前缺失的专家报告。"""
    required_reports = [
        "cultivation_report",
        "fertigation_report",
        "environment_report",
    ]

    return [
        report_name
        for report_name in required_reports
        if not state.get(report_name)
    ]


def risk_agent(state: TomatoState) -> dict[str, object]:
    """风险专家：读取前置专家报告和现场观察，生成风险报告。"""
    cultivation_report = state.get("cultivation_report", "")
    fertigation_report = state.get("fertigation_report", "")
    environment_report = state.get("environment_report", "")
    observation = state.get("observation", "")

    # 先检查是否有缺失报告；这个结果会写回 State，供下游判断报告是否完整。
    missing_reports = find_missing_reports(state)

    # 风险专家会读取前面专家的报告，再统一做风险复核。
    matched_knowledge = [
        knowledge
        for knowledge in RISK_KNOWLEDGE
        if knowledge_matches(state, knowledge)
    ]

    findings = [knowledge["finding"] for knowledge in matched_knowledge]
    suggestions = [knowledge["suggestion"] for knowledge in matched_knowledge]
    risk_levels = [
        knowledge["risk_level"]
        for knowledge in matched_knowledge
        if "risk_level" in knowledge
    ]

    if not findings:
        findings.append("当前未命中明确高风险规则。")
    if not suggestions:
        suggestions.append("继续观察现场变化，并保持各项数据连续记录。")

    # overall_risk 是结构化风险等级，后续 Graph 条件边会直接读取它。
    # 注意：不能只把风险等级写在 risk_report 文本里，否则程序无法稳定判断分支。
    if "high" in risk_levels:
        overall_risk = "high"
    elif risk_levels:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    report = f"""风险状态：
{format_bullets(findings)}

依据：
- 栽培报告是否存在：{bool(cultivation_report)}
- 水肥报告是否存在：{bool(fertigation_report)}
- 环境报告是否存在：{bool(environment_report)}
- 现场观察：{observation}

建议：
{format_bullets(suggestions)}

综合风险等级：
{overall_risk}
"""
    return {
        "risk_report": report,
        "risk_level": overall_risk,
        "missing_reports": missing_reports,
        "risk_evidence": findings,
    }
