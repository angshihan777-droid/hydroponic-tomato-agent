import sys
from pathlib import Path

# 手动检查脚本放在 checks/ 子目录里，需要把项目根目录加入导入路径。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agents.fertigation_agent import fertigation_agent
from app.state import create_initial_state


def main() -> None:
    # 1. 准备一块带有水肥异常的初始会议白板。
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

    # 2. 单独调用水肥专家，不经过 Graph。
    result = fertigation_agent(state)

    # 3. 先看它返回了哪些 State 字段，再看报告内容。
    print("水肥专家返回字段：", list(result.keys()))
    print("水肥专家报告：")
    print(result["fertigation_report"])


if __name__ == "__main__":
    main()
