# Multi-PBO Fixture Runtime Evidence

Reviewed and executed 2026-09-14 UTC from repository HEAD `103238a83078784b7ee6cd6486f63d7973e3fe92`. This runtime probe only wrote `TEMP/multi-pbo-runtime/` and this report plus its JSON companion; it did not change `examples/en/multi-pbo`, EN docs, configuration, firewall, accounts, or the game installation.

## Result

The unchanged fixture built successfully with the official DayZ Experimental Tools, producing four final named PBOs, exact BankRev prefix/member records, signatures, and exhaustive DSCheck OK records. The dedicated DayZDiag `1.29.0.163709` main run mounted all four fixture PBOs and reached Mission compilation, but the separate Mission probe failed before `OnInit()` because `PBOExample` and `PBOExampleServer` were unresolved. Therefore this run does not establish the requested function-call markers, server-component result, or data-sentinel read; it is a real fixture-runtime failure rather than a successful multi-PBO resolution result.

## Build and byte evidence

`examples/en/multi-pbo/build.ps1` was run once with the installed tools root `D:\SteamLibrary\steamapps\common\DayZ Experimental Tools` and dedicated work root `D:\StarDZ\docs\wiki\TEMP\multi-pbo-runtime`. It created `pboexample-20260913-222858-1661085b`; its receipt is `TEMP/multi-pbo-runtime/pboexample-20260913-222858-1661085b/receipt.json`.

| Component | Final archive SHA-256 | BankRev prefix/member result |
|---|---|---|
| Core | `A1814154B07343E577EC1270709392B52F131397AE69FAB0B7DF2E22B9BBF963` | `PBOExample/Core`; `PBOExample/Core\config.cpp` |
| Scripts | `83012028B8FF366A41DC3C24934D5F407A826C1E499BAA0AE929F9BFE0049F25` | `PBOExample/Scripts`; `PBOExample/Scripts\scripts\3_game\pboexample.c`, `config.cpp` |
| Data | `5E1B70D38A3999B6CC15B635A4C02F58BA53601BFA901E348DD9B168482F208E` | `PBOExample/Data`; `PBOExample/Data\data\example.txt`, `config.cpp` |
| Server | `EF70F72CD983B7A0628CD80BFC9D23DA31E8714CD42B89624E4E18CE1A6F4501` | `PBOExample/Server`; `PBOExample/Server\scripts\5_mission\pboexampleserver.c`, `config.cpp` |

The exact source sentinel `examples/en/multi-pbo/src/Data/data/example.txt` has SHA-256 `C460C6E58E3051A463E565F55D835469415E3536B9EF6095178D3D60041CB941`; BankRev confirms those bytes were packed under the requested virtual path. The fixture receipt contains the official tool hashes, all signature hashes, member tables, build commands, and the DSCheck stdout proving one expected OK result per `.bisign`.

## Main runtime attempt

The test-only `@MultiPboRuntimeProbe` was built separately (`MultiPboRuntimeProbe.pbo` SHA-256 `6CCE4CFEA58C569C3E499AAEBB7DFB356ADF37A43062826E9EF8D4D5322A94A8`). Its `modded MissionServer.OnInit()` contains calls to `PBOExample.GetFixtureName()`, `PBOExampleServer.IsServerComponent()`, and `OpenFile`/`ReadFile` for exactly `PBOExample/Data/data/example.txt`; its source SHA-256 is `FAF495615C77E372498957487FE63156768B19C1DC2B85CEBE0E801B26E669C2`.

The one 45-second process (PID 59096) used `-mod=<release>/@PBOExample` and `-serverMod=<release>/@PBOExampleServer;<runtime>/@MultiPboRuntimeProbe`, with a private 43-file Central Economy mission, separate profile/storage directories, `instanceId = 26072`, game port `26072`, Steam query port `26073`, and `-ip=127.0.0.1`. Its RPT records fixture PBO mounting and `SteamGameServer_Init(7f000001,8766,26072,26073,3,1.29.163709)`; from 01:31:51 through 01:32:11 UTC the PID owned UDP `127.0.0.1:26072`, `127.0.0.1:26074`, and `0.0.0.0:26073`.

At RPT lines 1420--1421 and script-log lines 9--10 the main run reports `Can't find variable 'PBOExample'` and `Can't find variable 'PBOExampleServer'` in the independent probe. Consequently no `MULTIPBO:RUNTIME:*` markers ran and the data file was not read. The wildcard query socket is reported exactly as observed; no firewall setting was changed and it does not establish public reachability.

## Negative controls

Each control used a separate copied release and separate profile/storage directories, then one bounded 35-second fresh process. No process was restarted or retried.

| Control | Deliberate copy-only change | Observed result |
|---|---|---|
| missing Core | Moved only copied `PBOExample_Core.pbo` and its `.bisign` into `TEMP/multi-pbo-runtime/negative-missing-core-removed/` | PID 60012 did not reach a script-module record, Steam initialization, or an owned endpoint during the bound; its RPT contains only the invocation. The harness stopped that PID (`0xFFFFFFFF`). This does not claim a fatal dependency rule. |
| incorrect script path | Repacked only copied Scripts PBO with `files[] = { "PBOExample/Scripts/scripts/3_Game_DOES_NOT_EXIST" };` | PID 27444 mounted copied packages, reached Steam initialization and the same three endpoints, then the independent probe failed with the same two unresolved fixture-class diagnostics. This does not isolate a distinct bad-path diagnostic because the unchanged fixture already fails the class-resolution probe. |

## Repair proposal for council

Do not accept the current fixture as runtime-verified. The minimal reproduction is the unchanged release plus the separate probe source and main RPT/script log cited above. Before changing the fixture, the council should independently inspect why the two `CfgMods.defs.files[]` entries do not result in the classes being available across the Game and Mission modules, then propose a fixture-only revision that aligns each script PBO prefix, member path, `CfgMods` module path, and package-loading role; rebuild with the existing script and rerun the exact independent probe. The proposed revision must be reviewed before any mutation because this run does not prove whether the issue is a virtual-path mapping, cross-package script-module behavior, or another loader constraint.

## Evidence limits and cleanup

This is not evidence of client join, signature enforcement, Workshop behavior, PBO size limits, serverMod-only signature enforcement, or public-server operation. All three owned PIDs (59096, 60012, 27444) were observed exited after their bounded harnesses; a final process/endpoint check found no `DayZDiag_x64`/`DayZServer_x64` process and no listener on ports 26072--26074.

The companion JSON includes paths, process records, hashes, tool hashes, and exact launch arguments.
