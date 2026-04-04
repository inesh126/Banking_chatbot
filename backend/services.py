from tools.transaction import get_transactions
from tools.balance import get_balance
from tools.statement import generate_statement


def handle_query(parsed):
    intent = parsed["intent"]

    if intent == "get_balance":
        return {"ok": True, "intent": intent, "response": get_balance()}

    if intent == "get_transactions":
        filters = parsed.get("filters", {})
        transactions = get_transactions(**filters)
        return {
            "ok": True,
            "intent": intent,
            "filters": filters,
            "count": len(transactions),
            "response": transactions,
        }

    if intent == "get_statement":
        month = parsed.get("month")
        if month is None:
            return {
                "ok": False,
                "intent": intent,
                "response": "Please specify which month you want the statement for.",
            }
        return {"ok": True, "intent": intent, "response": generate_statement(month)}

    return {
        "ok": False,
        "intent": "unknown",
        "response": "Sorry, I didn't understand. Try asking about balance, transactions, or a monthly statement.",
    }
