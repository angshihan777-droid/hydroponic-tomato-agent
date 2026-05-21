from agents.cultivation_agent import cultivation_agent
from agents.environment_agent import environment_agent
from agents.fertigation_agent import fertigation_agent
from agents.risk_agent import risk_agent
from app.state import create_initial_state


def main() -> None:
    state = create_initial_state(
        tomato_stage="坐果期",
        ph=6.7,
        ec=3.2,
        air_temperature=31,
        air_humidity=86,
        light_hours=5.5,
        irrigation_count=8,
        substrate_moisture="过湿",
        observation="叶片发黄，棚内闷湿，个别果实有裂果迹象",
    )

    state.update(cultivation_agent(state))
    state.update(fertigation_agent(state))
    state.update(environment_agent(state))
    result = risk_agent(state)

    print("风险专家返回字段：", list(result.keys()))
    print("风险专家报告：")
    print(result["risk_report"])


if __name__ == "__main__":
    main()
