# Public Proof Verification — Sprint 003

The evidence register at [milestones.json](../evidence/milestones.json) contains **dated, narrowly scoped** results. These are not deployment, revenue, independent external certification or general security claims.

## Verify on a local machine

Python 3.11+; no third-party dependencies, payment, GitHub authentication or secrets required for offline verification:

```bash
python3 -m unittest discover -s tests -v
python3 tools/verify_milestones.py
```

To **requery GitHub's official REST API** (public repository identity, current PR head/state, workflow head/conclusion, job ownership/conclusion):

```bash
python3 tools/verify_milestones.py --live
```

Optional `GH_TOKEN` may increase API rate limits; **never print it** or commit it. If the API is unavailable or disagrees, live verification **fails closed**. Live checks do not replay tests or independently hash historic CI logs.

## Evidence interpretation

- Snapshot: the first investigation observed four **open, unmerged** engineering PRs, and corresponding successful job metadata on 25 October 2026.
- Historical job test counts and `logs_sha256` were observed separately and are stored for auditing. Current script checks their structure but does **not** download or rehash historical logs.
- Reference CI may use mocks and deterministic offline behavior; none of these jobs demonstrates deployed autonomous agents, paying customers, real model inference or production reliability.
- CI job `offline-evidence` is reproducible and never accesses the network. Job `live-evidence` explicitly queries GitHub on the PR's CI run and reports a time-bounded current state, not a permanent certification.
- Reviewers may open any source revision, PR and GitHub Actions run directly using the immutable links in the register.

**Claim ≠ Evidence ≠ Verification.**
