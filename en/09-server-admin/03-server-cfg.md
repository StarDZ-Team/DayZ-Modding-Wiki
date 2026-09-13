# serverDZ.cfg Reference


---

> **Summary:** The `serverDZ.cfg` parameters with their purpose, valid values, and default behavior. This file controls server identity, network settings, gameplay rules, time acceleration, logging, persistence, and mission selection.
>
> **Scope:** the grouped sections below cover the parameters most servers touch. Every parameter Bohemia documents on the official [Server Configuration](https://community.bistudio.com/wiki/DayZ:Server_Configuration) page is present on this page -- the less commonly changed ones are collected in [Additional Official Parameters](#additional-official-parameters) rather than repeated in every group. Four parameters documented here (`BattlEye`, `enableCfgGameplayFile`, `storeHouseStateDisabled`, `shardId`) do **not** appear on that official page; each is marked where it occurs. The official page itself was last edited 2024-10-10, so parameters added after that date may be documented only in patch notes.

---

## Table of Contents

- [File Format](#file-format)
- [Server Identity](#server-identity)
- [Network & Security](#network-security)
- [Gameplay Rules](#gameplay-rules)
- [Time & Weather](#time-weather)
- [Performance & Login Queue](#performance-login-queue)
- [Logging & Debug](#logging-debug)
- [Persistence & Instance](#persistence-instance)
- [Mission Selection](#mission-selection)
- [Additional Official Parameters](#additional-official-parameters)
- [Complete Example File](#complete-example-file)
- [Launch Parameters That Override Config](#launch-parameters-that-override-config)

---

## File Format

`serverDZ.cfg` uses Bohemia's config format (similar to C). Rules:

- Every parameter assignment ends with a **semicolon** `;`
- Strings are enclosed in **double quotes** `""`
- Array parameters use brace syntax: `motd[] = { "Line 1", "Line 2" };`
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
motd[] = { "Welcome!", "Rules: no toxicity." };  // Message of the day lines
motdInterval = 5;                    // Seconds between MOTD lines
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `hostname` | string | `""` | Displayed in the server browser. Max ~100 characters. |
| `password` | string | `""` | Leave empty for a public server. Players must enter this to join. |
| `passwordAdmin` | string | `""` | Used with the `#login` command in-game. **Set this on every server.** |
| `description` | string | `""` | Multi-line descriptions are not supported. Keep it short. |
| `motd[]` | string array | `{}` | Message-of-the-day lines shown in chat after players join. Each array element is one line. |
| `motdInterval` | int | `1` | Seconds between successive MOTD lines. Raise it so lines do not scroll past too fast. |

---

## Network & Security

```cpp
maxPlayers = 60;                     // Maximum player slots
verifySignatures = 2;                // PBO signature verification (only 2 is supported)
forceSameBuild = 1;                  // Require matching client/server exe version
enableWhitelist = 0;                 // Enable/disable whitelist
disableVoN = 0;                      // Disable voice over network
vonCodecQuality = 20;                // VoN audio quality (0-20)
guaranteedUpdates = 1;               // Network protocol (always use 1)
steamQueryPort = 2305;               // Steam query port for the server browser
disableBanlist = 0;                  // Ignore ban.txt when set to 1
BattlEye = 1;                        // Enable/disable BattlEye anti-cheat
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `maxPlayers` | int | 1-60 | 60 | Affects RAM usage. Each player adds ~50-100 MB. |
| `verifySignatures` | int | 2 | 2 | Only value 2 is supported. Verifies PBO files against `.bisign` keys. |
| `forceSameBuild` | int | 0, 1 | 1 | When 1, clients must match the server's exact executable version. Always keep at 1. |
| `enableWhitelist` | int | 0, 1 | 0 | When 1, only players listed in `whitelist.txt` can connect. Which identifier form that file takes is not documented by Bohemia -- see [Access Control](09-access-control.md#which-identifier-goes-in-these-files). |
| `disableVoN` | int | 0, 1 | 0 | Set to 1 to completely disable in-game voice chat. |
| `vonCodecQuality` | int | 0-20 | 20 | Higher values mean better voice quality but more bandwidth. **20 is the maximum**, not a mid-range balance -- the official reference documents the range as `values 0-20`. Lower it only if VoN bandwidth is a measured problem. |
| `guaranteedUpdates` | int | 1 | 1 | Network protocol setting. Always use 1. |
| `steamQueryPort` | int | 1-65535 | none documented | The UDP port Steam uses to query the server for the browser. Bohemia's sample config sets `2305` and describes the parameter as the fix for a server not appearing in the client browser; it states no default, so set it explicitly. If you run several servers on one machine, give each a unique value so they all appear in the browser. |
| `disableBanlist` | bool | false, true | false | When `true`, the server ignores the server-root `ban.txt`. Leave at `false` to enforce that ban list. Bohemia's [official reference](https://community.bistudio.com/wiki/DayZ:Server_Configuration) uses `disableBanlist = false;` and documents `false` as the default, as it does for `disablePrioritylist` below. Integer/boolean parser equivalence for this key is unverified here. Which identifier form the file takes is not documented by Bohemia -- see [Access Control](09-access-control.md#which-identifier-goes-in-these-files). |
| `BattlEye` | int | 0, 1 | 1 | Enables the BattlEye anti-cheat layer. Keep at 1 on public servers. Not documented on the official reference page -- see [the note below](#parameters-this-page-documents-that-bohemia-s-reference-does-not-list). |

---

## Gameplay Rules

```cpp
disable3rdPerson = 0;                // Disable third-person camera
disableCrosshair = 0;                // Disable the crosshair
disablePersonalLight = 1;            // Disable the ambient player light
lightingConfig = 0;                  // Night brightness (0 = brighter, 1 = darker)
respawnTime = 5;                     // Seconds a dead player waits before respawn
disableBaseDamage = 0;               // Block damage to fences/watchtowers
disableContainerDamage = 0;          // Block damage to tents/barrels
enableCfgGameplayFile = 0;           // Load cfggameplay.json from the mission
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | Set to 1 for first-person-only servers. This is the most common "hardcore" setting. |
| `disableCrosshair` | int | 0, 1 | 0 | Set to 1 to remove the crosshair. Often paired with `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | The "personal light" is a subtle glow around the player at night. Most servers disable it (value 1) for realism. |
| `lightingConfig` | int | 0, 1, 2 | 0 | 0 = brighter nights (moonlight visible). 1 = pitch-black nights (requires flashlight/NVG). 2 = Sakhal-specific lighting. |
| `respawnTime` | int | seconds | 5 | How long a dead player must wait before the respawn button becomes active. |
| `disableBaseDamage` | int | 0, 1 | 0 | When 1, player-built base structures (fences, watchtowers) cannot take damage. |
| `disableContainerDamage` | int | 0, 1 | 0 | When 1, deployable containers (tents, barrels, sea chests) cannot take damage. |
| `enableCfgGameplayFile` | int | 0, 1 | 0 | When 1, the server loads `cfggameplay.json` from the mission folder to override gameplay tuning (stamina, building, map, world). Confirmed by vanilla script rather than by the official config page -- see [the note below](#parameters-this-page-documents-that-bohemia-s-reference-does-not-list). |

---

## Time & Weather

```cpp
serverTime = "SystemTime";                 // Initial time
serverTimeAcceleration = 12;               // Time speed multiplier (0.1-64)
serverNightTimeAcceleration = 1;           // Night time speed multiplier (0.1-64)
serverTimePersistent = 0;                  // Save time between restarts
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `serverTime` | string | `"SystemTime"` or `"YYYY/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` uses the machine's local clock. Set a fixed time like `"2024/9/15/12/0"` for a permanent daytime server. |
| `serverTimeAcceleration` | float | 0.1-64 | 1 | Multiplier for in-game time. At 12, a full 24-hour cycle takes 2 real hours. At 1, time is real-time. At 24, a full day passes in 1 hour. **A value of `0` is accepted as a special case that freezes time** -- combine it with a fixed `serverTime` for a permanent day (or night) server. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Multiplied by `serverTimeAcceleration`. At value 4 with acceleration 12, night passes at 48x speed (very short nights). |
| `serverTimePersistent` | int | 0, 1 | 0 | When 1, the server saves its in-game clock to disk and resumes from it after restart. When 0, time resets to `serverTime` on every restart. |

### Common Time Configurations

**Always daytime (frozen time):**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;        // 0 freezes the clock at the serverTime value
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
multithreadedReplication = 1;        // Spread network replication across threads
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `loginQueueConcurrentPlayers` | int | 1+ | 5 | How many players can load in simultaneously. Lower values reduce server load spikes after a restart. Raise to 10-15 if your hardware is strong and players complain about queue times. |
| `loginQueueMaxPlayers` | int | 1+ | 500 | If this many players are already queuing, new connections are rejected. 500 is fine for most servers. |
| `multithreadedReplication` | int | 0, 1 | 1 | When 1, the server spreads network object replication across worker threads. Leave at 1 on modern multi-core hardware. The **number** of worker threads does not come from this parameter: the official reference states it "is derived by settings of jobsystem in dayzSettings.xml by `maxcores` and `reservedcores` parameters" -- see [The jobsystem block in dayzsetting.xml](#the-jobsystem-block-in-dayzsetting-xml) below. |

### The jobsystem block in dayzsetting.xml

This file in the server root is easy to dismiss as a client video-settings leftover. It is not: Bohemia's [Server Configuration](https://community.bistudio.com/wiki/DayZ:Server_Configuration) reference has an **XML Configuration** section whose entire content is this file's `<jobsystem>` block, and it is what sizes the server's worker-thread pool.

```xml
<jobsystem globalqueue="4096" threadqueue="1024">
    <pc maxcores="4" reservedcores="1" />
</jobsystem>
```

| Attribute | Meaning |
|-----------|---------|
| `maxcores` | Maximum number of CPU cores the job system will use. |
| `reservedcores` | Number of cores held back for the engine's other threads. |
| `globalqueue` / `threadqueue` | Job-queue sizes for the global and per-thread queues. |

Bohemia's inline comment gives the arithmetic: the worker-thread count is `maxcores - reservedcores`, **but at least one worker thread is always allocated**. So `maxcores="4" reservedcores="1"` yields three workers, and a configuration that would compute zero or fewer still gets one.

This is the knob that actually sizes the pool `multithreadedReplication` uses. The `-cpuCount=` launch parameter is a separate control -- Bohemia documents it as setting "the number of logical CPU cores to use for parallel tasks processing", and advises it be less than or equal to the number of available cores.

> **Filename spelling.** Bohemia's page spells this file `dayzsettings.xml` in its heading and `dayzSettings.xml` in the `multithreadedReplication` text, while the singular `dayzsetting.xml` is what the server root is widely reported to contain. No DayZ dedicated-server install was available to this audit, so the on-disk spelling could not be confirmed; check your own server root before editing, and be aware both spellings are in circulation.

---

## Logging & Debug

```cpp
timeStampFormat = "Short";           // Timestamp style in .RPT logs
logAverageFps = 1;                   // Write average FPS to the log
logMemory = 1;                       // Write memory usage to the log
logPlayers = 1;                      // Write connected-player count to the log
logFile = "server_console.log";      // Console log file name
adminLogPlayerHitsOnly = 0;          // Log only player-on-player hits
adminLogPlacement = 0;               // Log object placement
adminLogBuildActions = 0;            // Log base-building actions
adminLogPlayerList = 0;              // Periodically log the player list
enableDebugMonitor = 0;              // In-game debug overlay for players
```

| Parameter | Type | Valid Values | Default | Notes |
|-----------|------|-------------|---------|-------|
| `timeStampFormat` | string | `"None"`, `"Short"`, `"Full"` | `"None"` | Prefix format for lines in the `.RPT` log. `"Short"` is the most readable for day-to-day work. |
| `logAverageFps` | int | 0, 1 | 0 | When 1, periodic average-FPS lines are written to the log. Useful for spotting performance dips. |
| `logMemory` | int | 0, 1 | 0 | When 1, periodic memory-usage lines are written to the log. |
| `logPlayers` | int | 0, 1 | 0 | When 1, the current connected-player count is written to the log periodically. |
| `logFile` | string | file name | `""` | Name of the console log file written to the profiles directory. |
| `adminLogPlayerHitsOnly` | int | 0, 1 | 0 | When 1, the admin log records only player-versus-player hits (not zombie/animal hits). Requires the `-adminlog` launch parameter. |
| `adminLogPlacement` | int | 0, 1 | 0 | When 1, object placement events are written to the admin log. |
| `adminLogBuildActions` | int | 0, 1 | 0 | When 1, base-building actions are written to the admin log. |
| `adminLogPlayerList` | int | 0, 1 | 0 | When 1, the full connected-player list is written to the admin log at intervals. |
| `enableDebugMonitor` | int | 0, 1 | 0 | When 1, players can open an in-game debug overlay (position, stats). Leave 0 on production servers. |

The `adminLog*` parameters only take effect when the server is launched with `-adminlog`. See [Launch Parameters](#launch-parameters-that-override-config).

---

## Persistence & Instance

```cpp
instanceId = 1;                      // Server instance identifier
storageAutoFix = 1;                  // Auto-repair corrupted persistence files
storeHouseStateDisabled = 0;         // Persist building states (0 = persist)
shardId = "123abc";                  // Private-shard identifier -- the widely circulated community sample, NOT a
                                     // form the script evidence supports (see notes below)
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `instanceId` | int | 1 | Identifies the server instance. Persistence data is stored in `storage_<instanceId>/`. If you run multiple servers on the same machine, give each a different `instanceId`. |
| `storageAutoFix` | int | 1 | When 1, the server checks persistence files on startup and replaces corrupted ones with empty files. Always leave this at 1. |
| `storeHouseStateDisabled` | int | 0 | Reported to stop building interior states (opened doors, ruined walls) from persisting between restarts when set to 1. **Unconfirmed** -- not on the official reference page and not read by any vanilla script; see [the note below](#parameters-this-page-documents-that-bohemia-s-reference-does-not-list). |
| `shardId` | string | `""` | Commonly described as joining servers into a shared private hive when they use the same value. **Unconfirmed**, and the only vanilla script handling a `shardId` implies a different format -- see [the note below](#parameters-this-page-documents-that-bohemia-s-reference-does-not-list). |

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

## Additional Official Parameters

These are documented on Bohemia's official Server Configuration page but are changed less often than the groups above. Values shown are the ones in Bohemia's own sample; where the official text names a default explicitly, that is stated.

### Access and moderation

| Parameter | Sample | Notes |
|-----------|--------|-------|
| `disablePrioritylist` | `false` | Disables use of `priority.txt` (official default: `false`). Prioritised players jump ahead of everyone else in the login queue. Bohemia's own example for this file is semicolon-separated and SteamID64-shaped -- `SteamId;SteamId;01234567890123456;01234567890123456` -- not one identifier per line. See [Access Control](09-access-control.md#which-identifier-goes-in-these-files). |
| `disableMultiAccountMitigation` | `false` | Disables multi-account mitigation **on consoles** when `true` (official default: `false`). |
| `disableRespawnDialog` | `0` | Set to 1 to suppress the respawn dialog, so new characters always spawn as random. Read by vanilla script at `scripts/3_game/cfggameplaydatajson.c`. |

### Connection quality and kicks

| Parameter | Sample | Notes |
|-----------|--------|-------|
| `pingWarning` | `200` | Ping in milliseconds at which the client shows the initial yellow ping warning. |
| `pingCritical` | `250` | Ping in milliseconds at which the client shows the red ping warning. |
| `MaxPing` | `300` | Ping in milliseconds at which a player is kicked. Note the capital `M` -- this is how the official reference spells it. |
| `serverFpsWarning` | `15` | Server FPS below which the initial server-FPS warning is triggered. The official reference states a **minimum accepted value of 11**; it does not label 15 a default. See [Performance Tuning](08-performance.md#monitoring-server-health). |
| `clientPort` | `2304` | Forces the port clients connect with. |

### Anti-cheat and validation

| Parameter | Sample | Notes |
|-----------|--------|-------|
| `speedhackDetection` | `1` | Enables speedhack detection. Official range is 1-10 and may be a float, where **1 is strict and 10 is benevolent**. Omitting it disables the check. |
| `shotValidation` | `1` | `1` enables shot validation, `0` disables it. |
| `allowFilePatching` | `1` | When `1`, clients launched with `-filePatching` may connect. Leave it at `0` on a production server: it is what lets a client run with unpacked, unsigned script data. Needed on a **development** server when you are iterating on scripts. A mismatch here is what produces a connect refusal reporting **`EConnectErrorServer.FILE_PATCHING`** (*"The server does not accept the client's current filePatching setting."*) -- see [Diagnosing the FILE_PATCHING connect refusal](#diagnosing-the-file-patching-connect-refusal). |

### Performance and network bubbles

| Parameter | Sample | Notes |
|-----------|--------|-------|
| `simulatedPlayersBatch` | `20` | Caps how many players are simulated per frame. |
| `networkRangeClose` | `20` | Network bubble radius in metres for spawning close objects that contain items (backpacks and similar). Official default when unset: 20. |
| `networkRangeNear` | `150` | Bubble radius in metres for near inventory-item objects (despawn is +10%). Official default when unset: 150. |
| `networkRangeFar` | `1000` | Bubble radius in metres for far objects other than inventory items (despawn +10%). Official default when unset: 1000. |
| `networkRangeDistantEffect` | `4000` | Bubble radius in metres for effects -- currently sound effects only. Official default when unset: 4000. |
| `networkObjectBatchLogSlow` | `5` | Maximum seconds a bubble may take to iterate before the slow pass is logged to the console. |
| `networkObjectBatchEnforceBandwidthLimits` | `1` | Enables an object-creation limiter driven by bandwidth statistics. |
| `networkObjectBatchUseEstimatedBandwidth` | `0` | `0` uses actual data sent since the last server frame; `1` uses a crude estimate. |
| `networkObjectBatchUseDynamicMaximumBandwidth` | `1` | Whether the limit is a fraction of the fluctuating maximum sendable bandwidth (`1`) or a hard limit (`0`). |
| `networkObjectBatchBandwidthLimit` | `0.8` | The limit itself. A `[0,1]` fraction or a `[1,inf]` absolute value, depending on the parameter above. |
| `networkObjectBatchCompute` | `1000` | Objects checked in the create/destroy lists per server frame. |
| `networkObjectBatchSendCreate` | `10` | Maximum objects sent for creation per frame. |
| `networkObjectBatchSendDelete` | `10` | Maximum objects sent for deletion per frame. |

Raising the `networkRange*` values increases what each client is told about, and therefore both server CPU and bandwidth. Treat them as a trade, not free view distance.

### Render distance

| Parameter | Sample | Notes |
|-----------|--------|-------|
| `defaultVisibility` | `1375` | Highest terrain render distance the server permits. If a client's own `viewDistance` is lower, the client value applies. |
| `defaultObjectViewDistance` | `1375` | Highest object render distance the server permits. If a client's own `preferredObjectViewDistance` is lower, the client value applies. |

### Parameters this page documents that Bohemia's reference does not list

These four appear in widely circulated `serverDZ.cfg` files and in the sections above, but are **absent from the official Server Configuration page**. Absence from that page is not proof they do nothing -- the page was last edited 2024-10-10 and is not exhaustive for every engine-read key -- but their behaviour here is not backed by a Bohemia-authored description:

| Parameter | Status |
|-----------|--------|
| `enableCfgGameplayFile` | **Confirmed by vanilla script**, not by the official config page: `scripts/3_game/cfggameplayhandler.c` reads it via `ServerConfigGetInt("enableCfgGameplayFile")` to decide whether to load `cfggameplay.json`. |
| `BattlEye` | Widely used and consistent with BattlEye being toggleable, but not documented on the official page and not read by any vanilla script in the extraction. Unconfirmed. |
| `storeHouseStateDisabled` | Not on the official page and not read by any vanilla script in the extraction. The described effect (building interior states not persisted) is **unconfirmed** -- verify on your own server before relying on it. |
| `shardId` | Not on the official page. The only vanilla scripts that handle a `shardId` are two files in the client server browser, and both apply the identical test -- a server counts as official when the value is **3 characters long and numerically below 200**: `scripts/5_mission/gui/newui/serverbrowsermenu/serverbrowserdetailscontainer.c` (`SetType()`, line 150) labels the server type from it, and `serverbrowserentry.c:298` sets the official/private flag on the list entry from it. Both are inside `PLATFORM_WINDOWS` / not-`PLATFORM_CONSOLE` guards, so this is client browser presentation, not server-side hive logic. The test does not match the "six alphanumeric characters" convention repeated in community guides. Whether setting `shardId` actually joins servers to a shared private hive is **unconfirmed by any primary source**. |


---

## Complete Example File

This is a working `serverDZ.cfg` covering the parameters most servers change. It is deliberately not every parameter on this page -- the entries in [Additional Official Parameters](#additional-official-parameters) are omitted so the file stays readable, and every one of them is optional:

```cpp
hostname = "EXAMPLE NAME";              // Server name
password = "";                          // Password to connect to the server
passwordAdmin = "";                     // Password to become a server admin
description = "";                       // Server browser description

motd[] = { "Welcome to the server", "Have fun and be respectful" };
motdInterval = 5;                       // Seconds between MOTD lines

enableWhitelist = 0;                    // Enable/disable whitelist (value 0-1)
disableBanlist = 0;                     // Ignore ban.txt when set to 1
BattlEye = 1;                           // Enable/disable BattlEye (value 0-1)

maxPlayers = 60;                        // Maximum amount of players

verifySignatures = 2;                   // Verifies .pbos against .bisign files (only 2 is supported)
forceSameBuild = 1;                     // Require matching client/server version (value 0-1)

disableVoN = 0;                         // Enable/disable voice over network (value 0-1)
vonCodecQuality = 20;                   // Voice over network codec quality, higher is better (values 0-20)

steamQueryPort = 2305;                  // Steam query port (unique per instance)

disable3rdPerson = 0;                   // Toggles the 3rd person view (value 0-1)
disableCrosshair = 0;                   // Toggles the cross-hair (value 0-1)

disablePersonalLight = 1;               // Disables personal light for all clients
lightingConfig = 0;                     // 0 for brighter, 1 for darker night

respawnTime = 5;                        // Seconds before a dead player can respawn
disableBaseDamage = 0;                  // Block damage to fences/watchtowers (value 0-1)
disableContainerDamage = 0;             // Block damage to tents/barrels (value 0-1)
enableCfgGameplayFile = 0;              // Load cfggameplay.json from the mission (value 0-1)

serverTime = "SystemTime";              // Initial in-game time ("SystemTime" or "YYYY/MM/DD/HH/MM")
serverTimeAcceleration = 12;            // Time speed multiplier (0.1-64; 0 freezes time)
serverNightTimeAcceleration = 1;        // Night time speed multiplier (0.1-64), also multiplied by serverTimeAcceleration
serverTimePersistent = 0;               // Save time between restarts (value 0-1)

guaranteedUpdates = 1;                  // Network protocol (always use 1)
multithreadedReplication = 1;           // Spread replication across threads (value 0-1)

loginQueueConcurrentPlayers = 5;        // Players processed simultaneously during login
loginQueueMaxPlayers = 500;             // Maximum login queue size

timeStampFormat = "Short";              // Log timestamp format ("None"/"Short"/"Full")
logAverageFps = 1;                      // Log average FPS
logMemory = 1;                          // Log memory usage
logPlayers = 1;                         // Log connected player count
logFile = "server_console.log";         // Console log file name

adminLogPlayerHitsOnly = 0;             // Log only PvP hits (requires -adminlog)
adminLogPlacement = 0;                  // Log object placement
adminLogBuildActions = 0;               // Log base-building actions
adminLogPlayerList = 0;                 // Periodically log the player list

enableDebugMonitor = 0;                 // In-game debug overlay (value 0-1)

instanceId = 1;                         // Server instance id (affects storage folder naming)
storageAutoFix = 1;                     // Auto-repair corrupted persistence (value 0-1)
storeHouseStateDisabled = 0;            // Persist building states (value 0-1)
shardId = "123abc";                     // Widely circulated community sample; format and effect unconfirmed -- see notes

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
| `-mission=` | Mission used by the server | `-mission=mpmissions\dayzOffline.enoch` |
| `-storage=` | Custom root folder for the storage location | `-storage=D:\dayz-storage` |
| `-dologs` | Enable all log messages in the RPT file | -- |
| `-adminlog` | Enable admin logging (needed by `adminLog*`) | -- |
| `-netlog` | Enable network traffic logging | -- |
| `-freezeCheck` | Stop + crash dump on freeze | -- |
| `-cpuCount=` | Logical CPU cores to use for parallel task processing (keep at or below the cores available) | `-cpuCount=4` |
| `-limitFPS=` | Cap server FPS to lower CPU use (current max 200) | `-limitFPS=60` |
| `-filePatching` | File-patching mode -- see the caution below | -- |

**`-freezeCheck` does not restart the server.** Bohemia documents it as: *"Stops the server when frozen for more than 5 min and create a dump file."* It halts the frozen process and writes a dump you can send to support; bringing the server back up is entirely the job of your own external supervision (a Scheduled Task, a systemd unit, or a hosting panel's watchdog). If you assume it self-recovers, the server stays down until someone notices. See [Server Restart Automation](12-advanced.md#server-restart-automation) for a working restart loop, and [Server Setup](01-server-setup.md#step-2-launch-the-server) for the same parameter in context.

The official casing is `-freezeCheck`. This page uses the official casing throughout; whether the engine also accepts `-freezecheck` was not tested for this audit.

#### Diagnosing the FILE_PATCHING connect refusal

A client refused at connect with the message *"The server does not accept the client's current filePatching setting."* has hit this parameter. That message is first-party: it is the shipped English text of the `server_browser_bad_file_patching` key in `languagecore/stringtable.csv` (line 796), and `connecterrorservermodule.c:10` and `:56` map `EConnectErrorServer.FILE_PATCHING` to that same string key, commented *"Bad file patching"*. **Identify the refusal by that message and by the `FILE_PATCHING` enum name, not by a hex code.** DayZ formats connect errors as an int made of two shorts, category in the high half and code in the low half (`ErrorModuleHandler`, `scripts/3_game/global/errormodulehandler/errormodulehandler.c`). In the shipped enum the first member's `= -1` is commented out, so the enum starts at `0`: `Unknown = 0, Generic = 1, ConnectErrorClient = 2, ConnectErrorServer = 3, ...`. Composing the halves the way this page describes them gives `0x00030005` for a `ConnectErrorServer` category / `FILE_PATCHING` code refusal, derived explicitly from `ErrorCategory.ConnectErrorServer = 3` and `EConnectErrorServer.FILE_PATCHING = 5`. `0x00020005` decomposes instead to `ErrorCategory.ConnectErrorClient` (category `2`) code `5`, which `connecterrorclientmodule.c` declares as `INVALID_SESSION` (*"The guid of the session is empty"*) -- unrelated to file patching. If a client or a third-party launcher reports a hex code for this refusal, do not assume it matches the packing above without checking that tool's own source against the enum names first.

So the server reached a decision and rejected the client. Check that `allowFilePatching = 1` is set in the config the server actually loaded (`-config=`), and that the server was restarted after the change. Note that admins report this refusal persisting even with `-filePatching` on both the server and client command lines, with no settled community answer; if you hit that, the setting to verify first is the server-side `allowFilePatching`, not the client switch.

**`-filePatching` is documented inconsistently by Bohemia.** The Server Configuration page describes it as *"Ensures that only PBOs are loaded and NO unpacked data"*, while the same page's `allowFilePatching` entry and the official Modding Basics procedure both describe it as the flag that lets a client load **unpacked** data. Two of the three point the same way, but this wiki does not silently pick a winner -- do not rely on `-filePatching` as a "PBO-only" hardening switch. Modding use of the flag is covered in Part 8.

### Full Launch Example

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@Lantern ^
  -servermod=@Lantern_AIServer ^
  -dologs -adminlog -netlog -freezeCheck
```

Mods are loaded in the order specified in `-mod=`. Dependency order matters: if Mod B requires Mod A, list Mod A first. In this example the shared library `@Lantern` is listed before the content mods that depend on it.
