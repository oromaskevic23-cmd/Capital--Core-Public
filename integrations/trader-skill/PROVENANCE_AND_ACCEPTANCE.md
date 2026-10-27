# Third-party provenance and enterprise acceptance

## Upstream
Repository: https://github.com/Jakeschincariol/trader-skill
License declared by upstream: MIT
Source review date: 2026-10-27
Upstream blob SHA evidence:
- README.md: 449cb93a62fb072cb01b9bbb454197edc30f39a0
- trader-risk/check.py: ff2f59b53d8bba5727b0e9d9b1e5bbc11e178996
- trader-budget/size.py: 6920c8429867b9b578383374e2bf9a1b84e181bc
- trader-broker/ticket.py: 94064133f2ea72fa64434aebfbf7ea9f6489db96

These hashes identify individual Git blobs. The upstream commit and dependency tree are NOT pinned. Do not treat this as a completed software supply-chain attestation.

## Import status
**No third-party Python source is imported into IMPERIAL Core.** The local paper_gate and enterprise_bridge are original isolated reference implementations, not installations of upstream skills. Broker integration is prohibited. The upstream skill instructions must be reviewed as untrusted input; never give them execution or approval authority.

## Test boundary
The offline adapter simulates:
HANTER task validation -> VELION ⚡️ synthetic proposal (no LLM inference) -> MORGAN risk check -> Guardian denial of execution.
Hash-chained in-memory audit detects accidental tampering but is not an immutable, signed, or persistent production ledger.

## Acceptance gates
- [x] Source file spot-check and exclusion of broker adapter
- [x] Offline integration code and tests committed
- [x] Previous paper-gate CI run 40526762644 SUCCESS (before integration changes)
- [ ] Current head integration CI SUCCESS
- [ ] Pin upstream commit, validate full source/dependency tree and license
- [ ] Independent QA reviewer approval
- [ ] Real authenticated HANTER/MORGAN/VELION staging service calls
- [ ] Persistent append-only ledger, replay protection, signing, and retention policy
- [ ] Threat model, rollback and production change approval

**No live trading, brokerage connection, external funds, or revenue is authorized or claimed.**
