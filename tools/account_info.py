from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_account_snapshot

@tool
def account_info(query: str) -> str:
    """Use for account balance, account number, currency, and account type questions."""
    try:
        snapshot = get_account_snapshot()
        return build_tool_result(
            data=snapshot,
            metadata={"tool": "account_info", "query": query},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load account information: {exc}",
            metadata={"tool": "account_info", "query": query},
        )
