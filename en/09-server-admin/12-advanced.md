# Advanced Server Operations

> **Summary:** Operational tasks that go beyond a single-map vanilla server: running additional maps and custom map mods (Namalsk, Deer Isle), automating restarts safely, scheduling in-game messages via **messages.xml**, and populating the world with animal territories through **cfgenvironment.xml**. Deep-dives for **cfggameplay.json**, **cfgweather.xml**, economy file splitting, and custom dynamic events now live in their own reference chapters (linked below).

---

## Table of Contents

- [Multi-Map Servers](#multi-map-servers)
- [Custom Map Mods](#custom-map-mods)
- [Running Multiple Maps at Once](#running-multiple-maps-at-once)
- [cfgenvironment.xml and Animal Territories](#cfgenvironment-xml-and-animal-territories)
- [Server Restart Automation](#server-restart-automation)
- [Scheduled Messages](#scheduled-messages)
- [Moved Topics](#moved-topics)

---

## Multi-Map Servers

DayZ ships three official maps, each as its own mission folder inside `mpmissions/`:

| Map | Mission Folder |
|-----|---------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Every mission folder carries its own Central Economy files (`types.xml`, `events.xml`, `cfgeconomycore.xml`, and the rest). Switching maps means pointing the server at a different mission folder — the CE files come along with it.

Select the active mission with the `template` line in the `Missions` class of **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.enoch";
    };
};
```

Or override it on the command line, which wins over the config:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -mission=mpmissions/dayzOffline.enoch -port=2302
```

Only one mission template is active per running server process. To offer several maps, run several server instances (see [Running Multiple Maps at Once](#running-multiple-maps-at-once)).

---

## Custom Map Mods

Community terrains such as **Namalsk** and **Deer Isle** are distributed as regular DayZ mods plus a matching mission folder. Getting one online is a two-part job: load the map addon, then run a mission built for that terrain.

**1. Load the map mod.** Add the map addon to the server's `-mod` list, exactly like any other mod, and subscribe clients to the same addon so they can connect:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -mod=@Namalsk;@NamalskSurvival -port=2302
```

Load order follows the map's own documentation — a terrain and its gameplay companion addon usually ship together, and the companion is loaded after the terrain.

**2. Use a mission built for that world.** A terrain mod cannot use the Chernarus mission — the mission folder name encodes the world it belongs to. The map author supplies a starter mission; copy it into `mpmissions/` and point `template` at it:

```cpp
class Missions {
    class DayZ {
        template = "regular.namalsk";
    };
};
```

Common community mission folder names look like `regular.namalsk`, `hardcore.namalsk`, and `empty.deerisle`. Always take the exact folder name from the map mod's release notes rather than guessing — the suffix after the dot must match the terrain's world name, and the server refuses to load a mission whose world it cannot resolve.

**3. Regenerate persistence on the first boot.** A custom map has its own storage layout. When you switch to a new terrain, wipe (or move aside) the old `storage_*` folder so the Central Economy rebuilds it for the new world. Skipping this step is the most common cause of a custom-map server that boots but spawns no loot.

When updating a map mod, expect the mission's CE files to change between versions. Merge your customizations into the new mission folder instead of overwriting the author's files wholesale.

---

## Running Multiple Maps at Once

A single server process serves one map. To host, say, Chernarus and Livonia together, run two independent instances. Each needs its own:

- **config file** — a separate `serverDZ.cfg` with its own `hostname` and `template`
- **profile directory** — pass a distinct `-profiles=` path so logs and bans do not collide
- **port range** — the game port and the Steam query/RCON ports must not overlap

```batch
start "" DayZServer_x64.exe -config=cherno.cfg  -profiles=P:\cherno  -port=2302
start "" DayZServer_x64.exe -config=livonia.cfg -profiles=P:\livonia -port=2402
```

Steam reserves the game port plus the next few ports for queries, so leave a gap (2302, 2402, …) rather than using adjacent numbers. The two instances share the same DayZ install and the same mods — only the mission, config, profile, and ports differ.

---

## cfgenvironment.xml and Animal Territories

The file **cfgenvironment.xml** in your mission folder maps territory files in the `env/` subdirectory to animal behaviors. Each animal group is a `<territory>` element with a `<file usable="..." />` child, referenced by name without the `env/` prefix or `.xml` extension:

The root `<env>` element holds a single `<territories>` wrapper. Inside it, first declare every territory file with a `<file path="env/x.xml" />` line, then list the `<territory>` mappings:

```xml
<env>
    <territories>
        <file path="env/red_deer_territories.xml" />
        <file path="env/wolf_territories.xml" />
        <file path="env/bear_territories.xml" />

        <territory type="Herd" name="Deer" behavior="DZDeerGroupBeh">
            <file usable="red_deer_territories" />
        </territory>
        <territory type="Herd" name="Wolf" behavior="DZWolfGroupBeh">
            <file usable="wolf_territories" />
        </territory>
        <territory type="Herd" name="Bear" behavior="BlissBearGroupBeh">
            <file usable="bear_territories" />
        </territory>
    </territories>
</env>
```

The `<file path="..." />` declarations use the full `env/…​.xml` path, while the `<file usable="..." />` child inside each `<territory>` references the same file by name only (no `env/` prefix, no `.xml`).

The `env/` folder contains the animal territory files themselves:

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
| **domestic_animals_territories.xml** | Mixed domestic animals |
| **zombie_territories.xml** | Infected (not an animal file, but it lives in `env/` and uses the same schema) |

A territory entry defines circular zones, grouped under a `<territory>` element by color (not by name -- vanilla `<territory>` elements carry only a `color` attribute):

```xml
<territory color="4294923520">
    <zone name="Graze" smin="0" smax="0" dmin="0" dmax="0" x="1920" z="13115" r="100"/>
    <zone name="Graze" smin="0" smax="0" dmin="0" dmax="0" x="2085" z="13415" r="200"/>
</territory>
```

- `x`, `z` -- zone center coordinates; `r` -- radius in meters
- `name` (on `<zone>`) -- a behavior/role label for that zone, not a per-animal description. Every `<zone>` in every vanilla file carries all eight attributes: `name`, `smin`, `smax`, `dmin`, `dmax`, `x`, `z`, `r`.
- `smin`, `smax`, `dmin`, `dmax` -- four integer counts. Vanilla does set them to non-zero values, so they are a live tuning knob, not a reserved field. What the engine does with them is a separate question -- see below.

#### What the vanilla files actually contain

Counted across all 13 `env/` files of Chernarus in the local extraction, and cross-checked against all 39 `env/` files across the seven mission folders that contain one -- the three `dayzOffline` missions (Chernarus 13, Livonia 13, Sakhal 8) and four Halloween folders (`halloween.chernarusplus` 2, and one file each in `halloweenOffline.chernarusplus`, `.enoch` and `.sakhal`) -- in Bohemia's [DayZ-Central-Economy](https://github.com/BohemiaInteractive/DayZ-Central-Economy) repository at commit `9a21bb9` (2026-08-13) -- 817 `<territory>` elements and 10,665 `<zone>` elements in total:

- **`<territory>` carries a `color` attribute and nothing else.** All 817 of them. No vanilla `<territory>` has a `name`.
- **Zone labels come from a small per-file vocabulary, not free text.** 29 distinct values across all missions, and each file draws from its own short set:

| File group | Zone `name` values used |
|------------|------------------------|
| Grazing animals (cattle, domestic_animals, pig, red_deer, roe_deer, sheep_goat, wild_boar) | `Graze`, `Rest`, `Water` (`sheep_goat` uses only `Graze` and `Rest`) |
| `bear_territories.xml` | `Graze` only -- all 71 Chernarus zones |
| `wolf_territories.xml` | `HuntingGround`, `Rest`, `Water` |
| `fox`, `hare`, `hen` | `Zone_fox`, `Zone_Hare`, `Zone_hen` -- one label per file, and the casing is inconsistent between missions (`Zone_Fox` and `Zone_hare` also occur) |
| `zombie_territories.xml` | 15 `Infected*` labels on Chernarus, including `InfectedVillage`, `InfectedSolitude`, `InfectedCityTier1`, `InfectedVillageTier1`, `InfectedIndustrial`, `InfectedArmy`, `InfectedArmyHard`, `InfectedMedic`, `InfectedPolice`, `InfectedNBC` |

  Because `Zone_fox` is just the species name and the casing varies between files, these labels are **not** demonstrably a fixed engine-recognised vocabulary. Treat an existing label as the safe choice rather than inventing one.

- **The four counts are non-zero in vanilla.** On Chernarus, `fox`, `hare` and `hen` set `dmax="2"` on every one of their 1,621 zones, and `zombie_territories.xml` uses `dmin` 1-15 and `dmax` 2-20 across its 768 zones, with `smin` up to 8 and `smax` up to 10 on a handful of high-value military and NBC zones. Across all missions in the official repository the ranges widen to `dmin` 1-30 and `dmax` 1-40. Every other Chernarus file leaves all four at `0`.

#### What the counts mean

Unresolved, and deliberately left that way. The pattern is *consistent with* the widely repeated reading -- `s` for a static minimum/maximum and `d` for a dynamic minimum/maximum population for the zone -- and a zone like `<zone name="InfectedArmyHard" smin="6" smax="8" dmin="8" dmax="12" .../>` reads naturally that way. But:

- Nothing in the 2,800-file vanilla Enforce Script tree references `smin`, `smax`, `dmin` or `dmax`. These files are parsed entirely engine-side, so there is no script implementation to read.
- Bohemia has published no description of these attributes.

So: the values are real and you can change them, but this wiki will not tell you exactly what the engine does with a given number. Change one at a time on a test server and observe.

When you build a custom map's animal population, add one territory file per species, register each in **cfgenvironment.xml**, and place zones on the terrain that actually has the ground cover those animals expect.

---

## Server Restart Automation

DayZ has no built-in restart scheduler. Restarts are driven from outside the game by an OS-level task that stops the server, backs up persistence, checks for updates, and relaunches.

### Windows

Create **restart_server.bat** and run it from a Windows Scheduled Task every 4-6 hours:

```batch
@echo off
rem A plain "taskkill" (no /f) requests a graceful close so the engine can
rem run its shutdown save. Do NOT add /f here -- a forced kill is exactly
rem the "killed process" case World State & Persistence warns loses
rem everything since the last timed save.
taskkill /im DayZServer_x64.exe
timeout /t 30

rem Build a locale-independent timestamp (yyyy-MM-dd_HHmm) via PowerShell.
rem Do NOT slice %date% by character offset -- its layout changes with the
rem machine's regional settings and the backup path will silently break.
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmm"') do set STAMP=%%i

rem storage_1/ lives inside the mission folder, not profiles/ -- see
rem Directory Structure & Mission Folder and World State & Persistence.
xcopy /e /i /y "C:\DayZServer\mpmissions\dayzOffline.chernarusplus\storage_1" "C:\DayZBackups\%STAMP%\storage_1\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login your_steam_username +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

> **Why not `%date:~-4%`?** The classic trick of slicing `%date%` by character offset assumes a fixed layout, but `%date%` is formatted from Windows regional settings. On a machine set to `dd/MM/yyyy` the same slice produces a different (or invalid) folder name, and the backup lands somewhere you never look. Asking PowerShell for `Get-Date -Format yyyy-MM-dd_HHmm` returns the same string on every machine regardless of locale.
>
> **Why not `taskkill /f`?** `/f` sends a forced termination, giving the engine no chance to run its shutdown save -- see [When the Server Saves](07-persistence.md#when-the-server-saves). A plain `taskkill` requests a graceful close first. If the process is still running after the timeout, that is a sign something hung and needs investigating, not a reason to reach for `/f` as routine practice.

### Linux

Create a shell script and add it to cron (`0 */4 * * *` runs it every four hours):

```bash
#!/bin/bash
# Plain `kill` sends SIGTERM, which the engine treats as a graceful shutdown
# request (unlike `kill -9`/SIGKILL). Give it time to actually exit before
# copying or updating anything.
kill $(pidof DayZServer)
while pidof DayZServer > /dev/null; do sleep 2; done

# storage_1/ lives inside the mission folder, not profiles/ -- see
# Directory Structure & Mission Folder and World State & Persistence.
cp -r /home/dayz/server/mpmissions/dayzOffline.chernarusplus/storage_1 "/home/dayz/backups/$(date +%F_%H%M)_storage_1"
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login your_steam_username +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

> **Unattended logins:** DayZ Server's depot (app 223350) does not accept `+login anonymous` -- both scripts above need a real, authenticated Steam account (see [Installing DayZ Server](01-server-setup.md#installing-dayz-server) for what is and isn't confirmed about the ownership requirement). For a scheduled task to run unattended, cache that account's SteamCMD login first (run `steamcmd.exe +login your_steam_username` once interactively and complete Steam Guard) so subsequent non-interactive runs reuse the cached credentials instead of hanging on a password prompt.

Always back up `storage_1/` **before** each restart. Persistence corrupted during an unclean shutdown can wipe player bases and vehicles, and a pre-restart backup is the only way back. Pair the restart schedule with the warning broadcasts in the next section so players are not caught mid-action.

---

## Scheduled Messages

The file **db/messages.xml** in your mission folder controls scheduled server broadcasts and the countdown warnings shown before a restart:

Each `<message>` carries its settings as **child elements**, not attributes. A shutdown countdown message uses `<deadline>` (measured in **minutes** from server start) plus `<shutdown>1</shutdown>`; a repeating broadcast uses `<repeat>` (interval in minutes) with optional `<delay>` and `<onconnect>`:

```xml
<messages>
    <message>
        <deadline>360</deadline>
        <shutdown>1</shutdown>
        <text>#name will shutdown in #tmin minutes.</text>
    </message>
    <message>
        <repeat>15</repeat>
        <text>Welcome to the server! Back up your loadout before the restart.</text>
    </message>
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>Welcome to #name — restarts run every 6 hours.</text>
    </message>
</messages>
```

- `<deadline>` -- for a shutdown message, the number of **minutes** after server start at which it stops (so `360` = 6 hours). The engine shows the countdown automatically.
- `<shutdown>` -- `1` marks the message as a shutdown timer; omit it (or set `0`) for a normal broadcast.
- `<repeat>` -- interval in minutes at which a non-shutdown message is re-broadcast.
- `<delay>` -- minutes to wait before the first broadcast; with `<onconnect>1</onconnect>` the delay is counted from each player's connection.
- Tokens such as `#name` (server name) and `#tmin` (minutes remaining) are substituted at runtime.

The messages system **does** stop the server when a `<deadline>` elapses, and it displays the warnings on the way there. Set the `<deadline>` to match the interval of your external restart task (from [Server Restart Automation](#server-restart-automation)) so the on-screen countdown ends exactly when the OS task relaunches the process.

> **Linux reliability note:** community bug reports on the Bohemia feedback tracker describe cases where a Linux server logs the shutdown event from a `messages.xml` deadline but the process does not fully terminate. Do not treat the in-game countdown as your only shutdown mechanism -- keep the OS-level `kill`/scheduled-task step from [Server Restart Automation](#server-restart-automation) as the authoritative way to actually stop the process, and use `messages.xml` for the player-facing warning only.

---

## Moved Topics

Several deep-dives that once lived here now have dedicated homes:

- **cfggameplay.json** (stamina, shock, movement, base-building rules) and **cfgweather.xml** — see [World Configuration Systems](../06-engine-api/23-world-systems.md).
- **Splitting types.xml and custom categories/tags** (`cfgeconomycore.xml`, `cfglimitsdefinitionuser.xml`) — see [Loot Economy Deep Dive](04-loot-economy.md).
- **Custom dynamic events** (`events.xml`, `cfgeventspawns.xml`, `cfgeventgroups.xml`) — see [Vehicle & Dynamic Event Spawning](05-vehicle-spawning.md).
