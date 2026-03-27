# Chapter 9.8: Performance Tuning

[Home](../README.md) | [<< Previous: Persistence](07-persistence.md) | [Next: Access Control >>](09-access-control.md)

---

> **Summary:** Server performance in DayZ comes down to three things: item count, dynamic events, and mod/player load. This chapter covers the specific settings that matter, how to diagnose problems, and what hardware actually helps -- all based on real community data from 400+ Discord reports of FPS drops, lag, and desync.

---

## Table of Contents

- [What Affects Server Performance](#what-affects-server-performance)
- [globals.xml Tuning](#globalsxml-tuning)
- [Economy Tuning for Performance](#economy-tuning-for-performance)
- [cfgeconomycore.xml Logging](#cfgeconomycorexml-logging)
- [serverDZ.cfg Performance Settings](#serverdzycfg-performance-settings)
- [Mod Performance Impact](#mod-performance-impact)
- [Hardware Recommendations](#hardware-recommendations)
- [Monitoring Server Health](#monitoring-server-health)
- [Common Performance Mistakes](#common-performance-mistakes)

---

## What Affects Server Performance

From community data (400+ Discord mentions of FPS/performance/lag/desync), the three biggest performance factors are:

1. **Item count** -- high `nominal` values in `types.xml` mean the Central Economy tracks and processes more objects every cycle. This is consistently the number one cause of server-side lag.
2. **Event spawning** -- too many active dynamic events (vehicles, animals, helicrashes) in `events.xml` consume spawn/cleanup cycles and entity slots.
3. **Player count + mod count** -- each connected player generates entity updates, and each mod adds script classes that the engine must compile and execute every tick.

The server game loop runs at a fixed 30 FPS tick rate. When the server cannot maintain 30 FPS, players experience desync -- rubber-banding, delayed item pickups, and hit registration failures. Below 15 server FPS, the game becomes unplayable.

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
| `AnimalMaxCount` | 200 | Cap for animals. Animals have simpler AI than zombies but still consume tick time. Lower to 100 if you see FPS issues. |
| `ZoneSpawnDist` | 300 | Distance in meters at which zombie zones activate around players. Lowering to 200 means fewer simultaneous active zones. |
| `SpawnInitial` | 1200 | Number of items the CE spawns on first start. Higher values mean a longer initial load. Does not affect steady-state performance. |
| `CleanupLifetimeDefault` | 45 | Default cleanup time in seconds for items without a specific lifetime. Lower values mean faster cleanup cycles but more frequent CE processing. |

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

These control how many items and item types the CE processes per cycle. Lower values reduce CE load per tick but slow down loot respawning. The vanilla defaults above are already conservative.

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

To diagnose performance, set `log_ce_statistics` to `"true"`. This outputs CE cycle timing to the server RPT log. Look for lines showing how long each CE cycle takes -- if cycles exceed 1000ms, the economy is overloaded.

Set `log_ce_lootspawn` and `log_ce_lootcleanup` to `"true"` to see which item types are spawning and cleaning up most frequently. These are your candidates for nominal reduction.

**Turn logging off after diagnosis.** Log writes themselves consume I/O and can worsen performance if left enabled permanently.

---

## serverDZ.cfg Performance Settings

The main server configuration file has limited performance-related options:

| Setting | Effect |
|---------|--------|
| `maxPlayers` | Lower this if the server struggles. Each player generates network traffic and entity updates. Going from 60 to 40 players can recover 5-10 server FPS. |
| `instanceId` | Determines the `storage_1/` path. Not a performance setting, but if your storage is on a slow disk, it affects persistence I/O. |

**What you cannot change:** the server tick rate is fixed at 30 FPS. There is no setting to increase or decrease it. If the server cannot maintain 30 FPS, it simply runs slower.

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

Community consensus: "Items (types) and event spawning are the most demanding -- mods that add thousands of types.xml entries hurt more than mods that add complex scripts."

---

## Hardware Recommendations

DayZ server game logic is **single-threaded**. Multi-core CPUs help with OS overhead and network I/O, but the main game loop runs on one core.

| Component | Recommendation | Why |
|-----------|---------------|-----|
| **CPU** | Highest single-thread performance you can get. AMD 5600X or better. | Game loop is single-threaded. Clock speed and IPC matter more than core count. |
| **RAM** | 8 GB minimum, 12-16 GB for heavily modded servers | Mods and large maps consume memory. Running out causes stutters. |
| **Storage** | SSD required | `storage_1/` persistence I/O is constant. HDD causes hitching during save cycles. |
| **Network** | 100 Mbps+ with low latency | Bandwidth matters less than ping stability for desync prevention. |

Community tip: "OVH provides good value -- around $60 USD for a dedicated 5600X machine that handles 60-slot modded servers."

Avoid shared/VPS hosting for populated servers. The noisy-neighbor problem on shared hardware causes unpredictable FPS drops that are impossible to diagnose from your end.

---

## Monitoring Server Health

### Server FPS

Check the RPT log for lines containing server FPS. A healthy server maintains 30 FPS consistently. Warning thresholds:

| Server FPS | Status |
|------------|--------|
| 25-30 | Normal. Minor fluctuations are expected during heavy combat or restarts. |
| 15-25 | Degraded. Players notice desync on item interactions and combat. |
| Below 15 | Critical. Rubber-banding, failed actions, hit registration broken. |

### CE Cycle Warnings

With `log_ce_statistics` enabled, watch for CE cycle times. Normal is under 500ms. If cycles regularly exceed 1000ms, your economy is too heavy.

### Storage Growth

Monitor the size of `storage_1/`. Unchecked growth indicates persistence bloat -- too many placed objects, tents, or stashes accumulating. Regular server wipes or reducing `FlagRefreshMaxDuration` in `globals.xml` help control this.

### Player Reports

Desync reports from players are your most reliable real-time indicator. If multiple players report rubber-banding simultaneously, the server FPS has dropped below 15.

---

## Common Performance Mistakes

### Nominal Values Too High

Setting every item to `nominal=50` because "more loot is fun" creates tens of thousands of tracked objects. The CE spends its entire cycle managing items instead of running the game. Start with vanilla nominals and increase selectively.

### Too Many Vehicle Events

Vehicles are expensive entities with physics simulation, attachment tracking, and persistence. Vanilla spawns around 50 vehicles total. Servers running 150+ vehicles see significant FPS loss.

### Running 30+ Mods Without Testing

Each mod is fine in isolation. The compound effect of 30+ mods -- thousands of extra types, dozens of per-frame scripts, and increased memory pressure -- can drop server FPS by 50% or more. Add mods in batches of 3-5 and test after each batch.

### Never Restarting the Server

Some mods have memory leaks that accumulate over time. Schedule automatic restarts every 4-6 hours. Most server hosting panels support this. Even well-written mods benefit from periodic restarts because the engine's own memory fragmentation increases over long sessions.

### Ignoring Storage Bloat

A `storage_1/` folder that grows to several gigabytes slows down every persistence cycle. Wipe or trim it periodically, especially if you allow base building with no decay limits.

### Logging Left Enabled

CE diagnostic logging, script debug logging, and admin tool logging all write to disk every tick. Enable them for diagnosis, then turn them off. Persistent verbose logging on a busy server can cost 1-2 FPS by itself.

---

[Home](../README.md) | [<< Previous: Persistence](07-persistence.md) | [Next: Access Control >>](09-access-control.md)
