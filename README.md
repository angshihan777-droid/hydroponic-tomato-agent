# 无土番茄智能种植决策助手

一个面向无土番茄种植场景的多智能体 RAG 决策 Demo。项目使用 LangGraph 编排栽培、水肥、环境、风险、复核和决策 Agent，通过知识库检索为日报提供可追溯证据，并支持可选 LLM 增强生成。

## 核心能力

- 多 Agent 工作流：栽培、水肥、环境三个专家并行分析，风险 Agent 汇总，高风险时进入复核 Agent。
- RAG 检索：Markdown 知识库切块，支持 BM25、embedding fallback 和 hybrid 检索。
- 可解释输出：展示风险等级、结构化结果、证据 chunk、来源链接和检索分数。
- LLM 可选增强：未配置 API key 时自动使用规则日报，配置后调用 OpenAI-compatible `/v1/chat/completions`。
- Streamlit 演示：可输入现场数据、配置模型、查看日报和证据。

## 技术栈

- Python
- LangGraph
- Streamlit
- BM25 + hashing char-ngram embedding fallback
- pytest

默认 embedding fallback 是纯 Python 的轻量实现，方便离线演示。需要更强语义检索时，可安装 `sentence-transformers` 并设置：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-embedding.txt
$env:EMBEDDING_BACKEND="sentence-transformers"
$env:EMBEDDING_MODEL="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

## 项目结构

```text
backend/
  app/              # 状态、Graph 编排、业务入口
  agents/           # 栽培、水肥、环境、风险、复核、决策 Agent
  knowledge/        # 规则知识卡片与 RAG Markdown 知识库
  retrieval/        # BM25 + embedding hybrid retriever
  eval/             # RAG 评估脚本
  llm_client.py     # OpenAI-compatible LLM 客户端

frontend/
  streamlit_app.py  # Streamlit 前端

scripts/
  run_demo.py       # 命令行演示入口

tests/
  test_workflow.py
```

## 运行

安装依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

命令行 Demo：

```powershell
.\.venv\Scripts\python.exe scripts\run_demo.py
```

RAG 评估：

```powershell
.\.venv\Scripts\python.exe -m backend.eval.check_real_retriever
```

启动前端：

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend\streamlit_app.py
```

浏览器打开：

```text
http://localhost:8501
```

## LLM 配置

LLM 是可选能力。Streamlit 侧边栏可以配置 provider、base URL、模型和 API key。本地保存会写入 `.local_llm_config.json`，该文件已加入 `.gitignore`，不要提交密钥。

也可以用环境变量：

```powershell
$env:LLM_PROVIDER="deepseek"
$env:DEEPSEEK_API_KEY="你的 key"
$env:DEEPSEEK_MODEL="deepseek-chat"
```

或：

```powershell
$env:LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="你的 key"
$env:OPENAI_MODEL="gpt-4o-mini"
```

## 测试与评估

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m backend.eval.check_real_retriever
```

当前内置评估集包含 9 个农业检索问题、15 个知识库 chunk。默认 hybrid 检索在当前评估集上 Top-3 Recall 为 1.00，Hit Rate 为 1.00。默认模式使用轻量 embedding fallback，安装 `requirements-embedding.txt` 后可切换到真实 sentence-transformers embedding。

## GitHub 上传说明

`.gitignore` 默认忽略所有 Markdown 文件，只放行：

- `README.md`
- `backend/knowledge/docs/*.md`

这样可以保留项目说明和知识库文档，同时避免把个人学习笔记、开发设计草稿、阶段记录等 Markdown 上传到 GitHub。

## 简历描述参考

基于 LangGraph 构建多智能体无土番茄种植决策系统，集成 BM25 + embedding 混合检索、农业知识库 evidence 注入、风险分级与高风险复核流程，并通过 Streamlit 提供可交互演示。系统支持 LLM 增强生成与规则 fallback，保证无密钥环境下仍可运行。
