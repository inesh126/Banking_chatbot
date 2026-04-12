from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.query_helpers import detect_min_amount, detect_month, detect_transaction_type, extract_keywords
from utils.data_loader import get_transactions

@tool
def transaction_search(query: str) -> str:
    """Use for user-specific transaction lookups by month, merchant, category, credit or debit type, or minimum amount; input is a natural-language transaction query and the tool returns matching transactions plus the detected filters."""
    try:
        month = detect_month(query)
        txn_type = detect_transaction_type(query)
        min_amount = detect_min_amount(query)
        keywords = extract_keywords(query)
        base_results = get_transactions(month=month, min_amount=min_amount, txn_type=txn_type)

        matches = []
        for txn in base_results:
            searchable_values = {
                txn["description"].lower(),
                txn["category"].lower(),
                txn["type"].lower(),
            }
            if searchable_values & keywords or not keywords - {"show", "me", "my", "transactions", "transaction", "did", "i", "pay"}:
                matches.append(txn)

        return build_tool_result(
            data={
                "transactions": matches,
                "count": len(matches),
                "filters": {
                    "month": month,
                    "txn_type": txn_type,
                    "min_amount": min_amount,
                },
            },
            metadata={"tool": "transaction_search", "query": query},
            message=(
                "No matching transactions were found in the demo dataset."
                if not matches else
                "Matching transactions retrieved from the demo dataset."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to search transactions: {exc}",
            metadata={"tool": "transaction_search", "query": query},
        )
