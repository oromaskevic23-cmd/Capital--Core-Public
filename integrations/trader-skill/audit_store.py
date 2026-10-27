"""Local staging audit ledger. Append-only at application layer; not a production WORM store."""
import hashlib
import json
import sqlite3

class Ledger:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.db.execute("CREATE TABLE IF NOT EXISTS audit (seq INTEGER PRIMARY KEY, event TEXT NOT NULL, prev TEXT NOT NULL, digest TEXT NOT NULL)")
        self.db.commit()

    def verify(self):
        prev = "0" * 64
        for n, event, previous, digest in self.db.execute("SELECT seq,event,prev,digest FROM audit ORDER BY seq"):
            expected = hashlib.sha256((str(n) + "|" + event + "|" + prev).encode()).hexdigest()
            if previous != prev or expected != digest:
                return False
            prev = digest
        return True

    def append(self, event):
        if not self.verify():
            raise ValueError("audit integrity failure")
        payload = json.dumps(event, sort_keys=True, separators=(",", ":"))
        last = self.db.execute("SELECT seq,digest FROM audit ORDER BY seq DESC LIMIT 1").fetchone()
        n, prev = (last[0] + 1, last[1]) if last else (1, "0" * 64)
        digest = hashlib.sha256((str(n) + "|" + payload + "|" + prev).encode()).hexdigest()
        with self.db:
            self.db.execute("INSERT INTO audit VALUES (?,?,?,?)", (n, payload, prev, digest))
        return digest
