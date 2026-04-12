from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_loans

@tool
def loans(query: str) -> str:
    """Use for loan-specific account facts such as outstanding amount, EMI, and next due date; input is a natural-language loan question and the tool returns structured loan records for the user."""
    try:
        loan_data = get_loans()
        return build_tool_result(
            data={"loans": loan_data, "count": len(loan_data)},
            metadata={"tool": "loans", "query": query},
            message=(
                "No loan records are available in the demo dataset."
                if not loan_data else
                "Loan records retrieved from the demo dataset."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load loan information: {exc}",
            metadata={"tool": "loans", "query": query},
        )
