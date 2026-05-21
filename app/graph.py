from langgraph.graph import StateGraph, START, END
from app.state import TomatoState
#agent大列表
from agents.cultivation_agent import cultivation_agent
from agents.fertigation_agent import fertigation_agent
from agents.environment_agent import environment_agent
from agents.risk_agent import risk_agent
from agents.decision_agent import decision_agent

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
    "decision_agent": decision_agent,
    }

    for name, node in nodes.items():
        graph.add_node(name, node)
    
    #搭建流程
    edges = [
    (START, "cultivation_agent"),
    ("cultivation_agent", "fertigation_agent"),
    ("fertigation_agent", "environment_agent"),
    ("environment_agent", "risk_agent"),
    ("risk_agent", "decision_agent"),
    ("decision_agent", END),
]

    for start, end in edges:
        graph.add_edge(start, end)

    #编译 Graph
    return graph.compile()