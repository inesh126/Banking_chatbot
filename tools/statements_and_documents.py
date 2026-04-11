from calendar import month_name

from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.query_helpers import detect_month
from utils.data_loader import get_transactions

@tool
def statements_and_documents(query: str) -> str:
    """Use for monthly statements, transaction ledgers, and document-style transaction exports."""
    try:
        month = detect_month(query)
        transactions = get_transactions(month=month)
        statement_period = month_name[month] if month else "All transactions"

        return build_tool_result(
            data={
                "statement_period": statement_period,
                "transaction_count": len(transactions),
                "transactions": transactions,
            },
            metadata={"tool": "statements_and_documents", "query": query, "month": month},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to build statement data: {exc}",
            metadata={"tool": "statements_and_documents", "query": query},
        )
