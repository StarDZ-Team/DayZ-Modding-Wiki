# Persistence-harness council review

**Review date:** 2026-09-14  
**Repository HEAD inspected:** `f1bb001c0a49d4e8fd727b79a8b6c12133846fed`  
**Reviewed delivery:** `persistence-harness-research.md` SHA-256 `1DD3FBE68B18ADAD21A0AADD03143902AB5A0E280FFCB9B30BAD4C17D1C52282`; JSON SHA-256 `6A9D780FB26109ED2DD027B7C9BD6D725C6CB5C62B44DD3E3F8ADA3B7061DFAA`  
**Scope performed:** independent static review only; no game, server, client, Workbench, compiler, packer, dev server, build, install, or commit

## Decision

**Conditionally accepted as a sound test design, but not ready to implement yet.** The CE include, explicit type record, persistent-flag hypothesis, CE-finished/trigger gate, `instanceId = 1` storage mapping, scheduled shutdown route, immutable-branch matrix, same-v1 control, v1-to-v2 chain, true resave/reload, and repeated bad/control branches are appropriate. Implementation is gated on the existing fixture-interface repair and the eight small harness-contract corrections below. This is an implementation gate only; it is not runtime approval and does not claim that any fixture has persisted.

## Accepted

1. The proposed `<ce folder="EntityPersistenceFixture"><file name="types.xml" type="types" /></ce>` placement and fully specified `flags` field match the official CE modding syntax. The proposed numeric values are acceptable controlled inputs: `nominal/min/restock=0`, `lifetime=3888000`, `quantmin/quantmax=-1`, `cost=100`, and all six flags explicit. They are not an official prescription for persistence.
2. The configured class derives from `Battery9V`, ultimately under the official `Inventory_Base` economy root; `db/economy.xml` enables dynamic init/load/respawn/save. `GetEconomyProfile() != null` and positive lifetime checks are valid runtime preconditions, not static proof.
3. `ECE_SETUP | ECE_UPDATEPATHGRAPH | ECE_CREATEPHYSICS` is a defensible persistent-spawn hypothesis. Extracted `objectspawner.c:48-56` removes `ECE_DYNAMIC_PERSISTENCY` and `ECE_NOLIFETIME` when CE persistence is enabled. The recipe correctly excludes `ECE_NOPERSISTENCY_WORLD`, `ECE_DYNAMIC_PERSISTENCY`, `ECE_NOLIFETIME`, and `ECE_LOCAL`. Only a fresh-process reload can validate the hypothesis.
4. `MissionServer.OnInit()` is too early to authorize spawn. The observed `[CE][Hive] :: Init sequence finished.` marker plus a profile-local trigger is a reasonable build-specific gate; reload phases must also observe their exact callback set before triggering enumeration or mutation.
5. `-storage=<branch-root>` with `instanceId = 1` selecting `<branch-root>/storage_1/` is supported by the retained diagnostic RPT (`:1442`) and must be asserted from each current run's log. It remains version/recipe scoped.
6. An active `messages.xml` countdown with `deadline>0` and `shutdown=1` is the official scheduled-shutdown path. The official page says shutdown is ignored without countdown and the final one-minute state saves, kicks, and locks the server. Waiting for self-exit is correct; crash, `RestartMission()`, `RequestExit()`, Ctrl+C, `Stop-Process`, or harness `Kill()` cannot count as graceful completion.
7. The independent baseline clones, same-v1 control, migration chain, non-default v2 mutation followed by a fresh v2 reload, and two bad/control clones from one immutable `pre-bad` snapshot answer the intended questions without treating file changes or callbacks as persistence proof.
8. The research correctly bounds third-party sources: CF/COT mission-loaded conventions, Expansion `RequestExit`, and VPP spawn/restart choices are implementation examples, not CE completion or flush guarantees.

## Rejected or corrected wording

1. Reject `"persistence comes from CE eligibility, dynamic load/save, and creation without a no-persist flag"` as a source guarantee. Those settings form the test hypothesis; the same-version fresh-process readback is the first persistence evidence.
2. The pinned/installed `db/messages.xml` does not itself demonstrate an active five-minute shutdown. Its `deadline=600` example is inside an XML comment. The active five-minute entry is a proposed private-mission change whose semantics come from the official Server Messages documentation; it remains runtime-unverified on the pinned executable.
3. Fence and WoodenCrate are valid examples of zero nominal/min/restock and long lifetime, but the XML alone does not prove the research phrase `persisted player-created entities`. Keep only the configuration comparison.
4. A shutdown delay or self-exit does not establish a CE commit or OS flush. `OnStoreSave` markers and storage hash deltas are supporting observations only; exact next-process label/PID/value readback is required.
5. Public-mod behavior and native declarations do not prove persistence. The local StarDZ barrel comment explicitly says its expectation was not independently tested and remains only a negative-control warning.

## Minimum corrections before implementation

1. **Fixture interface gate:** do not implement until the v1 file exposes label setter plus label/charge getters and v2 exposes label setter plus label/charge/locked getters. Matrix already has the full required interface. At review time the exact hashes remained v1 `CD15...8205`, v2 `4D74...85A`, matrix `A3A8...090D`; this is an acknowledged repair dependency, not a checkout-age claim.
2. **Compile-smoke verdict:** replace the impossible blanket `no config/script errors` condition with explicit positive witnesses and a narrow error policy. Require World/Mission/init module-load markers, a typed fixture reference, `ConfigIsExisting(...)=true`, and self-exit. Fail on compile/config/addon errors attributable to the candidate or any new error relative to a no-mod control; allow only exact pre-recorded diagnostic noise such as the retained `PluginConfigDebugProfile is not Registred` `SCRIPT (E)` stack (`RPT:1409-1416`).
3. **Countdown budget:** state that `deadline=5` runs from server start and the one-minute shutdown state begins at about T+240 s. Refuse to create a state-changing trigger after T+180 s, require `PHASE_READY_FOR_SHUTDOWN` by T+210 s and before any shutdown-state marker, then wait for self-exit until a declared bound (recommended T+420 s). A missed bound invalidates the run before any owned-PID cleanup. Twelve planned processes imply about 60 minutes of countdown time, plus copying/inspection; this is feasible but must be budgeted.
4. **Run correlation:** give every process a unique run ID, unique profile, empty/nonexistent trigger, and fresh log set. Trigger content and every harness marker must contain both phase and run ID. Do not accept an unscoped marker or a marker predating process start.
5. **PID oracle:** record all four PID blocks per label. If seed assigns a nonzero ID, verify it immediately; if seed is all-zero, adopt the first same-v1 reload ID as canonical. Require the canonical per-label IDs to match across `verify-v1`, the clone-derived upgrade chain, and both valid controls in bad branches. A changed/missing PID is failure, not merely a note; the faulty entity's post-failure presence remains an observed outcome.
6. **Exact stage assertions:** before `set-true-v2`, require exactly three schema-2 `LOAD_OK` records, all `locked=false`, produced by the prior migration resave. Before each bad write, require exactly three schema-2 records with the expected `false/false/true` values and zero omit flags. Correlate required `SAVE` markers after mutation/phase-ready and before self-exit; a prior periodic save does not satisfy the stage.
7. **Snapshot isolation:** clone only after the owned process has self-exited and its ports/handles are released. Reject symlinks/hardlinks/reparse points; generate sorted relative-path/size/SHA-256 manifests on source and destination and require equality. Never launch against `baseline-v1` or `pre-bad`; re-hash them before every clone and after all trials. Snapshot the exact PBO/source/config/mission hashes per run as well as storage.
8. **Bad-matrix confounder:** set and record `storageAutoFix = 0` for all branches so automatic replacement of storage does not obscure the malformed-record experiment. This is a deliberate harness choice, not a claim about its default. Keep both valid controls mandatory; if CE never reaches the completion marker or either control fails, preserve the branch and report an isolation failure rather than varying timers.

## Explicit implementation gate

Implementation may begin only when all eight corrections above are encoded in the harness specification and the repaired fixture files are re-read and hashed. The first executable gate is three isolated compile/config-load smokes; no persistence claim is allowed there. Runtime approval then requires, in order, a self-exited seed, a fresh same-v1 reload, the schema-1-to-schema-2 reload/resave chain, a fresh reload of the non-default `locked=true` value, and two independent bad/control trials with both controls intact. Any crash or harness kill makes that process ineligible as save/reload evidence.

## Unresolved until runtime

- Whether the custom type receives the intended economy profile/lifetimes and is actually saved with the proposed flags.
- Exact callback order and persistent-ID assignment time on `DayZDiag_x64.exe` `1.29.0.163709`.
- Exact scheduled-shutdown log/exit behavior and whether the following process can read the just-written records.
- Native disposition of the truncated schema-2 entity and isolation of following records.
- Native commit/flush internals; these are not required if the genuine fresh-process readback matrix succeeds, but must not be claimed.

## Reopened evidence

- Official CE checkout `https://github.com/BohemiaInteractive/DayZ-Central-Economy.git` at `9a21bb9f5fb9c62a7ce2761402196091588133e6`: `init.c` `73658F...AFB`; `db/economy.xml` `62C140...F8F8`; `cfgeconomycore.xml` `095417...4615`; `db/types.xml` `59093B...AFA8`; `db/messages.xml` `55C9C2...C8A`.
- Official Samples `https://github.com/BohemiaInteractive/DayZ-Samples.git` at `da5e5437c9502620d9853fb6eed14701135ab2ea`: `Test_GardenPlot/config.cpp` `2C66BE...D37`.
- Extracted scripts: `centraleconomy.c` `6948B1...46A3`; `entityai.c` `AD0818...57F5`; `game.c` `CF5290...3158`; `objectspawner.c` `6CC150...F4B9`; `ensystem.c` `8BE625...B188`.
- Public checkouts were reopened at CF `0763e7e7548c9a0bed6626afff835de80693ebf3`, COT `41f2c2b99565d0e3970163e162efbf1283fdca62`, Expansion `6dacd00f6d943ebbd99e0cf1baad93f470d96419`, and VPP `dc22e420df3b54e821055f9764da1e48f4a31e71`; cited file hashes matched the research ledger.
- Retained runtime substrate: RPT `40CC6F...41C1`, with `storage_1` selection at `:1442` and CE completion at `:4654`; executable SHA-256 `34F637...A69A`, product `1.29.0.163709`.
- Official Bohemia Server Messages, Error Codes, Server Configuration, CE Configuration, and CE mission-files pages were re-queried on 2026-09-14. Indexed bodies supported the bounded semantics above; direct page opens returned HTTP 403. No inaccessible page was treated as freshly opened full text.
