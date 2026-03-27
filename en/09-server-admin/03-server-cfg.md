# Chapter 9.3: serverDZ.cfg Complete Reference

[Home](../README.md) | [<< Previous: Directory Structure](02-directory-structure.md) | **serverDZ.cfg Reference** | [Next: Loot Economy Deep Dive >>](04-loot-economy.md)

---

> **Summary:** Every parameter in `serverDZ.cfg` documented with its purpose, valid values, and default behavior. This file controls server identity, network settings, gameplay rules, time acceleration, and mission selection.

---

## Table of Contents

- [File Format](#file-format)
- [Server Identity](#server-identity)
- [Network & Security](#network--security)
- [Gameplay Rules](#gameplay-rules)
- [Time & Weather](#time--weather)
- [Performance & Login Queue](#performance--login-queue)
- [Persistence & Instance](#persistence--instance)
- [Mission Selection](#mission-selection)
- [Complete Example File](#complete-example-file)
- [Launch Parameters That Override Config](#launch-parameters-that-override-config)

---

## File Format

`serverDZ.cfg` uses Bohemia's config format (similar to C). Rules:

- Every parameter assignment ends with a **semicolon** `;`
- Strings are enclosed in **double quotes** `""`
- Comments use `//` for single-line
- The `class Missions` block uses braces `{}` and ends with `};`
- The file must be UTF-8 or ANSI encoded -- no BOM

A missing semicolon will cause the server to fail silently or ignore subsequent parameters.

---

## Server Identity

```cpp
hostname = "My DayZ Server";         // Server name shown in browser
password = "";                       // Password to connect (empty = public)
passwordAdmin = "";                  // Password for admin login via in-game console
description = "";                    // Description shown in server browser details
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `hostname` | string | `""` | Displayed in the server browser. Max ~100 characters. |
| `password` | string | `""` | Leave empty for a public server. Players must enter this to join. |
| `passwordAdmin` | string | `""` | Used with the `#login` command in-game. **Set this on every server.** |
| `description` | string | `""` | Multi-line descriptions are not supported. Keep it short. |

---

## Network & Security

```cpp
maxPlayers = 60;                     // Maximum player slots
verifySignatures = 2;                // PBO signature verification (only 2 is supported)
forceSameBuild = 1;                  // Require matching client/server exe version
enableWhitelist = 0;                 // Enable/disable whitelist
disableVoN = 0;                      // Disable voice over network
vonCodecQuality = 20;               // VoN audio quality (0-30)
guaranteedUpdates = 1;               // Network protocol (always use 1)
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `maxPlayers` | int | 1-60 | 60 | Affects RAM usage. Each player adds ~50-100 MB. |
| `verifySignatures` | int | 2 | 2 | Only value 2 is supported. Verifies PBO files against `.bisign` keys. |
| `forceSameBuild` | int | 0, 1 | 1 | When 1, clients must match the server's exact executable version. Always keep at 1. |
| `enableWhitelist` | int | 0, 1 | 0 | When 1, only Steam64 IDs listed in `whitelist.txt` can connect. |
| `disableVoN` | int | 0, 1 | 0 | Set to 1 to completely disable in-game voice chat. |
| `vonCodecQuality` | int | 0-30 | 20 | Higher values mean better voice quality but more bandwidth. 20 is a good balance. |
| `guaranteedUpdates` | int | 1 | 1 | Network protocol setting. Always use 1. |

### Shard ID

```cpp
shardId = "123abc";                  // Six alphanumeric characters for private shards
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `shardId` | string | `""` | Used for private hive servers. Players on servers with the same `shardId` share character data. Leave empty for a public hive. |

---

## Gameplay Rules

```cpp
disable3rdPerson = 0;               // Disable third-person camera
disableCrosshair = 0;               // Disable the crosshair
disablePersonalLight = 1;           // Disable the ambient player light
lightingConfig = 0;                 // Night brightness (0 = brighter, 1 = darker)
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | Set to 1 for first-person-only servers. This is the most common "hardcore" setting. |
| `disableCrosshair` | int | 0, 1 | 0 | Set to 1 to remove the crosshair. Often paired with `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | The "personal light" is a subtle glow around the player at night. Most servers disable it (value 1) for realism. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = brighter nights (moonlight visible). 1 = pitch-black nights (requires flashlight/NVG). |

---

## Time & Weather

```cpp
serverTime = "SystemTime";                 // Initial time
serverTimeAcceleration = 12;               // Time speed multiplier (0-24)
serverNightTimeAcceleration = 1;           // Night time speed multiplier (0.1-64)
serverTimePersistent = 0;                  // Save time between restarts
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `serverTime` | string | `"SystemTime"` or `"YYYY/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` uses the machine's local clock. Set a fixed time like `"2024/9/15/12/0"` for a permanent daytime server. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Multiplier for in-game time. At 12, a full 24-hour cycle takes 2 real hours. At 1, time is real-time. At 24, a full day passes in 1 hour. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Multiplied by `serverTimeAcceleration`. At value 4 with acceleration 12, night passes at 48x speed (very short nights). |
| `serverTimePersistent` | int | 0, 1 | 0 | When 1, the server saves its in-game clock to disk and resumes from it after restart. When 0, time resets to `serverTime` on every restart. |

### Common Time Configurations

**Always daytime:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Fast day/night cycle (2-hour days, short nights):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Real-time day/night:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Performance & Login Queue

```cpp
loginQueueConcurrentPlayers = 5;     // Players processed at once during login
loginQueueMaxPlayers = 500;          // Max login queue size
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `loginQueueConcurrentPlayers` | int | 5 | How many players can load in simultaneously. Lower values reduce server load spikes after a restart. Raise to 10-15 if your hardware is strong and players complain about queue times. |
| `loginQueueMaxPlayers` | int | 500 | If this many players are already queuing, new connections are rejected. 500 is fine for most servers. |

---

## Persistence & Instance

```cpp
instanceId = 1;                      // Server instance identifier
storageAutoFix = 1;                  // Auto-repair corrupted persistence files
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `instanceId` | int | 1 | Identifies the server instance. Persistence data is stored in `storage_<instanceId>/`. If you run multiple servers on the same machine, give each a different `instanceId`. |
| `storageAutoFix` | int | 1 | When 1, the server checks persistence files on startup and replaces corrupted ones with empty files. Always leave this at 1. |

---

## Mission Selection

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

The `template` value must exactly match a folder name inside `mpmissions/`. Available vanilla missions:

| Template | Map | DLC Required |
|----------|-----|:---:|
| `dayzOffline.chernarusplus` | Chernarus | No |
| `dayzOffline.enoch` | Livonia | Yes |
| `dayzOffline.sakhal` | Sakhal | Yes |

Custom missions (e.g., from mods or community maps) use their own template name. The folder must exist in `mpmissions/`.

---

## Complete Example File

This is the complete default `serverDZ.cfg` with all parameters:

```cpp
hostname = "EXAMPLE NAME";              // Server name
password = "";                          // Password to connect to the server
passwordAdmin = "";                     // Password to become a server admin

description = "";                       // Server browser description

enableWhitelist = 0;                    // Enable/disable whitelist (value 0-1)

maxPlayers = 60;                        // Maximum amount of players

verifySignatures = 2;                   // Verifies .pbos against .bisign files (only 2 is supported)
forceSameBuild = 1;                     // Require matching client/server version (value 0-1)

disableVoN = 0;                         // Enable/disable voice over network (value 0-1)
vonCodecQuality = 20;                   // Voice over network codec quality (values 0-30)

shardId = "123abc";                     // Six alphanumeric characters for private shard

disable3rdPerson = 0;                   // Toggles the 3rd person view (value 0-1)
disableCrosshair = 0;                   // Toggles the cross-hair (value 0-1)

disablePersonalLight = 1;              // Disables personal light for all clients
lightingConfig = 0;                     // 0 for brighter, 1 for darker night

serverTime = "SystemTime";             // Initial in-game time ("SystemTime" or "YYYY/MM/DD/HH/MM")
serverTimeAcceleration = 12;           // Time speed multiplier (0-24)
serverNightTimeAcceleration = 1;       // Night time speed multiplier (0.1-64), also multiplied by serverTimeAcceleration
serverTimePersistent = 0;              // Save time between restarts (value 0-1)

guaranteedUpdates = 1;                 // Network protocol (always use 1)

loginQueueConcurrentPlayers = 5;       // Players processed simultaneously during login
loginQueueMaxPlayers = 500;            // Maximum login queue size

instanceId = 1;                        // Server instance id (affects storage folder naming)

storageAutoFix = 1;                    // Auto-repair corrupted persistence (value 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Launch Parameters That Override Config

Some settings can be overridden via command-line parameters when launching `DayZServer_x64.exe`:

| Parameter | Overrides | Example |
|-----------|-----------|---------|
| `-config=` | Config file path | `-config=serverDZ.cfg` |
| `-port=` | Game port | `-port=2302` |
| `-profiles=` | Profiles output directory | `-profiles=profiles` |
| `-mod=` | Client-side mods (semicolon-separated) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Server-only mods | `-servermod=@MyServerMod` |
| `-BEpath=` | BattlEye path | `-BEpath=battleye` |
| `-dologs` | Enable logging | -- |
| `-adminlog` | Enable admin logging | -- |
| `-netlog` | Enable network logging | -- |
| `-freezecheck` | Auto-restart on freeze | -- |
| `-cpuCount=` | CPU cores to use | `-cpuCount=4` |
| `-noFilePatching` | Disable file patching | -- |

### Full Launch Example

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Mods are loaded in the order specified in `-mod=`. Dependency order matters: if Mod B requires Mod A, list Mod A first.

---

**Previous:** [Directory Structure](02-directory-structure.md) | [Home](../README.md) | **Next:** [Loot Economy Deep Dive >>](04-loot-economy.md)
