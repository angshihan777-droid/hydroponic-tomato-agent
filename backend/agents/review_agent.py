from backend.app.state import TomatoState


def format_bullets(items: list[str]) -> str:
    if not items:
        return "- 暂无明确复核依据。"
    return "\n".join(f"- {item}" for item in items)


def review_agent(state: TomatoState) -> dict[str, str]:
    missing_reports = state.get("missing_reports", [])
    missing_report_text = (
        format_bullets(missing_reports)
        if missing_reports
        else "- 三份专家报告均已生成。"
    )

    review_report = f"""复核结论：当前风险等级为 {state.get("risk_level", "low")}，已触发高风险复核流程。

复核依据：
{format_bullets(state.get("risk_evidence", []))}

信息完整性：
{missing_report_text}

现场观察：
{state.get("observation", "")}

给决策专家的提醒：
- 最终日报应优先提示复测关键指标，并强调通风、根区和果实异常复查。
"""
    return {"review_report": review_report}
