# File Organization Best Practices


---

> **Summary:** How you organize files determines whether your mod is maintainable at 10 files or 1,000. This chapter covers the canonical directory structure, naming conventions, content vs script vs framework mods, client-server splits, and complete worked example layouts.

---

## Table of Contents

- [The Canonical Directory Structure](#the-canonical-directory-structure)
- [Naming Conventions](#naming-conventions)
- [Three Types of Mods](#three-types-of-mods)
- [Client-Server Split Mods](#client-server-split-mods)
- [What Goes Where](#what-goes-where)
- [PBO Naming and @mod Folder Naming](#pbo-naming-and-mod-folder-naming)
- [Worked Example Layouts](#worked-example-layouts)
- [Anti-Patterns](#anti-patterns)

---

## The Canonical Directory Structure

This is the standard layout used by professional DayZ mods. Not every folder is required -- only create what you need.

```
MyMod/                                    <-- Project root (development)
  mod.cpp                                 <-- Launcher metadata
  stringtable.csv                         <-- Localization; shown at the dev-tree root for
                                               convenience, but it must end up at the ROOT OF A
                                               PACKED PBO beside that PBO's config.cpp
                                               (see "Anti-Patterns" below)

  Scripts/                                <-- Script PBO root
    config.cpp                            <-- CfgPatches + CfgMods + script module defs
    Inputs.xml                            <-- Custom keybindings (optional)
    Data/
      Credits.json                        <-- Author credits
      Version.hpp                         <-- Version string (optional)

    1_Core/                               <-- engineScriptModule (rare)
      MyMod/
        Constants.c

    3_Game/                               <-- gameScriptModule
      MyMod/
        MyModConfig.c                     <-- Configuration class
        MyModRPCs.c                       <-- RPC identifiers / registration
        Data/
          SomeDataClass.c                 <-- Pure data structures

    4_World/                              <-- worldScriptModule
      MyMod/
        Entities/
          MyCustomItem.c                  <-- Custom items
          MyCustomVehicle.c
        Managers/
          MyModManager.c                  <-- World-aware managers
        Actions/
          ActionMyCustom.c                <-- Custom player actions

    5_Mission/                            <-- missionScriptModule
      MyMod/
        MyModRegister.c                   <-- Mod registration (startup hook)
        GUI/
          MyModPanel.c                    <-- UI panel scripts
          MyModHUD.c                      <-- HUD overlay scripts

  GUI/                                    <-- GUI PBO root (separate from Scripts)
    config.cpp                            <-- GUI-specific config (imageSets, styles)
    layouts/                              <-- .layout files
      mymod_panel.layout
      mymod_hud.layout
    imagesets/                            <-- .imageset files + texture atlases
      mymod_icons.imageset
      mymod_icons.edds
    looknfeel/                            <-- .styles files
      mymod.styles

  Data/                                   <-- Data PBO root (models, textures, items)
    config.cpp                            <-- CfgVehicles, CfgWeapons, etc.
    Models/
      my_item.p3d                         <-- 3D models
    Textures/
      my_item_co.paa                      <-- Color textures
      my_item_nohq.paa                    <-- Normal maps
    Materials/
      my_item.rvmat                       <-- Material definitions

  Sounds/                                 <-- Sound files
    alert.ogg                             <-- Audio files (always .ogg)
    ambient.ogg

  ServerFiles/                            <-- Files for server admins to copy
    types.xml                             <-- Central Economy spawn definitions
    cfgspawnabletypes.xml                 <-- Attachment presets
    README.md                             <-- Installation guide

  Keys/                                   <-- Signature keys
    MyMod.bikey                           <-- Public key for server verification
```

---

## Naming Conventions

### Mod/Project Names

Use PascalCase with a clear prefix. The examples below use the wiki's fictional **Lantern** framework family and the fictional **NightPatrol** content mod:

```
Lantern_Core         <-- Framework package, class prefix: LNT_
Lantern_Missions     <-- Feature mod built on the framework
Lantern_Admin        <-- Admin tool built on the framework
NightPatrol          <-- Content mod, class prefix: NP_ (skips the underscore in the mod name)
```

### Class Names

Use a short prefix unique to your mod, followed by an underscore and the class purpose. Three styles you will encounter:

```c
// Framework prefix style: LNT_[Name]
// Every class in the Lantern framework carries the same short tag.
class LNT_ModuleWorld {}
class LNT_EventArgs {}
class LNT_Log {}

// Content-mod short-tag style: NP_[Name]
// A two-letter tag keeps long item class names readable.
class NP_PatrolFlashlight {}
class NP_SignalFlare {}

// Unprefixed manager-noun style: [Name]Manager
// Some mods skip the prefix entirely. Readable, but risky:
// another mod defining the same name collides at compile time.
class ChatCommandManager {}
class WebhookManager {}
```

**Rules:**
- Prefix prevents collisions with other mods
- Keep it short (2-4 characters)
- Be consistent within your mod
- Avoid the unprefixed style unless your class names are already highly specific

### File Names

Name each file after the primary class it contains:

```
LNT_Log.c            <-- Contains class LNT_Log
LNT_RPC.c            <-- Contains class LNT_RPC
MyModConfig.c        <-- Contains class MyModConfig
ActionMyCustom.c     <-- Contains class ActionMyCustom
```

One class per file is the ideal. Multiple small helper classes in one file is acceptable when they are tightly coupled.

### Layout Files

Use lowercase with your mod prefix:

```
my_admin_panel.layout
my_killfeed_overlay.layout
mymod_settings_dialog.layout
```

### Variable Names

```c
// Member variables: m_ prefix
protected int m_Count;
protected ref array<string> m_Items;
protected ref LNT_ConfigBase m_Config;

// Static variables: s_ prefix
static int s_InstanceCount;
static ref LNT_Log s_Logger;

// Constants: ALL_CAPS
const int MAX_PLAYERS = 60;
const float UPDATE_INTERVAL = 0.5;
const string MOD_NAME = "MyMod";

// Local variables: camelCase (no prefix)
int count = 0;
string playerName = identity.GetName();
float deltaTime = timeArgs.DeltaTime;

// Parameters: camelCase (no prefix)
void SetConfig(LNT_ConfigBase config, bool forceReload)
```

---

## Three Types of Mods

DayZ mods fall into three categories. Each has a different structure emphasis.

### 1. Content Mod

Adds items, weapons, vehicles, buildings -- primarily 3D assets with minimal scripting.

```
MyWeaponPack/
  mod.cpp
  Data/
    config.cpp                <-- CfgVehicles, CfgWeapons, CfgMagazines, CfgAmmo
    Weapons/
      MyRifle/
        MyRifle.p3d
        MyRifle_co.paa
        MyRifle_nohq.paa
        MyRifle.rvmat
    Ammo/
      MyAmmo/
        MyAmmo.p3d
  Scripts/                    <-- Minimal (may not even exist)
    config.cpp
    4_World/
      MyWeaponPack/
        MyRifle.c             <-- Only if the weapon needs custom behavior
  ServerFiles/
    types.xml
```

**Characteristics:**
- Heavy on `Data/` (models, textures, materials)
- Heavy on `Data/config.cpp` (CfgVehicles, CfgWeapons definitions)
- Minimal or no scripting
- Scripts only when items need custom behavior beyond what config defines

### 2. Script Mod

Adds gameplay features, admin tools, systems -- primarily code with minimal assets.

```
MyAdminTools/
  mod.cpp
  stringtable.csv
  Scripts/
    config.cpp
    3_Game/
      MyAdminTools/
        Config.c
        RPCHandler.c
        Permissions.c
    4_World/
      MyAdminTools/
        PlayerManager.c
        VehicleManager.c
    5_Mission/
      MyAdminTools/
        AdminMenu.c
        AdminHUD.c
  GUI/
    layouts/
      admin_menu.layout
      admin_hud.layout
    imagesets/
      admin_icons.imageset
```

**Characteristics:**
- Heavy on `Scripts/` (most code in 3_Game, 4_World, 5_Mission)
- GUI layouts and imagesets for UI
- Little or no `Data/` (no 3D models)
- Usually depends on a framework (a shared library such as the wiki's Lantern example, or a custom one)

### 3. Framework Mod

Provides shared infrastructure for other mods -- logging, RPC, configuration, UI systems.

```
Lantern_Core/
  mod.cpp
  stringtable.csv
  Scripts/
    config.cpp
    Data/
      Credits.json
    1_Core/                     <-- Frameworks often use 1_Core
      Lantern/
        LNT_Constants.c
        LNT_LogLevel.c
    3_Game/
      Lantern/
        Config/
          LNT_ConfigManager.c
          LNT_ConfigBase.c
        RPC/
          LNT_RPC.c
        Events/
          LNT_EventBus.c
        Logging/
          LNT_Log.c
        Permissions/
          LNT_Permissions.c
        UI/
          LNT_ViewBase.c
          LNT_DialogBase.c
    4_World/
      Lantern/
        Module/
          LNT_ModuleManager.c
          LNT_ModuleBase.c
        Player/
          LNT_PlayerData.c
    5_Mission/
      Lantern/
        LNT_MissionHooks.c
        LNT_ModRegistration.c
  GUI/
    config.cpp
    layouts/
    imagesets/
    icons/
    looknfeel/
```

**Characteristics:**
- Uses all script layers (1_Core through 5_Mission)
- Deep subdirectory hierarchy in each layer
- Defines `defines[]` for feature detection
- Other mods depend on it via `requiredAddons`
- Provides base classes that other mods extend

---

## Client-Server Split Mods

When a mod has both client-visible behavior (UI, entity rendering) and server-only logic (spawning, AI brains, secure state), it should split into two packages.

### Directory Structure

```
MyMod/                                    <-- Project root (development repo)
  MyMod_Sub/                           <-- Client package (loaded via -mod=)
    mod.cpp
    stringtable.csv
    Scripts/
      config.cpp                          <-- type = "mod"
      3_Game/MyMod/                       <-- Shared data classes, RPCs
      4_World/MyMod/                      <-- Client-side entity rendering
      5_Mission/MyMod/                    <-- Client UI, HUD
    GUI/
      layouts/
    Sounds/

  MyMod_SubServer/                     <-- Server package (loaded via -serverMod=)
    mod.cpp
    Scripts/
      config.cpp                          <-- type = "servermod"
      3_Game/MyModServer/                 <-- Server-side data classes
      4_World/MyModServer/                <-- Spawning, AI logic, state management
      5_Mission/MyModServer/              <-- Server startup/shutdown hooks
```

### Key Rules for Split Mods

1. **The client package is loaded by everyone** (server and all clients via `-mod=`)
2. **The server package is loaded only by the server** (via `-serverMod=`)
3. **The server package depends on the client package** (via `requiredAddons`)
4. **Never put UI code in the server package** -- clients will not receive it
5. **Keep secure/private logic in the server package** -- it is never sent to clients

### Dependency Chain

```cpp
// Client package config.cpp
class CfgPatches
{
    class MyMod_Sub_Scripts
    {
        requiredAddons[] = { "DZ_Scripts", "MyMod_Core_Scripts" };
    };
};

// Server package config.cpp
class CfgPatches
{
    class MyMod_SubServer_Scripts
    {
        requiredAddons[] = { "DZ_Scripts", "MyMod_Sub_Scripts", "MyMod_Core_Scripts" };
        //                                  ^^^ depends on client package
    };
};
```

### Worked Example: Missions Client-Server Split

Using the wiki's fictional Lantern mod family:

```
Lantern_Missions/
  Lantern_Missions/                       <-- Client (-mod=)
    mod.cpp                               type = "mod"
    Scripts/
      config.cpp                          requiredAddons: Lantern_Core_Scripts
      3_Game/Lantern_Missions/            Shared enums, config, RPC IDs
      4_World/Lantern_Missions/           Mission markers (client rendering)
      5_Mission/Lantern_Missions/         Mission UI, radio HUD
    GUI/layouts/                          Mission panel layouts
    Sounds/                               Radio beep sounds

  Lantern_MissionsServer/                 <-- Server (-serverMod=)
    mod.cpp                               type = "servermod"
    Scripts/
      config.cpp                          requiredAddons: Lantern_Missions_Scripts, Lantern_Core_Scripts
      3_Game/Lantern_MissionsServer/      Server config extensions
      4_World/Lantern_MissionsServer/     Mission spawner, loot manager
      5_Mission/Lantern_MissionsServer/   Server mission lifecycle
```

---

## What Goes Where

### Data/ Directory

Physical assets and item definitions:

```
Data/
  config.cpp          <-- CfgVehicles, CfgWeapons, CfgMagazines, CfgAmmo
  Models/             <-- .p3d 3D model files
  Textures/           <-- .paa, .edds texture files
  Materials/          <-- .rvmat material definitions
  Animations/         <-- .anim animation files (rare)
```

### Scripts/ Directory

All Enforce Script code:

```
Scripts/
  config.cpp          <-- CfgPatches, CfgMods, script module definitions
  Inputs.xml          <-- Keybinding definitions
  Data/
    Credits.json      <-- Author credits
    Version.hpp       <-- Version string
  1_Core/             <-- Fundamental constants and utilities
  3_Game/             <-- Configs, RPCs, data classes
  4_World/            <-- Entities, managers, gameplay logic
  5_Mission/          <-- UI, HUD, mission lifecycle
```

### GUI/ Directory

User interface resources:

```
GUI/
  config.cpp          <-- GUI-specific CfgPatches (for imageset/style registration)
  layouts/            <-- .layout files (widget trees)
  imagesets/          <-- .imageset XML + .edds texture atlases
  icons/              <-- Icon imagesets (may be separate from general imagesets)
  looknfeel/          <-- .styles files (widget visual properties)
  fonts/              <-- Custom font files (rare)
  sounds/             <-- UI sound files (click, hover, etc.)
```

### Sounds/ Directory

Audio files:

```
Sounds/
  alert.ogg           <-- Always .ogg format
  ambient.ogg
  click.ogg
```

Sound config (CfgSoundSets, CfgSoundShaders) goes in `Scripts/config.cpp`, not in a separate Sounds config.

### ServerFiles/ Directory

Files that server administrators copy to their server's mission folder:

```
ServerFiles/
  types.xml                   <-- Item spawn definitions for Central Economy
  cfgspawnabletypes.xml       <-- Attachment/cargo presets
  cfgeventspawns.xml          <-- Event spawn positions (rare)
  README.md                   <-- Installation instructions
```

---

## PBO Naming and @mod Folder Naming

### PBO Names

Each PBO gets a descriptive name with the mod prefix:

```
@MyMod/
  Addons/
    MyMod_Scripts.pbo         <-- Script code
    MyMod_Data.pbo            <-- Models, textures, items
    MyMod_GUI.pbo             <-- Layouts, imagesets, styles
    MyMod_Sounds.pbo          <-- Audio (sometimes bundled with Data)
```

The PBO filename, its virtual prefix, its `CfgPatches` class, and the containing `@` folder have separate roles. A filename does not need to match the `CfgPatches` class, although a clear manifest mapping prevents confusion. Do not assume a one-to-one PBO-to-addon mapping: a PBO can expose additional configuration roots, and resource archives can be laid out without a root config.

### @mod Folder Name

The `@` prefix is a Steam Workshop convention. During development, you may omit it:

```
Development:    MyMod/           <-- No @ prefix
Workshop:       @MyMod/          <-- With @ prefix
```

The `@` has no technical meaning to the engine. It is purely organizational convention.

### Multiple PBOs Per Mod

Large mods split into multiple PBOs for several reasons:

1. **Separate update cycles** -- update scripts without re-downloading 3D models
2. **Clear ownership** -- scripts, data, and GUI resources can have separate source and staging roots
3. **Build pipeline** -- different PBOs built by different tools

```
@MyMod_Weapons/
  Addons/
    MyMod_Weapons_Scripts.pbo    <-- Script behavior
    MyMod_Weapons_Data.pbo       <-- Weapon models, textures, configs
```

Each independently load-ordered configuration addon needs a unique `CfgPatches` entry. `requiredAddons[]` uses those class names, not PBO filenames or prefixes, to declare initialization dependencies:

```cpp
// Scripts/config.cpp
class CfgPatches
{
    class MyMod_Weapons_Scripts
    {
        requiredAddons[] = { "DZ_Scripts", "DZ_Weapons_Firearms" };
    };
};

// Data/config.cpp
class CfgPatches
{
    class MyMod_Weapons_Data
    {
        requiredAddons[] = { "DZ_Data", "DZ_Weapons_Firearms" };
    };
};
```

---

## Worked Example Layouts

The trees below are constructed teaching examples built around the wiki's fictional **Lantern** mod family (the framework whose code is developed in Part 7) and the fictional **NightPatrol** content mod. Each one condenses a layout pattern commonly seen in large published mods.

### Framework Mod: Lantern_Core

A full-featured framework uses every script layer and splits each layer into subsystem folders:

```
Lantern_Core/
  Lantern_Core/                           <-- Client package
    mod.cpp
    stringtable.csv
    GUI/
      config.cpp
      fonts/
      icons/                              <-- Icon weight imagesets
      imagesets/
      layouts/
        Lantern/AdminPanel/
        Lantern/Dialogs/
        Lantern/Modules/
        Lantern/Options/
        Lantern/Prefabs/
        Lantern/Tooltip/
      looknfeel/
      sounds/
    Scripts/
      config.cpp
      Inputs.xml
      1_Core/Lantern/                     <-- Log levels, constants
      2_GameLib/Lantern/UI/               <-- MVC attribute system
      3_Game/Lantern/                     <-- One folder per subsystem
        Chat/
        Config/
        Core/
        Events/
        Logging/
        Module/
        MVC/
        Notifications/
        Permissions/
        PlayerData/
        RPC/
        Settings/
        Theme/
        Timer/
        UI/
      4_World/Lantern/                    <-- Player data, world managers
      5_Mission/Lantern/                  <-- Admin panel, mod registration

  Lantern_Core_Server/                    <-- Server package
    mod.cpp
    Scripts/
      config.cpp
      ...
```

### Admin Tool: Lantern_Admin -- Umbrella Directory + Common Folder

Some teams wrap every mod they ship inside a single top-level "umbrella" directory named after the team. All internal paths then start with the team name, which guarantees no path collision with any other mod. Here the fictional Northlight team packs its `Lantern_Admin` tool under `Northlight/Admin/`:

```
Northlight/Admin/                         <-- Umbrella dir: team name wraps the mod folder
  mod.cpp
  GUI/
    config.cpp
    layouts/
      cursors/
      dialogs/
      vehicles/
    textures/
  Objects/Debug/
    config.cpp                            <-- Debug entity definitions
  Scripts/
    config.cpp
    Data/
      Credits.json
      Version.hpp
      Inputs.xml
    Common/                               <-- Shared across all layers
    1_Core/
    3_Game/
    4_World/
    5_Mission/
  Language/
    config.cpp                            <-- Dedicated string table PBO
```

Note the `Common/` folder pattern: it is listed in every script module's `files[]` in `config.cpp`, so its types compile into all layers -- a way to share utility classes without duplicating them per layer.

### Content Mod: NightPatrol Weapon Pack

```
NightPatrol/
  NightPatrol/
    mod.cpp
    Data/
      config.cpp                          <-- CfgWeapons, CfgMagazines, CfgAmmo definitions
      Ammo/                               <-- Organized by caliber
        556x45/
        762x39/
        9x19/
      Attachments/                        <-- Scopes, suppressors, grips
      Magazines/
      Weapons/                            <-- One folder per weapon model
    Scripts/
      config.cpp                          <-- Script module definitions
      3_Game/NightPatrol/                 <-- Weapon config, stat constants
      4_World/NightPatrol/                <-- Weapon behavior overrides
      5_Mission/NightPatrol/              <-- Registration, UI
```

Content mods have a massive `Data/` directory and relatively small `Scripts/`.

### UI Kit: Lantern_UI -- and a files[] Casing Trap

```
Lantern_UI/
  mod.cpp
  GUI/
    config.cpp
    imagesets/
    icons/
      lnt_brands.imageset
      lnt_light.imageset
      lnt_regular.imageset
      lnt_solid.imageset
      lnt_thin.imageset
    looknfeel/
  Scripts/
    config.cpp
    Credits.json
    Version.hpp
    1_Core/
    2_GameLib/                            <-- One of the few uses of layer 2
    3_Game/
    4_World/
    5_Mission/
```

A casing trap seen in published mods: the physical folders use canonical casing (`Scripts/`, `GUI/`, `1_Core/`), but the `config.cpp` `files[]` paths reference them in lowercase (`Lantern_UI/scripts/1_core`, `Lantern_UI/gui/...`). The mismatch works because Windows is case-insensitive, but it can break on Linux servers, which are case-sensitive. Keep your `files[]` paths matching the actual folder casing exactly.

---

## Anti-Patterns

### 1. Flat Script Dump

```
Scripts/
  3_Game/
    AllMyStuff.c            <-- 2000 lines, 15 classes
    MoreStuff.c             <-- 1500 lines, 12 classes
```

**Fix:** One file per class, organized in subdirectories by subsystem.

### 2. Wrong Layer Placement

```
Scripts/
  3_Game/
    MyMod/
      PlayerManager.c       <-- References PlayerBase (defined in 4_World)
      MyPanel.c             <-- UI code (belongs in 5_Mission)
      MyItem.c              <-- Extends ItemBase (belongs in 4_World)
```

**Fix:** Follow the layer rules from [The Five Script Layers](01-five-layers.md). Move entity code to `4_World` and UI code to `5_Mission`.

### 3. No Mod Subdirectory in Script Layers

```
Scripts/
  3_Game/
    Config.c                <-- Name collision risk with other mods!
    RPCs.c
```

**Fix:** Always namespace with a subdirectory:

```
Scripts/
  3_Game/
    MyMod/
      Config.c
      RPCs.c
```

### 4. Placing stringtable.csv Somewhere It Won't Be Packed

`stringtable.csv` belongs at the **root of a packed PBO, beside that PBO's `config.cpp`**. Bohemia's own `Test_Stringtable` sample ships exactly that and nothing else -- the addon source folder contains two files, `config.cpp` and `stringtable.csv`, side by side, with no `mod.cpp` anywhere in the sample. The general Real Virtuality documentation says the same thing in older words: the stringtable "must be located in the primary folder of the mission/addon/campaign."

Published mods vary in where they keep the file in their *development* tree -- some at the project root next to `mod.cpp`, some already at `Scripts/stringtable.csv` -- and that is fine, because only the packed result matters. The trap is shipping it at the mod root of the final `@MyMod/` distribution folder: that location sits outside `Addons/` and is never inside a PBO, so nothing reads it. Pick one PBO (commonly Scripts) to own the file, make sure your build step packs it at that PBO's root, and confirm with a test string in-game.

```
MyMod/
  Scripts/
    config.cpp               <-- PBO root
    stringtable.csv          <-- Beside it, exactly as Bohemia's Test_Stringtable sample ships
```

### 5. Mixed Assets and Scripts in One PBO

```
MyMod/
  config.cpp
  Scripts/3_Game/...
  Models/weapon.p3d
  Textures/weapon_co.paa
```

**Fix:** Separate into multiple PBOs:

```
MyMod/
  Scripts/
    config.cpp
    3_Game/...
  Data/
    config.cpp
    Models/weapon.p3d
    Textures/weapon_co.paa
```

### 6. Deeply Nested Subdirectories

```
Scripts/3_Game/MyMod/Systems/Core/Config/Managers/Settings/PlayerSettings.c
```

**Fix:** Keep nesting to 2-3 levels maximum. Flatten when possible:

```
Scripts/3_Game/MyMod/Config/PlayerSettings.c
```

### 7. Inconsistent Naming

```
mymod_Config.c
MyMod_rpc.c
MYMOD_Manager.c
my_mod_panel.c
```

**Fix:** Pick one convention and stick with it:

```
MyModConfig.c
MyModRPC.c
MyModManager.c
MyModPanel.c
```

---

## Summary Checklist

Before publishing your mod, verify:

- [ ] `mod.cpp` is at the mod root (next to `Addons/` or `Scripts/`)
- [ ] `stringtable.csv` is packed at a PBO root beside that PBO's `config.cpp` (not left only in the unpacked dev-tree "mod root" next to `mod.cpp`) -- verify the localized strings show up in-game
- [ ] Every configuration addon has its `config.cpp` at that addon's PBO root
- [ ] `requiredAddons[]` lists ALL dependencies
- [ ] Script module `files[]` paths match the actual directory structure
- [ ] Every `.c` file is inside a mod-namespaced subdirectory (e.g., `3_Game/MyMod/`)
- [ ] Class names have a unique prefix to avoid collisions
- [ ] Entity classes are in `4_World`, UI classes are in `5_Mission`, data classes are in `3_Game`
- [ ] No secrets or debug code in the published PBOs
- [ ] Server-only logic is in a separate package loaded with `-serverMod=` (if applicable)

---

## Patterns Observed in Published Mods

| Pattern | Detail |
|---------|--------|
| Deep subsystem folders in `3_Game` | Large framework mods commonly have 15+ folders under `3_Game/` (Config, RPC, Events, Logging, Permissions, etc.) |
| `Common/` shared folder | Included in every script module's `files[]` to provide cross-layer utility types |
| Lowercase paths in `files[]` | Physical folders are `Scripts/`, `GUI/`, but `config.cpp` `files[]` reference them as lowercase (`scripts/`, `gui/`, `1_core`) -- works on Windows but risks issues on Linux |
| Separate GUI PBO | Common in large mods: GUI resources (layouts, imagesets, styles) packed into a dedicated PBO with its own config.cpp |
| Minimal Scripts for content mods | In weapon packs the `Data/` directory dominates; `Scripts/` has only a thin config.cpp and optional behavior overrides |

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| One class per file | Each `.c` file contains one class | Small helper classes and enums are often co-located with their parent class for convenience |
| Separate PBOs for Scripts/Data/GUI | Clean separation by concern | Small mods often merge everything into a single PBO to simplify distribution |
| Mod subfolder prevents collisions | `3_Game/MyMod/` namespaces files | True, but class names still collide globally -- the subfolder only prevents file-level conflicts |
| `stringtable.csv` at mod root | Engine finds it automatically | The documented layout is the root of a packed PBO, beside that PBO's `config.cpp`, as Bohemia's `Test_Stringtable` sample ships it. The dev-tree "mod root" next to `mod.cpp` is outside `Addons/` and is never packed by itself, so a file left only there is never read |
| ServerFiles/ ships with the mod | Server admins copy types.xml | Many mod authors forget to include ServerFiles, forcing admins to create types.xml entries manually |

---

## Compatibility & Impact

- **Multi-Mod:** File organization itself does not cause conflicts. Treat duplicate normalized virtual paths as a release-build failure by default; same-prefix winner behavior needs a controlled runtime test before you permit a documented exception.
- **Performance:** The engine recursively scans all listed `files[]` directories regardless of nesting depth. No published benchmark quantifies compile-time cost by directory depth, so treat "nesting is free" as a reasonable expectation rather than a measured fact; total script volume, not folder depth, is what drives compile time in practice. Organize for readability.
