import unittest
from enterprise_bridge import run,verify
T={"task_id":"SIM-001","symbol":"AAPL","notional_usd":"100.00","equity_usd":"5000.00","cash_usd":"5000.00"}
class IntegrationTests(unittest.TestCase):
    def test_route(self):
        r=run(T)
        self.assertEqual(r["status"],"PAPER_ELIGIBLE")
        self.assertFalse(r["execution_authorized"])
        self.assertTrue(verify(r["ledger"]))
        self.assertEqual([x["component"] for x in r["ledger"]],["HANTER","VELION ⚡️","MORGAN","GUARDIAN"])
    def test_kill(self):
        self.assertEqual(run(T,kill_switch=True)["status"],"BLOCK")
    def test_over_cap(self):
        self.assertEqual(run({**T,"notional_usd":"600"})["status"],"BLOCK")
    def test_schema(self):
        self.assertEqual(run({**T,"broker":"live"})["status"],"BLOCK")
    def test_tamper(self):
        r=run(T)
        r["ledger"][1]["outcome"]="LIVE"
        self.assertFalse(verify(r["ledger"]))
    def test_empty(self):
        self.assertFalse(verify([]))
    def test_nan(self):
        self.assertEqual(run({**T,"notional_usd":"NaN"})["status"],"BLOCK")
    def test_symbol(self):
        self.assertEqual(run({**T,"symbol":"BTC/USD"})["status"],"BLOCK")
    def test_bad_id(self):
        self.assertEqual(run({**T,"task_id":""})["status"],"BLOCK")
    def test_cash(self):
        self.assertEqual(run({**T,"cash_usd":"6000"})["status"],"BLOCK")
if __name__=="__main__":unittest.main()
