# Runtime probe record — 2026-09-13

> **Status:** Bounded harness preparation and launcher-observability attempt complete. No Enforce Script behavior is marked passed: the stable diagnostic client started but never emitted a fresh RPT or any `RTP:` marker before each owned process was stopped.

---

## Scope and safety record

- No `en/` content was edited and no commit was made.
- `runtime-inventory.json` was read before use and remains present; SHA-256 at closeout: `3B4DFE8A2AF2B872258516DB98F9AE6A2AC89BD281EE995327DE275E25B2483A`.
- No DayZ, DayZServer, Workbench, Addon Builder, or FileBank process was running before the first launch.
- No server was started and no port was opened. This intentionally leaves listen-server semantics untested rather than exposing an experimental server or mixing the older experimental build with the stable client.
- Every launched `DayZDiag_x64.exe` was started hidden, with a supplied disposable profile path; owned PIDs were `43384`, `40240`, `5612`, and `49220`. Final process check found no DayZ/DayZServer/FileBank process.

## Tool and source identity

| Item | Observed identity |
| --- | --- |
| Stable diagnostic executable | `D:\SteamLibrary\steamapps\common\DayZ\DayZDiag_x64.exe`; product `1.29.0.163709`; 20,245,560 bytes; SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A` |
| Experimental diagnostic executable | Inventory only: product `1.29.0.163401`; not launched |
| Experimental server executable | Inventory only: product `1.29.0.163401`; not launched |
| PBO packer | `D:\SteamLibrary\steamapps\common\DayZ Experimental Tools\Bin\PboUtils\FileBank.exe`; SHA-256 `F89AAEB22421B9158FBBF173F75D52B6F3DE69986CB462E58956C78DA82C4CAF` |
| Packer command form | `FileBank.exe -property prefix=<probe-prefix> -dst <isolated @mod/Addons> <isolated source>`; all four invocations exited `0` with no stderr |
| Extracted runtime flow read | `D:\DayZ Projects\scripts\3_game\dayzgame.c:2099-2129,2338-2354`; `scripts\3_game\autotest\autotestrunner.c:1-65`; `scripts\5_mission\mission\missiongameplay.c:223-238`; plus `scripts\5_mission\somemission.c:1-27` and `mission\missionmainmenu.c`/`missiongameplay.c` entry classes |

The extracted flow shows that `-autotest` sets `m_AutotestEnabled` only after JSON loads and requires `-mission`; the runner is ticked by `MissionGameplay`, not by `MissionMainMenu`. Therefore a self-terminating native autotest was not inferred from `AutotestRunner` merely being present.

## Harness

The disposable harness is in [`TEMP/wiki-runtime-probes`](../../../TEMP/wiki-runtime-probes/README.md). Its regular client hook is `modded class MissionMainMenu { override void OnInit() { ... } }`, selected to avoid connecting to or hosting a server.

| Probe | Source | Packed PBO (bytes; SHA-256) | Intended observation |
| --- | --- | --- | --- |
| baseline | [`runtime_baseline.c`](../../../TEMP/wiki-runtime-probes/source/baseline/Scripts/5_Mission/runtime_baseline.c) | `@baseline\Addons\baseline.pbo` (1,963; `FFFC1FD2601F888C006B497C9978297A41CBAB34DD2E6611453416A102A56ED2`) | `Normalize()` zero vector, no-arg `typename.Spawn()`, no-`override` derived dispatch, `autoptr` alias destructor, and same-callback static counter |
| constructor argument negative | [`runtime_spawn_argument_negative.c`](../../../TEMP/wiki-runtime-probes/source/spawn-argument-negative/Scripts/5_Mission/runtime_spawn_argument_negative.c) | `@spawn-argument-negative\Addons\spawn-argument-negative.pbo` (1,126; `3E09305AD0C6FACD6AA84D82BFD16C941AE4E5E347D6ECC72BB2D554C60FEF84`) | whether a `typename.Spawn()` call reaches a class with an argument-taking constructor |
| `Object.IsDeleted` negative | [`runtime_object_isdeleted_negative.c`](../../../TEMP/wiki-runtime-probes/source/object-isdeleted-negative/Scripts/5_Mission/runtime_object_isdeleted_negative.c) | `@object-isdeleted-negative\Addons\object-isdeleted-negative.pbo` (834; `F7455CD8C92A72C8457E2CE93B7EE6AFA8B7D4BA9CA4B9186B2540D531C6ADA7`) | compiler acceptance/rejection of the method on the actual executable build |
| global `Print` negative | [`runtime_global_print_negative.c`](../../../TEMP/wiki-runtime-probes/source/global-print-negative/Scripts/5_Mission/runtime_global_print_negative.c) | `@global-print-negative\Addons\global-print-negative.pbo` (652; `D683C827DBD6FBF2A080A9A165E63521E8183B31C4A5504337AA1E899D182768`) | parser/compiler acceptance of a top-level `Print` statement |

The last three are deliberately separate PBOs. They were packed but not launched after the baseline execution path failed to yield a log, so none has a compiler-result claim.

## Actual launcher observations

All commands used `Start-Process -WindowStyle Hidden -WorkingDirectory D:\SteamLibrary\steamapps\common\DayZ -PassThru` and never used `-server`, `-connect`, `-join`, a user mission, or a public endpoint.

| Run | Exact arguments | Observation |
| --- | --- | --- |
| launch check, PID 43384 | `-profiles="...\profiles\launch-check" -noSplash` | After eight seconds the exact shell markers were `RTP:PID=43384`, `RTP:RUNNING=43384`, and `RTP:STOPPED`. This establishes only that the executable can be started and stopped by this harness. |
| baseline, PID 40240 | `-mod="...\mods\@baseline" -profiles="...\profiles\baseline2" -doLogs -scriptDebug=true -noSplash -skipIntro -noPause` | After 20 seconds the process remained present with CPU `0.0625`; it was then stopped as an owned process. No profile directory/log appeared. |
| baseline closure attempt, PID 5612 | same baseline arguments, profile `...\profiles\baseline-clean` | The launcher reported `RTP:OWNED_PID=5612`; a later process check still saw it at CPU `0.09375`, then a cleanup check found it absent. No marker and no fresh RPT were observed. |
| `-autotest` control, PID 49220 | `-profiles="...\profiles\autotest-log-check" -doLogs -scriptDebug=true -autotest="...\profiles\autotest-log-check\missing.json" -noSplash -skipIntro -noPause` | The launcher reported `RTP:AUTOTEST_LOGCHECK_PID=49220`; the later owned-process check found it still running at CPU `0.109375`, so it was stopped. This did not self-terminate and emitted no RPT, consistent with an execution environment that never reached the extracted script path; it is not evidence about `AutotestRunner` support. |

Expected owned log locations were `TEMP/wiki-runtime-probes/profiles/<run>/`. At closeout, the only file below `profiles/` was the pre-created `.gitkeep`. The only matching RPTs in the installed game directory were pre-existing `DayZDiag_x64_2026-07-18_13-32-27.RPT` and `DayZDiag_x64_2026-07-18_13-42-02.RPT`; neither was modified during these runs. Windows Application events in the launch interval contained no DayZDiag application-error record.

## Evidence limits and conclusions

- **Zero-vector normalization, `typename.Spawn` constructor restriction, omitted-`override` dispatch, `autoptr` alias lifetime, and static lifetime:** no runtime marker was observed; all remain unverified on 1.29.0.163709. The baseline's static counter would only establish same-callback process state, not persistence through a mission reload.
- **`Object.IsDeleted` availability and global-scope `Print`:** the isolated negative sources are ready, but no actual compiler log was emitted. Do not claim either method absence or parser behavior from source search.
- **Listen-server and `SERVER` semantics:** untested. Stable inventory has no server executable, while the available server is the older experimental 1.29.0.163401 build; no mixed-version or exposed server was launched.
- **Official documentation:** on 2026-09-13, direct automated fetches of [DayZ:Modding Basics](https://community.bistudio.com/wiki/DayZ:Modding_Basics) and [DayZ:Workbench Script Debugging](https://community.bistudio.com/wiki/DayZ:Workbench_Script_Debugging) returned HTTP 403. Search-indexed content for the former corroborates the five DayZ script modules and development-only file patching, but it does not provide a runnable command line; no Reforger documentation was used as DayZ evidence.
- **User-provided local leads were read as fallible secondary material:** `API_ENFORCE_TIPOS_E_CONTAINERS.md` (SHA-256 `E3C6CC59D363990F6599A4B27B57E004B79EA4F83267D46D0BF24771396047B8`, relevant lines 380-417, 838-867, 1476, 1646-1647), `DAYZ_ENFORCE_SCRIPT_REFERENCE.md` (`2FD5EAC54A2EA849FCA334E613D55884A35D02D5843E60261F3DD88F15479FD5`, lines 980-985 and 1522-1530), and `STARDZ_AUTONOMOUS_TEST_LOOP.md` (`78EDCBB17948E12C2089B246D14091580975214ECA294CCF9D527C1561F38207`, lines 11-20, 33-75). Their claims were not promoted to runtime facts.

### Next useful step

Resolve why the stable diagnostic executable remains resident without creating its configured profile/RPT (for example, obtain a visible local diagnosis or a supported stable diagnostic server/client launch path), then run the four already packed PBOs one at a time and archive their fresh RPTs before making language documentation claims.
