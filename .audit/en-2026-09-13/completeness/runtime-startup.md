# Stable DayZDiag Startup Diagnosis and Runtime Probes

> **Status:** The stable diagnostic executable started and compiled isolated probe PBOs after correcting the launcher argument shape. This is build-specific evidence for DayZ `1.29.0.163709`, not a general engine-version guarantee.

## Scope and integrity

- Audited executable: `D:\SteamLibrary\steamapps\common\DayZ\DayZDiag_x64.exe`, product version `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`, executable timestamp `2026-08-13 04:52:12` local as recorded by its RPT.
- Packer: `D:\SteamLibrary\steamapps\common\DayZ Experimental Tools\Bin\PboUtils\FileBank.exe`, SHA-256 `F89AAEB22421B9158FBBF173F75D52B6F3DE69986CB462E58956C78DA82C4CAF`. Each reported PBO packing run exited `0`; runtime compilation, rather than FileBank's exit code, establishes whether the contained Enforce Script compiled.
- Owned workspace: [`TEMP/wiki-runtime-probes`](../../../TEMP/wiki-runtime-probes/README.md). No English page, previous audit record, installed-game file, user server, or production save was changed.
- All launched DayZDiag processes were locally owned and stopped or observed terminated: `40308`, `37672`, `16340`, `44964`, `48644`, `48612`, `49820`, `24008`, `42660`, `3884`, `46224`, `15196`, `45752`, `37412`, and `14680`. The closeout check found no `DayZDiag_x64`, `DayZServer_x64`, or `FileBank` process.

The prior reports remain byte-for-byte unchanged: `runtime-probes.md` SHA-256 `0FAD140CE47CBAE7A3D055118BCD8407735587DCD3E0045AFBA23D42387B5FDA` and `runtime-probes.json` SHA-256 `23D47A37AFD677F1E7FB6C4119F4EE1E59819C5B0AF5628E0F3F56C2EAB173E0`.

## Startup obstacle

The obstacle was the tested PowerShell launcher argument shape, not demonstrated Steam, modal-dialog, or executable incompatibility.

1. PID `40308` reproduced the stalled launch with the literal argument `-profiles="D:\StarDZ\docs\wiki\TEMP\wiki-runtime-probes\profiles\startup-diag-client"`. After five seconds it had consumed `0.09375` CPU seconds, used approximately 32 MiB working set, created no profile, and exposed no top-level window.
2. WMI preserved the inner quotes in that PID's command line. Suspending its main thread (`39948`) and reading its context/memory found the exact NUL-terminated string `"D:\StarDZ\docs\wiki\TEMP\wiki-runtime-probes\profiles\startup-diag-client"\DataCache\cache_lock`; the quote characters were part of the path the process was using.
3. The main thread was in Windows `Wait/ExecutionDelay`. Static inspection around DayZDiag RVA `0x69956` showed the observed path-open retry path calling RVA `0x37F960` with `ECX=0x3E8` before jumping back, consistent with a one-second wait/retry loop. This disassembly supports the live path observation; it is not, by itself, a public API contract.
4. PID `37672` was then launched with a single quote-free argument value, `-profiles=D:\StarDZ\docs\wiki\TEMP\wiki-runtime-probes\profiles\startup-corrected-client`. It accumulated `54.4` CPU seconds, used roughly 2 GiB working set, created a fresh RPT and script log in that directory, and exposed a DayZ window.
5. OS-level inspection found no window for the stalled PID and a normal DayZ window for the corrected PID; it found no intervening Steam or loader modal. `WindowStyle=Hidden` did not prevent the GUI executable from later creating that window.

Use `ProcessStartInfo.ArgumentList` and add each complete option as one argument without literal quote characters, as recorded in the harness README. This finding is specifically about `-profiles="..."` as passed by the tested launcher. It does not contradict Bohemia's batch examples, which quote the whole argument, for example `"-mod=P:\Mods\@FirstMod"`.

One intermediate PID (`44964`) exposed a second harness error: a dynamically constructed call added `-profiles=` and the directory as two arguments. Its WMI command line contained `-profiles= D:\...`, so logs went to `%LOCALAPPDATA%\DayZ` rather than the isolated profile. The two newly created owned logs were copied to `profiles/baseline-arglist-bug/` (RPT SHA-256 `53938D1DBDF7BC730CBEA6989A62615B6E96F6474FCBF56B0583FC19A25B10DA`; script-log SHA-256 `E4A56BA4BBB4E6BFCD90C87EFF8871E5018CCE0A295484CC28DA2F77F0E3B3A4`) and only those exact two originals were deleted; a closeout check confirmed both originals absent.

## Harness correction

The original baseline put an omitted-`override` case in the same Mission module as all positive probes. On the first corrected launch (PID `16340`), `profiles/baseline-corrected/script_2026-09-13_20-21-01.log`, line 9, reported `Overriding function 'Label' but not marked as 'override'`, and line 10 reported `Can't compile "Mission" script module!`. That compile error prevented every intended runtime marker.

The baseline child method now explicitly uses `override`, and the omitted-`override` case is its own PBO. The rebuilt baseline PBO is 1,974 bytes with SHA-256 `B2C059E3D239DC57367E6D21E6FA2A4D83043991E8436A6917A01475132FC7F0`; the isolated omitted-override PBO is 999 bytes with SHA-256 `7D398952953952314002346ACE4861782551B2D678237B6FF560FBA192D41A1B`.

## Runtime and compiler results

Each case ran alone with a separate `-mod` and `-profiles` path. The first lines of every cited RPT record the full command line, executable timestamp, and `Version 1.29.163709`.

| Probe | Exact evidence | Bounded conclusion for build `1.29.0.163709` |
|---|---|---|
| Corrected baseline, PID `48644` | `profiles/baseline-isolated/script_2026-09-13_20-25-40.log`, SHA-256 `BABF4385BD4B864FEBF424416118BBF94B8FDF1E899D5A69F1C2234E301F26B3`, lines 36-46; paired RPT SHA-256 `FF324C5188DB2B9E1D178557CA4A45E148E7BF37D73681FD09FC1231B392CFD8` | Mission module compiled and every baseline marker ran. |
| Zero vector normalization | Line 37: `RTP:ZERO:RETURN=0 VALUE=<0.000000, 0.000000, 0.000000>` | `vector.Zero.Normalize()` returned `0` and left this vector zero. The EN statements that it produces NaN are contradicted on this build. |
| Parameterless `typename.Spawn()` | Lines 38-39: constructor marker then `RTP:SPAWN:NONNULL` | A class with a no-argument constructor was instantiated successfully. |
| `Spawn()` with one required scalar parameter, PID `48612` | `profiles/spawn-argument-isolated/script_2026-09-13_20-26-53.log`, SHA-256 `B526A0161D22225B9CAFC9815513FA3746376D0ED89E64919D29EBFFDCE4ECC6`, lines 36-38: `CTOR=0`, then `NONNULL`; PBO SHA-256 `3E09305AD0C6FACD6AA84D82BFD16C941AE4E5E347D6ECC72BB2D554C60FEF84` | `Spawn()` instantiated this class and supplied integer zero. This contradicts a blanket “parameterless constructor only” statement, but does not establish behavior for every constructor signature. |
| Virtual dispatch with `override` | Baseline line 40: `RTP:DISPATCH:child-with-override` through a base-typed variable | The corrected override compiled and dispatched to the child implementation. |
| Omitted `override`, PID `42660` | `profiles/omitted-override-isolated/script_2026-09-13_20-29-22.log`, SHA-256 `4E432020840281FCB59324A1DEFD600F6F137B9A9925CA3413DFDECF17AAB4D4`, lines 9-10; PBO SHA-256 `7D398952953952314002346ACE4861782551B2D678237B6FF560FBA192D41A1B` | The compiler rejected the override; it was not merely a warning and did not create an unrelated new method. |
| `autoptr` inner lexical block | Baseline lines 41-43: `ALIAS_ASSIGNED`, `POST_SCOPE`, then `DESTRUCTOR` | In this function, the destructor ran after the print following the inner braces, on function exit. This does not safely establish all alias/dereference behavior or all scopes. |
| Static field in one callback | Baseline lines 44-45: counter `1`, then `2` | The static field retained state across two immediate calls in the same callback/process. Mission-restart persistence remains untested. |
| `Object.IsDeleted()`, PID `49820` | `profiles/object-isdeleted-isolated/script_2026-09-13_20-27-49.log`, SHA-256 `FC4027982D586892A721CBDCEA5EF019F1EFD61F47581626EE4CCAFCB838090B`, lines 9-10: `Undefined function 'Object.IsDeleted'`; PBO SHA-256 `F7455CD8C92A72C8457E2CE93B7EE6AFA8B7D4BA9CA4B9186B2540D531C6ADA7` | The tested instance call is not declared for `Object` and prevents Mission-module compilation. This does not prove every possible deletion-detection claim. |
| Bare global `Print`, PID `24008` | `profiles/global-print-isolated/script_2026-09-13_20-28-38.log`, SHA-256 `9BB9FA292E40CEFF294E507A9B2221CD4C4D7701BE4C98A8D2453B0C9E5D4572`, lines 9-10: source line 1 `Syntax error`; PBO SHA-256 `D683C827DBD6FBF2A080A9A165E63521E8183B31C4A5504337AA1E899D182768` | A bare top-level call statement was rejected. This does not mean globally declared functions or types are illegal. |

Candidate EN repairs, not made under this task's ownership, are:

- `en/01-enforce-script/07-math-vectors.md:664` and `:700` for zero normalization.
- `en/01-enforce-script/09-casting-reflection.md:313` and `:582` for the blanket `Spawn()` constructor restriction.
- `en/01-enforce-script/03-classes-inheritance.md:901` and `en/01-enforce-script/13-functions-methods.md:746`, `:1059`, and `:1068` for omitted `override` being described as warning/new-method behavior.
- Static-restart, ownership, and deletion guidance needs wording limited to what the probes actually establish rather than extrapolation from one marker sequence.

## Stable diagnostic server result

Bohemia's current `DayZ:Workbench Script Debugging` page says `DayZDiag_x64.exe` can act as a client or server when `-server` is added. `DayZ:Modding Basics` also publishes a diagnostic multiplayer-server command, and `DayZ:Server Configuration` documents server startup parameters. These official indexed pages were consulted on 2026-09-13: [Workbench Script Debugging](https://community.bistudio.com/wiki/DayZ%3AWorkbench_Script_Debugging), [Modding Basics](https://community.bistudio.com/wiki/DayZ%3AModding_Basics), and [Server Configuration](https://community.bistudio.com/wiki/DayZ%3AServer_Configuration). Direct page retrieval had previously returned HTTP 403, so the indexed official text and local snapshots were used transparently rather than representing a blocked direct fetch as opened content.

Local fallible snapshots corroborate the two launch examples: `D:\StarDZ\docs\DayZ\Workbench Script Debugging.md` SHA-256 `2E46B120066884C1D2EE5B10705D4214C35DFB08B69249100E7DF00F10146F16`, especially line 51, and `D:\StarDZ\docs\DayZ\Modding Basics.md` SHA-256 `1A0B2C1F7A69E369E74D923CB77D4716B9DD21941B0C02DA5015FA7F708B5839`, especially lines 157 and 172. These snapshots are supporting leads, not substitutes for version-specific runtime evidence.

PID `3884` launched the stable executable with `-server -ip=127.0.0.1 -port=24042`, isolated profiles/storage, and the disposable config. Its script log, `profiles/stable-server-local2/script_2026-09-13_20-32-07.log` (SHA-256 `8BCE0F51517FF0C0DCE676707E387DF24A8486CF810880586FDE8883FC3E5DE1`), loaded GameLib, Game, and World with `SERVER_FOR_WINDOWS`, `SERVER`, `NO_GUI`, and `NO_GUI_INGAME` defines. Its RPT (SHA-256 `A5586DCAD4439F17297C0E69342FE9FB70AAF032E65F642A775C89B7D273E3D0`) recorded the exact `-server` command, counted down termination at lines 436-445, and recorded successful termination at line 449.

A separate `server-context` PBO (SHA-256 `83CBDBD50A1C2CBEAE2343875A340E6BEC10EDF9A5166403457AB429253A701F`) attempted to print an `RTP:SERVER:BEGIN` marker from `MissionServer.OnInit`. Attempts used both the minimal disposable mission and a shallow checkout of the official Central Economy repository pinned at commit `9a21bb9f5fb9c62a7ce2761402196091588133e6` (commit date `2026-08-13T17:46:30+02:00`). The best retained attempts loaded only through World, then terminated; neither loaded the Mission module nor emitted the marker. No listening endpoint or completed mission context is claimed. The missing mission startup is unresolved, and absence in a single endpoint snapshot is not treated as proof that stable diagnostic server mode cannot listen.

## Corrections to the previous report

The previous report correctly refused to mark behavior probes passed without logs, but two explanations must not be carried forward:

- Its statement that the no-log `-autotest` result was “consistent with an execution environment that never reached the extracted script path” was an unsupported inference. The exact defect was the literal quoted profile path, after which the corrected executable reached scripts normally.
- Its stable-server note emphasized the absence of a separate stable server executable and left stable listen semantics untested. That inventory observation is not evidence of server unavailability: official documentation identifies stable `DayZDiag_x64.exe -server`, and the local run proved stable server-mode defines and orderly server-mode termination. A listening mission still remains unverified.

The raw `scripts.txt` metadata snapshots were not translated into game build numbers: `D:\StarDZ\docs\vanilla_metadata\scripts.txt` contains `version=121029`, while `D:\DayZ Projects\scripts.txt` contains `version=124588`. They are distinct snapshots and neither field was used as proof of runtime version.

## Remaining limits

- Results apply only to the hashed stable diagnostic executable and the exact hashed sources/PBOs/logs captured in `runtime-startup.json`.
- No mission reload was performed, so static lifetime across restart is unresolved.
- No stale alias was dereferenced; only destructor ordering was observed for the tested `autoptr` function.
- No usable stable MissionServer/listener context was reached. The server startup prerequisite or mission-path issue still needs an independently validated reproduction.
- No VitePress build was run because this task did not change EN or shared site configuration. The runtime logs validate Enforce compilation/runtime for the listed cases, not documentation rendering or gameplay semantics.
