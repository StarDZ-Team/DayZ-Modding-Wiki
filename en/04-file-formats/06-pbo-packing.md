# PBO Packing


---

## Introduction

A **PBO** (Packed Bank of Objects) is DayZ's archive format -- the equivalent of a `.zip` file for game content. Every mod the game loads is delivered as one or more PBO files. When a player subscribes to a mod on Steam Workshop, they download PBOs. When a server loads mods, it reads PBOs. The PBO is the final deliverable of the entire modding pipeline.

Understanding how to create PBOs correctly -- when to binarize, how to set prefixes, how to structure the output, and how to automate the process -- is the last step between your source files and a working mod. This chapter covers everything from the basic concept through advanced automated build workflows.

---

## Table of Contents

- [What is a PBO?](#what-is-a-pbo)
- [PBO Internal Structure](#pbo-internal-structure)
- [AddonBuilder: The Packing Tool](#addonbuilder-the-packing-tool)
- [The -packonly Flag](#the-packonly-flag)
- [The -prefix Flag](#the-prefix-flag)
- [Binarization: When Needed vs. Not](#binarization-when-needed-vs-not)
- [Key Signing](#key-signing)
- [@mod Folder Structure](#mod-folder-structure)
- [Automated Build Scripts](#automated-build-scripts)
- [Multi-PBO Mod Builds](#multi-pbo-mod-builds)
- [Common Build Errors and Solutions](#common-build-errors-and-solutions)
- [Testing: File Patching vs. PBO Loading](#testing-file-patching-vs-pbo-loading)
- [Best Practices](#best-practices)

---

## What is a PBO?

A PBO is a flat archive file that contains a directory tree of game assets. Packing combines files under virtual paths. Do not equate the archive format with a general-purpose ZIP compressor; the installed FileBank reports its old -compress option as unsupported.

### Key Characteristics

- **Build output size:** Texture and model conversion affect size before packing; measure the resulting archive rather than assuming a ZIP-like compression ratio.
- **Flat header:** A list of file entries with paths, sizes, and offsets.
- **Prefix metadata:** Each PBO declares an internal path prefix that maps its contents into the engine's virtual filesystem.
- **Read-only at runtime:** The engine reads from PBOs but never writes to them.
- **Signed for multiplayer:** PBOs can be signed with a Bohemia-style key pair for server signature verification.

### Why PBOs Instead of Loose Files

- **Distribution:** One file per mod component is simpler than thousands of loose files.
- **Integrity:** Key signing ensures the mod has not been tampered with.
- **Performance:** The engine's file I/O is optimized for reading from PBOs.
- **Organization:** The prefix system ensures no path collisions between mods.

---

## PBO Internal Structure

When you open a PBO (using a tool like PBO Manager or MikeroTools), you see a directory tree:

```
MyMod.pbo
  [header property: prefix=MyMod] <-- Metadata, not an ordinary file entry
  config.bin                      <-- Binarized config.cpp (or config.cpp if -packonly)
  Scripts/
    3_Game/
      MyConstants.c
    4_World/
      MyManager.c
    5_Mission/
      MyUI.c
  data/
    models/
      my_item.p3d                 <-- Binarized ODOL (or MLOD if -packonly)
    textures/
      my_item_co.paa
      my_item_nohq.paa
      my_item_smdi.paa
    materials/
      my_item.rvmat
  sound/
    gunshot_01.ogg
  GUI/
    layouts/
      my_panel.layout
```

### $PBOPREFIX$

A `$PBOPREFIX$` text file can be a source-side convention used by packing tools. The runtime path prefix is stored as the `prefix` property in the PBO header, not as a required runtime text-file entry. For example:

```
MyMod
```

This tells the engine: "When something references `MyMod\data\textures\my_item_co.paa`, look inside this PBO at `data\textures\my_item_co.paa`."

### config.bin vs. config.cpp

- **config.bin:** Binarized (binary) version of config.cpp, created by Binarize. Faster to parse at load time.
- **config.cpp:** The original text-format configuration. Works in the engine but is slightly slower to parse.

When you build with binarization, config.cpp becomes config.bin. When you use `-packonly`, config.cpp is included as-is.

---

## AddonBuilder: The Packing Tool

**AddonBuilder** is Bohemia's official PBO packing tool, included with DayZ Tools. It can operate in GUI mode or command-line mode.

### GUI Mode

1. Launch AddonBuilder from DayZ Tools Launcher.
2. **Source directory:** Browse to your mod folder on P: (e.g., `P:\MyMod`).
3. **Output directory:** Browse to your output folder (e.g., `P:\output`).
4. **Options:**
   - **Binarize:** Check to run Binarize on content (converts P3D, textures, configs).
   - **Sign:** Check and select a key to sign the PBO.
   - **Prefix:** Enter the mod prefix (e.g., `MyMod`).
5. Click **Pack**.

### Command-Line Mode

Command-line mode is preferred for automated builds:

```bash
AddonBuilder.exe [source_path] [output_path] [options]
```

**Full example:**
```bash
"P:\DayZ Tools\Bin\AddonBuilder\AddonBuilder.exe" ^
    "P:\MyMod" ^
    "P:\output" ^
    -prefix="MyMod" ^
    -sign="P:\keys\MyKey.biprivatekey"
```

### Command-Line Options

| Flag | Description |
|------|-------------|
| `-prefix=<path>` | Set the PBO internal prefix (critical for path resolution) |
| `-packonly` | Skip binarization, pack files as-is |
| `-sign=<key_path>` | Sign the PBO with the specified BI key (full `.biprivatekey` file path) |
| `-include=<path>` | File containing patterns for files copied directly without binarization; not an overall packing whitelist |
| `-exclude=<path>` | Exclude file list -- skip files matching this filter |
| `-binarize=<path>` | Path to Binarize.exe (if not in default location) |
| `-temp=<path>` | Temporary directory for Binarize output |
| `-clear` | Delete the current project subfolder in the temporary binarization directory before binarizing |
| `-project=<path>` | Project drive path (usually `P:\`) |
| `-binarizeAllTextures` | Convert TGA/PNG textures even when unreferenced or absent from textures.lst |
| `-binarizeFullLogs` | Enable extended Binarize logging |
| `-binarizeNoLogs` | Disable extended Binarize logging |
| `-dssignfile=<path>` | Override the DSSignFile executable path |
| `-help` | Display installed command-line help |

---

## The -packonly Flag

The `-packonly` flag is one of the most important options in AddonBuilder. It tells the tool to skip all binarization and pack the source files exactly as they are.

### When to Use -packonly

| Mod Content | Use -packonly? | Reason |
|-------------|---------------|--------|
| Scripts only (.c files) | **Yes** | Scripts are never binarized |
| UI layouts (.layout) | **Yes** | Layouts are never binarized |
| Audio only (.ogg) | **Yes** | OGG is already game-ready |
| Pre-converted textures (.paa) | **Yes** | Already in final format |
| Config.cpp (no CfgVehicles) | **Yes** | Simple configs work unbinarized |
| Config.cpp (with CfgVehicles) | **No** | Item definitions require binarized config |
| P3D models (MLOD) | **No** | Should be binarized to ODOL for performance |
| TGA/PNG textures (need conversion) | **No** | Must be converted to PAA |

### Practical Guidance

For a **script-only mod** (like a framework or utility mod with no custom items):
```bash
AddonBuilder.exe "P:\MyScriptMod" "P:\output" -prefix="MyScriptMod" -packonly
```

For an **item mod** (weapons, clothing, vehicles with models and textures):
```bash
AddonBuilder.exe "P:\MyItemMod" "P:\output" -prefix="MyItemMod" -sign="P:\keys\MyKey.biprivatekey"
```

> **Tip:** Many mods split into multiple PBOs precisely to optimize the build process. Script PBOs use `-packonly` (fast), while data PBOs with models and textures get full binarization (slower but necessary).

---

## The -prefix Flag

The `-prefix` flag sets the PBO's internal path prefix, which FileBank stores as a `prefix` header property. This prefix is critical -- it determines how the engine resolves paths to content inside the PBO.

### How Prefix Works

```
Source: P:\MyMod\data\textures\item_co.paa
Prefix: MyMod
PBO internal path: data\textures\item_co.paa

Engine resolution: MyMod\data\textures\item_co.paa
  --> Looks in MyMod.pbo for: data\textures\item_co.paa
  --> Found!
```

### Multi-Level Prefixes

For mods that use a subfolder structure, the prefix can include multiple levels:

```bash
# Source on P: drive
P:\MyMod\MyMod\Scripts\3_Game\MyClass.c

# If prefix is "MyMod\MyMod\Scripts"
# PBO internal: 3_Game\MyClass.c
# Engine path: MyMod\MyMod\Scripts\3_Game\MyClass.c
```

### Prefix Must Match References

If your config.cpp references `MyMod\data\texture_co.paa`, then the PBO containing that texture must have prefix `MyMod` and the file must be at `data\texture_co.paa` inside the PBO. A mismatch causes the engine to fail to find the file.

### Common Prefix Patterns

| Mod Structure | Source Path | Prefix | Config Reference |
|---------------|-------------|--------|-----------------|
| Simple mod | `P:\MyMod\` | `MyMod` | `MyMod\data\item.p3d` |
| Namespaced mod | `P:\MyMod_Weapons\` | `MyMod_Weapons` | `MyMod_Weapons\data\rifle.p3d` |
| Script sub-package | `P:\MyFramework\MyMod\Scripts\` | `MyFramework\MyMod\Scripts` | (referenced via config.cpp `CfgMods`) |

---

## Binarization: When Needed vs. Not

Binarization is the conversion of human-readable source formats into engine-optimized binary formats. It is the most time-consuming step in the build process and the most common source of build errors.

### What Gets Binarized

| File Type | Binarized To | Required? |
|-----------|-------------|-----------|
| `config.cpp` | `config.bin` | Optional binary config; choose the asset build workflow independently |
| `.p3d` (MLOD) | `.p3d` (ODOL) | Recommended -- ODOL loads faster and is smaller |
| `.tga` / `.png` | `.paa` | Required -- engine needs PAA at runtime |
| `.edds` | `.edds` | GUI texture resource; keep the format referenced by the imageset |
| `.rvmat` | `.rvmat` (processed) | Paths resolved, minor optimization |
| `.wrp` | `.wrp` (optimized) | Required for terrain/map mods |

### What is NOT Binarized

| File Type | Reason |
|-----------|--------|
| `.c` scripts | Scripts are loaded as text by the engine |
| `.ogg` audio | Already in game-ready format |
| `.layout` files | Already in game-ready format |
| `.paa` textures | Already in final format (pre-converted) |
| `.json` data | Read as text by script code |

### Config.cpp Binarization Details

Config.cpp binarization is the step most modders encounter issues with. The binarizer parses the config.cpp text, validates its structure, resolves inheritance chains, and outputs a binary config.bin.

Text config.cpp files can define game config classes, including CfgVehicles. Choose binarization for the assets and release workflow, not merely because a class name is present. For example, model.cfg animation data must be baked into the model; `-packonly` does not perform that work. Script-only addons with ready-to-use resources can use `-packonly`.

---

## Key Signing

PBOs can be signed with a cryptographic key pair. Servers use signature verification to ensure all connected clients have the same (unmodified) mod files.

### Key Pair Components

| File | Extension | Purpose | Who Has It |
|------|-----------|---------|------------|
| Private key | `.biprivatekey` | Signs PBOs during build | Mod author only (KEEP SECRET) |
| Public key | `.bikey` | Verifies signatures | Server admins, distributed with mod |

### Generating Keys

Use DayZ Tools' **DSSignFile** or **DSCreateKey** utilities:

```bash
# Generate a key pair
DSCreateKey.exe MyModKey

# This creates:
#   MyModKey.biprivatekey   (keep secret, do not distribute)
#   MyModKey.bikey          (distribute to server admins)
```

### Signing During Build

```bash
AddonBuilder.exe "P:\MyMod" "P:\output" ^
    -prefix="MyMod" ^
    -sign="P:\keys\MyModKey.biprivatekey"
```

This produces:
```
P:\output\
  MyMod.pbo
  MyMod.pbo.MyModKey.bisign    <-- Signature file
```

### Server-Side Key Installation

Server admins place the public key (`.bikey`) in the server's `keys/` directory:

```
DayZServer/
  keys/
    MyModKey.bikey             <-- Allows clients with this mod to connect
```

---

## @mod Folder Structure

DayZ expects mods to be organized in a specific directory structure using the `@` prefix convention:

```
@MyMod/
  addons/
    MyMod.pbo                  <-- Packed mod content
    MyMod.pbo.MyKey.bisign     <-- PBO signature (optional)
  keys/
    MyKey.bikey                <-- Public key for servers (optional)
  mod.cpp                      <-- Mod metadata
```

### mod.cpp

The `mod.cpp` file provides metadata displayed in the DayZ launcher:

```cpp
name = "My Awesome Mod";
author = "ModAuthor";
version = "1.0.0";
url = "https://steamcommunity.com/sharedfiles/filedetails/?id=XXXXXXXXX";
```

### Multi-PBO Mods

Large mods often split into multiple PBOs within a single `@mod` folder:

```
@MyFramework/
  addons/
    MyMod_Core_Scripts.pbo        <-- Script layer
    MyMod_Core_Data.pbo           <-- Textures, models, materials
    MyMod_Core_GUI.pbo            <-- Layout files, imagesets
  keys/
    MyMod.bikey
  mod.cpp
```

### Loading Mods

Mods are loaded via the `-mod` parameter:

```bash
# Single mod
DayZDiag_x64.exe -mod="@MyMod"

# Multiple mods (semicolon-separated)
DayZDiag_x64.exe -mod="@MyFramework;@MyMod_Weapons;@MyMod_Missions"
```

The `@` folder must be in the game's root directory, or an absolute path must be provided.

---

## Automated Build Scripts

Manual PBO packing through AddonBuilder's GUI is acceptable for small, simple mods. For larger projects with multiple PBOs, automated build scripts are essential.

### Batch Script Pattern

A typical `build_pbos.bat`:

```batch
@echo off
setlocal

set TOOLS="P:\DayZ Tools\Bin\AddonBuilder\AddonBuilder.exe"
set OUTPUT="P:\@MyMod\addons"
set KEY="P:\keys\MyKey.biprivatekey"

echo === Building Scripts PBO ===
%TOOLS% "P:\MyMod\Scripts" %OUTPUT% -prefix="MyMod\Scripts" -packonly -clear

echo === Building Data PBO ===
%TOOLS% "P:\MyMod\Data" %OUTPUT% -prefix="MyMod\Data" -sign=%KEY% -clear

echo === Build Complete ===
pause
```

### Python Build Script Pattern

For more sophisticated builds, a Python script provides better error handling, logging, and conditional logic:

```python
import subprocess
import os
import sys

ADDON_BUILDER = r"P:\DayZ Tools\Bin\AddonBuilder\AddonBuilder.exe"
OUTPUT_DIR = r"P:\@MyMod\addons"
KEY_PATH = r"P:\keys\MyKey.biprivatekey"

PBOS = [
    {
        "name": "Scripts",
        "source": r"P:\MyMod\Scripts",
        "prefix": r"MyMod\Scripts",
        "packonly": True,
    },
    {
        "name": "Data",
        "source": r"P:\MyMod\Data",
        "prefix": r"MyMod\Data",
        "packonly": False,
    },
]

def build_pbo(pbo_config):
    """Build a single PBO."""
    cmd = [
        ADDON_BUILDER,
        pbo_config["source"],
        OUTPUT_DIR,
        f"-prefix={pbo_config['prefix']}",
    ]

    if pbo_config.get("packonly"):
        cmd.append("-packonly")
    else:
        cmd.append(f"-sign={KEY_PATH}")

    print(f"Building {pbo_config['name']}...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR building {pbo_config['name']}:")
        print(result.stderr)
        return False

    print(f"  {pbo_config['name']} built successfully.")
    return True

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    success = True
    for pbo in PBOS:
        if not build_pbo(pbo):
            success = False

    if success:
        print("\nAll PBOs built successfully.")
    else:
        print("\nBuild completed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Integration with a Build Orchestrator

For a multi-mod workspace, the build script above is usually just one stage of a larger orchestrator: a single command that builds every PBO, links the output into the game directory, launches the server, and tails the script log for errors. That closes the whole edit-build-test loop with one keystroke.

A minimal `build.py` orchestrator sketch:

```python
import subprocess
import sys

def build_all():
    """Build every PBO (see build_pbo above)."""
    # ... loop over PBOS, return False on any failure
    return True

def link_output():
    """Junction @MyMod from the output dir into the DayZ install."""
    subprocess.run([
        "cmd", "/c", "mklink", "/J",
        r"C:\DayZ\@MyMod", r"P:\@MyMod",
    ])

def launch_server():
    """Start the diag server with the mod loaded."""
    subprocess.Popen([
        r"C:\DayZ\DayZDiag_x64.exe", "-server",
        "-mod=@MyMod", "-config=serverDZ.cfg", "-doLogs",
    ])

def tail_log():
    """Follow the newest script log and print SCRIPT (E) lines."""
    # ... open the latest script_*.log, poll for new lines,
    # highlight errors so failures are visible immediately

if __name__ == "__main__":
    if not build_all():
        sys.exit(1)
    link_output()
    if "server" in sys.argv:
        launch_server()
        tail_log()
```

Typical subcommands to expose: `build` (PBOs only), `server` (build + launch + monitor), and `check` (scan the latest log offline). A single command that does all of it eliminates manual steps and reduces human error.

---

## Multi-PBO Mod Builds

Large mods benefit from splitting into multiple PBOs. This has several advantages:

### Why Split into Multiple PBOs

1. **Faster rebuilds.** If you change only a script, rebuild only the script PBO (with `-packonly`, which takes seconds). The data PBO (with binarization) takes minutes and does not need rebuilding.
2. **Modular loading.** Server-only PBOs can be excluded from client downloads.
3. **Cleaner organization.** Scripts, data, and GUI are clearly separated.
4. **Parallel builds.** Independent PBOs can be built simultaneously.

### Typical Split Pattern

```
@MyMod/
  addons/
    MyMod_Core.pbo           <-- config.cpp, CfgPatches (binarized)
    MyMod_Scripts.pbo         <-- All .c script files (-packonly)
    MyMod_Data.pbo            <-- Models, textures, materials (binarized)
    MyMod_GUI.pbo             <-- Layouts, imagesets (-packonly)
    MyMod_Sounds.pbo          <-- OGG audio files (-packonly)
```

### Dependency Between PBOs

When one PBO depends on another (e.g., scripts reference items defined in the config PBO), the `requiredAddons[]` in `CfgPatches` ensures correct load order:

```cpp
// In MyMod_Scripts config.cpp
class CfgPatches
{
    class MyMod_Scripts
    {
        requiredAddons[] = {"MyMod_Core"};   // Load after the core PBO
    };
};
```

### Keep Every Single PBO Reasonably Small

Splitting a texture-heavy or model-heavy addon can make incremental builds and diagnosis easier. Do not diagnose an `ACCESS_VIOLATION` solely from archive size: inspect the logs and isolate the failing addon and asset. A particular byte threshold is not a substitute for testing the packaged mod.

To preserve resource paths while splitting, move distinct files into sibling source folders and pack both with the same `-prefix` header value. Ensure the two archives do not contain overlapping virtual file paths:

```
MyMod/Data/Weapons/Rifles/      -> packs to MyMod_Weapons_Rifles.pbo   (prefix: MyMod\Data\Weapons\Rifles)
MyMod/Data/Weapons/Rifles2/     -> packs to MyMod_Weapons_Rifles2.pbo  (prefix: MyMod\Data\Weapons\Rifles  <- same!)
```

Because the *physical* folder name (`Rifles2`) never has to appear in the *virtual* prefix, every existing `model=`/texture reference under `Rifles/...` keeps resolving correctly with zero script or config changes -- you are only moving files between two PBOs that both present themselves under the same virtual path.

---

## Common Build Errors and Solutions

### Error: "Include file not found"

**Cause:** Config.cpp references a file (model, texture) that does not exist at the expected path.
**Solution:** Verify the file exists on P: at the exact path referenced. Check spelling and capitalization.

### Error: "Binarize failed" with no details

**Cause:** Binarize crashed on a corrupted or invalid source file.
**Solution:**
1. Check which file Binarize was processing (look at its log output).
2. Open the problematic file in the appropriate tool (Object Builder for P3D, TexView2 for textures).
3. Validate the file.
4. Common culprits: non-power-of-2 textures, corrupted P3D files, invalid config.cpp syntax.

### Error: "Addon requires addon X"

**Cause:** CfgPatches `requiredAddons[]` lists an addon that is not present.
**Solution:** Either install the required addon, add it to the build, or remove the requirement if it is not actually needed.

### Error: Config.cpp parse error (line X)

**Cause:** Syntax error in config.cpp.
**Solution:** Open config.cpp in a text editor and check line X. Common issues:
- Missing semicolons after class definitions.
- Unclosed braces `{}`.
- Missing quotes around string values.
- Backslash at end of line (line continuation is not supported).

### Error: PBO prefix mismatch

**Cause:** The prefix in the PBO does not match the paths used in config.cpp or materials.
**Solution:** Ensure `-prefix` matches the path structure expected by all references. If config.cpp references `MyMod\data\item.p3d`, the PBO prefix must be `MyMod` and the file must be at `data\item.p3d` inside the PBO.

### Error: "Signature check failed" on server

**Cause:** Client's PBO does not match the server's expected signature.
**Solution:**
1. Ensure both server and client have the same PBO version.
2. Re-sign the PBO with a fresh key if needed.
3. Update the `.bikey` on the server.

### Error: "Cannot open file" during Binarize

**Cause:** P: drive is not mounted or the file path is incorrect.
**Solution:** Mount P: drive and verify the source path exists.

---

## Testing: File Patching vs. PBO Loading

Development involves two testing modes. Choosing the right one for each situation saves significant time.

### File Patching (Development)

| Aspect | Detail |
|--------|--------|
| **Speed** | Instant -- edit file, restart game |
| **Setup** | Mount P: drive, launch with `-filePatching` flag |
| **Executable** | `DayZDiag_x64.exe` (Diag build required) |
| **Signing** | Not applicable (no PBOs to sign) |
| **Limitations** | No binarized configs, Diag build only |
| **Best for** | Script development, UI iteration, rapid prototyping |

### PBO Loading (Release Testing)

| Aspect | Detail |
|--------|--------|
| **Speed** | Slower -- must rebuild PBO for each change |
| **Setup** | Build PBO, place in `@mod/addons/` |
| **Executable** | `DayZDiag_x64.exe` or retail `DayZ_x64.exe` |
| **Signing** | Supported; required when joining servers that enforce PBO signature verification |
| **Limitations** | Rebuild required for every change |
| **Best for** | Final testing, multiplayer testing, release validation |

### Recommended Workflow

1. **Develop with file patching:** Write scripts, adjust layouts, iterate on textures. Restart the game to test. No build step.
2. **Build PBOs periodically:** Test the binarized build to catch binarization-specific issues (config parse errors, texture conversion problems).
3. **Final test with PBO only:** Before release, test exclusively from PBOs to ensure the packed mod works identically to the file-patched version.
4. **Sign and distribute PBOs:** Generate signatures for multiplayer compatibility.

---

## Best Practices

1. **Use `-packonly` for script PBOs.** Scripts are never binarized, so `-packonly` is always correct and much faster.

2. **Verify the PBO prefix.** Set `-prefix` explicitly when you need a specific virtual path; otherwise Addon Builder may calculate it automatically. In either case, confirm the stored prefix matches all resource references.

3. **Automate your builds.** Create a build script (batch or Python) from day one. Manual packing does not scale and is error-prone.

4. **Keep source and output separate.** Source on P:, built PBOs in a separate output directory or `@mod/addons/`. Never pack from the output directory.

5. **Sign your PBOs for any multiplayer testing.** Unsigned PBOs are rejected by servers with signature verification enabled. Sign during development even if it seems unnecessary -- it prevents "works for me" issues when others test.

6. **Version your keys.** When you make breaking changes, generate a new key pair. This forces all clients and servers to update together.

7. **Test both file patching and PBO modes.** Some bugs only appear in one mode. Binarized configs behave differently from text configs in edge cases.

8. **Clean your output directory regularly.** Stale PBOs from previous builds can cause confusing behavior. Remove stale output PBOs deliberately. `-clear` cleans temporary binarization data for the current project; it does not clean the output directory.

9. **Split large mods into multiple PBOs.** The time saved on incremental rebuilds pays for itself within the first day of development.

10. **Read the build logs.** Binarize and AddonBuilder produce log files. When something goes wrong, the answer is almost always in the logs. The installed AddonBuilder `logger.xml` writes `AddonBuilder.rpt`, `AddonBuilderProcess.rpt` and `AddonBuilder.User.rpt` under `DayZ Tools\Bin\Logs\`. The Windows temporary directory (or `-temp`) holds binarized intermediate files, not these configured log files.

---

## Observed in Real Mods

| Pattern | Where Seen | Detail |
|---------|------------|--------|
| Many PBOs per mod with fine-grained splits | Large content frameworks | 20+ separate PBOs for scripts, data, GUI, vehicles, and per-feature modules, enabling independent rebuilds and optional client/server separation |
| Scripts/Data/GUI triple-split | Framework mods | Each mod produces 2-3 PBOs: `_Scripts.pbo` (packonly), `_Data.pbo` (binarized models/textures), `_GUI.pbo` (packonly layouts) |
| Single monolithic PBO | Simple retexture mods | Small mods with only a config.cpp and a few PAA textures pack everything into one PBO with binarization |
| Key versioning per major release | Actively updated mods | A new key pair for breaking updates forces all clients and servers to update in sync |

---

## Compatibility & Impact

- **Multi-Mod:** PBO prefix collisions cause the engine to load one mod's files instead of another's. Choose distinct virtual paths for unrelated assets; split PBOs can share a prefix if their file paths do not overlap. Check the PBO header prefix carefully when debugging "file not found" errors in multi-mod environments.
- **Performance:** PBO loading is fast (sequential file reads), but mods with many large PBOs increase server startup time. Binarized content loads faster than unbinarized. Use ODOL models and PAA textures for release builds.
- **Tool options:** Check the help embedded in your installed AddonBuilder when scripting a build; use full paths for tools and signing keys.
