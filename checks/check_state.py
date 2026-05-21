import sys
from pathlib import Path

# 手动检查脚本放在 checks/ 子目录里，需要把项目根目录加入导入路径。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.state import create_initial_state


def main() -> None:
    # 1. 创建一块初始会议白板
    state = create_initial_state(
        tomato_stage="坐果期",
        ph=6.7,
        ec=3.2,
        air_temperature=31,
        air_humidity=86,
        light_hours=5.5,
        irrigation_count=8,
        substrate_moisture="过湿",
        observation="下部叶片发黄，棚内闷湿",
    )

    # 2. 检查关键字段是否存在
    required_fields = [
        "tomato_stage",
        "ph",
        "ec",
        "air_temperature",
        "air_humidity",
        "light_hours",
        "irrigation_count",
        "substrate_moisture",
        "observation",
        "cultivation_report",
        "fertigation_report",
        "environment_report",
        "risk_report",
        "daily_report",
        "structured_result",
    ]
    missing_fields = [field for field in required_fields if field not in state]

    print("缺失字段：", missing_fields)
    print("水肥专家报告默认值：", repr(state["fertigation_report"]))
    print("结构化结果类型：", type(state["structured_result"]).__name__)
   

if __name__ == "__main__":
    main()
