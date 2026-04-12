from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.data_loader import get_beneficiaries

@tool
def beneficiaries_and_payees(query: str) -> str:
    """Use for saved beneficiary or payee lookup questions; input is a natural-language question about existing beneficiaries and the tool returns the stored beneficiary list and count."""
    try:
        beneficiaries = get_beneficiaries()
        return build_tool_result(
            data={"beneficiaries": beneficiaries, "count": len(beneficiaries)},
            metadata={"tool": "beneficiaries_and_payees", "query": query},
            message=(
                "No saved beneficiaries are available in the demo dataset."
                if not beneficiaries else
                "Beneficiary records retrieved from the demo dataset."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to load beneficiary information: {exc}",
            metadata={"tool": "beneficiaries_and_payees", "query": query},
        )
