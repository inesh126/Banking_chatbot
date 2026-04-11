from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_deposits

@tool
def deposits_and_investments(query: str) -> str:
    """Use for fixed deposits, maturity dates, deposit amounts, and deposit interest rates."""
    try:
        deposits = get_deposits()
        return build_tool_result(
            data={"deposits": deposits, "count": len(deposits)},
            metadata={"tool": "deposits_and_investments", "query": query},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load deposit information: {exc}",
            metadata={"tool": "deposits_and_investments", "query": query},
        )
