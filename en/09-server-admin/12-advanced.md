# Chapter 9.12: Advanced Server Topics

[Home](../README.md) | [<< Previous: Troubleshooting](11-troubleshooting.md) | [Part 9 Home](01-server-setup.md)

---

> **Summary:** Deep configuration files, multi-map setups, economy splitting, animal territories, dynamic events, weather control, automated restarts, and the messages system.

---

## Table of Contents

- [cfggameplay.json Deep Dive](#cfggameplayjson-deep-dive)
- [Multi-Map Servers](#multi-map-servers)
- [Custom Economy Tuning](#custom-economy-tuning)
- [cfgenvironment.xml and Animal Territories](#cfgenvironmentxml-and-animal-territories)
- [Custom Dynamic Events](#custom-dynamic-events)
- [Server Restart Automation](#server-restart-automation)
- [cfgweather.xml](#cfgweatherxml)
- [Messages System](#messages-system)

---

## cfggameplay.json Deep Dive

The file **cfggameplay.json** lives in your mission folder and overrides hardcoded gameplay defaults. Enable it in **serverDZ.cfg** first:

```cpp
enableCfgGameplayFile = 1;
```

Vanilla structure:

```json
{
  "version": 123,
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false,
    "disableRespawnDialog": false,
    "disableRespawnInUnconsciousness": false
  },
  "PlayerData": {
    "disablePersonalLight": false,
    "StaminaData": {
      "sprintStaminaModifierErc": 1.0, "sprintStaminaModifierCro": 1.0,
      "staminaWeightLimitThreshold": 6000.0, "staminaMax": 100.0,
      "staminaKg": 0.3, "staminaMin": 0.0,
      "staminaDepletionSpeed": 1.0, "staminaRecoverySpeed": 1.0
    },
    "ShockHandlingData": {
      "shockRefillSpeedConscious": 5.0, "shockRefillSpeedUnconscious": 1.0,
      "allowRefillSpeedModifier": true
    },
    "MovementData": {
      "timeToSprint": 0.45, "timeToJog": 0.0,
      "rotationSpeedJog": 0.3, "rotationSpeedSprint": 0.15
    },
    "DrowningData": {
      "staminaDepletionSpeed": 10.0, "healthDepletionSpeed": 3.0,
      "shockDepletionSpeed": 10.0
    },
    "WeaponObstructionData": { "staticMode": 1, "dynamicMode": 1 }
  },
  "WorldsData": {
    "lightingConfig": 0, "objectSpawnersArr": [],
    "environmentMinTemps": [-3, -2, 0, 4, 9, 14, 18, 17, 13, 11, 9, 0],
    "environmentMaxTemps": [3, 5, 7, 14, 19, 24, 26, 25, 18, 14, 10, 5]
  },
  "BaseBuildingData": { "canBuildAnywhere": false, "canCraftAnywhere": false },
  "UIData": {
    "use3DMap": false,
    "HitIndicationData": {
      "hitDirectionOverrideEnabled": false, "hitDirectionBehaviour": 1,
      "hitDirectionStyle": 0, "hitDirectionIndicatorColorStr": "0xffbb0a1e",
      "hitDirectionMaxDuration": 2.0, "hitDirectionBreakPointRelative": 0.2,
      "hitDirectionScatter": 10.0, "hitIndicationPostProcessEnabled": true
    }
  }
}
```

- `version` -- must match what your server binary expects. Do not change it.
- `lightingConfig` -- `0` (default) or `1` (brighter nights).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 values, one per month (Jan-Dec).
- `disablePersonalLight` -- removes the faint ambient light near new players at night.
- `staminaMax` and sprint modifiers control how far players can run before exhaustion.
- `use3DMap` -- switches the in-game map to the terrain-rendered 3D variant.

---

## Multi-Map Servers

DayZ supports multiple maps through different mission folders inside `mpmissions/`:

| Map | Mission Folder |
|-----|---------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Each map has its own CE files (`types.xml`, `events.xml`, etc.). Switch maps via `template` in **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Or with a launch parameter: `-mission=mpmissions/dayzOffline.enoch`

To run multiple maps simultaneously, use separate server instances with their own config, profile directory, and port range.

---

## Custom Economy Tuning

### Splitting types.xml

Split items into multiple files and register them in **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

The server loads and merges all files with `type="types"`.

### Custom Categories and Tags

**cfglimitsdefinition.xml** defines categories/tags for `types.xml` but gets overwritten on updates. Use **cfglimitsdefinitionuser.xml** instead:

```xml
<lists>
    <categories>
        <category name="custom_rare" />
    </categories>
    <tags>
        <tag name="custom_event" />
    </tags>
</lists>
```

---

## cfgenvironment.xml and Animal Territories

The file **cfgenvironment.xml** in your mission folder links to territory files in the `env/` subdirectory:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

The `env/` folder contains these animal territory files:

| File | Animals |
|------|---------|
| **bear_territories.xml** | Brown bears |
| **wolf_territories.xml** | Wolf packs |
| **fox_territories.xml** | Foxes |
| **hare_territories.xml** | Rabbits/hares |
| **hen_territories.xml** | Chickens |
| **pig_territories.xml** | Pigs |
| **red_deer_territories.xml** | Red deer |
| **roe_deer_territories.xml** | Roe deer |
| **sheep_goat_territories.xml** | Sheep/goats |
| **wild_boar_territories.xml** | Wild boars |
| **cattle_territories.xml** | Cows |

A territory entry defines circular zones with position and animal count:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- center coordinates; `r` -- radius in meters
- `dmin`, `dmax` -- min/max animal count in the zone
- `smin`, `smax` -- reserved (set to `-1`)

---

## Custom Dynamic Events

Dynamic events (heli crashes, convoys) are defined in **events.xml**. To create a custom event:

**1. Define the event** in **events.xml**:

```xml
<event name="StaticMyCustomCrash">
    <nominal>3</nominal> <min>1</min> <max>5</max>
    <lifetime>1800</lifetime> <restock>600</restock>
    <saferadius>500</saferadius> <distanceradius>200</distanceradius> <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1" />
    <position>fixed</position> <limit>child</limit> <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_Mi8_Crashed" />
    </children>
</event>
```

**2. Add spawn positions** in **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Add infected guards** (optional) -- add `<secondary type="ZmbM_PatrolNormal_Autumn" />` elements in your event definition.

**4. Grouped spawns** (optional) -- define clusters in **cfgeventgroups.xml** and reference the group name in your event.

---

## Server Restart Automation

DayZ has no built-in restart scheduler. Use OS-level automation.

### Windows

Create **restart_server.bat** and run it via Windows Scheduled Task every 4-6 hours:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Create a shell script and add it to cron (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Always back up `storage_1/` before each restart. Corrupted persistence during shutdown can wipe player bases and vehicles.

---

## cfgweather.xml

The file **cfgweather.xml** in your mission folder controls weather patterns. Each map ships with its own defaults:

Each phenomenon has `min`, `max`, `duration_min`, and `duration_max` (seconds):

| Phenomenon | Default Min | Default Max | Notes |
|------------|-------------|-------------|-------|
| `overcast` | 0.0 | 1.0 | Drives cloud density and rain probability |
| `rain` | 0.0 | 1.0 | Only triggers above an overcast threshold. Set max to `0.0` for no rain |
| `fog` | 0.0 | 0.3 | Values above `0.5` produce near-zero visibility |
| `wind_magnitude` | 0.0 | 18.0 | Affects ballistics and player movement |

---

## Messages System

The file **db/messages.xml** in your mission folder controls scheduled server messages and shutdown warnings:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- minutes before the message triggers (for shutdown messages, minutes before server stops)
- `shutdown` -- `1` for shutdown-sequence messages, `0` for regular broadcasts

The messages system does not restart the server. It only displays warnings when a restart schedule is configured externally.

---

[Home](../README.md) | [<< Previous: Troubleshooting](11-troubleshooting.md) | [Part 9 Home](01-server-setup.md)
