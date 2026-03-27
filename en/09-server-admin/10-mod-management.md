# Chapter 9.10: Mod Management

[Home](../README.md) | [<< Previous: Access Control](09-access-control.md) | [Next: Troubleshooting >>](11-troubleshooting.md)

---

> **Summary:** Install, configure, and maintain third-party mods on a DayZ dedicated server. Covers launch parameters, Workshop downloads, signature keys, load order, server-only vs client-required mods, updates, and the most common mistakes that cause crashes or player kicks.

---

## Table of Contents

- [How Mods Load](#how-mods-load)
- [Launch Parameter Format](#launch-parameter-format)
- [Workshop Mod Installation](#workshop-mod-installation)
- [Mod Keys (.bikey)](#mod-keys-bikey)
- [Load Order and Dependencies](#load-order-and-dependencies)
- [Server-Only vs Client-Required Mods](#server-only-vs-client-required-mods)
- [Updating Mods](#updating-mods)
- [Troubleshooting Mod Conflicts](#troubleshooting-mod-conflicts)
- [Common Mistakes](#common-mistakes)

---

## How Mods Load

DayZ loads mods through the `-mod=` launch parameter. Each entry is a path to a folder containing PBO files and a `config.cpp`. The engine reads every PBO in each mod folder, registers its classes and scripts, then continues to the next mod in the list.

Server and client must have the same mods in `-mod=`. If the server lists `@CF;@MyMod` and the client only has `@CF`, the connection fails with a signature mismatch. Server-only mods placed in `-servermod=` are the exception -- clients never need those.

---

## Launch Parameter Format

A typical modded server launch command:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Parameter | Purpose |
|-----------|---------|
| `-mod=` | Mods required by both server and all connecting clients |
| `-servermod=` | Server-only mods (clients do not need them) |

Rules:
- Paths are **semicolon-separated** with no spaces around the semicolons
- Each path is relative to the server root directory (e.g., `@CF` means `<server_root>/@CF/`)
- You can use absolute paths: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **Order matters** -- dependencies must appear before the mods that need them

---

## Workshop Mod Installation

### Step 1: Download the Mod

Use SteamCMD with the DayZ **client** App ID (221100) and the mod's Workshop ID:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

Downloaded files land in:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Step 2: Create a Symlink or Copy

Workshop folders use numeric IDs, which are unusable in `-mod=`. Create a named symlink (recommended) or copy the folder:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Using a junction means updates via SteamCMD automatically apply -- no re-copying required.

### Step 3: Copy the .bikey

See the next section.

---

## Mod Keys (.bikey)

Every signed mod ships with a `keys/` folder containing one or more `.bikey` files. These files tell BattlEye which PBO signatures to accept.

1. Open the mod folder (e.g., `@CF/keys/`)
2. Copy every `.bikey` file into the server's root `keys/` directory

```
DayZServer/
  keys/
    dayz.bikey              # Vanilla -- always present
    cf.bikey                # Copied from @CF/keys/
    vpp_admintools.bikey    # Copied from @VPPAdminTools/keys/
```

Without the correct key, any player running that mod gets: **"Player kicked: Modified data"**.

---

## Load Order and Dependencies

Mods load left-to-right in the `-mod=` parameter. A mod's `config.cpp` declares its dependencies:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

If `MyMod` requires `CF`, then `@CF` must appear **before** `@MyMod` in the launch parameter:

```
-mod=@CF;@MyMod          ✓ correct
-mod=@MyMod;@CF          ✗ crash or missing classes
```

**General load order pattern:**

1. **Framework mods** -- CF, Community-Online-Tools
2. **Library mods** -- BuilderItems, any shared asset pack
3. **Feature mods** -- map additions, weapons, vehicles
4. **Dependent mods** -- anything that lists the above as `requiredAddons`

When in doubt, check the mod's Workshop page or documentation. Most mod authors publish their required load order.

---

## Server-Only vs Client-Required Mods

| Parameter | Who needs it | Typical examples |
|-----------|-------------|------------------|
| `-mod=` | Server + all clients | Weapons, vehicles, maps, UI mods, clothing |
| `-servermod=` | Server only | Economy managers, logging tools, admin backends, scheduler scripts |

The rule is straightforward: if a mod contains **any** client-side scripts, layouts, textures, or models, it must go in `-mod=`. If it only runs server-side logic with no assets the client ever touches, use `-servermod=`.

Putting a server-only mod in `-mod=` forces every player to download it. Putting a client-required mod in `-servermod=` causes missing textures, broken UI, or script errors on the client.

---

## Updating Mods

### Procedure

1. **Stop the server** -- updating files while the server is running can corrupt PBOs
2. **Re-download** via SteamCMD:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Copy updated .bikey files** -- mod authors occasionally rotate their signing keys. Always copy the fresh `.bikey` from the mod's `keys/` folder to the server's `keys/` directory
4. **Restart the server**

If you used symlinks (junctions), step 2 updates the mod files in place. If you copied files manually, you must copy them again.

### Client-Side Updates

Players subscribed to the mod on Steam Workshop receive updates automatically. If you update a mod on the server and a player has the old version, they get a signature mismatch and cannot connect until their client updates.

---

## Troubleshooting Mod Conflicts

### Check the RPT Log

Open the latest `.RPT` file in `profiles/`. Search for:

- **"Cannot register"** -- a class name collision between two mods
- **"Missing addons"** -- a dependency is not loaded (wrong load order or missing mod)
- **"Signature verification failed"** -- `.bikey` mismatch or missing key

### Check the Script Log

Open the latest `script_*.log` in `profiles/`. Look for:

- **"SCRIPT (E)"** lines -- script errors, often caused by load order or version mismatch
- **"Definition of variable ... already exists"** -- two mods define the same class

### Isolate the Problem

When you have many mods and something breaks, test incrementally:

1. Start with only framework mods (`@CF`)
2. Add one mod at a time
3. Launch and check logs after each addition
4. The mod that causes errors is the culprit

### Two Mods Editing the Same Class

If two mods both use `modded class PlayerBase`, the one loaded **last** (rightmost in `-mod=`) wins. Its `super` call chains to the other mod's version. This usually works, but if one mod overrides a method without calling `super`, the other mod's changes are lost.

---

## Common Mistakes

**Wrong load order.** The server crashes or logs "Missing addons" because a dependency was not loaded yet. Fix: move the dependency mod earlier in the `-mod=` list.

**Forgetting `-servermod=` for server-only mods.** Players are forced to download a mod they do not need. Fix: move server-only mods from `-mod=` to `-servermod=`.

**Not updating `.bikey` files after a mod update.** Players get kicked with "Modified data" because the server's key does not match the mod's new PBO signatures. Fix: always re-copy `.bikey` files when updating mods.

**Repacking mod PBOs.** Re-packing a mod's PBO files breaks its digital signature, causes BattlEye kicks for every player, and violates most mod authors' terms. Never repack a mod you did not create.

**Mixing Workshop paths with local paths.** Using the raw Workshop numeric path for some mods and named folders for others causes confusion when updating. Pick one approach -- symlinks are the cleanest.

**Spaces in mod paths.** A path like `-mod=@My Mod` breaks parsing. Rename mod folders to avoid spaces, or wrap the entire parameter in quotes: `-mod="@My Mod;@CF"`.

**Outdated mod on server, updated on client (or vice versa).** Version mismatch prevents connection. Keep server and Workshop versions in sync. Update all mods and the server at the same time.

---

[Home](../README.md) | [<< Previous: Access Control](09-access-control.md) | [Next: Troubleshooting >>](11-troubleshooting.md)
