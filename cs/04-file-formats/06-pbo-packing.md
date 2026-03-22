# Chapter 4.6: PBO Packing

[Domů](../../README.md) | [<< Předchozí: DayZ Tools Workflow](05-dayz-tools.md) | **Balení PBO** | [Další: Průvodce Workbench >>](07-workbench-guide.md)

---

## Úvod

A **PBO** (Packed Bank of Objects) is DayZ's archive format -- the equivalent of a `.zip` file for game content. Every mod the game loads is delivered as one or more PBO files. When hráč subscribes to a mod on Steam Workshop, they download PBOs. Když server loads mods, it reads PBOs. The PBO is the final deliverable of the celý modding pipeline.

Understanding how to create PBOs správně -- when to binarize, how to set prefixes, how to structure the output, and how to automate the process -- is the last step mezi your zdrojový soubors and a working mod. This chapter covers každýthing from the basic concept through advanced automated build workflows.

---

## Obsah

- [What is a PBO?](#what-is-a-pbo)
- [PBO Internal Structure](#pbo-interní-structure)
- [AddonBuilder: The Packing Tool](#addonbuilder-the-packing-tool)
- [The -packonly Flag](#the--packonly-flag)
- [The -prefix Flag](#the--prefix-flag)
- [Binarization: When Needed vs. Not](#binarization-when-needed-vs-not)
- [Key Signing](#key-signing)
- [@mod Folder Structure](#mod-folder-structure)
- [Automated Sestavte Scripts](#automated-build-scripts)
- [Multi-PBO Mod Builds](#multi-pbo-mod-builds)
- [Běžné Sestavte Errors and Solutions](#common-build-errors-and-solutions)
- [Testing: File Patching vs. PBO Loading](#testing-file-patching-vs-pbo-loading)
- [Best Practices](#best-practices)

---

## What is a PBO?

A PBO is a flat archive file that contains a directory tree of game assets. It has no compression (unlike ZIP) -- files inside are stored at their original size. The "packing" is purely organizational: mnoho files become one file with an interní path structure.

### Key Characteristics

- **No compression:** Files are stored verbatim. The PBO's size equals the sum of its contents plus a small header.
- **Flat header:** A list of file entries with paths, sizes, and offsets.
- **Prefix metadata:** Each PBO declares an interní path prefix that maps its contents into engine's virtual filesystem.
- **Read-only za běhu:** Engine reads from PBOs but nikdy writes to them.
- **Signed for multiplayer:** PBOs can be signed with a Bohemia-style key pair for server signature verification.

### Why PBOs Instead of Loose Files

- **Distribution:** One file per mod component is simpler than thousands of loose files.
- **Integrity:** Key signing ensures the mod has not been tampered with.
- **Výkon:** Engine's file I/O is optimized for reading from PBOs.
- **Organization:** The prefix system ensures no path collisions mezi mods.

---

## PBO Internal Structure

Když open a PBO (using a přílišl like PBO Manager or MikeroTools), you viz a directory tree:

```
MyMod.pbo
  $PBOPREFIX$                    <-- Text file containing the prefix path
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

The `$PBOPREFIX$` file is a tiny text file at the root of the PBO that declares the mod's path prefix. Například:

```
MyMod
```

This tells engine: "When některéthing references `MyMod\data\textures\my_item_co.paa`, look inside this PBO at `data\textures\my_item_co.paa`."

### config.bin vs. config.cpp

- **config.bin:** Binarized (binary) version of config.cpp, created by Binarize. Faster to parse at load time.
- **config.cpp:** The original text-format configuration. Works in engine but is slightly slower to parse.

Když build with binarization, config.cpp becomes config.bin. Když use `-packonly`, config.cpp is included as-is.

---

## AddonBuilder: The Packing Tool

**AddonBuilder** is Bohemia's official PBO packing přílišl, included with DayZ Tools. It can operate in GUI mode or command-line mode.

### GUI Mode

1. Spusťte AddonBuilder from DayZ Tools Launcher.
2. **Source directory:** Browse to your mod folder on P: (e.g., `P:\MyMod`).
3. **Output directory:** Browse to your output folder (e.g., `P:\output`).
4. **Options:**
   - **Binarize:** Zkontrolujte to run Binarize on content (converts P3D, textures, configs).
   - **Sign:** Zkontrolujte and select a key to sign the PBO.
   - **Prefix:** Enter the mod prefix (e.g., `MyMod`).
5. Klikněte **Pack**.

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
    -sign="P:\keys\MyKey"
```

### Command-Line Options

| Flag | Description |
|------|-------------|
| `-prefix=<path>` | Nastavte the PBO interní prefix (critical for path resolution) |
| `-packonly` | Skip binarization, pack files as-is |
| `-sign=<key_path>` | Sign the PBO with the specified BI key (private key path, no extension) |
| `-include=<path>` | Zahrňte file list -- pouze pack files matching this filter |
| `-exclude=<path>` | Exclude file list -- skip files matching this filter |
| `-binarize=<path>` | Path to Binarize.exe (if not in výchozí location) |
| `-temp=<path>` | Temporary directory for Binarize output |
| `-clear` | Clear output directory before packing |
| `-project=<path>` | Project drive path (usually `P:\`) |

---

## The -packonly Flag

The `-packonly` flag is one of the většina důležitý options in AddonBuilder. It tells the přílišl to skip all binarization and pack the zdrojový soubors exactly as they are.

### When to Use -packonly

| Mod Content | Use -packonly? | Reason |
|-------------|---------------|--------|
| Scripts pouze (.c files) | **Yes** | Scripts are nikdy binarized |
| UI layouts (.layout) | **Yes** | Layouts are nikdy binarized |
| Audio pouze (.ogg) | **Yes** | OGG is již game-ready |
| Pre-converted textures (.paa) | **Yes** | Already in final format |
| Config.cpp (no CfgVehicles) | **Yes** | Simple configs work unbinarized |
| Config.cpp (with CfgVehicles) | **No** | Item definitions require binarized config |
| P3D models (MLOD) | **No** | Should be binarized to ODOL for performance |
| TGA/PNG textures (need conversion) | **No** | Must be converted to PAA |

### Practical Guidance

For a **script-only mod** (like a framework or utility mod with no vlastní items):
```bash
AddonBuilder.exe "P:\MyScriptMod" "P:\output" -prefix="MyScriptMod" -packonly
```

For an **item mod** (weapons, clothing, vehicles with models and textures):
```bash
AddonBuilder.exe "P:\MyItemMod" "P:\output" -prefix="MyItemMod" -sign="P:\keys\MyKey"
```

> **Tip:** Many mods split into více PBOs precisely to optimize the build process. Script PBOs use `-packonly` (fast), while data PBOs with models and textures get plný binarization (slower but nutný).

---

## The -prefix Flag

The `-prefix` flag sets the PBO's interní path prefix, which is written to the `$PBOPREFIX$` file inside the PBO. This prefix is critical -- it determines how engine resolves paths to content inside the PBO.

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

For mods that use a subfolder structure, the prefix can include více levels:

```bash
# Source on P: drive
P:\MyMod\MyMod\Scripts\3_Game\MyClass.c

# If prefix is "MyMod\MyMod\Scripts"
# PBO internal: 3_Game\MyClass.c
# Engine path: MyMod\MyMod\Scripts\3_Game\MyClass.c
```

### Prefix Must Match References

Pokud váš config.cpp references `MyMod\data\texture_co.paa`, then the PBO containing that texture must have prefix `MyMod` and soubor must be at `data\texture_co.paa` inside the PBO. A mismatch causes engine to fail to find soubor.

### Běžné Prefix Patterns

| Mod Structure | Source Path | Prefix | Config Reference |
|---------------|-------------|--------|-----------------|
| Simple mod | `P:\MyMod\` | `MyMod` | `MyMod\data\item.p3d` |
| Namespaced mod | `P:\MyMod_Weapons\` | `MyMod_Weapons` | `MyMod_Weapons\data\rifle.p3d` |
| Script sub-package | `P:\MyFramework\MyMod\Scripts\` | `MyFramework\MyMod\Scripts` | (referenced via config.cpp `CfgMods`) |

---

## Binarization: When Needed vs. Not

Binarization is the conversion of human-readable zdrojový formáts into engine-optimized binary formats. It is the většina time-consuming step in the build process and the většina common source of build errors.

### What Gets Binarized

| File Type | Binarized To | Required? |
|-----------|-------------|-----------|
| `config.cpp` | `config.bin` | Required for mods defining items (CfgVehicles, CfgWeapons) |
| `.p3d` (MLOD) | `.p3d` (ODOL) | Recommended -- ODOL loads faster and is smaller |
| `.tga` / `.png` | `.paa` | Required -- engine needs PAA za běhu |
| `.edds` | `.paa` | Required -- stejný as výše |
| `.rvmat` | `.rvmat` (processed) | Paths resolved, minor optimization |
| `.wrp` | `.wrp` (optimized) | Required for terrain/map mods |

### What is NOT Binarized

| File Type | Reason |
|-----------|--------|
| `.c` scripts | Scripts are loaded as text by engine |
| `.ogg` audio | Already in game-ready format |
| `.layout` files | Already in game-ready format |
| `.paa` textures | Already in final format (pre-converted) |
| `.json` data | Přečtěte as text by script code |

### Config.cpp Binarization Details

Config.cpp binarization is the step většina modders encounter issues with. The binarizer parses the config.cpp text, platnýates its structure, resolves inheritance chains, and outputs a binary config.bin.

**When binarization je povinný for config.cpp:**
- The config defines `CfgVehicles` entries (items, weapons, vehicles, buildings).
- The config defines `CfgWeapons` entries.
- The config defines entries that reference models or textures.

**When binarization is NOT povinný:**
- The config pouze defines `CfgPatches` and `CfgMods` (mod registration).
- The config pouze defines sound configurations.
- Script-only mods with minimal config.

> **Rule of thumb:** Pokud váš config.cpp adds physical items to the herní svět, potřebujete binarization. If it pouze registers scripts and defines non-item data, `-packonly` works fine.

---

## Key Signing

PBOs can be signed with a cryptographic key pair. Servers use signature verification to ensure all connected clients have the stejný (unmodified) mod files.

### Key Pair Components

| File | Extension | Purpose | Who Has It |
|------|-----------|---------|------------|
| Private key | `.biprivatekey` | Signs PBOs during build | Mod author pouze (KEEP SECRET) |
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

### Signing Během Build

```bash
AddonBuilder.exe "P:\MyMod" "P:\output" ^
    -prefix="MyMod" ^
    -sign="P:\keys\MyModKey"
```

This produces:
```
P:\output\
  MyMod.pbo
  MyMod.pbo.MyModKey.bisign    <-- Signature file
```

### Server-Side Key Installation

Server admins place the public key (`.bikey`) in server's `keys/` directory:

```
DayZServer/
  keys/
    MyModKey.bikey             <-- Allows clients with this mod to connect
```

---

## @mod Folder Structure

DayZ expects mods to be organized in a specifický directory structure using the `@` prefix convention:

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

Large mods často split into více PBOs within a jeden `@mod` folder:

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

The `@` folder musí být in the game's root directory, or an absolute path musí být provided.

---

## Automated Sestavte Scripts

Manual PBO packing through AddonBuilder's GUI is acceptable for small, simple mods. For larger projects with více PBOs, automated build scripts are essential.

### Batch Script Pattern

A typical `build_pbos.bat`:

```batch
@echo off
setlocal

set TOOLS="P:\DayZ Tools\Bin\AddonBuilder\AddonBuilder.exe"
set OUTPUT="P:\@MyMod\addons"
set KEY="P:\keys\MyKey"

echo === Building Scripts PBO ===
%TOOLS% "P:\MyMod\Scripts" %OUTPUT% -prefix="MyMod\Scripts" -packonly -clear

echo === Building Data PBO ===
%TOOLS% "P:\MyMod\Data" %OUTPUT% -prefix="MyMod\Data" -sign=%KEY% -clear

echo === Build Complete ===
pause
```

### Python Sestavte Script Pattern (dev.py)

For more sophisticated builds, a Python script provides better error handling, logging, and conditional logic:

```python
import subprocess
import os
import sys

ADDON_BUILDER = r"P:\DayZ Tools\Bin\AddonBuilder\AddonBuilder.exe"
OUTPUT_DIR = r"P:\@MyMod\addons"
KEY_PATH = r"P:\keys\MyKey"

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

### Integration with dev.py

The MyMod project uses `dev.py` as the central build orchestrator:

```bash
python dev.py build          # Build all PBOs
python dev.py server         # Build + launch server + monitor logs
python dev.py full           # Build + server + client
```

This pattern je doporučeno for jakýkoli multi-mod workspace. A jeden command builds každýthing, launches server, and starts monitoring -- eliminating manual steps and reducing human error.

---

## Multi-PBO Mod Builds

Large mods benefit from splitting into více PBOs. This has several advantages:

### Why Split into Multiple PBOs

1. **Faster rebuilds.** Pokud change pouze a script, rebuild pouze the script PBO (with `-packonly`, which takes seconds). The data PBO (with binarization) takes minutes and ne need rebuilding.
2. **Modular loading.** Server-only PBOs can be excluded from client downloads.
3. **Cleaner organization.** Scripts, data, and GUI are clearly oddělenýd.
4. **Parallel builds.** Independent PBOs can be built současně.

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

### Dependency Mezi PBOs

When one PBO depends on další (e.g., scripts reference items defined in the config PBO), the `povinnýAddons[]` in `CfgPatches` ensures correct pořadí načítání:

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

---

## Běžné Sestavte Errors and Solutions

### Error: "Zahrňte file not found"

**Cause:** Config.cpp references a file (model, texture) that ne exist at the expected path.
**Solution:** Ověřte soubor exists on P: at the exact path referenced. Zkontrolujte spelling and capitalization.

### Error: "Binarize failed" with no details

**Cause:** Binarize crashed on a corrupted or neplatný zdrojový soubor.
**Solution:**
1. Zkontrolujte which file Binarize was processing (look at its log output).
2. Otevřete the problematic file in the appropriate přílišl (Object Builder for P3D, TexView2 for textures).
3. Validate soubor.
4. Běžné culprits: non-power-of-2 textures, corrupted P3D files, neplatný config.cpp syntax.

### Error: "Addon requires addon X"

**Cause:** CfgPatches `povinnýAddons[]` lists an addon that is not present.
**Solution:** Either install the povinný addon, add it to the build, or remove the requirement if it is not actually needed.

### Error: Config.cpp parse error (line X)

**Cause:** Syntax error in config.cpp.
**Solution:** Otevřete config.cpp in a text editor and check line X. Běžné issues:
- Missing semicolons after class definitions.
- Unclosed braces `{}`.
- Missing quotes around string values.
- Backslash at end of line (line continuation is not podporovaný).

### Error: PBO prefix mismatch

**Cause:** The prefix in the PBO ne match cestas used in config.cpp or materials.
**Solution:** Zajistěte `-prefix` matches cesta structure expected by all references. If config.cpp references `MyMod\data\item.p3d`, the PBO prefix must be `MyMod` and soubor must be at `data\item.p3d` inside the PBO.

### Error: "Signature check failed" on server

**Cause:** Client's PBO ne match server's expected signature.
**Solution:**
1. Zajistěte oba server and client have the stejný PBO version.
2. Re-sign the PBO with a fresh key if needed.
3. Aktualizujte the `.bikey` on server.

### Error: "Cannot open file" during Binarize

**Cause:** P: drive is not mounted or soubor path is incorrect.
**Solution:** Mount P: drive and verify the source path exists.

---

## Testing: File Patching vs. PBO Loading

Development involves two testing modes. Choosing the right one for každý situation saves significant time.

### File Patching (Development)

| Aspect | Detail |
|--------|--------|
| **Speed** | Instant -- edit file, restart game |
| **Setup** | Mount P: drive, launch with `-filePatching` flag |
| **Executable** | `DayZDiag_x64.exe` (Diag build povinný) |
| **Signing** | Not applicable (no PBOs to sign) |
| **Limitations** | No binarized configs, Diag build pouze |
| **Best for** | Script development, UI iteration, rapid prototyping |

### PBO Loading (Release Testing)

| Aspect | Detail |
|--------|--------|
| **Speed** | Slower -- must rebuild PBO for každý change |
| **Setup** | Sestavte PBO, place in `@mod/addons/` |
| **Executable** | `DayZDiag_x64.exe` or retail `DayZ_x64.exe` |
| **Signing** | Supported (povinný for multiplayer) |
| **Limitations** | Rebuild povinný for každý change |
| **Best for** | Final testing, multiplayer testing, release platnýation |

### Recommended Workflow

1. **Develop with file patching:** Zapište scripts, adjust layouts, iterate on textures. Restart the game to test. No build step.
2. **Sestavte PBOs periodically:** Testujte the binarized build to catch binarization-specific issues (config parse errors, texture conversion problems).
3. **Final test with PBO pouze:** Před release, test exclusively from PBOs to ensure the packed mod works identicky to soubor-patched version.
4. **Sign and distribute PBOs:** Generate signatures for multiplayer compatibility.

---

## Osvědčené postupy

1. **Use `-packonly` for script PBOs.** Scripts are nikdy binarized, so `-packonly` is vždy correct and much faster.

2. **Vždy set a prefix.** Bez a prefix, engine cannot resolve paths to your mod's content. Every PBO must have a correct `-prefix`.

3. **Automate your builds.** Vytvořte a build script (batch or Python) from day one. Manual packing ne scale and is error-prone.

4. **Udržujte source and output oddělený.** Source on P:, built PBOs in a oddělený output directory or `@mod/addons/`. Nikdy pack from the output directory.

5. **Sign your PBOs for jakýkoli multiplayer testing.** Unsigned PBOs are rejected by servers with signature verification enabled. Sign during development dokonce if it seems unnecessary -- it prevents "works for me" issues when jinýs test.

6. **Version your keys.** Když make breaking changes, generate a nový key pair. This forces all clients and servers to update together.

7. **Testujte oba file patching and PBO modes.** Some bugs pouze appear in one mode. Binarized configs behave odlišnýly from text configs in edge cases.

8. **Clean your output directory regularly.** Stale PBOs from previous builds can cause confusing behavior. Use the `-clear` flag or ručně clean before building.

9. **Split large mods into více PBOs.** The time saved on incremental rebuilds pays for itself within the first day of development.

10. **Přečtěte the build logs.** Binarize and AddonBuilder produce log files. When některéthing goes wrong, the answer is almost vždy in the logs. Zkontrolujte `%TEMP%\AddonBuilder\` and `%TEMP%\Binarize\` for detailed output.

---

## Pozorováno v reálných modech

| Vzor | Mod | Detail |
|---------|-----|--------|
| 20+ PBOs per mod with fine-grained splits | Expansion (all modules) | Splits into oddělený PBOs for Scripts, Data, GUI, Vehicles, Book, Market, etc., enabling nezávislý rebuilds and volitelný client/server separation |
| Scripts/Data/GUI triple-split | StarDZ (Core, Missions, AI) | Každý mod produces 2-3 PBOs: `_Scripts.pbo` (packonly), `_Data.pbo` (binarized models/textures), `_GUI.pbo` (packonly layouts) |
| Single monolithic PBO | Simple retexture mods | Small mods with pouze a config.cpp and a few PAA textures pack každýthing into one PBO with binarization |
| Key versioning per major release | Expansion | Generates nový key pairs for breaking updates, forcing all clients and servers to update in sync |

---

## Kompatibilita a dopad

- **Více modů:** PBO prefix collisions cause engine to load one mod's files místo další's. Every mod must use a unique prefix. Zkontrolujte `$PBOPREFIX$` carefully when debugging "file not found" errors in multi-mod environments.
- **Výkon:** PBO loading is fast (sequential file reads), but mods with mnoho large PBOs increase server startup time. Binarized content loads faster than unbinarized. Use ODOL models and PAA textures for release builds.
- **Verze:** The PBO format itself has not changed. AddonBuilder receives periodic fixes via DayZ Tools updates, but the command-line flags and packing behavior have been stable since DayZ 1.0.

---

## Navigace

| Previous | Up | Next |
|----------|----|------|
| [4.5 DayZ Tools Workflow](05-dayz-tools.md) | [Part 4: File Formats & DayZ Tools](01-textures.md) | [Další: Workbench Guide](07-workbench-guide.md) |
