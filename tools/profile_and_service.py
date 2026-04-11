from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_profile

@tool
def profile_and_service(query: str) -> str:
    """Use for KYC status, branch details, linked ATM card state, and contact profile questions."""
    try:
        profile = get_profile()
        return build_tool_result(
            data=profile,
            metadata={"tool": "profile_and_service", "query": query},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load profile information: {exc}",
            metadata={"tool": "profile_and_service", "query": query},
        )
