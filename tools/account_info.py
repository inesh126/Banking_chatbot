from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_account_snapshot

@tool
def account_info(query: str) -> str:
    """Use for user-specific account facts such as balance, account number, account type, and currency; input is the user's natural-language question and the tool returns a structured account snapshot JSON payload."""
    try:
        snapshot = get_account_snapshot()
        if not snapshot or snapshot.get("balance") is None:
            return build_tool_result(
                data={"account": snapshot or {}},
                metadata={"tool": "account_info", "query": query},
                message="No account information is available in the demo dataset.",
            )

        return build_tool_result(
            data=snapshot,
            metadata={"tool": "account_info", "query": query},
            message="Account information retrieved from the demo dataset.",
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load account information: {exc}",
            metadata={"tool": "account_info", "query": query},
        )
