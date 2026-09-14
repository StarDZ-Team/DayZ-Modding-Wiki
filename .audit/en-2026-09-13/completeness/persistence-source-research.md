# PERSIST-C01 entity-persistence source intake

Date: 2026-09-14  
Wiki revision inspected: `23c336eb5740b6b5e5d2d8bc2329288b70ccc26c`  
Scope: entity `OnStoreSave` / `OnStoreLoad` serialization only. JSON databases, backup policy, and general server storage are out of scope.

## Result

The strongest existing home for a concise canonical explanation is `en/06-engine-api/01-entity-system.md`, immediately after **EntityAI → Lifecycle Events**. It already owns `EntityAI` callbacks, while `en/07-patterns/04-config-persistence.md` explicitly teaches reflected JSON configuration and would blur two different persistence formats. If the material grows into a full runnable lab, the cleaner long-term home is the coverage map's proposed `en/07-patterns/08-entity-persistence-migration.md`, linked from the entity page; this intake does not create that page.

The current EN tree has one materially misleading troubleshooting recipe and two important omissions. `en/troubleshooting.md:196` says to write a version first and then use `if (version < CURRENT)`, without distinguishing the callback's engine-owned `version` from a mod-owned schema field. `en/06-engine-api/01-entity-system.md:785-800,976-982` does not list or explain the storage callbacks. `en/06-engine-api/17-construction-system.md:206-221` shows only the save half and then jumps to `AfterStoreLoad()`, omitting the matching ordered reads and their failure returns.

## Opened evidence

### Extracted DayZ scripts: static source evidence

The local extraction is a hashable snapshot, not a wholesale build attribution. Its adjacent `D:/DayZ Projects/scripts.txt` says `product=dayz`, raw `version=124588` (SHA-256 `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F`). The audit separately identifies official DayZ Script Diff commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1` as Build `1.29.163709`, Scripts Rev. `125372`, but this task did not recreate an upstream byte comparison for the persistence files.

| File and lines opened | SHA-256 | What the source establishes |
|---|---|---|
| `D:/DayZ Projects/scripts/3_game/entities/entityai.c:2913-2994,2994-3070` | `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5` | The callbacks are server-side persistence hooks. The embedded example says to propagate through the hierarchy, read the same format and order as written, check every `Read`, and return `false` on failure. The implementation gates old engine layouts with the callback `version` (`<= 103`, `>= 140`). |
| `D:/DayZ Projects/scripts/3_game/global/game.c:5,49-50` | `CF529055C48596108034CE6B11826B09BBF5D93E6C550E37785947873D8C3158` | This snapshot defines `GAME_STORAGE_VERSION = 142` and passes it to `StorageVersion(...)`. This is evidence of the engine/script storage revision in this snapshot, not a mod schema number. |
| `D:/DayZ Projects/scripts/1_core/proto/serializer.c:1-65` | `3C365E5EF418438220CD2A2012C57EF385DDCAD835D712D136D31E6DFE7D2F5D` | `ParamsReadContext` / `ParamsWriteContext` are serializers (`gameplay.c:15-16`); `Serializer.Read` and `Write` return `bool`, and the API serializes primitives, containers, arrays, and classes. |
| `D:/DayZ Projects/scripts/4_world/entities/core/inherited/itemoptics.c:303-329` | `814AB79D363BCC0AF6FB3434D391FE1059840562DCC0A5001193B489DE03B9B3` | A concrete vanilla subclass calls `super` first on save and load, returns `false` if the parent fails, and reads a field only for engine storage `version >= 126`. |
| `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase.c:420-474` | `22283A8E3869CAF8CE1D6BFE5606057575C4F2C315E766723D3F44DAA7E47F4F` | `BaseBuildingBase` writes four fields in a fixed order, reads the same four in that order, assigns defaults and returns `false` on a failed read, then restores derived state in `AfterStoreLoad()`. |
| `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase/fence.c:212-256` | `38059886AF6313CF8442D1362A183021A863616E1CD12878D6663BFCC1C65B60` | A vanilla migration branches on engine storage `version < 110`, reading a legacy field for old records and the replacement field for newer records; both branches preserve stream position before reading the next field. |

These files establish declarations and shipped script patterns. They do **not** establish the engine's exact reaction to a callback returning `false`, whether a failed entity is deleted, how a corrupted record affects following records, or that any proposed fixture compiles or survives a restart.

### Local documentation: research leads, not authority

| File and lines opened | SHA-256 | Assessment |
|---|---|---|
| `D:/StarDZ/docs/REFERENCIA_VERSOES_E_MIGRACAO.md:374-503` | `E3BBC9D5295202BA063F7D3B3659B2928F32171F811BBA8B8B0A201B6F97EFCD` | Correctly identifies `GAME_STORAGE_VERSION`, the hierarchy/same-order contract, and the value of per-mod schema versions. Lines 460-461 are too broad: the callback `version` is shown by vanilla as an engine-layout revision; it is not a mod-controlled schema version. Lines 500-503 contain the safer recommendation: store a separate mod-owned version. |
| `D:/StarDZ/docs/DAYZ_MOD_ARCHITECTURE_PATTERNS.md:2242-2295` | `315C4C07A240C46D239984288F903860D46076A34376AC9CEDF5281D57D87B5B` | The CF appendix demonstrates hierarchy propagation, ordered reads, immediate failure returns, and a CF-owned storage version. It is framework guidance, not vanilla behavior. |
| `D:/StarDZ/docs/GUIA_SEGURANCA_E_MULTIPLAYER.md:1086-1195` | `43AAECA6B5A5353499FE592C47615766EDE14DC8AB53B9E21B6551E32CFB07E8` | Relevant boundary: serialization is not authentication, persistent player keys must not use the reusable session `GetPlayerId()`, and code without exceptions must check every `ctx.Read()`. This supports defensive wording but does not describe entity persistence runtime. |

### StarDZ beta implementation: implementation evidence only

`D:/StarDZ/StarDZ_Systems/StarDZ_Systems/Scripts/3_Game/StarDZ_Systems/Groups/SDZ_GroupStash.c:1-251` (SHA-256 `4A8149C81E759084D7A1973A7E8E3173F8A2C5CE603198075EB44025474C47AA`) is the only `OnStoreSave` / `OnStoreLoad` hit found in StarDZ source outside the wiki, and those names occur only in comments. Lines 53-59 assert that a script-spawned barrel and its contents should use normal `EntityAI` persistence but explicitly admit no game test. Lines 151-214 implement separate JSON bookkeeping with fail-closed load behavior. This beta code is useful as a warning against converting expectation into runtime fact; it is not an entity-serialization implementation and does not satisfy PERSIST-C01.

### Pinned public implementation: framework evidence only

Repository: `https://github.com/Arkensor/DayZ-CommunityFramework.git`  
Checkout: `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/DayZ-CommunityFramework`  
Commit: `0763e7e7548c9a0bed6626afff835de80693ebf3` (clean checkout when inspected)
Accessed: 2026-09-14

| File and lines opened | SHA-256 | What it demonstrates |
|---|---|---|
| `JM/CF/Scripts/4_World/CommunityFramework/Entities/ItemBase.c:1-87` | `159DB6F8DC122BF7F7D00186107D33918A7C7B1C52CEBC226776AA10DF2A2C58` | CF's `ItemBase` integration calls vanilla `super` first and propagates load failure. Its documented mod callback reads in order and uses the mod context's `GetVersion()`, explicitly sourced from `CfgMods.storageVersion`. |
| `JM/CF/Scripts/4_World/CommunityFramework/ModStorage/CF_ModStorageObject.c:25-161` | `4B37540E26D7F708AA8B53715C7D11B2F95C7FC18A9E7ADBF5D6E244A9B6F242` | CF writes its own format version and per-mod records, preserves unloaded-mod data, separates the callback engine version from CF's version, checks all header reads, and returns `false` when the stream cannot be completed. |
| `JM/CF/Scripts/3_Game/CommunityFramework/ModStorage/CF_ModStorage.c:1-305` | `6FCF72DDC889D751F02BE1097DBC19126F851E7712A90EC2F52FA61B4E59D7B0` | CF has framework format `VERSION = 5`, stores each mod's own `m_Version`, and rejects out-of-range or wrong-type sequential reads. |
| `JM/CF/Scripts/3_Game/CommunityFramework/Mods/ModStructure.c:302-315` | `E1257321B4F711A72C1703319DB980CDA376C7CFC24955723720BEDA23C131A8` | `GetStorageVersion()` returns the mod's configured storage version, distinct from the engine callback version. |

CF corroborates a robust third-party design, but it adds framing and presence tracking that direct vanilla callbacks do not provide. Its behavior must not be described as an engine guarantee.

## Precise EN findings and proposed reader-facing additions

### PERSIST-C01-A — canonical callback contract is absent

Affected page: `en/06-engine-api/01-entity-system.md` (SHA-256 `84DED2A22E62A935C1AA0F98F0D32B1082473AE0C653DF6B4D77C63E2D9C39E4`), especially lines 785-800 and 976-982.

Add a subsection after **Lifecycle Events**, using wording like:

> `OnStoreSave()` and `OnStoreLoad()` are server-side entity-persistence callbacks. In every override, call `super.OnStoreSave(ctx)` before writing your fields; on load, call `super.OnStoreLoad(ctx, engineVersion)` first and return `false` if it fails. Your reads must match your writes in type, order, and version branch. Check every `ctx.Read(...)`; a missing, truncated, or wrong-type field is a load failure, not a default-value signal unless you deliberately support that older schema.
>
> The callback's `engineVersion` is DayZ's storage version (`GAME_STORAGE_VERSION` in the game scripts). Your mod does not own it. Store a separate mod schema integer as the first field of **your custom segment** (after `super`), increment it when your layout changes, and branch on that value. Introduce the marker in version 1; adding a marker later to already-saved unframed data is ambiguous and needs a separately proven compatibility strategy.

Proposed bounded example (source-reviewed, not yet compiled or run):

```c
class PCT_PersistBox extends ItemBase
{
    static const int MOD_SCHEMA_VERSION = 2;

    protected int m_Charges;
    protected string m_Label;
    protected bool m_Locked; // Added in v2

    override void OnStoreSave(ParamsWriteContext ctx)
    {
        super.OnStoreSave(ctx);
        ctx.Write(MOD_SCHEMA_VERSION);
        ctx.Write(m_Charges);
        ctx.Write(m_Label);
        ctx.Write(m_Locked);
    }

    override bool OnStoreLoad(ParamsReadContext ctx, int engineVersion)
    {
        if (!super.OnStoreLoad(ctx, engineVersion))
            return false;

        int schemaVersion;
        if (!ctx.Read(schemaVersion))
            return false;
        if (schemaVersion < 1 || schemaVersion > MOD_SCHEMA_VERSION)
            return false;
        if (!ctx.Read(m_Charges))
            return false;
        if (!ctx.Read(m_Label))
            return false;

        if (schemaVersion >= 2)
        {
            if (!ctx.Read(m_Locked))
                return false;
        }
        else
        {
            m_Locked = false;
        }

        return true;
    }
}
```

Do not claim that `ctx.Write(...)` failures are safely recoverable through this callback: `Serializer.Write` returns `bool`, but `OnStoreSave` itself returns `void`, and no save-failure runtime behavior was tested here.

### PERSIST-C01-B — troubleshooting conflates two version domains

Affected page: `en/troubleshooting.md:196` (SHA-256 `DA08530090F727F679BC051FB98899061A8AB80B9A58F26BDBD02A77E0053BE4`).

Replace the fix cell with:

> Call `super` first on both paths. Read the same types in the same order you wrote them, and return `false` as soon as any required `ctx.Read(...)` fails. The callback's `version` is the DayZ engine storage version; do not compare it with your mod's `CURRENT_SCHEMA`. Write a mod-owned schema number as the first field after `super`, read it into a separate variable, and use that value to select your old/new layout.

### PERSIST-C01-C — construction page shows only half the contract

Affected page: `en/06-engine-api/17-construction-system.md:206-221` (SHA-256 `CDA6F6997163EFBA17073A26C5147FCC6C01B0F5B588A58EA1490FAA87B1D066`).

After the save example, show or summarize `BaseBuildingBase.OnStoreLoad`: parent first, then `m_SyncParts01`, `m_SyncParts02`, `m_SyncParts03`, `m_HasBase`, returning `false` on each failed read. Clarify that `AfterStoreLoad()` reconstructs derived part state only after deserialization; it is not a replacement for reading the stored fields. Link to the canonical entity callback section for schema migration.

### PERSIST-C01-D — keep config and operator pages scoped

`en/07-patterns/04-config-persistence.md` (SHA-256 `33082B96074D4A1E1767426F070C333A4658FB822DBB33C6BAEB6786FFBC4374`) should retain its JSON/config focus and add only a short contrast/link: reflected JSON migration is not the ordered `ParamsReadContext` entity stream. `en/09-server-admin/07-persistence.md` (SHA-256 `7DE855D73B655D66019D6F99BB9D171B67893A181B72AE92439BB82E59FE6C53`) and `en/09-server-admin/11-troubleshooting.md` (SHA-256 `00ED8F7FD2ADBE348CCB43FEBD295BDDD9DBC77DAF30A6D27D10F75372495BC2`) should link operators from mod-update/restart failures to the canonical section, without teaching binary layouts in server-operations pages.

## One discriminating future fixture plan

Use an isolated custom entity classname and isolated `storage_<instanceId>` so no real server data is at risk. Record the exact DayZ/Diag executable version and hash, fixture source/PBO hashes, launch line, storage copy hashes, RPT/script-log paths, entity persistent ID/position, and clean process exit for every phase.

1. **v1 control:** compile/package a v1 fixture whose custom segment writes `schema=1`, `charges=17`, `label="v1-control"` after `super`. Spawn exactly one entity, request/allow a normal server save, stop cleanly, and preserve the untouched storage directory.
2. **v1 → v2 upgrade:** launch the same storage with the v2 reader shown above. Log the callback `engineVersion`, mod `schemaVersion`, each read result, restored values, the v2 default `locked=false`, final callback result, and whether the entity exists after load. Save cleanly as v2, restart once more, and verify the now-v2 field survives.
3. **truncated declared-v2 case:** in a separate isolated storage, use a deliberately bad writer that writes `schema=2`, `charges`, and `label` but omits the required v2 `locked` field, then cleanly stop. Launch the normal v2 reader once. The discriminating expectation is that the required `ctx.Read(m_Locked)` returns `false` and the callback returns `false`; separately observe, without presupposing, whether the engine drops, resets, or retains the entity and whether later records still load.
4. **Controls:** repeat the valid v2 record in the same build/storage recipe to show that any failure is caused by the omitted field rather than packaging or startup. Do not hand-edit a production `storage_1` file.

Stopping condition: stop after one complete valid chain and one independently repeated truncated/control pair produce the same callback markers. If the truncated read unexpectedly succeeds, later records are affected, or the engine reaction is inconsistent, stop variation testing immediately, preserve all storage/log hashes, and return to source/council analysis; do not spend tokens on ad hoc byte mutations or state a deletion/corruption rule from an ambiguous run.

## Remaining uncertainty

- No Enforce compilation, PBO build, server save/restart/load, corruption injection, or game/client test was performed.
- The exact engine behavior after `OnStoreLoad` returns `false` remains unknown.
- The extraction files are individually hashed snapshots; this task did not prove that each is byte-identical to official Script Diff commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1`.
- The proposed direct-callback schema assumes a custom entity whose persisted custom segment contained the marker from its first released schema. Adding fields to previously persisted vanilla/modded entities, mod removal/reinstallation, and coexistence among multiple mods require framing/presence design beyond this bounded intake; CF demonstrates one third-party solution but is not vanilla authority.
- This is evidence intake only, not author implementation or independent council approval.
