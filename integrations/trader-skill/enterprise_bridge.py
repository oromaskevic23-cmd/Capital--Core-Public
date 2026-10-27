"""Offline integration contract: HANTER -> VELION -> MORGAN -> Guardian."""
import hashlib
import json
from decimal import Decimal
from paper_gate import evaluate

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def run(task, *, kill_switch=False):
    ledger=[]
    def event(component,action,outcome):
        row={"seq":len(ledger)+1,"component":component,"action":action,"outcome":outcome,"previous_hash":ledger[-1]["hash"] if ledger else "0"*64}
        row["hash"]=digest(row)
        ledger.append(row)
    if not isinstance(task,dict) or set(task)!={"task_id","symbol","notional_usd","equity_usd","cash_usd"} or not isinstance(task.get("task_id"),str) or not task["task_id"]:
        event("HANTER","validate","BLOCK")
        return {"status":"BLOCK","execution_authorized":False,"ledger":ledger}
    event("HANTER","route","STAGING")
    if kill_switch is not False:
        event("GUARDIAN","kill_switch","BLOCK")
        return {"status":"BLOCK","execution_authorized":False,"ledger":ledger}
    event("VELION ⚡️","proposal","SYNTHETIC_NO_INFERENCE")
    decision=evaluate({"symbol":task["symbol"],"side":"buy","notional_usd":task["notional_usd"]},equity=task["equity_usd"],cash=task["cash_usd"])
    event("MORGAN","risk",decision["status"])
    event("GUARDIAN","execution","DENIED")
    return {"status":decision["status"],"execution_authorized":False,"ledger":ledger}

def verify(ledger):
    prev="0"*64
    for i,row in enumerate(ledger,1):
        if not isinstance(row,dict) or set(row)!={"seq","component","action","outcome","previous_hash","hash"}:
            return False
        if row["seq"]!=i or row["previous_hash"]!=prev or row["hash"]!=digest({k:v for k,v in row.items() if k!="hash"}):
            return False
        prev=row["hash"]
    return bool(ledger)
