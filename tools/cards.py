from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_cards

@tool
def cards(query: str) -> str:
    """Use for card-related account facts such as debit or credit card status, last four digits, monthly limits, statement due date, and minimum due; input is a natural-language card question and the tool returns structured card records."""
    try:
        cards_data = get_cards()
        return build_tool_result(
            data={"cards": cards_data, "count": len(cards_data)},
            metadata={"tool": "cards", "query": query},
            message=(
                "No card records are available in the demo dataset."
                if not cards_data else
                "Card records retrieved from the demo dataset."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load card information: {exc}",
            metadata={"tool": "cards", "query": query},
        )
