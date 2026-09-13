# EN completeness acceptance ledger

Goal agreement: [AGENTS.md](../../../AGENTS.md). Started from commit `8fa131365f59a343602cefd682290535cd435cc2` on `wiki-reorg`. This ledger lists required evidence, not a declaration that it exists.

| Requirement | Evidence required for completion | Current checkpoint |
|---|---|---|
| Existing EN correctness | Page/claim coverage, source-use records, independent final reviews, resolution of recorded defects | Prior doublecheck exists; unresolved claims remain |
| Missing knowledge | Topic coverage map grounded in current pages, sources and modder/admin workflows; implemented and reviewed required additions | Research task `task_32d95ff449e4` |
| PBO limits | Scoped evidence separating format, entry, archive, packer, engine and distribution behavior; version-qualified wording | Research task `task_a155d6b407bc` |
| Multi-PBO architecture | Source-backed layouts and dependency explanations with reproducible examples and validation records | Same packaging research task; implementation pending |
| Sources actually consulted | URLs/commits and paths/lines or symbols for extraction, local docs, beta mods, official sources and public mods | Prior records exist; new task records required |
| Examples | Explicit prerequisites and execution contexts; relevant compilation/tool/runtime results and expected/error behavior | Runtime executables inventoried; execution not yet validated |
| Unresolved prior findings | Reopened evidence and, where needed, bounded runtime experiments, followed by independent adjudication | Eight prior unresolved leads remain; do not silently count as verified |
| Navigation | Strict current EN anchor/file checks plus independent semantic review of changed targets | 210 inline Markdown anchor repairs approved by council task `task_113cdcf92dfd` and committed in `789abaf`; checker does not cover all HTML/reference-style/absolute links |
| Final generated artifacts | Updated affected generated docs and graph from accepted EN bytes, with consistency checks | Pending final content |
| Integrated build | Actual zero exit code for final revision and recorded Node/memory settings | Pending final content |
| Rolling integration | Council-approved exact diffs, scoped commits on current branch, no unrelated user files | Anchor delivery integrated in `789abaf`; further content deliveries pending |
| Worker/worktree preservation | Accepted settlements and release/retention decisions; unique commits/changes accounted for before worktree removal | Current research wave uses main checkout with disjoint ownership |
| Honest closure | Requirement-by-requirement final audit, no known repairs or required coverage/validation outstanding | Overall goal active |

Current Orca Run: `run_335030a972ec`. Runtime `89eeffb6-5c9c-4090-b251-d1e5c5858123`. Coordinator `term_21c4c30a-a530-43d2-90a1-ca3dfec14e63`. Re-query Orca before relying on these dated lifecycle pointers.

Models for this wave: Sol/high for packaging research and coverage analysis, Terra/medium for anchor implementation, independent Sol/medium for anchor review. Launch receipts confirmed these effective selections. No Claude used.

Follow-up runtime probes are assigned to Terra/high under task `task_78cb9a6ddd42`, dispatch `ctx_6feecc9d7abc`. Existing runtime inventory is only presence/version evidence. The task must produce isolated test sources and actual observations before conclusions can be reviewed.

The broader goal is not reduced to this first wave. The coverage findings determine additional bounded research, implementation and council tasks. A completed inventory, a passing Markdown check, or a lack of reported defects is insufficient evidence of full completion.
