import re
from calendar import month_name


MONTH_LOOKUP = {
    month.lower(): index
    for index, month in enumerate(month_name)
    if month
}


def detect_month(query: str):
    query_lower = query.lower()
    for name, index in MONTH_LOOKUP.items():
        if name in query_lower:
            return index
    return None


def detect_transaction_type(query: str):
    query_lower = query.lower()
    if any(word in query_lower for word in ["debit", "spent", "spend", "expense", "withdraw"]):
        return "debit"
    if any(word in query_lower for word in ["credit", "salary", "deposit", "received", "income", "refund"]):
        return "credit"
    return None


def detect_min_amount(query: str):
    patterns = [
        r"(?:above|over|greater than|more than|minimum|min)\s+(\d+)",
        r"(\d+)\s*(?:and above|or more|\+)",
    ]
    query_lower = query.lower()
    for pattern in patterns:
        match = re.search(pattern, query_lower)
        if match:
            return int(match.group(1))
    return None


def extract_keywords(query: str):
    return {token.lower() for token in re.findall(r"[a-zA-Z]+", query)}
