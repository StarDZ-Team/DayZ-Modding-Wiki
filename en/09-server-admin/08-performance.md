# Performance Tuning


---

> **Summary:** Server performance in DayZ comes down to three things: item count, dynamic events, and mod/player load. This chapter covers the specific settings that matter, how to diagnose problems, and what hardware actually helps, based on the CE's documented spawn/cleanup mechanics and widely-repeated server-admin community guidance. Where a claim below is a community rule of thumb rather than an engine-documented figure, it is marked as such.

---

## Table of Contents

- [What Affects Server Performance](#what-affects-server-performance)
- [globals.xml Tuning](#globals-xml-tuning)
- [Economy Tuning for Performance](#economy-tuning-for-performance)
- [cfgeconomycore.xml Logging](#cfgeconomycore-xml-logging)
- [serverDZ.cfg Performance Settings](#serverdz-cfg-performance-settings)
- [Mod Performance Impact](#mod-performance-impact)
- [Hardware Recommendations](#hardware-recommendations)
- [Monitoring Server Health](#monitoring-server-health)
- [Common Performance Mistakes](#common-performance-mistakes)

---

## What Affects Server Performance

Based on how the Central Economy and entity replication work (see [Loot Economy Deep Dive](04-loot-economy.md) and [Vehicle & Dynamic Event Spawning](05-vehicle-spawning.md)), and on the factors server-admin communities most consistently point to when diagnosing lag, the three biggest performance factors are:

1. **Item count** -- high `nominal` values in `types.xml` mean the Central Economy tracks and processes more objects every cycle. This is consistently the number one cause of server-side lag.
2. **Event spawning** -- too many active dynamic events (vehicles, animals, helicrashes) in `events.xml` consume spawn/cleanup cycles and entity slots.
3. **Player count + mod count** -- each connected player generates entity updates, and each mod adds script classes that the engine must compile and execute every tick.

The server game loop runs at a variable FPS that fluctuates with load. When the server cannot keep up, players experience desync -- rubber-banding, delayed item pickups, and hit registration failures.

Bohemia's sample `serverDZ.cfg` sets `serverFpsWarning = 15`, and the official reference documents a **minimum accepted value of 11**. It does not call 15 a default, and it does not describe 15 as a playability threshold -- it is the value below which the server logs its initial FPS warning. The FPS figures used throughout this chapter are **community rules of thumb** collected from server-admin practice, not engine-documented thresholds; they are useful for spotting a trend in your own logs, not for comparing servers.

---

## globals.xml Tuning

These are the vanilla defaults for the parameters that directly affect performance:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### What Each Value Controls

| Parameter | Default | Performance Effect |
|-----------|---------|-------------------|
| `ZombieMaxCount` | 1000 | Cap for total infected on the server. Each zombie runs AI pathfinding. Lowering to 500-700 noticeably improves server FPS on populated servers. |
| `AnimalMaxCount` | 200 | Cap for spawned animals across all zones; ambient wildlife is not counted against it. Animals have simpler AI than zombies but still consume tick time. Lower to 100 if you see FPS issues. |
| `ZoneSpawnDist` | 300 | Distance in meters at which zombie zones activate around players. Lowering to 200 means fewer simultaneous active zones. |
| `SpawnInitial` | 1200 | Number of spawn attempts (tests) allowed during initial item spawn, not a count of items spawned. The amount of loot spawned on first start is governed by `InitialSpawn` (default 100, a percentage). Higher values mean a longer initial load. Does not affect steady-state performance. |
| `CleanupLifetimeDefault` | 45 | Default lifetime in seconds for entities with no economy setup of their own that are already at damage >= 1.0 (ruined or dead) -- Bohemia's qualifier, not a blanket timer on every unconfigured item. Lower values mean faster cleanup cycles but more frequent CE processing. |

**Recommended performance profile** (for servers struggling above 40 players):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Economy Tuning for Performance

The Central Economy runs a continuous loop checking every item type against its `nominal`/`min` targets. More item types with higher nominals means more work per cycle.

### Reduce Nominal Values

Every item in `types.xml` with `nominal > 0` is tracked by the CE. If you have 2000 item types with an average nominal of 20, the CE is managing 40,000 objects. Reduce nominals across the board to cut this number:

- Common civilian items: lower from 15-40 to 10-25
- Weapons: keep low (vanilla is already 2-10)
- Clothing variants: consider disabling color variants you do not need (`nominal=0`)

### Reduce Dynamic Events

In `events.xml`, each active event spawns and monitors entity groups. Lower the `nominal` on vehicle and animal events, or set `<active>0</active>` on events you do not need.

### Use Idle Mode

When no players are connected, the CE can pause entirely:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` means the server enters idle mode 60 seconds after the last player disconnects. `IdleModeStartup=1` means the server starts in idle mode and only activates the CE when the first player connects. This prevents the server from churning through spawn cycles while empty.

### Tune Respawn Rate

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

These control how much the CE processes per respawn cycle. Bohemia's descriptions are specific: `RespawnLimit` is *"How many items of one type can be spawned at once"* -- a per-type cap, not a total -- `RespawnTypes` is *"How many different types can be respawned at once"*, and `RespawnAttempt` is *"How many attempts are performed during single item respawn"*. Lower values reduce CE load per tick but slow down loot respawning. The vanilla values above are already conservative.

---

## cfgeconomycore.xml Logging

Enable CE diagnostic logs temporarily to measure cycle times and identify bottlenecks. In your `cfgeconomycore.xml`:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

To diagnose performance, set `log_ce_statistics` to `"true"`. This outputs CE cycle timing to the server RPT log. Look for lines showing how long each CE cycle takes, and compare them against your own server's baseline (see [CE Cycle Warnings](#ce-cycle-warnings) for the commonly quoted figures and why they are only rules of thumb).

Set `log_ce_lootspawn` and `log_ce_lootcleanup` to `"true"` to see which item types are spawning and cleaning up most frequently. These are your candidates for nominal reduction.

**Turn logging off after diagnosis.** Log writes themselves consume I/O and can worsen performance if left enabled permanently.

---

## serverDZ.cfg Performance Settings

The main server configuration file has a handful of performance-related options:

| Setting | Effect |
|---------|--------|
| `maxPlayers` | Lower this if the server struggles. Each player generates network traffic and entity updates. Admins commonly report recovering several FPS by dropping from 60 to 40 slots, but the size of that gain is a rule of thumb, not a documented figure -- measure it on your own server. |
| `instanceId` | Determines the `storage_1/` path. Not a performance setting, but if your storage is on a slow disk, it affects persistence I/O. |
| `simulatedPlayersBatch` | Caps how many players the server simulates per frame. Bohemia's sample value is 20, and the official reference describes it as being there "for server performance gain". |
| `networkRangeClose` / `networkRangeNear` / `networkRangeFar` / `networkRangeDistantEffect` | The network bubble radii, in metres, that decide how much of the world each client is told about. Official defaults when unset are 20 / 150 / 1000 / 4000. Raising them costs both server CPU and bandwidth. |
| `networkObjectBatchCompute` / `networkObjectBatchSendCreate` / `networkObjectBatchSendDelete` | How many objects are checked, created and deleted per server frame. Bohemia's samples are 1000 / 10 / 10. |
| `networkObjectBatchLogSlow` | Logs a bubble iteration to the console when it exceeds this many seconds. Useful purely for diagnosis. |
| `serverFpsWarning` | The FPS below which the server logs its initial FPS warning. Bohemia's sample is 15 and the documented minimum is 11. It changes logging only -- it does not make the server run faster. |
| `defaultVisibility` / `defaultObjectViewDistance` | Server-side caps on terrain and object render distance (Bohemia's sample: 1375 each). A client asking for less still gets less. |

These are all documented in [serverDZ.cfg Reference -> Additional Official Parameters](03-server-cfg.md#additional-official-parameters). This chapter does not give tuned values for them, because this audit found no Bohemia-published or measured guidance on what to set them to -- change one at a time and measure.

**What you cannot change:** there is no setting to force a higher minimum server FPS. Server FPS is variable and fluctuates with load. You can cap the maximum with the `-limitFPS=` launch parameter (current max is 200) to lower CPU usage on low-population servers, but if the server cannot keep up under load, it simply runs slower.

---

## Mod Performance Impact

Each mod adds script classes that the engine compiles at startup and executes every tick. The impact varies dramatically by mod quality:

- **Content-only mods** (weapons, clothing, buildings) add item types but minimal script overhead. Their cost is in CE tracking, not tick processing.
- **Script-heavy mods** with `OnUpdate()` or `OnTick()` loops run code every server frame. Poorly optimized loops in these mods are the most common cause of mod-related lag.
- **Trader/economy mods** that maintain large inventories add persistent objects the engine must track.

### Guidelines

- Add mods incrementally. Test server FPS after each addition, not after adding 10 at once.
- Monitor server FPS with admin tools or RPT log output after adding new mods.
- If a mod causes issues, check its source for expensive per-frame operations.

Common server-admin guidance (a rule of thumb, not an engine-documented figure): items (types) and event spawning tend to be more demanding than mod scripts alone -- mods that add thousands of `types.xml` entries generally hurt CE cycle time more than mods that add a modest amount of per-frame script logic. Poorly written per-frame scripts can still dominate, so profile before assuming either factor is your bottleneck.

---

## Hardware Recommendations

DayZ server game logic is **single-threaded**. Multi-core CPUs help with OS overhead and network I/O, but the main game loop runs on one core.

That is not the whole picture for replication, though. With `multithreadedReplication = 1` the server processes network object replication on worker threads, and the size of that worker pool is set outside `serverDZ.cfg` -- in the `<jobsystem>` block of `dayzsetting.xml`, as `maxcores - reservedcores` with a floor of one worker. If you are sizing hardware or tuning threading, that block and the `-cpuCount=` launch parameter are the two controls involved; both are documented in [serverDZ.cfg Reference](03-server-cfg.md#the-jobsystem-block-in-dayzsetting-xml).

| Component | Recommendation | Why |
|-----------|---------------|-----|
| **CPU** | Highest single-thread performance you can get. AMD 5600X or better. | Game loop is single-threaded. Clock speed and IPC matter more than core count. |
| **RAM** | 8 GB minimum, 12-16 GB for heavily modded servers | Mods and large maps consume memory. Running out causes stutters. |
| **Storage** | SSD required | `storage_1/` persistence I/O is constant. HDD causes hitching during save cycles. |
| **Network** | 100 Mbps+ with low latency | Bandwidth matters less than ping stability for desync prevention. |

Dedicated-hardware pricing and specific provider offers change constantly, so this chapter does not endorse a provider or a price point -- shop for single-thread clock speed and IPC first, and confirm current pricing directly with the host.

Avoid shared/VPS hosting for populated servers. The noisy-neighbor problem on shared hardware causes unpredictable FPS drops that are impossible to diagnose from your end.

---

## Monitoring Server Health

### Server FPS

Check the RPT log for lines containing server FPS. The bands below are **community rules of thumb**, not engine-documented thresholds -- Bohemia documents only the `serverFpsWarning` parameter itself (sample 15, minimum 11). Use them to read the trend in your own logs:

| Server FPS | Status |
|------------|--------|
| 25-30 | Commonly reported as healthy. Minor fluctuations are expected during heavy combat or restarts. |
| 15-25 | Degraded in practice -- this is where admins typically start getting desync reports on item interactions and combat. |
| Below 15 | Where `serverFpsWarning`'s sample value sits. Admins consistently report rubber-banding, failed actions and unreliable hit registration in this range. |

### CE Cycle Warnings

With `log_ce_statistics` enabled, watch for CE cycle times. The often-quoted targets -- under 500ms normal, over 1000ms overloaded -- are **community rules of thumb**, not figures Bohemia publishes. What matters more than the absolute number is the direction: compare a cycle time against the same server's own baseline before you changed anything.

### Storage Growth

Monitor the size of `storage_1/`. Unchecked growth indicates persistence bloat -- too many placed objects, tents, or stashes accumulating. Regular server wipes or reducing `FlagRefreshMaxDuration` in `globals.xml` help control this. `FlagRefreshMaxDuration` is the refresh budget a raised territory flag holds, so lowering it shortens how long an unvisited base keeps its parts alive -- see [World State & Persistence](07-persistence.md#territory-flags-and-base-decay).

### Player Reports

Desync reports from players are your most reliable real-time indicator. Simultaneous rubber-banding reports from several players usually mean server FPS has dropped -- confirm it in the log rather than assuming a specific number.

---

## Common Performance Mistakes

### Nominal Values Too High

Setting every item to `nominal=50` because "more loot is fun" creates tens of thousands of tracked objects. The CE spends its entire cycle managing items instead of running the game. Start with vanilla nominals and increase selectively.

### Too Many Vehicle Events

Vehicles are expensive entities with physics simulation, attachment tracking, and persistence. Vanilla Chernarus spawns around 60 land vehicles and boats total across all `Vehicle*` events (nominal values summed from `events.xml` -- see [Vehicle & Dynamic Event Spawning](05-vehicle-spawning.md)). Raising that several-fold is a widely reported cause of FPS loss; the specific thresholds admins quote are rules of thumb, so raise the count in steps and measure.

### Running 30+ Mods Without Testing

Each mod is fine in isolation. The compound effect of a large mod set -- thousands of extra types, dozens of per-frame scripts and increased memory pressure -- is what hurts. The specific figures admins repeat ("30+ mods", "50% FPS loss") are **rules of thumb with no engine-documented basis**, and the real cost depends entirely on what the mods do, not how many there are. The actionable part is the method: add mods in batches of 3-5 and measure after each batch.

### Never Restarting the Server

Some mods have memory leaks that accumulate over time. Schedule automatic restarts every 4-6 hours. Most server hosting panels support this. Even well-written mods benefit from periodic restarts because the engine's own memory fragmentation increases over long sessions.

### Ignoring Storage Bloat

A `storage_1/` folder that grows to several gigabytes slows down every persistence cycle. Wipe or trim it periodically, especially if you allow base building with no decay limits.

### Logging Left Enabled

CE diagnostic logging, script debug logging, and admin tool logging all write to disk every tick. Enable them for diagnosis, then turn them off. Persistent verbose logging on a busy server can cost 1-2 FPS by itself.
