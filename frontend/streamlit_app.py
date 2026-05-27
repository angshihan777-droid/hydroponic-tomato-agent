import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from backend.app.service import run_decision_workflow
from backend.llm_client import list_llm_models


LOCAL_LLM_CONFIG_PATH = Path(".local_llm_config.json")
PROVIDER_OPTIONS = ["openai", "deepseek", "openai-compatible"]
PROVIDER_LABELS = {
    "openai": "OpenAI",
    "deepseek": "DeepSeek",
    "openai-compatible": "OpenAI 兼容接口",
}
PROVIDER_DEFAULTS = {
    "openai": {
        "base_url": "https://api.openai.com",
        "model": "gpt-4o-mini",
        "base_url_editable": True,
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "base_url_editable": False,
    },
    "openai-compatible": {
        "base_url": "https://api.openai.com",
        "model": "gpt-4o-mini",
        "base_url_editable": True,
    },
}


def default_llm_config() -> dict[str, str]:
    return {
        "provider": "deepseek",
        "base_url": PROVIDER_DEFAULTS["deepseek"]["base_url"],
        "model": PROVIDER_DEFAULTS["deepseek"]["model"],
        "api_key": "",
    }


def load_local_llm_config() -> dict[str, str]:
    if not LOCAL_LLM_CONFIG_PATH.exists():
        return default_llm_config()
    try:
        saved_config = json.loads(LOCAL_LLM_CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default_llm_config()

    config = default_llm_config()
    for key in ["provider", "base_url", "model", "api_key"]:
        if isinstance(saved_config.get(key), str):
            config[key] = saved_config[key]
    if config["provider"] not in PROVIDER_OPTIONS:
        config["provider"] = "deepseek"
    return config


def save_local_llm_config(config: dict[str, str]) -> None:
    LOCAL_LLM_CONFIG_PATH.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def provider_default(provider: str, key: str) -> str:
    return str(PROVIDER_DEFAULTS[provider][key])


def get_model_options(api_key: str, base_url: str) -> list[str]:
    cache_key = f"{base_url}|{api_key[-8:] if api_key else ''}"
    if st.session_state.get("model_cache_key") != cache_key:
        st.session_state.model_cache_key = cache_key
        st.session_state.model_options = list_llm_models(
            api_key=api_key,
            base_url=base_url,
        )
    return st.session_state.model_options


st.set_page_config(page_title="无土番茄智能种植决策助手", layout="wide")
st.title("无土番茄智能种植决策助手")
st.caption("LangGraph 多智能体 + 知识库检索 + 可选 LLM 日报生成")

if "llm_config" not in st.session_state:
    st.session_state.llm_config = load_local_llm_config()
if "model_options" not in st.session_state:
    st.session_state.model_options = []
if "model_cache_key" not in st.session_state:
    st.session_state.model_cache_key = ""

with st.sidebar:
    st.header("现场数据")
    tomato_stage = st.selectbox("生长阶段", ["苗期", "开花期", "坐果期", "采收期"], index=2)
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=6.7, step=0.1)
    ec = st.number_input("EC", min_value=0.0, max_value=10.0, value=3.2, step=0.1)
    air_temperature = st.number_input("空气温度（℃）", value=31.0, step=0.5)
    air_humidity = st.number_input("空气湿度（%）", min_value=0.0, max_value=100.0, value=86.0, step=1.0)
    light_hours = st.number_input("光照时长（小时）", min_value=0.0, max_value=24.0, value=5.5, step=0.5)
    irrigation_count = st.number_input("今日灌溉次数", min_value=0, max_value=50, value=8, step=1)
    substrate_moisture = st.selectbox("基质湿度", ["偏干", "适中", "过湿"], index=2)

    with st.expander("LLM 配置", expanded=True):
        saved_config = st.session_state.llm_config
        provider_index = PROVIDER_OPTIONS.index(saved_config.get("provider", "deepseek"))
        llm_provider = st.selectbox(
            "服务商",
            PROVIDER_OPTIONS,
            index=provider_index,
            format_func=lambda value: PROVIDER_LABELS[value],
        )

        default_base_url = provider_default(llm_provider, "base_url")
        default_model = provider_default(llm_provider, "model")
        base_url_editable = bool(PROVIDER_DEFAULTS[llm_provider]["base_url_editable"])

        if llm_provider == saved_config.get("provider"):
            initial_base_url = saved_config.get("base_url") or default_base_url
            initial_model = saved_config.get("model") or default_model
        else:
            initial_base_url = default_base_url
            initial_model = default_model

        llm_base_url = st.text_input(
            "接口地址",
            value=initial_base_url,
            disabled=not base_url_editable,
            help="OpenAI 兼容接口通常使用 /v1/chat/completions。",
        )
        llm_api_key = st.text_input(
            "密钥",
            value=saved_config.get("api_key", ""),
            type="password",
            help="保存后会写入本地 .local_llm_config.json，请勿提交到 Git。",
        )

        model_options = get_model_options(api_key=llm_api_key, base_url=llm_base_url)
        if model_options:
            preferred_model = initial_model if initial_model in model_options else model_options[0]
            llm_model = st.selectbox(
                "模型",
                model_options,
                index=model_options.index(preferred_model),
            )
        else:
            llm_model = st.text_input("模型", value=initial_model)
            st.caption("未配置密钥或拉取失败时，可手动填写模型名；系统仍可使用规则日报。")

        test_col, save_col = st.columns(2)
        with test_col:
            if st.button("测试连接", use_container_width=True):
                tested_models = list_llm_models(api_key=llm_api_key, base_url=llm_base_url)
                st.session_state.model_options = tested_models
                if tested_models:
                    st.success(f"连接成功，发现 {len(tested_models)} 个模型。")
                else:
                    st.error("连接失败或未返回模型，请检查 API key、地址和网络。")
        with save_col:
            if st.button("保存配置", use_container_width=True):
                st.session_state.llm_config = {
                    "provider": llm_provider,
                    "base_url": llm_base_url,
                    "model": llm_model,
                    "api_key": llm_api_key,
                }
                save_local_llm_config(st.session_state.llm_config)
                st.success("已保存到本地配置文件。")

        has_key = "已配置" if st.session_state.llm_config["api_key"] else "未配置，使用规则 fallback"
        st.caption(
            f"当前：{PROVIDER_LABELS[st.session_state.llm_config['provider']]} / "
            f"{st.session_state.llm_config['model']} / {has_key}"
        )

observation = st.text_area(
    "现场观察记录",
    value="叶片发黄，棚内闷湿，个别果实有裂果迹象",
    height=120,
)

if st.button("生成今日管理建议", type="primary", use_container_width=True):
    active_llm_config = st.session_state.llm_config
    try:
        result = run_decision_workflow(
            tomato_stage=tomato_stage,
            ph=ph,
            ec=ec,
            air_temperature=air_temperature,
            air_humidity=air_humidity,
            light_hours=light_hours,
            irrigation_count=int(irrigation_count),
            substrate_moisture=substrate_moisture,
            observation=observation,
            llm_provider=active_llm_config["provider"],
            llm_api_key=active_llm_config["api_key"],
            llm_base_url=active_llm_config["base_url"],
            llm_model=active_llm_config["model"],
        )
    except Exception as exc:
        st.error(f"生成失败：{exc}")
        st.stop()

    report = result.get("llm_daily_report") or result.get("daily_report", "")
    report_source = "LLM 增强" if result.get("llm_daily_report") else "规则 fallback"
    evidence = result.get("rag_evidence", [])

    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    metric_col_1.metric("风险等级", result.get("risk_level", "unknown"))
    metric_col_2.metric("日报来源", report_source)
    metric_col_3.metric("知识库证据数", len(evidence))

    if result.get("llm_error"):
        st.info(result["llm_error"])

    st.divider()
    st.subheader("今日日报")
    st.markdown(report)

    st.divider()
    st.subheader("知识库证据")
    if not evidence:
        st.info("当前未检索到 RAG 证据。")
    for item in evidence:
        title = item.get("title", "")
        doc_id = item.get("doc_id", "")
        score = item.get("score", 0)
        with st.expander(f"{title} · {doc_id} · score={score:.2f}"):
            st.caption(
                f"混合分：{score:.2f} / BM25：{item.get('bm25_score', 0):.2f} / "
                f"Embedding：{item.get('embedding_score', 0):.2f}"
            )
            st.write(item.get("content", ""))
            if item.get("source"):
                st.caption("来源：" + ", ".join(item["source"]))

    st.divider()
    st.subheader("结构化结果")
    st.json(json.loads(json.dumps(result.get("structured_result", {}), ensure_ascii=False)))
