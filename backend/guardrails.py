import logging
import re


LOGGER = logging.getLogger(__name__)

UNSUPPORTED_ACTION_PATTERNS = [
    r"\bsend money\b",
    r"\btransfer funds?\b",
    r"\bmake (?:a )?payment\b",
    r"\bpay (?:someone|someone else|a person|a bill|my bill|now)\b",
    r"\bwire transfer\b",
    r"\bupi\b",
    r"\bneft\b",
    r"\bimps\b",
    r"\brtgs\b",
]


def normalize_user_message(message: str) -> str:
    return " ".join((message or "").strip().split())


def detect_unsupported_action(message: str):
    normalized = normalize_user_message(message).lower()
    if not normalized:
        return {"kind": "empty", "match": None}

    for pattern in UNSUPPORTED_ACTION_PATTERNS:
        if re.search(pattern, normalized):
            return {"kind": "unsupported_action", "match": pattern}

    return None


def build_input_guardrail_response(message: str):
    trigger = detect_unsupported_action(message)
    if not trigger:
        return None

    if trigger["kind"] == "empty":
        LOGGER.info("Input guardrail triggered: empty message")
        return {
            "ok": False,
            "response": "Please enter a banking question to continue.",
            "tool_outputs": [],
            "guardrail": {
                "layer": "input",
                "kind": "empty_message",
            },
        }

    LOGGER.info("Input guardrail triggered: unsupported action pattern=%s", trigger["match"])
    return {
        "ok": False,
        "response": (
            "I cannot perform payments or transfers in this demo system. "
            "I can still help with balances, transactions, statements, cards, loans, profile details, and FAQs."
        ),
        "tool_outputs": [],
        "guardrail": {
            "layer": "input",
            "kind": "unsupported_action",
        },
    }
