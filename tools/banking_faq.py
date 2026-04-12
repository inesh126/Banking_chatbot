from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_faq

@tool
def banking_faq(query: str) -> str:
    """Use for lightweight FAQ facts already present in the account dataset, such as service hours or transfer limit values; input is a natural-language FAQ question and the tool returns structured FAQ fields."""
    try:
        faq = get_faq()
        if not faq:
            return build_tool_result(
                data={},
                metadata={"tool": "banking_faq", "query": query},
                message="No FAQ entries are available in the demo dataset.",
            )

        return build_tool_result(
            data=faq,
            metadata={"tool": "banking_faq", "query": query},
            message="FAQ fields retrieved from the demo dataset.",
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load FAQ information: {exc}",
            metadata={"tool": "banking_faq", "query": query},
        )
