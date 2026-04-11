from llm.client import call_llm_json, llm_is_configured
from llm.prompt import EXTRACTION_SYSTEM_PROMPT, build_extraction_user_prompt


def _sanitize_month(month):
    if month is None:
        return None

    if isinstance(month, int) and 1 <= month <= 12:
        return month

    if isinstance(month, str) and month.isdigit():
        month = int(month)
        if 1 <= month <= 12:
            return month

    return None


def _sanitize_min_amount(min_amount):
    if min_amount is None:
        return None

    if isinstance(min_amount, int) and min_amount >= 0:
        return min_amount

    if isinstance(min_amount, str) and min_amount.isdigit():
        return int(min_amount)

    return None


def _sanitize_llm_result(parsed):
    if not isinstance(parsed, dict):
        return {"intent": "unknown"}

    intent = parsed.get("intent")
    if intent == "get_balance":
        return {"intent": "get_balance"}

    if intent == "get_statement":
        return {"intent": "get_statement", "month": _sanitize_month(parsed.get("month"))}

    if intent == "get_transactions":
        raw_filters = parsed.get("filters", {})
        if not isinstance(raw_filters, dict):
            raw_filters = {}

        filters = {}
        month = _sanitize_month(raw_filters.get("month"))
        txn_type = raw_filters.get("txn_type")
        min_amount = _sanitize_min_amount(raw_filters.get("min_amount"))

        if month is not None:
            filters["month"] = month
        if txn_type in {"debit", "credit"}:
            filters["txn_type"] = txn_type
        if min_amount is not None:
            filters["min_amount"] = min_amount

        return {"intent": "get_transactions", "filters": filters}

    return {"intent": "unknown"}


def _history_to_text(history):
    if not history:
        return None

    lines = []
    for entry in history:
        role = entry.get("role", "user")
        label = "User" if role == "user" else "Assistant"
        lines.append(f"{label}: {entry.get('content', '')}")
    return "\n".join(lines)


def _require_llm_parse_query(query: str, history=None):
    if not llm_is_configured():
        raise RuntimeError("LLM is not configured. Set LLM_API_KEY and LLM_MODEL.")

    history_text = _history_to_text(history)
    parsed = call_llm_json(EXTRACTION_SYSTEM_PROMPT, build_extraction_user_prompt(query, history_text))
    return _sanitize_llm_result(parsed)


def parse_query(query: str, history=None):
    return _require_llm_parse_query(query, history)
