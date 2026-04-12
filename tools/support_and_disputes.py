from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_support_tickets

@tool
def support_and_disputes(query: str) -> str:
    """Use for support-ticket, dispute-status, and unknown-transaction support questions; input is a natural-language support question and the tool returns structured support ticket records for the user."""
    try:
        tickets = get_support_tickets()
        return build_tool_result(
            data={"support_tickets": tickets, "count": len(tickets)},
            metadata={"tool": "support_and_disputes", "query": query},
            message=(
                "No support tickets are available in the demo dataset."
                if not tickets else
                "Support ticket records retrieved from the demo dataset."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load support information: {exc}",
            metadata={"tool": "support_and_disputes", "query": query},
        )
