from __future__ import annotations

import json
import os
from dataclasses import dataclass
import urllib.error
import urllib.request


@dataclass(frozen=True)
class LLMResponse:
    content: str | None = None
    error: str | None = None


def get_llm_config() -> dict[str, str]:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "deepseek":
        return {
            "provider": "deepseek",
            "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
            "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        }
    return {
        "provider": "openai",
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com"),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    }


def list_llm_models(*, api_key: str, base_url: str) -> list[str]:
    if not api_key:
        return []

    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    return sorted(
        item["id"] for item in data.get("data", []) if isinstance(item.get("id"), str)
    )


def generate_llm_daily_report(
    prompt: str,
    *,
    provider: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
) -> LLMResponse:
    config = get_llm_config()
    active_api_key = api_key or config["api_key"]
    active_base_url = base_url or config["base_url"]
    active_model = model or config["model"]

    if not active_api_key:
        return LLMResponse(error="未配置 API key，已使用规则日报。")

    payload = {
        "model": active_model,
        "messages": [
            {
                "role": "system",
                "content": "你是农业技术员日报助手，请基于给定报告和证据生成简洁、可执行的中文管理建议。",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        f"{active_base_url.rstrip('/')}/v1/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {active_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return LLMResponse(error=f"LLM HTTP 错误：{exc.code}")
    except (urllib.error.URLError, TimeoutError) as exc:
        return LLMResponse(error=f"LLM 网络错误：{exc}")
    except json.JSONDecodeError:
        return LLMResponse(error="LLM 响应不是合法 JSON。")

    try:
        content = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError):
        return LLMResponse(error="LLM 响应格式不符合 chat/completions。")
    return LLMResponse(content=content)
