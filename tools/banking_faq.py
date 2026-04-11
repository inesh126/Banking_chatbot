from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_faq

@tool
def banking_faq(query: str) -> str:
    """Use for service hours, transfer limits, and simple banking FAQ lookups from the demo dataset."""
    try:
        faq = get_faq()
        return build_tool_result(
            data=faq,
            metadata={"tool": "banking_faq", "query": query},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load FAQ information: {exc}",
            metadata={"tool": "banking_faq", "query": query},
        )
