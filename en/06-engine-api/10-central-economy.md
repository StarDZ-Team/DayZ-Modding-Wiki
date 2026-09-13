# Central Economy Script API

> **Summary:** The Central Economy (CE) is DayZ's server-side spawning engine — it reads `types.xml`, `globals.xml`, `events.xml`, and the other mission XML files and keeps the world stocked with loot, vehicles, infected, and animals. This chapter covers the **script side** of the CE: the `CEApi` interface, ECE spawn flags, `CEItemProfile`, per-entity lifetime control, and the hooks the engine fires when the CE creates an entity.

---

## Table of Contents

- [The CE at a Glance](#the-ce-at-a-glance)
- [Where the XML Reference Lives](#where-the-xml-reference-lives)
- [The Hive and CE Availability](#the-hive-and-ce-availability)
- [Getting the CE API](#getting-the-ce-api)
- [ECE Spawn Flags](#ece-spawn-flags)
- [Rotation Flags (RF)](#rotation-flags-rf)
- [Reading an Item's Economy Profile](#reading-an-item-s-economy-profile)
- [Controlling Lifetime from Script](#controlling-lifetime-from-script)
- [Reading globals.xml from Script](#reading-globals-xml-from-script)
- [Avoidance Queries](#avoidance-queries)
- [The EEOnCECreate Hook](#the-eeoncecreate-hook)
- [Developer and Diagnostic Tools](#developer-and-diagnostic-tools)
- [Summary](#summary)

---

## The CE at a Glance

The Central Economy is an engine system that runs entirely on the server. On a continuous loop it:

1. Reads `types.xml` to learn every item's **nominal** (target count) and **min** (respawn threshold).
2. Matches items to spawn locations through **usage** flags (`Military`, `Town`, ...) and **value** flags (`Tier1`-`Tier4`).
3. Counts existing instances, and spawns replacements when a count drops below `min`.
4. Deletes items whose **lifetime** expires untouched.
5. Runs dynamic events (`events.xml`) for vehicles, helicopter crashes, and infected on their own schedule.

The CE is configured through XML files in the mission folder (`types.xml`, `globals.xml`, `events.xml`, `cfgspawnabletypes.xml`, `cfgrandompresets.xml`, `cfgeconomycore.xml`, `cfglimitsdefinition.xml`, `cfgeventspawns.xml`). Script code does not drive the spawn loop — but it can query the CE, adjust lifetimes, spawn through it, and react when it creates entities. That script surface is what this chapter documents.

---

## Where the XML Reference Lives

The full field-by-field XML reference is in the server administration part of this wiki:

- **[Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md)** — `types.xml`, `globals.xml`, `cfgspawnabletypes.xml`, `cfgrandompresets.xml`, `cfgeconomycore.xml`, `cfglimitsdefinition.xml`, tuning, and troubleshooting.
- **[Vehicle & Dynamic Event Spawning](../09-server-admin/05-vehicle-spawning.md)** — `events.xml`, `cfgeventspawns.xml`, and `cfgeventgroups.xml`.

---

## The Hive and CE Availability

The CE only exists when the mission initializes a **Hive** — the persistence backend that owns the economy. The vanilla mission `init.c` does this in `main()`:

```c
void main()
{
    // Initialize the economy
    Hive ce = CreateHive();
    if (ce)
    {
        ce.InitOffline();
    }

    // ... weather, date, mission setup ...
}
```

The `Hive` class (defined in `3_game/hive/hive.c`) exposes:

```c
class Hive
{
    proto native void InitOnline(string ceSetup, string host = "");
    proto native void InitOffline();
    proto native void InitSandbox();

    proto native bool IsIdleMode();

    proto native void SetShardID(string shard);
    proto native void SetEnviroment(string env);

    proto native void CharacterSave(Man player);
    proto native void CharacterKill(Man player);
    proto native void CharacterExit(Man player);
}

proto native Hive CreateHive();
proto native void DestroyHive();
proto native Hive GetHive();
```

Key consequences for mod code:

- **Server only.** A client connected to a server has no Hive and no CE. Only the server (or an offline/single-player mission that called `CreateHive()`) has one.
- **Null-check everything.** `GetCEApi()` returns `null` when no CE is running — for example in the main menu or on a client.

---

## Getting the CE API

`GetCEApi()` (defined in `3_game/ce/centraleconomy.c`) returns the `CEApi` interface:

```c
CEApi ce = GetCEApi();
if (!ce)
{
    return; // no CE on this machine (client, or no Hive)
}
```

The vanilla game itself uses this exact pattern — for example `DayZGame` reads a global economy variable only after checking the API exists:

```c
if (GetCEApi())
{
    bool wetUpdate = (GetCEApi().GetCEGlobalInt("WorldWetTempUpdate") == 1);
}
```

The `CEApi` methods fall into a few groups, covered in the sections below: lifetime manipulation, globals access, avoidance queries, and developer/diagnostic tooling.

---

## ECE Spawn Flags

When you spawn entities from script with `GetGame().CreateObjectEx()`, the **ECE flags** control both placement behavior and how the entity relates to the CE. They are plain `int` constants defined in `3_game/ce/centraleconomy.c`:

```c
proto native Object CreateObjectEx(string type, vector pos, int iFlags, int iRotation = RF_DEFAULT);
```

### Placement and Setup Flags

| Flag | Value | Meaning |
|------|-------|---------|
| `ECE_NONE` | 0 | No flags |
| `ECE_SETUP` | 2 | Process full entity setup (when creating a NEW entity) |
| `ECE_TRACE` | 4 | Trace under the entity when placing it |
| `ECE_CENTER` | 8 | Use the model shape's center for placement |
| `ECE_UPDATEPATHGRAPH` | 32 | Update the navmesh where the object is placed |
| `ECE_ROTATIONFLAGS` | 512 | Enable rotation flags for placement |
| `ECE_CREATEPHYSICS` | 1024 | Create the collision envelope and physics data |
| `ECE_INITAI` | 2048 | Initialize AI (infected, animals) |
| `ECE_AIRBORNE` | 4096 | Create a flying unit in the air |
| `ECE_NOSURFACEALIGN` | 262144 | Do not align the object to the surface |
| `ECE_KEEPHEIGHT` | 524288 | Keep the given height (no trace / surface placement) |
| `ECE_LOCAL` | 1073741824 | Create the object locally (not networked) |

### CE-Interaction Flags

| Flag | Value | CE Behavior |
|------|-------|-------------|
| `ECE_EQUIP_ATTACHMENTS` | 8192 | Equip the configured attachments from `cfgspawnabletypes.xml` |
| `ECE_EQUIP_CARGO` | 16384 | Fill the configured cargo from `cfgspawnabletypes.xml` |
| `ECE_EQUIP` | 24576 | Both of the above (`ECE_EQUIP_ATTACHMENTS + ECE_EQUIP_CARGO`) |
| `ECE_EQUIP_CONTAINER` | 2097152 | Populate a dynamic-event/group container during spawn |
| `ECE_NOLIFETIME` | 4194304 | Do not set a CE lifetime — the entity never despawns from idle cleanup |
| `ECE_NOPERSISTENCY_WORLD` | 8388608 | Do not save this object in world persistence |
| `ECE_NOPERSISTENCY_CHAR` | 16777216 | Do not save this object in character persistence |
| `ECE_DYNAMIC_PERSISTENCY` | 33554432 | Spawns without persistency; becomes persistent once a player takes it |

### Predefined Combinations

Use these instead of hand-building masks when they fit:

| Combination | Value | Composition |
|-------------|-------|-------------|
| `ECE_PLACE_ON_SURFACE` | 1060 | `ECE_CREATEPHYSICS \| ECE_UPDATEPATHGRAPH \| ECE_TRACE` |
| `ECE_IN_INVENTORY` | 787456 | `ECE_CREATEPHYSICS \| ECE_KEEPHEIGHT \| ECE_NOSURFACEALIGN` |
| `ECE_OBJECT_SWAP` | 787488 | `ECE_CREATEPHYSICS \| ECE_UPDATEPATHGRAPH \| ECE_KEEPHEIGHT \| ECE_NOSURFACEALIGN` |
| `ECE_FULL` | 25126 | `ECE_SETUP \| ECE_TRACE \| ECE_ROTATIONFLAGS \| ECE_UPDATEPATHGRAPH \| ECE_EQUIP` |

### Examples

**Spawn an item that persists forever (no CE lifetime):**

```c
vector pos = "7500 0 7500";
pos[1] = GetGame().SurfaceY(pos[0], pos[2]);
int flags = ECE_PLACE_ON_SURFACE | ECE_NOLIFETIME;
Object obj = GetGame().CreateObjectEx("Barrel_Green", pos, flags);
```

**Spawn a weapon with its CE-configured attachments and cargo:**

```c
vector pos = "7500 0 7500";
pos[1] = GetGame().SurfaceY(pos[0], pos[2]);
int flags = ECE_PLACE_ON_SURFACE | ECE_EQUIP;
Object obj = GetGame().CreateObjectEx("AKM", pos, flags);
// The AKM rolls its attachment slots per cfgspawnabletypes.xml
```

**Spawn event loot that becomes persistent only when picked up:**

```c
vector pos = "7500 0 7500";
pos[1] = GetGame().SurfaceY(pos[0], pos[2]);
int flags = ECE_PLACE_ON_SURFACE | ECE_DYNAMIC_PERSISTENCY;
Object obj = GetGame().CreateObjectEx("FirstAidKit", pos, flags);
```

See [Entity System](01-entity-system.md) for the general entity creation and deletion API.

---

## Rotation Flags (RF)

The fourth parameter of `CreateObjectEx()` takes **RF rotation flags** (also from `centraleconomy.c`), which control how the object may be oriented when placed:

| Flag | Value | Meaning |
|------|-------|---------|
| `RF_NONE` | 0 | No rotation flags |
| `RF_FRONT` / `RF_TOP` / `RF_LEFT` / `RF_RIGHT` / `RF_BACK` / `RF_BOTTOM` | 1 / 2 / 4 / 8 / 16 / 32 | Allow placement on that side |
| `RF_ALL` | 63 | All six sides |
| `RF_IGNORE` | 64 | Ignore placement RF flags — spawn as the model was created |
| `RF_RANDOMROT` | 64 | Allow random rotation around the axis when placing |
| `RF_ORIGINAL` | 128 | Use the default placement set up on the object in config |
| `RF_DEFAULT` | 512 | Use the default placement set up on the object in config |

```c
vector pos = "7500 0 7500";
pos[1] = GetGame().SurfaceY(pos[0], pos[2]);
Object obj = GetGame().CreateObjectEx("Mag_AKM_30Rnd", pos, ECE_PLACE_ON_SURFACE, RF_RANDOMROT);
```

---

## Reading an Item's Economy Profile

Every entity the CE tracks has a **`CEItemProfile`** — the parsed `types.xml` entry for its type. On the server you get it from `EntityAI.GetEconomyProfile()` (returns `null` when the type has no economy entry):

```c
class CEItemProfile
{
    proto native int   GetNominal();      // target count on the map
    proto native int   GetMin();          // minimum count before respawn
    proto native float GetQuantityMin();  // min quantity (0.0 - 1.0)
    proto native float GetQuantityMax();  // max quantity (0.0 - 1.0)
    proto native float GetQuantity();     // random quantity in that range (0.0 - 1.0)
    proto native float GetLifetime();     // default lifetime in seconds
    proto native float GetRestock();      // restock cooldown in seconds
    proto native int   GetCost();         // priority during respawn/cleanup
    proto native int   GetUsageFlags();   // usage flag bitmask
    proto native int   GetValueFlags();   // value (tier) flag bitmask
}
```

**Example — log the economy settings of the item a player is holding:**

```c
void PrintHeldItemEconomy(PlayerBase player)
{
    EntityAI held = player.GetHumanInventory().GetEntityInHands();
    if (!held)
    {
        return;
    }

    CEItemProfile profile = held.GetEconomyProfile();
    if (!profile)
    {
        Print(held.GetType() + " has no types.xml entry");
        return;
    }

    Print(held.GetType() + " nominal=" + profile.GetNominal() + " min=" + profile.GetMin());
    Print("lifetime=" + profile.GetLifetime() + " restock=" + profile.GetRestock());
}
```

Note the quantity getters return a **0.0-1.0 fraction**, while the `quantmin`/`quantmax` fields in `types.xml` are written as percentages (-1 to 100).

---

## Controlling Lifetime from Script

### Per-Entity Lifetime

`EntityAI` exposes direct control over the CE cleanup timer of a single entity (server side):

```c
// From 3_game/entities/entityai.c
proto native void  SetLifetime(float fLifeTime); // override REMAINING lifetime (seconds)
proto native float GetLifetime();                // remaining lifetime (seconds)
proto native void  IncreaseLifetime();           // reset lifetime to its default
proto native void  SetLifetimeMax(float fLifeTime); // override max lifetime for this instance
proto native float GetLifetimeMax();             // max lifetime (default comes from types.xml)
```

`IncreaseLifetimeUp()` is a script helper that resets the lifetime of an entity **and every parent up its inventory hierarchy** — this is what "touching" an item effectively does:

```c
void KeepAlive(EntityAI item)
{
    item.IncreaseLifetimeUp();
}
```

### Area Lifetime via CEApi

`CEApi` can adjust lifetimes in bulk. Results are clamped between 3 seconds and 10 years:

```c
CEApi ce = GetCEApi();
if (!ce)
{
    return;
}

vector center = "7500 0 7500";

// Extend everything within 100 m by one hour
ce.RadiusLifetimeIncrease(center, 100, 3600);

// Shorten everything within 100 m by 10 minutes
ce.RadiusLifetimeDecrease(center, 100, 600);

// Reset everything within 100 m to its types.xml default
ce.RadiusLifetimeReset(center, 100);

// Subtract 60 seconds from the lifetime of EVERY item in the world
ce.TimeShift(60);
```

`OverrideLifeTime(float seconds)` sets a debug lifetime applied to any dynamic event spawned afterwards; pass `0` to turn it off again.

---

## Reading globals.xml from Script

`CEApi` exposes typed getters for the `<var>` entries in `globals.xml`. The `type` attribute in the XML decides which getter matches: `type="0"` is int, `type="1"` is float, `type="2"` is string.

```c
CEApi ce = GetCEApi();
if (!ce)
{
    return;
}

int zombieMax = ce.GetCEGlobalInt("ZombieMaxCount");     // returns int.MIN if not found
float dmgMax = ce.GetCEGlobalFloat("LootDamageMax");     // returns float.MIN if not found
```

`CEApi` exposes typed getters for entries loaded from `globals.xml`. The inspected declarations and official CE documentation do not establish whether arbitrary custom `<var>` names are supported in every build, so treat custom globals as version-specific until tested on the target server. Use a mod-owned config file when portability matters. The full parameter reference for the documented variables is in [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md#globals-xml-economy-parameters).

---

## Avoidance Queries

The CE uses optimized internal checks to avoid spawning dynamic events on top of players and vehicles. The same checks are exposed to script — useful for custom spawners that should behave like the CE:

```c
CEApi ce = GetCEApi();
if (!ce)
{
    return;
}

vector pos = "4500 0 10200";

// true = area is clear of players within 500 m; false = a player is inside
bool clearOfPlayers = ce.AvoidPlayer(pos, 500);

// true = area is clear of vehicles; optional third parameter narrows it
// to one dynamic event name (empty string = all vehicles)
bool clearOfVehicles = ce.AvoidVehicle(pos, 500, "VehicleCivilianSedan");

// Exact player count within a radius
int players = ce.CountPlayersWithinRange(pos, 1000);

if (clearOfPlayers && clearOfVehicles)
{
    // safe to place a custom event here
}
```

Note the polarity: `AvoidPlayer()`/`AvoidVehicle()` return **true when the area is clear** (the avoidance succeeded) and false when something is inside the radius.

---

## The EEOnCECreate Hook

When the CE (or the debug spawner) creates a **new** entity, the engine calls `EEOnCECreate()` on it. This fires only for fresh CE spawns — not for entities loaded back from persistence and not for script-created objects. Vanilla uses it, for example, to randomize the food stage of spawned fruit and to set up helicopter crash sites.

**Example — a custom supply cache that starts with a random amount of starter loot when the CE spawns it.** The class goes in `4_World`:

```c
class LNT_SupplyCache : Barrel_ColorBase
{
    override void EEOnCECreate()
    {
        super.EEOnCECreate();

        // Runs on the server, only when the CE spawned this instance fresh
        int rolls = Math.RandomIntInclusive(1, 3);
        for (int i = 0; i < rolls; i++)
        {
            GetInventory().CreateInInventory("Rag");
        }
    }
}
```

Registration in `config.cpp` (the cache reuses the vanilla barrel model by inheriting from `Barrel_ColorBase`):

```cpp
class CfgPatches
{
    class Lantern_Core_Scripts
    {
        units[] = {"LNT_SupplyCache"};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = {"DZ_Data", "DZ_Gear_Camping"};
    };
};

class CfgVehicles
{
    class Barrel_ColorBase;
    class LNT_SupplyCache : Barrel_ColorBase
    {
        scope = 2;
        displayName = "Supply Cache";
    };
};
```

For the crate to actually spawn, it also needs a `types.xml` entry on the server — see [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md).

---

## Developer and Diagnostic Tools

Most of the remaining `CEApi` surface is developer/diagnostic tooling. These methods are marked **DEVELOPER/DIAG ONLY** in the engine headers — they are meant for the diagnostic executable and offline testing, not for live gameplay logic:

### Force-Spawning Through the CE

| Method | Purpose |
|--------|---------|
| `SpawnDE(string name, vector pos, float angle = -1)` | Force-spawn a dynamic event (`"StaticHeliCrash"`, vehicle events, ...); bypasses limits and avoidance |
| `SpawnDEEx(string name, vector pos, float angle, int flags)` | Same, with custom ECE flags |
| `SpawnLoot(string type, vector pos, float angle, int count = 1, float range = 1)` | Spawn one or more loot items in a circle |
| `SpawnEntity(string type, vector pos, float range, int count)` | Like `SpawnLoot`, works better for animals/infected/vehicles |
| `SpawnSingleEntity(string type, vector pos)` | Spawn one entity and get the `Object` back |
| `SpawnGroup(string groupName, vector pos, float angle = -1)` | Force-spawn a building prototype group with its loot |
| `SpawnAnalyze(string type)` | Emulate spawning of a type and dump images/logs to `storage/lmap`; `"*"` produces a CSV for all types |

```c
CEApi ce = GetCEApi();
if (ce)
{
    ce.SpawnDE("StaticHeliCrash", "4500 0 10200");
}
```

### Economy Logging and Maps

| Method | Purpose |
|--------|---------|
| `EconomyLog(string category)` | Dump a CSV to `storage/log/` — categories in `EconomyLogCategories` (e.g. `Economy`, `RespawnQueue`, `InfectedZone`) |
| `EconomyMap(string what)` | Render spawn locations to a `.tga` in `storage/lmap/` — a class name, or `EconomyMapStrings` helpers like `ALL_LOOT` or `EconomyMapStrings.Category("food")` |
| `EconomyOutput(string what, float range)` | Write diagnostics to the server log — strings in `EconomyOutputStrings` (`STATUS`, `SUSPICIOUS`, `EMPTY`, `CLOSE`, ...) |

### Loot-Point Exports

Used when building or fixing map loot data:

| Method | Output |
|--------|--------|
| `ExportSpawnData()` | Regenerates `storage/spawnpoints.bin` |
| `ExportProxyData(vector center = vector.Zero, float radius = 0)` | `storage/export/mapgrouppos.xml` (zero vector/radius = whole map) |
| `ExportClusterData()` | `storage/export/mapgroupcluster.xml` |
| `ExportProxyProto()` | `storage/export/mapgroupproto.xml` |
| `MarkCloseProxy(float radius, bool allSelections)` | Invalidate loot points closer than `radius` |
| `RemoveCloseProxy()` | Delete the invalidated points |
| `ListCloseProxy(float radius)` | Log loot points closer than `radius` without touching them |

---

## Summary

| API | Where | Purpose |
|-----|-------|---------|
| `CreateHive()` / `GetHive()` | `3_game/hive/hive.c` | Initialize/access the persistence backend that owns the CE |
| `GetCEApi()` | `3_game/ce/centraleconomy.c` | Access the `CEApi`; returns `null` without a Hive (e.g. on clients) |
| ECE flags | `3_game/ce/centraleconomy.c` | Control placement, persistence, and CE equipment when spawning via `CreateObjectEx()` |
| RF flags | `3_game/ce/centraleconomy.c` | Placement rotation control for `CreateObjectEx()` |
| `EntityAI.GetEconomyProfile()` | `3_game/entities/entityai.c` | Read the parsed `types.xml` entry (`CEItemProfile`) of an entity |
| `SetLifetime()` / `IncreaseLifetimeUp()` | `EntityAI` | Per-entity CE cleanup timer control |
| `RadiusLifetime*()` / `TimeShift()` | `CEApi` | Bulk lifetime manipulation |
| `GetCEGlobalInt/Float/String()` | `CEApi` | Read `globals.xml` variables (including custom ones) from script |
| `AvoidPlayer()` / `AvoidVehicle()` | `CEApi` | CE-style spawn avoidance checks for custom spawners |
| `EEOnCECreate()` | `EntityAI` | Per-entity hook fired when the CE creates the entity fresh |

- The CE runs **only on the server**; always null-check `GetCEApi()`.
- The XML configuration itself is documented in [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md) and [Vehicle & Dynamic Event Spawning](../09-server-admin/05-vehicle-spawning.md).
- Diag-marked `CEApi` methods are tooling, not gameplay API — keep them out of production code paths.
