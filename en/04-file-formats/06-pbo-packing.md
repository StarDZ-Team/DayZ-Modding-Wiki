# PBO Packing


---

## Introduction

A **PBO** (Packed Bank of Objects) is DayZ's archive format for packed mod content. A launch package can contain one or more PBOs. PBOs are a release artifact, but a successful pack alone does not prove that the game can load the addon, compile its scripts, enforce its signature, or distribute it through Workshop.

Understanding how to create PBOs correctly -- when to binarize, how to set prefixes, how to structure the output, and how to automate the process -- is the last step between your source files and a working mod. This chapter covers everything from the basic concept through advanced automated build workflows.

---

## Table of Contents

- [What is a PBO?](#what-is-a-pbo)
- [PBO Internal Structure](#pbo-internal-structure)
- [PBO Size Limits: What Is and Is Not Established](#pbo-size-limits-what-is-and-is-not-established)
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
- [Evidence and Validation Scope](#evidence-and-validation-scope)

---

## What is a PBO?

A PBO is a flat archive file that contains a directory tree of game assets. Packing combines files under virtual paths. Do not equate the archive format with a general-purpose ZIP compressor; the installed FileBank reports its old -compress option as unsupported.

The reverse-engineered format recognizes a `Cprs` member marker and records original and stored sizes, so member compression exists in the format family. However, the reopened DayZ Experimental Tools Addon Builder `1.0.240639` help exposes no compression switch. Do not document obsolete `-compress` commands or promise ZIP-style whole-archive compression; asset conversion and binarization are separate from PBO member packing.

### Key Characteristics

- **Build output size:** Texture and model conversion affect size before packing; measure the resulting archive rather than assuming a ZIP-like compression ratio.
- **Header entries and contiguous payloads:** The reverse-engineered format describes member paths, packing method, uncompressed size, a reserved field, timestamp, and stored size. The historical `Offset` field is normally zero; readers walk the contiguous data block rather than using it as a member seek offset.
- **Prefix metadata:** Each PBO declares an internal path prefix that maps its contents into the engine's virtual filesystem.
- **Read-only at runtime:** The engine reads from PBOs but never writes to them.
- **Signed for multiplayer:** A server configured to verify signatures can check client PBOs against `.bisign` and installed `.bikey` files. Exact enforcement still requires a server join test.

### Why PBOs Instead of Loose Files

- **Distribution:** One file per mod component is simpler than thousands of loose files.
- **Integrity:** Signing supports server-side verification when that server is configured to enforce it; it is not a substitute for testing the actual client/server deployment.
- **Performance:** The engine's file I/O is optimized for reading from PBOs.
- **Organization:** Prefix metadata gives mounted files a virtual namespace that you can inspect and diagnose. It does not prevent two archives from publishing the same normalized virtual path, so check the complete release for collisions.

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

## PBO Size Limits: What Is and Is Not Established

Keep these boundaries separate. A 32-bit field in a member header is not, by itself, a total-archive, DayZ-runtime, or Workshop limit.

| Boundary | What is established | What remains unproven |
|----------|---------------------|-----------------------|
| Member fields | The reverse-engineered format describes unsigned 32-bit `OriginalSize` and `DataSize` fields for one member. A value above `4,294,967,295` cannot fit in either field. | A usable maximum member size in a particular packer or DayZ build. |
| Total archive format | The reviewed layout has no single 32-bit total-PBO-size field, and the historical `Offset` field is unused/reserved. | A universal 2 GiB or 4 GiB total-PBO ceiling. |
| Packer and signer | Addon Builder and the DS tools have independent implementation limits. | Their boundary behavior without a retained test for the exact tool build. |
| DayZ runtime | A loader can fail for causes unrelated to a header field. | An authoritative, versioned total-PBO ceiling. |
| Filesystem and deployment | Copying, hosting, and server-management tooling introduce separate constraints. | That any one of those limits is a PBO-format limit. |
| Workshop distribution | Workshop transfer and item storage are service concerns. | A fixed DayZ item-content ceiling from the reviewed Steamworks page. |

Retail DayZ `1.29.0.163709` was observed with 117 PBOs totaling `21,638,391,975` bytes; the largest inspected archive was `1,216,702,399` bytes. Those are shipping observations, not lower or upper limits.

Split an addon when it improves build, replacement, upload, or diagnosis workflow. For a boundary experiment, vary one condition at a time and retain the exact PBO hash and size, tool and game versions, command line, logs, crash artifacts, and client/server result. Do not turn one crash into a universal limit.

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
| Text config.cpp, with or without CfgVehicles | **Maybe** | Text configs can define game classes; choose binarization for the assets and release workflow, not merely because `CfgVehicles` is present |
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

PBOs can be signed with a cryptographic key pair. For a distributed client/shared package, sign every final PBO after its last byte-changing operation, keep the private key out of the release, and distribute the public key to server operators. A server's actual enforcement must still be tested with that server configuration.

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

### Sign Final Bytes, Then Check the Release

```bash
AddonBuilder.exe "P:\MyMod" "P:\output" ^
    -prefix="MyMod" ^
    -packonly
```

This produces:
```
P:\output\
  MyMod.pbo
```

First inspect and rename the PBO to its final release name. Then sign that exact file with `DSSignFile.exe`:

```batch
DSSignFile.exe P:\keys\MyModKey.biprivatekey P:\release\@MyMod\Addons\MyMod.pbo
```

Require the expected `.bisign` beside the final PBO and record hashes for both files. The installed `DSSignFile` reports signature v3 by default and offers `-v2`; that is unrelated to the server setting `verifySignatures = 2`.

### DSCheck Is a Narrow Tool Check

Run `DSCheckSignatures.exe <checked-directory> <keys-directory>` against a clean release directory and interpret all of its stdout, not only its exit code. The fixture linked below requires a one-to-one set of expected `Signature ... is OK` lines and rejects missing keys, missing signatures, wrong signatures, duplicates, and other output.

This is deliberately narrow: in the recorded tool experiment, DSCheck accepted an old `.bisign` next to rebuilt PBO bytes and returned exit code zero when a public key was missing. It is not proof that adjacent PBO bytes match, that `verifySignatures = 2` rejects each failure mode, or that PBOs loaded only through `-serverMod` are operationally checked. Prove those with clean client/server tests.

### Server-Side Key Installation

Server admins place the public key (`.bikey`) in the server's `keys/` directory:

```
DayZServer/
  keys/
    MyModKey.bikey             <-- Allows clients with this mod to connect
```

### Key Rotation

Reuse an available, uncompromised key for ordinary updates. Rotate when the private key is compromised, lost or otherwise unavailable, or when you intentionally reset trust. A rotation means re-signing final PBOs and requires server operators to install the new `.bikey`; do not rotate merely because the update is a breaking version.

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

### Multi-PBO and Server Packages

Use a separate package for content that must stay server-side. The folder boundary is the documented launch boundary; a PBO inside a shared package is not documented as selectively excluded from clients.

```
@MyMod/                              <-- `-mod=@MyMod` on server and clients
  Addons/
    MyMod_Core.pbo
    MyMod_Scripts.pbo
    MyMod_Data.pbo
  Keys/
    MyStudio.bikey
  mod.cpp

@MyModServer/                        <-- `-serverMod=@MyModServer` on the server only
  Addons/
    MyMod_Server.pbo
  mod.cpp
```

`-mod=` and `-serverMod=` select mod folders/packages. The reviewed DayZ server documentation says `-serverMod` folders are not broadcast to clients. It does not document per-PBO server-only routing within one `@MyMod`; verify the clean-client distribution behavior of your target deployment before making a stronger claim.

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

Use automation for every multi-PBO release, but do not treat exit code `0` as success. The accepted workflow is deliberately two-phase so a release-wide collision check happens before any key or signature exists.

### Reliable Two-Phase Workflow

**Phase 1 — build and inspect every component.** For each manifest component, use a separate source root, temporary directory, and build-output directory. Invoke Addon Builder with a validated `-toolsDirectory` (or explicit dependent-tool paths), retain stdout/stderr, reject `FATAL`/`ERROR`, require exactly one new non-empty PBO, move it to its manifest final name, and inspect that final PBO's prefix and complete member table with BankRev.

After every component is finally named and inspected, combine `prefix + member` paths, normalize them case-insensitively, and fail on a duplicate by default. This is a conservative release policy, not a demonstrated engine rule: sharing a prefix is not itself a dependency mechanism or proof of an error. Allow a duplicate only through a documented allowlist backed by a controlled runtime test for the supported DayZ build; do not rely on launch-list order to choose a winner.

**Phase 2 — hash, sign, and package only the clean set.** Hash each final PBO, sign those final bytes, require exactly one expected `.bisign` beside each PBO, and copy only manifest-listed PBOs, signatures, `mod.cpp`, and public keys into the release packages. Run an exhaustive stdout-checked DSCheck pass against clean release and keys directories, then retain the manifest, commands, tool hashes, PBO/signature hashes, prefixes, member inventory, collision result, and DSCheck output in a receipt.

### Reproducible Fixture

The repository provides [an isolated four-component fixture](../../examples/en/multi-pbo/README.md). Its README explains the local `manifest.json` fields and the exact command below; open the manifest from your local checkout rather than relying on a separately published JSON route. The fixture requires PowerShell, a writable `WorkRoot` **outside** `examples/en/multi-pbo`, and an installed DayZ Experimental Tools root that contains Addon Builder, BankRev, and the DS utilities:

```powershell
.\examples\en\multi-pbo\build.ps1 `
  -ToolRoot 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools' `
  -WorkRoot 'D:\StarDZ\docs\wiki\TEMP\pbo-example-run'
```

It builds `Core`, `Scripts`, `Data`, and `Server` into two folder-level packages, verifies final names and prefixes, performs the global collision check before creating a key or signature, and writes a receipt beneath `WorkRoot`. The recorded accepted run used the official tools listed in the fixture's README on 2026-09-13. The checked-in fixture subsequently ran in one bounded headless DayZDiag `1.29.0.163709` server case: its script class and server component resolved, and it read the Data sentinel (`81` bytes). The harness stopped that server for cleanup, rather than observing a natural clean shutdown, and this runtime case does not run automatically.

That one fixed-fixture case does **not** validate client join/distribution, dependency-control variations, `verifySignatures = 2` enforcement, serverMod-only signature behavior, numeric size limits, Workshop service behavior, or behavior on other game or tool versions.


---

## Multi-PBO Mod Builds

Split an addon when it improves rebuild time, ownership, or release diagnosis. Keep the following four names distinct:

| Name | Example | Purpose |
|------|---------|---------|
| Launch package | `@MyMod` in `-mod=@MyMod` | Makes a mod folder and its PBOs available to a process. |
| Physical archive | `MyMod_Scripts.pbo` | Build, signing, and distribution unit; its filename is not a dependency identifier. |
| Virtual root | `MyMod/Scripts` prefix | Mounts a member as a virtual path such as `MyMod/Scripts/3_Game/Foo.c`. |
| Addon identity | `MyMod_Scripts` in `CfgPatches` | A name another addon can put in `requiredAddons[]`. |

`requiredAddons[]` contains `CfgPatches` class names, never PBO filenames, prefixes, mod-folder names, or Workshop IDs. It declares configuration/addon initialization dependencies after the required packages have already been installed and placed on the relevant launch list; it does not download or discover a missing package. Give each independently load-ordered configuration addon a unique `CfgPatches` class, but do not claim a one-to-one PBO-to-addon mapping: a PBO can expose additional configuration roots, and retail resource PBOs can exist without a root config.

### Prefixes, Virtual Paths, and Dependencies

The prefix mounts archive members into one virtual namespace. `CfgMods.inputs` and script-module `files[]` refer to those mounted virtual paths, not paths relative to a physical PBO root. A path authored in one configuration can be supplied by another archive only if the final mounted namespace resolves it; treat cross-PBO path arrangements as a packaged-runtime test, not syntax proof. The fixture's raw manifest stores PBO prefixes with backslashes (for example, `PBOExample\\Scripts`), while its `CfgMods` `files[]` values use forward-slash virtual paths (for example, `PBOExample/Scripts/scripts/3_Game`); retain the separator form required by each context.

```cpp
// MyMod_Scripts/config.cpp, packed as MyMod_Scripts.pbo with prefix MyMod/Scripts
class CfgPatches
{
    class MyMod_Scripts
    {
        requiredAddons[] = { "MyMod_Core", "DZ_Scripts" };
    };
};

class CfgMods
{
    class MyMod
    {
        type = "mod";
        class defs
        {
            class worldScriptModule
            {
                value = "";
                files[] = { "MyMod/Scripts/4_World" };
            };
        };
    };
};
```

The example's `requiredAddons[]` values are addon identities, while `files[]` is a virtual path formed after the prefix is mounted. `CfgMods.dependencies[]` names script-module dependencies; it is not a replacement for `requiredAddons[]` and is not a physical-PBO dependency declaration.

### Shared and Server-Only Packages

Put shared/client PBOs in `@MyMod` and load that folder with `-mod`. Put server-only code and assets in a separate `@MyModServer` folder and load it only with `-serverMod`. The server addon can depend on a shared addon, for example `MyMod_Server -> MyMod_Scripts -> MyMod_Core -> DZ_Data`; in that case both packages must be installed and listed on the server. Do not place a server-only PBO inside the shared Workshop package and assume the engine will omit it from clients.

### Size and Collision Discipline

Splitting a texture-heavy or model-heavy addon can make incremental builds and diagnosis easier. Do not diagnose an `ACCESS_VIOLATION` solely from archive size; inspect logs and isolate the failing addon and asset. A numeric threshold is not a substitute for testing the packaged mod.

Sharing a prefix is a virtual-tree merge, not a dependency relationship. Normalize virtual paths case-insensitively across the release and fail on duplicates by default. Permit one only through an explicit allowlist plus a controlled runtime test for the supported DayZ build; never rely on textual launch order to choose a winning file.

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
2. Rebuild and sign the final PBO bytes with the existing trusted key.
3. Replace the server `.bikey` only when the signing key was intentionally rotated.

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

5. **Sign final distributed PBOs for signature-verified multiplayer testing.** Sign after the last byte-changing operation, retain the expected `.bisign`, and test against the target server configuration.

6. **Reuse keys deliberately.** Keep an uncompromised key for ordinary updates. Rotate only after compromise, loss/unavailability, or an intentional trust reset, then arrange for every server to install the new public key.

7. **Test both file patching and PBO modes.** Some bugs only appear in one mode. Binarized configs behave differently from text configs in edge cases.

8. **Clean your output directory regularly.** Stale PBOs from previous builds can cause confusing behavior. Remove stale output PBOs deliberately. `-clear` cleans temporary binarization data for the current project; it does not clean the output directory.

9. **Split large mods into multiple PBOs.** The time saved on incremental rebuilds pays for itself within the first day of development.

10. **Read the build logs.** Binarize and AddonBuilder produce log files. When something goes wrong, the answer is almost always in the logs. The installed AddonBuilder `logger.xml` writes `AddonBuilder.rpt`, `AddonBuilderProcess.rpt` and `AddonBuilder.User.rpt` under `DayZ Tools\Bin\Logs\`. The Windows temporary directory (or `-temp`) holds binarized intermediate files, not these configured log files.

---

## Observed Implementation Choices

Pinned code examples show several project-specific layouts: Community Framework separates [`JM_CF_GUI` in `JM/CF/GUI/config.cpp`](https://github.com/Arkensor/DayZ-CommunityFramework/blob/0763e7e7548c9a0bed6626afff835de80693ebf3/JM/CF/GUI/config.cpp#L1-L13) from the [`JM_CF_Scripts` `CfgPatches`/`CfgMods` roots](https://github.com/Arkensor/DayZ-CommunityFramework/blob/0763e7e7548c9a0bed6626afff835de80693ebf3/JM/CF/Scripts/config.cpp#L1-L103); Community Online Tools declares [`JM_COT_Scripts` and its script modules](https://github.com/Jacob-Mango/DayZ-CommunityOnlineTools/blob/41f2c2b99565d0e3970163e162efbf1283fdca62/JM/COT/Scripts/config.cpp#L1-L103); Expansion defines [`DayZExpansion_Core_Scripts`](https://github.com/salutesh/DayZ-Expansion-Scripts/blob/6dacd00f6d943ebbd99e0cf1baad93f470d96419/DayZExpansion/Core/Scripts/config.cpp#L1-L110); DayZ Editor separates its [`Editor_Scripts` configuration](https://github.com/InclementDab/DayZ-Editor/blob/992e6b29b42b5d8e609632b59771335a23d205eb/DayZEditor/Scripts/config.cpp#L1-L64) from [`Editor_GUI`](https://github.com/InclementDab/DayZ-Editor/blob/992e6b29b42b5d8e609632b59771335a23d205eb/DayZEditor/GUI/config.cpp#L10-L21); and VPP Admin Tools uses a root [`DZM_VPPAdminToolsScripts` config](https://github.com/VanillaPlusPlus/VPP-Admin-Tools/blob/dc22e420df3b54e821055f9764da1e48f4a31e71/config.cpp#L1-L10). These are implementation examples, not engine contracts; do not infer a required split, loader rule, or signing policy from them.

---

## Compatibility & Impact

- **Multi-Mod:** Choose distinct virtual paths for unrelated assets and reject normalized duplicate virtual paths in your release build. Same-prefix collision winner behavior was not established by this audit, so do not rely on it.
- **Performance:** PBO loading is fast (sequential file reads), but mods with many large PBOs increase server startup time. Binarized content loads faster than unbinarized. Use ODOL models and PAA textures for release builds.
- **Tool options:** Check the help embedded in your installed AddonBuilder when scripting a build; use full paths for tools and signing keys.

---

## Evidence and Validation Scope

The format-field discussion uses the explicitly unofficial [PBO File Format](https://community.bistudio.com/wiki/PBO_File_Format) description, the reviewed retail archive, and the recorded reader inspection; it is not a Bohemia-supported format contract. The package, dependency, and virtual-path guidance was cross-checked against the [DayZ Modding Structure](https://community.bistudio.com/wiki/DayZ:Modding_Structure) snapshot, the official DayZ Samples pinned [`Test_Inputs/config.cpp` `CfgPatches`, `inputs`, and module paths](https://github.com/BohemiaInteractive/DayZ-Samples/blob/da5e5437c9502620d9853fb6eed14701135ab2ea/Test_Inputs/config.cpp#L1-L33), and the extracted `DZ/data_sakhal/config.cpp`. Folder-level launch routing and `verifySignatures = 2` wording comes from the reviewed [DayZ Server Configuration](https://community.bistudio.com/wiki/DayZ:Server_Configuration) snapshot.

The local audit receipt retains the reviewed source hashes, tool versions, accepted fixture run, and unresolved runtime tests, accessed 2026-09-13. A documentation build checks this page's rendering and links only; it does not validate a PBO, Enforce compilation, game/server behavior, signature enforcement, Workshop delivery, or a numeric archive boundary.
