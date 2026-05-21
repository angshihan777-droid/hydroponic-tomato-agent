from typing import Any

from app.state import TomatoState


def format_bullets(items: list[str]) -> str:
    """把字符串列表格式化成 Markdown 项目符号。"""
    return "\n".join(f"- {item}" for item in items)


def confidence_from_state(state: TomatoState) -> str:
    """根据风险报告粗略给出置信度。"""
    risk_report = state.get("risk_report", "")
    if "medium" in risk_report:
        return "medium"
    return "high"


def decision_agent(state: TomatoState) -> dict[str, Any]:
    """决策专家：汇总所有专家报告，生成技术员日报和结构化结果。"""
    cultivation_report = state.get("cultivation_report", "")
    fertigation_report = state.get("fertigation_report", "")
    environment_report = state.get("environment_report", "")
    risk_report = state.get("risk_report", "")

    status_summary = "已完成栽培、水肥、环境和风险四类视角的综合分析。"
    today_recommendations = [
        "优先处理已命中的水肥和环境异常，避免一次性大幅调整。",
        "持续记录同一时段的 pH、EC、温湿度、光照和现场观察。",
        "对叶片发黄、基质过湿或高湿环境等问题进行次日复查。",
    ]
    risk_warnings = [
        "如风险报告为 medium，需要优先复查根区、通风和叶面病害迹象。"
    ]
    action_checklist = [
        "复测 pH、EC 和基质湿度。",
        "检查棚内通风和叶面结露情况。",
        "记录异常植株照片和位置，便于次日对比。",
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
"""

    structured_result = {
        "status_summary": status_summary,
        "today_recommendations": today_recommendations,
        "risk_warnings": risk_warnings,
        "action_checklist": action_checklist,
        "confidence": confidence,
    }

    return {
        "daily_report": daily_report,
        "structured_result": structured_result,
    }
