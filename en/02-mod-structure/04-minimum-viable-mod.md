# Anatomy of a Minimal Mod

---

> **Summary:** This chapter dissects the smallest structure DayZ will load as a script mod -- three files, zero dependencies -- and explains what every line is for. It is the reference companion to the hands-on tutorial: read this to understand *why* the skeleton looks the way it does.

---

> **Want to build it step by step?** The hands-on, start-to-finish walkthrough -- installing DayZ Tools, setting up the P: drive, packing with Addon Builder, launching, and verifying -- lives in [Your First Mod (Hello World)](../08-tutorials/01-first-mod.md). That tutorial is the place to *do* it; this chapter is the place to *understand* it.

---

## Table of Contents

- [The Three-File Skeleton](#the-three-file-skeleton)
- [File 1: mod.cpp -- Launcher Metadata](#file-1-mod-cpp-launcher-metadata)
- [File 2: config.cpp -- Engine Registration](#file-2-config-cpp-engine-registration)
- [File 3: The Script -- Hooking the Mission](#file-3-the-script-hooking-the-mission)
- [The Load Sequence](#the-load-sequence)
- [Where the Output Goes](#where-the-output-goes)
- [Testing Without Packing](#testing-without-packing)
- [Growing the Skeleton](#growing-the-skeleton)
- [Depending on a Framework](#depending-on-a-framework)
- [Troubleshooting Reference](#troubleshooting-reference)
- [Best Practices](#best-practices)
- [Theory vs Practice](#theory-vs-practice)

---

## The Three-File Skeleton

A working script mod needs exactly **three files**:

```
HelloMod/
  mod.cpp                       <-- launcher metadata
  Scripts/
    config.cpp                  <-- engine registration
    5_Mission/
      HelloMod/
        HelloMission.c          <-- your code
```

Each file answers a different question for a different consumer:

| File | Read by | Answers |
|------|---------|---------|
| `mod.cpp` | DayZ Launcher / Workshop | "What is this mod called and who made it?" |
| `config.cpp` | Engine (config loader) | "What does this PBO provide, and where are its scripts?" |
| `HelloMission.c` | Engine (script compiler) | "What code runs, and when?" |

The example mod used throughout this chapter -- **HelloMod** -- loads without errors and prints `[HelloMod] Mission started!` to the script log. It is the DayZ equivalent of "Hello World."

---

## File 1: mod.cpp -- Launcher Metadata

`HelloMod/mod.cpp`:

```cpp
name = "Hello Mod";
author = "YourName";
version = "1.0";
overview = "My first DayZ mod - prints a message on mission start.";
```

This is the minimum metadata. The DayZ Launcher shows "Hello Mod" in the mod list; the engine itself does not need this file to load your scripts, but the launcher and Workshop do. The full set of optional fields (logos, action URLs, credits) is covered in [mod.cpp & Workshop](03-mod-cpp.md).

Note where it lives: `mod.cpp` sits at the **mod root**, next to the `Addons/` folder in a packed mod -- never inside a PBO.

---

## File 2: config.cpp -- Engine Registration

`HelloMod/Scripts/config.cpp`:

```cpp
class CfgPatches
{
    class HelloMod_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data"
        };
    };
};

class CfgMods
{
    class HelloMod
    {
        dir = "HelloMod";
        name = "Hello Mod";
        author = "YourName";
        type = "mod";

        dependencies[] = { "Mission" };

        class defs
        {
            class missionScriptModule
            {
                value = "";
                files[] = { "HelloMod/Scripts/5_Mission" };
            };
        };
    };
};
```

Two classes, two jobs:

- **CfgPatches** declares the PBO to the engine. The class name (`HelloMod_Scripts`) must be globally unique across every loaded mod. `requiredAddons[] = { "DZ_Data" }` says "load me after vanilla DayZ data" -- this is what guarantees the vanilla classes you `modded` already exist when your scripts compile. A PBO without a `CfgPatches` entry is ignored.
- **CfgMods** tells the engine where your scripts live. HelloMod registers only a `missionScriptModule` pointing at `5_Mission`, because that is the layer where mission lifecycle hooks (`MissionServer`, `MissionGameplay`) are available. `dependencies[] = { "Mission" }` matches: it declares which vanilla script modules your mod plugs into.

The full breakdown of every `config.cpp` section is in [config.cpp Deep Dive](02-config-cpp.md); the layer system behind `5_Mission` is in [The Five Script Layers](01-five-layers.md).

---

## File 3: The Script -- Hooking the Mission

`HelloMod/Scripts/5_Mission/HelloMod/HelloMission.c`:

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        Print("[HelloMod] Mission started! Server is running.");
    }
};

modded class MissionGameplay
{
    override void OnInit()
    {
        super.OnInit();
        Print("[HelloMod] Mission started! Client is running.");
    }
};
```

Line by line:

- `modded class MissionServer` extends the vanilla server mission class without replacing the file it lives in. When the server starts a mission, `OnInit()` fires and your message prints.
- `modded class MissionGameplay` does the same on the client side.
- `super.OnInit()` calls the previous implementation in the chain (vanilla, or another mod's) first. **Never skip it** -- multiple mods can `modded` the same class, and one missing `super` call breaks every mod that loads after yours.
- `Print()` writes to the DayZ script log.

The subdirectory `5_Mission/HelloMod/` is convention, not requirement -- the engine compiles every `.c` file under the path listed in `files[]`. Namespacing your files under a folder named after your mod keeps multi-mod servers debuggable.

---

## The Load Sequence

Here is what the engine does with those three files, in order:

```
1. Engine starts, reads config.cpp files from all PBOs
2. CfgPatches "HelloMod_Scripts" is registered
   --> requiredAddons ensures it sorts after DZ_Data
3. CfgMods "HelloMod" is registered
   --> Engine records the missionScriptModule path
4. Engine compiles each script module in layer order
   --> HelloMission.c is compiled as part of 5_Mission
   --> "modded class MissionServer" patches the vanilla class
5. Server starts a mission
   --> MissionServer.OnInit() is called
   --> Your override runs, calling super.OnInit() first
   --> Print() writes to the script log
6. Client connects and loads
   --> MissionGameplay.OnInit() is called on the client
   --> Print() writes to the client's script log
```

The `modded` keyword is the key mechanism: "take the existing class and add my changes on top." Every DayZ script mod integrates with vanilla code this way.

---

## Where the Output Goes

`Print()` output lands in the **script log**, and DayZ writes logs to different places depending on how the game was launched:

### Client (default)

```
C:\Users\<YourName>\AppData\Local\DayZ\
```

Look for the most recent files:

```
script_<date>_<time>.log      <-- script output only (easiest to search)
DayZ_<date>_<time>.RPT        <-- engine + script output combined
```

### Dedicated server (`-profiles`)

A dedicated server writes its logs to the directory you pass with the `-profiles` launch parameter:

```
DayZServer_x64.exe -config=serverDZ.cfg -profiles=P:\ServerProfile -mod=@HelloMod
```

With that command, `script_*.log`, the server `.RPT`, and crash logs all appear in `P:\ServerProfile\`. Always set `-profiles` explicitly on a server -- it keeps logs, mod-written JSON files (`$profile:` paths), and crash dumps in one predictable folder instead of scattered next to the executable.

### What to look for

Open the newest script log and search for `[HelloMod]`:

```
[HelloMod] Mission started! Server is running.
```

Lines starting with `SCRIPT (E):` are compile or runtime errors -- see the [Troubleshooting Reference](#troubleshooting-reference) below.

---

## Testing Without Packing

DayZ can load unpacked scripts during development via **file patching**, which skips the PBO step entirely:

```
DayZDiag_x64.exe -mod=HelloMod -filePatching
```

This loads `.c` files directly from the folder -- the fastest way to iterate on script changes.

For distribution (Workshop, servers), the mod must be packed into a PBO and laid out like this:

```
@HelloMod/
  mod.cpp
  Addons/
    HelloMod_Scripts.pbo
```

```
DayZDiag_x64.exe -mod=@HelloMod
```

PBO packing -- Addon Builder settings, prefixes, binarization, and automated build scripts -- has its own chapter: [PBO Packing](../04-file-formats/06-pbo-packing.md).

---

## Growing the Skeleton

The three-file skeleton scales by adding layers and content folders, not by restructuring.

### Add a 3_Game Layer

Constants, configuration classes, and RPC definitions that do not depend on world entities:

```
HelloMod/
  Scripts/
    config.cpp              <-- add gameScriptModule entry
    3_Game/
      HelloMod/
        HelloConfig.c       <-- configuration class
    5_Mission/
      HelloMod/
        HelloMission.c      <-- existing file
```

Update `config.cpp` accordingly:

```cpp
dependencies[] = { "Game", "Mission" };

class defs
{
    class gameScriptModule
    {
        value = "";
        files[] = { "HelloMod/Scripts/3_Game" };
    };
    class missionScriptModule
    {
        value = "";
        files[] = { "HelloMod/Scripts/5_Mission" };
    };
};
```

### Add a 4_World Layer

Custom items, player extensions, and world managers get a `worldScriptModule` entry the same way:

```
HelloMod/
  Scripts/
    config.cpp              <-- add worldScriptModule entry
    3_Game/
      HelloMod/
        HelloConfig.c
    4_World/
      HelloMod/
        HelloManager.c      <-- world-aware logic
    5_Mission/
      HelloMod/
        HelloMission.c
```

Remember the layer rule from [The Five Script Layers](01-five-layers.md): lower layers cannot reference types defined in higher layers.

### Add UI

A `.layout` file plus a `5_Mission` script (widgets and layouts are Part 3 of this guide):

```
HelloMod/
  GUI/
    layouts/
      hello_panel.layout    <-- UI layout file
  Scripts/
    5_Mission/
      HelloMod/
        HelloPanel.c        <-- UI script
```

### Add a Custom Item

Item definitions live in a separate `Data/config.cpp` (CfgVehicles), with behavior scripted in `4_World`:

```
HelloMod/
  Data/
    config.cpp              <-- CfgVehicles with item definition
    Models/
      hello_item.p3d        <-- 3D model
  Scripts/
    4_World/
      HelloMod/
        HelloItem.c         <-- item behavior script
```

The full walkthrough is the [Custom Item tutorial](../08-tutorials/02-custom-item.md).

---

## Depending on a Framework

To build on top of a script framework, add its `CfgPatches` class name to your `requiredAddons`. Using the wiki's Lantern teaching framework (built across Part 7):

```cpp
// In config.cpp
requiredAddons[] = { "DZ_Data", "Lantern_Core_Scripts" };
```

This guarantees the framework's scripts compile before yours, so your code can reference its classes. Public frameworks such as Community Framework document their own patch name in their installation instructions -- substitute it here.

---

## Troubleshooting Reference

### "Addon HelloMod_Scripts requires addon DZ_Data which is not loaded"

Your `requiredAddons` references an addon that is not present. Make sure `DZ_Data` is spelled correctly and the DayZ base game data is loaded.

### No Log Output (Mod Seems to Not Load)

Check these in order:

1. **Is the mod in the launch parameter?** Verify `-mod=HelloMod` or `-mod=@HelloMod` is in your launch command.
2. **Is config.cpp in the right place?** It must be at the root of the PBO (or the root of the `Scripts/` folder when file-patching).
3. **Are the script paths correct?** The `files[]` paths in `config.cpp` must match the actual directory structure. `"HelloMod/Scripts/5_Mission"` means the engine looks for that exact path.
4. **Is there a CfgPatches class?** Without it, the PBO is ignored.

### SCRIPT (E): Undefined variable / Undefined type

Your code references something that does not exist at that layer. Common causes:

- Referencing `PlayerBase` from `3_Game` (it is defined in `4_World`)
- Typo in a class or variable name
- Missing `super.OnInit()` call in another mod (causes cascade failures)

### SCRIPT (E): Member not found

The method or property you are calling does not exist on that class. Double-check the vanilla API. Common mistake: calling methods from a newer DayZ version when running an older one.

### Mod Loads But Script Does Not Run

- Check that your `.c` file is inside the directory listed in `files[]`
- Ensure the file has a `.c` extension (not `.txt` or `.cs`)
- Verify the `modded class` name matches the vanilla class exactly (case-sensitive)

### PBO Packing Errors

- Ensure `config.cpp` is at the root level inside the PBO
- File paths inside PBOs use forward slashes (`/`), not backslashes
- Make sure there are no binary files in the Scripts folder (only `.c` and `.cpp`)
- For prefix and binarization issues, see [PBO Packing](../04-file-formats/06-pbo-packing.md)

---

## Best Practices

- Always call `super.OnInit()` before your custom code in modded mission classes -- skipping it breaks other mods' initialization.
- Use a unique prefix in your `Print()` messages (e.g., `[HelloMod]`) so you can grep log files quickly.
- Start with `5_Mission` only. Add `3_Game` and `4_World` layers incrementally as your mod grows.
- Use `-filePatching` during development to avoid re-packing PBOs on every change.
- On servers, always pass `-profiles=<folder>` so logs and profile data land in one known place.
- Keep your first mod under 3 files until it works, then expand. Debugging a minimal structure is far easier.

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| `Print()` outputs to log | Messages appear in script log | Output goes to **both** the `.RPT` file and the `script_<date>_<time>.log` file. Check either one; the script log is often easier to search since it contains only script output |
| `-filePatching` loads loose files | Unpacked mods work instantly | Some assets (models, textures) still require PBO packing; scripts work loose, but `.layout` files may not load from unpacked folders on all setups |
| `modded class` patches vanilla | Your override replaces the original | Multiple mods can `modded class` the same class; they chain in load order. If one skips `super.OnInit()`, all later mods break |
| `DZ_Data` is the only needed dependency | Minimal `requiredAddons` | Works for pure script mods, but if you reference any vanilla weapon/item class, you also need `DZ_Scripts` or the specific vanilla PBO |
| Three files is enough | Mod loads with mod.cpp + config.cpp + one .c file | True for a script-only mod, but adding items or UI requires additional PBOs (Data, GUI) |
