# Entity persistence fixture implementation

**Date:** 2026-09-14  
**Scope:** isolated `examples/en/entity-persistence/` fixture and `TEMP/entity-persistence-fixture/` package receipts only. No English wiki prose, server profile, production mod configuration, keys, commit, game process, client, or server was changed or launched.

## Delivered fixture

`EntityPersistenceFixtureBattery` is a configured leaf of the actual vanilla `Battery9V` class. Its three variants deliberately share `CfgPatches` identity `EntityPersistenceFixture`, `CfgVehicles` class name `EntityPersistenceFixtureBattery`, PBO name `EntityPersistenceFixture.pbo`, and raw-backslash archive prefix `EntityPersistenceFixture`; only one variant belongs in a test install at a time.

- **v1:** writes schema `1`, `charges = 17`, and `label = "v1-control"` after its parent data.
- **v2:** writes schema `2` plus `locked`; it reads a v1 record into the same two fields and sets `locked = false` explicitly, and exposes `SetFixtureLocked(bool)` for a later reviewed harness.
- **declared-v2-missing-field:** writes a declared v2 record but intentionally omits `locked`, logs the three preceding write results, and then requires the missing field on load. It tests an incomplete custom layout, not asserted byte-level truncation.

Every override calls `super.OnStoreSave(ctx)` before custom writes and calls/propagates `super.OnStoreLoad(ctx, engineVersion)` before custom reads. Each read/write has deterministic log markers; the scripts record write return values but make no unsupported claim about the runtime reaction to a failed `OnStoreSave` write.

## Reopened source evidence

| Classification | Reopened path / pinned revision | Relevant symbols or lines | Use and boundary |
|---|---|---|---|
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/3_game/entities/entityai.c`, SHA-256 `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5` | 2913-3070, `OnStoreSave`, `OnStoreLoad` | Establishes server-side callbacks, parent propagation, same stream order, and checked required reads. It does not expose native record framing or failure consequences. |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/1_core/proto/serializer.c`, SHA-256 `3C365E5EF418438220CD2A2012C57EF385DDCAD835D712D136D31E6DFE7D2F5D` | 1-65, `Serializer.Write`, `Serializer.Read` | Establishes `bool` method declarations only. |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/3_game/gameplay.c`, SHA-256 `AA12624843F51C70200D37449559FDBADB042D333D4EE74C989E0CA632D2F0FE` | 15-16 | Establishes `ParamsReadContext` / `ParamsWriteContext` aliases. |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/core/inherited/itemoptics.c`, SHA-256 `814AB79D363BCC0AF6FB3434D391FE1059840562DCC0A5001193B489DE03B9B3` | 303-331 | Corroborates parent-first callbacks and an engine-version layout gate. |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase.c`, SHA-256 `22283A8E3869CAF8CE1D6BFE5606057575C4F2C315E766723D3F44DAA7E47F4F` | 420-474 | Corroborates matching ordered fields, defaulting before a failed required read, and later `AfterStoreLoad` reconstruction. |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase/fence.c`, SHA-256 `38059886AF6313CF8442D1362A183021A863616E1CD12878D6663BFCC1C65B60` | 212-256 | Corroborates compatibility branches that preserve stream position. |
| Extracted DayZ snapshot | `D:/DayZ Projects/DZ/gear/consumables/config.cpp` and `scripts/4_world/entities/itembase/battery9v.c` | config 913 onward; script 1 onward | Establishes the real Battery9V config/script lineage and inherited vanilla model/config. No new asset was added. |
| Official DayZ Samples cache | `TEMP/server-mission-investigation/reference/DayZ-Samples/Test_Building/config.cpp` | `CfgPatches`, `CfgVehicles` | Reopened as a config-layout reference only; this fixture does not borrow its model. |
| Pinned third party | `DayZ-CommunityFramework` commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, `CF_ModStorageObject.c:25-161`, SHA-256 `4B37540E26D7F708AA8B53715C7D11B2F95C7FC18A9E7ADBF5D6E244A9B6F242` | CF framing/version implementation | Demonstrates CF’s separate, framework-owned framing and confirms it is not proof of vanilla framing. |
| Existing local packaging evidence | `TEMP/multi-pbo-confirmation/build/.../receipt.json` | Addon Builder / BankRev paths and hashes | Reused only the observed archive-helper conventions and raw-backslash prefix convention; no settled multi-PBO result was re-audited. |

For a future spawn harness, the reopened snapshot declares `CGame.CreateObjectEx(string, vector, int, int)` in `scripts/3_game/global/game.c:702` and uses `MissionServer.OnInit()` in `scripts/5_mission/mission/missionserver.c:83-91`. CF’s in-memory test invokes `OnStoreSave` and `OnStoreLoad` through `ScriptReadWriteContext`; it is not a server persistence test. The reopened sources did not show a generic entity-world-save or clean-shutdown API, so no harness code or lifecycle claim was invented.

## Archive-only validation

The fixture helper invoked installed DayZ Experimental Tools Addon Builder `1.0.240639` with `-packonly`, then verified the requested raw-backslash prefix and both source members using BankRev. The final successful receipts are isolated under `TEMP/entity-persistence-fixture/build/`; no signing or keys were generated.

| Variant | PBO SHA-256 | Bytes | Receipt |
|---|---|---:|---|
| v1 | `146890DF99DC32188BB87C39D39ECE3A2A11E9A77B4E50042178D0CFE2FE0730` | 2373 | `final-build/entity-persistence-v1-20260914-010328-553331bb/receipt.json` |
| v2 | `1EAC1A7207E94EE346C789AD78076DA81E101CDED1B0D4E0E2DCD8C908719A3A` | 3111 | `final-build/entity-persistence-v2-20260914-010331-dff0b183/receipt.json` |
| declared-v2-missing-field | `73E348B80FCDF4516BFD95815A56DC3D6A34C1B8386A4431625BB0DEA3CB6753` | 2621 | `final-build/entity-persistence-declared-v2-missing-field-20260914-010334-08ae8700/receipt.json` |

Both successful member tables contain `EntityPersistenceFixture\\config.cpp` and `EntityPersistenceFixture\\scripts\\4_world\\entitypersistencefixture\\entitypersistencefixturebattery.c`; BankRev reports prefix `EntityPersistenceFixture\\`. Tool hashes: Addon Builder `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`; BankRev `2C35799EB437DEACB3720F8D322A399D935739537EBA335839E873AA21A26A75`.

`-packonly` creates/inspects PBOs but does not validate Enforce Script compilation. No standalone compiler invocation was established from the reopened evidence without a game/tool workflow, so compilation remains pending. No `npm` build applies to this non-site-fixture scope.

## Pending runtime matrix

The fixture README records the ordered test plan: v1 same-build reload; hash-preserved v1 storage reopened by v2 with `locked = false`; explicit `SetFixtureLocked(true)` followed by v2 save/reload; then a declared-v2-missing-field case bracketed by valid v2 controls. Each future run must use new disposable storage and retain executable, PBO/source, storage-before/after, mod-order, callback-log, ID/position, and clean-exit evidence.

Residual unknowns are intentionally unchanged: native storage-version forwarding, vanilla framing and omitted/wrong-type serializer behavior, `OnStoreLoad(false)` treatment, following-record isolation, save timing, and mod removal/shared-class compatibility. No runtime trial was started before council review.
