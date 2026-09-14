# Stable diagnostic server Mission investigation

Recorded locally on 2026-09-13 (UTC artifacts cross into 2026-09-14), against repository HEAD `0df58c20761f654cd91ece04d9469be4b1728c6b`. This worker changed only this report, its JSON companion, and `TEMP/server-mission-investigation/`; concurrent EN edits belong to other workers. No commit, game-install mutation, firewall change, account change, public-server connection, or child worker was made.

## Result

**The retained recipe was missing `instanceId`. Adding only `instanceId = 1;` to the controlled configuration allowed stable DayZDiag `1.29.0.163709` to execute `MissionServer.OnInit`, with `IsServer=true`, `IsMultiplayer=true`, and an owned UDP endpoint at `127.0.0.1:24962`.** Neither `guaranteedUpdates` nor a new mission/dependency was needed for this observed transition. This is a minimal diagnostic repair, not a production server configuration recommendation.

The single subsequent lifecycle test reached mission finish, destruction, Mission-module reload, and a second `MissionServer.OnInit` in the same PID. A Mission-module static initializer reset its counter to `100` before incrementing to `101`; the World-module counter persisted and advanced from `201` to `202`. That test later exited with access-violation status `0xC0000005`, before its planned clean-exit marker. Healthy restart operation and equivalence to administrator `#restart` remain unverified.

## Controlled startup evidence

All paths below are relative to [`TEMP/server-mission-investigation`](../../../TEMP/server-mission-investigation/). Full commands, UTC samples, exact PIDs, endpoint ownership, exit observations, sources, and hashes are retained there and indexed in the JSON companion.

| Case | PID | Changed hypothesis | Observed result |
|---|---:|---|---|
| `console-control` | 50100 | Add `logFile` to the old config to expose validation failures; move test ports to 24962/24963 and cap FPS | Launcher accidentally used a mixed-slash config path. RPT explicitly reported that it could not find that config, then exited `-1`. Not used as the missing-instance control. |
| `console-native` | 13756 | Correct the config and mod arguments to native backslashes; retain old configuration settings plus console logging | Loaded World, temporarily bound loopback UDP 24962 and 24964, then counted down and exited `-1`. No Mission module or server console log was created. |
| `instance-id` | 47740 | Add only `instanceId = 1;` to `console-native.cfg`; isolate profile/storage under new paths | Loaded Mission and the unchanged official CE `init.c`, ran all five retained `RTP:SERVER:*` markers, and retained the loopback game endpoint through the final sample. Still alive at the 50-second bound, then killed only via its owned Process object. |
| `lifecycle` | 33556 | Use a private copy of the same CE mission and a purpose-built lifecycle marker PBO | Two OnInit/OnMissionStart sequences in one process, separated by RestartMission, OnMissionFinish, destructor, and Mission-module reload; subsequently exited `-1073741819` without a harness kill. |

`instance-id` script log `profiles/instance-id/script_2026-09-13_21-56-54.log` lines 9–10 identifies the Mission and mission-init modules; lines 20–24 contain the server markers. Its console line 1 reports `SteamGameServer_Init(7f000001,8766,24962,24963,3,1.29.163709)` and lines 5–6 identify CE initialization and private `storage_1`. The paired process JSON records the UDP game endpoint owned by PID 47740 from `00:57:08.1865086Z` through `00:57:44.2089071Z`.

The runtime config comparison is decisive for this recipe: `instance-id.cfg` differs from `console-native.cfg` only by whitespace and `instanceId = 1;`. Both already reference the same original mission and server-context PBO, use backslash argument values, and omit `guaranteedUpdates`. The stable executable also contains the ASCII diagnostic `instanceId parameter is mandatory and must be valid 32-bit integer` at file offset `0xED3050`, retained in `native-config-strings.json`. This string is corroborating binary evidence, not a claim that the failed control printed it. The failed control's RPT contains no explicit missing-instance diagnostic.

The prior retained attempts already supplied native backslash paths. The mixed-slash failure was introduced and corrected within this investigation; it does not explain those historical attempts. `launch-forward-slash-retained.ps1` preserves that mistake, while `launch-control-retained.ps1` preserves the corrected startup harness. Each option is one `ProcessStartInfo.ArgumentList` element, with no literal embedded quotes. Launch uses hidden window style, `UseShellExecute=false`, and `CreateNoWindow=true`.

## Single lifecycle test

Source: `source/lifecycle/config.cpp`, `Scripts/4_World/world_state.c`, and `Scripts/5_Mission/lifecycle.c`. FileBank packed them into `mods/@lifecycle/Addons/lifecycle.pbo`, exiting `0`; DayZ's module records establish actual compilation. The probe depends on `DZ_Data` and registers World and Mission modules. The private mission is a byte-identical copy of official CE `dayzOffline.chernarusplus`; the marker code changes only the added mod.

`profiles/lifecycle/script_2026-09-13_22-00-34.log` records:

| Lines | Observation |
|---|---|
| 20–23 | First OnInit; `MISSION_STATIC=101 WORLD_STATIC=201`; server and multiplayer true; OnMissionStart |
| 24–26 | `RestartMission()` call, OnMissionFinish with 101/201, MissionServer destructor |
| 27–28 | Mission and init.c modules loaded again |
| 38–41 | Second OnInit; `MISSION_STATIC=101 WORLD_STATIC=202`; server and multiplayer true; OnMissionStart |

The native `RestartMission()` declaration was opened in extracted `scripts/3_game/global/game.c:1106`; its call in `5_mission/gui/ingamemenuxbox.c:475` is a client-menu example, not proof of dedicated-server semantics. The direct server probe supplies the bounded observation above. `DayZGame.ReloadMission()` was also inspected but not invoked. No authenticated admin command, reconnect, new process restart, Game-module field, or other static type was tested.

The callback creates `$profile:smi-restart-requested.txt` before invoking RestartMission so a reloaded static cannot create an endless test loop. A second scheduled callback was intended to print `SMI:SECOND_LIFECYCLE:REQUEST_EXIT` and call `RequestExit(0)`. Neither that marker nor `SMI:RESTART_MISSION:RETURN` was observed. The RPT ends during CE restoration with a truncated `Accessing static object outs` line; similar landscape-object warnings also occur earlier. Exit code `0xC0000005` is observed; the native crash cause is not established by those warnings. No crash log or dump was created in this owned profile. In particular, a synchronous restart initiated from a mission-owned callback and its interaction with CE are still candidate causes, not proven engine defects.

**Exact remaining prerequisite:** obtain a controlled server lifecycle that returns to stable operation and exits cleanly, isolating the callback/CE restoration failure before extrapolating to production restart behavior; then test authenticated `#restart` separately if that claim remains necessary. Do not present the present PBO as a safe reusable restart implementation. The requested one lifecycle test was performed; no broader matrix or further game launches followed.

## Source provenance and limitations

- Runtime EXE: `D:/SteamLibrary/steamapps/common/DayZ/DayZDiag_x64.exe`, product version `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`. RPTs identify `1.29.163709` and executable timestamp `2026/08/13 04:52:12` local.
- Packer: `D:/SteamLibrary/steamapps/common/DayZ Experimental Tools/Bin/PboUtils/FileBank.exe`; the exact command, executable hash, PBO hash and source hashes are in the retained manifest. Packing is separate from runtime validation.
- [Official Central Economy](https://github.com/BohemiaInteractive/DayZ-Central-Economy/tree/9a21bb9f5fb9c62a7ce2761402196091588133e6), pinned `9a21bb9f5fb9c62a7ce2761402196091588133e6`: opened README, `dayzOffline.chernarusplus/init.c` (main, CE initialization, CustomMission, CreateCustomMission), and repository identity. The existing checkout was preserved; the lifecycle test used a private directory copy. Runtime CE output includes prototype parsing, ignored-type, and missing-event warnings, so this is not certification of the full CE dataset.
- [Official DayZ Samples](https://github.com/BohemiaInteractive/DayZ-Samples/tree/da5e5437c9502620d9853fb6eed14701135ab2ea), freshly cloned at `da5e5437c9502620d9853fb6eed14701135ab2ea`: opened README and `Test_Inputs/config.cpp` lines 1–33 for `DZ_Data` dependency and CfgMods module registration. This sample supplies registration context, not the instanceId diagnosis. The GitHub API request through the web tool failed; the Git clone succeeded and supplied the actual files.
- Opened and retained local official-page snapshots in `D:/StarDZ/docs/DayZ`: `Server Configuration.md` lines 1–69, 78–92 and 166–187; `Modding Basics.md` diagnostic-launch/mission examples around 118–185; `Workbench Script Debugging.md` server-mode text around 49–52. These are fallible local snapshots, with exact hashes in `source-snapshots.json`.
- [Official server configuration](https://community.bistudio.com/wiki/DayZ%3AServer_Configuration), web search accessed 2026-09-13: indexed official-page text includes `instanceId`, protocol setting and console-log option. It was search-index retrieval, not a fresh full-body HTTP fetch. No cross-game restart material or third-party forum claim is used as proof.
- Actually opened extracted `MissionServer.OnInit`, `MissionBase` construction, `RestartMission`/`ReloadMission`, `PluginItemDiagnostic.OnInit`, and `GetPlugin`; retained exact copies/hashes under `reference/local-snapshots/`. The extraction's version is not independently pinned here; build-specific conclusions come from the identified executable and fresh logs.

The diagnostic `PluginConfigDebugProfile is not Registred` stack appears before each successful OnInit. Extracted `PluginItemDiagnostic.OnInit` checks the returned pointer before using it, and `GetPlugin` emits a DIAG_DEVELOPER stack for a missing plugin. Its presence did not prevent the recorded startup markers; this does not establish that all diagnostic behavior is healthy.

Although the game endpoints were loopback-only, successful runs also bound Steam query UDP `0.0.0.0:24963`. Therefore the entire process was **not** limited to loopback interfaces. This investigation did not connect to a public server or alter firewall/account settings; Steam server initialization was logged, and no claim of zero external Steam traffic is made. The owned processes and test endpoints are now absent.

## Preservation and closeout

The original reports, PBOs, and CE checkout were not edited. Source snapshots, original and corrected launchers, all four configs, argument arrays, PID samples, RPT/script/console logs, sentinel, CE storage, and reference checkouts remain under the owned TEMP directory. `evidence-manifest.json` hashes all retained probe files outside reference Git metadata; the JSON companion records important source identities and exact marker lines. Probe files are investigative artifacts, not EN examples.

All four owned DayZ PIDs have exited: 50100 and 13756 self-terminated, 47740 was explicitly stopped after its bounded observation, and 33556 exited with access violation. Final OS checks found no DayZDiag/DayZServer process or endpoint on ports 24962–24964. No VitePress build was run because no wiki content or shared config was edited by this worker. Independent council review is still required before integrating these findings into EN guidance.
