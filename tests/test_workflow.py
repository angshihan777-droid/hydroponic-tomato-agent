from backend.app.service import run_decision_workflow
from backend.app.state import create_initial_state
from backend.retrieval.hybrid_retriever import search_chunks


def sample_state_kwargs() -> dict:
    return {
        "tomato_stage": "坐果期",
        "ph": 6.7,
        "ec": 3.2,
        "air_temperature": 31,
        "air_humidity": 86,
        "light_hours": 5.5,
        "irrigation_count": 8,
        "substrate_moisture": "过湿",
        "observation": "叶片发黄，棚内闷湿，个别果实有裂果迹象",
    }


def test_initial_state_defaults() -> None:
    state = create_initial_state(**sample_state_kwargs())
    assert state["risk_level"] == "low"
    assert state["rag_evidence"] == []
    assert state["llm_daily_report"] == ""


def test_hybrid_retriever_returns_evidence() -> None:
    results = search_chunks("基质过湿 排液不足 根区缺氧", top_k=3)
    doc_ids = [result["chunk"]["doc_id"] for result in results]
    assert "fertigation_substrate_wet" in doc_ids
    assert all("embedding_score" in result for result in results)


def test_workflow_high_risk_fallback_report() -> None:
    result = run_decision_workflow(**sample_state_kwargs())
    assert result["risk_level"] == "high"
    assert result["review_report"]
    assert result["daily_report"]
    assert result["rag_evidence"]
    assert result["llm_error"]
