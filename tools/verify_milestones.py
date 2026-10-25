#!/usr/bin/env python3
"""Independently re-check public IMPERIAL Core milestone claims against GitHub API.

Only scoped repo/PR/run/job metadata is verified. CI log content and log
hashes are NOT re-verified by this tool; no live service is tested.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence" / "milestones.json"
OWNER = "oromaskevic23-cmd"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def static_errors(record):
    errors = []
    name = record.get("repository_name")
    if not isinstance(name, str) or not NAME.fullmatch(name) or name in (".", ".."):
        return ["invalid repository name"]
    slug = OWNER + "/" + name
    root = "https://github.com/" + slug
    expected = {
        "repository": root,
        "commit_url": root + "/commit/" + str(record.get("commit")),
        "pull_request": root + "/pull/" + str(record.get("pull_request", "")).rsplit("/", 1)[-1],
        "run_url": root + "/actions/runs/" + str(record.get("run_id")),
        "job_url": root + "/actions/runs/" + str(record.get("run_id"))
                  + "/job/" + str(record.get("job_id")),
    }
    for key, url in expected.items():
        if record.get(key) != url:
            errors.append(key + " does not match immutable coordinates")
    if not SHA40.fullmatch(str(record.get("commit", ""))):
        errors.append("commit is not a SHA-1 identifier")
    if not SHA64.fullmatch(str(record.get("logs_sha256", ""))):
        errors.append("log digest format invalid")
    if record.get("visibility") != "public" or record.get("status") != "TESTED":
        errors.append("not scoped public TESTED evidence")
    if record.get("conclusion") != "success":
        errors.append("CI record is not success")
    if record.get("pull_request_state") != "open" or record.get("merged_at") is not None:
        errors.append("record does not identify the original open PR snapshot")
    counts = record.get("tests")
    if not isinstance(counts, dict) or any(type(counts.get(k)) is not int
                                          for k in ("tests", "pass", "fail", "skipped", "cancelled", "todo")):
        errors.append("invalid test summary fields")
    elif counts["tests"] < 1 or counts["pass"] != counts["tests"] or any(
            counts[key] != 0 for key in ("fail", "skipped", "cancelled", "todo")):
        errors.append("failed/incomplete test summary")
    for key in ("run_id", "job_id"):
        if type(record.get(key)) is not int or record[key] < 1:
            errors.append("invalid " + key)
    return errors


def github_get(endpoint):
    if not re.fullmatch(r"/repos/" + OWNER + r"/[A-Za-z0-9_.-]+"
                        r"(?:/pulls/\d+|/actions/runs/\d+|/actions/jobs/\d+)?", endpoint):
        raise ValueError("refused API endpoint")
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "imperial-public-evidence-check/1",
               "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    req = urllib.request.Request("https://api.github.com" + endpoint, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)


def live_errors(record, get=github_get):
    errors = []
    name = record["repository_name"]
    base = "/repos/" + OWNER + "/" + name
    pr_number = record["pull_request"].rsplit("/", 1)[-1]
    try:
        repository = get(base)
        pr = get(base + "/pulls/" + pr_number)
        run = get(base + "/actions/runs/" + str(record["run_id"]))
        job = get(base + "/actions/jobs/" + str(record["job_id"]))
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, OSError) as exc:
        return ["live GitHub API unavailable or refused: " + type(exc).__name__]
    if repository.get("private") is not False or repository.get("full_name") != OWNER + "/" + name:
        errors.append("repository visibility/identity mismatch")
    if pr.get("state") != "open" or pr.get("merged_at") is not None:
        errors.append("PR no longer open and unmerged")
    if pr.get("head", {}).get("sha") != record["commit"]:
        errors.append("PR head does not match cited commit")
    if run.get("id") != record["run_id"] or run.get("status") != "completed" or run.get("conclusion") != "success":
        errors.append("workflow execution is not a completed success")
    if run.get("head_sha") != record["commit"]:
        errors.append("workflow head does not match cited commit")
    if job.get("id") != record["job_id"] or job.get("run_id") != record["run_id"]:
        errors.append("CI job does not belong to cited workflow")
    if job.get("status") != "completed" or job.get("conclusion") != "success":
        errors.append("CI job is not a completed success")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="query official GitHub REST API for current PR/run/job status")
    args = parser.parse_args(argv)
    records = json.loads(DATA.read_text(encoding="utf-8"))
    if records.get("schema") != "imperial.public-milestones.v1":
        print("FAIL: unknown evidence schema")
        return 1
    entries = records.get("milestones")
    if not isinstance(entries, list) or len(entries) != 4:
        print("FAIL: incomplete or unexpected milestone register")
        return 1
    errors = []
    seen = set()
    for record in entries:
        name = record.get("project", "UNKNOWN")
        if record.get("repository_name") in seen:
            errors.append(name + ": duplicate repository evidence")
        seen.add(record.get("repository_name"))
        problems = static_errors(record)
        if not problems and args.live:
            problems = live_errors(record)
        if problems:
            errors.extend(name + ": " + err for err in problems)
        else:
            print("PASS:", name, "static coordinates + scoped metadata" + (" + live API" if args.live else ""))
    for err in errors:
        print("FAIL:", err)
    print("Evidence records:", len(entries), "| failures:", len(errors),
          "| mode:", "LIVE_API" if args.live else "OFFLINE")
    print("LIMIT: no live models, deployments, financial results, CI log replay or log-digest rehash confirmed")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
