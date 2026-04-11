from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_beneficiaries

@tool
def beneficiaries_and_payees(query: str) -> str:
    """Use for beneficiary and payee listing questions, especially existing saved beneficiaries."""
    try:
        beneficiaries = get_beneficiaries()
        return build_tool_result(
            data={"beneficiaries": beneficiaries, "count": len(beneficiaries)},
            metadata={"tool": "beneficiaries_and_payees", "query": query},
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load beneficiary information: {exc}",
            metadata={"tool": "beneficiaries_and_payees", "query": query},
        )
