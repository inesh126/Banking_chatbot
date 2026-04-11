from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_loans

@tool
def loans(query: str) -> str:
    """Use for loan balances, EMI amounts, outstanding amounts, and next due dates."""
    try:
        loan_data = get_loans()
        return build_tool_result(
            data={"loans": loan_data, "count": len(loan_data)},
            metadata={"tool": "loans", "query": query},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load loan information: {exc}",
            metadata={"tool": "loans", "query": query},
        )
