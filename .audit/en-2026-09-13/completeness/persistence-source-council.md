# Independent Council: Entity Persistence Source Research

**Review date:** 2026-09-14  
**Role:** independent reviewer; not the author  
**Repository revision:** `23c336eb5740b6b5e5d2d8bc2329288b70ccc26c`  
**Scope:** `OnStoreSave` / `OnStoreLoad`, engine storage version versus mod schema, ordered reads, and the proposed v1/v2/incomplete-record fixture  
**Decision:** conditional acceptance of the prose after the exact revisions below. The example is source-reviewed only; it was not compiled, packaged, saved, restarted, or run.

Author delivery hashes were generated with `Get-FileHash -Algorithm SHA256`:

- `persistence-source-research.md`: `AE2803D1FE5398BA16B13E6A1528C97842FBDDB505F671D5D05E7BF24E9B7525`
- `persistence-source-research.json`: `4FCBE564070F8518E20BEBB1B3031E7A0BFA794A144A723E9F9DEEB4CAFB11A1`

---

## Executive decision

The intake correctly identifies a real EN gap and correctly rejects using the callback `version` as a mod-controlled schema. The extracted `EntityAI` documentation establishes server-side callbacks, hierarchy propagation, same-format/same-order reads, per-read result checks, and `false` failure returns. Vanilla `ItemOptics`, `BaseBuildingBase`, and `Fence` corroborate those patterns; `game.c` registers `GAME_STORAGE_VERSION = 142` in this extraction, and vanilla readers branch on the callback argument at historical engine-layout thresholds.

Three qualifications are required before implementation:

1. Static script does not expose the native handoff from `StorageVersion(...)` to the callback. Call the argument **engine-owned storage-version context**, note that vanilla uses it for engine layout compatibility, and identify `142` only as this snapshot's registered value. Do not claim a native call trace that was not opened.
2. Direct callback serialization does not establish a framed, isolated “custom segment.” In a custom leaf class, the schema can be the first field written by that override after `super`; multiple mods patching shared classes need coordinated ordering or an independently proven framing/presence design.
3. `Serializer.Read` returning `false` establishes failure. The declarations do not prove that every omitted or wrong-type field necessarily returns `false` in the native persistence serializer. CF v5 performs its own count/type checks, which are framework behavior, not a vanilla guarantee.

The proposed class is structurally consistent with the reopened callback signatures and common Enforce syntax. It is not a complete runnable fixture: it lacks the entity `config.cpp`, script-module/PBO placement, spawn/save harness, logging, and compiled/runtime evidence.

---

## Finding dispositions and exact reader-facing wording

### PERSIST-C01-A — revision required; substance accepted

The canonical location after `EntityAI` **Lifecycle Events** is accepted. Replace the proposed prose with:

> `OnStoreSave()` and `OnStoreLoad()` are server-side entity-persistence callbacks. In an override, call `super.OnStoreSave(ctx)` before writing your fields. On load, call `super.OnStoreLoad(ctx, engineVersion)` first and return `false` if the parent fails. Read the same types in the same order and under the same compatibility branches used when writing. Check every `ctx.Read(...)`; if a required read returns `false`, return `false`. Supply a default and continue only when that omission is an explicitly supported older layout.
>
> The callback's `engineVersion` is engine-owned storage-version context; vanilla code uses it to select historical engine layouts. In the reviewed extraction, `CGame` registers `GAME_STORAGE_VERSION = 142`, but your mod does not control when that value changes. For a custom entity layout you control, write a separate mod schema integer as the first field added by your override after `super`, read it into a different variable, validate its supported range, and branch on that value. Introduce the marker in the first persisted schema. Existing unframed records, several mods extending the same class, and mod removal or reinstallation need a separately designed and tested compatibility/framing strategy.

Keep the proposed code block, but label it exactly:

> **Source-reviewed skeleton — not yet compiled or run.** This shows the ordering and version split for one custom leaf entity. A runnable fixture also needs entity configuration, script/PBO placement, a server spawn/save harness, and restart assertions.

After the code, add:

> `Serializer.Write(...)` returns `bool`, but `OnStoreSave(...)` returns `void`. The reviewed source and this unrun example do not establish how the persistence runtime handles a failed write.

Rejected wording:

- “first field of your custom segment” — direct callbacks were not shown to provide a framed per-mod segment.
- “a missing, truncated, or wrong-type field is a load failure” as an unconditional native behavior claim — the supported claim is that a required `Read` result of `false` must be handled as failure.
- An unqualified identity between the callback argument and `GAME_STORAGE_VERSION` — strongly supported by layout gates and registration, but the native forwarding implementation was not opened.

### PERSIST-C01-B — accepted with the same version qualification

Replace the troubleshooting cell with:

> Call `super` first on both paths. Read the same types in the same order you wrote them, and return `false` as soon as any required `ctx.Read(...)` returns `false`. The callback's `version` is engine-owned storage-version context used by vanilla compatibility branches; it is not your mod's `CURRENT_SCHEMA`. For a custom entity layout you control, write a separate schema number as the first field added by your override after `super`, read it into a separate variable, validate it, and use that value to select your old/new layout. Older unframed records need a separately tested migration strategy.

This corrects the current EN row, which uses one ambiguous `version` name for two domains and says “first” without accounting for inherited data written by `super`.

### PERSIST-C01-C — accepted

After the save example, add:

> `BaseBuildingBase.OnStoreLoad()` first calls `super.OnStoreLoad(ctx, version)` and propagates failure. It then reads `m_SyncParts01`, `m_SyncParts02`, `m_SyncParts03`, and `m_HasBase` in exactly the order written, returning `false` when a read fails. `AfterStoreLoad()` runs the later reconstruction step (`SetPartsAfterStoreLoad()`); it does not replace deserializing those stored fields. For custom schema changes, follow the entity-persistence versioning contract in [Entity System](01-entity-system.md#entity-persistence-callbacks).

The target anchor is illustrative until the canonical heading is actually chosen; implementation must make the link match the final heading.

### PERSIST-C01-D — partially accepted; narrow the cross-links

The JSON/config contrast is accepted. Add near the introduction of `en/07-patterns/04-config-persistence.md`:

> This chapter covers reflected JSON configuration and explicit file I/O. It does not cover the ordered `ParamsWriteContext` / `ParamsReadContext` stream used by entity `OnStoreSave()` and `OnStoreLoad()` callbacks; see [Entity System](../06-engine-api/01-entity-system.md#entity-persistence-callbacks).

An operator link is justified only where the page already discusses mod-update/restart load failures. Use:

> If custom entity fields disappear after a mod update, inspect the mod's `OnStoreSave()` / `OnStoreLoad()` order and schema migration before wiping storage; see [Entity System](../06-engine-api/01-entity-system.md#entity-persistence-callbacks). A failed callback's effect on the entity is runtime-dependent and is not established by this guide.

Do not scatter a generic link across both server pages without a matching symptom/context. `en/09-server-admin/07-persistence.md` explains operator storage; `en/09-server-admin/11-troubleshooting.md` is the better single home if it has the relevant failure row. This is an editorial scope decision, not a newly established engine fact.

---

## Evidence findings

### Accepted static evidence

- `entityai.c:2913-2994` explicitly documents server-side save/load callbacks, hierarchy propagation, matching format/order, checked reads, and `false` on failed required reads in its example.
- `entityai.c:2994-3070` uses the callback argument for `<= 103` and `>= 140` layout branches. Its energy read at `3000-3003` also proves that vanilla sometimes deliberately substitutes a default rather than immediately returning `false`; therefore “return false for every failed read” is guidance for required fields, not a universal description of every vanilla read.
- `game.c:5,49-50` registers `GAME_STORAGE_VERSION = 142` in this extraction.
- `serializer.c:55-61` establishes `bool Write`, `bool Read`, `CanWrite`, and `CanRead`; `gameplay.c:15-16` aliases the contexts to `Serializer`.
- `ItemOptics` calls `super` first, propagates parent failure, and gates its field at callback version `126`.
- `BaseBuildingBase` writes and reads four fields in matching order, resets the failed target to a default, returns `false`, and reconstructs derived state later in `AfterStoreLoad()`.
- `Fence` consumes one old or new field under the `< 110` branch before reading the common next field, illustrating stream-position preservation.

### Third-party and local-source limits

- CF cleanly separates callback `version`, CF format `VERSION = 5`, and per-mod `m_Version` from `CfgMods.storageVersion`. Its v5 per-mod reader verifies entry bounds and exact types.
- CF does **not** prove vanilla framing or vanilla wrong-type handling. It serializes its own count/type-tagged entries. In addition, `CF_ModStorageObject.OnStoreLoad_CF` logs a failed `CF_OnStoreLoad` but still returns `true`; only failure to complete CF's outer stream returns `false`. The intake's CF summary should preserve this distinction.
- `REFERENCIA_VERSOES_E_MIGRACAO.md:460-461` is rejected as authority for mod schema migration through the callback engine version; its later recommendation to keep a separate mod-owned version is the safe portion.
- The StarDZ group-stash comments assert expected standard entity persistence but explicitly lack a game test; the implemented persistence there is JSON bookkeeping and does not validate these callbacks.

---

## Fixture feasibility and required revision

The v1/v2 upgrade fixture is feasible in principle but is not ready to claim runnable. Revise the plan as follows:

1. Define one isolated configured entity classname, its `CfgPatches`/`CfgVehicles` entry, 4_World script placement, exact mod/PBO layout, spawn coordinates, persistence eligibility, and deterministic save/clean-shutdown procedure.
2. Build v1, write `schema=1`, `charges=17`, and `label="v1-control"`, then reload it once under the same v1 build. This same-build control must succeed before the upgrade is interpreted.
3. Preserve a hash-identified copy of the v1 storage, upgrade to v2, and verify schema 1 restores with `locked=false`. Then explicitly set `locked=true`, save as v2, restart, and verify `true` survives; resaving the default `false` would be a weak discriminator.
4. Rename “truncated declared-v2” to **declared-v2 missing-field fixture**. A clean bad writer that omits `locked` creates a semantically incomplete custom layout, not proven byte-level truncation of the engine record. Log every successful preceding write and every read result. Treat `Read(m_Locked) == false` as the hypothesis: direct serializer framing/type behavior is not established, so a succeeding read could mean later stream data was consumed.
5. Put a valid v2 entity before and after the bad entity, or use separately identified controls, and record whether both controls load. Do not infer record isolation, entity deletion, reset, retention, or following-record behavior from static source.
6. Record exact executable/build hashes, source/config/PBO hashes, launch line, mod order, storage before/after hashes, callback logs, persistent IDs/positions, and clean process exits. Preserve the intake's stopping condition: one valid chain and one repeated bad/control pair; stop and return to source analysis on inconsistent behavior.

The smallest justified next step is **not** a game run. First implement only the revised canonical subsection and troubleshooting/construction corrections, then independently inspect the exact diff. Separately scaffold and compile the isolated fixture with its missing config/harness pieces. Only after compile/package success should the controlled v1/v2/restart matrix run.

---

## Reopened source ledger

All hashes below were recomputed during this council with PowerShell `Get-FileHash -Algorithm SHA256`.

| Classification | Path / commit | Lines | SHA-256 | Council use |
|---|---|---:|---|---|
| Extracted script snapshot | `D:/DayZ Projects/scripts/3_game/entities/entityai.c` | 2913-3070 | `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5` | Callback docs and vanilla implementation |
| Extracted script snapshot | `D:/DayZ Projects/scripts/3_game/global/game.c` | 5, 49-50 | `CF529055C48596108034CE6B11826B09BBF5D93E6C550E37785947873D8C3158` | Registered storage version in snapshot |
| Extracted script snapshot | `D:/DayZ Projects/scripts/1_core/proto/serializer.c` | 1-65 | `3C365E5EF418438220CD2A2012C57EF385DDCAD835D712D136D31E6DFE7D2F5D` | Serializer declarations |
| Extracted script snapshot | `D:/DayZ Projects/scripts/3_game/gameplay.c` | 15-16 | `AA12624843F51C70200D37449559FDBADB042D333D4EE74C989E0CA632D2F0FE` | Context typedefs |
| Extracted script snapshot | `D:/DayZ Projects/scripts/4_world/entities/core/inherited/itemoptics.c` | 303-331 | `814AB79D363BCC0AF6FB3434D391FE1059840562DCC0A5001193B489DE03B9B3` | Hierarchy and version gate |
| Extracted script snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase.c` | 420-474 | `22283A8E3869CAF8CE1D6BFE5606057575C4F2C315E766723D3F44DAA7E47F4F` | Ordered fields and reconstruction |
| Extracted script snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase/fence.c` | 212-256 | `38059886AF6313CF8442D1362A183021A863616E1CD12878D6663BFCC1C65B60` | Old/new branch alignment |
| Extraction metadata | `D:/DayZ Projects/scripts.txt` | 1-3 | `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F` | `product=dayz`, raw `version=124588`; not wholesale build provenance |
| Local research lead | `D:/StarDZ/docs/REFERENCIA_VERSOES_E_MIGRACAO.md` | 374-503 | `E3BBC9D5295202BA063F7D3B3659B2928F32171F811BBA8B8B0A201B6F97EFCD` | Version-domain conflict and safer later recommendation |
| Local research lead | `D:/StarDZ/docs/DAYZ_MOD_ARCHITECTURE_PATTERNS.md` | 2242-2295 | `315C4C07A240C46D239984288F903860D46076A34376AC9CEDF5281D57D87B5B` | CF-oriented pattern only |
| Local research lead | `D:/StarDZ/docs/GUIA_SEGURANCA_E_MULTIPLAYER.md` | 1086-1195 | `43AAECA6B5A5353499FE592C47615766EDE14DC8AB53B9E21B6551E32CFB07E8` | Defensive serializer guidance only |
| Beta implementation | `D:/StarDZ/StarDZ_Systems/StarDZ_Systems/Scripts/3_Game/StarDZ_Systems/Groups/SDZ_GroupStash.c` | 1-251 | `4A8149C81E759084D7A1973A7E8E3173F8A2C5CE603198075EB44025474C47AA` | Untested expectation plus separate JSON code |

Pinned CF checkout: `https://github.com/Arkensor/DayZ-CommunityFramework.git`, commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, clean when reopened at `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/DayZ-CommunityFramework` on 2026-09-14.

| CF path | Lines | SHA-256 |
|---|---:|---|
| `JM/CF/Scripts/4_World/CommunityFramework/Entities/ItemBase.c` | 1-87 | `159DB6F8DC122BF7F7D00186107D33918A7C7B1C52CEBC226776AA10DF2A2C58` |
| `JM/CF/Scripts/4_World/CommunityFramework/ModStorage/CF_ModStorageObject.c` | 25-161 | `4B37540E26D7F708AA8B53715C7D11B2F95C7FC18A9E7ADBF5D6E244A9B6F242` |
| `JM/CF/Scripts/3_Game/CommunityFramework/ModStorage/CF_ModStorage.c` | 1-305 | `6FCF72DDC889D751F02BE1097DBC19126F851E7712A90EC2F52FA61B4E59D7B0` |
| `JM/CF/Scripts/3_Game/CommunityFramework/Mods/ModStructure.c` | 302-315 | `E1257321B4F711A72C1703319DB980CDA376C7CFC24955723720BEDA23C131A8` |

Current EN file hashes matched the author intake for all six reviewed pages. No EN file, build, compiler, packer, game, or server was run by this council.

---

## Unresolved

- Native propagation of `StorageVersion(...)` into the callback argument was not visible in the reopened script declarations.
- Direct persistence serializer behavior on an omitted final field, wrong type, or bytes beyond an override remains untested.
- Runtime consequences of `OnStoreLoad()` returning `false`, including entity and following-record treatment, remain unknown.
- Existing unframed data, several mods patching the same inheritance chain, and mod removal/reinstallation need separate design and tests.
- The extracted files remain individually hashed snapshots, not proven byte-identical to the separately cited Script Diff commit.
- The example has prose approval only after revision; it has no compilation or runtime approval.
