from backend.app.state import TomatoState
from backend.knowledge.risk_kb import RISK_KNOWLEDGE, RiskKnowledge


def format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def knowledge_matches(state: TomatoState, knowledge: RiskKnowledge) -> bool:
    actual_value = state.get(knowledge["field"], "")
    return knowledge["value"] in str(actual_value)


def find_missing_reports(state: TomatoState) -> list[str]:
    required_reports = ["cultivation_report", "fertigation_report", "environment_report"]
    return [name for name in required_reports if not state.get(name)]


def risk_agent(state: TomatoState) -> dict[str, object]:
    matched = [
        knowledge for knowledge in RISK_KNOWLEDGE if knowledge_matches(state, knowledge)
    ]
    findings = [item["finding"] for item in matched] or ["当前未命中明确高风险规则。"]
    suggestions = [item["suggestion"] for item in matched] or [
        "继续观察现场变化，并保持各项数据连续记录。"
    ]
    risk_levels = [item["risk_level"] for item in matched if "risk_level" in item]

    if "high" in risk_levels:
        overall_risk = "high"
    elif risk_levels:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    report = f"""风险状态：
{format_bullets(findings)}

依据：
- 栽培报告是否存在：{bool(state.get("cultivation_report"))}
- 水肥报告是否存在：{bool(state.get("fertigation_report"))}
- 环境报告是否存在：{bool(state.get("environment_report"))}
- 现场观察：{state.get("observation", "")}

建议：
{format_bullets(suggestions)}

综合风险等级：{overall_risk}
"""
    return {
        "risk_report": report,
        "risk_level": overall_risk,
        "missing_reports": find_missing_reports(state),
        "risk_evidence": findings,
    }
