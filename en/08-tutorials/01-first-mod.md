# Your First Mod (Hello World)


---

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Install DayZ Tools](#step-1-install-dayz-tools)
- [Step 2: Set Up the P: Drive (Workdrive)](#step-2-set-up-the-p-drive-workdrive)
- [Step 3: Create the Mod Directory Structure](#step-3-create-the-mod-directory-structure)
- [Step 4: Write mod.cpp](#step-4-write-mod-cpp)
- [Step 5: Write config.cpp](#step-5-write-config-cpp)
- [Step 6: Write Your First Script](#step-6-write-your-first-script)
- [Step 7: Pack the PBO with Addon Builder](#step-7-pack-the-pbo-with-addon-builder)
- [Step 8: Load the Mod in DayZ](#step-8-load-the-mod-in-dayz)
- [Step 9: Verify in the Script Log](#step-9-verify-in-the-script-log)
- [Step 10: Troubleshooting Common Issues](#step-10-troubleshooting-common-issues)
- [Complete File Reference](#complete-file-reference)
- [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, make sure you have:

- **Steam** installed and logged in
- **DayZ** game installed (retail version from Steam)
- A **text editor** (VS Code, Notepad++, or even Notepad)
- About **15 GB of free disk space** for DayZ Tools

That is everything.

---

## Step 1: Install DayZ Tools

DayZ Tools is a free application on Steam that includes everything you need to build mods: the Workbench script editor, Addon Builder for PBO packing, Terrain Builder, and Object Builder.

### How to Install

1. Open **Steam**
2. Go to **Library**
3. In the dropdown filter at the top, change **Games** to **Tools**
4. Search for **DayZ Tools**
5. Click **Install**
6. Wait for the download to complete. Budget several gigabytes, and note that the project drive you create in Step 2 needs a further 20 GB at minimum.

Before you launch the tools for the first time, **start DayZ itself at least once**. Bohemia calls this out explicitly: without it, Workbench fails with "game is not installed, exiting".

Once installed, you will find DayZ Tools in your Steam library under Tools. The default installation path is:

```
C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\
```

### What Gets Installed

| Tool | Purpose |
|------|---------|
| **Addon Builder** | Packs your mod files into `.pbo` archives |
| **Workbench** | Script editor with syntax highlighting |
| **Object Builder** | 3D model viewer and editor for `.p3d` files |
| **Terrain Builder** | Map/terrain editor |
| **TexView2** | Texture viewer/converter (`.paa`, `.edds`) |

For this tutorial, you only need **Addon Builder**. The others are useful later.

---

## Step 2: Set Up the P: Drive (Workdrive)

DayZ modding uses a virtual drive letter **P:** as a shared workspace. All mods and game data reference paths starting from P:, which keeps paths consistent across different machines.

### Creating the P: Drive

This is the procedure Bohemia documents, and it is two operations, not one: create the drive, then extract the game data onto it.

1. Launch **DayZ Tools** from Steam, choosing **Play DayZ Tools**
2. In the menu bar, click **Settings**
3. Untick **Default** next to the Project Drive path and choose a location with **at least 20 GB free**
4. In the **Drive Letter** dropdown, pick a letter. `P:\` is the recommended one and is what every guide, including this chapter, assumes
5. Click **Apply**
6. Back in the menu bar, go to **Tools > Extract Game Data**
7. Wait for it to finish -- this is the slow part, and it is the step that actually puts the game's files on the drive

### Verify It Works

Open **File Explorer** and navigate to `P:\`. You should see the extracted game data -- a `DZ` folder and a `scripts` folder among others. An empty or nearly empty `P:\` means step 6 did not run or did not complete; the drive mapping alone gets you nothing to reference.

### Alternative: Manual P: Drive

If the DayZ Tools GUI does not work, you can create a P: drive manually using a Windows command prompt (run as Administrator):

```batch
subst P: "C:\DayZWorkdrive"
```

Replace `C:\DayZWorkdrive` with any folder you want. This creates a temporary drive mapping that lasts until you reboot, and it maps a letter only -- it does **not** extract the game data, so you still need **Tools > Extract Game Data** from DayZ Tools pointed at that location before you can reference vanilla paths.

### What If I Do Not Want to Use P: Drive?

You can keep your source anywhere, but the official workflow puts it on the P: drive and so does every Bohemia walkthrough -- including the file-patching setup in Step 7, which links the DayZ installation folder to your source tree. Set it up; the rest of this chapter assumes it.

---

## Step 3: Create the Mod Directory Structure

Every DayZ mod follows a specific folder structure. Create the following directories and files on your P: drive (or in your DayZ game directory if not using P:):

```
P:\MyFirstMod\
    mod.cpp
    Scripts\
        config.cpp
        5_Mission\
            MyFirstMod\
                MissionHello.c
```

### Create the Folders

1. Open **File Explorer**
2. Navigate to `P:\`
3. Create a new folder called `MyFirstMod`
4. Inside `MyFirstMod`, create a folder called `Scripts`
5. Inside `Scripts`, create a folder called `5_Mission`
6. Inside `5_Mission`, create a folder called `MyFirstMod`

### Understanding the Structure

| Path | Purpose |
|------|---------|
| `MyFirstMod/` | Root of your mod |
| `mod.cpp` | Metadata (name, author) shown in the DayZ launcher |
| `Scripts/config.cpp` | Tells the engine what your mod depends on and where scripts live |
| `Scripts/5_Mission/` | The mission script layer (UI, startup hooks) |
| `Scripts/5_Mission/MyFirstMod/` | Subfolder for your mod's mission scripts |
| `Scripts/5_Mission/MyFirstMod/MissionHello.c` | Your actual script file |

That is three files: `mod.cpp`, `Scripts/config.cpp`, and one script. Steps 4 to 6 create them one at a time.

The folder name `MyFirstMod` is your mod's **root prefix**. It shows up again in the PBO prefix in Step 7, in the `files[]` paths inside `config.cpp`, and in the file-patching junction -- so pick it once and keep it consistent everywhere.

---

## Step 4: Write mod.cpp

Create the file `P:\MyFirstMod\mod.cpp` in your text editor and paste this content:

```cpp
name = "My First Mod";
author = "YourName";
version = "1.0";
overview = "My very first DayZ mod. Prints Hello World to the script log.";
```

### What Each Line Does

- **`name`** -- The display name shown in the DayZ launcher mod list. Players see this when selecting mods.
- **`author`** -- Your name or team name.
- **`version`** -- A free-form version string. Bohemia documents `mod.cpp` as presentation metadata, and nothing in the game's scripts reads `version`, so do not expect it to drive dependency or compatibility checks. Use it for humans.
- **`overview`** -- A description shown when expanding the mod details.

Save the file. That is your mod's identity card.

---

## Step 5: Write config.cpp

Create the file `P:\MyFirstMod\Scripts\config.cpp` and paste this content:

```cpp
class CfgPatches
{
    class MyFirstMod_Scripts
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
    class MyFirstMod
    {
        dir = "MyFirstMod";
        name = "My First Mod";
        author = "YourName";
        type = "mod";

        dependencies[] = { "Mission" };

        class defs
        {
            class missionScriptModule
            {
                value = "";
                files[] = { "MyFirstMod/Scripts/5_Mission" };
            };
        };
    };
};
```

### What Each Section Does

**CfgPatches** declares your mod to the DayZ engine:

- `class MyFirstMod_Scripts` -- A unique identifier for your mod's script package. Must not collide with any other mod.
- `units[] = {}; weapons[] = {};` -- Lists of entities and weapons your mod adds. Empty for now.
- `requiredVersion = 0.1;` -- Minimum game version. Always `0.1`.
- `requiredAddons[] = { "DZ_Data" };` -- Dependencies. `DZ_Data` is the base game data. This ensures your mod loads **after** the base game.

**CfgMods** tells the engine where your scripts live:

- `dir = "MyFirstMod";` -- Root directory of the mod.
- `type = "mod";` -- Declares the required CfgMods mod type. To keep an addon server-side, load it with the server startup parameter `-serverMod=`; do not change this value to `"servermod"`.
- `dependencies[] = { "Mission" };` -- Your code hooks into the Mission script module.
- `class missionScriptModule` -- Tells the engine to compile all `.c` files found in `MyFirstMod/Scripts/5_Mission/`.

**Why only `5_Mission`?** Because our Hello World script hooks into the mission startup event, which lives in the mission layer. Most simple mods start here.

---

## Step 6: Write Your First Script

Create the file `P:\MyFirstMod\Scripts\5_Mission\MyFirstMod\MissionHello.c` and paste this content:

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The SERVER mission has started.");
    }
};

modded class MissionGameplay
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The CLIENT mission has started.");
    }
};
```

### Line-by-Line Explanation

```c
modded class MissionServer
```
The `modded` keyword is the heart of DayZ modding. It says: "Take the existing `MissionServer` class from the vanilla game and add my changes on top." You are not creating a new class -- you are extending the existing one.

```c
    override void OnInit()
```
`OnInit()` is called by the engine when a mission starts. `override` tells the compiler that this method already exists in the parent class and we are replacing it with our version.

```c
        super.OnInit();
```
**This line is critical.** `super.OnInit()` calls the original vanilla implementation. If you skip this, the vanilla mission initialization code never runs and the game breaks. Always call `super` first.

```c
        Print("[MyFirstMod] Hello World! The SERVER mission has started.");
```
`Print()` writes a message to the DayZ script log file. The `[MyFirstMod]` prefix makes it easy to find your messages in the log.

```c
modded class MissionGameplay
```
`MissionGameplay` is the client-side equivalent of `MissionServer`. When a player joins a server, `MissionGameplay.OnInit()` fires on their machine. By modding both classes, your message appears in both server and client logs.

### About `.c` Files

DayZ scripts use the `.c` file extension. Despite looking like C, this is **Enforce Script**, DayZ's own scripting language. It has classes, inheritance, arrays, and maps, but it is not C, C++, or C#. Your IDE may show syntax errors -- that is normal and expected.

---

## Step 7: Pack the PBO with Addon Builder

DayZ loads mods from `.pbo` archive files (similar to .zip but in a format the engine understands). You need to pack your `Scripts` folder into a PBO.

### Using Addon Builder (GUI)

1. Open **DayZ Tools** from Steam
2. Click **Addon Builder** to launch it
3. Set **Source directory** to: `P:\MyFirstMod\Scripts\`
4. Set **Output/Destination directory** to a new folder: `P:\Mods\@MyFirstMod\addons\`

   Create `P:\Mods\@MyFirstMod\addons\` first if it does not exist. Keep `addons` (and later `keys`) **lowercase**, along with the files inside them -- Bohemia's packing instructions call this out because the DayZ Linux server binaries are case-sensitive.

5. In **Addon Builder Options**:
   - Set **Prefix** to: `MyFirstMod\Scripts`
   - At the bottom left, select **Options** and set **path to project folder** to your work drive (`P:\`)
   - Leave other options at defaults
6. Click **Pack**. If it fails, enable **Enable extended logging** to see why, or try it with **Binarize** unchecked.

If successful, you will see a file at:

```
P:\Mods\@MyFirstMod\addons\Scripts.pbo
```

### Set Up the Final Mod Structure

Now copy your `mod.cpp` next to the `Addons` folder:

```
P:\Mods\@MyFirstMod\
    mod.cpp                         <-- Copy from P:\MyFirstMod\mod.cpp
    addons\
        Scripts.pbo                 <-- Created by Addon Builder
```

The `@` prefix on the folder name is a convention for distributable mods. It signals to server administrators and the launcher that this is a mod package.

### Set Up File Patching for Fast Iteration

File patching lets the engine read loose `.c` files from your source tree, so a script edit costs a reconnect instead of a repack. It is layered **on top of** the packed mod you just built -- you do not skip packing, and `-mod=` keeps pointing at `@MyFirstMod`.

One extra step is needed: a directory junction that makes your source tree visible inside the DayZ installation folder, under your mod's root prefix (`MyFirstMod`). Run it once, in a command prompt, substituting your own DayZ path:

```batch
mklink /J "C:\Program Files (x86)\Steam\steamapps\common\DayZ\MyFirstMod" "P:\MyFirstMod"
```

Open the DayZ installation folder afterwards: a `MyFirstMod` entry should be there, and browsing into it should show the same `Scripts` folder you created on `P:`. If it does not, file patching will silently do nothing.

Two more conditions:

- File patching works only with the diagnostic executable, `DayZDiag_x64.exe` -- never with the retail build, and never for distribution.
- Any server you connect to needs `allowFilePatching = 1;` in its `serverDZ.cfg`, or your client will be refused. For a local diag server also set `BattlEye = 0;` and `verifySignatures = 0;`.

With that in place, a `.c` edit applies on the next reconnect or mission restart. A `config.cpp` edit does not: repack and relaunch. [Chapter 8.6](06-debugging-testing.md#file-patching-edit-without-rebuilding) explains why, and what the official documentation does and does not settle.

---

## Step 8: Load the Mod in DayZ

There are two ways to load your mod: through the launcher or via command-line parameters.

### Option A: DayZ Launcher

1. Open the **DayZ Launcher** from Steam
2. Go to the **Mods** tab
3. Click **Add local mod** (or "Add mod from local storage")
4. Browse to `P:\@MyFirstMod\`
5. Enable the mod by checking its checkbox
6. Click **Play** (make sure you are connecting to a local/offline server, or launching single-player)

### Option B: Command Line (Recommended for Development)

For faster iteration, launch DayZ directly with command-line parameters. Create a shortcut or batch file:

**Diagnostic executable, with file patching (needs the junction from Step 7):**

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" "-mod=P:\Mods\@MyFirstMod" -filePatching -server -config=serverDZ.cfg -port=2302
```

**Diagnostic executable, packed PBO only (what players will run, minus the diag build):**

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" "-mod=P:\Mods\@MyFirstMod" -server -config=serverDZ.cfg -port=2302
```

The `-server` flag launches a local listen server. `-filePatching` adds the loose-file path on top of the packed mod; the `serverDZ.cfg` you point at needs `allowFilePatching = 1;` for a file-patching client to connect. Test the second form too before you release -- it is the one that proves your PBO is actually complete.

### Quick Test: Offline Mode

The fastest way to test is to launch DayZ in offline mode:

```batch
DayZDiag_x64.exe "-mod=P:\Mods\@MyFirstMod" -filePatching
```

For offline testing, install a compatible offline mission and launch it using that mission's documented procedure. “Community Offline Mode” is a separate community tool and is not installed by this tutorial; otherwise, test by starting a local DayZ server with the mod loaded and joining it.

---

## Step 9: Verify in the Script Log

After launching DayZ with your mod, the engine writes all `Print()` output to log files.

### Finding the Log Files

DayZ stores logs in your local AppData directory:

```
C:\Users\<YourWindowsUsername>\AppData\Local\DayZ\
```

To get there quickly:
1. Press **Win + R** to open the Run dialog
2. Type `%localappdata%\DayZ` and press Enter

Look for the most recent file named like:

```
script_<date>_<time>.log
```

For example: `script_2025-01-15_14-30-22.log`

### What to Search For

Open the log file in your text editor and search for `[MyFirstMod]`. You should see one of these messages:

```
[MyFirstMod] Hello World! The SERVER mission has started.
```

or (if you loaded as a client):

```
[MyFirstMod] Hello World! The CLIENT mission has started.
```

**If you see your message: congratulations.** Your first DayZ mod is working. You have successfully:

1. Created a mod directory structure
2. Written a config that the engine reads
3. Hooked into vanilla game code with `modded class`
4. Printed output to the script log

### What If You See Errors?

If the log contains lines starting with `SCRIPT (E):`, something went wrong. Read the next section.

---

## Step 10: Troubleshooting Common Issues

### Problem: No Log Output At All (Mod Does Not Seem to Load)

**Check your launch parameters.** `-mod=` must point at the `@MyFirstMod` folder -- the one holding `mod.cpp` and `addons\` -- not at your source tree. If file patching is not taking effect, check the junction separately: open the DayZ installation folder and confirm the `MyFirstMod` link is there and browsable.

**Check that config.cpp exists at the right level.** It must be at `Scripts/config.cpp` inside your mod root. If it is in the wrong folder, the engine silently ignores your mod.

**Check the CfgPatches class name.** If there is no `CfgPatches` block, or its syntax is wrong, the entire PBO is skipped.

**Look at the main DayZ log** (not just the script log). Check:
```
C:\Users\<YourName>\AppData\Local\DayZ\DayZ_<date>_<time>.RPT
```
Search for your mod name. You may see messages like "Addon MyFirstMod_Scripts requires addon DZ_Data which is not loaded."

### Problem: `SCRIPT (E): Undefined variable` or `Undefined type`

This means your code references something the engine does not recognize. Common causes:

- **Typo in a class name.** `MisionServer` instead of `MissionServer` (note the double 's').
- **Wrong script layer.** If you reference `PlayerBase` from `5_Mission`, it should work. But if you accidentally placed your file in `3_Game` and reference mission types, you will get this error.
- **Missing `super.OnInit()` call.** Omitting it can cause cascading failures.

### Problem: `SCRIPT (E): Member not found`

The method you are calling does not exist on the class. Double-check the method name and make sure you are overriding a real vanilla method. `OnInit` exists on `MissionServer` and `MissionGameplay` -- but not on every class.

### Problem: Mod Loads But Script Never Executes

- **File extension:** Make sure your script file ends in `.c` (not `.c.txt` or `.cs`). Windows may hide extensions by default.
- **Script path mismatch:** The `files[]` path in `config.cpp` must match your actual directory. `"MyFirstMod/Scripts/5_Mission"` means the engine looks for a folder at that exact path relative to the mod root.
- **Class name:** `modded class MissionServer` is case-sensitive. It must match the vanilla class name exactly.

### Problem: PBO Packing Errors

- Ensure `config.cpp` is at the root level of what you are packing (the `Scripts/` folder).
- Check that the prefix in Addon Builder matches your mod path.
- Make sure there are no non-text files mixed into the Scripts folder (no `.exe`, `.dll`, or binary files).

### Problem: Game Crashes on Startup

- Check for syntax errors in `config.cpp`. A missing semicolon, brace, or quote mark can crash the config parser.
- Verify that `requiredAddons` lists valid addon names. A misspelled addon name causes a hard failure.
- Remove your mod from the launch parameters and confirm the game starts without it. Then add it back to isolate the issue.

---

## Complete File Reference

Here are all three files in their complete form, for easy copy-paste:

### File 1: `MyFirstMod/mod.cpp`

```cpp
name = "My First Mod";
author = "YourName";
version = "1.0";
overview = "My very first DayZ mod. Prints Hello World to the script log.";
```

### File 2: `MyFirstMod/Scripts/config.cpp`

```cpp
class CfgPatches
{
    class MyFirstMod_Scripts
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
    class MyFirstMod
    {
        dir = "MyFirstMod";
        name = "My First Mod";
        author = "YourName";
        type = "mod";

        dependencies[] = { "Mission" };

        class defs
        {
            class missionScriptModule
            {
                value = "";
                files[] = { "MyFirstMod/Scripts/5_Mission" };
            };
        };
    };
};
```

### File 3: `MyFirstMod/Scripts/5_Mission/MyFirstMod/MissionHello.c`

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The SERVER mission has started.");
    }
};

modded class MissionGameplay
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The CLIENT mission has started.");
    }
};
```

---

## Next Steps

Now that you have a working mod, here are the natural progressions:

1. **[Chapter 8.2: Creating a Custom Item](02-custom-item.md)** -- Define a new in-game item with textures and spawning.
2. **Add more script layers** -- Create `3_Game` and `4_World` folders to organize configuration, data classes, and entity logic. See [Chapter 2.1: The 5-Layer Script Hierarchy](../02-mod-structure/01-five-layers.md).
3. **Add keybindings** -- Create an `Inputs.xml` file and register custom key actions.
4. **Create UI** -- Build in-game panels using layout files and `ScriptedWidgetEventHandler`. See [Chapter 3: GUI System](../03-gui-system/01-widget-types.md).
5. **Use a framework** -- Integrate with a public framework such as [Community Framework (CF)](https://github.com/Arkensor/DayZ-CommunityFramework), or build your own on the example framework developed in [Part 7: Patterns](../07-patterns/01-singletons.md), which covers RPC, config management, permissions, and events.

---

## Tips

- Use `-filePatching` for script iteration. It cuts the edit-test cycle from minutes to seconds -- but it runs on top of a packed mod plus the junction from Step 7, so pack first.
- Start with the `5_Mission` layer. Only add `3_Game` and `4_World` when you actually need them.
- Always call `super` first in overridden methods. Omitting it silently breaks vanilla behavior and every other mod hooking the same method.
- Use a unique prefix in `Print()` output (e.g., `[MyFirstMod]`). Logs contain thousands of lines -- a prefix is the only way to find yours.
- A missing semicolon or brace in `config.cpp` is a parse failure, and the symptom is usually that your classes simply are not there rather than a readable error. Check the `.RPT` file first when a mod loads but nothing it defines exists.

---

## Gotchas

- Treat `mod.cpp` as presentation only. Bohemia documents it as the file that "holds information for mod presentation", and the game's own mod reader pulls `name`, `picture`, `logo`, `logoSmall`, `logoOver`, `tooltip` and `overview` -- not `version`. Version your mod for people, not for the engine.
- A typo in `requiredAddons` is a dependency that cannot resolve, and the failure does not show up as a script error. Check the `.RPT` file rather than the script log when a mod seems to load but does nothing. (How the engine reacts in detail is not documented by Bohemia; the practical advice is to read the `.RPT`.)
- File patching is not a way to skip packing. The documented procedure packs the PBO first, loads it with `-mod=@MyFirstMod`, and then exposes the source tree through a junction so loose `.c` and `.layout` files can be read. Script edits apply on the next reconnect or mission restart. After a `config.cpp` edit, repack and relaunch -- no primary Bohemia source says a loose `config.cpp` is re-read under file patching, and it is parsed at engine startup in any case.
- Offline and listen-server sessions do not exercise the same code paths as a dedicated server -- identity and network-dependent APIs are the usual place this bites, so null-check anything you read from `GetIdentity()` instead of assuming it is populated. Always retest on a real dedicated server before release; [Chapter 8.6](06-debugging-testing.md#testing-server-mods) covers how.

**Next:** [Chapter 8.2: Creating a Custom Item](02-custom-item.md)
