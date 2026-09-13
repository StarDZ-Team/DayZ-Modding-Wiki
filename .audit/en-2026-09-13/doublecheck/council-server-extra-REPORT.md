# Council Review: Server Extra Findings

## Scope

Independent adjudication of only `SR2-004`, `SR2-005`, and `SR2-006` from the finalized server-reference audit. The quoted English text was reopened at baseline `bf7ae1947876071ed4e25578dc595d896f2e6263`; `en/09-server-admin/01-server-setup.md` has SHA-256 `4DAF36B80ECD152B61222AB9D4DB96EDB487F3C6BE9F9784742191EE895BDED7` and `en/troubleshooting.md` has SHA-256 `F63C0C82F7BE34A8DDA4677496FAB971F908F13D1DF2330CC05A9FB9730FA73B`.

Official Bohemia Community pages were independently reopened through indexed current page bodies on 2026-09-13. Direct requests remain HTTP 403, so no new whole-page byte hash is claimed. Relevant primary pages:

- `https://community.bohemia.net/wiki/DayZ%3AServer_Configuration`
- `https://community.bohemia.net/wiki/DayZ%3AModding_Basics`
- `https://community.bohemia.net/wiki/DayZ%3AWorkbench_Script_Debugging`

## Dispositions

### SR2-004 — reject

Old text:

> DayZ Server is single-threaded for gameplay logic. Clock speed matters more than core count.

Final new text: none.

The cited primary source documents worker threads for the server's **replication system** and separately documents `-cpuCount` for parallel task processing. Neither statement establishes that gameplay/script simulation itself runs across multiple threads, so it does not contradict the page's deliberately qualified “for gameplay logic” claim. It also does not establish a general clock-speed-versus-core-count comparison. The proposed replacement changes a qualified gameplay-thread claim into a whole-process observation; that observation is true as far as replication goes, but it is not an evidenced correction of the quoted sentence.

### SR2-005 — accept exact repair

Old text:

> This is normal. DayZ Server is single-threaded. Do not run multiple server instances on the same core -- use processor affinity or separate machines.

New text:

> High utilization on one core can reflect a main-thread bottleneck, but the server also uses parallel tasks and can use multithreaded replication. Check server FPS and profile the workload before assigning affinity; size replication workers through `dayzsettings.xml` when `multithreadedReplication` is enabled.

Unlike SR2-004, this sentence generalizes about the entire server executable. Bohemia's current Server Configuration page explicitly says `multithreadedReplication` enables multithreaded processing of server replication, derives its workers from `<jobsystem>` `maxcores` and `reservedcores`, and documents `-cpuCount` as selecting logical cores for parallel task processing. That directly refutes the whole-server statement and makes the unconditional affinity prescription too strong. The replacement preserves the possibility of a main-thread bottleneck without conflating replication workers with gameplay logic.

### SR2-006 — accept exact repair

Old text:

> | `-filePatching` | Load unpacked files (requires DayZDiag) |

New text:

> | `-filePatching` | Context-dependent: use it with `DayZDiag_x64.exe` for unpacked-file development; Bohemia's dedicated-server reference currently describes the server flag as allowing only PBO data. Verify the executable-specific behavior on your target build. |

Bohemia's Modding Basics page launches `DayZDiag_x64.exe` with `-filePatching` for a project-drive mod and explains direct development/hotloading; Workbench Script Debugging likewise identifies DayZDiag as the executable used for direct script modification. In contrast, the current dedicated-server launch-parameter table says `-filePatching` ensures only PBOs are loaded and no unpacked data. The apparently opposite official descriptions are executable/context specific. The proposed replacement reports both documented meanings and explicitly avoids claiming untested runtime behavior.

## Result

- Accept exact repair: `SR2-005`, `SR2-006`
- Reject: `SR2-004`
- English edits: none
- Runtime tests/build: none

This review does not establish that gameplay logic is multithreaded, quantify core-scaling, or guarantee `filePatching` behavior for any particular build beyond the cited executable-specific documentation.
