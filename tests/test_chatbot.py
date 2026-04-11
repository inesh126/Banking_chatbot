import json
import unittest
from unittest.mock import patch

from backend.services import handle_query
from llm.banking_agent import spending_summary, statements_and_documents


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


class BankingServiceTests(unittest.TestCase):
    @patch("backend.services.run_banking_agent", return_value={"ok": True, "response": "Your current account balance is 45230."})
    def test_handle_query_uses_banking_agent(self, mock_run_banking_agent):
        result = handle_query("What is my balance?")
        mock_run_banking_agent.assert_called_once_with("What is my balance?")
        self.assertTrue(result["ok"])
        self.assertEqual(result["response"], "Your current account balance is 45230.")


if __name__ == "__main__":
    unittest.main()
