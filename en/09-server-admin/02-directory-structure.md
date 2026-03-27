# Chapter 9.2: Directory Structure & Mission Folder

[Home](../README.md) | [<< Previous: Server Setup](01-server-setup.md) | **Directory Structure** | [Next: serverDZ.cfg Reference >>](03-server-cfg.md)

---

> **Summary:** A complete walkthrough of every file and folder in the DayZ server directory and the mission folder. Knowing what each file does -- and which ones are safe to edit -- is essential before touching the loot economy or adding mods.

---

## Table of Contents

- [Top-Level Server Directory](#top-level-server-directory)
- [The addons/ Folder](#the-addons-folder)
- [The keys/ Folder](#the-keys-folder)
- [The profiles/ Folder](#the-profiles-folder)
- [The mpmissions/ Folder](#the-mpmissions-folder)
- [Mission Folder Structure](#mission-folder-structure)
- [The db/ Folder -- Economy Core](#the-db-folder----economy-core)
- [The env/ Folder -- Animal Territories](#the-env-folder----animal-territories)
- [The storage_1/ Folder -- Persistence](#the-storage_1-folder----persistence)
- [Top-Level Mission Files](#top-level-mission-files)
- [Which Files to Edit vs Leave Alone](#which-files-to-edit-vs-leave-alone)

---

## Top-Level Server Directory

```
DayZServer/
  DayZServer_x64.exe          # Server executable
  serverDZ.cfg                 # Main server config (name, password, mods, time)
  dayzsetting.xml              # Rendering settings (irrelevant for dedicated servers)
  ban.txt                      # Banned Steam64 IDs, one per line
  whitelist.txt                # Whitelisted Steam64 IDs, one per line
  steam_appid.txt              # Contains "221100" -- do not edit
  dayz.gproj                   # Workbench project file -- do not edit
  addons/                      # Vanilla game PBOs
  battleye/                    # Anti-cheat files
  config/                      # Steam config (config.vdf)
  dta/                         # Core engine PBOs (scripts, GUI, graphics)
  keys/                        # Signature verification keys (.bikey files)
  logs/                        # Engine-level logs
  mpmissions/                  # All mission folders
  profiles/                    # Runtime output (script logs, player DB, crash dumps)
  server_manager/              # Server management utilities
```

---

## The addons/ Folder

Contains all vanilla game content packed as PBO files. Each PBO has a matching `.bisign` signature file:

```
addons/
  ai.pbo                       # AI behavior scripts
  ai.pbo.dayz.bisign           # Signature for ai.pbo
  animals.pbo                  # Animal definitions
  characters_backpacks.pbo     # Backpack models/configs
  characters_belts.pbo         # Belt item models
  weapons_firearms.pbo         # Weapon models/configs
  ... (100+ PBO files)
```

**Never edit these files.** They are overwritten every time you update the server via SteamCMD. Mods override vanilla behavior through the `modded` class system, not by changing PBOs.

---

## The keys/ Folder

Contains `.bikey` public key files used to verify mod signatures:

```
keys/
  dayz.bikey                   # Vanilla signature key (always present)
```

When you add a mod, copy its `.bikey` file into this folder. The server uses `verifySignatures = 2` in `serverDZ.cfg` to reject any PBO that does not have a matching `.bikey` in this folder.

If a player loads a mod whose key is not in your `keys/` folder, they get a **"Signature check failed"** kick.

---

## The profiles/ Folder

Created on first server launch. Contains runtime output:

```
profiles/
  BattlEye/                              # BE logs and bans
  DataCache/                             # Cached data
  Users/                                 # Per-player preference files
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Admin log
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Engine report (crash info, warnings)
  script_2026-03-08_11-34-35.log           # Script log (your primary debug tool)
```

The **script log** is the most important file here. Every `Print()` call, every script error, and every mod loading message goes here. When something breaks, this is where you look first.

Log files accumulate over time. Old logs are not automatically deleted.

---

## The mpmissions/ Folder

Contains one subfolder per map:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (free)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

The folder name format is `<missionName>.<terrainName>`. The `template` value in `serverDZ.cfg` must match one of these folder names exactly.

---

## Mission Folder Structure

The Chernarus mission folder (`mpmissions/dayzOffline.chernarusplus/`) contains:

```
dayzOffline.chernarusplus/
  init.c                         # Mission entry point script
  db/                            # Core economy files
  env/                           # Animal territory definitions
  storage_1/                     # Persistence data (players, world state)
  cfgeconomycore.xml             # Economy root classes and logging settings
  cfgenvironment.xml             # Links to animal territory files
  cfgeventgroups.xml             # Event group definitions
  cfgeventspawns.xml             # Exact spawn positions for events (vehicles, etc.)
  cfgeffectarea.json             # Contaminated zone definitions
  cfggameplay.json               # Gameplay tuning (stamina, damage, building)
  cfgignorelist.xml              # Items excluded from the economy entirely
  cfglimitsdefinition.xml        # Valid category/usage/value tag definitions
  cfglimitsdefinitionuser.xml    # User-defined custom tag definitions
  cfgplayerspawnpoints.xml       # Fresh spawn locations
  cfgrandompresets.xml           # Reusable loot pool definitions
  cfgspawnabletypes.xml          # Pre-attached items and cargo on spawned entities
  cfgundergroundtriggers.json    # Underground area triggers
  cfgweather.xml                 # Weather configuration
  areaflags.map                  # Area flag data (binary)
  mapclusterproto.xml            # Map cluster prototype definitions
  mapgroupcluster.xml            # Building group cluster definitions
  mapgroupcluster01.xml          # Cluster data (part 1)
  mapgroupcluster02.xml          # Cluster data (part 2)
  mapgroupcluster03.xml          # Cluster data (part 3)
  mapgroupcluster04.xml          # Cluster data (part 4)
  mapgroupdirt.xml               # Dirt/ground loot positions
  mapgrouppos.xml                # Map group positions
  mapgroupproto.xml              # Prototype definitions for map groups
```

---

## The db/ Folder -- Economy Core

This is the heart of the Central Economy. Five files control what spawns, where, and how much:

```
db/
  types.xml        # THE key file: defines every item's spawn rules
  globals.xml      # Global economy parameters (timers, limits, counts)
  events.xml       # Dynamic events (animals, vehicles, helicopters)
  economy.xml      # Toggles for economy subsystems (loot, animals, vehicles)
  messages.xml     # Scheduled server messages to players
```

### types.xml

Defines spawn rules for **every item** in the game. At approximately 23,000 lines, this is by far the largest economy file. Each entry specifies how many copies of an item should exist on the map, where it can spawn, and how long it persists. See [Chapter 9.4](04-loot-economy.md) for a deep dive.

### globals.xml

Global parameters that affect the entire economy: zombie counts, animal counts, cleanup timers, loot damage ranges, respawn timing. There are 33 parameters total. See [Chapter 9.4](04-loot-economy.md) for the full reference.

### events.xml

Defines dynamic spawn events for animals and vehicles. Each event specifies a nominal count, spawn constraints, and child variants. For example, the `VehicleCivilianSedan` event spawns 8 sedans across the map in 3 color variants.

### economy.xml

Master toggles for economy subsystems:

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

| Flag | Meaning |
|------|---------|
| `init` | Spawn items on first server start |
| `load` | Load saved state from persistence |
| `respawn` | Allow respawning of items after cleanup |
| `save` | Save state to persistence files |

### messages.xml

Scheduled messages broadcast to all players. Supports countdown timers, repeat intervals, on-connect messages, and shutdown warnings:

```xml
<messages>
    <message>
        <deadline>600</deadline>
        <shutdown>1</shutdown>
        <text>#name will shutdown in #tmin minutes.</text>
    </message>
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>Welcome to #name</text>
    </message>
</messages>
```

Use `#name` for server name and `#tmin` for time remaining in minutes.

---

## The env/ Folder -- Animal Territories

Contains XML files that define where each animal species can spawn:

```
env/
  bear_territories.xml
  cattle_territories.xml
  domestic_animals_territories.xml
  fox_territories.xml
  hare_territories.xml
  hen_territories.xml
  pig_territories.xml
  red_deer_territories.xml
  roe_deer_territories.xml
  sheep_goat_territories.xml
  wild_boar_territories.xml
  wolf_territories.xml
  zombie_territories.xml
```

These files contain hundreds of coordinate points defining territory zones across the map. They are referenced by `cfgenvironment.xml`. You rarely need to edit these unless you want to change where animals or zombies spawn geographically.

---

## The storage_1/ Folder -- Persistence

Holds the server's persistent state between restarts:

```
storage_1/
  players.db         # SQLite database of all player characters
  spawnpoints.bin    # Binary spawn point data
  backup/            # Automatic backups of persistence data
  data/              # World state (placed items, base building, vehicles)
```

**Never edit `players.db` while the server is running.** It is an SQLite database locked by the server process. If you need to wipe characters, stop the server first and delete or rename the file.

To do a **full persistence wipe**, stop the server and delete the entire `storage_1/` folder. The server will recreate it on next launch with a fresh world.

To do a **partial wipe** (keep characters, reset loot):
1. Stop the server
2. Delete files in `storage_1/data/` but keep `players.db`
3. Restart

---

## Top-Level Mission Files

### cfgeconomycore.xml

Registers root classes for the economy and configures CE logging:

```xml
<economycore>
    <classes>
        <rootclass name="DefaultWeapon" />
        <rootclass name="DefaultMagazine" />
        <rootclass name="Inventory_Base" />
        <rootclass name="HouseNoDestruct" reportMemoryLOD="no" />
        <rootclass name="SurvivorBase" act="character" reportMemoryLOD="no" />
        <rootclass name="DZ_LightAI" act="character" reportMemoryLOD="no" />
        <rootclass name="CarScript" act="car" reportMemoryLOD="no" />
        <rootclass name="BoatScript" act="car" reportMemoryLOD="no" />
    </classes>
    <defaults>
        <default name="log_ce_loop" value="false"/>
        <default name="log_ce_dynamicevent" value="false"/>
        <default name="log_ce_vehicle" value="false"/>
        <default name="log_ce_lootspawn" value="false"/>
        <default name="log_ce_lootcleanup" value="false"/>
        <default name="log_ce_lootrespawn" value="false"/>
        <default name="log_ce_statistics" value="false"/>
        <default name="log_ce_zombie" value="false"/>
        <default name="log_storageinfo" value="false"/>
        <default name="log_hivewarning" value="true"/>
        <default name="log_missionfilewarning" value="true"/>
        <default name="save_events_startup" value="true"/>
        <default name="save_types_startup" value="true"/>
    </defaults>
</economycore>
```

Set `log_ce_lootspawn` to `"true"` when debugging item spawn issues. It produces detailed output in the RPT log showing which items the CE is trying to spawn and why they succeed or fail.

### cfglimitsdefinition.xml

Defines the valid values for `<category>`, `<usage>`, `<value>`, and `<tag>` elements used in `types.xml`:

```xml
<lists>
    <categories>
        <category name="tools"/>
        <category name="containers"/>
        <category name="clothes"/>
        <category name="food"/>
        <category name="weapons"/>
        <category name="books"/>
        <category name="explosives"/>
        <category name="lootdispatch"/>
    </categories>
    <tags>
        <tag name="floor"/>
        <tag name="shelves"/>
        <tag name="ground"/>
    </tags>
    <usageflags>
        <usage name="Military"/>
        <usage name="Police"/>
        <usage name="Medic"/>
        <usage name="Firefighter"/>
        <usage name="Industrial"/>
        <usage name="Farm"/>
        <usage name="Coast"/>
        <usage name="Town"/>
        <usage name="Village"/>
        <usage name="Hunting"/>
        <usage name="Office"/>
        <usage name="School"/>
        <usage name="Prison"/>
        <usage name="Lunapark"/>
        <usage name="SeasonalEvent"/>
        <usage name="ContaminatedArea"/>
        <usage name="Historical"/>
    </usageflags>
    <valueflags>
        <value name="Tier1"/>
        <value name="Tier2"/>
        <value name="Tier3"/>
        <value name="Tier4"/>
        <value name="Unique"/>
    </valueflags>
</lists>
```

If you use a `<usage>` or `<value>` tag in `types.xml` that is not defined here, the item will silently fail to spawn.

### cfgignorelist.xml

Items listed here are completely excluded from the economy, even if they have entries in `types.xml`:

```xml
<ignore>
    <type name="Bandage"></type>
    <type name="CattleProd"></type>
    <type name="Defibrillator"></type>
    <type name="HescoBox"></type>
    <type name="StunBaton"></type>
    <type name="TransitBus"></type>
    <type name="Spear"></type>
    <type name="Mag_STANAGCoupled_30Rnd"></type>
    <type name="Wreck_Mi8"></type>
</ignore>
```

This is used for items that exist in the game code but are not intended to spawn naturally (unfinished items, deprecated content, seasonal items out of season).

### cfggameplay.json

A JSON file that overrides gameplay parameters. Controls stamina, movement, base damage, weather, temperature, weapon obstruction, drowning, and more. This file is optional -- if absent, the server uses default values.

### cfgplayerspawnpoints.xml

Defines where freshly spawned players appear on the map, with distance constraints from infected, other players, and buildings.

### cfgeventspawns.xml

Contains exact world coordinates where events (vehicles, helicrashes, etc.) can spawn. Each event name from `events.xml` has a list of valid positions:

```xml
<eventposdef>
    <event name="VehicleCivilianSedan">
        <pos x="12071.933594" z="9129.989258" a="317.953339" />
        <pos x="12302.375001" z="9051.289062" a="60.399284" />
        <pos x="10182.458985" z="1987.5271" a="29.172445" />
        ...
    </event>
</eventposdef>
```

The `a` attribute is the rotation angle in degrees.

---

## Which Files to Edit vs Leave Alone

| File / Folder | Safe to Edit? | Notes |
|---------------|:---:|-------|
| `serverDZ.cfg` | Yes | Main server config |
| `db/types.xml` | Yes | Item spawn rules -- your most common edit |
| `db/globals.xml` | Yes | Economy tuning parameters |
| `db/events.xml` | Yes | Vehicle/animal spawn events |
| `db/economy.xml` | Yes | Economy subsystem toggles |
| `db/messages.xml` | Yes | Server broadcast messages |
| `cfggameplay.json` | Yes | Gameplay tuning |
| `cfgspawnabletypes.xml` | Yes | Attachment/cargo presets |
| `cfgrandompresets.xml` | Yes | Loot pool definitions |
| `cfglimitsdefinition.xml` | Yes | Add custom usage/value tags |
| `cfgplayerspawnpoints.xml` | Yes | Player spawn locations |
| `cfgeventspawns.xml` | Yes | Event spawn coordinates |
| `cfgignorelist.xml` | Yes | Exclude items from economy |
| `cfgweather.xml` | Yes | Weather patterns |
| `cfgeffectarea.json` | Yes | Contaminated zones |
| `init.c` | Yes | Mission entry script |
| `addons/` | **No** | Overwritten on update |
| `dta/` | **No** | Core engine data |
| `keys/` | Add only | Copy mod `.bikey` files here |
| `storage_1/` | Delete only | Persistence -- do not hand-edit |
| `battleye/` | **No** | Anti-cheat -- do not touch |
| `mapgroup*.xml` | Careful | Building loot positions -- advanced editing only |

---

**Previous:** [Server Setup](01-server-setup.md) | [Home](../README.md) | **Next:** [serverDZ.cfg Reference >>](03-server-cfg.md)
