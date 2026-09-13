# Creating a Custom Item


---

> **Summary:** This tutorial walks you through adding a brand-new item to DayZ. You will define the item in config.cpp, give it textures using hidden selections, add it to the server's spawn table, create a string table for its display name, and test it in-game. By the end, you will have a custom item that players can find, pick up, and carry in their inventory.

---

## Table of Contents

- [What We Are Building](#what-we-are-building)
- [Prerequisites](#prerequisites)
- [Step 1: Define the Item Class in config.cpp](#step-1-define-the-item-class-in-config-cpp)
- [Step 2: Set Up Hidden Selections for Textures](#step-2-set-up-hidden-selections-for-textures)
- [Step 3: Create Basic Textures](#step-3-create-basic-textures)
- [Step 4: Add to types.xml for Server Spawning](#step-4-add-to-types-xml-for-server-spawning)
- [Step 5: Create a Display Name with Stringtable](#step-5-create-a-display-name-with-stringtable)
- [Step 6: Test In-Game](#step-6-test-in-game)
- [Step 7: Polish -- Model, Textures, and Sounds](#step-7-polish-model-textures-and-sounds)
- [Complete File Reference](#complete-file-reference)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## What We Are Building

We will create an item called **Ration Snack** -- a retextured snack packet that players can find in the world, pick up, and store in their inventory. It will:

- Use a vanilla model (borrowed from an existing item) so we do not need 3D modeling
- Have a custom retextured appearance using hidden selections
- Appear in the server's spawn table
- Have a proper display name and description

This is the standard workflow for creating any item in DayZ, whether it is food, tools, clothing, or building materials.

The model we borrow is the one vanilla uses for `Crackers` and `Chips`. It is chosen deliberately: `DZ\gear\food\config.cpp` declares that model's hidden selection by name, so every path, selection and texture in this chapter can be checked against a shipped config instead of guessed. Step 2 shows exactly how that check is done, so you can repeat it for any other model.

---

## Prerequisites

- A working mod structure (complete [Chapter 8.1](01-first-mod.md) first)
- A text editor
- DayZ Tools installed (for texture conversion, optional)

We will build on top of the mod from Chapter 8.1. Your current structure should look like:

```
MyFirstMod/
    mod.cpp
    Scripts/
        config.cpp
        5_Mission/
            MyFirstMod/
                MissionHello.c
```

---

## Step 1: Define the Item Class in config.cpp

Items such as this ration packet are defined in `CfgVehicles`. Firearms and magazines use `CfgWeapons` and `CfgMagazines` respectively.

### Create a Data config.cpp

It is best practice to keep item definitions in a separate PBO from your scripts. Create a new folder structure:

```
MyFirstMod/
    mod.cpp
    Scripts/
        config.cpp              <-- Already exists (scripts)
    Data/
        config.cpp              <-- NEW (item definitions)
```

Create the file `MyFirstMod/Data/config.cpp` with this content:

```cpp
class CfgPatches
{
    class MyFirstMod_Data
    {
        units[] = { "MFM_RationSnack" };
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data",
            "DZ_Gear_Food"
        };
    };
};

class CfgVehicles
{
    class Inventory_Base;

    class MFM_RationSnack : Inventory_Base
    {
        scope = 2;
        displayName = "$STR_MFM_RationSnack";
        descriptionShort = "$STR_MFM_RationSnack_Desc";
        model = "\DZ\gear\food\salty_chips.p3d";
        rotationFlags = 1;
        weight = 50;
        itemSize[] = { 2, 2 };
        absorbency = 0.5;

        class DamageSystem
        {
            class GlobalHealth
            {
                class Health
                {
                    hitpoints = 100;
                    healthLevels[] =
                    {
                        { 1.0, {} },
                        { 0.7, {} },
                        { 0.5, {} },
                        { 0.3, {} },
                        { 0.0, {} }
                    };
                };
            };
        };

        hiddenSelections[] = { "camoGround" };
        hiddenSelectionsTextures[] = { "MyFirstMod\Data\Textures\ration_snack_co.paa" };
    };
};
```

`requiredAddons[]` declares which vanilla addons yours depends on. `DZ_Gear_Food` is the `CfgPatches` class of the addon that ships `salty_chips.p3d` -- you can read it at the top of `DZ\gear\food\config.cpp`, the same way that file declares its own dependency on `DZ_Data`. Whenever you borrow a vanilla asset, name the addon that ships it here.

### What Each Field Does

| Field | Value | Explanation |
|-------|-------|-------------|
| `scope` | `2` | Makes the item public -- spawnable and visible in admin tools. Use `0` for base classes that should never spawn directly. |
| `displayName` | `"$STR_MFM_RationSnack"` | References a string table entry for the item name. The `$STR_` prefix tells the engine to look it up in `stringtable.csv`. |
| `descriptionShort` | `"$STR_MFM_RationSnack_Desc"` | Short description shown in the inventory tooltip. |
| `model` | Path to `.p3d` | The 3D model. We borrow `salty_chips.p3d`, the model vanilla `Crackers` and `Chips` use. The `\DZ\` prefix references vanilla game files. |
| `rotationFlags` | `1` | Bitmask controlling which inventory rotations the engine allows. The meaning of individual bits is not documented in the shipped configs or scripts, so copy the value a vanilla item with a similar shape uses. `1` is what vanilla's own `Snack_ColorBase` sets, and is the most common value in the game data (161 uses); `17` is the next most common (114). |
| `weight` | `50` | Weight in grams. Free choice -- vanilla's snack items use `10`. |
| `itemSize[]` | `{ 2, 2 }` | Inventory grid size, in `{ columns, rows }` order -- `{ 2, 2 }` matches what vanilla sets for this model. `{ 1, 2 }` would be 1 column wide and 2 rows tall. |
| `absorbency` | `0.5` | How much the item absorbs water (0 = none, 1 = fully). Affects item when it rains. Vanilla uses values across the whole 0--1 range. |
| `hiddenSelections[]` | `{ "camoGround" }` | Named texture slots on the model that can be overridden. `"camoGround"` is the selection vanilla's `Crackers` declares for this exact model, which is why it is safe to use here. For any other model, confirm the name first (see [Finding Hidden Selection Names](#finding-hidden-selection-names)). |
| `hiddenSelectionsTextures[]` | Path to `.paa` | Your custom texture for each hidden selection. |

### About the Parent Class

```cpp
class Inventory_Base;
```

This line is a **forward declaration**. It tells the config parser that `Inventory_Base` exists (it is defined in vanilla DayZ). Your item class then inherits from it:

```cpp
class MFM_RationSnack : Inventory_Base
```

`Inventory_Base` is the standard parent for small items that go in the player's inventory. Other common parent classes include:

| Parent Class | Use For |
|-------------|---------|
| `Inventory_Base` | Generic inventory items |
| `Edible_Base` | Food and drink |
| `Clothing_Base` | Wearable clothing/armor |
| `Weapon_Base` | Firearms |
| `Magazine_Base` | Magazines and ammo boxes |
| `HouseNoDestruct` | Buildings and structures |

### About DamageSystem

The `DamageSystem` block defines how the item takes damage and degrades. The `healthLevels` array maps health percentages to texture states:

- `1.0` = pristine
- `0.7` = worn
- `0.5` = damaged
- `0.3` = badly damaged
- `0.0` = ruined

The empty `{}` after each level is where you would specify damage overlay textures. For simplicity, we leave them empty.

---

## Step 2: Set Up Hidden Selections for Textures

Hidden selections are the mechanism DayZ uses to swap textures on a 3D model without modifying the model file itself. The selection names are defined by the model, so you cannot invent them -- you have to find out what the model already exposes.

For `salty_chips.p3d` the answer is in the game data. `DZ\gear\food\config.cpp` defines:

```cpp
class Crackers: Snack_ColorBase
{
    model="\DZ\gear\food\salty_chips.p3d";
    hiddenSelections[]=
    {
        "camoGround"
    };
    hiddenSelectionsTextures[]=
    {
        "\dz\gear\food\Data\salted_crackers_co.paa"
    };
};
```

`Crackers` declares `hiddenSelections[]` itself rather than inheriting it, so this is a confirmed model-to-selection pairing: the model is `salty_chips.p3d`, the selection is `camoGround`, and one texture slot is filled. `Chips` is a second class in the same file using the same model and selection with a different texture -- which is exactly the retexture you are about to do.

### How Hidden Selections Work

1. The 3D model (`.p3d`) defines named regions called **selections**
2. In config.cpp, `hiddenSelections[]` lists which selections you want to override
3. `hiddenSelectionsTextures[]` provides your replacement textures, in matching order

```cpp
hiddenSelections[] = { "camoGround" };
hiddenSelectionsTextures[] = { "MyFirstMod\Data\Textures\ration_snack_co.paa" };
```

The first entry in `hiddenSelectionsTextures` replaces the first entry in `hiddenSelections`. If you had multiple selections:

```cpp
hiddenSelections[] = { "camoGround", "camoMale", "camoFemale" };
hiddenSelectionsTextures[] = { "path\tex1.paa", "path\tex2.paa", "path\tex3.paa" };
```

### Finding Hidden Selection Names

For a vanilla model, read the vanilla `config.cpp` of an item that already uses it. Search the extracted game data for the model filename and look at the class that sets it:

| What you find | What it tells you |
|---------------|-------------------|
| The class declares `hiddenSelections[]` itself | The names and their order, directly. This is the case for `salty_chips.p3d` via `Crackers`. |
| Only `hiddenSelectionsTextures[]`, no `hiddenSelections[]` | The selection list is inherited from a base class. The number of texture entries tells you how many slots exist, but **not** their names -- and if the base class lives in an addon whose config you cannot read, the names are not recoverable this way. |
| Neither | That class does not retexture through config at all. |

The second row is a real limitation, not a formality. The vanilla book model `book_kniga.p3d` is an example: all 145 book entries in `DZ\gear\books\config.cpp` set only `hiddenSelectionsTextures[]` and inherit from `Book_Base`, which that file merely forward-declares. The selection name for that model is therefore not discoverable from the shipped configs, and a guessed name fails silently -- the item loads and the texture is simply ignored. That is why this chapter borrows a model whose selection name a shipped config states outright.

**Object Builder** shows a model's **Named Selections** list, and that is the authoritative answer -- for a model you can open. Bohemia's Object Builder documentation lists its P3D input support as *"nonbinarized version[MLOD]"* and its P3D output as *"nonbinarized"*. The `.p3d` files shipped with the retail game are binarized, so Object Builder is the right tool for a source model you or another modder authored and not a way to inspect a borrowed vanilla one. For borrowed assets, read a vanilla `config.cpp` that already uses the model.

---

## Step 3: Create Basic Textures

DayZ uses `.paa` format for textures. During development, you can start with a simple colored image and convert it later.

### Create the Texture Folder

```
MyFirstMod/
    Data/
        config.cpp
        Textures/
            ration_snack_co.paa
```

### Option A: Use a Placeholder (Fastest)

For initial testing, you can point `hiddenSelectionsTextures` to a vanilla texture instead of creating your own:

```cpp
hiddenSelectionsTextures[] = { "\dz\gear\food\Data\salted_crackers_co.paa" };
```

That is the exact path vanilla `Crackers` uses, copied with its original casing. Your item will look identical to vanilla crackers but will function as your custom item, which is a useful first test: if it renders correctly, the model path and the selection name are both right, and anything that goes wrong afterwards is in your own texture. Replace it with your own texture once you confirm that.

### Option B: Create a Custom Texture

1. **Create a source image:**
   - Open any image editor (GIMP, Photoshop, Paint.NET, or even MS Paint)
   - Create a new image at **512x512 pixels** (power-of-2 dimensions are required: 256, 512, 1024, 2048)
   - Fill it with a color or design. For a ration packet, a flat colour with some lettering is enough to tell it apart from vanilla.
   - Save as `.tga` (TGA format) or `.png`

2. **Convert to `.paa`:**
   - Open **TexView2** from DayZ Tools
   - Go to **File > Open** and select your `.tga` or `.png`
   - Go to **File > Save As** and save as `.paa` format
   - Save it to `MyFirstMod/Data/Textures/ration_snack_co.paa`

   The `_co` suffix is a naming convention meaning "color" (the diffuse/albedo texture). Other suffixes include `_nohq` (normal map), `_smdi` (specular), and `_as` (ambient shadow).

### Texture Naming Conventions

| Suffix | Type | Purpose |
|--------|------|---------|
| `_co` | Color (Diffuse) | The main color/appearance texture |
| `_nohq` | Normal Map | Surface detail and lighting normals |
| `_smdi` | Specular | Shininess and metallic properties |
| `_as` | Ambient shadow | Baked ambient-shadow/occlusion information |
| `_de` | Detail | Additional detail overlay |

For a first item, you only need the `_co` texture. The model will use default values for the others.

---

## Step 4: Add to types.xml for Server Spawning

The `types.xml` file controls what items spawn in the world, how many exist at once, and where they appear. This file lives in the server's **mission folder** (not in your mod).

### Locate types.xml

For a standard DayZ server, `types.xml` is at:

```
<DayZ Server>\mpmissions\dayzOffline.chernarusplus\db\types.xml
```

Or for a multiplayer mission:

```
<DayZ Server>\mpmissions\dayzOffline.chernarusplus\db\types.xml
```

### Add Your Item Entry

Open `types.xml` and add this block inside the root `<types>` element:

```xml
<type name="MFM_RationSnack">
    <nominal>10</nominal>
    <lifetime>14400</lifetime>
    <restock>1800</restock>
    <min>5</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0" />
    <category name="food" />
    <usage name="Town" />
    <usage name="Village" />
    <value name="Tier1" />
    <value name="Tier2" />
</type>
```

### What Each Tag Means

| Tag | Value | Explanation |
|-----|-------|-------------|
| `name` | `"MFM_RationSnack"` | Must match your config.cpp class name exactly |
| `nominal` | `10` | Target number of this item in the world at any time |
| `lifetime` | `14400` | Seconds before a dropped item despawns (14400 = 4 hours) |
| `restock` | `1800` | Minimum restock delay in seconds for this type; it is not the frequency of all Central Economy checks. |
| `min` | `5` | Minimum number the Central Economy tries to maintain |
| `quantmin` / `quantmax` | `-1` | Quantity range (-1 = not applicable, used for items with variable quantity like water bottles) |
| `cost` | `100` | Economy priority weight (higher = spawns more readily) |
| `flags` | Various | What counts toward the nominal limit |
| `category` | `"food"` | Item category for economy balancing |
| `usage` | `"Town"`, `"Village"` | Where the item spawns (location categories) |
| `value` | `"Tier1"`, `"Tier2"` | Map tier zones where the item appears |

### Common Usage and Value Tags

**Usage (where it spawns):**
- `Town`, `Village`, `Farm`, `Industrial`, `Military`, `Hunting`, `Medic`, `Coast`, `Firefighter`, `Prison`, `Police`, `School`, `ContaminatedArea`

**Value (map tier):**
- `Tier1` -- coast/starter areas
- `Tier2` -- inland towns
- `Tier3` -- military/northwest
- `Tier4` -- deepest inland/endgame

---

## Step 5: Create a Display Name with Stringtable

The string table provides localized text for item names and descriptions. DayZ reads string tables from `stringtable.csv` files.

### Create the Stringtable

Create the file `MyFirstMod/Data/Stringtable.csv` with this content:

```csv
"Language","original","english","czech","german","russian","polish","hungarian","italian","spanish","french","chinese","japanese","portuguese","chinesesimp",
"STR_MFM_RationSnack","Ration Snack","Ration Snack","","","","","","","","","","","","",
"STR_MFM_RationSnack_Desc","A sealed packet of salted crackers from an old ration kit.","A sealed packet of salted crackers from an old ration kit.","","","","","","","","","","","","",
```

This is the real column set and order used by DayZ's own `languagecore/stringtable.csv` and by Bohemia's `Test_Stringtable` sample: `Language, original, english, czech, german, russian, polish, hungarian, italian, spanish, french, chinese, japanese, portuguese, chinesesimp` -- 14 language columns after the key, all lowercase, and **no `korean` column**. Every row ends with a trailing comma, the header included, so each row parses to 16 CSV fields with an empty last one. Fill in at least `original` and `english`; the other columns can be left as empty strings -- vanilla itself ships rows with every language cell empty (13 rows in `languagecore/stringtable.csv`), so blanks are acceptable. Note that vanilla more often repeats the English string in an untranslated column than leaves it empty, and no source checked here establishes what the engine does at runtime with a genuinely empty cell.

### How String References Work

In your config.cpp, you wrote:

```cpp
displayName = "$STR_MFM_RationSnack";
```

The `$STR_` prefix tells the engine: "Look for a string table entry named `STR_MFM_RationSnack`." The engine searches all loaded `Stringtable.csv` files for a matching row and returns the text for the player's language.

### CSV Format Rules

- The first row must be the header with language names (in the exact order shown above)
- Each subsequent row is: `"KEY","original text","english text","czech text",...`
- All values must be double-quoted
- Separate values with commas
- Every row ends with a trailing comma after the last language column -- header and data rows alike. That is how both `languagecore/stringtable.csv` and Bohemia's own `Test_Stringtable` sample are written
- Save as UTF-8 encoding (important for non-ASCII characters in other languages). The vanilla file carries a UTF-8 byte-order mark

---

## Step 6: Test In-Game

### Update Your Scripts config.cpp

Before testing, you need to update your `Scripts/config.cpp` to also pack the Data folder, OR pack the Data folder as a separate PBO.

**Option A: Separate PBO (Recommended)**

Pack `MyFirstMod/Data/` as a second PBO:

```
@MyFirstMod/
    mod.cpp
    Addons/
        Scripts.pbo          <-- Contains Scripts/config.cpp and 5_Mission/
        Data.pbo             <-- Contains Data/config.cpp, Textures/, Stringtable.csv
```

Use Addon Builder with:
- Source: `MyFirstMod/Data/`
- Prefix: `MyFirstMod/Data`

**Option B: File Patching (Development)**

File patching lets the engine read loose files from your source tree instead of the packed copy, so you can iterate on scripts without repacking. It does **not** replace packing: the official procedure packs the PBO first and then exposes the source tree through a directory junction. In short --

1. Pack as in Option A, so `P:\Mods\@MyFirstMod\addons\` contains your PBOs.
2. Create the junction once, replacing the path with your own DayZ installation folder:

```batch
mklink /J "C:\Program Files (x86)\Steam\steamapps\common\DayZ\MyFirstMod" "P:\MyFirstMod"
```

3. Launch the diagnostic executable with the **packed** mod plus `-filePatching`:

```batch
start /D "C:\Program Files (x86)\Steam\steamapps\common\DayZ" DayZDiag_x64.exe "-mod=P:\Mods\@MyFirstMod" -filePatching
```

4. If you are connecting to a server, that server needs `allowFilePatching = 1;` in `serverDZ.cfg`, or the client will be refused.

Edits to `.c` and `.layout` files are picked up without repacking. After editing `config.cpp` -- which is most of what you do in this chapter -- repack and relaunch: no primary Bohemia source states that a loose `config.cpp` is re-read under file patching. [Chapter 8.6](06-debugging-testing.md#file-patching-edit-without-rebuilding) covers the whole workflow and what each step is for.

### Spawn the Item Using the Script Console

The fastest way to test your item without waiting for it to spawn naturally:

1. Launch DayZ with your mod loaded
2. Join your local server or start offline mode
3. Open the **script console** (if using DayZDiag, this is available from the debug menu)
4. In the script console, type:

```c
GetGame().GetPlayer().GetInventory().CreateInInventory("MFM_RationSnack");
```

5. Press **Execute** (or the run button)

The item should appear in your character's inventory.

### Alternative: Spawn Near Player

If your inventory is full, spawn the item on the ground near your character:

```c
vector pos = GetGame().GetPlayer().GetPosition();
GetGame().CreateObject("MFM_RationSnack", pos, false, false, true);
```

### What to Check

1. **Does the item appear?** If yes, the config.cpp class definition is correct.
2. **Does it have the right name?** Check that "Ration Snack" appears (not `$STR_MFM_RationSnack`). If you see the raw string reference, the stringtable is not loading.
3. **Does it have the right texture?** If using a custom texture, verify the colors match. If the item still looks exactly like vanilla crackers, your own texture is not being found and the model fell back to its own material; if it appears white or pink, the path is wrong in a way that resolved to nothing at all.
4. **Can you pick it up?** If the item spawns but cannot be picked up, check `itemSize` and `scope`.
5. **Does the inventory icon look correct?** The size should match your `itemSize[]` definition.

---

## Step 7: Polish -- Model, Textures, and Sounds

Once your item works with a borrowed model, you can upgrade it with custom assets.

### Custom 3D Model

Creating a custom `.p3d` model requires:

1. **Blender or 3DS Max** with the DayZ tools plugin (Blender is free)
2. Export the model as `.p3d` using Object Builder
3. Define proper geometry (visual mesh), fire geometry (collision), and view geometry (LODs)
4. Create UV maps for your textures
5. Define named selections for hidden selections

This is a significant undertaking. For most items, retexturing a vanilla model (as we did above) is sufficient.

### Improved Textures

For a professional-looking item:

1. Create a **2048x2048** texture for close-up detail (or 1024x1024 for small items)
2. Include a **normal map** (`_nohq.paa`) for surface detail without extra polygons
3. Include a **specular map** (`_smdi.paa`) for material properties (shininess, roughness)
4. Update your config:

```cpp
hiddenSelections[] = { "camoGround" };
hiddenSelectionsTextures[] = { "MyFirstMod\Data\Textures\ration_snack_co.paa" };
hiddenSelectionsMaterials[] = { "MyFirstMod\Data\Textures\ration_snack.rvmat" };
```

An `.rvmat` (Rvmat material file) ties all texture maps together. The material for the very model this chapter borrows is `DZ\gear\food\data\salted_crackers.rvmat`, and it is the right thing to copy: it sets `PixelShaderID = "Super"` / `VertexShaderID = "Super"` (not `"NormalMap"`) and chains six stages -- the normal map at `Stage1`, a grey placeholder at `Stage2`, a mask at `Stage3`, an alpha-surface placeholder at `Stage4`, the specular map at `Stage5` and a fresnel term at `Stage6`. The simplified two-stage version below shows the field names only; this wiki has not compiled or rendered it, so do not treat it as a working material. To get one that loads, copy the vanilla file and swap in your own texture paths:

```cpp
ambient[] = { 1.0, 1.0, 1.0, 1.0 };
diffuse[] = { 1.0, 1.0, 1.0, 1.0 };
forcedDiffuse[] = { 0.0, 0.0, 0.0, 0.0 };
emmisive[] = { 0.0, 0.0, 0.0, 1.0 };
specular[] = { 1.0, 1.0, 1.0, 1.0 };
specularPower = 60;

PixelShaderID = "Super";
VertexShaderID = "Super";

class Stage1
{
    texture = "MyFirstMod\Data\Textures\ration_snack_nohq.paa";
    uvSource = "tex";
};

class Stage2
{
    texture = "MyFirstMod\Data\Textures\ration_snack_smdi.paa";
    uvSource = "tex";
};
```

### Custom Sounds

To add a sound when the item is used or picked up:

1. Create a `.ogg` audio file in OGG Vorbis format.
2. Define `CfgSoundShaders` and `CfgSoundSets` in your Data config.cpp:

```cpp
class CfgSoundShaders
{
    class MFM_SnackOpen_SoundShader
    {
        samples[] = {{ "MyFirstMod\Data\Sounds\snack_open", 1 }};
        volume = 0.6;
        range = 3;
        limitation = 0;
    };
};

class CfgSoundSets
{
    class MFM_SnackOpen_SoundSet
    {
        soundShaders[] = { "MFM_SnackOpen_SoundShader" };
        volumeFactor = 1.0;
        frequencyFactor = 1.0;
        spatial = 1;
    };
};
```

Note: Sound file paths in `samples[]` do NOT include the `.ogg` extension.

### Adding Script Behavior

To give your item custom behavior (for example, an action when the player uses it), create a script class in `4_World`:

```
MyFirstMod/
    Scripts/
        config.cpp              <-- Add worldScriptModule entry
        4_World/
            MyFirstMod/
                MFM_RationSnack.c
        5_Mission/
            MyFirstMod/
                MissionHello.c
```

Update `Scripts/config.cpp` to include the new layer:

```cpp
dependencies[] = { "World", "Mission" };

class defs
{
    class worldScriptModule
    {
        value = "";
        files[] = { "MyFirstMod/Scripts/4_World" };
    };
    class missionScriptModule
    {
        value = "";
        files[] = { "MyFirstMod/Scripts/5_Mission" };
    };
};
```

Create `4_World/MyFirstMod/MFM_RationSnack.c`:

```c
class MFM_RationSnack extends Inventory_Base
{
    override bool CanPutInCargo(EntityAI parent)
    {
        if (!super.CanPutInCargo(parent))
            return false;

        return true;
    }

    override void SetActions()
    {
        super.SetActions();
        // Add custom actions here
        // AddAction(ActionInspectPacket);
    }

    override void OnInventoryEnter(Man player)
    {
        super.OnInventoryEnter(player);
        Print("[MyFirstMod] Player picked up the Ration Snack!");
    }

    override void OnInventoryExit(Man player)
    {
        super.OnInventoryExit(player);
        Print("[MyFirstMod] Player dropped the Ration Snack.");
    }
};
```

---

## Complete File Reference

### Final Directory Structure

```
MyFirstMod/
    mod.cpp
    Scripts/
        config.cpp
        4_World/
            MyFirstMod/
                MFM_RationSnack.c
        5_Mission/
            MyFirstMod/
                MissionHello.c
    Data/
        config.cpp
        Stringtable.csv
        Textures/
            ration_snack_co.paa
```

### MyFirstMod/mod.cpp

```cpp
name = "My First Mod";
author = "YourName";
version = "1.1";
overview = "My first DayZ mod with a custom item: the Ration Snack.";
```

### MyFirstMod/Scripts/config.cpp

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

        dependencies[] = { "World", "Mission" };

        class defs
        {
            class worldScriptModule
            {
                value = "";
                files[] = { "MyFirstMod/Scripts/4_World" };
            };
            class missionScriptModule
            {
                value = "";
                files[] = { "MyFirstMod/Scripts/5_Mission" };
            };
        };
    };
};
```

### MyFirstMod/Data/config.cpp

```cpp
class CfgPatches
{
    class MyFirstMod_Data
    {
        units[] = { "MFM_RationSnack" };
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data",
            "DZ_Gear_Food"
        };
    };
};

class CfgVehicles
{
    class Inventory_Base;

    class MFM_RationSnack : Inventory_Base
    {
        scope = 2;
        displayName = "$STR_MFM_RationSnack";
        descriptionShort = "$STR_MFM_RationSnack_Desc";
        model = "\DZ\gear\food\salty_chips.p3d";
        rotationFlags = 1;
        weight = 50;
        itemSize[] = { 2, 2 };
        absorbency = 0.5;

        class DamageSystem
        {
            class GlobalHealth
            {
                class Health
                {
                    hitpoints = 100;
                    healthLevels[] =
                    {
                        { 1.0, {} },
                        { 0.7, {} },
                        { 0.5, {} },
                        { 0.3, {} },
                        { 0.0, {} }
                    };
                };
            };
        };

        hiddenSelections[] = { "camoGround" };
        hiddenSelectionsTextures[] = { "MyFirstMod\Data\Textures\ration_snack_co.paa" };
    };
};
```

### MyFirstMod/Data/Stringtable.csv

```csv
"Language","original","english","czech","german","russian","polish","hungarian","italian","spanish","french","chinese","japanese","portuguese","chinesesimp",
"STR_MFM_RationSnack","Ration Snack","Ration Snack","","","","","","","","","","","","",
"STR_MFM_RationSnack_Desc","A sealed packet of salted crackers from an old ration kit.","A sealed packet of salted crackers from an old ration kit.","","","","","","","","","","","","",
```

### types.xml Entry (Server Mission Folder)

```xml
<type name="MFM_RationSnack">
    <nominal>10</nominal>
    <lifetime>14400</lifetime>
    <restock>1800</restock>
    <min>5</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0" />
    <category name="food" />
    <usage name="Town" />
    <usage name="Village" />
    <value name="Tier1" />
    <value name="Tier2" />
</type>
```

---

## Troubleshooting

### Item Does Not Appear When Spawned via Script Console

- **Class name mismatch:** The name in the spawn command must match your config.cpp class name exactly: `"MFM_RationSnack"` (case-sensitive).
- **config.cpp not loaded:** Check that your Data PBO is packed and loaded, or that file patching is active.
- **CfgPatches missing:** Every config.cpp must have a valid `CfgPatches` block.

### Item Name Shows as `$STR_MFM_RationSnack` (Raw String Reference)

- **Stringtable not found:** Ensure `Stringtable.csv` is in the same PBO as the config that references it, or in the mod root.
- **Wrong key name:** The key in the CSV must match exactly (without the `$` prefix): `"STR_MFM_RationSnack"`.
- **CSV format error:** Make sure all values are double-quoted and the header row is correct.

### Item Appears All White, Pink, or Invisible

- **Texture path wrong:** Verify that `hiddenSelectionsTextures[]` points to the correct `.paa` file path. Paths use backslashes in config.cpp.
- **Hidden selection name wrong:** The selection name must match what the model defines, and a wrong name fails silently -- the item renders with the model's own material and nothing is logged. Confirm the name against a vanilla `config.cpp` that uses the same model.
- **Texture not in PBO:** If using packed PBOs, the texture file must be inside the PBO.

### Item Cannot Be Picked Up

- **`scope` not set to 2:** Ensure `scope = 2;` is in your item class.
- **`itemSize` too large:** If the item size exceeds the player's inventory space, they cannot pick it up.
- **Parent class wrong:** Make sure you are inheriting from `Inventory_Base` or another valid item parent.

### Item Spawns But Has Wrong Size in Inventory

- **`itemSize[]`:** The values are `{ columns, rows }`. `{ 1, 2 }` means 1 wide and 2 tall. `{ 2, 3 }` means 2 wide and 3 tall.

---

## Next Steps

1. **[Chapter 8.3: Building an Admin Panel Module](03-admin-panel.md)** -- Create a UI panel with server-client communication.
2. **Add variants** -- Create color variants of your item using different hidden selection textures.
3. **Add crafting recipes** -- Vanilla crafting recipes are defined in Enforce Script, not `config.cpp`: create a `4_World` class extending `RecipeBase` (see `4_World/classes/recipes/recipes/` in the vanilla scripts for examples like `AttachHolster`) and register it through `PluginRecipesManagerBase.RegisterRecipies()`. `CfgRecipes` is not a real config.cpp mechanism for this -- the engine defines only an unused internal path constant (`CFG_RECIPESPATH`) with that name.
4. **Create clothing** -- Extend `Clothing_Base` instead of `Inventory_Base` for wearable items.
5. **Build a weapon** -- Extend `Weapon_Base` for firearms with attachments and animations.

---

## Best Practices

- **Use `scope=2` for items that should be spawnable.** `scope=0` hides the item from admin tools and spawn commands. `scope=1` is for internal base classes only.
- **Always test hidden selections with a known-good texture first.** Point `hiddenSelectionsTextures[]` at the vanilla texture the model already uses, confirm it renders, then swap in your own. If the vanilla one works and yours does not, the problem is your texture or its path -- not the selection name.
- **Keep Data and Scripts in separate PBOs.** Item definitions (`CfgVehicles`) in `Data/config.cpp` and scripts in `Scripts/config.cpp` lets you update one without rebuilding the other.
- **Use the `$STR_` prefix for all player-visible text.** Even if you only support English, string table entries make future localization possible without code changes.
- **Test with the script console before adding to `types.xml`.** Spawning via `CreateInInventory()` confirms your config works before you spend time debugging spawn table issues.

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| `CfgVehicles` | Only for vehicles | Despite the name, `CfgVehicles` holds ALL entity definitions: items, buildings, animals, vehicles, and everything else. |
| Hidden selections | Replace any texture on any model | Not all models expose them, and a wrong selection name fails silently -- no error, no log line, the model just keeps its own material. Confirm the name against a vanilla config that uses the same model before blaming your texture. |
| `itemSize[]` | Defines how big the item looks in inventory | The order is `{ columns, rows }`, not `{ width, height }`: `{ 1, 2 }` is 1 column wide and 2 rows tall. Many modders mix these up and get a sideways item. |
| Stringtable fallback | Empty language columns fall back to English | Vanilla ships rows with empty language cells, so leaving columns blank is acceptable -- but vanilla more often repeats the English string than leaves a cell empty, and the runtime fallback behavior for a genuinely empty cell is not established here. Separately, if the entire Stringtable.csv fails to load (wrong path, encoding issue), you see raw `$STR_` keys in-game with no error in the script log. |

---

## What You Learned

In this tutorial you learned:
- How to define a new item class in `CfgVehicles` with inheritance from `Inventory_Base`
- How hidden selections allow retexturing vanilla models without 3D modeling
- How to add items to the server spawn table via `types.xml`
- How to create localized display names with `Stringtable.csv`
- How to add script behavior to an item class in the `4_World` layer

**Next:** [Chapter 8.3: Building an Admin Panel Module](03-admin-panel.md)

---

**Previous:** [Chapter 8.1: Your First Mod (Hello World)](01-first-mod.md)
**Next:** [Chapter 8.3: Building an Admin Panel Module](03-admin-panel.md)
