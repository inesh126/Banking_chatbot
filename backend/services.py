from llm.banking_agent import run_banking_agent


def handle_query(message: str):
    return run_banking_agent(message)
