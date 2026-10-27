import tempfile
import unittest
from pathlib import Path
from audit_store import Ledger

class AuditTests(unittest.TestCase):
    def test_persistent_hash_chain(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/"audit.db")
            a=Ledger(path)
            a.append({"component":"HANTER","outcome":"STAGING"})
            a.db.close()
            b=Ledger(path)
            self.assertTrue(b.verify())
            self.assertEqual(b.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0],1)
            b.db.close()

    def test_tamper_detection(self):
        with tempfile.TemporaryDirectory() as folder:
            a=Ledger(str(Path(folder)/"audit.db"))
            a.append({"component":"GUARDIAN","outcome":"DENIED"})
            a.db.execute("UPDATE audit SET event='tampered' WHERE seq=1")
            a.db.commit()
            self.assertFalse(a.verify())
            with self.assertRaises(ValueError):
                a.append({"component":"MORGAN","outcome":"BLOCK"})
            a.db.close()

if __name__=="__main__":
    unittest.main()
