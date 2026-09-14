# Scaffolding a Mod Project


---

> **Summary:** Every new DayZ mod starts from the same skeleton of boilerplate: `mod.cpp`, `config.cpp`, and stubs for each script layer. Instead of recreating those files by hand for every project, you keep a reusable *scaffold* and copy it. This tutorial shows you how to assemble a minimal scaffold once, then rename it safely into a fresh mod using a repeatable, scripted workflow -- so you spend your time writing game logic, not wiring up boilerplate.

---

## Table of Contents

- [Why Scaffold?](#why-scaffold)
- [What the Scaffold Contains](#what-the-scaffold-contains)
- [Step 1: Get a Scaffold](#step-1-get-a-scaffold)
- [Step 2: Understand the File Structure](#step-2-understand-the-file-structure)
- [Step 3: Choose Your Names](#step-3-choose-your-names)
- [Step 4: A Safe, Scripted Rename](#step-4-a-safe-scripted-rename)
- [Step 5: Update config.cpp](#step-5-update-config-cpp)
- [Step 6: Update mod.cpp](#step-6-update-mod-cpp)
- [Step 7: Build and Test](#step-7-build-and-test)
- [Integration with DayZ Tools and Workbench](#integration-with-dayz-tools-and-workbench)
- [Template vs. Manual Setup](#template-vs-manual-setup)
- [Community Templates](#community-templates)
- [Next Steps](#next-steps)

---

## Why Scaffold?

Once you have built a Hello World mod by hand (as covered in [Chapter 8.1: Your First Mod](01-first-mod.md)), you know that the *first* few files of every mod are nearly identical. The engine always needs:

- a `mod.cpp` so the launcher can list your mod,
- a `config.cpp` that registers your mod and points the engine at each script layer,
- a folder for each of the three script layers (`3_Game`, `4_World`, `5_Mission`).

Recreating that from memory for every project is slow and easy to get subtly wrong -- a mismatched folder name or a forgotten `files[]` path costs you a debugging session. A **scaffold** solves this: you set up the skeleton correctly *once*, keep it around, and copy it whenever you start a new mod. The only work left is renaming a handful of identifiers, which this tutorial makes mechanical.

This is the recommended starting point for anyone who has already built a Hello World mod and wants to move on to real projects.

---

## What the Scaffold Contains

A good scaffold includes everything a mod needs to compile and load -- and nothing feature-specific:

| File / Folder | Purpose |
|---------------|---------|
| `mod.cpp` | Mod metadata (name, author, version) displayed in the DayZ launcher |
| `Scripts/config.cpp` | CfgPatches and CfgMods declarations that register the mod with the engine |
| `Scripts/3_Game/` | Game-layer script stub (enums, constants, config classes) |
| `Scripts/4_World/` | World-layer script stub (entities, managers, world interactions) |
| `Scripts/5_Mission/` | Mission-layer script stub (UI, mission hooks) |
| `.gitignore` | Pre-configured ignores for DayZ development (PBOs, logs, temp files) |

The scaffold follows the standard 5-layer script hierarchy documented in [Chapter 2.1: The 5-Layer Script Hierarchy](../02-mod-structure/01-five-layers.md). All three script layers are wired up in `config.cpp` so you can immediately drop code into any layer without touching the configuration again.

> A scaffold is deliberately *minimal*. When you want a richer starting point -- one that already ships a config system, a singleton manager, client-server RPC, a UI panel, keybinds, and localization -- use the full [Chapter 8.9: Professional Mod Template](09-professional-template.md) instead. This chapter is about the smallest reusable skeleton; Chapter 8.9 is the feature-rich illustrative template (not runtime-validated).

---

## Step 1: Get a Scaffold

You have three ways to obtain a scaffold. Pick whichever fits how you like to work.

### Option A: Trim Down the Professional Template

Chapter 8.9 is a feature-rich illustrative skeleton, not a validated production fixture. If you use it as a personal scaffold, first materialize and test the renamed version, then remove systems you do not want while repeating the relevant checks.

### Option B: Assemble a Minimal Skeleton by Hand

If you prefer to know exactly what is in your scaffold, build it yourself once. Create this tree on your `P:` drive:

```
P:\_ModScaffold\
    mod.cpp
    .gitignore
    Scripts\
        config.cpp
        3_Game\
            ModName\
                (empty -- game-layer scripts go here)
        4_World\
            ModName\
                (empty -- world-layer scripts go here)
        5_Mission\
            ModName\
                ModInit.c
```

Populate `config.cpp` and `mod.cpp` using the templates in [Step 5](#step-5-update-config-cpp) and [Step 6](#step-6-update-mod-cpp) below (with `ModName`/placeholder identifiers), and put a single startup print in `5_Mission/ModName/ModInit.c`:

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        Print("[ModName] Server initialized!");
    }
};
```

Keep `_ModScaffold` untouched -- you copy *from* it, you never build *in* it.

### Option C: Start From a Community Template

Several modders publish ready-made starter repositories on GitHub. Using one is fine; just clone it into a fresh working folder rather than developing inside the original, and read its license before reusing any code it ships. See [Community Templates](#community-templates) at the end of this chapter for links.

### Copy the Scaffold for Your New Mod

However you obtained it, start a new project by *copying* the scaffold to a new folder named after your mod:

```batch
xcopy /E /I P:\_ModScaffold P:\MyAwesomeMod
```

Now `P:\MyAwesomeMod` is your project. The rest of this tutorial renames its placeholder identifiers into `MyAwesomeMod`.

---

## Step 2: Understand the File Structure

After copying, your mod directory looks like this:

```
P:\MyAwesomeMod\
    mod.cpp
    Scripts\
        config.cpp
        3_Game\
            ModName\
                (game-layer scripts)
        4_World\
            ModName\
                (world-layer scripts)
        5_Mission\
            ModName\
                (mission-layer scripts)
```

### How Each Piece Fits Together

**`mod.cpp`** is the identity card of your mod. It controls what players see in the DayZ launcher mod list. See [Chapter 2.3: mod.cpp & Workshop](../02-mod-structure/03-mod-cpp.md) for all available fields.

**`Scripts/config.cpp`** is the most critical file. It tells the DayZ engine:
- What your mod depends on (`CfgPatches.requiredAddons[]`)
- Where each script layer lives (`CfgMods.class defs`)
- What preprocessor defines to set (`defines[]`)

See [Chapter 2.2: config.cpp Deep Dive](../02-mod-structure/02-config-cpp.md) for a complete reference.

**`Scripts/3_Game/`** loads first. Place enums, constants, RPC IDs, configuration classes, and anything that does not reference world entities here.

**`Scripts/4_World/`** loads second. Place entity classes (`modded class ItemBase`), managers, and anything that interacts with game objects here.

**`Scripts/5_Mission/`** loads last. Place mission hooks (`modded class MissionServer`), UI panels, and startup logic here. This layer can reference types from all lower layers.

---

## Step 3: Choose Your Names

The scaffold ships with placeholder names (`ModName`, and whatever the config uses). Before touching anything, decide on the six identifiers that will replace them. Writing them down first is what makes the rename mechanical instead of error-prone.

| Identifier | Example | Used In |
|------------|---------|---------|
| **Mod display name** | `"My Awesome Mod"` | mod.cpp, config.cpp |
| **Directory name** | `MyAwesomeMod` | Folder name, config.cpp paths |
| **CfgPatches class** | `MyAwesomeMod_Scripts` | config.cpp CfgPatches |
| **CfgMods class** | `MyAwesomeMod` | config.cpp CfgMods |
| **Script subfolder** | `MyAwesomeMod` | Inside 3_Game/, 4_World/, 5_Mission/ |
| **Preprocessor define** | `MYAWESOMEMOD` | config.cpp defines[], #ifdef checks |

### Naming Rules

- **No spaces or special characters** in directory and class names. Use PascalCase or underscores.
- **CfgPatches class names must be globally unique.** Two mods with the same CfgPatches class name will conflict on any server that loads both. Prefix the class with your mod name.
- **Script subfolder names** inside each layer should match your mod name for consistency and to keep PBO prefixes clean.

---

## Step 4: A Safe, Scripted Rename

The fragile way to rename a scaffold is to open every file and manually find-and-replace `ModName`. Miss one path in `config.cpp` and the mod silently loads no scripts. A safer approach is to script the replacement so it is exhaustive and repeatable.

### Rename in the Right Order

Do it in this order so nothing references a name that no longer exists:

1. **Text inside files first** -- replace the placeholder token everywhere in `config.cpp` and `mod.cpp`.
2. **Folder names second** -- rename the `ModName` subfolder inside each script layer.
3. **The mod root last** -- if your copied folder is not already named after your mod, rename it.

### A Rename Script

Run this from the mod root. It replaces the placeholder token `ModName` inside every text file, then renames the per-layer subfolders. Adjust `$old` and `$new` to match your scaffold's placeholder and your chosen name.

```batch
@echo off
setlocal
set OLD=ModName
set NEW=MyAwesomeMod

powershell -NoProfile -Command ^
  "Get-ChildItem -Recurse -Include *.cpp,*.c,*.xml,*.csv | ForEach-Object { (Get-Content $_.FullName -Raw) -replace '%OLD%','%NEW%' | Set-Content $_.FullName }"

for %%L in (3_Game 4_World 5_Mission) do (
    if exist "Scripts\%%L\%OLD%" ren "Scripts\%%L\%OLD%" "%NEW%"
)

echo Rename complete. Review config.cpp before building.
```

> Scripted find-and-replace is only as safe as your placeholder token. Choose a scaffold whose placeholder (`ModName`) does not appear as a substring of any real keyword -- never use a token like `Mod` or `Script` that collides with engine identifiers.

After the script runs, always **read `config.cpp` once by eye** (next step) to confirm every path now points at your real folders. A five-second review beats a silent no-op mod.

---

## Step 5: Update config.cpp

Whether you renamed by script or by hand, `config.cpp` should now read like this. Verify each section.

### CfgPatches

The patch class carries your unique name and lists what your mod depends on:

```cpp
class CfgPatches
{
    class MyAwesomeMod_Scripts    // <-- Your globally-unique patch name
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data"            // Base game dependency
        };
    };
};
```

If your mod depends on another mod, add that mod's CfgPatches class name to `requiredAddons[]`. For example, a mod built on top of a shared framework declares the framework's script patch:

```cpp
requiredAddons[] =
{
    "DZ_Data",
    "Lantern_Core_Scripts"    // Depends on the Lantern_Core framework
};
```

Here `Lantern_Core_Scripts` is the CfgPatches class published by a framework mod your mod is built on. Replace it with the actual patch class name of whatever framework you depend on -- the framework's own documentation lists it. Getting this name right is what guarantees the engine loads the dependency *before* your scripts compile.

### CfgMods

The CfgMods block ties your mod's identity to its script paths:

```cpp
class CfgMods
{
    class MyAwesomeMod
    {
        dir = "MyAwesomeMod";
        name = "My Awesome Mod";
        author = "YourName";
        type = "mod";

        dependencies[] = { "Game", "World", "Mission" };

        class defs
        {
            class gameScriptModule
            {
                value = "";
                files[] = { "MyAwesomeMod/Scripts/3_Game" };
            };
            class worldScriptModule
            {
                value = "";
                files[] = { "MyAwesomeMod/Scripts/4_World" };
            };
            class missionScriptModule
            {
                value = "";
                files[] = { "MyAwesomeMod/Scripts/5_Mission" };
            };
        };
    };
};
```

**Key points:**
- The `dir` value must match your mod's root folder name exactly.
- Each `files[]` path is relative to the mod root and uses forward slashes.
- The `dependencies[]` array lists which vanilla script modules you hook into. Most mods use all three: `"Game"`, `"World"`, and `"Mission"`.

### Preprocessor Defines (Optional)

If you want other mods to detect your mod's presence, add a `defines[]` array to your CfgMods class:

```cpp
class MyAwesomeMod
{
    // ... (dir, name, author, type, dependencies, class defs above)

    // Enable cross-mod detection
    defines[] = { "MYAWESOMEMOD" };
};
```

Other mods can then use `#ifdef MYAWESOMEMOD` to conditionally compile code that integrates with yours. See [Chapter 7.6: The Event Bus Pattern](../07-patterns/06-events.md) for how mods discover and talk to one another at runtime.

**Server-mod caveat (observed behaviour, not documented by Bohemia).** A `defines[]` symbol declared by a package loaded via `-mod=` reaches `#ifdef` checks in other `-mod=` packages. It has been observed *not* to reach packages loaded as `-servermod=` (`type = "servermod"`): in a production multi-package mod, the same `#ifdef` guard compiled in a `type = "mod"` package and was silently compiled out in a `type = "servermod"` package, with the runtime registration log as the discriminator and an unguarded third package as the control. Bohemia does not document `defines[]` propagation either way, so treat this as a field observation rather than a specified rule -- but do design around it, because a silently-false `#ifdef` is indistinguishable from a clean build.

Two ways to stay safe:

- **Declare the symbol in each package's own `defines[]`.** A package always sees its own defines.
- **Or register unconditionally** and make the dependency hard, via `requiredAddons[]`.

There is a trap in the first option worth knowing before you pick it. Once a server-only package self-declares a symbol, every `#ifdef` on that symbol inside it is unconditionally true and has stopped detecting anything. That is safe only while `requiredAddons[]` already mandates whatever the guard was protecting. The two mechanisms are not interchangeable: `requiredAddons[]` is what makes a type *exist*; `defines[]` and `#ifdef` only decide whether code is *emitted*. For a hard dependency, list the addon and call it unguarded. Keep `#ifdef` for genuinely optional integration between `-mod=` packages, gated on a define the other package publishes and that you do not redeclare.

---

## Step 6: Update mod.cpp

Open `mod.cpp` in the root directory and fill in your mod's information:

```cpp
name         = "My Awesome Mod";
author       = "YourName";
version      = "1.0.0";
overview     = "A brief description of what your mod does.";
picture      = "";             // Optional: path to a preview image
logo         = "";             // Optional: path to a logo
logoSmall    = "";             // Optional: path to a small logo
logoOver     = "";             // Optional: path to a logo hover state
tooltip      = "My Awesome Mod";
action       = "";             // Optional: URL to your mod's website
```

At minimum, set `name`, `author`, and `overview`. The other fields are optional but improve how your mod presents in the launcher.

---

## Step 7: Build and Test

### Using File Patching (Fast Iteration)

The fastest way to test during development:

```batch
DayZDiag_x64.exe -mod=P:\MyAwesomeMod -filePatching
```

This loads your scripts directly from the source folders without packing a PBO. Edit a `.c` file, restart the game, and see changes immediately.

### Using Addon Builder (For Distribution)

When you are ready to distribute:

1. Open **DayZ Tools** from Steam
2. Launch **Addon Builder**
3. Set **Source directory** to `P:\MyAwesomeMod\Scripts\`
4. Set **Output directory** to `P:\@MyAwesomeMod\Addons\`
5. Set **Prefix** to `MyAwesomeMod\Scripts`
6. Click **Pack**

Then copy `mod.cpp` next to the `Addons` folder:

```
P:\@MyAwesomeMod\
    mod.cpp
    Addons\
        Scripts.pbo
```

### Verify in the Script Log

After launching, check the script log for your startup messages:

```
%localappdata%\DayZ\script_<date>_<time>.log
```

Search for your mod's prefix tag (e.g., `[MyAwesomeMod]`). If it is missing, the most common cause is a `files[]` path in `config.cpp` that still points at the old placeholder folder -- re-check [Step 5](#step-5-update-config-cpp).

---

## Integration with DayZ Tools and Workbench

### Workbench

DayZ Workbench can open and edit your mod's scripts with syntax highlighting:

1. Open **Workbench** from DayZ Tools
2. Go to **File > Open** and navigate to your mod's `Scripts/` folder
3. Open any `.c` file to edit with Enforce Script support

Workbench reads `config.cpp` to understand which files belong to which script module, so a correctly renamed `config.cpp` is essential here too.

### P: Drive Setup

Scaffolds are designed to work from the `P:` drive. If you keep your source elsewhere, create a junction:

```batch
mklink /J P:\MyAwesomeMod "D:\Projects\MyAwesomeMod"
```

This makes the mod accessible at `P:\MyAwesomeMod` without moving files.

### Addon Builder Automation

For repeated builds, drop a batch file in your mod's root:

```batch
@echo off
set DAYZ_TOOLS="C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools"
set SOURCE=P:\MyAwesomeMod\Scripts
set OUTPUT=P:\@MyAwesomeMod\Addons
set PREFIX=MyAwesomeMod\Scripts

%DAYZ_TOOLS%\Bin\AddonBuilder\AddonBuilder.exe %SOURCE% %OUTPUT% -prefix=%PREFIX% -clear
echo Build complete.
pause
```

---

## Template vs. Manual Setup

| Aspect | Scaffold | Manual (Chapter 8.1) |
|--------|----------|----------------------|
| **Time to first build** | ~2 minutes | ~15 minutes |
| **All 3 script layers** | Pre-configured | You add them as needed |
| **config.cpp** | Complete with all modules | Minimal (mission only) |
| **Git ready** | .gitignore included | You create your own |
| **Learning value** | Lower (files pre-made) | Higher (you build everything) |
| **Recommended for** | Experienced modders, new projects | First-time modders learning the ropes |

**Recommendation:** If this is your very first DayZ mod, start with [Chapter 8.1](01-first-mod.md) to understand every file. Once you are comfortable, keep a scaffold and copy it for all future projects.

---

## Community Templates

You do not have to build a scaffold from scratch. Several community-maintained starter templates exist on GitHub -- some minimal, some full-featured. They can save setup time, but treat any code they ship the same way you would treat any dependency: **read the license before reusing it**, and clone into a fresh working folder rather than developing inside the original repository.

- [InclementDab/DayZ-Mod-Template](https://github.com/InclementDab/DayZ-Mod-Template) -- a community starter skeleton.

None of the steps in this chapter depend on any particular external template; the rename workflow above applies to whichever scaffold you choose.

---

## Next Steps

With your scaffold-based mod up and running, you can:

1. **Add a custom item** -- Follow [Chapter 8.2: Creating a Custom Item](02-custom-item.md) to define items in config.cpp.
2. **Build an admin panel** -- Follow [Chapter 8.3: Building an Admin Panel](03-admin-panel.md) for server management UI.
3. **Add chat commands** -- Follow [Chapter 8.4: Adding Chat Commands](04-chat-commands.md) for in-game text commands.
4. **Graduate to the full template** -- When your project outgrows a minimal skeleton, adopt the [Chapter 8.9: Professional Mod Template](09-professional-template.md) with config, RPC, UI, and build automation.
5. **Study config.cpp in depth** -- Read [Chapter 2.2: config.cpp Deep Dive](../02-mod-structure/02-config-cpp.md) to understand every field.
6. **Add dependencies** -- If your mod builds on a framework, update `requiredAddons[]` and see [Chapter 2.4: The Minimum Viable Mod](../02-mod-structure/04-minimum-viable-mod.md).
