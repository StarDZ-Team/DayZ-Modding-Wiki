# PBO boundary implementation council

**Decision: rejected; small-control execution remains gated.** Return I01–I15 to the owners for repair, then reopen the exact final files and repeat the council. The approved experiment specification remains approved for implementation; neither the current harness nor a native boundary result is approved.

Reviewed Git `d795fca51eca92781a4dbdfc89d753790569fb4d` on 2026-09-14 as Codex dispatched task `task_986653517a9a`. No subworkers, author edits, commits, installations, wiki builds, packers, signers, BankRev or DayZ processes ran. Requested review model was Astra high; this worker does not independently assert its backend model.

All 14 fixture-file hashes match both final deliveries. Exact hashes, 30 source/input receipts, evidence hashes, accepted/rejected/unresolved dispositions and safe command results are in the companion JSON and `TEMP/pbo-boundary-implementation-council/inspection-receipt.json`.

---

## What passed, and its scope

- **A01** All 14 delivered fixture text files match the authors final hashes, including final neutral contract B49448E24F19378EBCF5E8F54B9908E156139D161D7923A8A21676FEB1928C6B. Thirty reopened source/input hashes match their expected receipts where provided. Evidence: `inspection-receipt.json`.
- **A02** Eight case sizes/tokens/order, one separate fixed probe setup, seven runtime-eligible cases and tool-only plus-one entry match approved plan data. This is data parity, not enforced execution proof. Evidence: `inspection-receipt.json:matrixArithmetic`.
- **A03** Independent Python digest-block generation reproduces the PowerShell 1048583-byte output SHA256 B47BD3579A0E4F74911E2D60A0A884D9250D92EB958A58FF9279EEDAC33DB039. Generator closes/reopens and records stream hashes; parser payload hashing uses fixed 1 MiB buffers. Evidence: `adversarial-results.json; generate-fixture.ps1`.
- **A04** Both separately authored parsers produce identical full agreement projections for a tiny normal source-backed fixture and retained 441-byte native control. Retained control H151, C188,F0,T0,S339,dataEnd420,sentinelEnd=null, A441; method/original/reserved zero; sizes188,81; raw footer 00B451A3F09D692D6CD01FD70619D69F8D942B7115, SHA256 1CE4ADB9D28C778E083CA506E0042217CE6A68FF2EC7FC085E2E19596D619071. Evidence: `native_441/a.json; native_441/b.json; adversarial-results.json`.
- **A05** A uint64 arithmetic accepts 2^32 and 2^64-1, rejects 2^64; B analogous pure checks pass. Both reject tiny uint32-max ranges beyond EOF. No giant file or native numeric limit was tested. Evidence: `a-arithmetic.json; author-b-tests.log; invalid-comparison.json`.
- **A06** Supplied PowerShell suite reran 26/26 and supplied Python suite reran 19/19 after source inspection. Tiny invalid headers/order/footer/compression/conventions and raw/probe null-sentinel controls pass their tested expectations. Their omissions include the blocking cases above. Evidence: `author-a-tests/static-tests.json; author-b-tests.log`.
- **A07** 64-bit STARTUPINFO is size104 with dwFlags at offset60 (misleading field name show), handles80/88/96; observed redirects and normal exit work. Suspended assignment/job ownership works on tested success and descendant timeout paths; all five observed process identities absent after review. Startup failure remains rejected. Evidence: `all-layouts.json; job-adversaries.json; final-process-absence.json`.
- **A08** Probe config/module/path context matches approved standalone Mission design; seven literal opens, bounded ReadFile4096 and CloseFile align with independently reopened ensystem.c declarations382-443 and retained prior probe/log shape. No PBO/receipt hash embedded and no success claim is printed. New source has not been compiled or run. Evidence: `inspection-receipt.json; exact probe-source files`.
- **A09** Exact Builder flags use packonly/clear/temp/prefix/toolsDirectory/filebank and omit include; installed embedded help and config/logger/exclude/user configs were reopened. BankRev is not executed; retained properties/member/signature/build logs were read. Public parser source is third-party implementation evidence only. Evidence: `embedded-help.json; include-help.txt; inspection-receipt.json`.

The retained official-tool PBO was reopened as 441 bytes without BankRev. Header hash is `386BD6CE8FAC2F38FA1538E13360FEF5A30CDEF708EF79DFCED4EBB25F6F6993`; member ranges are `[151,339)` and `[339,420)`; exact prefix is `PBOExample\Data`. Raw footer and member bytes are retained in the council evidence. This is parser verification against an earlier native artifact, not a new native experiment.

---

## Required author repairs

### I01 — Validator A overwrites member source while reporting valid_exact

**Severity/owner:** blocking / A. **Disposition:** rejected, repair required.

**Exact location:** `scripts/validate-pbo.ps1:13,39-45,90; PboBoundary.Common.psm1:135-147`.

ReportPath=the first member source passes all checks, atomically replaces cfg bytes with the success report, and exits 0. Only archive/inventory/sources-manifest names are protected; physical report ancestry and member source aliases are not protected.

**Required repair:** Before any report write, protect all declared sources and all input identities through physical paths/file IDs; reject destination reparse ancestry and aliases on every failure path, preserving original bytes. Retest exact, case, hard-link, junction-parent and malformed-input alias cases.

**Evidence:** `exact-alias-reproductions.json; alias-repro.py`. Verification: reproduced.

### I02 — Malformed CLI error reporting overwrites member source

**Severity/owner:** blocking / B. **Disposition:** rejected, repair required.

**Exact location:** `scripts/validate_pbo.py:_write_parse_error_if_safe, main`.

Adding --unknown with ReportPath pointing at a declared member source enters _write_parse_error_if_safe before sources are inspected; it overwrites cfg with contract_input_error JSON and exits 3. Normal-mode source alias rejection passes.

**Required repair:** Use one fail-closed destination-safety policy for parse errors and regular execution; no report is preferable when protection of declared inputs cannot be established. Keep exact before/after hashes and malformed duplicate-option coverage.

**Evidence:** `exact-alias-reproductions.json; alias-repro.py`. Verification: reproduced.

### I03 — Validator A does not implement bounded strict JSON/source contract

**Severity/owner:** high / A. **Disposition:** rejected, repair required.

**Exact location:** `scripts/validate-pbo.ps1:31-45`.

Duplicate schemaVersion and missing required caseId both produce valid_exact; malformed JSON becomes internal_error. Source map is a case-insensitive PowerShell hashtable even though inventory uniqueness is ordinal: K and k pass inventory then are rejected as duplicate source keys. Input JSON is read wholly without a byte/count cap; source key-set equality, canonical field types and uppercase hash syntax are not strictly checked.

**Required repair:** Bound JSON bytes/depth/member/source counts before allocation; reject duplicate keys and required-field/type defects; require exact source-key set with agreed ordinal semantics; canonical decimal strings and uppercase hex; map invalid input to contract_input_error. The malformed JSON defect is definite; caps/extra-key policy should be made shared contract text.

**Evidence:** `adversarial-results.json: duplicate_json, missing_case_id, malformed_json, case_keys`. Verification: reproduced.

### I04 — Valid field/property edge cases disagree between validators

**Severity/owner:** high / A. **Disposition:** rejected, repair required.

**Exact location:** `scripts/validate-pbo.ps1:55,72-78`.

A rejects a valid empty config (OriginalSize=DataSize=0) alongside nonempty DataSize-convention members as mixed, while B accepts. A rejects exactly 1024 properties before reading the terminating empty key; B accepts. Eight corrupted tiny archives were rejected by both, but failure projections all differ because B hashes archive before parse and preserves established fields earlier; oversized string outcomes also differ.

**Required repair:** Count properties only after seeing a nonempty key; determine conventions from archive-wide compatibility, preserving the ambiguous zero-length case. Agree explicit failure projection and outcome rules without requiring identical independent diagnostic wording; add cross-validator edge-case tests.

**Evidence:** `adversarial-results.json: empty_datasize, 1024_properties; invalid-comparison.json`. Verification: reproduced.

### I05 — Malformed schema shapes escape into internal errors

**Severity/owner:** high / B. **Disposition:** rejected, repair required.

**Exact location:** `scripts/validate_pbo.py:_parse_inventory,_parse_u64_decimal,_read_json`.

fixtureProfile=[] triggers unhashable-type internal_error; a 5000-digit canonical decimal triggers Python integer conversion limit and internal_error. The contract calls input-invalid failures exit 3. Source validation opens aliases and checks only regular file/length/hash, so reparse/hard-link/sparse/compressed physical policy is not independently enforced.

**Required repair:** Validate types before set membership, reject decimal length above 20 before int conversion, bound depth and classify JSON recursion/type failures. Agree which physical checks belong in each validator versus controller and fail closed for the physical paths required by the accepted harness.

**Evidence:** `adversarial-results.json: b_json_list_profile,b_long_decimal`. Verification: reproduced.

### I06 — Forged validator reports accepted despite failed processes and wrong identity

**Severity/owner:** blocking / A/controller. **Disposition:** rejected, repair required.

**Exact location:** `scripts/controller.ps1:76-77`.

Exact Run-Validators function accepts agreement=true and valid=true from two stub reports with implementation=forged-not-a-validator, wrong implementation hash, outcome=internal_error, exitCode=99, timedOut=true, resource guard breach and cleanup=false. The PBO argument is unrelated to the report.

**Required repair:** Require exact schema/field types, distinct approved implementation IDs and full implementation/dependency hashes, valid_exact/exit0, no guard/timeout, proven cleanup, normal mode, exact archive/inventory/source identity and exact projection. Preserve separate parser verdicts when process fails, but never accept the stage from those alone. Canonicalization must preserve arrays versus scalars/nulls.

**Evidence:** `controller-adversaries.ps1; controller-adversaries.json:forgedValidatorAcceptance`. Verification: reproduced.

### I07 — Fabricated crash/abort receipt and unrelated seed produce read_exact

**Severity/owner:** blocking / A/evaluator. **Disposition:** rejected, repair required.

**Exact location:** `scripts/evaluate-runtime.ps1:25-43; controller.ps1:115-116`.

No runtime was launched. The evaluator accepts a receipt with executable=NEVER_LAUNCHED, root=null, no identities, access-violation exit, timeout, resource guard and cleanup=false. Fresh fake logs match an invented seed although actual archived sentinel is only the eight bytes sentinel, not the claimed case/nonce string. Hashing mutable external files is not proof of a run.

**Required repair:** Bind an immutable approved launch context to exact deployed boundary/probe bytes, source recipe/sentinel hash, two independently valid agreed reports, executable/config/mission hashes, root identity/start/end and log paths/hashes; enforce runtime lifecycle and classify crash/resource/compile outcomes independently from read observation. Reject incomplete/forged/aliased receipts and bind claimed expected bytes to the parser sentinel range. Do not treat metadata as PBO-read bytes.

**Evidence:** `evaluator-adversary.py; forged-runtime/execution.json; forged-runtime/result.json`. Verification: reproduced.

### I08 — Run state and attempts are trusted without provenance or sequential ownership

**Severity/owner:** blocking / A/controller. **Disposition:** rejected, repair required.

**Exact location:** `scripts/controller.ps1:39-56,83-87,98-103,115`.

Require-Run accepts schemaVersion=999, unrelated recorded root, wrong controller/matrix/contract hashes, negative packaging count, runtimeLaunches=999, and a forged small-control pass/probe pointer. No prior case/receipt rehash, lock, next-case-order check or runtime launch ceiling check is enforced. Failure trap can write receipts/state in a supplied physical directory before its runtime-base containment was accepted.

**Required repair:** Validate exact state schema/root/run ID, immutable approved code/matrix/contract and probe identities, prior case receipts and small-control all-stage proof before dispatch; use exclusive run ownership and bounded monotonic counters/order. Failure handling must not write outside an already accepted owned run root. Keep retries separately source-gated or explicitly unsupported.

**Evidence:** `controller-adversaries.json:unsafeStateAccepted; controller-adversaries.ps1`. Verification: reproduced.

### I09 — Cleanup accepts forged eligibility for retained evidence

**Severity/owner:** blocking / A/controller. **Disposition:** rejected, repair required.

**Exact location:** `scripts/controller.ps1:59,119,129-130`.

The exact Cleanup branch accepts schemaVersion=999, wrong manifest.runRoot, no receipts and a literal retained-parser-valid.pbo under RunRoot, and calls the recording Remove-Item stub with -Recurse. Its simulated output claims allAbsent=true. The original tiny target still exists: no real removal ran. Eligibility paths are not linked to reread parser/range receipts, and descendants are not individually checked for links before recursion.

**Required repair:** Validate manifest schema and root, restrict eligible source/temp/key categories, require immutable receipt and hash eligibility with no retained/log/PBO overlap, validate descendants/ancestors without following links and recheck physical containment immediately before deletion. Confirm real absence only after successful bounded literal removal; protect process-live paths.

**Evidence:** `cleanup-simulation.ps1; cleanup-would-remove.json; cleanup-simulation.log`. Verification: reproduced.

### I10 — Failed native startup can leak an unowned suspended process and handles

**Severity/owner:** blocking / A/common. **Disposition:** rejected, repair required.

**Exact location:** `scripts/PboBoundary.Common.psm1:55-65,185`.

ContainedProcess.Start creates job/redirect files and may throw before returning ownership. If CreateProcessW succeeds but AssignProcessToJobObject fails, catch terminates the empty job, not the still-suspended root. Caller launcher stays null, so no disposal/wait occurs. Failures opening redirects or creating/setting a job also lack transactional disposal. SetHandleInformation return values are ignored.

**Required repair:** Make startup transactional with safe handles/try-finally; retain and terminate/wait the exact newly created process handle when assignment fails, then close thread/process/job/redirect handles. Check inherited-handle setup and restrict inheritance to explicit handles; prove failure cleanup with a safe injectable native shim before any native experiment. No real assignment-failure test was attempted because current cleanup is unsafe.

**Evidence:** `exact source inspection; inspection-receipt.json`. Verification: static_defect_not_dangerously_exercised.

### I11 — Exit 259 is misclassified as a running process; census remains incomplete

**Severity/owner:** high / A/common. **Disposition:** rejected, repair required.

**Exact location:** `scripts/PboBoundary.Common.psm1:67-69,188-236`.

A new PowerShell child executing exit 259 is absent, yet helper waits until timeout, records process_timeout/terminatedByHarness and null exitCode. Normal exit0, exit17 stdout/stderr, and a two-process timeout tree passed and all five observed identities were independently absent afterward. Polling records only descendants surviving a sample and does not hash child images; fast FileBank identity cannot be proved from a missing sample. Resource samples carry PID but no creation identity.

**Required repair:** Wait on process handles/job events rather than treating GetExitCodeProcess==259 as liveness; retain actual exit code. Capture descendant creation/exit and image/hash provenance or explicitly fail unverifiable tool selection; bind each resource sample to the captured identity. Ensure cleanup always disposes even if queries fail.

**Evidence:** `job-adversaries.ps1; exit259/process.json; final-process-absence.json`. Verification: reproduced_plus_static_census_limit.

### I12 — Full eight-case allocation schedule cannot pass its own cap

**Severity/owner:** blocking / A/controller. **Disposition:** rejected, repair required.

**Exact location:** `scripts/controller.ps1:61,111,119; README Cleanup`.

Each completed runtime case retains both canonical PBO and copied runtime Boundary.pbo; cleanup schedules only fillers/temp/key. Even after all eligible cleanup, before member-u32-max the lower-bound existing PBO bytes are 30062673920; adding source and three projected copies is 47242543100 (>40 GiB), before overhead. Thus the seventh expected-valid case aborts before Builder if earlier cases pass.

**Required repair:** Account every retained/runtime/source/temp/scratch artifact in one schedule; retain one canonical immutable archive and safely remove redundant deployed copies after proven process cleanup and hash receipt, or revise the approved resource plan through council. Do not weaken the 40 GiB guard. Recompute all eight cases and probe overhead with no large files.

**Evidence:** `inspection-receipt.json:matrixArithmetic; inspection-receipt.py`. Verification: pure_arithmetic.

### I13 — Source inventory and stage resource checks are incomplete

**Severity/owner:** high / A/controller/common. **Disposition:** rejected, repair required.

**Exact location:** `scripts/controller.ps1:60-61,93,111; PboBoundary.Common.psm1:150-176,185; generate-fixture.ps1:75-78`.

Assert-ExactSource ignores hidden unexpected files because Get-ChildItem lacks -Force and does not bound inventory size or verify source records map exactly under Source. Allocation scan checks files but skips rejecting descendant reparse directories. The process starts before first during-resource check; mission/PBO Copy-Item and source rehash are not continuously guarded. Generator checks every 64 MiB after writes, so an actual hard cap has a possible overshoot.

**Required repair:** Perform bounded physical tree traversal including hidden/system entries and all directories; validate exact source mapping and no links/sparse/compression; measure/check before launch or copy and during all lengthy stages. Reserve projected next writes so owned allocation cannot overshoot the hard cap; independently bound mission inventory and copied artifacts.

**Evidence:** `controller-adversaries.json:hiddenUnexpectedSourceAccepted; source inspection`. Verification: reproduced.

### I14 — Small-control failures can still advance to signing/runtime; outputs lost from parsing

**Severity/owner:** high / A/controller. **Disposition:** rejected, repair required.

**Exact location:** `scripts/controller.ps1:93,103-119`.

RunCase proceeds from any discovered PBO to BankRev/sign/runtime when parsers agree even if Builder outcome is failure. The failure only halts after all later stages. If multiple PBOs exist, pbo=null so none is parsed; PrepareProbe throws on failed Builder before parsing its retained output. This contradicts stop-on-small-control-stage-failure plus independent artifact interpretation.

**Required repair:** Preserve/discover and parse each bounded produced artifact independently after failed Builder, while halting downstream native stages until Builder accepted_exact. Journal each stage before invoking the next, preserve partial outcomes on exceptions, handle unexpected plus-one output explicitly and keep probe setup accounting separate. Add safe end-to-end stub state transition tests.

**Evidence:** `exact RunCase/PrepareProbe stage nesting; inspection-receipt.json`. Verification: static_defect.

### I15 — Builder error log and tool identity gates are weaker than specified

**Severity/owner:** high / A/controller. **Disposition:** rejected, repair required.

**Exact location:** `scripts/controller.ps1:69,73-74,79-80,109`.

Tool-Outcome accepts 2026-09-14 01:23:45,000 [ERROR] 1: Example.Main - native builder failed at exit0. That shape is the installed RollingFile/Console pattern, and copied shared logs are not evaluated for failure. BankRev prefix check is substring rather than exact parsed property; DSCheck accepts exactly one arbitrary Signature ... is OK without matching the expected bisign; DSCreateKey process verdict is discarded. Child executable hashes/effective config are not established.

**Required repair:** Parse actual retained log formats and separate invocation-scoped shared-log deltas; fail FATAL/ERROR at exit0 without rewriting parser results. Require exact BankRev property/member facts (allow only the explicitly observed trailing slash convention), exact expected signature identity/hash, key-create outcome and immutable scoped executable/config receipts. Keep effective user config unresolved unless observed.

**Evidence:** `controller-adversaries.json:toolLogClassifications; installed logger.xml; retained Data tool logs`. Verification: reproduced.

---

## Shared contract decisions before repair

- **K01 — Failure projection:** Define whether agreementProjection applies only to valid_exact. Recommended: exact whole projection for valid_exact; on failure compare specified stage/outcome and only jointly established facts, with unavailable keys null and no fabricated zeros. A hashes archive late, B early; this is not by itself false evidence.
- **K02 — Canonical paths and source keys:** Define sourceKey ordinal case-sensitive uniqueness and reject empty/dot/dotdot/drive/UNC/device/ADS/NUL or forward-slash archive path components. Both validators currently accept matching inventory/header ..\outside.txt; neither extracts it, so the reproduction did not write outside council data. Define source/report physical-identity safety and hard-link/reparse policy explicitly for both validators.
- **K03 — Bounded JSON and error taxonomy:** Specify shared JSON byte/depth/member/source caps and exact-required/type/duplicate-key behavior, unknown-field policy and bounds failures. Recommend contract_input_error/3 for malformed input; resource_guard_error/4 for explicit size/depth budget refusal; invalid_header/2 for corrupt archive. Both must include required report fields when safely writable.
- **K04 — Zero-length OriginalSize:** Zero-byte entries are compatible with both zero and dataSize. Determine one archive-wide compatible convention; respect an explicit compatible requested convention; when observe and every member is empty, choose documented zero precedence. Nonempty mixed fields must reject.

These are proposals for coordinator/author agreement; the council did not edit the neutral contract. Distinguish unresolved contract wording from definite source overwrite, forged-success, lifecycle, cleanup and resource-schedule defects.

---

## Safe reproductions and process evidence

All synthetic archives are parser tests only. `adversarial.py` generated only tiny fixtures; `alias-repro.py` contains exact argv, actual before/after SHA-256 and source bytes for both overwrite cases. Its disposable source starts as three bytes `cfg`, SHA-256 `E67D23E7820C49A8051DAC2831F38290F5E72F66C8DB5079EEB60D82F14894C0`. No original source or retained archive was overwritten.

`controller-adversaries.ps1` imports only an allowlist of inspected function ASTs; its Invoke-Stage is an in-process stub and executable placeholders are never launched. `cleanup-simulation.ps1` selects the exact Cleanup AST with Remove-Item replaced by a recording stub; the retained fixture remains present. `evaluator-adversary.py` invokes only the inspected evaluator in PowerShell and demonstrates read_exact with no game process or matching archived sentinel.

The supplied suites were inspected before execution. B temporary directories were redirected into the council evidence root and automatically removed; its largest test logical file is 16 MiB plus one guard byte, not a boundary payload. Python bytecode writes were disabled. A uses two 1 MiB-plus-seven-byte generator checks and bounded benign PowerShell children. Normal exit and two-process timeout cleanup receipts retain PID/creation identities. Additional council exit17/redirect and exit259 children were newly owned and short; independent final checks found all five observed identities absent.

PowerShell native layout measurements match x64 STARTUPINFO despite confusing field names. The exit259 finding agrees with [Microsoft GetExitCodeProcess documentation](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodeprocess); offsets were checked against [Microsoft STARTUPINFOW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfow), accessed 2026-09-14. No dangerous real assignment-failure injection was attempted.

The eight-case storage calculation is pure integer arithmetic. It assumes every earlier eligible filler/temp is cleaned and omits all overhead, making the case6 failure conservative. No large file was allocated to obtain this result.

---

## Source reopening and remaining verification

Opened `D:/DayZ Projects/scripts/1_core/proto/ensystem.c` FileMode/OpenFile/ReadFile/CloseFile declarations and extracted scripts metadata; retained prior Mission probe config/source and its RPT/script marker evidence; installed Builder binary embedded help, executable config, logger.xml, exclude.lst, both user configs and build manifest; retained Data Builder/BankRev/signature receipts and logs; and pinned raw armake2 pbo.rs, HEMTT header/file/read/write.rs and armake build/unpack.c. Exact source hashes match the original plan/implementation ledgers; third-party writers only corroborate layout/arithmetic and demonstrate allocation/cast risks, not native limits.

Public source commits: armake2 `3cc3362101900ff41504db3e780dd1625634cf94`; HEMTT `bf2168ce03d5bb8bd3849090e9b2996402624b1c`; armake `e4940fae0d28c4dd07d9d2c591f8e056545fee3f`. Source files were reopened from the pinned retained raw corpus, not merely accepted from author summaries. Their repository URLs/paths/lines/hashes are in JSON.

One guessed prior log name (`Data-build.log`) did not exist; the actual retained `Data-addon-builder.log` and BankRev properties/member logs were then opened. This lookup error is not a packaging failure.

Full native controller execution, new Enforce compilation, probe packaging, small-control stages and all eight boundary outcomes remain unperformed. The pure suites and targeted stubs do not constitute an exhaustive end-to-end production pass. After repair, require complete safe stage/failure/ownership tests and another exact-final independent review before considering the separately authorized small-control launch. Large experiments and conclusions remain separately unproven.

No runtime, native member/total/offset/footer size ceiling, compression limit, client distribution, signature enforcement or Workshop conclusion follows from this review.
