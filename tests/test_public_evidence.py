"""Negative-path tests for public milestone evidence. No network."""
import copy
import json
from pathlib import Path
import unittest
from tools.verify_milestones import static_errors, live_errors

DATA = json.loads((Path(__file__).resolve().parents[1] /
                   "evidence" / "milestones.json").read_text())["milestones"]


def fake_api(record, overrides=None):
    b = "/repos/oromaskevic23-cmd/" + record["repository_name"]
    n = record["pull_request"].split("/")[-1]
    responses = {
        b: {"private": False, "full_name": "oromaskevic23-cmd/" + record["repository_name"]},
        b + "/pulls/" + n: {"state": "open", "merged_at": None,
                             "head": {"sha": record["commit"]}},
        b + "/actions/runs/" + str(record["run_id"]):
            {"id": record["run_id"], "status": "completed", "conclusion": "success",
             "head_sha": record["commit"]},
        b + "/actions/jobs/" + str(record["job_id"]):
            {"id": record["job_id"], "run_id": record["run_id"],
             "status": "completed", "conclusion": "success"},
    }
    responses.update(overrides or {})
    return responses.__getitem__


class PublicEvidenceTests(unittest.TestCase):
    def test_all_four_static_records(self):
        self.assertEqual(len(DATA), 4)
        for record in DATA:
            with self.subTest(project=record["project"]):
                self.assertEqual(static_errors(record), [])

    def test_all_four_live_metadata_fixtures(self):
        for record in DATA:
            with self.subTest(project=record["project"]):
                self.assertEqual(live_errors(record, fake_api(record)), [])

    def test_reject_deceptive_external_repository(self):
        record = copy.deepcopy(DATA[0])
        record["repository"] = "https://github.com/attacker/HANTER"
        self.assertTrue(static_errors(record))

    def test_reject_cross_project_job_url(self):
        record = copy.deepcopy(DATA[0])
        record["job_url"] = "https://github.com/attacker/repo/actions/runs/1/job/2"
        self.assertTrue(static_errors(record))

    def test_reject_mismatched_test_counts(self):
        record = copy.deepcopy(DATA[0])
        record["tests"]["pass"] -= 1
        self.assertTrue(static_errors(record))

    def test_reject_incorrect_log_hash(self):
        record = copy.deepcopy(DATA[0])
        record["logs_sha256"] = "not-a-digest"
        self.assertTrue(static_errors(record))

    def test_reject_pr_head_mismatch(self):
        record = DATA[0]
        b = "/repos/oromaskevic23-cmd/" + record["repository_name"]
        target = b + "/pulls/3"
        self.assertTrue(live_errors(record, fake_api(record, {
            target: {"state": "open", "merged_at": None, "head": {"sha": "0" * 40}}
        })))

    def test_reject_failed_run(self):
        record = DATA[0]
        target = "/repos/oromaskevic23-cmd/HANTER/actions/runs/" + str(record["run_id"])
        self.assertTrue(live_errors(record, fake_api(record, {
            target: {"id": record["run_id"], "head_sha": record["commit"],
                     "status": "completed", "conclusion": "failure"}
        })))

    def test_reject_failed_job(self):
        record = DATA[0]
        target = "/repos/oromaskevic23-cmd/HANTER/actions/jobs/" + str(record["job_id"])
        self.assertTrue(live_errors(record, fake_api(record, {
            target: {"id": record["job_id"], "run_id": record["run_id"],
                     "status": "completed", "conclusion": "failure"}
        })))

    def test_reject_missing_api(self):
        record = DATA[0]
        def failing_get(path):
            raise ValueError("permission denied")
        self.assertTrue(live_errors(record, failing_get))


if __name__ == "__main__":
    unittest.main()
