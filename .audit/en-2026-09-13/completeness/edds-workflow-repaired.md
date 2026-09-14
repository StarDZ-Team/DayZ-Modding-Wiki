# EDDS workflow repair disposition

**Prepared:** 2026-09-14 America/Sao_Paulo  
**Scope:** concrete source/project preparation only. The prior research and council reports remain unchanged historical records.

## Council repairs

| Repair | Disposition | Prepared result and boundary |
|---|---|---|
| 1. Project/source mount | repaired, observation pending | `TEMP/edds-fixture-preparation/EDDSProbe.gproj` uses the installed `GameProjectClass`/`FileSystemPathClass` shape and an explicit physical source root. `P:` was absent; no mapping or installed project was changed, so virtual `EDDSProbe` visibility remains untested. |
| 2. DDS language and offsets | repaired | `verify_preparation.py --edds` describes structural non-equivalence only, not native rejection, and selects `0x80` after a legacy header or `0x94` after a DX10 header. |
| 3. Original source/import control | repaired | A deterministic 64x32 RGBA PNG generator and byte-level verifier implement the exact asymmetric L, alpha-cyan, and magenta control. The future instructions permit one default import and record generated values as observations. |
| 4. Resource identity | repaired | The descriptor has a declared `EDDSProbe/GUI/imagesets/probe_ui.edds` plain-path fallback; a later exact copied Workbench identity may replace only that path. No GUID is generated, inferred, copied, or claimed necessary. |
| 5. Standalone PBO definition | repaired | `config.cpp` defines one `EDDSProbe` client mod with `CfgPatches`, justified `DZ_Scripts`, `Game`/`World`/`Mission` dependencies, `imageSets`, and `missionScriptModule`. |
| 6. Client probe script | repaired | The modded `MissionGameplay.OnInit()` calls `super.OnInit()`, creates and guards the layout/widgets, logs unique create/load markers and both load booleans, then calls `SetImage(0)` only after success. No Enforce compilation was performed. |
| 7. Alpha/render control | repaired | The layout uses white tint, blend, and source alpha; its alpha sprite spans dark and light backgrounds while retaining an opaque magenta control. Future screenshots may show behavior but cannot establish exact alpha 128 alone. |

## Evidence reopened for this implementation

- Installed Workbench project: `D:/SteamLibrary/steamapps/common/DayZ Experimental Tools/Bin/Workbench/dayz.gproj`, SHA-256 `269DAAD629D0007176B4B81ADFB52740A23A11955C24C414B82727F15EE41928`; it has `FileSystemPathClass` entries for `./` and `P:/` and existing StarDZ image-set entries. `P:` was absent at preparation.
- Workbench executable: `D:/SteamLibrary/steamapps/common/DayZ Experimental Tools/Bin/Workbench/workbenchApp.exe`, SHA-256 `B61D240394845EF9EAB3B5F459D487B50DBF3C42713FB9E9E50CE945F5A894C6`; prior council-recorded version is `1.29.163.401`.
- Extracted APIs: `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c` SHA-256 `6BB20A54119A25BAB3933607BF8B703C3123853B36BF2E4141AEAC83CF215C9E` (widget alpha/blend flags, `CreateWidgets`, `LoadImageFile`, `SetImage`) and `scripts/5_mission/mission/missiongameplay.c` SHA-256 `E0A2157DBBF1C795F8228745BEF493218434A1B5125912F6EDFE032BFE457DB2` (`MissionGameplay.OnInit`).
- Extracted descriptor/layout examples: `gui/imagesets/dayz_gui.imageset` SHA-256 `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A` and `gui/layouts/day_z_hud_cars.layout` SHA-256 `6E2893932679783DBA2C2404B18D8CFC841DFD0EEA7C521A05400D3BBF8637C2`.
- Pinned public implementation reopened locally: DayZ Dabs Framework commit `fd859fd891f45a4a9c9089597db0c621ef3a9de5`, `DabsFramework/GUI/icons/brands.imageset` SHA-256 `1DE25A2BA41771632814F126C2C326B5D8A2F1DF74BEA2344CF56120081D101D` and `DabsFramework/Scripts/config.cpp` SHA-256 `74E0CC3791ADD0F6F7E650162B3BD96D2F8188A9F130209965AAE00E26D372D1`. Its plain path is precedent only, not proof of runtime viability.

## Static checks actually run

`python examples/en/edds-probe/scripts/generate_probe_png.py` wrote the source PNG. `python examples/en/edds-probe/scripts/verify_preparation.py` passed its PNG byte/pixel checks and its config/imageset/layout/script structure checks, confirming that generated EDDS and metadata remain absent. No Workbench, packer, build, Enforce compiler, game, server, or client was launched.

The remaining prerequisites are a later observed private-project visibility check, one default Workbench import, retention of its generated output/identity, PBO table verification, and the bounded client baseline run.
