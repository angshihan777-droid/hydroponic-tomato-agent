from app.state import TomatoState
from knowledge.cultivation_kb import CULTIVATION_KNOWLEDGE, CultivationKnowledge


def knowledge_matches(state: TomatoState, knowledge: CultivationKnowledge) -> bool:
    """判断某条栽培知识是否命中当前 State。"""
    field = knowledge["field"]
    actual_value = state.get(field, "")
    operator = knowledge["operator"]
    expected_value = knowledge["value"]

    if operator == "contains":
        return expected_value in str(actual_value)

    return False


def format_bullets(items: list[str]) -> str:
    """把字符串列表格式化成 Markdown 项目符号。"""
    return "\n".join(f"- {item}" for item in items)


def cultivation_agent(state: TomatoState) -> dict[str, str]:
    """栽培专家：读取 State，查询栽培知识库，生成栽培报告。"""
    # 先从栽培知识库里找出命中的知识卡片。
    matched_knowledge = []
    for knowledge in CULTIVATION_KNOWLEDGE:
        if knowledge_matches(state, knowledge):
            matched_knowledge.append(knowledge)

    # 再把命中的知识卡片拆成报告需要的栏目。
    findings = []
    suggestions = []
    risks = []
    for knowledge in matched_knowledge:
        findings.append(knowledge["finding"])
        suggestions.append(knowledge["suggestion"])
        if "risk" in knowledge:
            risks.append(knowledge["risk"])

    # 如果没有命中任何知识卡片，也要给下游一个明确结论。
    if not findings:
        findings.append("当前没有明显的栽培问题。")
    if not suggestions:
        suggestions.append("继续保持当前的管理措施，定期观察。")

    # 拼接成固定格式报告，方便后续 Risk_Agent 和 Decision_Agent 读取。
    report = f"""栽培状态：
{format_bullets(findings)}

建议：
{format_bullets(suggestions)}

风险：
{format_bullets(risks) if risks else "- 暂无明确栽培风险命中。"}
"""
    return {"cultivation_report": report}
