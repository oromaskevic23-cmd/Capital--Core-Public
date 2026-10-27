# Trader Skill — IMPERIAL Core integration (staging only)

Upstream: https://github.com/Jakeschincariol/trader-skill
License: MIT. Original code and attribution remain with upstream authors.

## Scope
This is a **reviewed integration manifest**, not an installation of the 11 upstream skills, and not a deployed trading agent. The upstream repository contains 11 skills. Each must undergo CYBER HAK dependency, network, secrets, prompt-injection, licensing and execution review before importing any executable code.

| IMPERIAL component | Intended role | Permission |
|---|---|---|
| HANTER | route research tasks and audit requests | read-only |
| VELION ⚡️ | summarize evidence, never claim verified forecasts | analysis only |
| MORGAN | budget, risk, portfolio scenario research | paper only |
| CYBER HAK / Guardian | block unapproved capabilities | deny by default |
| ProofGraph | store hashes and provenance | no order execution |
| Approval Gateway | future explicit per-order owner consent | disabled in this stage |

## Mandatory controls
- FREE_ONLY; no paid subscriptions, exchange or brokerage accounts created.
- PAPER_ONLY=true; LIVE_TRADING_ENABLED=false; ORDER_EXECUTION_ENABLED=false.
- No brokerage connectors, API keys, secrets, wallet signing, transfers or real orders.
- No automated copying of investors or Congressional trades into actual transactions.
- Third-party scripts run only after independent source review in a network-restricted sandbox.
- Data sources and SEC User-Agent must be configured legitimately; no fabricated financial performance.
- Trading approval cannot be inferred from general approval to install this integration.
- Keep a full audit trail and explicit owner authorization before any later live-trading design.

## Import procedure (not yet executed)
1. Pin the exact upstream commit SHA and record file hashes.
2. Review all 11 SKILL.md instructions and Python tools, including the broker tool.
3. Run upstream offline unit tests with Python 3.8+ in isolation.
4. Verify that all brokerage/order paths remain disabled in IMPERIAL adapters.
5. Open a separate reviewed PR for an allowlisted, pinned, non-executing subset.
6. Require CI, independent QA and Owner approval before enabling any financial action.

## Status
SPECIFIED / REVIEW REQUIRED. No skills are installed into a runtime by this manifest. No CI or paper-trading E2E is claimed.
