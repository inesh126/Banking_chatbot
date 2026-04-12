import logging
import re


LOGGER = logging.getLogger(__name__)

UNCERTAIN_PHRASES = [
    r"\bi think\b",
    r"\bmaybe\b",
    r"\bprobably\b",
    r"\bi guess\b",
    r"\bmight be\b",
    r"\bcould be\b",
]

DATA_GROUNDED_TERMS = [
    "balance",
    "transaction",
    "statement",
    "card",
    "loan",
    "beneficiary",
    "deposit",
    "support",
    "kyc",
    "profile",
]

LIMITATION_PHRASES = [
    "cannot",
    "can't",
    "not supported",
    "do not have access",
    "unable to",
    "could not",
]


def validate_agent_response(response: str, tool_outputs):
    cleaned = " ".join((response or "").split())
    if not cleaned:
        LOGGER.info("Output guardrail triggered: empty response")
        return (
            "I could not produce a grounded answer from the available banking tools in this demo system."
        )

    lowered = cleaned.lower()
    if any(re.search(pattern, lowered) for pattern in UNCERTAIN_PHRASES):
        LOGGER.info("Output guardrail triggered: uncertain phrasing")
        return (
            "I can only answer using confirmed results from the available banking tools in this demo system."
        )

    if (
        not tool_outputs and
        any(term in lowered for term in DATA_GROUNDED_TERMS) and
        not any(phrase in lowered for phrase in LIMITATION_PHRASES)
    ):
        LOGGER.info("Output guardrail triggered: data-like answer without tool outputs")
        return (
            "I can only answer banking-data questions when I can confirm them with the available tools in this demo system."
        )

    return cleaned
