from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_cards

@tool
def cards(query: str) -> str:
    """Use for debit card and credit card status, card limits, last four digits, and due information."""
    try:
        cards_data = get_cards()
        return build_tool_result(
            data={"cards": cards_data, "count": len(cards_data)},
            metadata={"tool": "cards", "query": query},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load card information: {exc}",
            metadata={"tool": "cards", "query": query},
        )
