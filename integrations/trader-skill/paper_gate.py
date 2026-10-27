"""Offline, fail-closed risk gate for simulated proposals. No order execution."""
from decimal import Decimal, InvalidOperation
import re

_DECIMAL = re.compile(r"^(?:0|[1-9][0-9]*)(?:\.[0-9]{1,2})?$")
_SYMBOL = re.compile(r"^[A-Z]{1,5}$")

def _money(value):
    if not isinstance(value, str) or not _DECIMAL.fullmatch(value):
        raise ValueError("money must be a nonnegative decimal string with <=2 decimals")
    result = Decimal(value)
    if not result.is_finite():
        raise ValueError("nonfinite amount")
    return result

def evaluate(order, *, equity, cash, max_order_pct="0.10", min_cash_pct="0.10", kill_switch=False):
    """Pure decision; PAPER_ELIGIBLE is never an authorization to execute."""
    def deny(reason):
        return {"status": "BLOCK", "reason": reason, "execution_authorized": False}
    if type(kill_switch) is not bool or kill_switch:
        return deny("owner kill switch engaged or invalid")
    if not isinstance(order, dict) or set(order) != {"symbol", "side", "notional_usd"}:
        return deny("invalid order schema")
    if not isinstance(order["symbol"], str) or not _SYMBOL.fullmatch(order["symbol"]):
        return deny("invalid symbol")
    if order["side"] != "buy":
        return deny("only synthetic long buys supported")
    try:
        amount, total, available = (_money(v) for v in (order["notional_usd"], equity, cash))
        cap, reserve = (Decimal(v) for v in (max_order_pct, min_cash_pct))
        if not all(v.is_finite() and Decimal(0) <= v <= Decimal(1) for v in (cap, reserve)):
            return deny("invalid limits")
    except (ValueError, InvalidOperation, TypeError):
        return deny("invalid money or limits")
    if amount <= 0 or total <= 0 or available > total:
        return deny("invalid balance")
    if amount > total * cap:
        return deny("max order cap exceeded")
    if available - amount < total * reserve:
        return deny("cash buffer violated")
    return {"status": "PAPER_ELIGIBLE", "reason": "synthetic checks passed", "execution_authorized": False}
