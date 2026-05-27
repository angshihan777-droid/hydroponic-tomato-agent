from backend.app.state import TomatoState
from backend.knowledge.cultivation_kb import CULTIVATION_KNOWLEDGE, CultivationKnowledge


def format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def knowledge_matches(state: TomatoState, knowledge: CultivationKnowledge) -> bool:
    actual_value = state.get(knowledge["field"], "")
    return knowledge["value"] in str(actual_value)


def cultivation_agent(state: TomatoState) -> dict[str, str]:
    matched = [
        knowledge
        for knowledge in CULTIVATION_KNOWLEDGE
        if knowledge_matches(state, knowledge)
    ]
    findings = [item["finding"] for item in matched] or ["当前没有明显栽培异常。"]
    suggestions = [item["suggestion"] for item in matched] or [
        "继续保持当前管理措施，并定期观察植株长势、叶色和坐果情况。"
    ]
    risks = [item["risk"] for item in matched if "risk" in item]

    report = f"""栽培状态：
{format_bullets(findings)}

建议：
{format_bullets(suggestions)}

风险：
{format_bullets(risks) if risks else "- 暂无明确栽培风险命中。"}
"""
    return {"cultivation_report": report}
