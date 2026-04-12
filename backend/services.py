from backend.guardrails import build_input_guardrail_response, normalize_user_message
from llm.banking_agent import run_banking_agent


def handle_query(message: str):
    normalized_message = normalize_user_message(message)
    guardrail_response = build_input_guardrail_response(normalized_message)
    if guardrail_response:
        return guardrail_response

    return run_banking_agent(normalized_message)
