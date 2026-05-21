from typing import Any, TypedDict


class TomatoState(TypedDict, total=False):
    """无土番茄多 Agent 系统的共享白板。"""

    # 用户输入区：农业技术员带进会议的现场数据
    tomato_stage: str
    ph: float
    ec: float
    air_temperature: float
    air_humidity: float
    light_hours: float
    irrigation_count: int
    substrate_moisture: str
    observation: str

    # Agent 输出区：每位专家把自己的判断写回这里
    cultivation_report: str
    fertigation_report: str
    environment_report: str
    risk_report: str

    # 最终输出区：给人看的日报 + 给程序用的结构化结果
    daily_report: str
    structured_result: dict[str, Any]


def create_initial_state(
    *,
    tomato_stage: str,
    ph: float,
    ec: float,
    air_temperature: float,
    air_humidity: float,
    light_hours: float,
    irrigation_count: int,
    substrate_moisture: str,
    observation: str,
) -> TomatoState:
    """创建一块完整的初始会议白板。"""
    return {
        "tomato_stage": tomato_stage,
        "ph": ph,
        "ec": ec,
        "air_temperature": air_temperature,
        "air_humidity": air_humidity,
        "light_hours": light_hours,
        "irrigation_count": irrigation_count,
        "substrate_moisture": substrate_moisture,
        "observation": observation,
        "cultivation_report": "",
        "fertigation_report": "",
        "environment_report": "",
        "risk_report": "",
        "daily_report": "",
        "structured_result": {},
    }

