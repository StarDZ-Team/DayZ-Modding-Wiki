# Independent council: server Mission startup and lifecycle

Reviewed 2026-09-14 UTC against repository HEAD `0df58c20761f654cd91ece04d9469be4b1728c6b`. This council made no EN edit, commit, game-install change, firewall/account change, or public-server connection. Its only writes are this report, its JSON companion, and `TEMP/server-mission-council/`. It ran no child worker and performed no new lifecycle/restart launch.

## Verdict

**Accept the investigation's scoped startup result and bounded static-lifetime observation. Reject every broader restart-safety, interface-isolation, or production-readiness extrapolation.** The fresh independent pair reproduced the exact startup transition on DayZDiag `1.29.0.163709`: omission of `instanceId` terminated before the Mission module; adding only `instanceId = 1;` reached the modded `MissionServer.OnInit()` and retained a PID-owned game socket through the test bound. The retained lifecycle run does show Mission-module static reinitialization and World-module static persistence across one direct `GetGame().RestartMission()` in the same PID, but its subsequent `0xC0000005` exit makes it unsuitable as a healthy restart recipe.

This is diagnostic evidence for one executable build, one CE mission, and one probe mod. It is not certification of `DayZServer_x64.exe`, public hosting, client connectivity, authenticated administration, persistence correctness, or production restart behavior.

## Independent startup rerun

The council used fresh UDP ports `25972` (game), `25973` (Steam query), and `25974` (additional game-owned endpoint) and distinct `profiles/<case>` and `storage/<case>` directories under `TEMP/server-mission-council/`. Preflight checks at `2026-09-14T01:10:54.7854180Z` and `2026-09-14T01:12:07.4296395Z` found no DayZDiag/DayZServer process and no endpoint on those ports. `launch-case.ps1` used `ProcessStartInfo.ArgumentList`, `UseShellExecute=false`, `WindowStyle=Hidden`, and `CreateNoWindow=true`; cleanup addressed only the retained `Process` object.

The two configs are semantically identical except for this one line in `instance-id-1.cfg`:

```cpp
instanceId = 1;
```

| Case | PID | Bound | Result |
|---|---:|---:|---|
| `missing-instance` | 48988 | 35 s | Loaded GameLib, Game, and World only. Briefly owned UDP `127.0.0.1:25972` and `:25974`, began a ten-second termination countdown, and exited itself with signed status `-1` (`0xFFFFFFFF`). No Mission module, mission `init.c`, server console, or `RTP:SERVER` marker appeared. |
| `instance-id-1` | 61376 | 55 s | `SteamGameServer_Init` succeeded, Mission and mission `init.c` loaded, and all five `RTP:SERVER` markers ran from the modded `MissionServer.OnInit()`. PID 61376 owned UDP `127.0.0.1:25972`, `127.0.0.1:25974`, and query UDP `0.0.0.0:25973` from the first endpoint sample at `01:12:22.9790110Z` through the last at `01:13:04.1772301Z`. The harness then killed only PID 61376. |

Exact successful markers are in `profiles/instance-id-1/script_2026-09-13_22-12-10.log`: Mission module line 9, mission `init.c` line 10, and `RTP:SERVER:BEGIN`, `IS_SERVER=true`, `IS_MULTIPLAYER=true`, `DEFINE=1`, `END` at lines 20–24. The paired RPT records `SteamGameServer_Init(7f000001,8766,25972,25973,3,1.29.163709)` at line 439 and the same markers at lines 1418–1422. The server console records the Steam initialization at line 1 and the council-owned `storage_1` selection at line 6.

The missing-instance RPT lines 440–449 record the countdown and line 453 records successful termination. Its script log ends after World at line 8 and `~DayZGame()` at line 9. As in the retained control, this failed log does **not** print an explicit missing-`instanceId` error. The exact executable nevertheless contains `[ERROR][Server config] :: instanceId parameter is mandatory and must be valid 32-bit integer.` beginning at ASCII file offset `0xED3050`; the fresh controlled delta and that build-specific binary string together support the scoped diagnosis.

The game socket was loopback-bound, but the same successful PID bound its query socket to wildcard `0.0.0.0:25973`. Therefore do not say the process was loopback-only. A wildcard local bind also does not by itself prove public reachability, firewall traversal, or external traffic.

## Retained lifecycle evidence reopened

The lifecycle PBO has SHA-256 `4D2A20A0A4683ABABFF225CE9061D76E1C4542148A735D7406DC149DAA3F8D3B`. Its reviewed source registers World and Mission modules; `SMI_WorldState.s_Count` initializes to `200` in `4_World`, while `SMI_MissionState.s_Count` initializes to `100` in `5_Mission`. The FileBank receipt records exit `0`, and the runtime log's `WikiServerLifecycle` define, marker strings, and World/Mission module records show that the probe scripts loaded. The private CE mission was independently compared with the official checkout: both trees had 43 files and no relative-path or SHA-256 difference.

The retained script log shows this single sequence in PID 33556:

| Lines | Observation |
|---|---|
| 20–23 | First `MissionServer.OnInit`/`OnMissionStart`; Mission `101`, World `201`, server and multiplayer true. |
| 24–26 | Direct `GetGame().RestartMission()` call, `OnMissionFinish` with `101/201`, then `MissionServer` destructor. |
| 27–28 | Mission module and mission `init.c` load again; no second World-module load is recorded. |
| 38–41 | Second `MissionServer.OnInit`/`OnMissionStart`; Mission `101`, World `202`, server and multiplayer true. |

This supports the narrow inference that the reviewed Mission-module initializer ran again while the reviewed World-module static remained live across that direct restart in this same process. It does not establish a language-wide guarantee for all statics, other modules, other builds, reconnects, process restarts, or administrator commands.

The process record reports signed exit `-1073741819`, exactly `0xC0000005`, without a harness kill. Neither `SMI:RESTART_MISSION:RETURN` nor the planned `SMI:SECOND_LIFECYCLE:REQUEST_EXIT` appears. The RPT truncates during second-cycle CE restoration at line 5140 (`Accessing static object outs`). Similar landscape warnings occur before the restart, so the warning text is not proof of the access violation's cause. The synchronous mission-owned callback, CE restoration, or an unrelated native defect remain hypotheses only.

Extracted `game.c:1106` declares native `RestartMission()`. `ingamemenuxbox.c:475` calls it from a client-menu flow, which is not evidence for a dedicated-server admin command. `dayzgame.c:1411-1416` defines a separate `ReloadMission()` wrapper around protected `CreateMission(m_MissionPath)` under `ENABLE_LOGGING`; it was inspected but not invoked. No source or runtime evidence reviewed here equates direct `RestartMission()` with authenticated admin `#restart`.

## Council dispositions

### Accepted

1. Within this DayZDiag `1.29.0.163709` recipe, the missing `instanceId` is the controlled difference that separates termination before Mission from a stable bounded startup reaching `MissionServer.OnInit()`.
2. `instanceId = 1` is sufficient for that transition without adding `guaranteedUpdates`; this does not establish that `guaranteedUpdates` is universally optional.
3. The successful PID owned the loopback game endpoint while the query socket bound wildcard. The entire process was not loopback-only.
4. The retained PBO produced two Mission lifecycles in one PID: the tested Mission static reinitialized and the tested World static persisted.
5. The lifecycle process then exited with observed status `0xC0000005`; no clean post-restart operation was demonstrated.
6. The official CE checkout is pinned to `9a21bb9f5fb9c62a7ce2761402196091588133e6`, the DayZ Samples checkout to `da5e5437c9502620d9853fb6eed14701135ab2ea`, and both worktrees were clean when reopened.

### Rejected

1. Any statement that the whole successful process was loopback-only.
2. Any presentation of the lifecycle probe or direct `RestartMission()` call as a safe reusable restart implementation.
3. Any equivalence between direct `GetGame().RestartMission()` and authenticated administrator `#restart`.
4. Any claim that the truncated landscape warning, CE restoration, or the callback is the established cause of `0xC0000005`.
5. Any production certification, public reachability claim, or universal cross-version rule derived from these DayZDiag probes.

### Unresolved

1. Why the failed control suppresses the executable's explicit missing-`instanceId` diagnostic instead of logging it.
2. The native cause of the lifecycle access violation.
3. Whether a controlled restart can reach stable post-restart operation and clean exit.
4. Authenticated `#restart` lifecycle behavior and its relation, if any, to direct `RestartMission()`.
5. Static lifetime behavior for other modules, types, callbacks, executables, and DayZ builds.
6. Fresh full-body access to the official Bohemia Server Configuration page: a direct request at `2026-09-14T01:16:33.3395240Z` returned HTTP 403. The reviewed local snapshot documents `instanceId`, `logFile`, and `steamQueryPort`, but its content was treated as a local reference rather than proof of current web text.

## Exact proposed EN wording

No EN file was changed. If the coordinator accepts these findings, use the following exact scoped wording.

For `en/09-server-admin/03-server-cfg.md`, replace the `instanceId` table row with:

> | `instanceId` | int | required in the tested build; no default established | Identifies the server instance and selects persistence under `storage_<instanceId>/`. In a controlled DayZDiag `1.29.0.163709` startup, omitting this key terminated before the Mission module loaded; adding only `instanceId = 1;` let `MissionServer.OnInit()` run and selected `storage_1`. Set an explicit, unique 32-bit integer for each instance. This scoped diagnostic result is not production-server certification. |

For `en/09-server-admin/01-server-setup.md`, add after the sample `serverDZ.cfg` block:

> Keep `instanceId` explicit. In a controlled DayZDiag `1.29.0.163709` test, a config without it terminated before the Mission module loaded, while the otherwise identical config with `instanceId = 1;` reached `MissionServer.OnInit()`. This verifies the diagnostic startup path only; it does not certify `DayZServer_x64.exe`, client connectivity, or public production hosting.

For the local-server verification discussion in `en/09-server-admin/01-server-setup.md`, add:

> A loopback game bind does not prove that every socket in the process is loopback-only. In the same diagnostic run, the game endpoint was `127.0.0.1:<game-port>` but the configured Steam query endpoint was `0.0.0.0:<steamQueryPort>`. Check each PID-owned endpoint and your firewall separately; a wildcard bind alone does not prove public reachability.

For `en/01-enforce-script/08-memory-management.md`, replace the first paragraph under **Static State and Mission Lifecycle** with:

> A controlled DayZDiag `1.29.0.163709` dedicated-server probe called `GetGame().RestartMission()` once from a `MissionServer` callback. In the same PID, the Mission script module and mission `init.c` loaded again: a Mission-module `static int` initializer ran again (`100` to `101` in each `OnInit()`), while a World-module `static int` was not reinitialized and advanced from `201` to `202`. The process then exited with `0xC0000005` before its clean-exit marker, so treat this as a bounded module-lifetime observation—not a safe restart recipe or evidence about authenticated `#restart`, reconnects, or process restarts.

Replace the two comments in that section's `MyLockCounter` example with:

```c
// Ordinary calls in one loaded module share the same static value.
// Mission-module reload and World-module persistence were observed only in the bounded probe above.
```

Keep the existing defensive `Cleanup()` recommendation. Do not claim that cleanup made the reviewed restart safe; the probe crashed before planned clean exit.

## Sources and evidence limits

- Executable: `D:/SteamLibrary/steamapps/common/DayZ/DayZDiag_x64.exe`, 20,245,560 bytes, product `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`.
- Packer: `D:/SteamLibrary/steamapps/common/DayZ Experimental Tools/Bin/PboUtils/FileBank.exe`, 194,480 bytes, SHA-256 `F89AAEB22421B9158FBBF173F75D52B6F3DE69986CB462E58956C78DA82C4CAF`; version fields are blank.
- Official CE: `https://github.com/BohemiaInteractive/DayZ-Central-Economy.git` at `9a21bb9f5fb9c62a7ce2761402196091588133e6`; `init.c` lines 1–6 initialize CE and lines 95–98 construct `CustomMission` derived from `MissionServer`.
- Official DayZ Samples: `https://github.com/BohemiaInteractive/DayZ-Samples.git` at `da5e5437c9502620d9853fb6eed14701135ab2ea`; `Test_Inputs/config.cpp` demonstrates `DZ_Data` dependency and CfgMods script-module registration. It does not diagnose `instanceId` or restart semantics.
- Extracted local scripts were used for declarations and call sites only. Their extraction version is not independently pinned; runtime conclusions are tied to the hashed executable and logs.
- The exhaustive reviewed-file hash list, exact process samples, and machine-readable dispositions are in the JSON companion.

## Cleanup

PID 48988 exited by itself. The bounded harness killed only its owned PID 61376 after the final sample. At `2026-09-14T01:18:24.1694938Z`, neither owned PID existed, no DayZDiag/DayZServer process existed, and no endpoint remained on `25972–25974`; see `TEMP/server-mission-council/cleanup.json` (SHA-256 `A1FAE3000C8CFB2A19AC5F1D39576F03ABB4F8A40991DE94D9CCC9BFA95A5477`). No original investigation artifact was modified.
