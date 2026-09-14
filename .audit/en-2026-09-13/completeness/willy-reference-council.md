# Independent council: Willy repositories and offline validator

Date: 2026-09-13 (trial completed 2026-09-14 UTC). This council reopened the pinned repositories, their manifests and selected tests, the retained assessment output, and the local extraction. It ran only the Pack's stdlib validator tests, vanilla-control gate, and a candidate scan of the committed multi-PBO example. It did not install dependencies, start an MCP/game process, invoke an installer, change host registration or profile configuration, edit EN, or create a commit.

## Verdict

Approve a **limited, revision-pinned offline evaluation** of `dayz-script-validator`. Reject using its raw findings as DayZ runtime verdicts, reject calling the current local extraction `1.29.0.163709` wholesale, and continue to reject MCP/environment adoption on the assessment alone.

The independent vanilla-control run did exactly what a version gate should do: it failed against a tree different from the committed `1.29.0.163451` baseline. The current tree produced digest `94fb3e56…c336`, while the baseline records `bdbc7d5a…6706`; the current discovery set is 2,811 files / 12,668,262 bytes versus the baseline's 2,806 / 12,630,470. `ES-EMPTY-IFDEF-UNSUPPORTED-PATTERN` also increased from 254 to 263. This is evidence of baseline/tree drift, not evidence that the current tree fails to compile or that any particular warning is a defect.

The committed `examples/en/multi-pbo` scan returned PASS across eight discovered supported files. That result is useful only as a zero-finding candidate scan: the validator has no `CfgPatches`, `requiredAddons`, multi-PBO dependency-graph, packing, signing, or runtime-load checks. Because the example root has no `$PBOPREFIX$`, its layout prefix/file rules also skip silently.

## Council dispositions

| ID | Disposition | Reviewed claim | Council decision |
| --- | --- | --- | --- |
| WC-001 | Approve with scope | Both repositories were pinned at the intake commits. | Reopened clean worktrees at `dayz-mcp` `ffa47e7c…df8c` (tree `4d12f2d5…34b`) and Knowledge Pack `9727ae83…f933` (tree `e46b7fa0…17a`). Repository code is third-party evidence. |
| WC-002 | Reject and replace | “The wiki's prior authoritative local extraction record identifies `1.29.0.163709`.” | The audit record at `doublecheck/REPORT.md:25` identifies Bohemia DayZ-Script-Diff commit `86974a0…0a1` as Build `1.29.163709` / Scripts Rev. `125372`, and separately identifies the current executable as `1.29.0.163709`. `metadata-comparison.json` explicitly prevents wholesale attribution of the extraction: adjacent `scripts.txt` says raw `version=124588`, while other extracted components carry other raw values. Describe individual extraction files as local snapshots; use exact file hashes and note any independently established upstream byte match. |
| WC-003 | Approve with scope | MCP call shapes and ECE constants agree with reopened extracted declarations. | The cited `CreateObjectEx`, ECE, `ScriptRPC.Send`, and `DayZGame.OnRPC` declarations agree at the inspected lines/hashes. This is static declaration agreement only; it does not validate MCP transport, game behavior, or the extraction's overall build identity. |
| WC-004 | Approve with correction | MCP/Pack dependency statement. | `tools/pyproject.toml` and `requirements-mcp.txt` **declare** `mcp==1.27.2`, `Pillow==12.2.0`, and `psutil==7.2.2`; `dependency-lock.json` hashes a vendored Windows psutil wheel and author toolchains. This council did not install or resolve them. Replace “The installed MCP dependencies are …” with “The MCP manifests declare …”; version pins without an executed install receipt are not installed-state evidence. |
| WC-005 | Approve with scope | Pack self-validation passed. | The retained `packctl-validate.json` says PASS with eight zero-finding groups and hashes to `8574e2be…0e14`. This council reopened it but did not rerun it. It establishes the Pack's own static integrity checks at the pinned commit, not claim truth, runtime compatibility, or game behavior. |
| WC-006 | Reject as defect evidence | Validator's two MCP layout FAIL findings. | Both findings are static false positives at this call site. The rule flags every `.layout` string literal without recognizing filesystem namespaces or use sites. `$profile:mcp_hot.layout` is a runtime filesystem candidate, not a PBO path. The correctly prefixed but absent hot layout is also optional: `EnsureHost()` calls `FileExist(candidate)` and continues before `CreateWidgets(candidate)`; the packed fallback is last. The findings expose missing rule semantics, not a demonstrated crash. |
| WC-007 | Approve as candidates only | Five exact-`GetType()` warnings. | The warnings correctly identify exact comparison syntax, but the universal recommendation to replace it with `IsKindOf` is not generally valid. The reopened sites search for caller-supplied exact `validation.type`, `typeName`, `classFilter`, or `expectedType`; exactness may be intentional. Review the API contract for each site before changing behavior. |
| WC-008 | Approve with scope | Validator baseline workflow is bounded and read-only. | `vanilla_control.py` calls `validate_addon`, hashes discovered inputs, and reads the baseline. It writes only on explicit `--update`; the council command omitted that flag. Its comparison uses error `(rule,file)` pairs and warning counts by rule, so it does not detect warning relocation or line-level changes when counts remain equal. |
| WC-009 | Approve with scope | The Pack validator can be tried on wiki examples. | The candidate scan is reproducible and clean, but PASS must not be promoted to a multi-PBO or DayZ validation result. Missing `$PBOPREFIX$` disables two relevant rules, and no source rule was found for `CfgPatches`/`requiredAddons` graph correctness. |
| WC-010 | Approve source description; reject operational adoption | The MCP contains real read-only and mutating capabilities plus lifecycle guardrails. | Reopened code confirms a stdio FastMCP app, an embedded `127.0.0.1` bridge, mutating Enforce dispatch including `CreateObjectEx`, registration/config writes, lease checks, retail quarantine, and forced-kill cleanup. None was launched here. Source guardrails and mocked tests are not a safety certificate for a live host/game boundary. |
| WC-011 | Correct terminology | The “read-only Knowledge Pack query surface” includes preparation. | `dayz_knowledge_find`, `show`, and `status` are read-only. `dayz_knowledge_prepare` extracts and atomically publishes an index to disk, so it is a bounded local write even though it does not download/update the Pack. The function docstring at `knowledge.py:619` says “two read-only” while four tools are registered. |
| WC-012 | Approve non-adoption | Do not run the Pack updater/skill sync or register MCP solely from this report. | `knowledge_pack.ensure_pack` performs unpinned `git pull --ff-only` or clone; optional sync writes the user skill directory. `apply_host_timeouts` journals and writes both host configs. These paths conflict with the audit's pinned-source requirement and are unnecessary for the offline validator. |

## Reproduced offline trial

All commands used PowerShell with `login:false`; no installer or `--update` was used.

1. Vanilla control:

   ```text
   python "C:\Users\Leonardo Mello\AppData\Local\Temp\wiki-audit-20260914\DayZ-Modding-Knowledge-Pack\tools\dayz-script-validator\scripts\vanilla_control.py" --vanilla-root "D:\DayZ Projects\scripts" --baseline "C:\Users\Leonardo Mello\AppData\Local\Temp\wiki-audit-20260914\DayZ-Modding-Knowledge-Pack\tools\dayz-script-validator\tests\baselines\vanilla_control_baseline.json" --json
   ```

   Exit `1`, expected for the observed tree/baseline mismatch. The stdout JSON payload is preserved with line endings normalized to LF at `TEMP/willy-reference-council/vanilla-control.json`.

2. Committed multi-PBO candidate scan:

   ```text
   python "C:\Users\Leonardo Mello\AppData\Local\Temp\wiki-audit-20260914\DayZ-Modding-Knowledge-Pack\tools\dayz-script-validator\scripts\script_validator.py" "D:\StarDZ\docs\wiki\examples\en\multi-pbo"
   ```

   Exit `0`, PASS, eight files, no findings. The stdout JSON payload is preserved with line endings normalized to LF at `TEMP/willy-reference-council/script-validator-multi-pbo.json`.

3. Validator tests, from `tools/dayz-script-validator`, with `PYTHONDONTWRITEBYTECODE=1`:

   ```text
   python -m unittest discover tests
   ```

   Exit `0`; 157 tests ran in 0.539 seconds. Captured output: `TEMP/willy-reference-council/validator-unittest.txt`. The tests include pure baseline-comparison coverage, but the layout tests contain no `$profile:` or `FileExist`-before-`CreateWidgets` case; their passing status does not address the MCP false positives.

The complete argv arrays, cwd, Python `3.14.4`, exit codes, input sizes, hashes, and side-effect declaration are in `TEMP/willy-reference-council/trial-receipt.json`.

## Rule limitations established from source

- The layout-prefix detector extracts every string literal ending in `.layout` from `.c` files and requires the addon's `$PBOPREFIX$`; it does not distinguish `$profile:`, `$saves:`, `$mission:`, variables, dead/optional branches, `FileExist` guards, or actual `CreateWidgets` call arguments.
- The missing-layout detector similarly checks every correctly prefixed literal against the unpacked addon tree. It is case-insensitive, but not control-flow aware; its message states a missing file reaches `CreateWidgets` even when source proves the call is skipped.
- Both rules skip silently when `$PBOPREFIX$` is absent. Scanning a repository-level multi-PBO fixture therefore bypasses the very per-addon prefix anchor they need.
- The vanilla gate compares errors at `(rule_id,file)` granularity and warnings as counts per rule. It deliberately detects tree digest drift, but equal counts can mask moved warnings and repeated errors in one file collapse to one pair.
- A vanilla-control FAIL means the scanned tree differs from the measured allowlist. It does not mean vanilla does not compile, and a PASS would mean only that findings and digest match that baseline.
- Direct `script_validator.py` PASS is neither an Enforce compiler result nor evidence of packed virtual paths, Addon Builder behavior, signing, client/server load order, or game runtime.

## Small isolated MCP smoke-test plan

This plan is supported without host auto-registration, but it remains outside this no-install/no-launch dispatch. The user already authorizes relevant isolated tooling/tests; execution needs a separately scoped coordinator dispatch after the preparation and source review below, not a new user-permission prerequisite. The plan must not be inferred as approval to adopt the MCP into the normal environment.

1. Copy the pinned MCP and Pack commits into an owned disposable directory. Record commit/tree IDs and hashes again. Do not run `install-mcp.ps1`, `install_mcp.py`, `dayz_mcp.knowledge_pack install`, `--register`, `--pin-clis`, or skill sync.
2. Create a disposable Python 3.11+ virtual environment under that directory. Stage the exact `mcp`, Pillow, and psutil distributions into a local wheelhouse, record filenames/SHA-256 values, then install from that wheelhouse only. The repository currently supplies a hash for its vendored psutil wheel, but the version-only requirements are not an executed lock receipt for all three packages.
3. Redirect `LOCALAPPDATA`, `APPDATA`, `DAYZ_MCP_PACK_DIR`, and `DAYZ_MCP_KNOWLEDGE_JSON` to owned disposable paths. Generate the index from the pinned Pack with `python -m dayz_mcp.knowledge extract --pack <pinned-pack> --out <temp>\knowledge.json`; do not call `dayz_knowledge_prepare` in the first smoke.
4. First run an in-process registry smoke: construct `ServerConfig(mode="embedded", key=<ephemeral>, runtime_dir=<temp>)`, call `build_app`, list tools, and invoke only `dayz_knowledge_status`, `dayz_knowledge_find`, and `dayz_knowledge_show` through FastMCP's test call path. Assert no host config/profile files changed by comparing before/after hashes.
5. If the in-process smoke passes, run a separate stdio transport smoke by invoking `python -m dayz_mcp --embedded --port <unused-loopback-port> --keyfile <fresh ACL-restricted temp key> --idle-timeout 30 --client-platform unknown` directly from the isolated venv. Do not use `--client` (it resolves registered daemon provenance and may auto-spawn) or `--daemon`. Send initialize/list-tools and the same three read-only knowledge calls through an MCP client, then close stdin and prove process exit and loopback-port release.
6. Capture stdout/stderr, the exact MCP requests/responses with secrets redacted, process identity, port ownership before/during/after, and a recursive before/after inventory of only the disposable roots plus read-only hashes of the real host registration/profile paths. Any unexpected external write, daemon/game process, or registration delta fails the smoke.

This plan tests MCP tool registration, stdio transport, and the read-only knowledge calls. It does not test DayZ, the add-on bridge, lifecycle tools, mutating tools, installer recovery, or live-host safety.

## Provenance and selected hashes

| Source | Revision / SHA-256 | Reopened evidence |
| --- | --- | --- |
| `dayz-mcp` | commit `ffa47e7ca8c82f4785279e919cb9d40053bddf8c`; tree `4d12f2d59eb1ab382aa1feb08123b84e3e2de34b` | `server.py:3685-3730,5967-6089`; `server_cli.py:46-104`; `knowledge.py:358-415,615-694`; `knowledge_pack.py:14-105,238-273`; `host_config.py:1144-1210`; `process_lifecycle.py:2238-2309,3035-3050,3206-3294`; MCP bridge/dialog files and selected tests. |
| Knowledge Pack | commit `9727ae83e65ac26a1cd386c64821b00159f8f933`; tree `e46b7fa0683f4567794cd49466d14de1183e617a` | Compatibility matrix, validator README/code/detectors, delivered baseline, and 157 tests. |
| `vanilla_control.py` | `E99BDA82AFC0C6AC9DE86F36A3AEAAD5E6C3C1B2B06EB31CA84D56BC7B1CAC85` | Read/write boundary and comparison semantics. |
| layout prefix detector | `D5A53E206B52C96147F569C4C696B17F7E4B7BCDF1E616D3EB99577072EDE7FA` | Literal extraction, `$PBOPREFIX$` parse, silent skip, no namespace/control-flow model. |
| missing-layout detector | `D479D04F59DFF20CDECC791E9BA7AF50D8E19E16F1025E4E063DBF611BBD83A0` | Literal existence check and unconditional diagnostic wording. |
| MCP dialog controller | `FB527DB88F9490DC7D6A17923CFC4BF80FD3784D8FF88DC79DE6AAA21B207941` | Optional three-path probe; `FileExist` guard; packed fallback. |
| MCP dependency declarations | `pyproject.toml` `337F2D85…17F`; requirements `F434BF27…B98`; lock `F1C682DA…6BA` | Declarations only; no council install. |
| extraction metadata | `D:/DayZ Projects/scripts.txt` `E45D501E…F55`; audit comparison `21026A87…664` | Raw `version=124588`; heterogeneous component-version warning. |
| extracted filesystem/widget declarations | `ensystem.c` `8BE62599…188`; `enwidgets.c` `6BB20BAD…C9E` | `FileExist`, documented filesystem prefixes for file APIs, and `CreateWidgets` declaration; no runtime execution. |
| retained author outputs | assessment Markdown `E3FE5DA8…FE7`; JSON `4E5BF88A…523`; validator MCP scan `8B1E3298…35E`; Pack self-check `8574E2BE…E14` | Reopened as prior evidence, not treated as independent execution. |
| prior version-scope record | `doublecheck/REPORT.md` `4471254DB087C2FBF1A47B9C565FD5DB3826CFE834D10D4CE4A53F27024821D8` | Line 25 scopes `1.29.163709 / 125372` to the pinned Script Diff and forbids silently assigning that version to every extraction file. |

Full unshortened hashes and machine-readable dispositions are in `willy-reference-council.json`.

## Required author-report corrections

1. Replace the wholesale `1.29.0.163709` extraction attribution in the Decision and WILLY-002 text with the scoped Script Diff/current-executable wording above.
2. Replace “installed MCP dependencies” with “declared MCP dependencies”; no install receipt was produced.
3. Reclassify both layout FAILs as known detector false positives for this guarded optional probe, not merely an unresolved “tool/source tension.” Add the exact limitations: no filesystem-namespace, use-site, or guard analysis.
4. State that the five `GetType()` warnings may flag intentional exact-type contracts; do not prescribe `IsKindOf` without per-site semantic review.
5. Distinguish the three read-only knowledge calls from `dayz_knowledge_prepare`, which writes an index.
6. Add the independent vanilla-control FAIL and multi-PBO PASS receipts with their narrow meanings. Do not rebaseline automatically and do not treat the multi-PBO PASS as packaging/dependency/runtime validation.
7. Keep the recommendation against MCP registration/environment adoption. For a later coordinator-dispatched MCP smoke under the user's standing isolated-test authorization, use the disposable no-registration plan above and record external-state before/after evidence; do not invent another permission gate.

## Remaining limits

No MCP dependency set or MCP test suite was executed, because dependencies were not installed in this council and the task prohibited MCP launch/install. No PBO was packed, no DayZ or DayZDiag process ran, and no profile-layout resolution was tested in-engine. The local extraction remains a hashable snapshot with heterogeneous adjacent metadata; only exact file matches to a pinned official source may inherit that source's build attribution.
