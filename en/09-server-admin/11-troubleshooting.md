# Server Troubleshooting


---

> **Summary:** A symptom index for the most common DayZ **server operations** problems -- startup failures, connection issues, crashes, loot and vehicle spawning, persistence, and performance. Find your symptom, run the first-aid check, then follow the link to the chapter that owns the full fix.

> **Scope:** This chapter is for **running a server**. For problems inside **mod code** -- script errors, RPC, UI, PBO builds -- see the mod-development [Troubleshooting Guide](../troubleshooting.md).

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

If `DayZServer_x64.exe` crashes immediately with a missing DLL error, install the current **Microsoft Visual C++ Redistributable for Visual Studio 2015-2022 (x64)** from [Microsoft's download page](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist) and restart. Microsoft distributes 2015-2022 as one package, so do not go looking for a standalone 2019 build.

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

DayZ needs these UDP ports forwarded and open in your firewall:

| Port | Protocol | Purpose |
|------|----------|---------|
| 2302 | UDP | Main game traffic |
| 2303-2304 | UDP | Steam networking |
| 2305 | UDP | Steam query port — the value in Bohemia's sample config (`steamQueryPort = 2305`) and the conventional choice |

Forwarding the whole **2302-2305** block off the base port is long-standing admin practice and the advice here, but treat it as convention rather than an engine guarantee: Bohemia documents `-port=` as the port the server listens on and shows `clientPort = 2304` and `steamQueryPort = 2305` as sample values, and publishes no statement that a four-port block is reserved or that it shifts with `-port=`. The dependable approach is to set `steamQueryPort` (and `clientPort`, if you use it) explicitly and forward exactly what you set.

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

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- the most common script error. A mod is calling a method on a deleted or uninitialized object. This is a mod bug, not a server misconfiguration. Report it to the mod author with the full `script_*.log`.

### Finding Script Errors

Script errors land in the `script_*.log`, **not** the `.RPT`. Search that file for `SCRIPT (E)`; the class and method name tells you which mod is responsible. Log locations:

- **Server:** the `profiles/` directory (set with `-profiles=`, otherwise the server root)
- **Client:** `%localappdata%\DayZ\`

Engine-level failures -- missing addons, signature errors, hard crashes -- go in the `.RPT` instead. See [Reading Log Files](#reading-log-files).

### Crash on Restart

If the server crashes on every restart, **storage_1/** may be corrupted. Stop the server and back up `storage_1/` first. A widely used community first step is to delete `storage_1/data/events.bin` and restart -- the file itself is first-party: Bohemia documents the `save_events_startup` default in `cfgeconomycore.xml` as *"If disabled, no `data/events.bin` is created at startup"*, so the server recreates it. That deletion is **community recovery practice, not a documented Bohemia procedure**, and it discards saved dynamic-event state. If it does not help, delete the entire `storage_1/` directory (wipes all persistence). See [World State & Persistence](07-persistence.md) for a safe recovery routine, and [Loot Economy Deep Dive](04-loot-economy.md#persistence-backups-and-world-segments) for the startup-dump and backup defaults.

### Crash After Mod Update

Revert to the previous mod version. Check the Workshop changelog for breaking changes -- renamed classes, removed configs, and changed RPC formats are common causes.

---

## Loot Not Spawning

Loot lives in the central economy (CE). Most "it won't spawn" cases are a registration or tag mismatch, not a missing item.

| Symptom | Likely cause | First-aid check |
|---------|-------------|-----------------|
| A custom item never appears anywhere | types file not registered in **cfgeconomycore.xml** | Confirm a `<file name="..." type="types" />` entry exists for your file |
| One item is absent, the rest spawn fine | Category / usage / value tag mismatch | Tags in types.xml must match **cfglimitsdefinition.xml** names exactly (case-sensitive: `Military`, not `military`) |
| Item is registered but count stays at zero | `nominal` is `0` | Set `nominal` to at least `1` for natural spawning |
| Item loads with no errors but still absent | No matching map group positions | Assign categories/usages that already have positions in **mapgroupproto.xml** |

**First-aid:** search the `script_*.log` at boot for CE load lines and any complaint about your economy files. A rejected types file logs an error there.

Full field-by-field walkthrough of `cfgeconomycore.xml`, tag definitions, `nominal`/`min`/`lifetime` tuning, and map group positions: see [Loot Economy Deep Dive](04-loot-economy.md).

---

## Vehicles Not Spawning

Vehicles use the **event system**, not types.xml.

| Symptom | Likely cause | First-aid check |
|---------|-------------|-----------------|
| No vehicles anywhere | Event set to `<active>0</active>` | Set the event to `<active>1</active>` in **events.xml** |
| Event active but no vehicles appear | Missing spawn coordinates | `<position>fixed</position>` events need entries in **cfgeventspawns.xml** |
| Vehicle count drops over time and never recovers | Wrecks occupy slots | Set `remove_damaged="1"` so the CE cleans up destroyed vehicles |

**First-aid:** confirm the event name in `events.xml` matches the name referenced in `cfgeventspawns.xml` exactly.

Full event structure (`nominal`/`min`/`max`, radii, children, spawn coordinates) is covered in [Vehicle & Dynamic Event Spawning](05-vehicle-spawning.md).

---

## Persistence Issues

| Symptom | Likely cause | First-aid check |
|---------|-------------|-----------------|
| Bases and stored objects disappear | Territory flag's refresh budget ran out | Check `FlagRefreshMaxDuration` in **globals.xml** (vanilla `3456000` = 40 days). That is the budget a raised flag holds; once it is spent the flag stops refreshing item lifetimes and the parts in its radius become eligible for cleanup as their own lifetimes expire. `FlagRefreshFrequency` (vanilla `432000` = 5 days) is the automatic refresh interval, not a player deadline -- see [World State & Persistence](07-persistence.md#territory-flags-and-base-decay) |
| Items vanish after a restart | `lifetime` expired | Each item has a `lifetime` (seconds) in **types.xml**; container contents inherit the container's lifetime |
| `storage_1/` grows very large | Too many economy items | Reduce `nominal` values, especially food, clothing, and ammunition |
| All players spawn fresh | Player data lost | Player inventories live in `storage_1/players/`; back up `storage_1/` regularly |

**First-aid:** never edit persistence files while the server is running -- it will overwrite your changes on the next save.

Lifetime reference values, flag refresh tuning, and safe `storage_1/` maintenance are covered in [World State & Persistence](07-persistence.md).

---

## Performance Problems

| Symptom | Likely cause | First-aid check |
|---------|-------------|-----------------|
| Low server FPS (30+ is the commonly cited target -- a community rule of thumb, not an engine-documented threshold) | Too many entities or heavy loot | Reduce `ZombieMaxCount` and `AnimalMaxCount` in **globals.xml**; lower `nominal` values |
| Rubber-banding, delayed actions, invisible zombies (desync) | Low server FPS -- admins consistently report this below roughly 15, which is also where Bohemia's `serverFpsWarning` sample sits, though Bohemia does not publish it as a playability threshold | Fix the underlying FPS problem -- there is no desync-specific setting |
| Restarts take longer than 2-3 minutes | Oversized `storage_1/` | Reduce loot nominals and set appropriate lifetimes to shrink persistence |

**First-aid:** watch server FPS in the admin console or a monitoring tool before changing settings, so you can measure the effect of each change. The FPS bands above are community rules of thumb; the qualified version, with the official `serverFpsWarning` facts, is in [Server Performance Tuning](08-performance.md#monitoring-server-health).

Default values, the entity/loot/persistence trade-offs, and a step-by-step tuning method are in [Performance Tuning](08-performance.md).

---

## Reading Log Files

### Server Log Locations

Both logs live in `profiles/` -- the directory passed to `-profiles=`, or the server root if that flag is unset:

- **`script_<date>_<time>.log`** -- script output and `SCRIPT (E)` errors. This is your primary debugging tool.
- **`DayZServer_x64_<date>_<time>.RPT`** -- the engine report: startup, crashes, missing addons, and signature failures.

### What to Search For

| Search term | Log | Meaning |
|-------------|-----|---------|
| `SCRIPT (E)` | script log | Script error -- a mod has a bug |
| `Cannot register` | RPT | Class-name collision between two mods |
| `Missing addons` | RPT | A dependency is not loaded (wrong load order or missing mod) |
| `Signature verification failed` | RPT | `.bikey` mismatch or missing key |
| `Cannot open` | RPT | Missing file (PBO, config, mission) |
| `Crash` | RPT | Application-level crash |

For mod-conflict diagnosis using these same logs, see [Mod Management](10-mod-management.md#troubleshooting-mod-conflicts).

### BattlEye Logs

BattlEye logs are in the `BattlEye/` directory within your server root. These show kick and ban events. If players report being kicked unexpectedly, check here first.

---

## Quick Diagnostic Checklist

When something goes wrong, work through this list in order:

```
1. Check the script_*.log for SCRIPT (E), and the .RPT for engine errors
2. Verify every -mod= path exists and contains addons/*.pbo
3. Verify all .bikey files are copied to keys/
4. Check serverDZ.cfg for syntax errors (missing semicolons)
5. Check port forwarding: the game port (2302 by default) plus whatever you set steamQueryPort to (conventionally 2305)
6. Verify mission folder matches the template value in serverDZ.cfg
7. Check storage_1/ for corruption (deleting data/events.bin is the common community first step -- the server recreates it at startup)
8. Test with zero mods first, then add mods one at a time
```

Step 8 is the most powerful technique. If the server works vanilla but breaks with mods, you can isolate the problem mod through binary search -- add half your mods, test, then narrow down.
