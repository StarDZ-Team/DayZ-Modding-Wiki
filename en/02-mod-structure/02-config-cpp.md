# config.cpp Deep Dive

---

> **Summary:** A `config.cpp` declares an addon's dependencies, scripts, items, and integration points. Most configuration addons have one at their PBO root; do not assume every physical PBO maps one-to-one to one configuration addon.

---

## Table of Contents

- [Overview](#overview)
- [Where config.cpp Lives](#where-config-cpp-lives)
- [Path Conventions](#path-conventions)
- [CfgPatches Block](#cfgpatches-block)
- [CfgMods Block](#cfgmods-block)
- [class defs: Script Module Paths](#class-defs-script-module-paths)
- [class defs: imageSets and widgetStyles](#class-defs-imagesets-and-widgetstyles)
- [defines Array](#defines-array)
- [CfgVehicles: An Entity Primer](#cfgvehicles-an-entity-primer)
- [CfgSoundSets and CfgSoundShaders: A Primer](#cfgsoundsets-and-cfgsoundshaders-a-primer)
- [CfgAddons: Preload Declarations](#cfgaddons-preload-declarations)
- [Complete Annotated Examples](#complete-annotated-examples)
- [Common Mistakes](#common-mistakes)
- [Complete Template](#complete-template)

---

## Overview

A DayZ mod typically has one or more PBO files, with configuration addons containing a `config.cpp` at their PBO root. The engine reads those configs during startup to determine:

1. **What your mod depends on** (CfgPatches) — this chapter is the canonical reference for `requiredAddons` and mod load order
2. **Where your scripts are** (CfgMods class defs)
3. **What items/entities it adds** (CfgVehicles, CfgWeapons, etc.)
4. **What sounds it adds** (CfgSoundSets, CfgSoundShaders)
5. **What preprocessor symbols it defines** (defines[])

A mod usually has separate PBOs for different concerns:
- `MyMod/Scripts/config.cpp` -- script definitions and module paths
- `MyMod/Data/config.cpp` -- item/vehicle/weapon definitions
- `MyMod/GUI/config.cpp` -- imageset and style declarations

---

## Where config.cpp Lives

```
@MyMod/
  Addons/
    MyMod_Scripts.pbo         --> contains Scripts/config.cpp
    MyMod_Data.pbo            --> contains Data/config.cpp (items, vehicles)
    MyMod_GUI.pbo             --> contains GUI/config.cpp (imagesets, styles)
```

Multiple PBOs from the same mod are common. Give every independently load-ordered configuration addon a unique `CfgPatches` class, but do not use that class name as evidence that each physical PBO has exactly one addon identity: a PBO can expose additional configuration roots, while shipping resource PBOs can exist without a root config.

---

## Path Conventions

Two path styles appear inside `config.cpp`, and mixing them arbitrarily is a common source of confusion. The engine accepts both separators in config files, but the community conventions are:

| Path kind | Convention | Example |
|-----------|-----------|---------|
| Script module directories (`files[]` in `class defs`) | Forward slashes, no leading separator | `"MyMod/Scripts/3_Game"` |
| Asset references (`model`, textures, sound `samples[]`) | Backslashes, model paths with a leading `\` | `"\MyMod\Data\Models\item.p3d"` |

Pick these conventions and keep them consistent across your mod.

A related convention applies outside `config.cpp`, in **Enforce Script string literals** (`.c` files). The `\\` and `\"` escape sequences are supported there, and vanilla uses both: `3_game/objectspawner.c:4` declares `"DZ\\plants"` in a path array (alongside the forward-slash form `"DZ/plants"`), and `3_game/tools/jsonfileloader.c:14` formats `"Cannot open file \"%1\" for reading"`. What favours forward slashes is that engine subsystems expect them in resource paths -- `3_game/particles/particlelist.c:391-393` rewrites `\` to `/` and warns that the wrong delimiter was used, but only in a diagnostic build: both the rewrite and the warning sit inside `#ifdef DIAG_DEVELOPER` (`:390`-`:395`), under a comment that reads "Silently fail on retail" (`:389`). On a **retail** build neither happens -- the backslash path falls straight through unmodified (`:397`). Prefer `/` in in-game resource paths for that reason: on the build your players actually run, nothing fixes a wrong delimiter for you.

---

## CfgPatches Block

`CfgPatches` is **required** in every config.cpp. It declares a named patch and its dependencies.

### Syntax

```cpp
class CfgPatches
{
    class MyMod_Scripts          // Unique patch name (must not collide with other mods)
    {
        units[] = {};            // Entity classnames this PBO adds (for editor/spawner)
        weapons[] = {};          // Weapon classnames this PBO adds
        requiredVersion = 0.1;   // Minimum game version (always 0.1 in practice)
        requiredAddons[] =       // PBO dependencies -- CONTROLS LOAD ORDER
        {
            "DZ_Data"            // Almost always needed
        };
    };
};
```

### requiredAddons: The Dependency Chain

This is the most critical field in the entire config, and this section is the wiki's canonical reference for it -- the [5-Layer Script Hierarchy](01-five-layers.md) chapter (layer order *inside* one mod) and the server-side [Mod Management](../09-server-admin/10-mod-management.md) chapter (the `-mod=` launch line) both build on it.

`requiredAddons` tells the engine:

1. **Load order:** Your PBO's config is merged and its scripts compile AFTER all listed addons
2. **Hard dependency:** If a listed addon is missing, your mod fails to load with an error

Each entry must match a prerequisite `CfgPatches` class name. It is not a PBO filename, prefix, mod-folder name, or Workshop ID:

| Dependency | requiredAddons Entry | When to Use |
|-----------|---------------------|-------------|
| Vanilla DayZ data | `"DZ_Data"` | Almost always (items, configs) |
| Vanilla DayZ scripts | `"DZ_Scripts"` | When extending vanilla script classes |
| Vanilla weapons | `"DZ_Weapons_Firearms"` | When adding weapons/attachments |
| Vanilla magazines | `"DZ_Weapons_Magazines"` | When adding magazines/ammo |
| A framework mod | The `CfgPatches` name the framework documents | When building on top of another mod |
| Lantern Core (this wiki's teaching framework) | `"Lantern_Core_Scripts"` | Running example used throughout this wiki |

**Example: Multiple dependencies**

```cpp
requiredAddons[] =
{
    "DZ_Scripts",
    "DZ_Data",
    "DZ_Weapons_Firearms",
    "DZ_Weapons_Ammunition",
    "DZ_Weapons_Magazines",
    "Lantern_Core_Scripts"
};
```

### How the Engine Resolves Load Order

- The engine builds a dependency graph from the `requiredAddons` of every loaded PBO, then merges configs and compiles scripts in dependency order.
- If configuration addon A lists configuration addon B, then A's config classes can inherit from B's, and A's `modded` classes stack on top of B's.
- Chains are **transitive**. If Mod_A depends on Mod_B, and Mod_B depends on `DZ_Data`, then Mod_A does not need to list `DZ_Data`. Listing explicit dependencies is still good practice for clarity and resilience against upstream changes.
- The order of entries on the server's `-mod=` launch line is **not** a substitute for `requiredAddons`. If your mod needs another mod loaded first, declare it here -- never rely on launcher ordering.
- The declaration does not install or discover its prerequisite. The package containing that addon must already be installed and present on the relevant `-mod` or `-serverMod` launch list.

### units[] and weapons[]

These arrays list the classnames of entities and weapons defined in this PBO. They serve two purposes:

1. The DayZ editor uses them to populate spawn lists
2. Other tools (like admin panels) use them for item discovery

```cpp
units[] = { "MyMod_SomeBuilding", "MyMod_SomeVehicle" };
weapons[] = { "MyMod_CustomRifle", "MyMod_CustomPistol" };
```

For script-only PBOs, leave both empty -- or omit them entirely. The arrays are optional and default to empty when not declared.

---

## CfgMods Block

`CfgMods` is required when your PBO adds or modifies scripts, inputs, or GUI resources. It defines the mod identity and its script module structure.

### Basic Structure

```cpp
class CfgMods
{
    class MyMod                   // Mod identifier (used internally)
    {
        dir = "MyMod";            // Root directory of the mod (PBO prefix path)
        name = "My Mod Name";     // Human-readable name
        author = "AuthorName";    // Author string
        credits = "AuthorName";   // Credits string
        overview = "Description"; // Mod description
        picture = "";             // Logo image path
        action = "";              // URL (website/Discord)
        type = "mod";             // Required value documented by Bohemia
        extra = 0;                // Reserved, always 0

        // Keybind definitions (optional)
        inputs = "MyMod/Scripts/Data/Inputs.xml";

        // Preprocessor symbols (optional)
        defines[] = { "MYMOD_LOADED" };

        // Script module dependencies
        dependencies[] = { "Game", "World", "Mission" };

        // Script module paths
        class defs
        {
            // ... (covered in next section)
        };
    };
};
```

### Which Keys the Engine Actually Reads

`CfgMods` accumulates keys from three different sources, and telling them apart saves you from copying a key that does nothing on a plain server:

| Key | Read by | Notes |
|-----|---------|-------|
| `type`, `inputs`, `skeletonDefinitions`, `dependencies[]`, `class defs` | Engine (native) | The set Bohemia's [Modding Structure](https://community.bistudio.com/wiki/DayZ:Modding_Structure) page documents. `type = "mod";` is annotated *required* there. |
| `name`, `picture`, `logo`, `logoSmall`, `logoOver`, `tooltip`, `overview` | Vanilla script | `ModStructure.LoadData()` reads exactly these seven for the in-game mod list (`3_game/client/mods/modstructure.c:24-30`). |
| `author`, `credits`, `creditsJson`, `versionPath`, `version` | Community Framework | CF's `modded class ModStructure` adds the readers (`JM/CF/Scripts/3_Game/CommunityFramework/Mods/ModStructure.c:74-77,130,143,176-190`). Nothing in vanilla script reads them. |
| `dir`, `extra`, `defines[]` | Not read by any script | Widely used by convention; no vanilla script reader and no entry on the Modding Structure page. |

`creditsJson` in particular is a **Community Framework integration point**, not a vanilla key: CF loads the referenced JSON and merges it into the in-game credits screen (`.../Credits/CreditsLoader.c:24-47`). Include it only when your mod already depends on CF; on a server without CF it is inert.

### Key Fields Explained

**`dir`** -- The root path prefix commonly written for the mod's own bookkeeping. Script-side `files[]` entries are mounted virtual paths, so they work whether or not `dir` is present.

**`type`** -- Bohemia documents only `type = "mod";` and marks it required. Keep that documented value in `CfgMods` for both shared and separately launched server packages. Folder-level launch flags route the package: `-mod=` makes an installed shared package available to the client and server processes, while `-serverMod=` loads a separate folder only in the server process. No reviewed source documents `type = "servermod";` as the routing mechanism -- see [Server vs Client Architecture](06-server-client-split.md#the-config-cpp-type-field).

**`dependencies`** -- Which vanilla script modules your mod extends. Almost always `{ "Game", "World", "Mission" }`. Possible values: `"Core"`, `"GameLib"`, `"Game"`, `"World"`, `"Mission"`.

**`inputs`** -- A mounted virtual path to an `Inputs.xml` file that defines custom keybindings, for example `samples/test_inputs/my_new_inputs.xml` in the official sample. It is not simply a path relative to a physical PBO root. As with `files[]`, another archive can supply the path only if the final mounted namespace resolves it; test that cross-PBO arrangement in a packaged runtime.

---

## class defs: Script Module Paths

The `class defs` block inside `CfgMods` is where you tell the engine which folders contain your scripts for each layer.

### All Available Script Modules

```cpp
class defs
{
    class engineScriptModule        // 1_Core
    {
        value = "";                 // Entry function (empty = default)
        files[] = { "MyMod/Scripts/1_Core" };
    };
    class gameLibScriptModule       // 2_GameLib (rarely used)
    {
        value = "";
        files[] = { "MyMod/Scripts/2_GameLib" };
    };
    class gameScriptModule          // 3_Game
    {
        value = "";
        files[] = { "MyMod/Scripts/3_Game" };
    };
    class worldScriptModule         // 4_World
    {
        value = "";
        files[] = { "MyMod/Scripts/4_World" };
    };
    class missionScriptModule       // 5_Mission
    {
        value = "";
        files[] = { "MyMod/Scripts/5_Mission" };
    };
};
```

### The `value` Field

The `value` field specifies a custom entry function name for that script module. When empty (`""`), the engine uses the default entry point. When set, the engine calls that global function when initializing the module.

Some frameworks override the entry point to bootstrap themselves before any other code in the module runs:

```cpp
class gameScriptModule
{
    value = "LNT_CreateGame";    // Custom entry point -- a global function the framework defines in 3_Game
    files[] = { "Lantern_Core/Scripts/3_Game" };
};
```

For most mods, leave `value` empty.

### The `files` Array

Each entry is a **directory path** (not individual files). The engine recursively compiles all `.c` files in the listed directories:

```cpp
class gameScriptModule
{
    value = "";
    files[] =
    {
        "MyMod/Scripts/3_Game"      // All .c files in this directory tree
    };
};
```

You can list multiple directories. This is how the "Common folder" pattern works:

```cpp
class gameScriptModule
{
    value = "";
    files[] =
    {
        "MyMod/Scripts/Common",     // Shared code compiled into EVERY module
        "MyMod/Scripts/3_Game"      // Layer-specific code
    };
};
class worldScriptModule
{
    value = "";
    files[] =
    {
        "MyMod/Scripts/Common",     // Same shared code, also available here
        "MyMod/Scripts/4_World"
    };
};
```

### Only Define What You Use

You do not need to declare all five script modules. Only declare the ones your mod actually uses:

```cpp
// A simple mod that only has 3_Game and 5_Mission code
class defs
{
    class gameScriptModule
    {
        files[] = { "MyMod/Scripts/3_Game" };
    };
    class missionScriptModule
    {
        files[] = { "MyMod/Scripts/5_Mission" };
    };
};
```

---

## class defs: imageSets and widgetStyles

If your mod uses custom icons or GUI styles, declare them inside `class defs`:

### imageSets

```cpp
class defs
{
    class imageSets
    {
        files[] =
        {
            "MyMod/GUI/imagesets/icons.imageset",
            "MyMod/GUI/imagesets/items.imageset"
        };
    };
    // ... script modules ...
};
```

ImageSets are XML files that map named regions of a texture atlas to sprite names. Once declared here, any script can reference the icons by name.

### widgetStyles

```cpp
class defs
{
    class widgetStyles
    {
        files[] =
        {
            "MyMod/GUI/looknfeel/custom.styles"
        };
    };
    // ... script modules ...
};
```

Widget styles define reusable visual properties (colors, fonts, padding) for GUI widgets. A UI-heavy framework typically declares several imagesets and one shared style sheet -- the [Lantern_Core annotated example](#complete-annotated-examples) below shows the full shape.

---

## defines Array

The `defines[]` array in `CfgMods` creates preprocessor symbols that other mods can check with `#ifdef`.

> **Do not rely on implicit mod-presence defines.** Some modders report that a mod's `CfgMods` class name becomes usable with `#ifdef` even without an explicit `defines[]` entry. Bohemia's [Modding Structure](https://community.bistudio.com/wiki/DayZ:Modding_Structure) page documents `type`, `inputs`, `skeletonDefinitions`, `dependencies[]` and `class defs` under `CfgMods` and does not mention `defines[]` at all, so neither the array nor an implicit class-name symbol has a documented contract you can lean on. Declare an explicit `defines[]` presence flag (as shown below) whenever you want other mods to detect yours with `#ifdef`, and declare it in every package whose own code tests it. The same caution applies in reverse when you integrate with someone else's mod: do not assume `#ifdef <TheirModName>` is available, because mods publish their detection symbols by different means. Use whatever symbol that mod's own documentation tells you to test.

```cpp
defines[] =
{
    "MYMOD_CORE",           // Other mods can do: #ifdef MYMOD_CORE
    // "MYMOD_DEBUG"        // Commented out = disabled in release
};
```

### Use Cases

**Feature detection across mods.** A content mod can light up optional integration when a framework is present:

```c
// In another mod's code (here: the NightPatrol content mod checking for Lantern Core):
#ifdef LANTERN_CORE
    Print("[NightPatrol] Lantern Core detected, enabling integration");
#else
    Print("[NightPatrol] Running without Lantern Core");
#endif
```

**Presence flag plus debug switch.** The minimal pattern most mods need:

```cpp
defines[] =
{
    "LANTERN_CORE",         // Presence flag -- downstream mods check #ifdef LANTERN_CORE
    // "LANTERN_DEBUG"      // Uncomment for debug builds; ship releases with it commented out
};
```

**Per-subsystem toggles.** Larger frameworks declare one define per optional subsystem, so downstream mods can guard each integration point independently:

```cpp
defines[] =
{
    "LANTERN_MODULE_CONFIG",       // Config persistence subsystem compiled in
    "LANTERN_MODULE_RPC",          // RPC helper layer
    "LANTERN_MODULE_EVENTS",       // Event bus
    "LANTERN_MODULE_PERMISSIONS"   // Permission checks
};
```

---

## CfgVehicles: An Entity Primer

`CfgVehicles` is the primary config class for defining in-game items, buildings, vehicles, and other entities. Despite the name "vehicles", it covers ALL entity types.

This section is a primer on the config mechanics. For the full item-creation walkthrough (textures, types.xml, stringtable), see [Creating a Custom Item](../08-tutorials/02-custom-item.md); for the script-side entity classes behind these configs, see [Entity System](../06-engine-api/01-entity-system.md).

### Basic Item Definition

```cpp
class CfgVehicles
{
    class ItemBase;                          // Forward-declare the parent class
    class MyMod_CustomItem : ItemBase        // Inherit from vanilla base
    {
        scope = 2;                           // 0=hidden, 1=static/map objects, 2=public
        displayName = "Custom Item";
        descriptionShort = "A custom item.";
        model = "\MyMod\Data\Models\item.p3d";
        weight = 500;                        // Grams
        itemSize[] = { 2, 3 };               // Inventory slots (width, height)
        rotationFlags = 17;                   // Allowed rotation in inventory
        inventorySlot[] = {};                 // Which attachment slots it fits
    };
};
```

### Forward Declarations

When overriding a class from another addon, you must forward-declare the parent class so the config parser can resolve the inheritance chain:

```cpp
class CfgVehicles
{
    class Inventory_Base;                        // Forward declaration
    class MyCustomItem : Inventory_Base          // Now the parser knows the parent
    {
        scope = 2;
        displayName = "Custom Item";
    };
};
```

### scope Values

| Value | Meaning | Usage |
|-------|---------|-------|
| `0` | Hidden | Hidden from everything -- not spawnable, not in editor, not in script console. Used for base classes and abstract parents. |
| `1` | Static/map objects | For objects placed on the map: houses, wrecks, rocks, trees. These are NOT general "editor-only" items -- they are static world objects that exist as part of the terrain. They cannot be spawned through the Central Economy or admin tools. |
| `2` | Public | Fully spawnable -- appears in the script console, admin tools, and can be used in `types.xml` or `events.xml`. This is the scope for any item, vehicle, or entity that players interact with. |

### Matching the Script Hierarchy

The class hierarchy in script must mirror the `config.cpp` inheritance. A common pattern is an abstract config parent with `scope = 0` and concrete, spawnable children with `scope = 2`:

```cpp
class CfgVehicles
{
    class ItemBase;                              // Forward declaration

    class MyMod_MedicalBase : ItemBase           // Abstract parent -- never spawned
    {
        scope = 0;
        displayName = "";
    };

    class MyMod_FieldBandage : MyMod_MedicalBase
    {
        scope = 2;                               // Public -- spawnable
        displayName = "Field Bandage";
        descriptionShort = "A sterile bandage for wound treatment.";
        model = "\MyMod\Data\Models\bandage.p3d";
        weight = 50;
    };
};
```

The matching script classes (in `4_World`) use the same names and the same parent chain:

```c
class MyMod_MedicalBase : ItemBase
{
}

class MyMod_FieldBandage : MyMod_MedicalBase
{
}
```

The engine binds a config class to the script class with the same name. If a config class has no matching script class, the engine walks up the config hierarchy and uses the nearest parent that has one.

### Abstract Base for Static Objects

The same abstract-base pattern applies to `scope = 1` map objects. Here a set of static signal lamps shares one hidden base class:

```cpp
class CfgVehicles
{
    class HouseNoDestruct;                       // Vanilla static-object parent
    class LNT_SignalLampBase : HouseNoDestruct
    {
        scope = 0;                               // Abstract -- shared properties only
    };
    class LNT_SignalLampRed : LNT_SignalLampBase
    {
        scope = 1;                               // Static map object
    };
    class LNT_SignalLampGreen : LNT_SignalLampBase
    {
        scope = 1;
    };
};
```

### The += Operator for Config Arrays

You can use `+=` to append to an array inherited from a parent class instead of overwriting it. This is not a DayZ-specific addition -- it is long-standing Real Virtuality config syntax ([Array+=](https://community.bistudio.com/wiki/Array%2B%3D) on the Bohemia community wiki, introduced in Arma 3), inherited by DayZ's config parser along with the rest of the engine's config system. Shipped DayZ mods rely on it: DayZ Expansion appends to vanilla arrays this way in `DayZExpansion/NamalskAdventure/Dta/Weapons/Ammunition/config.cpp:18-21`, which re-declares vanilla's `Ammunition_Base` with `Magazine_Base` as its **direct** parent and then appends `repairableWithKits[]+={100};` at that same level -- the direct-parent relationship the limitation below requires, not a class "extending" `Ammunition_Base` from further down -- and in sixteen configs across that repository:

```cpp
class CfgVehicles
{
    class MyItem : ItemBase
    {
        attachments[] += { "MyCustomAttachment" };  // Appends instead of replacing
    };
};
```

Without `+=`, using `=` replaces the entire array, potentially removing attachments added by other mods or vanilla.

> **`+=` appends across exactly one inheritance step.** It adds to an array inherited from the **direct** parent, and only when that parent states the array explicitly. Inherit through an intermediate class that does not restate the array and the `+=` degrades into a plain `=`, so you replace the array instead of extending it -- the outcome you were trying to avoid, with no error to tell you. When appending to a vanilla array, inherit directly from the class that declares it, or restate the array at each level.

Buildings, vehicles, weapons, and complete item definitions go well beyond this primer -- the [Creating a Custom Item](../08-tutorials/02-custom-item.md) tutorial and the [Entity System](../06-engine-api/01-entity-system.md) chapter own that ground.

---

## CfgSoundSets and CfgSoundShaders: A Primer

Custom audio requires two config classes working together: a SoundShader (the audio file reference) and a SoundSet (the playback configuration).

```cpp
class CfgSoundShaders
{
    class MyMod_Alert_SoundShader
    {
        samples[] = {{ "MyMod\Sounds\alert", 1 }};  // Path without extension, probability
        volume = 0.8;                                 // Base volume (0.0 to 1.0)
        range = 50;                                   // Audible range in meters (3D only)
        limitation = 0;                               // 0 = no limit on concurrent plays
    };
};

class CfgSoundSets
{
    class MyMod_Alert_SoundSet
    {
        soundShaders[] = { "MyMod_Alert_SoundShader" };
        volumeFactor = 1.0;                           // Multiplier on shader volume
        frequencyFactor = 1.0;                        // Pitch multiplier
        spatial = 1;                                  // 0 = 2D (UI sounds), 1 = 3D (world)
    };
};
```

The `samples` array uses double braces. Each entry is `{ "path_without_extension", probability }`. If you list multiple samples, the engine picks randomly based on probability weights.

Playing the set from script:

```c
// 2D UI sound (spatial = 0) -- position is ignored
SEffectManager.PlaySound("MyMod_Alert_SoundSet", vector.Zero);

// 3D world sound (spatial = 1) -- pass a world position
vector pos = "7500 300 7500";
SEffectManager.PlaySound("MyMod_Alert_SoundSet", pos);
```

That is the whole config surface. Sound categories, attenuation curves, looping, format choices, and production tooling are owned by the [Audio](../04-file-formats/04-audio.md) chapter.

---

## CfgAddons: Preload Declarations

`CfgAddons` is an optional block that hints to the engine about preloading assets:

```cpp
class CfgAddons
{
    class PreloadAddons
    {
        class MyMod
        {
            list[] = {};       // List of addon names to preload (usually empty)
        };
    };
};
```

In practice, most mods declare this with an empty `list[]`. It ensures the engine recognizes the mod during the preload phase. Some mods skip it entirely without issues.

---

## Complete Annotated Examples

> **Note:** Lantern (by the fictional team Northlight) and NightPatrol are this wiki's constructed teaching mods, not published projects. The Lantern subsystems referenced below are built step by step in [Part 7: Architecture Patterns](../07-patterns/01-singletons.md).

### Framework Mod (Script-Only): Lantern_Core

The base library every other Lantern package depends on. Script-only: empty `units[]`/`weapons[]`, GUI resources, and all five concerns in one `CfgMods` entry.

```cpp
class CfgPatches
{
    class Lantern_Core_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = { "DZ_Scripts" };   // Extends vanilla script classes
    };
};

class CfgMods
{
    class Lantern_Core
    {
        name = "Lantern Core";
        dir = "Lantern_Core";
        author = "Northlight";
        overview = "Lantern Core - shared library and admin framework";
        inputs = "Lantern_Core/Scripts/Data/Inputs.xml";
        type = "mod";
        defines[] = { "LANTERN_CORE" };        // Presence flag for downstream mods
        dependencies[] = { "Core", "Game", "World", "Mission" };

        class defs
        {
            class imageSets
            {
                files[] =
                {
                    "Lantern_Core/GUI/imagesets/lnt_prefabs.imageset",
                    "Lantern_Core/GUI/imagesets/lnt_hud.imageset",
                    "Lantern_Core/GUI/imagesets/lnt_icons.imageset"
                };
            };
            class widgetStyles
            {
                files[] =
                {
                    "Lantern_Core/GUI/looknfeel/lnt_prefabs.styles"
                };
            };
            class engineScriptModule
            {
                files[] = { "Lantern_Core/Scripts/1_Core" };
            };
            class gameScriptModule
            {
                files[] = { "Lantern_Core/Scripts/3_Game" };
            };
            class worldScriptModule
            {
                files[] = { "Lantern_Core/Scripts/4_World" };
            };
            class missionScriptModule
            {
                files[] = { "Lantern_Core/Scripts/5_Mission" };
            };
        };
    };
};
```

### Dependent Mod with a Common Folder: Lantern_Admin

An admin-tools package that builds on Lantern_Core. Two things to study here: the `requiredAddons` entry that guarantees Lantern_Core compiles first, and the Common-folder `files[]` pattern that compiles shared code into every script module.

```cpp
class CfgPatches
{
    class Lantern_Admin_Scripts
    {
        requiredVersion = 0.1;
        requiredAddons[] = { "Lantern_Core_Scripts", "DZ_Data" };
        // units[] and weapons[] omitted on purpose -- see note below
    };
};

class CfgMods
{
    class Lantern_Admin
    {
        name = "Lantern Admin Tools";
        dir = "Lantern_Admin";
        author = "Northlight";
        type = "mod";
        defines[] = { "LANTERN_ADMIN" };
        dependencies[] = { "Game", "World", "Mission" };

        class defs
        {
            class gameScriptModule
            {
                value = "";
                files[] =
                {
                    "Lantern_Admin/Scripts/Common",    // Shared helpers, visible in every module
                    "Lantern_Admin/Scripts/3_Game"
                };
            };
            class worldScriptModule
            {
                value = "";
                files[] =
                {
                    "Lantern_Admin/Scripts/Common",
                    "Lantern_Admin/Scripts/4_World"
                };
            };
            class missionScriptModule
            {
                value = "";
                files[] =
                {
                    "Lantern_Admin/Scripts/Common",
                    "Lantern_Admin/Scripts/5_Mission"
                };
            };
        };
    };
};
```

> **Note:** This `CfgPatches` block omits `units[]` and `weapons[]` entirely. These arrays are optional -- they default to empty when not declared. Script-only PBOs that add no spawnable entities or weapons can safely leave them out.

### Server-Only Feature Mod: Lantern_MissionsServer

Loaded via `-serverMod=`, so this separate package is not broadcast to clients. It depends on both the client-side missions package and the core library.

```cpp
class CfgPatches
{
    class Lantern_MissionsServer_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = { "DZ_Scripts", "Lantern_Missions_Scripts", "Lantern_Core_Scripts" };
    };
};

class CfgMods
{
    class Lantern_MissionsServer
    {
        name = "Lantern Missions Server";
        dir = "Lantern_MissionsServer";
        author = "Northlight";
        type = "mod";                    // Documented CfgMods value; -serverMod routes the folder
        defines[] = { "LANTERN_MISSIONSSERVER" };
        dependencies[] = { "Core", "Game", "World", "Mission" };

        class defs
        {
            class gameScriptModule
            {
                files[] = { "Lantern_MissionsServer/Scripts/3_Game" };
            };
            class worldScriptModule
            {
                files[] = { "Lantern_MissionsServer/Scripts/4_World" };
            };
            class missionScriptModule
            {
                files[] = { "Lantern_MissionsServer/Scripts/5_Mission" };
            };
        };
    };
};
```

### UI Kit with gameLibScriptModule and CfgVehicles: Lantern_UI

A GUI-focused package showing two rarer features in one config: the layer-2 `gameLibScriptModule`, and entity definitions living side by side with script declarations.

```cpp
class CfgPatches
{
    class Lantern_UI_Scripts
    {
        requiredVersion = 0.1;
        requiredAddons[] = { "DZ_Scripts", "Lantern_Core_Scripts" };
    };
};

class CfgMods
{
    class Lantern_UI
    {
        name = "Lantern UI Kit";
        dir = "Lantern_UI";
        author = "Northlight";
        type = "mod";
        dependencies[] = { "Game", "World", "Mission" };

        class defs
        {
            class imageSets
            {
                files[] =
                {
                    "Lantern_UI/GUI/imagesets/lnt_icons.imageset"
                };
            };
            class widgetStyles
            {
                files[] =
                {
                    "Lantern_UI/GUI/looknfeel/lnt_widgets.styles"
                };
            };
            class engineScriptModule
            {
                value = "";
                files[] = { "Lantern_UI/Scripts/1_Core" };
            };
            class gameLibScriptModule      // Rare: layer 2, for GameLib-dependent code
            {
                value = "";
                files[] = { "Lantern_UI/Scripts/2_GameLib" };
            };
            class gameScriptModule
            {
                value = "";
                files[] = { "Lantern_UI/Scripts/3_Game" };
            };
            class worldScriptModule
            {
                value = "";
                files[] = { "Lantern_UI/Scripts/4_World" };
            };
            class missionScriptModule
            {
                value = "";
                files[] = { "Lantern_UI/Scripts/5_Mission" };
            };
        };
    };
};

class CfgVehicles
{
    class HouseNoDestruct;                       // Vanilla static-object parent
    class LNT_SignalLampBase : HouseNoDestruct
    {
        scope = 0;                               // Abstract base -- shared properties
    };
    class LNT_SignalLampRed : LNT_SignalLampBase
    {
        scope = 1;                               // Static map object
    };
    class LNT_SignalLampGreen : LNT_SignalLampBase
    {
        scope = 1;
    };
};
```

---

## Common Mistakes

### 1. Wrong requiredAddons -- Mod Loads Before Its Dependency

```cpp
// WRONG: Your mod builds on Lantern Core but does not declare it,
// so it may load before Lantern Core
class CfgPatches
{
    class MyMod_Scripts
    {
        requiredAddons[] = { "DZ_Data" };  // Lantern_Core_Scripts not listed!
    };
};

// RIGHT: Declare ALL dependencies
class CfgPatches
{
    class MyMod_Scripts
    {
        requiredAddons[] = { "DZ_Data", "Lantern_Core_Scripts" };
    };
};
```

**Symptom:** Undefined type errors for classes from the dependency. The mod loaded before the dependency was compiled.

### 2. Missing Script Module Paths

```cpp
// WRONG: You have a Scripts/4_World/ folder but forgot to declare it
class defs
{
    class gameScriptModule
    {
        files[] = { "MyMod/Scripts/3_Game" };
    };
    // 4_World is missing! All .c files in 4_World/ are ignored.
};

// RIGHT: Declare every layer you use
class defs
{
    class gameScriptModule
    {
        files[] = { "MyMod/Scripts/3_Game" };
    };
    class worldScriptModule
    {
        files[] = { "MyMod/Scripts/4_World" };
    };
};
```

**Symptom:** Classes you defined simply do not exist. No error -- they are silently not compiled.

### 3. Wrong File Paths (Case Sensitivity)

While Windows is case-insensitive, DayZ paths can be case-sensitive in certain contexts (Linux servers, PBO packing):

```cpp
// RISKY: Mixed case that may fail on Linux
files[] = { "mymod/scripts/3_game" };   // Folder is actually "MyMod/Scripts/3_Game"

// SAFE: Match the actual directory case exactly
files[] = { "MyMod/Scripts/3_Game" };
```

### 4. CfgPatches Class Name Collision

```cpp
// WRONG: Using a common name that might collide with another mod
class CfgPatches
{
    class Scripts              // Too generic! Will collide.
    {
        // ...
    };
};

// RIGHT: Use a unique prefix
class CfgPatches
{
    class MyMod_Scripts        // Unique to your mod
    {
        // ...
    };
};
```

### 5. Circular requiredAddons

```cpp
// ModA config.cpp
requiredAddons[] = { "ModB_Scripts" };

// ModB config.cpp
requiredAddons[] = { "ModA_Scripts" };  // CIRCULAR! Engine fails to resolve.
```

### 6. Declaring dependencies[] Without Matching Script Modules

```cpp
// WRONG: Listed "World" as dependency but have no worldScriptModule
dependencies[] = { "Game", "World", "Mission" };

class defs
{
    class gameScriptModule
    {
        files[] = { "MyMod/Scripts/3_Game" };
    };
    // No worldScriptModule declared -- "World" dependency is misleading
    class missionScriptModule
    {
        files[] = { "MyMod/Scripts/5_Mission" };
    };
};
```

This does not cause an error, but it is misleading. Only list dependencies you actually use.

### 7. Putting CfgVehicles in the Scripts config.cpp

It works, but is poor practice. Keep item/entity definitions in a separate PBO (`Data/config.cpp`) and script definitions in `Scripts/config.cpp`.

### 8. An Empty String in units[]/weapons[]/magazines[]/ammo[]

```cpp
// WRONG -- a lone empty-string entry
class CfgPatches
{
    class MyMod_SomeGun_CFG
    {
        units[] = {};
        weapons[] = {};
        magazines[] = { "MyMod_SomeGun_Mag" };
        ammo[] = { "" };          // <-- looks harmless, is not
        requiredAddons[] = { "DZ_Data", "DZ_Weapons_Firearms" };
    };
};

// RIGHT -- an empty array, not an array containing an empty string
ammo[] = {};
```

These four arrays inside `CfgPatches` are **ownership claims**, resolved by the engine's addon-graph merger against every other loaded addon. A literal `""` asks the merger to resolve a class named the empty string, which is not a meaningful classname. No published source documents a specific crash signature for it, so treat any particular failure mode as anecdotal; the reliable point is the practical risk, because this typo is easy to introduce in a large or generated config and easy to miss visually. If you inherited or generated a large config (a merge of many vendor-supplied per-addon files is the most common source), grep every `units[]`/`weapons[]`/`magazines[]`/`ammo[]` array inside `CfgPatches` for a bare `""` -- a naive "extract quoted strings" regex (`"([^"]+)"`, one-or-more characters) will not find it, because it requires at least one character inside the quotes. Use a zero-or-more pattern (`"([^"]*)"`) or check for it explicitly, and test any suspect config on a non-production server before deploying it.

### 9. A Class Missing Its Terminating Semicolon

```cpp
// WRONG -- a missing ";" after a class body is a config syntax error
class MyMod_SomeItem_CFG
{
    requiredAddons[] = {};
    units[] = {};
    weapons[] = {};
}
class MyMod_NextItem_CFG
{
    ...
};

// RIGHT -- every class body ends with "};"
class MyMod_SomeItem_CFG
{
    requiredAddons[] = {};
    units[] = {};
    weapons[] = {};
};
```

This is easy to introduce with any script or merge tool that splits a config file on `;` to find class boundaries and then forgets to write that same `;` back out for each piece it re-emits.

Binarizing is the usual place a defect like this surfaces. The community wiki's [Config.cpp/bin File Format](https://community.bistudio.com/wiki/Config.cpp/bin_File_Format) page states that shipping a binarised config "guarantees the config.cpp it came from was syntactically correct (no missing semicolons, duplicate or missing classes, etc.)". That page carries Bohemia's "contains unofficial information" banner, so read it as a community description of the toolchain rather than a vendor guarantee, and do not assume binarization is the only stage that can reject a config. The guidance holds regardless of which stage catches it: check that every class body, not just the outermost containers, ends in `};`, especially in merged or auto-generated configs, and ship a binarised `config.bin` so the check happens at build time instead of at boot.

---

## Complete Template

Here is a production-ready `Scripts/config.cpp` template you can copy and modify:

```cpp
// ============================================================================
// Scripts/config.cpp -- MyMod Script Module Definitions
// ============================================================================

class CfgPatches
{
    class MyMod_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data",
            "DZ_Scripts"
            // Add your framework dependency patch names here
        };
    };
};

class CfgMods
{
    class MyMod
    {
        dir = "MyMod";
        name = "My Mod";
        author = "YourName";
        credits = "YourName";
        overview = "A brief description of what this mod does.";
        type = "mod";

        defines[] =
        {
            "MYMOD_LOADED"
            // "MYMOD_DEBUG"      // Uncomment for debug builds
        };

        dependencies[] = { "Game", "World", "Mission" };

        class defs
        {
            class imageSets
            {
                files[] = {};     // Add .imageset paths here
            };

            class widgetStyles
            {
                files[] = {};     // Add .styles paths here
            };

            class gameScriptModule
            {
                value = "";
                files[] = { "MyMod/Scripts/3_Game" };
            };

            class worldScriptModule
            {
                value = "";
                files[] = { "MyMod/Scripts/4_World" };
            };

            class missionScriptModule
            {
                value = "";
                files[] = { "MyMod/Scripts/5_Mission" };
            };
        };
    };
};
```
