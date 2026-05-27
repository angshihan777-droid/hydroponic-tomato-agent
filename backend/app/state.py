from typing import Any, TypedDict


class TomatoState(TypedDict, total=False):
    """Shared state for the hydroponic tomato multi-agent workflow."""

    tomato_stage: str
    ph: float
    ec: float
    air_temperature: float
    air_humidity: float
    light_hours: float
    irrigation_count: int
    substrate_moisture: str
    observation: str
    llm_provider: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str

    cultivation_report: str
    fertigation_report: str
    environment_report: str
    risk_report: str
    risk_level: str
    missing_reports: list[str]
    risk_evidence: list[str]
    review_report: str
    rag_evidence: list[dict[str, Any]]
    llm_daily_report: str
    llm_error: str

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
    llm_provider: str = "",
    llm_api_key: str = "",
    llm_base_url: str = "",
    llm_model: str = "",
) -> TomatoState:
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
        "llm_provider": llm_provider,
        "llm_api_key": llm_api_key,
        "llm_base_url": llm_base_url,
        "llm_model": llm_model,
        "cultivation_report": "",
        "fertigation_report": "",
        "environment_report": "",
        "risk_report": "",
        "risk_level": "low",
        "missing_reports": [],
        "risk_evidence": [],
        "review_report": "",
        "rag_evidence": [],
        "llm_daily_report": "",
        "llm_error": "",
        "daily_report": "",
        "structured_result": {},
    }
