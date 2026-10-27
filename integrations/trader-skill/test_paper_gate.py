import unittest
from paper_gate import evaluate

ORDER = {"symbol": "AAPL", "side": "buy", "notional_usd": "100.00"}

def check(order=None, **kwargs):
    return evaluate(ORDER if order is None else order, equity="5000.00", cash="5000.00", **kwargs)

class GateTests(unittest.TestCase):
    def test_eligible_never_authorized(self):
        self.assertEqual(check()["status"], "PAPER_ELIGIBLE")
        self.assertFalse(check()["execution_authorized"])
    def test_cap(self):
        self.assertEqual(check({**ORDER,"notional_usd":"501.00"})["status"], "BLOCK")
    def test_cash_buffer(self):
        self.assertEqual(evaluate(ORDER,equity="5000.00",cash="550.00")["status"], "BLOCK")
    def test_kill_switch(self):
        self.assertEqual(check(kill_switch=True)["status"], "BLOCK")
    def test_invalid_kill_switch(self):
        self.assertEqual(check(kill_switch="false")["status"], "BLOCK")
    def test_broker_field(self):
        self.assertEqual(check({**ORDER,"broker":"live"})["status"], "BLOCK")
    def test_sell(self):
        self.assertEqual(check({**ORDER,"side":"sell"})["status"], "BLOCK")
    def test_bad_symbol(self):
        self.assertEqual(check({**ORDER,"symbol":"AAPL;rm"})["status"], "BLOCK")
    def test_float(self):
        self.assertEqual(check({**ORDER,"notional_usd":100.0})["status"], "BLOCK")
    def test_nan(self):
        self.assertEqual(check({**ORDER,"notional_usd":"NaN"})["status"], "BLOCK")
    def test_negative(self):
        self.assertEqual(check({**ORDER,"notional_usd":"-1"})["status"], "BLOCK")
    def test_precision(self):
        self.assertEqual(check({**ORDER,"notional_usd":"1.001"})["status"], "BLOCK")
    def test_invalid_limits(self):
        self.assertEqual(check(max_order_pct="NaN")["status"], "BLOCK")
    def test_zero_equity(self):
        self.assertEqual(evaluate(ORDER,equity="0",cash="0")["status"], "BLOCK")
    def test_invalid_cash(self):
        self.assertEqual(evaluate(ORDER,equity="5000",cash="6000")["status"], "BLOCK")

if __name__ == "__main__":
    unittest.main()
