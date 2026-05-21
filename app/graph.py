from langgraph.graph import StateGraph, START, END
from app.state import TomatoState
#agent大列表
from agents.cultivation_agent import cultivation_agent
from agents.fertigation_agent import fertigation_agent
from agents.environment_agent import environment_agent
from agents.risk_agent import risk_agent
from agents.review_agent import review_agent
from agents.decision_agent import decision_agent


def route_after_risk(state: TomatoState) -> str:
    """根据风险等级决定是否进入复核专家。"""
    if state.get("risk_level") == "high":
        return "review"
    return "decision"


#开始画流程图
def build_graph():
    #建一张图
    graph = StateGraph(TomatoState)

    #搭建要用的节点
    nodes = {
    "cultivation_agent": cultivation_agent,
    "fertigation_agent": fertigation_agent,
    "environment_agent": environment_agent,
    "risk_agent": risk_agent,
    "review_agent": review_agent,
    "decision_agent": decision_agent,
    }

    for name, node in nodes.items():
        graph.add_node(name, node)
    
    # 前三位专家彼此独立，可以从 START 同时启动。
    graph.add_edge(START, "cultivation_agent")
    graph.add_edge(START, "fertigation_agent")
    graph.add_edge(START, "environment_agent")

    # 三份专家报告都写回 State 后，再汇聚到风险专家。
    graph.add_edge(
        ["cultivation_agent", "fertigation_agent", "environment_agent"],
        "risk_agent",
    )

    # 风险高时先进入复核专家；非高风险直接进入决策专家。
    graph.add_conditional_edges(
        "risk_agent",
        route_after_risk,
        {
            "review": "review_agent",
            "decision": "decision_agent",
        },
    )
    graph.add_edge("review_agent", "decision_agent")
    graph.add_edge("decision_agent", END)

    #编译 Graph
    return graph.compile()
