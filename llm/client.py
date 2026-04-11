import json

import requests

from config import LLM_API_KEY, LLM_API_URL, LLM_MODEL, LLM_TIMEOUT_SECONDS


def llm_is_configured():
    return bool(LLM_API_KEY and LLM_MODEL)


def _extract_content(payload):
    choices = payload.get("choices", [])
    if not choices:
        raise ValueError("LLM response did not include any choices.")

    message = choices[0].get("message", {})
    content = message.get("content")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for item in content:
            if item.get("type") == "text" and item.get("text"):
                text_parts.append(item["text"])
        if text_parts:
            return "\n".join(text_parts)

    raise ValueError("LLM response did not include text content.")


def call_llm_json(system_prompt: str, user_prompt: str):
    if not llm_is_configured():
        raise RuntimeError("LLM is not configured. Set LLM_API_KEY and LLM_MODEL.")

    response = requests.post(
        LLM_API_URL,
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        },
        timeout=LLM_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    content = _extract_content(response.json())
    return json.loads(content)


def call_llm_text(system_prompt: str, user_prompt: str):
    if not llm_is_configured():
        raise RuntimeError("LLM is not configured. Set LLM_API_KEY and LLM_MODEL.")

    response = requests.post(
        LLM_API_URL,
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        },
        timeout=LLM_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    return _extract_content(response.json())
