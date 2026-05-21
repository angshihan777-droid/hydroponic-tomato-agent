import json

from app.graph import build_graph
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

    graph = build_graph()
    result = graph.invoke(state)

    assert result["risk_level"] == "high"
    assert result["review_report"]

    print("风险等级：", result["risk_level"])
    print("复核报告：")
    print(result["review_report"])
    print("结构化结果：")
    print(json.dumps(result["structured_result"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
