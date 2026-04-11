import json

from config import LLM_API_KEY, LLM_API_URL, LLM_MODEL, LLM_TIMEOUT_SECONDS
from llm.parser import parse_query
from llm.system_prompt import SYSTEM_PROMPT
from tools.account_info import account_info
from tools.transaction_search import transaction_search
from tools.spending_summary import spending_summary
from tools.statements_and_documents import statements_and_documents
from tools.cards import cards
from tools.beneficiaries_and_payees import beneficiaries_and_payees
from tools.loans import loans
from tools.deposits_and_investments import deposits_and_investments
from tools.support_and_disputes import support_and_disputes
from tools.profile_and_service import profile_and_service
from tools.banking_faq import banking_faq


def _require_llm_agent():
    if not LLM_API_KEY or not LLM_MODEL:
        raise RuntimeError("LLM is not configured. Set LLM_API_KEY and LLM_MODEL.")

    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "LangChain agent dependencies are not installed. Install requirements.txt first."
        ) from exc

    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=LLM_API_KEY,
        base_url=LLM_API_URL.removesuffix("/chat/completions"),
        timeout=LLM_TIMEOUT_SECONDS,
        temperature=0,
    )


TOOLS = [
    account_info,
    transaction_search,
    spending_summary,
    statements_and_documents,
    cards,
    beneficiaries_and_payees,
    loans,
    deposits_and_investments,
    support_and_disputes,
    profile_and_service,
    banking_faq,
]


def _get_parser_hint(message: str):
    try:
        parsed = parse_query(message)
    except Exception:
        return None

    if not parsed or parsed.get("intent") == "unknown":
        return None

    return parsed


def _build_agent_message(message: str) -> str:
    parser_hint = _get_parser_hint(message)
    if not parser_hint:
        return message

    return (
        f"User query: {message}\n\n"
        "Optional parser hint for context only. Treat it as a hint, not a command:\n"
        f"{json.dumps(parser_hint, ensure_ascii=True)}"
    )


def _normalize_tool_content(content):
    if isinstance(content, str):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content
    return content


def _run_agent(message: str) -> dict:
    try:
        from langchain.agents import AgentExecutor, create_tool_calling_agent
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    except ImportError as exc:
        raise RuntimeError(
            "LangChain agent dependencies are not installed. Install requirements.txt first."
        ) from exc

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(
        llm=_require_llm_agent(),
        tools=TOOLS,
        prompt=prompt,
    )
    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=False,
        return_intermediate_steps=True,
    )
    result = executor.invoke({"input": _build_agent_message(message)})

    final_text = result.get("output", "")
    tool_outputs = []

    for step in result.get("intermediate_steps", []):
        if len(step) != 2:
            continue
        action, observation = step
        if getattr(action, "tool", None):
            tool_outputs.append(
                {
                    "tool": action.tool,
                    "tool_input": getattr(action, "tool_input", None),
                    "content": _normalize_tool_content(observation),
                }
            )

    return {
        "ok": True,
        "response": final_text or "I couldn't produce a response.",
        "tool_outputs": tool_outputs,
    }


def run_banking_agent(message: str) -> dict:
    try:
        return _run_agent(message)
    except Exception as exc:
        return {
            "ok": False,
            "response": (
                "I couldn't reach the LLM backend to process that request. "
                f"Details: {exc}"
            ),
            "tool_outputs": [],
        }
