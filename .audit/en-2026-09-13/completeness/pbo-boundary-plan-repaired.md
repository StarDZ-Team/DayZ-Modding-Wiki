# Repaired Bounded PBO Size-Boundary Experiment Specification

**Status:** pending independent exact-final review, then static harness review. No harness or experiment has been run.

**Scope:** the future experiment is limited to retained bytes, the installed DayZ Experimental Tools build `23909709`, and DayZDiag `1.29.0.163709`. It cannot establish a universal PBO, Workshop, distribution, client, compression, or other-build limit.

**History:** this replaces neither `pbo-boundary-plan.*` nor `pbo-boundary-council.*`; they remain immutable design/review history. The companion JSON is the executable-data contract. Exact reopened inputs and this delivery's output hashes are in `TEMP/pbo-boundary-plan-repair/hash-receipt.json`.

---

## Decision boundary

The reviewed reverse-engineered layouts contain per-member unsigned 32-bit fields and sequential payloads; they do not prove a native DayZ total-archive limit. This wave can report a stage outcome for this fixture only. It may distinguish a split-member result from a single-member result at the same aggregate filler sum, but it must not turn a shared failure into a causal diagnosis.

- If `sum-i31-at` succeeds and `member-i31-at` fails after the control gates, that supports a **stage-specific** single-member signed-length hypothesis. It is not native-format proof.
- If `member-i31-minus` passes and either or both `*i31-at` cases fail, record only a failure correlated with crossing this bracket. Aggregate extent, allocation/resource exhaustion, timeout, corruption/resource parsing, and distinct layout failures remain alternatives.
- If `sum-u32-minus` passes and `sum-u32-at` fails, record only a stage-specific failure correlated with this bracket; do not call it an offset, total-size, or field limit.
- `member-u32-plus1` is tool-only. No wrapping, hand-built, or substitute archive enters runtime.

No result claims an `OriginalSize` boundary when the observed uncompressed convention is zero.

---

## Constants, fixture, and exact matrix

`B31 = 2,147,483,648`, `B32 = 4,294,967,296`, `M = 1,048,576`. Generate each filler as a real, non-sparse, non-compressed file: form a 1 MiB canonical block from SHA-256 digests of UTF-8 `PBOBOUNDARY/v1/block/` plus `uint64-le(counter)` for counters `0..32767`, repeat it with its leading remainder, stream-hash during write, close, stream-rehash, and require exact length. Every generator and parser read uses a fixed small buffer; it must not derive an allocation from a member length.

Each boundary source root contains exactly `config.cpp`, the listed `payload/aa_filler_NN.txt` files, and `payload/zz_sentinel_<token>.txt`, in that required archive order. The ASCII sentinel has no BOM/newline:

```text
PBOBOUNDARY|schema=1|case=<token>|nonce=<run-id>|expected-path=PBOBoundary/<token>/payload/zz_sentinel_<token>.txt
```

Use underscore tokens, not hyphenated case IDs, in every virtual prefix, filename variable, and CfgPatches class: `small_control`, `member_i31_minus`, `sum_i31_at`, `member_i31_at`, `sum_u32_minus`, `sum_u32_at`, `member_u32_max`, and `member_u32_plus1`. Boundary prefix is exactly `PBOBoundary\<token>` and its config is dependency-free:

```cpp
class CfgPatches { class PBOBoundary_<token> { units[] = {}; weapons[] = {}; requiredVersion = 0.1; requiredAddons[] = {}; }; };
```

Let each parser's observed values be `H` (byte after the all-zero header terminator), `C` (`config.cpp` `DataSize`), `F` (filler `DataSize` sum), `T` (sentinel `DataSize`), `S = H+C+F`, and `A` (archive length). Accept that equation only after both parsers prove the exact, unique member set/order. For the current-Builder shape, require `A = S+T+21`; the last 21 bytes are `00` and a SHA-1 of every preceding archive byte.

| Order | Case/token | Exact filler `F` | Required observed gate | Runtime |
|---:|---|---:|---|---|
| 0 | `small-control` / `small_control` | 1,048,576 | full all-stage control | yes |
| 1 | `member-i31-minus` / `member_i31_minus` | 2,146,435,072 | `S = B31+H+C-M`; **`A < B31`** | yes if valid |
| 2 | `sum-i31-at` / `sum_i31_at` | 1,073,741,824 + 1,073,741,824 | `S = B31+H+C > B31`; exactly two such `DataSize`s | yes if valid |
| 3 | `member-i31-at` / `member_i31_at` | 2,147,483,648 | `S = B31+H+C > B31`; exactly one such `DataSize` | yes if valid |
| 4 | `sum-u32-minus` / `sum_u32_minus` | 4 × 1,073,479,680 | `S = B32+H+C-M`; **`A < B32`** | yes if valid |
| 5 | `sum-u32-at` / `sum_u32_at` | 4 × 1,073,741,824 | `S = B32+H+C > B32`; exactly four such `DataSize`s | yes if valid |
| 6 | `member-u32-max` / `member_u32_max` | 4,294,967,295 | `S = B32+H+C-1 > B32`; only conditionally runtime-eligible | yes if valid |
| 7 | `member-u32-plus1` / `member_u32_plus1` | 4,294,967,296 | no representable `UInt32 DataSize` | never |

The seven expected-valid filler totals are exactly `19,326,304,255` bytes (`17.999023436568677 GiB`) before overhead. Record decimal `H`, `C`, every member field/range, `T`, `S`, sentinel end, data end, footer start/end, and `A` from each parser; intended source order is not a physical-offset result.

---

## Stored-only field gate and strict parsing

The retained installed-Builder control PBO is SHA-256 `1CE4ADB9D28C778E083CA506E0042217CE6A68FF2EC7FC085E2E19596D619071`, length 441. Its reopened raw header `[0,151)` SHA-256 is `386BD6CE8FAC2F38FA1538E13360FEF5A30CDEF708EF79DFCED4EBB25F6F6993`; raw footer `[420,441)` is exactly `00B451A3F09D692D6CD01FD70619D69F8D942B7115` (SHA-256 `04EA3572087008D7F8768AC1C7DD5C8AB16F1C379C625D22679473262F62B1A5`). These bytes establish `H=151`, `config.cpp=(method 0, OriginalSize 0, DataSize 188, [151,339))`, `data\\example.txt=(0,0,81,[339,420))`, and the matching footer SHA-1.

For every uncompressed matrix member, require method `0` and `DataSize == closed source length`. The small control sets the only accepted `OriginalSize` convention: either `0` for every uncompressed member or exactly its `DataSize` for every uncompressed member. Larger cases must match it. Anything else is `unexpected_uncompressed_field_convention`; a zero convention scopes this wave to stored `DataSize` and makes no `OriginalSize` limit claim. `Cprs`, a nonzero method, or unequal stored source size is `not_comparable_compression_changed`, not size evidence.

Implement two independently authored streaming validators, hash each implementation in the receipt, and require exact agreement. One is PowerShell/.NET (`UInt32`, checked `UInt64`, 64-bit `FileStream`); the other is Python (`struct.unpack('<5I')`, arbitrary integer accumulation). Both must:

1. Use bounded NUL-string and property parsing, reject an unterminated/oversized name/property, accept exactly one first `Vers` property block, and require its other four `UInt32` fields to be zero.
2. Require exactly the all-zero 21-byte header terminator; require the exact unique member names/order (`config.cpp`, expected fillers, sentinel), the fixture's reserved field zero, and no additional member.
3. Check every `UInt64` range and contiguity; require `dataEnd == footerStart`, exactly `00 || SHA-1(all bytes before footer)` at `footerStart`, exact EOF at `footerStart+21`, and no trailing byte.
4. Fixed-buffer SHA-256 every archived member range and every closed source; compare filler ranges to their source and directly seek/read/hash the tiny sentinel. Prohibit `ReadAllBytes`, `read(size)`, and any buffer sized from a multi-GiB field.

The parser receipt contains header interpretation, implementation hashes, all values above, member SHA-256 values, whole-PBO SHA-256, computed/stored footer SHA-1, and agreement result. A parser-valid artifact remains parser-valid or invalid independently of its builder exit status.

---

## Packing, tool configuration, and stage gates

Before execution, record a new nonexistent literal case root; case-specific source, build, temporary, output, logs, and profile roots must be empty and fresh. The intended Builder invocation is exactly:

```powershell
& $addonBuilder $sourceRoot $buildDir '-packonly' '-clear' "-temp=$componentTemp" "-prefix=PBOBoundary\$token" "-toolsDirectory=$toolRoot" "-filebank=$fileBank"
```

`$fileBank` is the exact retained Experimental Tools `Bin/PboUtils/FileBank.exe` path/hash. The explicit `-packonly`, `-clear`, `-temp`, `-prefix`, `-toolsDirectory`, and `-filebank` inputs control only the settings they demonstrably override; they do **not** prove all installed/user settings are neutralized. Build the source inventory from the isolated root immediately before launch, hash its normalized expected set, and use the two actual archive tables as the only membership gate.

Static reopening of installed `AddonBuilder.exe` SHA-256 `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1` finds `-include=<file name>` and defines it as “Directly copies matched files to PBO” from an absolute wildcard-pattern file (`;`/`,` separators). It is not an exhaustive packing whitelist, so this wave does not pass `-include` and does not infer list syntax. The same embedded help documents `-exclude` as a pattern file and `-filebank` as an explicit FileBank path. Record full argv, tool/image hashes, UTC start/end, stdout/stderr, log copies, child image identities, exit code, resource samples, source/config/inventory hashes, exact output discovery, and final PBO hash.

Reopened configuration inputs are `AddonBuilder.exe.config` (`E614FCB04D8E3429FAB70466261F36383DE3BFCD230A058BC196AC0727482BBE`), `logger.xml` (`1D24D7D4AFB5249EFBEF3435195BBEA4D1A2D6317292637C7F834B69F8470005`), `PboUtils/exclude.lst` (`F678C872B0E146A51339F4D5C248D7E76ADEF31A80D439AD2FCC2E3CE07D099C`), and both `1.0.240.639` user configs (`B52A097818CB036EC72AFD6BD0A6402C5892E1B29AE671115CA977D0348E33C7`, `86F88CFCB6F908F26DB0D9882AF35C9D2087A16AE1F9CAC46FEF8028D6A57CB8`). The executable config names `logger.xml` and default FileBank; the logger writes shared `..\\Logs` files; the exclusion list excludes source/temp/docs and PBO/signing patterns; user configs contain differing DayZ Tools paths/settings. The effective per-user configuration and FileBank selection remain unresolved unless the captured child/config evidence proves them. Preserve these exact inputs and record `FileBank.exe` identity, never infer effectiveness from a setting.

Builder, parser A, parser B, BankRev, signer, signature check, and runtime each retain a separate outcome. If Builder returns nonzero or error text but leaves a PBO, preserve and parse that exact PBO; do not relabel its parser result. Builder `FATAL`/`ERROR` text is a Builder failure even at exit zero. Require exactly one new nonempty discovered output only for `accepted_exact`.

Run BankRev `-properties` and `-logFull` without extraction; require its exact prefix/member result. Sign only after parsers succeed, preserve PBO before/after SHA-256, require signer output without PBO mutation, and require exactly one DSCheck `is OK` result. The **small control must pass source, Builder, both parsers/agreement, BankRev, signing, signature check, and runtime before any large case**. Manual PBO construction is outside this wave and never substitutes a failed official-tool result.

---

## Runtime probe and gates

Build a separate small probe PBO with prefix `PBOBoundaryProbe`, source `probe-source/scripts/5_Mission/PBOBoundaryProbe.c`, and no boundary class/type dependency:

```cpp
class CfgPatches { class PBOBoundary_Probe { units[] = {}; weapons[] = {}; requiredVersion = 0.1; requiredAddons[] = { "DZ_Data" }; }; };
class CfgMods { class PBOBoundaryProbe { type = "mod"; dependencies[] = { "Mission" }; class defs { class missionScriptModule { value = ""; files[] = { "PBOBoundaryProbe/scripts/5_Mission" }; }; }; }; };
```

For the selected case, the probe tries these seven literal slash paths with `OpenFile(path, FileMode.READ)`, bounded `ReadFile`, and `CloseFile`:

```text
PBOBoundary/small_control/payload/zz_sentinel_small_control.txt
PBOBoundary/member_i31_minus/payload/zz_sentinel_member_i31_minus.txt
PBOBoundary/sum_i31_at/payload/zz_sentinel_sum_i31_at.txt
PBOBoundary/member_i31_at/payload/zz_sentinel_member_i31_at.txt
PBOBoundary/sum_u32_minus/payload/zz_sentinel_sum_u32_minus.txt
PBOBoundary/sum_u32_at/payload/zz_sentinel_sum_u32_at.txt
PBOBoundary/member_u32_max/payload/zz_sentinel_member_u32_max.txt
```

The fixed probe has no PBO hash or parser-receipt data embedded in the boundary archive. It prints every opened literal path, each bounded raw read, and an open count; it treats zero or multiple opens as failure and does not print a success claim. Before packing, write immutable external `run-context-seed.json` containing only run ID, selected token, nonce, expected sentinel bytes, source recipe, and its hash. After PBO parsing, atomically write/re-read external `run-context.json` that binds that seed hash to the final PBO SHA-256 and both parser receipt hashes. The external evaluator requires exactly one opened path and exact raw bytes matching the selected token/nonce in that context, then binds the context's PBO/receipt metadata; it never asserts that those metadata were read from the PBO. The one `Print` block is copied to RPT and script log; these are two copies of one execution, not independent experiments, and their raw blocks must match.

Use the retained `run-case.ps1` controls: one numeric instance ID; private mission/profile containment; `steamQueryPort = game port + 1`; three free ports before launch; captured cleanup; `WaitForExit`; and empty ports afterward. Assign 790/26300–26302 through 796/26360–26362 in matrix order. The known small control marker was about 20.8 seconds after start; 45 seconds is a per-case observation ceiling only. Absence is `timeout_no_marker`, inconclusive and never a numeric-limit result. Any retry is only an exact-byte rerun after source research records a falsifiable cause and distinguishing result; fresh profile/RPT/script/console logs are created after the recorded start time.

The runtime receipt includes executable/version/hash, argv, case/token, root and descendant process identities, instance/ports, parser/PBO/nonce receipt identity, RPT/script/console hashes, exact marker blocks, and cleanup result. `verifySignatures=0`; enforcement/client/distribution remain separate.

---

## Windows containment, storage, retention, and ceilings

For Addon Builder, FileBank, BankRev, signing utilities, and DayZ, create a captured Windows Job/process-tree scope before launch. Record root and every descendant PID, parent PID, image/argv where available, and immutable creation time; sample each observed identity's private/working bytes plus system free memory/disk. On guard breach, preserve current logs/crash artifacts, then terminate only the captured job/tree identities after rechecking PID **and creation time**, wait for every recorded identity, and prove no observed identity remains. Never kill by image name, port, broad parent discovery, or an unrelated PID.

Reject any run root, target, or existing ancestor containing a reparse point; use canonical physical paths rather than trusting lexical `Resolve-Path`/`GetFullPath`. Sources must have no reparse, sparse, or compressed attribute and exactly one hard link; record logical bytes and allocated bytes via `GetCompressedFileSizeW` (not a logical-length approximation). Before and continuously during every stage, project retained plus all live source/temp/output/scratch allocations from literal receipt paths; stop/abort so actual owned allocation never exceeds 40 GiB. Enforce: at start at least 64 GiB disk free; before a case 48 GiB disk/12 GiB physical memory free; during a captured tool 40 GiB disk/8 GiB physical memory free and 16 GiB private bytes for that tool.

Run sequentially. Retain parser-valid final PBOs, receipts/logs, small config/sentinel, generator/recipe, source and archive hashes, public signing material/bisigns, and crash artifacts; retain an unexpected plus-one PBO if produced. Delete a source filler or component temp only after range hashes match and its atomic receipt was re-read. Cleanup accepts only literal canonical paths enumerated in `cleanup.json`, checks child-of-recorded-run-root containment, and confirms every removed path is absent; it uses no glob or case-derived recursive target. The private key is never a public retained artifact.

---

## Ceiling, outcomes, receipt, and unresolved scope

The ceiling remains eight packaging attempts and seven launches, with at most two source-gated exact-byte retries (absolute ten/nine). Stop the wave on any small-control stage failure; invalid source/hash/parser/placement; guard breach; crash pending classification; already-discriminating pair; or trials no longer producing distinguishing evidence. Preserve evidence and return to source research/council rather than searching bytes, changing member counts, changing compression, selecting another packer, manually substituting an archive, joining a client, or testing Workshop.

Each case receipt independently records source, Builder, parser A, parser B, BankRev, signing, check, and runtime outcomes; artifacts and parse results survive failure at an earlier stage. It records commands, versions/hashes, full configuration/input hashes, resources and process identities, `H/C/F/T/S/A`, all member fields/ranges/hashes, footer and full-PBO hashes, logs/markers/crash files, projection samples, cleanup, and limitations.

Remain explicitly unresolved after this stored-only wave: compressed `OriginalSize` and `DataSize` semantics; decompression allocation; compressed/mixed cumulative boundaries; native DayZ member/total/archive-position/footer limits; client/signature enforcement/distribution/Workshop; other filesystem and build behavior; and effective user-config selection where not observed. C01–C12 are repaired pending exact independent review; C13–C17 retain their prior scoped/accepted limits.
