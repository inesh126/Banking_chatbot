from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_deposits

@tool
def deposits_and_investments(query: str) -> str:
    """Use for fixed-deposit and deposit-product questions such as maturity date, amount, and interest rate; input is a natural-language deposit question and the tool returns structured deposit records."""
    try:
        deposits = get_deposits()
        return build_tool_result(
            data={"deposits": deposits, "count": len(deposits)},
            metadata={"tool": "deposits_and_investments", "query": query},
            message=(
                "No deposit records are available in the demo dataset."
                if not deposits else
                "Deposit records retrieved from the demo dataset."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load deposit information: {exc}",
            metadata={"tool": "deposits_and_investments", "query": query},
        )
