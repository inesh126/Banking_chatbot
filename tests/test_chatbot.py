import json
import unittest
from unittest.mock import patch

from backend.services import handle_query
from llm.guardrails import validate_agent_response
from llm.banking_agent import spending_summary, statements_and_documents
from tools.knowledge_base_search import knowledge_base_search


class BankingAgentToolTests(unittest.TestCase):
    def test_spending_summary_returns_total_for_march(self):
        response = json.loads(spending_summary.invoke("How much did I spend in March?"))
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["data"]["total_spent"], 12900)
        self.assertEqual(response["data"]["month"], 3)

    def test_statement_tool_returns_march_statement(self):
        response = json.loads(statements_and_documents.invoke("Give me my March statement"))
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["data"]["statement_period"], "March")
        self.assertEqual(response["data"]["transaction_count"], 6)
        self.assertEqual(response["data"]["transactions"][0]["description"], "Swiggy")

    def test_knowledge_base_search_returns_relevant_chunk(self):
        response = json.loads(knowledge_base_search.invoke("What are your service hours?"))
        self.assertEqual(response["status"], "success")
        self.assertGreaterEqual(response["data"]["count"], 1)
        self.assertTrue(
            any("service" in match["text"].lower() for match in response["data"]["matches"])
        )


class BankingServiceTests(unittest.TestCase):
    @patch("backend.services.run_banking_agent", return_value={"ok": True, "response": "Your current account balance is 46300."})
    def test_handle_query_uses_banking_agent(self, mock_run_banking_agent):
        result = handle_query("What is my balance?")
        mock_run_banking_agent.assert_called_once_with("What is my balance?")
        self.assertTrue(result["ok"])
        self.assertEqual(result["response"], "Your current account balance is 46300.")

    @patch("backend.services.run_banking_agent")
    def test_handle_query_blocks_unsupported_payments(self, mock_run_banking_agent):
        result = handle_query("Please transfer funds to Ria now")
        mock_run_banking_agent.assert_not_called()
        self.assertFalse(result["ok"])
        self.assertIn("cannot perform payments or transfers", result["response"].lower())


class GuardrailTests(unittest.TestCase):
    def test_output_guardrail_replaces_uncertain_response(self):
        validated = validate_agent_response("I think your balance might be 46300.", [])
        self.assertEqual(
            validated,
            "I can only answer using confirmed results from the available banking tools in this demo system.",
        )


if __name__ == "__main__":
    unittest.main()
