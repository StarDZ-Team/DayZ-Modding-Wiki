# Independent Council: PBO Boundary Plan

**Reviewed:** 2026-09-14, independently of the author  
**Inputs:** `pbo-boundary-plan.md` SHA-256 `32191A96BCA74F1AAB27302430CA2AFF160344814445E8A44E80823AC09769F8`; `pbo-boundary-plan.json` SHA-256 `663CC823A25447550BD1592F3C088A28178C184617E092A75F42A30A83952131`  
**Verdict:** **rejected as implementation-ready**  
**Execution:** no payload, large file, packer, BankRev, signer, game, server, client, build, or dev server was created or launched.

The eight filler sums are correct and the staged approach is useful. The design still has blocking field-semantics, control, causality, parser, probe, process-tree, and cleanup defects. Repair both author files and obtain exact-diff council approval before implementation; obtain a static review of the implemented harness before any execution.

---

## Boundary recalculation

Let `H_i` be the **observed** byte after the zero header terminator, `C_i` the parsed `config.cpp` `DataSize`, `F_i` the filler `DataSize` sum, `T_i` the sentinel `DataSize`, `S_i` the sentinel start, and `A_i` the archive length. `S_i = H_i + C_i + F_i` is valid only after both parsers observe exactly `config.cpp`, all expected fillers, sentinel, in that order, with no extra member. For the required current-Builder shape, `A_i = S_i + T_i + 21`; the 21 bytes are `0x00` plus the matching 20-byte SHA-1 footer.

| Case | Correct `F_i` | Required actual `S_i` / gate |
|---|---:|---|
| `small-control` | `1,048,576` | `H_i + C_i + 1,048,576`; full-pipeline control only |
| `member-i31-minus` | `2,146,435,072` | `2^31 + H_i + C_i - 1,048,576`; require **`A_i < 2^31`** |
| `sum-i31-at` | `2,147,483,648` | `2^31 + H_i + C_i > 2^31`; two observed `1,073,741,824` members |
| `member-i31-at` | `2,147,483,648` | `2^31 + H_i + C_i > 2^31`; one observed `2^31` member |
| `sum-u32-minus` | `4,293,918,720` | `2^32 + H_i + C_i - 1,048,576`; require **`A_i < 2^32`** |
| `sum-u32-at` | `4,294,967,296` | `2^32 + H_i + C_i > 2^32`; four observed `1,073,741,824` members |
| `member-u32-max` | `4,294,967,295` | `2^32 + H_i + C_i - 1 > 2^32`; maximum stored `DataSize` only under the observed convention |
| `member-u32-plus1` | `4,294,967,296` | no representable `UInt32 DataSize`; tool-only, never runtime, no manual substitute |

No actual case offset exists until packing. Every future receipt must contain decimal `H_i`, `C_i`, `T_i`, `S_i`, sentinel end, data end, footer start/end, and `A_i` from both parsers. Intended order, a formula, or BankRev output is not a physical-offset result.

Seven expected-valid fillers total `19,326,304,255` bytes (`17.9990234366 GiB`) before overhead. With those finals retained, a final 4 GiB tool-only attempt can plausibly hold source + copied source + temp PBO + output PBO, projecting about 34 GiB; one more full-size scratch copy projects about 38 GiB. The 40 GiB cap is feasible but narrow and must use actual allocated bytes.

---

## Findings

### Rejected

| ID | Affected section | Finding and exact repair |
|---|---|---|
| C01 | MD 58–60; JSON `constants`, `binaryValidation` | The retained installed-Builder control uses method `0`, exact `DataSize`, but `OriginalSize=0`; the plan's equality gate necessarily fails. Require `DataSize == source length`; allow `OriginalSize` only `0` or the same length, and require every larger case to match the small-control convention. If it is zero, this wave tests stored `DataSize`, not `OriginalSize`. Add `unexpected_uncompressed_field_convention`. |
| C02 | MD 30–31; JSON `H-CUMULATIVE-I31` | Both at-boundary cases failing after the minus case does **not** identify a cumulative-offset defect. Replace with `unresolved`: it is also consistent with aggregate extent, allocation/resource exhaustion, timeout, corruption/resource parsing, or distinct layout failures. At `2^32`, minus-pass/at-fail shows only a stage-specific failure correlated with crossing this bracket. |
| C03 | MD 66–81; JSON below cases | `H+C<M` constrains sentinel start, not sentinel/footer/archive end. Require `member-i31-minus A_i < 2^31` and `sum-u32-minus A_i < 2^32`; record all ranges. |
| C04 | MD 97–103; JSON `binaryValidation` | Make both parsers executable strict validators: bounded NUL strings/properties; first-only `Vers` with its four remaining fields zero; exactly all-zero 21-byte terminator; exact/unique member set and order; reserved zero for this fixture; checked `UInt64`/Python ranges; `dataEnd==footerStart`; exact 21-byte footer, no trailing byte, independently streamed SHA-1 over bytes before the footer; fixed-buffer SHA-256 for every member/source. Prohibit `ReadAllBytes`, `read(size)`, and buffers sized from multi-GiB fields. Hash both parser implementations. |
| C05 | MD 44–56, 87–93, 137–151; JSON packaging/probe | Hyphenated prefixes add a documented cross-game character confound. Map case IDs to underscore tokens and use `PBOBoundary\<token>` plus legal `PBOBoundary_<token>` patch classes. Boundary config: `requiredAddons[]={}` and no scripts. Probe prefix `PBOBoundaryProbe`; `CfgPatches PBOBoundary_Probe` requires only `DZ_Data`; `CfgMods` depends on `Mission` and loads `PBOBoundaryProbe/scripts/5_Mission`; source is `probe-source/scripts/5_Mission/PBOBoundaryProbe.c`. It must have no boundary type dependency. |
| C06 | MD 137–151; JSON probe | The fixed probe must try seven literal `/` virtual paths via `OpenFile`/bounded `ReadFile`/`CloseFile`, require exactly one open, require the expected case, and compare exact bytes/nonce with the selected PBO parser receipt. Zero, multiple, or wrong-case opens never emit success. RPT and script log are two copies of one `Print` execution, not two experiments. |
| C07 | MD 125–151; JSON `secondsPerCase` | The retained small run reached its marker about 20.8 s after process start; large timing is unknown. A 45 s absence is only `timeout_no_marker`, never numeric-limit evidence. A longer/exact retry needs the existing sourced falsifiable-cause gate. Fresh profile/log files must be created after recorded start, and both exact blocks must carry the same run nonce and receipt/PBO identity. |
| C08 | MD 123, 151–164; JSON runtime/resource policy | `run-case.ps1` records only root PID and calls parameterless `Kill()`. Add a Windows job/process-tree layer: record root and descendant PID + creation time, sample tree private/working bytes and disk/memory, terminate only captured identities using entire-tree behavior, wait for every observed identity, and prove none remains. Apply this to Addon Builder/FileBank/signers and DayZ; preserve crash artifacts first. |
| C09 | MD 155–164; JSON resource/retention | Require a new nonexistent case root and fresh profile/storage/log roots. Reject `ReparsePoint` in the run root, target, or existing ancestors; resolve targets rather than trusting `Resolve-Path`/`GetFullPath`; require one hard link under the owned root for fillers; record logical and allocated length; reject sparse/compressed/reparse/hard-linked sources. Project retained and transient copies before each stage and enforce the 40 GiB cap continuously. Cleanup uses only literal canonical receipt paths and verifies absence. |
| C10 | MD 95–117, 170–176; JSON outcomes/trial budget | Preserve separate source, Builder, parser A/B, BankRev, signer, signature-check, and runtime outcomes. Tool nonzero/error text does not rewrite `parserValid`; preserve and parse any exact artifact. Conversely, small control must pass every stage—including exact BankRev, unchanged signed PBO, exactly one DSCheck `is OK`, and runtime read—before any large case. No manual PBO substitutes in this wave. |
| C11 | MD 19–26, 58–60; JSON exclusions | This stored-only wave cannot complete compressed `OriginalSize`, compressed `DataSize`, decompression allocation, or mixed cumulative boundaries. List them explicitly unresolved after execution. |
| C12 | JSON installed tools/source ledger | Record `AddonBuilder.exe.config`, `logger.xml`, `PboUtils/exclude.lst`, `FileBank.exe`, and both discovered 1.0.240.639 per-user `user.config` files. Record which config was effective where observable; otherwise state unresolved and neutralize relevant settings with explicit argv/include/exclude inputs. |

### Accepted or accepted with scope

- `C13`: reviewed reverse-engineered/third-party layouts have separate `UInt32` member fields, a normally-zero reserved field rather than physical offset, sequential payloads, and therefore need wider cumulative arithmetic. This is not native source proof.
- `C14`: `member-u32-max` is runtime-eligible only after exact official-tool validation; `member-u32-plus1` is tool-only and never becomes a manually wrapped or runtime archive.
- `C15`: stage-specific tool/parser/runtime/distribution outcomes and finite-success claim limits are conceptually correct.
- `C16`: two independently implemented parsers, streaming identity, tiny exact read, sequential wave, retry ceiling, crash retention, and no binary search are sound after the rejected details are repaired.
- `C17`: excluding compression is acceptable only while every compression-boundary question remains unresolved.

---

## Reopened source ledger

| Source | Lines/symbols reopened | Exact provenance | Scope |
|---|---|---|---|
| `D:/StarDZ/docs/REFERENCIA_LIMITES_E_MUROS.md` | 224–231 | `726033DB527944DF57EED0767FB2F0329AB65438B3D48E6247E19D98DAE18EA0` | historical lead only |
| `D:/StarDZ/docs/GUIA_FERRAMENTAS_E_BUILD.md` | 793–839, 1631–1671, 1910–1979 | `2ECAC825A7CC0995A2A97F5040CA26291A484E2CB5F5E42EBCC0195C5E9367D9` | historical lead/access limits |
| `D:/StarDZ/dev.py` | 35–45, 238–267, 384–403, 831–881, 1211–1258 | `E6862C2AB958B734B5A95B6FD3A0BA6B9B3AA066069188804A4BB2A0C23CC64F` | fallible beta policy, not native proof |
| `D:/DayZ Projects/scripts.txt`; `pboapi.c`; `ensystem.c` | metadata; `GetPBOVersion`; `FileMode`/`OpenFile`/`ReadFile`/`CloseFile` 382–443 | `E45D...F55F`; `9C4B...6A61`; `8BE6...188` | extracted version 124588; API declarations, no limit |
| `examples/en/multi-pbo/build.ps1`; `TEMP/multi-pbo-confirmation/run-case.ps1` | build 10–135; run 15–98 | `38F24D...956`; `FBAC12...E55` | exact prior helpers; no process tree |
| Retained `PBOExample_Data.pbo` | parsed `H=151`; members `(method,OriginalSize,DataSize)=(0,0,188),(0,0,81)`; data/footer 420; length 441; matching SHA-1 `B451...115` | PBO `1CE4ADB9D28C778E083CA506E0042217CE6A68FF2EC7FC085E2E19596D619071` | direct installed-Builder control |
| Retained runtime process/RPT and exact probe source | start `03:31:40.107Z`; marker local clock `00:32:00.912`; module config/script | process `1C38...2B68`; RPT `48D4...FC5`; config `3426...0D4`; script `FAF4...9C2` | about 20.8 s small-fixture timing only |
| Installed binaries/config | DayZDiag 1.29.0.163709; Tools build 23909709; AddonBuilder 1.0.240.639; BankRev 1.0.0.2; FileBank/sign/check; exe config/logger/exclude/two user configs | exact hashes are in companion JSON; inspected 2026-09-14 | proprietary sources unavailable; effective user config unresolved |
| armake2 `src/pbo.rs` | 18–25, 52–70, 97–142, 221–281 | commit `3cc3362101900ff41504db3e780dd1625634cf94`; `BEC43A...549`; existing checkout, origin GitHub | third-party only |
| HEMTT PBO `header.rs`, `file.rs`, `read.rs`, `write.rs` | u32 fields, u64 offsets, >u32 rejection, whole-member write buffer | commit `bf2168ce03d5bb8bd3849090e9b2996402624b1c`; hashes `D3D8...B66`,`77E5...1E2`,`9A8C...F53`,`CBCB...45F`; pinned raw HTTP 200 | third-party Arma tooling |
| armake `build.c`, `unpack.c` | 76–198; 53–121/195–263 | commit `e4940fae0d28c4dd07d9d2c591f8e056545fee3f`; `C68E...012`,`71D4...505`; pinned raw HTTP 200 | signed/platform hazards only |
| Bohemia wiki PBO, Addon Builder, DayZ Modding Structure, Arma 3 Creating an Addon | indexed content reopened 2026-09-14 | direct pages returned HTTP 403; URLs and disposition in JSON | PBO page explicitly unofficial/reverse-engineered; no official numeric ceiling found |

No retained historical failing PBO/log/dump/version receipt was found. No source reopened here is an official native PBO specification; parser/tool signing success cannot imply engine support.

---

## Remaining unresolved

- Native DayZ per-member, total archive, cumulative position, allocation, and footer limits on `1.29.0.163709`.
- Whether any current stage treats stored `DataSize` as signed at `2^31`.
- All eight actual tool/parser/runtime outcomes and physical offsets.
- All compressed layouts, client/signature-enforcement, Workshop/distribution, other filesystems, and other builds.
- Effective selection between the two installed per-user Addon Builder configurations.

