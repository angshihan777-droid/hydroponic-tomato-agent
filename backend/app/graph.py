from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from backend.agents.cultivation_agent import cultivation_agent
from backend.agents.decision_agent import decision_agent
from backend.agents.environment_agent import environment_agent
from backend.agents.fertigation_agent import fertigation_agent
from backend.agents.review_agent import review_agent
from backend.agents.risk_agent import risk_agent
from backend.app.state import TomatoState


def route_after_risk(state: TomatoState) -> str:
    if state.get("risk_level") == "high":
        return "review"
    return "decision"


@lru_cache(maxsize=1)
def build_graph():
    graph = StateGraph(TomatoState)
    graph.add_node("cultivation_agent", cultivation_agent)
    graph.add_node("fertigation_agent", fertigation_agent)
    graph.add_node("environment_agent", environment_agent)
    graph.add_node("risk_agent", risk_agent)
    graph.add_node("review_agent", review_agent)
    graph.add_node("decision_agent", decision_agent)

    graph.add_edge(START, "cultivation_agent")
    graph.add_edge(START, "fertigation_agent")
    graph.add_edge(START, "environment_agent")
    graph.add_edge(
        ["cultivation_agent", "fertigation_agent", "environment_agent"],
        "risk_agent",
    )
    graph.add_conditional_edges(
        "risk_agent",
        route_after_risk,
        {"review": "review_agent", "decision": "decision_agent"},
    )
    graph.add_edge("review_agent", "decision_agent")
    graph.add_edge("decision_agent", END)
    return graph.compile()
