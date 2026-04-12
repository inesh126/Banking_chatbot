from tools.tool_wrapper import build_tool_error, build_tool_result, tool
from utils.knowledge_base import search_knowledge_base


@tool
def knowledge_base_search(query: str) -> str:
    """Use for policy, FAQ, process, and explanatory banking questions that need retrieval rather than user-account data; input is the user's natural-language question and the tool returns the top relevant knowledge chunks with topic labels and similarity scores."""
    try:
        matches = search_knowledge_base(query)
        return build_tool_result(
            data={"matches": matches, "count": len(matches)},
            metadata={"tool": "knowledge_base_search", "query": query},
            message=(
                "No relevant knowledge-base entries were found for that question."
                if not matches else
                "Relevant knowledge-base entries were retrieved."
            ),
        )
    except Exception as exc:
        return build_tool_error(
            f"Unable to search the knowledge base: {exc}",
            metadata={"tool": "knowledge_base_search", "query": query},
        )
