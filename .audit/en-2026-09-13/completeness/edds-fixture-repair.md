# EDDS fixture repair receipt

**Prepared:** 2026-09-14 America/Sao_Paulo  
**Scope:** static repairs EF-03 through EF-07 only. This receipt supersedes the three incorrect extracted-source hashes in `edds-workflow-repaired.md`; it does not edit that historical report.

## Repair map

| Finding | Repair | Reopened evidence | Final artifact SHA-256 |
|---|---|---|---|
| EF-03 | Both probe `ImageWidget`s now explicitly use clamp and `stretch_w_h`; the readme states that the `128x64` alpha image crosses dark/light backgrounds and that the magenta marker is on the light half only. The original `64x32` PNG bytes/art are unchanged. | `D:/DayZ Projects/gui/layouts/day_z_hud_cars.layout:23-38`, SHA-256 `6E2893932679783D2618A9A63603966B83EEA225D1EF933301726C4B1068D7B2` | layout `0A4C807F438FD7C655D3E077D36B4287AD4FA0E54C99D7DF5DB1F4E3D759B4A7`; readme `C41D2A33F41CBB52F6659741EB2143CEF9D00A1970FDD9A1785E4A50817ED0EF`; PNG `EDB68FB0779781BF8F672D2595897EB870792675EB576BDDDF08E4E231B7522C` |
| EF-04 | The mission hook owns a persistent root, rejects duplicate initialization, unlinks/nulls a partial root after either cast fails, retains distinct create/load/SetImage booleans, and has a super-calling `OnMissionFinish()` that unlinks/nulls the root and emits `EDDSProbe/Teardown`. | Native `enwidgets.c:173,176-182,247-267`, SHA-256 `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E`; native `missiongameplay.c:96-125,257-267`, SHA-256 `E0A215D9E10300503CBC17F7A44BBABF58A2D1EF5CBB268D3DA1D279DC75C96A`; pinned CF `MissionGameplay.c:11-16`, commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, SHA-256 `F064E36874A81356661F19D05941C86BF985509A536107ED65CEE392D98F46EA` | mission `8F8E9B345618387BFFFD5AF08959624C73F73C9972940E17E59E66FDB444976F` |
| EF-05 | The Python verifier reads FourCC at `0x54`, selects legacy `0x80` or DX10 `0x94`, checks DDS/pixel-format header sizes, exact dimensions, mips `1..7`, every 8-byte `COPY`/`LZ4 ` entry, positive signed sizes, table bounds, and summed payload EOF. Its `--self-test` uses only in-memory synthetic valid/malformed bytes and says explicitly that no rendering claim follows. | Legacy `D:/DayZ Projects/DZ/water/ponds/data/pond_moss_ca.edds`, SHA-256 `2EAADDF7EBB52B90E47212A0200E050E55BA4AD7599F47974C31767853D0676E`; DX10 `D:/DayZ Projects/graphics/textures/water/dayzwater1_no.edds`, SHA-256 `4DA58F017C48244E676F42E3D3B13A01B5B45A68335EB60869507D376FB8F9B0` | verifier `7E2D1E06D30AF1B04D8C622C9E1B88B4F31E94F0FB875555E2EC7F58353C7581` |
| EF-06 | The future-only helper binds `SourceRoot` to the exact fixture, rejects equality/ancestor/descendant `SourceRoot`/`WorkRoot` overlap, requires ordinary existing roots before a fresh private run directory is created, invokes future BankRev `-properties` and `-logFull`, normalizes separators, and requires exactly the seven expected full member lines including `probe_ui.png`. Its future receipt retains argv, raw output/logs, tool path/version/hash, all source hashes, prefix line, and member lines. | Retained native-tool outputs at `TEMP/multi-pbo-confirmation/build/pboexample-20260914-002734-8140c691/logs/*-bankrev-{properties,members}.log` show `prefix = ...\`, `-properties`, and one full member line per entry; this fixture did not rerun those tools. | helper `FBE7B49D683A9F77789D073FC84D31825EE604CEE53AA57525565380752A0FA3`; AST checker `1331A4706F19014C96758A287BE4BE3DAF094F96ED99E37D454CE94A985C4F45` |
| EF-07 | Static verifier wording now limits text checks to text presence and does not present them as control-flow or compilation proof. This receipt supplies the current hashes and explicitly supersedes the three wrong historical values below. | Current extracted file hashes reopened from disk; exact values below. | receipt records the final hashes above; no generated EDDS, metadata, or GUID exists. |

## Superseded extracted-source hashes

`edds-workflow-repaired.md` reported the following values. They are superseded here by fresh SHA-256 calculations on 2026-09-14:

| Path | Historical incorrect value | Superseding current value |
|---|---|---|
| `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c` | `6BB20A54119A25BAB3933607BF8B703C3123853B36BF2E4141AEAC83CF215C9E` | `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E` |
| `D:/DayZ Projects/scripts/5_mission/mission/missiongameplay.c` | `E0A2157DBBF1C795F8228745BEF493218434A1B5125912F6EDFE032BFE457DB2` | `E0A215D9E10300503CBC17F7A44BBABF58A2D1EF5CBB268D3DA1D279DC75C96A` |
| `D:/DayZ Projects/gui/layouts/day_z_hud_cars.layout` | `6E2893932679783DBA2C2404B18D8CFC841DFD0EEA7C521A05400D3BBF8637C2` | `6E2893932679783D2618A9A63603966B83EEA225D1EF933301726C4B1068D7B2` |

## Static verification actually run

1. `python -B examples/en/edds-probe/scripts/verify_preparation.py` passed: source PNG/hash, pre-conversion absence, and static text checks passed.
2. `python -B examples/en/edds-probe/scripts/verify_preparation.py --self-test` passed: two in-memory synthetic structural cases (legacy and DX10) passed and nine malformed cases (header size, pixel-format size, dimensions, mip count, marker, non-positive size, table truncation, payload truncation, non-EOF payload) were rejected.
3. `powershell -NoProfile -ExecutionPolicy Bypass -File examples/en/edds-probe/scripts/verify_build_ast.ps1` passed: PowerShell parsed `build.ps1` with 84 command expressions and its static helper/argv/manifest checks passed. Three safe negative helper invocations also passed: a non-exact `SourceRoot`, `SourceRoot`/`WorkRoot` equality, and `WorkRoot` as a source ancestor all failed before tool lookup.
4. `git diff --check` passed for this repair; its output contained only unrelated existing CRLF warnings from `examples/en/entity-persistence`.

These tests do not run Addon Builder, BankRev, Workbench, a compiler, a VitePress build/dev server, a game, a client, or a server. They do not prove Enforce control flow/compilation, native EDDS acceptance, import visibility, exact PBO output, or rendering.

## Boundaries retained

The preserved rejected fixture is at `TEMP/edds-fixture-rejected-20260914-0703/preservation.json`; the source PNG remains byte-identical. The proposed private project and absent `P:` mapping remain unobserved runtime concerns, so this repair does not replace or modify either project. A fresh independent exact-file review must accept these bytes before the authorized single visibility/import/pack/client experiment.
