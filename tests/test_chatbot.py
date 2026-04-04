import unittest

from backend.services import handle_query
from llm.parser import parse_query
from tools.transaction import get_transactions


class ParserTests(unittest.TestCase):
    def test_balance_intent(self):
        parsed = parse_query("What is my balance?")
        self.assertEqual(parsed["intent"], "get_balance")

    def test_transaction_filters_are_extracted(self):
        parsed = parse_query("Show my debit transactions in March above 1000")
        self.assertEqual(parsed["intent"], "get_transactions")
        self.assertEqual(parsed["filters"]["month"], 3)
        self.assertEqual(parsed["filters"]["txn_type"], "debit")
        self.assertEqual(parsed["filters"]["min_amount"], 1000)

    def test_statement_requires_month_when_missing(self):
        parsed = parse_query("Give me my statement")
        self.assertEqual(parsed, {"intent": "get_statement", "month": None})


class ToolTests(unittest.TestCase):
    def test_get_transactions_filters_correctly(self):
        results = get_transactions(month=3, min_amount=2000, txn_type="debit")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["description"], "Amazon")

    def test_unknown_queries_fail_cleanly(self):
        result = handle_query({"intent": "unknown"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["intent"], "unknown")


if __name__ == "__main__":
    unittest.main()
