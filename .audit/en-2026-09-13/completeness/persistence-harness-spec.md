# Persistence harness implementation specification

**Recorded:** 2026-09-14  
**Status:** implementation contract; no runtime execution or persistence result is claimed.  
**Supersedes:** the rejected wording in `persistence-harness-research.md`; preserves that research and the council record unchanged.

---

## Gate and scope

Implement only a private, disposable harness and mission copy. Do not call the interface gate satisfied until the repaired fixture files are final, re-read, and hashed by the implementing/reviewing worker. The concurrent `repair2` fixture worker owns those files; this specification's dependency is the following intended public API, not the old council hashes:

| Variant | Required public methods |
|---|---|
| v1 | `SetFixtureCaseLabel(string)`, `GetFixtureCaseLabel()`, `GetFixtureCharges()` |
| v2 | v1 methods plus `SetFixtureLocked(bool)`, `GetFixtureLocked()` |
| matrix | v2 methods plus `SetFixtureOmitLockedOnSave(bool)`, `GetFixtureOmitLockedOnSave()`; omit remains non-serialized |

The matrix may start only after all three compile/config-load smokes pass and the interface dependency is verified. A smoke is not persistence evidence.

Use one private copy of official `dayzOffline.chernarusplus`, one PBO variant at a time, `instanceId = 1`, a unique `-profiles` directory and fresh logs per process, and a storage root only under the disposable harness root. Each current RPT must show the expected `<branch>/storage_1` selection. Set and record `storageAutoFix = 0` in every branch: this is a harness choice, not a statement of a default.

The private `cfgeconomycore.xml` includes:

```xml
<ce folder="EntityPersistenceFixture"><file name="types.xml" type="types" /></ce>
```

`types.xml` has the fully explicit controlled record: `nominal=0`, `min=0`, `restock=0`, `lifetime=3888000`, `quantmin=-1`, `quantmax=-1`, `cost=100`, and all six flags (`count_in_map=1`, the other five `0`). These are test inputs, not a guarantee of persistence. Seed creates only the three fixed cases with `ECE_SETUP | ECE_UPDATEPATHGRAPH | ECE_CREATEPHYSICS`, never `ECE_NOPERSISTENCY_WORLD`, `ECE_DYNAMIC_PERSISTENCY`, `ECE_NOLIFETIME`, or `ECE_LOCAL`.

---

## Run protocol and timing

Every run has a generated `runId`, phase, owned PID, unique port/profile/log directory, initially absent trigger, and receipt directory. Trigger content is exactly `phase=<phase>;runId=<runId>`. Every harness and fixture marker must include both fields; reject unscoped markers, markers predating process start, and markers from another phase/run.

The active private `db/messages.xml` entry—not the pinned official commented example—is:

```xml
<message><deadline>5</deadline><shutdown>1</shutdown><text>Entity persistence fixture shutdown in #tmin minute(s).</text></message>
```

This proposed mission edit uses the documented scheduled-shutdown route, but its behavior on the pinned executable remains runtime-unverified. The five-minute deadline starts at process start; model the shutdown state at about T+240 seconds. The controller may issue a state-changing trigger only through T+180, requires `PHASE_READY_FOR_SHUTDOWN` at or before T+210 and before any shutdown-state marker, and waits for self-exit through T+420. A missed cutoff/bound invalidates the run before any cleanup; only then may it terminate its retained owned process, and the run is ineligible as save/reload evidence. The budget is 13 fresh processes (about 65 countdown minutes): one mandatory fixture-free no-mod control, three candidate compile smokes, five valid-chain processes (`seed-v1`, `verify-v1`, `migrate-v2-default`, `set-true-v2`, `verify-true-v2`), and four bad write/read processes. The earlier 12-process/60-minute count excludes the mandatory no-mod control.

Before any trigger, require current-run module/mission markers, the current CE completion marker, and, for a reload, the complete expected callback set. A post-CE timeout is failure, never authority to enumerate or mutate. Before launching `seed-v1`, the controller records that its fresh storage root is absent. Startup may create storage, so post-CE seed checks require zero existing fixture objects and retain the prelaunch fresh-root proof; they must not require filesystem nonexistence after startup. Seed alone may create objects only after those checks. Ordinary reloads require all three fixtures and fail on any missing, extra, or duplicate fixture. Each bad-read requires both valid controls, records the faulty entity as present or absent without prescribing either result, and rejects unexpected or duplicate records; never spawn a replacement.

`PHASE_READY_FOR_SHUTDOWN` only proves in-process work is complete. Require phase-correlated `SAVE` markers after each mutation and after phase-ready but before self-exit; a periodic/pre-mutation save is insufficient. Self-exit, exit code, callback completion, or changed storage hashes are observations only. Exact next-process callback/readback is the persistence oracle.

---

## Exact record oracle

The three records are `control-false` at `7500/7500`, `faulty-writer` at `7502/7500`, and `control-true` at `7504/7500`; each must be within 0.75 m horizontally of its location. Their invariant fields are class, label, `charges=17`, position, and all four `GetPersistentID` blocks. Record all four blocks for each label.

At seed, a canonical nonzero PID means four present blocks with at least one nonzero block; zero-valued blocks within that four-block tuple are legitimate. If all four seed blocks are zero, adopt the first same-v1 reload's nonzero four-present-block PID as canonical. A partial PID means missing blocks, not a mixed zero/nonzero tuple, and any partial, changed, or missing PID is failure. Canonical IDs must then match in `verify-v1`, every valid record in the clone-derived upgrade chain, and both controls in both bad branches. The faulty reader's ultimate presence/absence is observed, not prescribed.

`LOAD_OK` and `SAVE` must state variant, schema, label, charges, four PID blocks, phase/run ID, and `locked` where applicable. Require every write boolean in a normal `SAVE` to be true. A matrix faulty `SAVE` must instead identify `locked=OMITTED` only for `faulty-writer`; controls must write normal locked values. `LOAD_FAIL` must identify phase/run ID, label, schema, and failure stage.

---

## Compile gate and error policy

Run isolated v1, v2, and matrix smokes with empty storage, no spawn/enumeration/persistence assertions, and the active shutdown route. Each candidate needs positive witnesses: Game, World, Mission, and private `init.c` module-load markers; a never-called typed parameter of `EntityPersistenceFixtureBattery`; `ConfigIsExisting("CfgVehicles EntityPersistenceFixtureBattery")=true`; and self-exit in time.

Capture a no-mod control RPT first using a fixture-free mission/controller: it must contain no typed `EntityPersistenceFixtureBattery` reference and no `ConfigIsExisting("CfgVehicles EntityPersistenceFixtureBattery")=true` assertion, because either witness would make the control itself candidate-dependent. Keep its common engine/CE/config baseline comparable to candidates and record the exact fixture-free differences. Reject a candidate for candidate-attributable compile/config/addon errors or any error new relative to that control. Do not require no `SCRIPT (E)` globally: permit only an exact, pre-recorded baseline diagnostic allowlist. Apply a recorded narrow normalization only to run-variable timestamp, PID, and profile-path prefixes; after that normalization, require exact diagnostic message text, source-code stack locations, and count. Physical RPT line numbers are not source-code locations and are not compared; any changed diagnostic message, stack location, or count fails. Packaging inspection is a separate package gate, not compilation proof.

---

## Immutable branch matrix

Before a snapshot or clone, the owned process must have self-exited and its port/handles be released. Reject symlinks, hardlinks, and reparse points. Create sorted relative-path/size/SHA-256 manifests for source and destination and require equality; capture PBO, source, config, mission, log, and storage hashes for every run. Never launch `baseline-v1` or `pre-bad`; re-hash each immediately before every clone and after all dependent trials.

| Phase | Input / required precondition | Exact pass output | Fail / stop |
|---|---|---|---|
| `seed-v1` | fresh storage; v1; CE/profile/lifetime preconditions | exactly 3 spawned schema-1 records, labels/charges/positions correct; save markers after ready | any profile/lifetime, count, or write failure; preserve |
| freeze `baseline-v1` | self-exited seed | independent manifest-equal immutable copy | any release/link/manifest failure |
| `verify-v1` | clone baseline; v1 | exactly 3 `LOAD_OK v1 schema=1`, charges 17 and canonical PID continuity; no spawn | any missing/new/duplicate/ID change |
| `migrate-v2-default` | clone baseline; v2 | exactly 3 `LOAD_OK v2 schema=1 migratedLocked=false`; getters all false; normal schema-2 saves after ready | callback/value/save failure |
| `set-true-v2` | upgrade chain after migration | before mutation exactly 3 schema-2 records with labels, charges, canonical PIDs, and `locked=false`; v2 has no omission getter or flag, so do not assert one here; mutate only `control-true=true`; normal saves after ready | precondition/mutation/save failure |
| `verify-true-v2` | fresh v2 upgrade chain | exactly 3 schema-2 loads: false/false/true by labels, charges 17, canonical PIDs; then freeze `pre-bad` | any value/ID/count failure |
| `bad-a-write`, `bad-b-write` | independent clones of immutable pre-bad; matrix | before mutation exactly schema-2 `false,false,true`, zero omit; set faulty true+omit only; normal controls save false/true and faulty save omits locked | precondition/control/write failure |
| `bad-a-read`, `bad-b-read` | respective matrix branch | `LOAD_FAIL stage=locked-read` for faulty; exactly one `LOAD_OK` false control and one `LOAD_OK` true control, both charges 17/canonical PID | CE-init timeout or either control failure: preserve branch and report isolation failure; do not vary timers |

The no-mod control baseline is mandatory for the compile error comparison; it has no fixture/persistence assertion. Stop after the valid chain and two independent bad/control trials. A CE-init failure, timing cutoff, control failure, ID discontinuity, unexpected callback order, or snapshot defect preserves receipts and ends that branch rather than causing blind retries or timing variation.

---

## Correction trace and evidence boundary

| Council correction | Encoded contract |
|---|---|
| HC-01 | final fixture API dependency and re-read/hash gate |
| HC-02 | three smokes, positive witnesses, no-mod-relative exact error allowlist |
| HC-03 | T+180/T+210/T+240/T+420 cutoffs and 13-run budget including the mandatory no-mod control |
| HC-04 | phase/run correlation on triggers, logs, and markers |
| HC-05 | four-block, per-label canonical PID oracle |
| HC-06 | exact pre-mutation values/callbacks and post-ready saves |
| HC-07 | physical manifest-equal snapshots and immutable rehashes |
| HC-08 | `storageAutoFix=0`, mandatory controls, preserve-and-stop failures |

Sources re-opened by the council: official Central Economy `9a21bb9f5fb9c62a7ce2761402196091588133e6` (`init.c`, `economy.xml`, `cfgeconomycore.xml`, `types.xml`, `messages.xml`); DayZ Samples `da5e5437c9502620d9853fb6eed14701135ab2ea`; extracted `centraleconomy.c`, `entityai.c`, `game.c`, `objectspawner.c`, and `ensystem.c`; and the retained DayZDiag `1.29.0.163709` RPT/executable receipts listed in `persistence-harness-council.md`. Official web message semantics were search-index evidence with direct requests blocked (HTTP 403). Settings, native declarations, public-mod practices, clean exit, and storage changes do not prove persistence; only the stated fresh-process results can do so.
