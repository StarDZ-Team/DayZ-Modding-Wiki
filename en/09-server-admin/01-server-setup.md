# Chapter 9.1: Server Setup & First Launch

[Home](../README.md) | **Server Setup** | [Next: Directory Structure >>](02-directory-structure.md)

---

> **Summary:** Install a DayZ Standalone dedicated server from scratch using SteamCMD, launch it with a minimal configuration, verify it appears in the server browser, and connect as a player. This chapter covers everything from hardware requirements to fixing the most common first-launch failures.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installing SteamCMD](#installing-steamcmd)
- [Installing DayZ Server](#installing-dayz-server)
- [Directory After Install](#directory-after-install)
- [First Launch with Minimal Config](#first-launch-with-minimal-config)
- [Verifying the Server is Running](#verifying-the-server-is-running)
- [Connecting as a Player](#connecting-as-a-player)
- [Common First-Launch Problems](#common-first-launch-problems)

---

## Prerequisites

### Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores, 2.4 GHz | 6+ cores, 3.5 GHz |
| RAM | 8 GB | 16 GB |
| Disk | 20 GB SSD | 40 GB NVMe SSD |
| Network | 10 Mbps upload | 50+ Mbps upload |
| OS | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

DayZ Server is single-threaded for gameplay logic. Clock speed matters more than core count.

### Software

- **SteamCMD** -- the Steam command-line client for installing dedicated servers
- **Visual C++ Redistributable 2019** (Windows) -- required by `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- usually already present
- Ports **2302-2305 UDP** forwarded on your router/firewall

---

## Installing SteamCMD

### Windows

1. Download SteamCMD from https://developer.valvesoftware.com/wiki/SteamCMD
2. Extract `steamcmd.exe` to a permanent folder, e.g. `C:\SteamCMD\`
3. Run `steamcmd.exe` once -- it will update itself automatically

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## Installing DayZ Server

DayZ Server's Steam App ID is **223350**. You can install it without logging into a Steam account that owns DayZ.

### One-Line Install (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### One-Line Install (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Update Script

Create a script you can re-run whenever a patch drops:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Update complete.
pause
```

The `validate` flag checks every file for corruption. On a fresh install, expect a 2-3 GB download.

---

## Directory After Install

After installation, the server root looks like this:

```
DayZServer/
  DayZServer_x64.exe        # The server executable
  serverDZ.cfg               # Main server configuration
  dayzsetting.xml            # Rendering/video settings (not relevant for dedicated)
  addons/                    # Vanilla PBO files (ai.pbo, animals.pbo, etc.)
  battleye/                  # BattlEye anti-cheat (BEServer_x64.dll)
  dta/                       # Core engine data (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Signature keys (dayz.bikey for vanilla)
  logs/                      # Engine logs (connection, content, audio)
  mpmissions/                # Mission folders
    dayzOffline.chernarusplus/   # Chernarus mission
    dayzOffline.enoch/           # Livonia mission (DLC)
    dayzOffline.sakhal/          # Sakhal mission (DLC)
  profiles/                  # Runtime output: RPT logs, script logs, player DB
  ban.txt                    # Banned player list (Steam64 IDs)
  whitelist.txt              # Whitelisted players (Steam64 IDs)
  steam_appid.txt            # Contains "221100"
```

Key points:
- **You edit** `serverDZ.cfg` and files inside `mpmissions/`.
- **You never edit** files in `addons/` or `dta/` -- they are overwritten on every update.
- **Mod PBOs** go into the server root or a subfolder (covered in a later chapter).
- **`profiles/`** is created on first launch and contains your script logs and crash dumps.

---

## First Launch with Minimal Config

### Step 1: Edit serverDZ.cfg

Open `serverDZ.cfg` in a text editor. For a first test, use the simplest possible config:

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### Step 2: Launch the Server

Open a Command Prompt in the server directory and run:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Flag | Purpose |
|------|---------|
| `-config=serverDZ.cfg` | Path to config file |
| `-port=2302` | Main game port (also uses 2303-2305) |
| `-profiles=profiles` | Output folder for logs and player data |
| `-dologs` | Enable server logging |
| `-adminlog` | Log admin actions |
| `-netlog` | Log network events |
| `-freezecheck` | Auto-restart on freeze detection |

### Step 3: Wait for Initialization

The server takes 30-90 seconds to fully start. Watch the console output. When you see a line like:

```
BattlEye Server: Initialized (v1.xxx)
```

...the server is ready for connections.

---

## Verifying the Server is Running

### Method 1: Script Log

Check `profiles/` for a file named like `script_YYYY-MM-DD_HH-MM-SS.log`. Open it and look for:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

These lines confirm the economy initialized and the mission loaded.

### Method 2: RPT File

The `.RPT` file in `profiles/` shows engine-level output. Look for:

```
Dedicated host created.
BattlEye Server: Initialized
```

### Method 3: Steam Server Browser

Open Steam, go to **View > Game Servers > Favorites**, click **Add a Server**, enter `127.0.0.1:2302` (or your public IP), and click **Find games at this address**. If the server appears, it is running and reachable.

### Method 4: Query Port

Use an external tool like https://www.battlemetrics.com/ or the `gamedig` npm package to query port 27016 (Steam query port = game port + 24714).

---

## Connecting as a Player

### From the Same Machine

1. Launch DayZ (not DayZ Server -- the regular game client)
2. Open the **Server Browser**
3. Go to the **LAN** tab or **Favorites** tab
4. Add `127.0.0.1:2302` to favorites
5. Click **Connect**

If running client and server on the same machine, use `DayZDiag_x64.exe` (the diagnostic client) instead of the retail client. Launch with:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### From Another Machine

Use your server's **public IP** or **LAN IP** depending on whether the client is on the same network. The ports 2302-2305 UDP must be forwarded.

---

## Common First-Launch Problems

### Server Starts But Immediately Closes

**Cause:** Missing Visual C++ Redistributable or a syntax error in `serverDZ.cfg`.

**Fix:** Install VC++ Redist 2019 (x64). Check `serverDZ.cfg` for missing semicolons -- every parameter line must end with `;`.

### "BattlEye initialization failed"

**Cause:** The `battleye/` folder is missing or antivirus is blocking `BEServer_x64.dll`.

**Fix:** Re-validate the server files via SteamCMD. Add an antivirus exception for the entire server folder.

### Server Runs But Does Not Appear in Browser

**Cause:** Ports not forwarded, or Windows Firewall blocking the executable.

**Fix:**
1. Add a Windows Firewall inbound rule for `DayZServer_x64.exe` (allow all UDP)
2. Forward ports **2302-2305 UDP** on your router
3. Check with an external port checker that 2302 UDP is open on your public IP

### "Version Mismatch" When Connecting

**Cause:** Server and client are on different versions.

**Fix:** Update both. Run the SteamCMD update command for the server. The client updates automatically through Steam.

### No Loot Spawning

**Cause:** The `init.c` file is missing or the Hive failed to initialize.

**Fix:** Verify `mpmissions/dayzOffline.chernarusplus/init.c` exists and contains `CreateHive()`. Check the script log for errors.

### Server Uses 100% of One CPU Core

This is normal. DayZ Server is single-threaded. Do not run multiple server instances on the same core -- use processor affinity or separate machines.

### Players Spawn as Crows / Stuck in Loading

**Cause:** The mission template in `serverDZ.cfg` does not match an existing folder in `mpmissions/`.

**Fix:** Check the template value. It must exactly match a folder name:

```cpp
template = "dayzOffline.chernarusplus";  // Must match mpmissions/ folder name
```

---

**[Home](../README.md)** | **Next:** [Directory Structure >>](02-directory-structure.md)
