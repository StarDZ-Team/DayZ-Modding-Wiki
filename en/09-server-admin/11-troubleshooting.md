# Chapter 9.11: Server Troubleshooting

[Home](../README.md) | [<< Previous: Mod Management](10-mod-management.md) | [Next: Advanced Topics >>](12-advanced.md)

---

> **Summary:** Diagnose and fix the most common DayZ server problems -- startup failures, connection issues, crashes, loot and vehicle spawning, persistence, and performance. Every solution here comes from real failure patterns across thousands of community reports.

---

## Table of Contents

- [Server Won't Start](#server-wont-start)
- [Players Can't Connect](#players-cant-connect)
- [Crashes and Null Pointers](#crashes-and-null-pointers)
- [Loot Not Spawning](#loot-not-spawning)
- [Vehicles Not Spawning](#vehicles-not-spawning)
- [Persistence Issues](#persistence-issues)
- [Performance Problems](#performance-problems)
- [Reading Log Files](#reading-log-files)
- [Quick Diagnostic Checklist](#quick-diagnostic-checklist)

---

## Server Won't Start

### Missing DLL Files

If `DayZServer_x64.exe` crashes immediately with a missing DLL error, install the latest **Visual C++ Redistributable for Visual Studio 2019** (x64) from Microsoft's official site and restart.

### Port Already in Use

Another DayZ instance or application is occupying port 2302. Check with `netstat -ano | findstr 2302` (Windows) or `ss -tulnp | grep 2302` (Linux). Kill the conflicting process or change your port with `-port=2402`.

### Missing Mission Folder

The server expects `mpmissions/<template>/` where the folder name exactly matches the `template` value in **serverDZ.cfg**. For Chernarus, that is `mpmissions/dayzOffline.chernarusplus/` and it must contain at least **init.c**.

### Invalid serverDZ.cfg

A single missing semicolon or wrong quote type prevents startup silently. Watch for:

- Missing `;` at end of value lines
- Smart quotes instead of straight quotes
- Missing `{};` block around class entries

### Missing Mod Files

Every path in `-mod=@CF;@VPPAdminTools;@MyMod` must exist relative to the server root and contain an **addons/** folder with `.pbo` files. A single bad path prevents startup.

---

## Players Can't Connect

### Port Forwarding

DayZ requires these ports forwarded and open in your firewall:

| Port | Protocol | Purpose |
|------|----------|---------|
| 2302 | UDP | Game traffic |
| 2303 | UDP | Steam networking |
| 2304 | UDP | Steam query (internal) |
| 27016 | UDP | Steam server browser query |

If you changed the base port with `-port=`, all other ports shift by the same offset.

### Firewall Blocking

Add **DayZServer_x64.exe** to your OS firewall exceptions. On Windows: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. On Linux, open the ports with `ufw` or `iptables`.

### Mod Mismatch

Clients must have the exact same mod versions as the server. If a player sees "Mod mismatch," either side has an outdated version. Update both when any mod receives a Workshop update.

### Missing .bikey Files

Every mod's `.bikey` file must be in the server's `keys/` directory. Without it, BattlEye rejects the client's signed PBOs. Look inside each mod's `keys/` or `key/` folder.

### Server Full

Check `maxPlayers` in **serverDZ.cfg** (default 60).

---

## Crashes and Null Pointers

### Null Pointer Access

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- the most common script error. A mod is calling a method on a deleted or uninitialized object. This is a mod bug, not a server misconfiguration. Report it to the mod author with the full RPT log.

### Finding Script Errors

Search the RPT log for `SCRIPT (E)`. The class and method name in the error tells you which mod is responsible. RPT locations:

- **Server:** `$profiles/` directory (or server root if no `-profiles=` is set)
- **Client:** `%localappdata%\DayZ\`

### Crash on Restart

If the server crashes on every restart, **storage_1/** may be corrupted. Stop the server, back up `storage_1/`, delete `storage_1/data/events.bin`, and restart. If that fails, delete the entire `storage_1/` directory (wipes all persistence).

### Crash After Mod Update

Revert to the previous mod version. Check the Workshop changelog for breaking changes -- renamed classes, removed configs, and changed RPC formats are common causes.

---

## Loot Not Spawning

### types.xml Not Registered

Items defined in **types.xml** will not spawn unless the file is registered in **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

If you use a custom types file (e.g. **types_custom.xml**), add a separate `<file>` entry for it.

### Wrong Category, Usage, or Value Tags

Every `<category>`, `<usage>`, and `<value>` tag in your types.xml must match a name defined in **cfglimitsdefinition.xml**. A typo like `usage name="Military"` (capital M) when the definition says `military` (lowercase) silently prevents the item from spawning.

### Nominal Set to Zero

If `nominal` is `0`, the CE will never spawn that item. This is intentional for items that should only exist via crafting, events, or admin placement. If you want the item to spawn naturally, set `nominal` to at least `1`.

### Missing Map Group Positions

Items need valid spawn positions inside buildings. If a custom item has no matching map group positions (defined in **mapgroupproto.xml**), the CE has nowhere to place it. Assign the item to categories and usages that already have valid positions on the map.

---

## Vehicles Not Spawning

Vehicles use the event system, **not** types.xml.

### events.xml Configuration

Vehicle spawns are defined in **events.xml**:

```xml
<event name="VehicleOffroadHatchback">
    <nominal>8</nominal>
    <min>5</min>
    <max>8</max>
    <lifetime>3888000</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="1" min="1" type="OffroadHatchback"/>
    </children>
</event>
```

### Missing Spawn Positions

Vehicle events with `<position>fixed</position>` require entries in **cfgeventspawns.xml**. Without defined coordinates, the event has nowhere to place the vehicle.

### Event Disabled

If `<active>0</active>`, the event is completely disabled. Set it to `1`.

### Damaged Vehicles Blocking Slots

If `remove_damaged="0"`, destroyed vehicles remain in the world forever and occupy spawn slots. Set `remove_damaged="1"` so the CE cleans up wrecks and spawns replacements.

---

## Persistence Issues

### Bases Disappearing

Territory flags must be refreshed before their timer expires. The default `FlagRefreshFrequency` is `432000` seconds (5 days). If no player interacts with the flag within that window, the flag and all objects within its radius are deleted.

Check the value in **globals.xml**:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Increase this value on low-population servers where players log in less frequently.

### Items Vanishing After Restart

Every item has a `lifetime` in **types.xml** (seconds). When it expires without player interaction, the CE removes it. Reference: `3888000` = 45 days, `604800` = 7 days, `14400` = 4 hours. Items inside containers inherit the container's lifetime.

### storage_1/ Growing Too Large

If your `storage_1/` directory grows beyond several hundred MB, your economy is producing too many items. Reduce `nominal` values across your types.xml, especially for high-count items like food, clothing, and ammunition. A bloated persistence file causes longer restart times.

### Player Data Lost

Player inventories and positions are stored in `storage_1/players/`. If this directory is deleted or corrupted, all players spawn fresh. Back up `storage_1/` regularly.

---

## Performance Problems

### Server FPS Dropping

DayZ servers target 30+ FPS for smooth gameplay. Common causes of low server FPS:

- **Too many zombies** -- reduce `ZombieMaxCount` in **globals.xml** (default 800, try 400-600)
- **Too many animals** -- reduce `AnimalMaxCount` (default 200, try 100)
- **Excessive loot** -- lower `nominal` values across your types.xml
- **Too many base objects** -- large bases with hundreds of items strain persistence
- **Heavy script mods** -- some mods run expensive per-frame logic

### Desync

Players experiencing rubber-banding, delayed actions, or invisible zombies are symptoms of desync. This almost always means server FPS has dropped below 15. Fix the underlying performance problem rather than looking for a desync-specific setting.

### Long Restart Times

Restart time is directly proportional to the size of `storage_1/`. If restarts take more than 2-3 minutes, you have too many persistent objects. Reduce loot nominal values and set appropriate lifetimes.

---

## Reading Log Files

### Server RPT Location

The RPT file is in `$profiles/` (if launched with `-profiles=`) or the server root. Filename pattern: `DayZServer_x64_<date>_<time>.RPT`.

### What to Search For

| Search term | Meaning |
|-------------|---------|
| `SCRIPT (E)` | Script error -- a mod has a bug |
| `[ERROR]` | Engine-level error |
| `ErrorMessage` | Fatal error that may cause shutdown |
| `Cannot open` | Missing file (PBO, config, mission) |
| `Crash` | Application-level crash |

### BattlEye Logs

BattlEye logs are in the `BattlEye/` directory within your server root. These show kick and ban events. If players report being kicked unexpectedly, check here first.

---

## Quick Diagnostic Checklist

When something goes wrong, work through this list in order:

```
1. Check the server RPT for SCRIPT (E) and [ERROR] lines
2. Verify every -mod= path exists and contains addons/*.pbo
3. Verify all .bikey files are copied to keys/
4. Check serverDZ.cfg for syntax errors (missing semicolons)
5. Check port forwarding: 2302 UDP + 27016 UDP
6. Verify mission folder matches the template value in serverDZ.cfg
7. Check storage_1/ for corruption (delete events.bin if needed)
8. Test with zero mods first, then add mods one at a time
```

Step 8 is the most powerful technique. If the server works vanilla but breaks with mods, you can isolate the problem mod through binary search -- add half your mods, test, then narrow down.

---

[Home](../README.md) | [<< Previous: Mod Management](10-mod-management.md) | [Next: Advanced Topics >>](12-advanced.md)
