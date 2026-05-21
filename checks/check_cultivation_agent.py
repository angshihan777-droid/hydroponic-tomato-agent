from app.state import create_initial_state
from agents.cultivation_agent import cultivation_agent

def main():
    state=create_initial_state(
        tomato_stage="坐果期",
        ph=6.7,
        ec=3.2,
        air_temperature=31,
        air_humidity=86,
        light_hours=5.5,
        irrigation_count=8,
        substrate_moisture="过湿",
        observation="叶片发黄，长势一般",
    )
     
    result = cultivation_agent(state)

    print("栽培专家返回字段：", list(result.keys()))
    print("栽培专家报告：")
    print(result["cultivation_report"])

if __name__ == "__main__":
    main()   