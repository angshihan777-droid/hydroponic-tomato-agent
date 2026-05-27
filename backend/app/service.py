from backend.app.graph import build_graph
from backend.app.state import TomatoState, create_initial_state


def run_decision_workflow(
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
    state = create_initial_state(
        tomato_stage=tomato_stage,
        ph=ph,
        ec=ec,
        air_temperature=air_temperature,
        air_humidity=air_humidity,
        light_hours=light_hours,
        irrigation_count=irrigation_count,
        substrate_moisture=substrate_moisture,
        observation=observation,
        llm_provider=llm_provider,
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
    )
    return build_graph().invoke(state)
