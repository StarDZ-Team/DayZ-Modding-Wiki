# Persistence harness implementation council

**Decision: REJECTED — technical gate closed before runtime.** Independent static review at `99c011b4d3ded81f4b45c5f30f326de7e92075b3` on 2026-09-14 found 14 rejected findings, including four direct execution blockers. Current package bytes and serialization telemetry have narrow acceptance; no Enforce compilation or persistence result is claimed.

The review task is complete. The author must repair the implementation and obtain a new review of its exact final bytes before the already-authorized runtime sequence. This is a technical correctness gate, not a new user-permission requirement.

## Evidence and reproducible checks

- Read every current file under `examples/en/entity-persistence`, both accepted specification files, closeout, both implementation reports, and the existing package receipts/logs/payloads. Both accepted specification hashes match the closeout.
- Reopened extracted native declarations and vanilla scripts, official pinned CE/Samples, public CF implementation, local migration documentation and StarDZ beta comments. Full source paths, symbols/line ranges, provenance and SHA-256 are in the adjacent JSON and [evidence receipt](../../../TEMP/entity-persistence-harness-council/evidence.json).
- PowerShell 7.6.0 isolated AST-imported parser probes: AST parses; original PID parser throws on read-only `$PID`; empty RPT lookup throws; one real diagnostic incorrectly consumes 3,794 lines; standalone script error is omitted; wrong schema/charges/locked/PID SAVE set is accepted. [Probe receipt](../../../TEMP/entity-persistence-harness-council/static-probes.json).
- Direct PBO reads show exact two-member payload/source equality, expected prefix and matching PBO/package-log hashes for v1, v2 and matrix. No packer/extractor was invoked. [Archive receipt](../../../TEMP/entity-persistence-harness-council/archive-review.json).
- Current prepared mission manifest and current physical-path/link inventory were independently checked and retained. No game/server/client/Workbench, dev/build/install, commit or runtime launch occurred. No author file was edited.

## Thirteen-process accounting

| Process | Variant | Required input | Current decision |
|---|---|---|---|
| no-mod-control | nomod | empty independent storage | Blocked; not run |
| smoke-v1 | v1 | empty independent storage | Blocked; not run |
| smoke-v2 | v2 | empty independent storage | Blocked; not run |
| smoke-matrix | matrix | empty independent storage | Blocked; not run |
| seed-v1 | v1 | fresh seed-v1 | Blocked; not run |
| verify-v1 | v1 | clone immutable baseline-v1 | Blocked; not run |
| migrate-v2-default | v2 | independent clone immutable baseline-v1 | Blocked; not run |
| set-true-v2 | v2 | validated migration output | Blocked; not run |
| verify-true-v2 | v2 | validated set-true output | Blocked; not run |
| bad-a-write | matrix | independent clone immutable pre-bad | Blocked; not run |
| bad-a-read | matrix | validated bad-a-write output | Blocked; not run |
| bad-b-write | matrix | independent clone immutable pre-bad | Blocked; not run |
| bad-b-read | matrix | validated bad-b-write output | Blocked; not run |

Neither `baseline-v1` nor `pre-bad` is a process target. They must remain immutable snapshots; the present code does not enforce their original manifests (R11).

## Rejected findings and repair requirements

### PHIC-R01 — All four five-minute smoke/control paths are unsatisfiable (blocker)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:191-202`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:362-374`; `examples/en/entity-persistence/harness/mission-template/init-nomod.c:8-20`; `examples/en/entity-persistence/harness/mission-template/init-v1.c:59-65`; `examples/en/entity-persistence/harness/mission-template/init-v2.c:47-54`; `examples/en/entity-persistence/harness/mission-template/init-matrix.c:45-51`.

Candidate smokes use phase smoke-v1/v2/matrix and empty storage, yet line 199 requires LOAD_OK for every non-seed candidate before creating the trigger. None of the templates handles a smoke phase: bypassing that first defect produces unsupported-phase, never Ready. The fixture-free control sets triggered after CE but line 202 still demands a PHASE_READY_FOR_SHUTDOWN variant=nomod marker after T+210; its template emits no ready marker or phase/run correlation. A normal five-minute control is killed at the cutoff. Smoke assertions therefore cannot satisfy the advertised 13-process protocol.

**Repair / next evidence:** Implement an explicit fixture-free baseline state and persistence-free candidate-smoke state. Require CE, genuine module/type/config witnesses and timely scheduled self-exit, with no LOAD/SAVE, spawn or enumeration assertion in any smoke. Correlate every no-mod marker. Add isolated controller transition checks for all four states before runtime.

**Basis:** accepted spec compile/no-mod protocol; retained official CE messages.xml countdown example.

### PHIC-R02 — PID parser throws, and canonicalization is not per label (blocker)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:232-239`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:264-278`.

Pid-Map assigns $pid at line 236, colliding case-insensitively with PowerShell read-only $PID. The imported original function throws on the first actual identity line under PowerShell 7.6.0. Independently, allZero is computed across every object rather than per label; a zero tuple for one object is accepted as canonical when another has a nonzero tuple, and distinct labels may share one tuple. The deferred path enumerates $seen.PSObject.Properties, which yields OrderedDictionary properties (Count, Keys, Values, etc.), not case entries. It does not restrict adoption to verify-v1 or preserve nonzero seed IDs per label. Identical duplicate callbacks are overwritten. If the oracle is missing at any later phase, line 268 creates it from that phase, so a migration can become the origin.

**Repair / next evidence:** Rename the match variable, enumerate dictionary entries explicitly, canonicalize each of the three labels independently, require four signed integer blocks and at least one nonzero per canonical tuple, reject missing/duplicate cases and duplicate object identities, and permit zero-seed fallback only at the first validated same-v1 reload. Persist and hash an immutable oracle tied to seed and verify-v1 receipts; subsequent phases must fail if it is absent or changed.

**Basis:** static-probes.json pidParser and orderedDictionaryPropertyEnumeration; entityai.c:3378-3380; accepted spec exact record oracle.

### PHIC-R03 — Snapshots cannot copy and existing reload storage cannot launch (blocker)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:170`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:219-227`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:296-308`.

Copy-Immutable passes Join-Path $From * to Copy-Item -LiteralPath. The star is literal, so normal storage directories have no such source; snapshot creation fails after making the destination. Even after repairing that, all clone/reload paths already exist and Invoke-OwnedServer runs New-Item -ItemType Directory on $storage without Force at line 170, with ErrorAction Stop. This rejects verify-v1, migration and every reused branch before process start.

**Repair / next evidence:** Enumerate source children explicitly with literal paths, including hidden files, and copy each to a fresh checked destination. Create only absent storage directories; for reload require the exact existing manifest-verified branch. Preserve a failed-copy receipt and do not reuse the partial destination without an explicit branch recovery decision.

**Basis:** PowerShell literal-path and directory creation semantics visible in original code; accepted spec immutable matrix.

### PHIC-R04 — Diagnostic normalization consumes unrelated logs and ignores unstacked errors (blocker)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:138-159`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:368`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:380-381`.

The retained RPT has leading whitespace, one-digit hour and variable fractional digits; regex ^\d\d:\d\d:\d\d\.\d\d\d does not normalize it. Stack separator lines retain SCRIPT (E): prefixes, so the ^----- terminator never matches. On the retained exact RPT the original parser returns a 3,794-line diagnostic containing MULTIPBO runtime events and the rest of the file, making baseline/candidate comparison impossible. An isolated SCRIPT (E): Unknown type returns zero diagnostics: compile/config/addon errors without this particular stack banner are invisible. The timestamp/profile/PID normalization is also not restricted to structured prefix fields, and diagnostic comparison is omitted entirely for persistence phases.

**Repair / next evidence:** Parse the observed RPT envelope first, stop stacks at the actual prefixed separator, retain exact message/source stack locations and occurrence count, and explicitly classify all compile/config/addon/error forms. Allow only reviewed baseline diagnostic tuples, not arbitrary baseline failures. Apply the error policy to every run, preserving native malformed-record observations separately. Prove identical normalized diagnostics compare equal while changed text, stack lines, counts and standalone errors fail.

**Basis:** static-probes.json retainedRpt and unstackedErrors; retained RPT:1417-1425; accepted spec error policy.

### PHIC-R05 — Module witnesses are invented labels emitted from one constructor (high)

**Exact locations:** `examples/en/entity-persistence/harness/mission-template/init-v1.c:16-25`; `examples/en/entity-persistence/harness/mission-template/init-v2.c:16-25`; `examples/en/entity-persistence/harness/mission-template/init-matrix.c:16-25`; `examples/en/entity-persistence/harness/mission-template/init-nomod.c:10-15`; `examples/en/entity-persistence/variants/v1/config.cpp:25-38`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:193`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:370-371`.

All Game/World/Mission/private-init MODULE_LOAD strings are printed together by the private mission constructor. They do not prove four distinct module loads. The PBOs contain only config.cpp and a World script, no candidate Game or Mission witness. The never-called typed method is a useful type-resolution requirement but is not a substitute for actual module records. Native RPT module lines exist in retained output and are not parsed.

**Repair / next evidence:** Use actual current-process engine module-load records for Game, World, Mission and the exact private init path, or add properly configured module-specific witnesses that cannot be emitted by the mission alone. Keep the typed World reference and exact correlated config=true observation. Do not require nonexistent Game/Mission PBO modules without adding valid CfgMods definitions.

**Basis:** direct PBO payload inspection; official Samples Test_GardenPlot/config.cpp:14-28; retained RPT:236,317,1415-1416.

### PHIC-R06 — Smoke receipts and branch progression are not bound to complete current inputs (high)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:78-80`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:311-320`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:359-385`.

A smoke gate contains only passed, variant, PBO hash and a receipt path. Assert-SmokeGate neither reopens the receipt nor binds controller, generated mission, CE/config content, source hashes, executable or no-mod baseline. The common private mission is rewritten on every action. Only matrix requires all three gate files; seed and migration can start without all three smokes or completed same-v1 verification. There is no durable phase-success ledger or predecessor validation, so set-true/verify-true/read phases can be invoked on arbitrary existing branches. Old passed files survive failed reruns and baseline-diagnostics.json can be replaced independently. The launched PBO is only compared with the caller-selected file, not with a verified package payload/current fixture source.

**Repair / next evidence:** Create a suite manifest binding exact reviewed package/source/controller/template/mission/CE/config/executable and no-mod differences, allowing only explicitly normalized per-run fields. Invalidate gates on any relevant change, require all three successful smokes before seed, and enforce the nine-phase DAG with immutable successful predecessor receipts and exact branch input manifests. Persist failed dispatch attempts so a stale success cannot authorize continuation.

**Basis:** accepted spec HC-01/02/04/07 and matrix; archive-review.json proves current packages only; current controller does not consume these proofs.

### PHIC-R07 — Timing and exit checks can accept late, premature or crashing runs (high)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:187-216`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:135-136`.

No shutdown-state marker is monitored. The controller tests whether ready exists only after elapsed>210, not when the marker occurred; a marker first observed at T+211 passes. If the process exits before the loop observes CE/trigger/cutoffs, only storage_1 and a candidate ready substring are checked afterward. A no-mod process that crashes before T+210 can bypass ready entirely; exitCode is recorded but never validated. selfExited means only not killed by this controller and can label a crash as success. Exceptions kill the retained process but skip the run receipt entirely because it is written after the try/finally. Get-Rpt indexes an empty array under StrictMode and throws if the first poll sees no RPT. Unique directories are useful, but log creation times, exact branch storage selection and marker event times are not verified.

**Repair / next evidence:** Persist the owned PID/start/input receipt before waiting and update final failure/kill/exit evidence in finally. Treat absent-yet RPT as pending. Record first observed CE, callback-completion, trigger, phase-ready, shutdown-state and exit timestamps; enforce every bound and order, reject premature/crash/non-success exit, and require the exact normalized Selected storage directory for this branch/storage_1. Never issue a state-changing trigger after a shutdown state. Preserve cleanup failures as failures.

**Basis:** static-probes.json emptyRptDirectoryThrows; retained instance-id-1 RPT:1442,4654; accepted spec run timing and failure policy.

### PHIC-R08 — Pre-trigger callback oracle is only one uncorrelated LOAD_OK substring (high)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:191-200`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:229-230`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:280-294`.

Before mutation the controller checks only LOAD_OK variant=name, not the complete current-run label/schema/charge/position/PID set or expected bad-read failure/control set. Missing callbacks cause an immediate throw at first CE rather than a bounded wait for the expected set. Exact evidence is partly checked only after mutation and process exit. Correlated-Lines filters wrong/unscoped phase/run lines out before line 282 tries to reject UNSCOPED, making that rejection unreachable. Marker matching is unanchored and does not reject trailing run IDs, unknown markers, duplicate fields or unexpected LOAD_FAIL events in ordinary phases. LOAD_OK records are not checked for charges or position in the parser; the in-game getters help but are a different observation from the exact callback oracle.

**Repair / next evidence:** Parse every fixture/harness event into a strict typed record and reject unscoped, stale, wrong-run, malformed and unexpected events before selecting expected ones. Wait only within the fixed deadline for the full expected callback set, validate canonical IDs and all per-case values before triggering mutation, allow startup LOAD callbacks before phase-ready, and separately validate final object enumeration and post-ready SAVE records.

**Basis:** accepted spec run protocol, exact oracle and HC-06; static-probes.json unscopedFilteredBeforeRejection.

### PHIC-R09 — SAVE boundary validates write booleans but not the saved experiment (high)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:243-262`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:287-293`.

The original Assert-SaveBoundary accepts a synthetic bad-a-write with schema=999, charges=999, all-zero PIDs and locked=false for all three labels, with no OMITTED faulty write. It counts required labels and checks true writes, but does not require the correct variant/schema/charges/positions/canonical IDs or case-specific locked values. Omission is permitted for faulty-writer in any matrix phase, not required exactly in bad writes. Unexpected SAVE labels are allowed. It checks saves after ready, but does not validate event timestamps against process lifetime or reject pre-mutation-only evidence independently of the ready marker. The spec requires the exact per-case post-mutation write, not just one successful serialization call.

**Repair / next evidence:** Validate each required post-ready SAVE against the phase oracle, including all fields and exact identity. Require exactly one faulty OMITTED event for each bad-write, normal false/true control saves, and no omission elsewhere. Reject unknown labels, false writes, conflicting or duplicate callback records; retain pre-ready saves as observations that cannot satisfy the phase.

**Basis:** static-probes.json invalidSaveBoundaryAccepted; matrix fixture:85-100; accepted spec exact record oracle and stage table.

### PHIC-R10 — Object enumeration has a vertical blind spot and bad reads accept unexpected objects (high)

**Exact locations:** `examples/en/entity-persistence/harness/mission-template/init-v1.c:68-77,96-124`; `examples/en/entity-persistence/harness/mission-template/init-v2.c:56-77`; `examples/en/entity-persistence/harness/mission-template/init-matrix.c:53-75,87-93`.

All enumeration uses a 10 m 3D sphere centered at 7502 0 7500, while the required oracle is horizontal X/Z and creation has no terrain-trace flag. No SurfaceY/vertical placement evidence is obtained. Objects outside that vertical band can be missed, including zero-count seed prechecks; exact world absence is not established. The current terrain outcome is untested. Matrix BadRead never checks found.Count or rejects an unknown label. Duplicate faulty-writer entities make Label return null and are reported as faulty absent, yet valid controls permit Ready. The parser also permits extra LOAD_OK/LOAD_FAIL records in bad-read so long as two control loads and one matching faulty failure exist. V2 Expected dereferences battery.GetPosition before its null check, so a missing label can cause a script error instead of a controlled failure.

**Repair / next evidence:** Make spawn height and enumeration coverage explicit and consistent with the fixed X/Z oracle, using source-supported terrain height or a deliberate bounded spatial volume that includes the full possible object height. Record world counts and exact per-case records. In bad reads allow exactly the two controls plus at most one faulty entity; reject unknown labels and duplicates, even when the native faulty object survives. Check null before dereferencing in v2 Expected. If world-wide absence is claimed, implement evidence that covers more than the local sphere.

**Basis:** game.c:702,929,1162; centraleconomy.c:10,27,37; accepted spec count/position and malformed-record exception.

### PHIC-R11 — Immutable snapshots are hashed but never checked against their original manifests (high)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:219-227`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:296-308`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:382-385`.

Copy-Immutable computes the source as it exists now and compares only the destination to that newly computed source. The stored baseline/pre-bad manifest is never read on later clones, so modified snapshots are silently blessed. There is no final rehash after the upgrade/bad chains, and no suite closure proving both independent bad branches completed. No original source rehash after copying detects concurrent source changes. Snapshot parents are named safely and snapshots are not selected as run storage, but those useful structural choices do not establish immutable first-v1/pre-bad content.

**Repair / next evidence:** Store the frozen source manifest and bind its hash to the successful parent run. Compare the current source to that immutable manifest before and after every clone, compare clone content exactly, rehash baseline/pre-bad after all dependent processes, and record final completion only when all thirteen process receipts and both clone identities are present.

**Basis:** accepted spec HC-07 immutable branch matrix.

### PHIC-R12 — Filesystem confinement does not validate ancestor paths or failed hardlink probes (high)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:34-61`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:107-125`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:162-180`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:219-227`.

Assert-ApprovedWorkRoot checks lexical equality and then the leaf/tree, but not each existing ancestor from the repository through TEMP; a junction ancestor can redirect an apparently approved root. Tree traversal probes hardlinks but accepts a failed fsutil call. Single PBO/executable inputs use Assert-Ordinary, which lacks the explicit hardlink-count check. Newly created destinations are not resolved and checked against the physical allowed base before use, and source/destination overlap for OfficialMissionRoot versus the private mission is not rejected. Existing private mission files are overwritten in place without a locked active-run/staging ownership check. The inspected current paths are ordinary; this finding concerns missing enforcement, not an observed attack or corruption.

**Repair / next evidence:** Validate every path component from a trusted physical root; reject reparse/links and fail closed if hardlink status is unknown. Check canonical physical source/destination separation, approved containment and no overlap before writing. Stage a fresh per-suite mission with exclusive ownership, preserve originals, and ensure no concurrent live run references files being replaced. Keep all deletion/move/copy checks in native PowerShell literal-path operations.

**Basis:** accepted spec Windows physical copies and no-overwrite rules; current path inventory in evidence.json; no current links observed.

### PHIC-R13 — CE instance-lifetime preconditions and complete runtime provenance are omitted (medium)

**Exact locations:** `examples/en/entity-persistence/harness/mission-template/init-v1.c:119-124`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:123-125`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:213-216`.

Seed checks a non-null economy profile and its configured lifetime equals 3888000, but never queries/logs the instance GetLifetimeMax or remaining GetLifetime. A valid type definition does not establish positive per-instance lifetime. The original source research explicitly required all three lifetime observations and the accepted final spec retains the broader profile/lifetime precondition. Per-run receipts capture init.c only for mission, no log hashes, no executable hash/version, no argv, no full CE mission manifest, no pre-run storage input hash and no persistent final validation status. This falls short of the advertised complete receipts and exact run inputs.

**Repair / next evidence:** Restore explicit profile, configured lifetime, instance maximum and remaining lifetime observations with source-supported positive bounds before seed acceptance. Persist complete before/after input and output manifests, executable version/hash/argv, CE files, all logs, exact context/trigger bytes and final outcome including failure. Keep configuration values separate from runtime proof.

**Basis:** entityai.c:3382-3392; centraleconomy.c:761; persistence-harness-research.md:155; accepted spec seed preconditions and hashes.

### PHIC-R14 — Advertised static validation is broader than the implemented checks (medium)

**Exact locations:** `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:327-339`; `examples/en/entity-persistence/harness/README.md:30`; `examples/en/entity-persistence/README.md:35-37`; `.audit/en-2026-09-13/completeness/persistence-harness-implementation.md:29-31`.

Static parses its own PowerShell AST and two XML files only. It does not parse JSON, the CE fragment or prepared mission/config, validate required locked/omit getters/setters/signatures, check forbidden methods in mission templates, validate Enforce syntax, or exercise controller branches. The method checks are substring presence/absence and cannot establish API validity. It passed despite the reserved $PID assignment and unsatisfiable smoke routing. README describes reviewed templates and a preserved-receipt protocol before the implementation council has accepted either.

**Repair / next evidence:** Narrow claims to the actual checks or add bounded static checks that validate the full contract: strict duplicate-key JSON, every XML/config/template, per-variant declared and called APIs, reserved PowerShell variable writes, all thirteen phase routes and pure event/state negative cases. Keep Enforce compilation explicitly unperformed until real smokes succeed, and describe this delivery as rejected pending repairs.

**Basis:** direct read of Static action; static-probes.json AST success plus runtime-free failures; author implementation claims.


## Accepted bounded properties

### PHIC-A01 — Current package receipts and exact archive payloads agree (informational)

**Exact locations:** `TEMP/entity-persistence-harness-council/archive-review.json`.

Independently read all three existing PBO byte streams, properties and member headers, then compared uncompressed payload bytes with each current config/script source. Prefix EntityPersistenceFixture, exact two-member set, archive SHA-256 and all three retained package log hashes match their receipts for every variant. No package or extraction tool was run.

**Repair / next evidence:** Retain this package-only acceptance bound to the recorded hashes; any fixture/config repair requires new matching package receipts before smoke.

**Basis:** archive-review.json.

### PHIC-A02 — Telemetry preserves inherited serialization order and variant interfaces (informational)

**Exact locations:** `examples/en/entity-persistence/variants/v1/scripts/4_World/EntityPersistenceFixture/EntityPersistenceFixtureBattery.c:17-101`; `examples/en/entity-persistence/variants/v2/scripts/4_World/EntityPersistenceFixture/EntityPersistenceFixtureBattery.c:19-128`; `examples/en/entity-persistence/variants/matrix/scripts/4_World/EntityPersistenceFixture/EntityPersistenceFixtureBattery.c:21-146`.

All variants call super first, then write schema/charges/label, and v2/matrix normally write locked last. Their readers keep ordered failure checks and schema-1 locked=false migration. Added file-context/identity diagnostics do not write to ctx. V1 has no locked/omit APIs and v2 has no omission API; corresponding mission templates respect those method restrictions. Matrix omission remains an instance flag outside explicit serialization. Diffs against HEAD confirm that telemetry edits did not reorder inherited/custom stream operations.

**Repair / next evidence:** Retain these narrow source properties while repairing the controller; they establish neither compilation nor native malformed-record behavior.

**Basis:** entityai.c:2913-3070; serializer.c:1-65; CF ItemBase.c:5-19; git diff and current fixture files.

### PHIC-A03 — CE inputs, launch recipe and API declarations support a bounded experiment (informational)

**Exact locations:** `examples/en/entity-persistence/harness/mission-template/EntityPersistenceFixture/types.xml:1-13`; `examples/en/entity-persistence/harness/mission-template/messages.xml:1-4`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:127-132`; `examples/en/entity-persistence/harness/mission-template/init-v1.c:1-5,121`.

The controlled type record includes all specified values/flags and the prepared private mission has the CE include. Dynamic init/load/save=1, instanceId=1 and storageAutoFix=0 are explicit. Official messages.xml documents countdown from startup, but its example is commented; the private five-minute entry is active. Extracted declarations support CreateHive/InitOffline, CreateObjectEx, config queries, four-block IDs, file context reads, enumeration and the callback queue. The retained recipe uses a hidden owned process and instanceId=1 selects storage_1 in an actual older RPT.

**Repair / next evidence:** Retain as source-backed inputs and historical recipe evidence only; fix the enforcement defects before using this harness.

**Basis:** official pinned CE/Samples; extracted declarations and retained instance-id-1 RPT; evidence.json.

### PHIC-A04 — Native malformed entity fate is not invented and valid controls are modeled (informational)

**Exact locations:** `examples/en/entity-persistence/harness/mission-template/init-matrix.c:71-93`; `examples/en/entity-persistence/variants/matrix/scripts/4_World/EntityPersistenceFixture/EntityPersistenceFixtureBattery.c:85-146`.

The matrix changes only faulty-writer true+omit in its intended mutation path, normally saves the controls, checks control getters after load and prints faulty present/absent without prescribing deletion. It never spawns replacements. Context exists before the process starts and fixture callbacks read it independently, so early startup callbacks can carry the correct phase/run without waiting for mission Ready. PollTrigger uses the engine-ticked system queue and m_Done makes further callbacks inert; no external timer worker is needed.

**Repair / next evidence:** Retain these design choices, while applying R08-R10 exact event/count repairs and stopping on control or CE failures.

**Basis:** matrix source; ensystem.c:397-501; tools.c:52-67; dayzgame.c:2999-3002.


## Unresolved evidence boundaries

### PHIC-U01 — No Enforce compilation or thirteen-process runtime result exists (runtime)

**Exact locations:** `all 13 planned processes`.

No current candidate was compiled or run in this review; packaging proves bytes only. Scheduled shutdown event/exit behavior and SAVE callback ordering on the pinned executable remain unobserved.

**Repair / next evidence:** After repaired-source council acceptance, execute the already-authorized fixed protocol once with fresh bound receipts; do not infer success from packaging, static checks, a kill or storage changes.

**Basis:** task scope; accepted spec.

### PHIC-U02 — Native malformed-record isolation and PID assignment timing remain unknown (runtime)

**Exact locations:** `nine persistence phases`.

Source declares four-block persistence identities and failure returns; it does not establish when nonzero IDs become available, whether a missing locked field fails exactly there, whether the faulty entity remains, or whether subsequent valid controls survive. No mocked parser check in this review is native evidence.

**Repair / next evidence:** Observe the specified same-v1, migration, nondefault and two independent bad/control trials. If CE or either control fails, preserve and stop that branch without timing variations.

**Basis:** entityai.c and Serializer native boundaries; CF is third-party framing, not native proof.

### PHIC-U03 — Extraction is a hashed snapshot, not proven byte-identical to installed 1.29 executable (source-provenance)

**Exact locations:** `D:/DayZ Projects/scripts.txt`; `D:/SteamLibrary/steamapps/common/DayZ/DayZDiag_x64.exe`.

scripts.txt records product=dayz and raw version=124588. Installed DayZDiag metadata is 1.29.0.163709 with the retained SHA-256. This review hashes declarations but does not establish every extraction file belongs to that exact binary.

**Repair / next evidence:** Keep static source provenance and runtime executable provenance separate in receipts; require compilation/runtime to resolve compatibility rather than relabeling the extraction.

**Basis:** evidence.json.

### PHIC-U04 — Terrain placement and fixture-free CE diagnostic comparability need discriminating evidence (runtime)

**Exact locations:** `examples/en/entity-persistence/harness/mission-template/init-v1.c:110-122`; `examples/en/entity-persistence/harness/Invoke-EntityPersistenceHarness.ps1:116-121`.

No terrain height was measured for the fixed X/Z cases. The fixture-free mission still receives the custom CE type entry despite the class being absent in no-mod; whether that creates a differing CE diagnostic is not established here.

**Repair / next evidence:** Resolve the spatial source design under R10 and record exact no-mod differences. During the repaired control/smokes, stop on a new or removed candidate-specific CE/config error rather than broadening the baseline allowlist.

**Basis:** native 3D enumeration declaration; current Initialize-Mission code.

## Exact reviewed core hashes

| Input | SHA-256 |
|---|---|
| `examples\en\entity-persistence\harness\Invoke-EntityPersistenceHarness.ps1` | `10CFBB244750D6A8E9193CF147FA7583023BD7001D907126A7EDDB4CAC3C68A8` |
| `examples\en\entity-persistence\variants\matrix\scripts\4_World\EntityPersistenceFixture\EntityPersistenceFixtureBattery.c` | `0573DFFDDEF375456E51459249C3367A8F2125FE085991AF4672E14F23A7A678` |
| `examples\en\entity-persistence\variants\v1\scripts\4_World\EntityPersistenceFixture\EntityPersistenceFixtureBattery.c` | `169357CCCF2E8797D7791A2AA842DAA755ACDF8527DBB59A9FE6204C1A5536D2` |
| `examples\en\entity-persistence\variants\v2\scripts\4_World\EntityPersistenceFixture\EntityPersistenceFixtureBattery.c` | `10386F5419115F2F81F3B039499493D872BCB5FA37A65F837FD6CD04DBDE0818` |
| `.audit\en-2026-09-13\completeness\persistence-harness-spec.md` | `0988F335D91C2411419F87032BBDC587E837CA57FCF332AFDD2745C687516286` |
| `.audit\en-2026-09-13\completeness\persistence-harness-spec.json` | `4890A1B39DF3552469009AEF1A2DB99053E2BFC16A76774F748EE6FD604554C8` |

The adjacent JSON contains every reviewed source/template/config/report hash, all accepted/rejected/unresolved IDs and HC-01–HC-08 coverage. Package acceptance applies only to these bytes; repaired controller/template inputs must be rebound to fresh smoke gates, and any changed fixture/config requires corresponding matching PBO payloads.
