# Entity persistence fixture

This isolated fixture packages one configured leaf entity, `EntityPersistenceFixtureBattery`, derived from vanilla `Battery9V`. It inherits the vanilla model and item configuration; it adds no art, keys, production configuration, or storage data.

## Variants

- `v1` writes mod schema `1`, `charges = 17`, and `label = "v1-control"` after `super.OnStoreSave(ctx)`.
- `v2` accepts schema `1` with `locked = false` as an explicit default, and writes/reads schema `2` with the added `locked` field.
- `matrix` keeps the v2 field layout for every entity. Its non-persisted `m_OmitLockedOnSave` flag defaults to `false`; setting it to `true` for one instance deliberately omits only that instance's final `locked` write. `SetFixtureCaseLabel`, `SetFixtureLocked`, and the assertion getters make a bad entity distinguishable from valid v2 controls before and after a restart.

Each variant has the same configured class name, patch identity, canonical output name (`EntityPersistenceFixture.pbo`), and single-level PBO prefix (`EntityPersistenceFixture`). Its `CfgMods` world-script virtual path is `EntityPersistenceFixture/scripts/4_World`, following the pinned Samples and Community Framework recipe. The helper renames its one fresh Addon Builder output to the manifest name before BankRev inspection; replacing that PBO is the intended upgrade variable, so do not place two variants together.

## Source basis and limits

The scripts use the `EntityAI` callback contract in the extracted snapshot at `D:/DayZ Projects/scripts/3_game/entities/entityai.c:2913-3070`: call `super` first, preserve write/read order, and return `false` when a required `Read` returns `false`. `Battery9V` is a real `ItemBase` script class (`scripts/4_world/entities/itembase/battery9v.c:1`) and its vanilla config entry inherits `Inventory_Base` and declares the model (`DZ/gear/consumables/config.cpp:913-957`).

The callback parameter is named `engineVersion` in this fixture to avoid confusing it with the mod-owned schema field. The source snapshot declares `Serializer.Write` and `Serializer.Read` as `bool`, but `OnStoreSave` returns `void`; this fixture logs write results without asserting how the native persistence runtime reacts to a failed write.

## Package-only build and inspection

Run this only with the installed DayZ Experimental Tools path and a disposable directory outside this fixture:

```powershell
./build.ps1 -ToolRoot 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools' -WorkRoot 'D:\StarDZ\docs\wiki\TEMP\entity-persistence-repair' -Variant v1
```

The helper accepts only that disposable `TEMP/entity-persistence-repair` root (or a child), rejects reparse points from `TEMP` through its generated run and Addon Builder `-clear` paths, creates a unique nonexistent child run without `-Force`, and confines the ordinary physical `-clear` directory to that run. It uses Addon Builder with `-packonly`, renames the sole output to the manifest PBO name, then BankRev checks the requested prefix plus the complete, case-insensitively unique source-member set; the receipt hashes the PBO and all three logs. This is archive packaging and inspection only: it does not compile Enforce Script or run DayZ. No known standalone script-compiler command was found in the reopened source/tool evidence, so compilation is pending a council-approved game/tool workflow.

## Future runtime matrix — not executed

Use a fresh, explicitly disposable server profile/storage directory; never point this fixture at a real server profile or copy real storage into it. The inspected source exposes `CGame.CreateObjectEx(string, vector, int, int)` (`scripts/3_game/global/game.c:702`) and `MissionServer.OnInit()` (`scripts/5_mission/mission/missionserver.c:83-91`), but it does not expose a generic entity-world save or clean-shutdown API; do not add one by inference.

1. With only `v1` installed, spawn the configured class through a council-reviewed mission harness or controlled operator method. Record its persistent ID, position, fixture log markers, PBO/source hashes, storage hashes, mod order, and clean process exit.
2. Perform a clean, externally controlled shutdown and reload the same `v1` build. Confirm the `v1-control` and `17` markers before interpreting an upgrade.
3. Preserve a hash-identified copy of the v1 storage, replace the PBO with `v2`, reload, and confirm the v1 record reads with `locked = false`.
4. Set `locked = true` through a council-reviewed harness calling `SetFixtureLocked(true)`, save and cleanly restart with `v2`, then confirm the true marker survives.
5. For the bad-writer case, use the `matrix` build and place a per-instance `SetFixtureOmitLockedOnSave(true)` entity between separately labeled valid v2 controls, whose flags remain at the default `false`. Record each `MATRIX_SET`, `SAVE`, `LOAD_OK`, and `LOAD_FAIL` marker, the case label, position, persistent-ID blocks, and assertion-getter result. A failed `Read(m_Locked)` is the test hypothesis; static source does not establish record isolation, entity treatment, or following-record behavior.

Stop after one valid chain and one repeated bad/control pair, or earlier on inconsistent behavior, and return to source analysis. Do not infer server-save timing, record framing, serializer wrong-type behavior, or `OnStoreLoad` failure consequences from this fixture.

The mission/operator harness, Central Economy persistence eligibility, save timing, and graceful shutdown procedure remain pending separate source research; this fixture does not invent them.
