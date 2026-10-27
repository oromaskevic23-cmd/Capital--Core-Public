"""IMPERIAL Core paper-only order proposal gate. No broker or network imports."""
from decimal import Decimal, InvalidOperation

def evaluate(order, *, equity, cash, max_order_pct=Decimal("0.10"), min_cash_pct=Decimal("0.10")):
    """Fail closed; this does not authorize any real or paper broker execution."""
    deny = lambda reason: {"status": "BLOCK", "reason": reason, "execution_authorized": False}
    if not isinstance(order, dict) or set(order) != {"symbol", "side", "notional_usd"}:
        return deny("invalid order schema")
    symbol = order["symbol"]
    if not isinstance(symbol, str) or not (1 <= len(symbol) <= 5 and symbol.isascii() and symbol.isalpha() and symbol.isupper()):
        return deny("invalid symbol")
    if order["side"] != "buy":
        return deny("only simulated long buys supported")
    try:
        if isinstance(order["notional_usd"], (bool, float)) or isinstance(equity, (bool, float)) or isinstance(cash, (bool, float)):
            return deny("decimal strings required")
        amount = Decimal(str(order["notional_usd"]))
        total = Decimal(str(equity))
        available = Decimal(str(cash))
        if not all(x.is_finite() for x in (amount, total, available)):
            return deny("non-finite amount")
    except (InvalidOperation, TypeError, ValueError):
        return deny("invalid monetary amount")
    if amount <= 0 or total <= 0 or available < 0 or available > total:
        return deny("invalid balance")
    if amount > total * max_order_pct:
        return deny("max order cap exceeded")
    if available - amount < total * min_cash_pct:
        return deny("cash buffer violated")
    return {"status": "PAPER_ELIGIBLE", "reason": "synthetic risk checks passed", "execution_authorized": False}
