from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.query_helpers import detect_month, extract_keywords
from utils.data_loader import get_transactions

@tool
def spending_summary(query: str) -> str:
    """Use for debit-spending totals, monthly spend analysis, and category-level spend summaries; input is a natural-language spending question and the tool returns total_spent, matched category or month, and the underlying debit transactions."""
    try:
        month = detect_month(query)
        keywords = extract_keywords(query)
        debits = get_transactions(month=month, txn_type="debit")
        categories = sorted({txn["category"] for txn in debits})
        matched_category = next((category for category in categories if category in keywords), None)

        relevant = [txn for txn in debits if txn["category"] == matched_category] if matched_category else debits
        total_spent = sum(abs(txn["amount"]) for txn in relevant)

        return build_tool_result(
            data={
                "total_spent": total_spent,
                "currency": "INR",
                "month": month,
                "category": matched_category,
                "transactions": relevant,
            },
            metadata={"tool": "spending_summary", "query": query},
            message=(
                "No debit transactions were found for the requested spending view."
                if not relevant else
                "Spending summary calculated from confirmed debit transactions."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to build spending summary: {exc}",
            metadata={"tool": "spending_summary", "query": query},
        )
