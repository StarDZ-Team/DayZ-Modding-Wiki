# Server Configuration Files

---

> **Summary:** DayZ servers are configured through XML, JSON, and script files in the mission folder (e.g., `mpmissions/dayzOffline.chernarusplus/`). This chapter is the modder-facing map of that file set: what each file does, how your mod hooks into it, and where the full tuning reference for each file lives. It also owns the canonical workflow for registering modded loot through `cfgeconomycore.xml`.

---

## Table of Contents

- [Overview: The Ownership Map](#overview-the-ownership-map)
- [init.c --- Mission Entry Point](#initc--mission-entry-point)
- [The Central Economy File Set](#the-central-economy-file-set)
- [cfgeconomycore.xml --- Registering Modded Loot](#cfgeconomycorexml--registering-modded-loot)
- [cfggameplay.json --- Gameplay Tuning](#cfggameplayjson--gameplay-tuning)
- [cfgplayerspawnpoints.xml --- Player Spawn Points](#cfgplayerspawnpointsxml--player-spawn-points)
- [serverDZ.cfg --- Server Settings and Mod Loading](#serverdzcfg--server-settings-and-mod-loading)
- [Common Mistakes](#common-mistakes)
- [Theory vs Practice](#theory-vs-practice)

---

## Overview: The Ownership Map

Every DayZ server loads its configuration from a **mission folder**. The Central Economy (CE) files define what items spawn, where, and for how long. The server executable itself is configured through `serverDZ.cfg`, which lives alongside the executable.

As a modder you rarely edit these files on a live server yourself --- the server admin does. Your job is to **ship correct, drop-in files** with your mod and to understand which file your feature touches. Each file below gets a short summary and a link to the chapter that owns its full reference:

| File | Location | What it is | Full reference |
|------|----------|------------|----------------|
| `init.c` | mission root | Mission entry point: Hive init, date, spawn loadout | this chapter |
| `db/types.xml` | mission `db/` | Item spawn definitions: quantities, lifetimes, locations | [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md) |
| `db/globals.xml` | mission `db/` | Global CE parameters: max counts, cleanup timers | [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md) |
| `db/economy.xml` | mission `db/` | CE subsystem toggles (dynamic, animals, zombies, vehicles) | this chapter |
| `db/events.xml` | mission `db/` | Dynamic events: heli crashes, convoys, animal herds | [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md) |
| `cfgspawnabletypes.xml` | mission root | Pre-attached items and cargo on spawned entities | [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md) |
| `cfgrandompresets.xml` | mission root | Reusable item pools for cfgspawnabletypes | [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md) |
| `cfgeconomycore.xml` | mission root | Root class registration + custom CE file registration | **this chapter (canonical)** |
| `cfglimitsdefinition.xml` | mission root | Valid `category`, `usage`, and `value` tag definitions | this chapter |
| `cfgplayerspawnpoints.xml` | mission root | Fresh-spawn and hop-spawn positions | [Player Spawning](../09-server-admin/06-player-spawning.md) |
| `cfggameplay.json` | mission root | Gameplay tuning: stamina, base building, UI, object spawner | [World Systems](../06-engine-api/23-world-systems.md) |
| `serverDZ.cfg` | next to executable | Server name, password, max players, mission selection | [serverDZ.cfg Complete Reference](../09-server-admin/03-server-cfg.md) |

For the **script-side** CE API (spawn flags, lifetime control, `EEOnCECreate`), see [Central Economy Script API](../06-engine-api/10-central-economy.md).

---

## init.c --- Mission Entry Point

The `init.c` script is the first thing the server executes. It initializes the Central Economy and creates the mission instance.

```c
void main()
{
    Hive ce = CreateHive();
    if (ce)
    {
        ce.InitOffline();
    }

    GetGame().GetWorld().SetDate(2024, 9, 15, 12, 0);
}

class CustomMission: MissionServer
{
    override PlayerBase CreateCharacter(PlayerIdentity identity, vector pos, ParamsReadContext ctx, string characterName)
    {
        Entity playerEnt;
        playerEnt = GetGame().CreatePlayer(identity, characterName, pos, 0, "NONE");
        Class.CastTo(m_player, playerEnt);
        GetGame().SelectPlayer(identity, m_player);
        return m_player;
    }

    override void StartingEquipSetup(PlayerBase player, bool clothesChosen)
    {
        EntityAI itemClothing = player.FindAttachmentBySlotName("Body");
        if (itemClothing)
        {
            itemClothing.GetInventory().CreateInInventory("BandageDressing");
        }
    }
}

Mission CreateCustomMission(string path)
{
    return new CustomMission();
}
```

The `Hive` manages the CE database. Without `CreateHive()`, no items spawn and persistence is disabled. `CreateCharacter` creates the player entity at spawn, and `StartingEquipSetup` defines the items a fresh character receives. Other useful `MissionServer` overrides include `OnInit()`, `OnUpdate()`, `InvokeOnConnect()`, and `InvokeOnDisconnect()`.

Note the division of labour: `main()` only sets up the Hive and the world date. It does **not** instantiate the mission. The engine calls the free function `CreateCustomMission(string path)` itself and uses the `Mission` you return from it --- calling it yourself from `main()` would build a second instance that nothing uses. Bohemia's own reference missions follow exactly this shape (`dayzOffline.chernarusplus/init.c` in the official [DayZ-Central-Economy](https://github.com/BohemiaInteractive/DayZ-Central-Economy) repository: `main()` ends after the date logic, and `CreateCustomMission` is defined at the bottom of the file).

The `path` parameter the engine passes in is the mission folder name; the vanilla reference missions ignore it and always return the same class.

### What NOT to Do in init.c

`init.c` belongs to the **server admin**, not to your mod. Treat it as read-only territory:

- **Do not ship mod logic in init.c.** A mission's `init.c` is replaced whenever the admin switches missions or maps, and two mods that both demand `init.c` edits force the admin to hand-merge them. Put your logic in a `modded class MissionServer` inside your mod's `5_Mission` scripts instead --- it applies automatically no matter which mission the admin runs, because `CustomMission` extends `MissionServer` and inherits every modded layer. See [Mission Hooks](../06-engine-api/11-mission-hooks.md).
- **Do not remove or reorder `CreateHive()` / `InitOffline()`.** Without the Hive there is no economy and no persistence, and the failure is silent apart from an empty map.
- **Do not mass-spawn static objects in init.c loops.** Hundreds of `GetGame().CreateObjectEx()` calls at mission start delay server startup and are invisible to admin tooling. Prefer the JSON object spawner driven from `cfggameplay.json`, which admins can edit without touching script.
- **Do not assume init.c runs once.** It runs on every server start and restart. Anything you spawn unconditionally will duplicate across restarts unless it is persistence-managed.

If your mod genuinely needs starting-gear changes, document a `StartingEquipSetup` snippet in your mod's README for admins to merge --- do not ask them to replace the whole file.

---

## The Central Economy File Set

These files drive the loot economy. The summaries below cover what each file is and how a mod hooks in; the field-by-field tuning reference (nominal/restock mechanics, flags, spawn-cycle internals) is owned by [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md).

### types.xml --- Item Spawn Definitions

Located at `db/types.xml`. Every item that can spawn through the CE needs an entry: target count (`nominal`), persistence time (`lifetime`), fill quantities, and the `category` / `usage` / `value` tags that control **where** it spawns.

```xml
<type name="AK74">
    <nominal>6</nominal>
    <lifetime>28800</lifetime>
    <restock>0</restock>
    <min>4</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1"
           count_in_player="0" crafted="0" deloot="0"/>
    <category name="weapons"/>
    <usage name="Military"/>
    <value name="Tier3"/>
    <value name="Tier4"/>
</type>
```

**Mod hook:** your mod's items get their own `types.xml` entries, shipped in a separate file and registered through `cfgeconomycore.xml` (see the [canonical workflow below](#cfgeconomycorexml--registering-modded-loot)) --- never by pasting into the vanilla `db/types.xml`.

### cfgspawnabletypes.xml --- Attachments and Cargo

Controls what spawns **already attached to or inside** other items: spawn damage ranges, attachment groups with chances, and cargo presets. Storage containers are marked `<hoarder />` here so the CE knows they hold player items.

**Mod hook:** if your item should spawn with attachments (a weapon with a magazine, a vest with pouches), ship a spawnabletypes file and register it the same way as your types file.

### cfgrandompresets.xml --- Reusable Loot Pools

Defines named `cargo` and `attachments` pools referenced by `cfgspawnabletypes.xml`, so several containers can share one loot table.

**Mod hook:** since game version 1.28 preset files can also be registered through `cfgeconomycore.xml`; before that, adding presets meant overwriting the vanilla file. See [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md) for the details.

### globals.xml --- Economy Parameters

Located at `db/globals.xml`. Server-wide CE knobs: `ZombieMaxCount`, cleanup lifetimes, login/logout timers, initial spawn percentage. The `type` attribute is `0` for integer, `1` for float --- using the wrong one truncates the value.

**Mod hook:** mods rarely ship globals changes; document recommended values in your README instead of shipping a replacement file, because there is only one `globals.xml` per server and last-write-wins.

### economy.xml --- Subsystem Control

Located at `db/economy.xml`. Toggles which CE subsystems are active:

```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```

This is the complete vanilla `db/economy.xml` element set (`DZ/worlds/chernarusplus/ce/db/economy.xml`); `dynamic`/`animals`/`zombies`/`vehicles` are the ones mods most commonly touch, but `randoms`, `custom`, `building`, and `player` (base-building and player-inventory persistence) are also toggled here. Flags: `init` (spawn on startup), `load` (load persistence), `respawn` (respawn after cleanup), `save` (persist to database). Total-conversion servers disable subsystems here rather than zeroing out hundreds of types entries.

---

## cfgeconomycore.xml --- Registering Modded Loot

`cfgeconomycore.xml` sits in the mission root and does two jobs that matter to every content mod: it registers **root classes** so the CE recognizes item hierarchies, and it registers **additional CE files** so mods never have to edit the vanilla `db/` files. This section is the canonical workflow; ship it with every item mod.

### Root Class Registration

Every spawnable class hierarchy must trace back to a registered root class:

```xml
<economycore>
    <classes>
        <rootclass name="DefaultWeapon" />
        <rootclass name="DefaultMagazine" />
        <rootclass name="Inventory_Base" />
        <rootclass name="SurvivorBase" act="character" reportMemoryLOD="no" />
        <rootclass name="DZ_LightAI" act="character" reportMemoryLOD="no" />
        <rootclass name="CarScript" act="car" reportMemoryLOD="no" />
    </classes>
</economycore>
```

If your mod's items inherit from `Inventory_Base`, `DefaultWeapon`, or `DefaultMagazine` (the normal case), nothing to do. If you introduce a genuinely new base class outside those hierarchies, add it as a `rootclass`. The `act` attribute marks special entity types: `character` for AI, `car` for vehicles.

### The `<ce>` Directive --- Custom Economy Files

The `<ce folder="...">` directive registers extra CE files from a subfolder of the mission. This is how modded loot enters the economy without touching any vanilla file. Suppose the fictional **NightPatrol** weapon pack adds a carbine; the admin's mission gains one folder and three lines:

```
mpmissions/dayzOffline.chernarusplus/
├── cfgeconomycore.xml          <- add a <ce> block here
├── db/
│   └── types.xml               <- untouched
└── nightpatrol_ce/
    ├── np_types.xml
    └── np_spawnabletypes.xml
```

Inside `cfgeconomycore.xml`, after the `<classes>` block:

```xml
<economycore>
    <classes>
        <!-- vanilla rootclass entries stay as they are -->
    </classes>

    <ce folder="nightpatrol_ce">
        <file name="np_types.xml" type="types" />
        <file name="np_spawnabletypes.xml" type="spawnabletypes" />
    </ce>
</economycore>
```

The registered file uses the same schema as its vanilla counterpart. `nightpatrol_ce/np_types.xml`:

```xml
<types>
    <type name="NP_Carbine">
        <nominal>4</nominal>
        <lifetime>28800</lifetime>
        <restock>0</restock>
        <min>2</min>
        <quantmin>-1</quantmin>
        <quantmax>-1</quantmax>
        <cost>100</cost>
        <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1"
               count_in_player="0" crafted="0" deloot="0"/>
        <category name="weapons"/>
        <usage name="Military"/>
        <value name="Tier3"/>
    </type>
</types>
```

Rules of the merge:

- The `type` attribute on `<file>` declares the schema: `types`, `spawnabletypes`, `globals`, `economy`, `events`, or `messages` (plus `randompresets` since 1.28).
- Registered files **merge** with the vanilla ones. An entry whose `name` matches an existing entry **replaces** it --- which means a mod can also retune vanilla items (say, raise `nominal` on a vanilla scope its weapon uses) from its own file.
- Multiple mods each register their own folder; they coexist as long as classnames are unique. If two files define the same classname, the last-loaded entry wins.
- Simply dropping extra XML files into `db/` does **nothing**. Only files registered via `<ce>` are read.

### The Full Modded-Loot Workflow

1. **Ship the files with the mod.** Put ready-to-use `<modname>_types.xml` / `<modname>_spawnabletypes.xml` (and an install note) in a `ServerFiles/` folder inside your released mod, so admins copy-paste instead of writing entries from scratch.
2. **Admin drops the folder** into the mission root and adds the `<ce>` block to `cfgeconomycore.xml`.
3. **Register custom tags, if any.** A `category`, `usage`, or `value` name that vanilla does not define must be declared --- see below.
4. **Register new root classes, if any** (rare; only for hierarchies outside the vanilla roots).
5. **Verify.** Start the server and check the RPT/CE logs: schema errors and unknown-tag warnings are reported there, and a rejected file means the item silently never spawns.

### Registering New category/usage/value Names

Any `category`, `usage`, or `value` used in a types file must exist in `cfglimitsdefinition.xml`. A genuinely new tag name (one that does not already exist anywhere in vanilla) has to be added to `cfglimitsdefinition.xml` itself. `cfglimitsdefinitionuser.xml` serves a different, narrower purpose and does not accept new tag definitions:

- `cfglimitsdefinition.xml` (root `<lists>`) is where every individual `category`, `tag`, `usage`, and `value` name is declared. This is the file a genuinely new tag must be added to; there is no separate "custom tags" file for brand-new names, so plan for a merge step on game updates.
- `cfglimitsdefinitionuser.xml` (root `<user_lists>`, **not** `<lists>`) only defines named **combinations of already-existing** `usage`/`value` flags, referenced later as a single shorthand tag. It cannot introduce a name that isn't already in `cfglimitsdefinition.xml`. The vanilla file ships combos like this:

```xml
<user_lists>
    <usageflags>
        <user name="TownVillage">
            <usage name="Town" />
            <usage name="Village" />
        </user>
    </usageflags>
    <valueflags>
        <user name="Tier12">
            <value name="Tier1" />
            <value name="Tier2" />
        </user>
    </valueflags>
</user_lists>
```

To add a wholly new tag such as `np_special`, append it to `cfglimitsdefinition.xml` directly:

```xml
<lists>
    <categories>
        <category name="np_special"/>
    </categories>
    <usageflags>
        <usage name="NightPatrolDungeon"/>
    </usageflags>
    <valueflags>
        <value name="NightPatrolEndgame"/>
    </valueflags>
</lists>
```

### Script-Side Economy Interaction

Items created via `CreateInInventory()` are automatically CE-managed. For world spawns from script, use ECE flags:

```c
EntityAI item = EntityAI.Cast(GetGame().CreateObjectEx("AK74", position, ECE_PLACE_ON_SURFACE));
```

`CreateObjectEx()` returns the base `Object` type (`proto native Object CreateObjectEx(string type, vector pos, int iFlags, int iRotation = RF_DEFAULT);` in `scripts/3_game/global/game.c`), so an explicit `EntityAI.Cast(...)` is required to use it as an `EntityAI`. Most vanilla call sites do exactly this (roughly 80 of the ~110 `CreateObjectEx()` calls in the script dump wrap the result in a `Cast`); the rest keep the plain `Object` return or discard it.

The full script surface --- spawn flags, lifetime control from script, `EEOnCECreate` --- is documented in [Central Economy Script API](../06-engine-api/10-central-economy.md).

---

## cfggameplay.json --- Gameplay Tuning

A JSON file in the mission root that the engine loads automatically if present. It tunes gameplay systems without any scripting: stamina and movement, base-building placement checks, world temperatures and lighting, map UI behavior, and the JSON object spawner (`ObjectSpawnersArr`) that spawns static objects from files admins can edit.

**Mod hook:** two things matter to modders. First, several hard checks your mod might fight against (hologram placement, base damage) are toggled here, not in script --- check `cfggameplay.json` before writing a workaround. Second, many values your users will ask you to make configurable are already admin-configurable here; point them at the file instead of duplicating the setting. Note that a JSON syntax error causes the whole file to be **silently ignored**, so admins should validate it after every edit.

Full structure and field reference: [World Systems](../06-engine-api/23-world-systems.md).

---

## cfgplayerspawnpoints.xml --- Player Spawn Points

Defines where fresh spawns and server-hoppers appear: spawn point lists, generator parameters (spacing, group radius), and fresh-spawn/hop-spawn sections. Lives in the mission root.

**Mod hook:** mods that add playable areas or custom maps ship recommended spawn point sets for admins to merge. Spawn *gear* is not defined here --- that is `StartingEquipSetup` in `init.c` or a modded `MissionServer`.

Full reference: [Player Spawning](../09-server-admin/06-player-spawning.md).

---

## serverDZ.cfg --- Server Settings and Mod Loading

This file sits next to the server executable, not in the mission folder. It controls server identity (`hostname`, `password`, `maxPlayers`), security (`verifySignatures`, `forceSameBuild`), and which mission loads:

```
hostname = "My DayZ Server";
maxPlayers = 60;
verifySignatures = 2;
forceSameBuild = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

**Mod hook:** mods are **not** listed in this file. They are loaded via launch parameters:

```
DayZServer_x64.exe -config=serverDZ.cfg -mod=@Lantern;@NightPatrol -servermod=@LanternAdminTools -port=2302
```

`-mod=` mods must also be installed by clients; `-servermod=` mods run server-side only. Your mod's documentation should state clearly which of the two it requires. With `verifySignatures = 2` the server rejects clients whose PBOs fail signature checks, so released mods must ship valid `.bisign` files and a public key.

Complete parameter reference: [serverDZ.cfg Complete Reference](../09-server-admin/03-server-cfg.md).

---

## Common Mistakes

### XML Syntax Errors

A single unclosed tag breaks the entire file. Always validate XML before deploying.

### Missing Tags in cfglimitsdefinition.xml

Using a `usage` or `value` in a types file that is not defined in `cfglimitsdefinition.xml` (or the user file) causes the item to silently fail to spawn. Check RPT logs for warnings.

### Unregistered CE Files

Placing extra XML files in `db/` or the mission root does nothing. Every custom file must be registered in `cfgeconomycore.xml` via a `<ce>` block.

### Missing Root Class

Items whose class hierarchy does not trace to a registered root class in `cfgeconomycore.xml` will never spawn, even with correct types entries.

### Editing Vanilla Files Directly

Pasting mod entries into the vanilla `types.xml` works but breaks on game updates and collides with other mods. Ship separate files registered through `cfgeconomycore.xml`. Brand-new `category`/`usage`/`value` names still have to be merged into `cfglimitsdefinition.xml` itself (see [Registering New category/usage/value Names](#registering-new-category-usage-value-names)); `cfglimitsdefinitionuser.xml` only aliases combinations of names that already exist there.

### cfggameplay.json Not Loading

A JSON syntax error causes the file to be silently ignored --- the server runs with defaults and nothing in the log points at the file.

### Wrong type in globals.xml

Using `type="0"` (integer) for a float value like `0.82` truncates it to `0`. Use `type="1"` for floats.

### Nominal Inflation

Every mod adds items, and totals add up. Total `nominal` across all types files should stay below roughly 10,000--15,000; beyond that the CE tick cost shows up as server FPS drops. Ship conservative defaults --- admins can always raise them.

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| `nominal` is a hard target | CE spawns exactly this many items | CE approaches nominal over time but fluctuates based on player interaction, cleanup cycles, and zone distance |
| `restock=0` means instant respawn | Items reappear immediately after despawn | The CE processes restocking on its own internal loop rather than instantaneously per item, so expect some delay regardless of the restock value. Set `log_ce_loop="true"` in `cfgeconomycore.xml`'s `<defaults>` block if you need to observe your server's actual loop timing |
| `cfggameplay.json` controls all gameplay | All tuning goes here | Many gameplay values are hardcoded in script or config.cpp and cannot be overridden by cfggameplay.json |
| `init.c` runs only on server start | One-time initialization | `init.c` runs every time the mission loads, including after server restarts. Persistent state is managed by the Hive, not init.c |
| Multiple types.xml files merge cleanly | CE reads all registered files | Files must be registered in cfgeconomycore.xml via `<ce folder="...">` directives. Simply placing extra XML files in `db/` does nothing |
