# Upstream source audit — 2026-10-27

Source: https://github.com/Jakeschincariol/trader-skill
Method: GitHub connector file reads; no remote code executed. File blob SHA identifiers are GitHub object hashes, not a pinned repository commit.

| Source | Git blob SHA | Initial static findings | Decision |
|---|---|---|---|
| README.md | 449cb93a62fb072cb01b9bbb454197edc30f39a0 | Python 3.8+, SEC data, broker integration instructions | REVIEW |
| trader-risk/SKILL.md | e51984e668d5d81df2deee546e793ad5797724f7 | Risk verdict, explicit approval requirements | REVIEW |
| trader-risk/check.py | ff2f59b53d8bba5727b0e9d9b1e5bbc11e178996 | 17,621 chars; stdlib imports; local file writes; no detected subprocess/network patterns in quick scan | CANDIDATE, NOT APPROVED |
| trader-budget/size.py | 6920c8429867b9b578383374e2bf9a1b84e181bc | 19,757 chars; stdlib imports; local file writes; no detected subprocess/network patterns in quick scan | CANDIDATE, NOT APPROVED |
| trader-analyst/facts.py | 805a9ecaf932e48e358733231ad65f98899084b3 | 23,992 chars; urllib network access and local file writes | NETWORK DENIED |
| trader-broker/SKILL.md | 6de039774f7b44fd42c63cbb8aa1e787967bc633 | Explicitly instructs brokerage connector and order placement after approvals | EXCLUDED |
| trader-broker/ticket.py | 94064133f2ea72fa64434aebfbf7ea9f6489db96 | 21,544 chars; local file writes, ticket generation; broker connector remains separate | EXCLUDED |
| .claude-plugin/marketplace.json | a4f71fc6832dd60daf09a524142809992c253cdd | Plugin manifest includes entire package, including broker skill | WHOLE-PACK INSTALL BLOCKED |

## Security conclusions

1. **Do not install the upstream marketplace plugin wholesale.** The broker skill can lead to live brokerage operations through external tools, contrary to IMPERIAL's staging policy.
2. The preliminary import/pattern scan is **not** a complete security review. Local writes require path traversal and symlink checks; no source code has been copied or executed.
3. Next permitted engineering work: pin upstream repository commit; inspect full code and transitive local imports; copy only an allowlisted offline subset (risk and budget); run isolated unit tests using synthetic portfolio data; block all broker adapters and network.
4. HANTER, MORGAN and VELION ⚡️ integration remains NOT DEPLOYED.
5. No tests or real trading results are claimed.
