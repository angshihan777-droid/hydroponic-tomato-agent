import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.service import run_decision_workflow


def main() -> None:
    result = run_decision_workflow(
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
    print("风险等级：", result["risk_level"])
    print("知识库证据：", [item["doc_id"] for item in result["rag_evidence"]])
    print()
    print(result["daily_report"])
    print("结构化结果：")
    print(json.dumps(result["structured_result"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
