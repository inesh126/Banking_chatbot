import re
from datetime import datetime


MONTH_NAMES = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def _extract_month(query: str):
    for month_name, month_number in MONTH_NAMES.items():
        if month_name in query:
            return month_number

    date_match = re.search(r"\b(20\d{2})-(\d{2})-\d{2}\b", query)
    if date_match:
        return int(date_match.group(2))

    current_date = datetime.now()
    if "this month" in query or "current month" in query:
        return current_date.month
    if "last month" in query:
        return 12 if current_date.month == 1 else current_date.month - 1

    return None


def _extract_transaction_type(query: str):
    if any(keyword in query for keyword in ("debit", "spent", "spend", "withdraw", "expense")):
        return "debit"
    if any(keyword in query for keyword in ("credit", "credited", "received", "salary", "deposit")):
        return "credit"
    return None


def _extract_min_amount(query: str):
    amount_match = re.search(
        r"(?:above|over|greater than|more than|at least|min(?:imum)? of)\s*(?:rs\.?|inr|rupees)?\s*(\d+)",
        query,
    )
    if not amount_match:
        amount_match = re.search(r"(?:rs\.?|inr|rupees)\s*(\d+)", query)

    return int(amount_match.group(1)) if amount_match else None


def parse_query(query: str):
    normalized_query = query.lower().strip()
    month = _extract_month(normalized_query)
    txn_type = _extract_transaction_type(normalized_query)
    min_amount = _extract_min_amount(normalized_query)

    if "balance" in normalized_query:
        return {"intent": "get_balance"}

    if "statement" in normalized_query:
        return {"intent": "get_statement", "month": month}

    if any(keyword in normalized_query for keyword in ("transactions", "transaction", "spending", "spent", "history")):
        filters = {}
        if month is not None:
            filters["month"] = month
        if txn_type is not None:
            filters["txn_type"] = txn_type
        if min_amount is not None:
            filters["min_amount"] = min_amount

        return {"intent": "get_transactions", "filters": filters}

    return {"intent": "unknown"}
