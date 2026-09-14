# EDDS fixture repair exact-final council

**Reviewed:** 2026-09-14 America/Sao_Paulo  
**Review revision:** `d795fca51eca92781a4dbdfc89d753790569fb4d`  
**Role:** independent Codex reviewer, Orca dispatch `task_78c05615c58f`  
**Disposition:** **Rejected with blocking repairs; do not open Workbench or import yet.**

The repaired layout, mission lifecycle, structural EDDS verifier, exact BankRev parser, current hashes, and bounded claims are substantially improved. The final gate still fails because `build.ps1` accepts a caller `WorkRoot` reached through a reparse-point ancestor that physically aliases the fixture source, the final operator-facing fallback instructions omit required decision and cleanup gates, and the active fixture retains stale bytecode for the rejected verifier. No Workbench, native converter, Addon Builder, BankRev, compiler, wiki build/dev server, game, client, or server was started.

## Council decisions

| ID | Decision | Exact result |
|---|---|---|
| EF-01 | Accept, no regression | The inspected generator reproduced the current `135`-byte PNG in memory byte-for-byte. Current and preserved rejected-fixture SHA-256 are both `EDB68FB0779781BF8F672D2595897EB870792675EB576BDDDF08E4E231B7522C`. |
| EF-02 | Accept, bounded, no regression | `config.cpp` and the imageset remain byte-identical to the preserved version. `DZ_Scripts`, the client module registration, atlas names/rectangles, and case agree; the plain EDDS path remains an unobserved hypothesis. |
| EF-03 | Accept, static | Both `ImageWidget`s declare clamp and `stretch_w_h`. `ProbeAlpha` spans absolute x `[84,212)`; its adjacent backgrounds split at x `148`. The source cyan region relative x `[4,28)` stretches to absolute x `[100,196)`, crossing both backgrounds, while magenta relative x `[24,28)` stretches to x `[180,196)`, wholly on the light half. The README now says exactly that. |
| EF-04 | Accept, static; runtime pending | `m_EDDSProbeRoot` persists ownership; duplicate `OnInit` returns; either missing cast unlinks and nulls the partial root; left/alpha load results are distinct; `SetImage(0)` results are logged separately; teardown calls `super.OnMissionFinish()`, unlinks/nulls the root, and emits `EDDSProbe/Teardown`. Reopened native signatures support `CreateWidgets`, `Unlink`, boolean `LoadImageFile`, and boolean `SetImage`; no compile is inferred. |
| EF-05 | Accept, structural only | FourCC is read at `0x54`; legacy/DX10 tables begin at `0x80`/`0x94`; header sizes, exact dimensions, `1..7` mips, every signed-positive `COPY`/`LZ4 ` entry, bounds, and exact EOF are checked. Both synthetic valid structures passed and all nine malformed cases failed. This proves neither native acceptance nor rendering. |
| EF-06 | **Reject, blocking** | Prefix/member parsing and future receipt fields are repaired, but directory safety is not. A `WorkRoot` whose final item was ordinary but whose ancestor was a junction into `source/EDDSProbe` passed all overlap checks and reached tool lookup. |
| EF-07 | Accept source repair; active artifact repair still required | The three superseding extracted-source hashes now match disk, and the verifier source accurately labels non-PNG checks as static text checks. The author reports three negative path checks without retaining their exact commands/output; this council reran them and also found the missed reparse case. The active tree still carries stale pre-repair verifier bytecode (ERFC-03). |
| EF-08 | Project accepted as unobserved proposal; **instructions blocking** | The private `.gproj` has the sourced project/file-system shape, its exact physical root exists, and it remains a legitimate visibility hypothesis. It is not rejected merely because Workbench has never opened it. The overall preparation is not safe to authorize because the runtime README sequence is incomplete (details below). |
| EF-09 | Accept, no regression | No `probe_ui.edds`, no `probe_ui.edds.meta`, and no brace-form 16-hex resource identity exist. The source PNG is unchanged. A GUID used only for a future private run-directory suffix is not claimed as a Workbench resource identity. |

## Blocking repairs

### ERFC-01: reparse-ancestor WorkRoot bypass

`Require-OrdinaryDirectory` at `build.ps1:18-23` checks only the final item. `Test-PathsOverlap` at lines 31-34 then compares lexical paths. The inspected evidence script created an owned temporary junction whose target was the exact fixture source and supplied its ordinary `GUI` child as `WorkRoot`:

```text
lexical WorkRoot:
D:\StarDZ\docs\wiki\TEMP\edds-fixture-repair-council\junction-check\source-alias\GUI

physical target:
D:\StarDZ\docs\wiki\examples\en\edds-probe\source\EDDSProbe\GUI
```

The helper did not emit either overlap error. It continued to `Require-File` and failed only because the deliberately empty fake tool root had no `AddonBuilder.exe`. No native executable started. This demonstrates that a future `runRoot` and Addon Builder `-clear` temp directory could be created physically inside the source despite the lexical safety checks.

Repair it before import: reject reparse points in every existing path component for fixture/source/work/tool roots, or use a demonstrated canonical physical-target resolution and compare physical equality plus both ancestor directions before creating `runRoot`. Retain a negative test proving that a `WorkRoot` below a reparse ancestor targeting `SourceRoot` fails before tool lookup.

### ERFC-02: incomplete operator-facing visibility/fallback sequence

`examples/en/edds-probe/README.md:24` says visibility is unresolved, but line 26 immediately instructs the import without an explicit stop-on-absence condition. `TEMP/edds-fixture-preparation/README.md:7` allows a mapping when `P:` is absent and says the mechanism is not prescribed; it omits the prior council's prerequisites of a captured direct-project failure, positive checks from both `Get-PSDrive P` and `subst`, a separate fallback `.gproj`, target recheck, and exact `subst P: /D` cleanup.

Make the runtime instructions self-contained and ordered:

1. Hash and open only the exact private project first.
2. Import nothing unless Resource Manager visibly shows the exact `EDDSProbe/GUI/imagesets/probe_ui.png`; capture the visibility evidence.
3. On direct-project failure, capture the error and stop that attempt.
4. Only after both `Get-PSDrive P` and `subst` positively show `P:` absent, create the owned `subst P: D:\StarDZ\docs\wiki\examples\en\edds-probe\source` mapping and use a separate fallback project naming `P:/`.
5. Before cleanup, recheck that `P:` still targets exactly that owned source root, then remove only it with `subst P: /D`. Never edit the installed `dayz.gproj`.
6. Keep the remaining bound: one default PNG import, structural inspection, one pack and one baseline client render; permit at most one source-supported objective reference/pack correction.

### ERFC-03: active stale verifier bytecode

The current `scripts/__pycache__/verify_preparation.cpython-314.pyc` is byte-identical to the preserved rejected fixture. Its Python 3.14 timestamp header records a source size of `7224`, while repaired `verify_preparation.py` is `11423` bytes; its unmarshalled top-level names omit `verify_edds_bytes`, `synthetic_edds`, and `run_self_tests`. Normal source execution will invalidate this cache, and this council did not execute it, but direct bytecode execution would still expose the rejected EF-05 verifier. Remove stale generated `__pycache__` artifacts from the active fixture and record the resulting inventory; do not regenerate or retain bytecode as a deliverable.

## BankRev parser and future receipt

This council did not merely search for `-properties` and `-logFull`. It extracted `ConvertTo-NormalizedVirtualPath`, `Get-NonEmptyLines`, `Get-BankRevMemberLines`, and `Assert-ExactMemberSet` from the actual `build.ps1` AST and ran them against retained native-tool lines:

```text
prefix = PBOExample\Data\
product = dayz ugc

PBOExample\Data\data\example.txt
PBOExample\Data\config.cpp
```

The property expression normalized the exact prefix once; the member parser returned exactly `data/example.txt` and `config.cpp`. The same functions accepted the complete seven-line EDDS manifest including `probe_ui.png` and rejected a `config.cpp.extra` substring substitution, a line outside the prefix boundary, and a duplicate normalized member.

The future argv and receipt are otherwise sound in scope: `-packonly`, `-clear`, private `-temp`, exact `-prefix=EDDSProbe`, `-properties`, `-logFull`, source hashes, executable paths/versions/hashes, raw outputs, log hashes/lines, PBO hash, required seven-member set, and observed original member lines are all represented. `-packonly` is correctly described as packaging rather than config parsing or Enforce compilation.

The repair receipt's statement that three path-negative runs passed has no durable author command/output receipt. Independent reruns confirmed non-exact `SourceRoot`, source/work equality, and a lexical source ancestor all fail before tool lookup, but those cases did not cover the reparse-ancestor bypass.

## Reopened native and pinned evidence

- `D:/DayZ Projects/scripts/config.cpp:1-9`, SHA-256 `F086DB66CDE5E60089C78FF170AA0488F5ABF7ABB37E6C13D404116D6D05A90A`: `CfgPatches/DZ_Scripts`.
- `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c:57-84,168-181,247-267`, SHA-256 `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E`: `SOURCEALPHA`, `BLEND`, `STRETCH`, `Widget.Unlink`, `WorkspaceWidget.CreateWidgets`, `bool LoadImageFile`, and `bool SetImage`.
- `D:/DayZ Projects/scripts/5_mission/mission/missiongameplay.c:96-125,257-276`, SHA-256 `E0A215D9E10300503CBC17F7A44BBABF58A2D1EF5CBB268D3DA1D279DC75C96A`: vanilla `OnInit`/`OnMissionFinish` signatures and initialization/teardown context.
- `D:/DayZ Projects/gui/layouts/day_z_hud_cars.layout:23-38`, SHA-256 `6E2893932679783D2618A9A63603966B83EEA225D1EF933301726C4B1068D7B2`: native blend/source-alpha/clamp/`stretch_w_h` layout precedent.
- `D:/DayZ Projects/gui/imagesets/dayz_gui.imageset:1-25`, SHA-256 `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A`: descriptor, texture and rectangle shape.
- Pinned CF checkout `0763e7e7548c9a0bed6626afff835de80693ebf3`, `JM/CF/Scripts/5_Mission/CommunityFramework/Mission/MissionGameplay.c:11-16`, SHA-256 `F064E36874A81356661F19D05941C86BF985509A536107ED65CEE392D98F46EA`: `OnMissionFinish` calls `super` before framework teardown. Its `JM/CF/Workbench/dayz.gproj` SHA-256 remains `B9198EDDA2A7620C967F0DEBCAAB61DA261108E018BF45734936B0FCB73C757F`; the checkout HEAD is exact and clean.
- Pinned Dabs checkout `fd859fd891f45a4a9c9089597db0c621ef3a9de5` is clean. `DabsFramework/GUI/icons/brands.imageset:1-16` SHA-256 `1DE25A2BA41771632814F126C2C326B5D8A2F1DF74BEA2344CF56120081D101D` uses a plain EDDS path; `DabsFramework/Scripts/config.cpp` SHA-256 `74E0CC3791ADD0F6F7E650162B3BD96D2F8188A9F130209965AAE00E26D372D1` registers image sets/modules; `DabsFramework/Workbench/dayz.gproj` SHA-256 `08C1582CE459451D71D61C53C45BF78383405F225456C25D15ACFA2CF4F4791D` shows a full project, not a requirement that every block is needed for import-only visibility.
- Installed `D:/SteamLibrary/steamapps/common/DayZ Experimental Tools/Bin/Workbench/dayz.gproj`, SHA-256 `269DAAD629D0007176B4B81ADFB52740A23A11955C24C414B82727F15EE41928`, was reopened without editing. `WorkbenchApp.exe` is version `1.29.163.401`, SHA-256 `B61D240394845EF9EAB3B5F459D487B50DBF3C42713FB9E9E50CE945F5A894C6`.
- Installed but unstarted Addon Builder is version `1.0.240.639`, SHA-256 `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`; BankRev is version `1.0.0.2`, SHA-256 `2C35799EB437DEACB3720F8D322A399D935739537EBA335839E873AA21A26A75`.

## EDDS byte-layout reopen

The legacy `pond_moss_ca.edds` is `984326` bytes, SHA-256 `2EAADDF7EBB52B90E47212A0200E050E55BA4AD7599F47974C31767853D0676E`. It has DDS header size `124`, pixel-format size `32`, zero FourCC bytes at `0x54`, 10 mips, table `[0x80,0xD0)`, positive `COPY`/`LZ4 ` blocks totaling `984118`, and payload end `984326`, exactly EOF.

The DX10 `dayzwater1_no.edds` is `1398364` bytes, SHA-256 `4DA58F017C48244E676F42E3D3B13A01B5B45A68335EB60869507D376FB8F9B0`. It has header sizes `124`/`32`, `DX10` at `0x54`, 11 mips, table `[0x94,0xEC)`, positive `COPY` blocks totaling `1398128`, and payload end `1398364`, exactly EOF. These source files validate table selection and bounded arithmetic; they are not 64x32 probe outputs and were not passed off as import results.

## Exact current hashes

| Current artifact | Bytes | SHA-256 |
|---|---:|---|
| `examples/en/edds-probe/README.md` | 5347 | `C41D2A33F41CBB52F6659741EB2143CEF9D00A1970FDD9A1785E4A50817ED0EF` |
| `examples/en/edds-probe/build.ps1` | 10523 | `FBE7B49D683A9F77789D073FC84D31825EE604CEE53AA57525565380752A0FA3` |
| `scripts/generate_probe_png.py` | 1737 | `117D1A2D40F7F460E8960E5986ED6DF47BB2209676449ED925E85F98C7831BF3` |
| `scripts/verify_preparation.py` | 11423 | `7E2D1E06D30AF1B04D8C622C9E1B88B4F31E94F0FB875555E2EC7F58353C7581` |
| `scripts/verify_build_ast.ps1` | 1683 | `1331A4706F19014C96758A287BE4BE3DAF094F96ED99E37D454CE94A985C4F45` |
| `scripts/__pycache__/generate_probe_png.cpython-314.pyc` | 3668 | `C8D3E5F8F74B4ED5A6C33734E2D6CCC6DEEADA623923B8A5B19CB51328B9C9FF` |
| `scripts/__pycache__/verify_preparation.cpython-314.pyc` | 12823 | `7C2D5DD1341E511423D7DB79E63026E1DBA76778858D360B107394DC6F04882A` |
| `source/EDDSProbe/config.cpp` | 560 | `A399BA5FF8E4C10C113F4021400FA292BDE065A85C2802FF7A512860872E8CA9` |
| `source/EDDSProbe/GUI/imagesets/probe_ui.imageset` | 504 | `B4D648347F441E58466923F427D2BD97DDC6D47FCBE419B3922A9EF5B5140A98` |
| `source/EDDSProbe/GUI/imagesets/probe_ui.png` | 135 | `EDB68FB0779781BF8F672D2595897EB870792675EB576BDDDF08E4E231B7522C` |
| `source/EDDSProbe/GUI/layouts/probe_ui.layout` | 1092 | `0A4C807F438FD7C655D3E077D36B4287AD4FA0E54C99D7DF5DB1F4E3D759B4A7` |
| `source/EDDSProbe/Scripts/5_Mission/EDDSProbeMission.c` | 1511 | `8F8E9B345618387BFFFD5AF08959624C73F73C9972940E17E59E66FDB444976F` |
| `TEMP/edds-fixture-preparation/EDDSProbe.gproj` | 392 | `A5632B06E21C4E87CA56BB51DFA4BEF7997C4881FF87B36D55D8E8AB90C03598` |
| `TEMP/edds-fixture-preparation/README.md` | 1223 | `904AF137EDF81FD01A68493EB82899A872141607079D41368A9C220CAD3E1CA6` |

The two `__pycache__` files were not executed; all verifier runs used `python -B` against source. The generator cache matches its current source header, but the verifier cache is stale pre-repair code as described in ERFC-03. The repair receipt's listed source-artifact hashes match current disk.

The three corrected extracted hashes are exact:

| Source | SHA-256 |
|---|---|
| `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c` | `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E` |
| `D:/DayZ Projects/scripts/5_mission/mission/missiongameplay.c` | `E0A215D9E10300503CBC17F7A44BBABF58A2D1EF5CBB268D3DA1D279DC75C96A` |
| `D:/DayZ Projects/gui/layouts/day_z_hud_cars.layout` | `6E2893932679783D2618A9A63603966B83EEA225D1EF933301726C4B1068D7B2` |

## Final diff against the preserved rejection

The preserved manifest is `TEMP/edds-fixture-rejected-20260914-0703/preservation.json`, SHA-256 `16E4F202019FC5052C010AF29BEF0B2D61D7E9C0F6B2E5A9D5C5D487CEED29A8`. Exact `git diff --no-index` review found intended changes only in `README.md`, `build.ps1`, `verify_preparation.py`, `probe_ui.layout`, and `EDDSProbeMission.c`, plus the new `verify_build_ast.ps1`. Generator, PNG, config, imageset, private project, and both preserved bytecode files remain hash-identical. The PNG remains unchanged at the source-pixel level.

## Commands and observed results

- `python -B examples/en/edds-probe/scripts/verify_preparation.py` — exit `0`; PNG/text checks passed and generated EDDS/meta absence passed.
- `python -B examples/en/edds-probe/scripts/verify_preparation.py --self-test` — exit `0`; two valid synthetic structures accepted and nine malformed cases rejected.
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/en/edds-probe/scripts/verify_build_ast.ps1` — exit `0`; parsed 84 command expressions. This is syntax/static shape only.
- In-memory execution of the inspected PNG generator functions under `python -B` — generated bytes equal current PNG, `135` bytes, expected SHA-256.
- Read-only PowerShell byte inspection of both cited native EDDS files — confirmed `0x54` FourCC selection, all table entries, positive sizes, table bounds, summed payloads, and exact EOF.
- `powershell -NoProfile -ExecutionPolicy Bypass -File TEMP/edds-fixture-repair-council/parser-and-path-check.ps1` — exit `0`; actual retained BankRev syntax and exact-member negatives passed, while the reparse-ancestor alias reached tool lookup and proved ERFC-01. The validated junction and empty owned test root were removed; the source PNG remained present.
- Three direct safe helper invocations — non-exact source, source/work equality, and lexical source ancestor each rejected before tool lookup.
- `Get-PSDrive P` and `subst` — both showed `P:` absent at review time. No mapping was created outside the owned temporary junction test.
- Hash and brace-pattern checks — no generated EDDS/meta and no invented resource identity found; current PNG equals preserved PNG.

Detailed machine-readable evidence is in `TEMP/edds-fixture-repair-council/verification.json`; the inspected test source is beside it. Its test root cleans itself and launches no native DayZ tool.

## Bounded observation decision

The private project remains a sourced but unobserved mount proposal. Its exact syntax/root are reasonable enough to remain the first visibility hypothesis, and absence of a prior Workbench launch is not grounds for rejection. The **complete final preparation is not yet sound enough to authorize that observation** because ERFC-01 and ERFC-02 are blocking; repair and independently rereview them before any import.

After acceptance, the approved observation remains narrowly bounded: direct private-project visibility first; one default import only after the exact source is visible; structural output inspection; one pack with exact prefix/seven-member proof; and one baseline client rendering, with at most one source-supported objective resource-reference or packaging correction. A `P:` mapping is fallback-only after captured direct-project failure and dual positive absence checks, uses a separate project, and must receive exact owned cleanup. All native conversion, metadata, resource identity, compilation, package output, and rendering results remain unresolved and must never be inferred from this static review.
