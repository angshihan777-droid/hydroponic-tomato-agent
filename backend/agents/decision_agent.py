from typing import Any

from backend.app.state import TomatoState
from backend.llm_client import generate_llm_daily_report
from backend.retrieval.hybrid_retriever import search_chunks


def format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def confidence_from_state(state: TomatoState) -> str:
    if state.get("missing_reports"):
        return "medium"
    if state.get("risk_level") == "high":
        return "medium"
    return "high"


def decision_agent(state: TomatoState) -> dict[str, Any]:
    cultivation_report = state.get("cultivation_report", "")
    fertigation_report = state.get("fertigation_report", "")
    environment_report = state.get("environment_report", "")
    risk_report = state.get("risk_report", "")
    review_report = state.get("review_report", "")
    observation = state.get("observation", "")

    rag_query = " ".join(
        [
            str(state.get("tomato_stage", "")),
            str(state.get("substrate_moisture", "")),
            observation,
            risk_report,
        ]
    )
    rag_results = search_chunks(rag_query, top_k=3)
    rag_evidence = [
        {
            "doc_id": result["chunk"]["doc_id"],
            "title": result["chunk"]["title"],
            "content": result["chunk"]["content"],
            "source": result["chunk"]["source"],
            "score": result["score"],
            "bm25_score": result["bm25_score"],
            "embedding_score": result["embedding_score"],
        }
        for result in rag_results
    ]

    status_summary = "已完成栽培、水肥、环境和风险视角的综合分析。"
    today_recommendations = [
        "优先处理已命中的水肥和环境异常，避免一次性大幅调整。",
        "复测 pH、EC、基质湿度和排液情况，确认传感器与现场读数一致。",
        "对叶片发黄、基质过湿或裂果迹象进行次日复查，并记录照片和位置。",
    ]
    risk_warnings = [
        "如风险等级为 high，应先稳定根区水分和棚内通风，再调整营养液策略。",
        "证据不足时不要把单一症状直接归因到缺肥或病害。",
    ]
    action_checklist = [
        "复测 pH、EC、回液 EC 和基质湿度。",
        "检查棚内通风、叶面结露和病斑扩展情况。",
        "查看排液比例、根系颜色和异常植株分布。",
    ]
    confidence = confidence_from_state(state)

    daily_report = f"""# 无土番茄技术员日报

## 当前状态判断
{status_summary}

## 今日综合建议
{format_bullets(today_recommendations)}

## 风险提醒
{format_bullets(risk_warnings)}

## 今日操作清单
{format_bullets(action_checklist)}

## 置信度
{confidence}

## 专家报告摘要
- 栽培报告：{"已生成" if cultivation_report else "未生成"}
- 水肥报告：{"已生成" if fertigation_report else "未生成"}
- 环境报告：{"已生成" if environment_report else "未生成"}
- 风险报告：{"已生成" if risk_report else "未生成"}
- 复核报告：{"已生成" if review_report else "未触发"}
"""

    structured_result = {
        "status_summary": status_summary,
        "today_recommendations": today_recommendations,
        "risk_warnings": risk_warnings,
        "action_checklist": action_checklist,
        "confidence": confidence,
        "risk_level": state.get("risk_level", "low"),
    }

    evidence_text = "\n\n".join(
        f'- {item["title"]} ({item["doc_id"]})\n{item["content"]}'
        for item in rag_evidence
    )
    llm_prompt = f"""请基于以下专家报告和 RAG 证据，生成一份给农业技术员看的今日管理日报。
要求：
1. 结论必须可执行。
2. 不要编造证据。
3. 如果证据不足，要明确说明。

专家报告：
栽培：{cultivation_report}
水肥：{fertigation_report}
环境：{environment_report}
风险：{risk_report}
复核：{review_report or "未触发复核。"}

RAG 证据：
{evidence_text or "未检索到相关证据。"}
"""
    llm_response = generate_llm_daily_report(
        llm_prompt,
        provider=state.get("llm_provider") or None,
        api_key=state.get("llm_api_key") or None,
        base_url=state.get("llm_base_url") or None,
        model=state.get("llm_model") or None,
    )

    return {
        "daily_report": daily_report,
        "llm_daily_report": llm_response.content if llm_response.content else "",
        "llm_error": llm_response.error if llm_response.error else "",
        "rag_evidence": rag_evidence,
        "structured_result": structured_result,
    }
