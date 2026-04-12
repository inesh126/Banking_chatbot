from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_profile

@tool
def profile_and_service(query: str) -> str:
    """Use for profile and service facts such as KYC status, branch, linked ATM card state, and phone number; input is a natural-language profile question and the tool returns structured profile data."""
    try:
        profile = get_profile()
        if not profile:
            return build_tool_result(
                data={},
                metadata={"tool": "profile_and_service", "query": query},
                message="No profile data is available in the demo dataset.",
            )

        return build_tool_result(
            data=profile,
            metadata={"tool": "profile_and_service", "query": query},
            message="Profile data retrieved from the demo dataset.",
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load profile information: {exc}",
            metadata={"tool": "profile_and_service", "query": query},
        )
