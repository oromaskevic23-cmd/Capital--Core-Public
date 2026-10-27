import unittest
from paper_gate import evaluate

class PaperGateTests(unittest.TestCase):
    def test_paper_proposal_never_authorized(self):
        r=evaluate({"symbol":"AAPL","side":"buy","notional_usd":"100"},equity="5000",cash="5000")
        self.assertEqual(r["status"],"PAPER_ELIGIBLE")
        self.assertFalse(r["execution_authorized"])
    def test_excessive_size(self):
        self.assertEqual(evaluate({"symbol":"AAPL","side":"buy","notional_usd":"600"},equity="5000",cash="5000")["status"],"BLOCK")
    def test_cash_buffer(self):
        self.assertEqual(evaluate({"symbol":"AAPL","side":"buy","notional_usd":"100"},equity="5000",cash="550")["status"],"BLOCK")
    def test_reject_sell(self):
        self.assertEqual(evaluate({"symbol":"AAPL","side":"sell","notional_usd":"100"},equity="5000",cash="5000")["status"],"BLOCK")
    def test_reject_float(self):
        self.assertEqual(evaluate({"symbol":"AAPL","side":"buy","notional_usd":100.0},equity="5000",cash="5000")["status"],"BLOCK")
    def test_reject_extra_keys(self):
        self.assertEqual(evaluate({"symbol":"AAPL","side":"buy","notional_usd":"100","broker":"live"},equity="5000",cash="5000")["status"],"BLOCK")

if __name__=="__main__":
    unittest.main()
