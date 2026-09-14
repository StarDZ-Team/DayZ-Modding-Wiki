# Textures (.paa, .edds, .tga)


---

DayZ uses **PAA** for model/material textures and **EDDS** for GUI resources such as imageset atlases. TGA and PNG are source artwork formats; the output format depends on the asset pipeline. This chapter covers the formats, naming conventions, resolution rules, and conversion workflow.

---

## Texture Formats Overview

DayZ uses four texture formats at different stages of the development pipeline:

| Format | Extension | Role | Alpha Support | Used At |
|--------|-----------|------|---------------|---------|
| **PAA** | `.paa` | Runtime game format (compressed) | Yes | Final build, shipped in PBOs |
| **EDDS** | `.edds` | Engine texture resource used by GUI | Yes | Workbench and shipped GUI atlases |
| **TGA** | `.tga` | Uncompressed source artwork | Yes | Artist workspace, Photoshop/GIMP export |
| **PNG** | `.png` | Portable source format | Yes | UI textures, external tools |

The general workflow is: **Source (TGA/PNG) --> DayZ Tools conversion --> PAA (game-ready)**.

---

## PAA Format

**PAA** (PAcked Arma) is the native compressed texture format used by the Enfusion engine at runtime. GUI resources can instead reference EDDS textures; do not convert every resource to PAA indiscriminately.

### Characteristics

- **Compressed:** Uses DXT1, DXT5, or ARGB8888 compression internally depending on alpha channel presence and quality settings.
- **Mipmapped:** PAA files contain a full mipmap chain, generated automatically during conversion. This is critical for rendering performance -- the engine selects the appropriate mip level based on distance.
- **Power-of-two dimensions:** The engine requires PAA textures to have dimensions that are powers of 2 (256, 512, 1024, 2048, 4096).
- **Read-only at runtime:** The engine loads PAA files directly from PBOs. You never edit a PAA file -- you edit the source and re-convert.

### Internal Compression Types

| Type | Alpha | Quality | Use Case |
|------|-------|---------|----------|
| **DXT1** | No (1-bit) | Good, 6:1 ratio | Opaque textures, terrain |
| **DXT5** | Full 8-bit | Good, 4:1 ratio | Textures with smooth alpha (glass, foliage) |
| **ARGB4444** | Full 4-bit | Medium | UI textures, small icons |
| **ARGB8888** | Full 8-bit | Lossless | Debug, highest quality (large file size) |
| **AI88** | Grayscale + alpha | Good | Normal maps, grayscale masks |

### When You See PAA Files

- Inside unpacked vanilla game data (`dta/` and addon PBOs)
- As the output of TexView2 conversion
- As the output of Binarize when processing source textures
- In your mod's final PBO after building

---

## EDDS Format

**EDDS** is an engine texture format used by the GUI resource pipeline. Shipped imagesets reference `.edds` atlases, for example `gui/imagesets/dayz_gui.imageset`. Keep these references and their resources together when packaging a GUI mod.

Reviewed imagesets reference `.edds` resources, but this review did not validate an EDDS creation, import, or conversion recipe. A DDS header alone does not establish that an arbitrary export or renamed file is a usable DayZ EDDS resource. Use TexView 2 or ImageToPAA only for the PAA material-texture workflow described below.

---

## TGA Format

**TGA** (Truevision TGA / Targa) is the traditional uncompressed source format for DayZ texture work. Many vanilla DayZ textures were originally authored as TGA files.

### Characteristics

- **Uncompressed:** No quality loss, full color depth (24-bit or 32-bit with alpha).
- **Large file sizes:** A 2048x2048 TGA with alpha is approximately 16 MB.
- **Alpha in dedicated channel:** TGA supports a proper 8-bit alpha channel (32-bit TGA), which maps directly to transparency in PAA.
- **TexView2 compatible:** TexView2 can open TGA files directly and convert them to PAA.

### When to Use TGA

- As your master source file for textures you author from scratch.
- When exporting from Substance Painter or Photoshop for DayZ.
- When the DayZ-Samples documentation specifies TGA as the source format.

### TGA Export Settings

When exporting TGA for DayZ conversion:

- **Bit depth:** 32-bit (if alpha is needed) or 24-bit (opaque textures)
- **Compression:** None (uncompressed)
- **Orientation:** Bottom-left origin (standard TGA orientation)
- **Resolution:** Must be power of 2 (see [Resolution Requirements](#resolution-requirements))

---

## PNG Format

**PNG** (Portable Network Graphics) is widely supported and can be used as an alternative source format, particularly for UI textures.

### Characteristics

- **Lossless compression:** Smaller than TGA but retains full quality.
- **Full alpha channel:** 32-bit PNG supports 8-bit alpha.
- **TexView2 compatible:** TexView2 can open and convert PNG to PAA.
- **UI-friendly:** Many UI imagesets and icons in mods use PNG as their source format.

### When to Use PNG

- **UI textures and icons:** PNG is the practical choice for imagesets and HUD elements.
- **Simple retextures:** When you only need a color/diffuse map with no complex alpha.
- **Cross-tool workflows:** PNG is universally supported across image editors, web tools, and scripts.

Bohemia documents PNG and uncompressed 24/32-bit TGA as source formats in [Arma: Texture Naming Rules](https://community.bistudio.com/wiki/Arma:_Texture_Naming_Rules). The filename suffix selects conversion rules in `TexConvert.cfg`.

---

## Texture Naming Conventions

DayZ uses a strict suffix system to identify the role of each texture. The engine and materials reference textures by filename, and the suffix tells both the engine and other modders what type of data the texture contains.

### Common Suffixes

| Suffix | Full Name | Purpose | Typical Format |
|--------|-----------|---------|----------------|
| `_co` | **Color / Diffuse** | The base color (albedo) of a surface | RGB, optional alpha |
| `_nohq` | **Normal Map (High Quality)** | Surface detail normals, defines bumps and grooves | RGB (tangent-space normal) |
| `_smdi` | **Specular / Diffuse-Inverse** | Stores specular intensity and power; diffuse is derived from the specular inverse | RGB channels encode separate data |
| `_ca` | **Color with Alpha** | Color texture where the alpha channel carries meaningful data (transparency, mask) | RGBA |
| `_as` | **Ambient Shadow** | Ambient occlusion / shadow bake | Grayscale |
| `_mc` | **Macro** | Large-scale color variation visible at distance | RGB |
| `_no` | **Normal Map (Standard)** | Lower quality normal map variant | RGB |
| `_mca` | **Vegetation macro resource** | Used by vanilla TreeAdv materials; interpret channels through the shader, not as a generic cutout mask | Shader-dependent |
| `_dt` | **Detail** | Tiling detail texture for close-up surface variation; average color should sit near 0.5 and mipmaps fade the texture out with distance | RGB |
| `_lco` | **Layer Color** | Terrain satellite/layer color | RGB |
| `_lca` | **Layer Color Alpha** | Layer-color alpha variant (`layer_color_alpha` in TexConvert.cfg) | RGBA |
| `_mask` | **Material Mask** | RGB mask for multimaterial blending | RGB |
| `_dtsmdi` | **Detail / Specular / Diffuse-Inverse** | SMDI variant retaining detail in red | RGB |
| `_ads` | **Ambient / Diffuse Shadow** | Green stores ambient shadow; blue stores diffuse shadow | RGB |


[Texture Map Types](https://community.bistudio.com/wiki/Texture_Map_Types) describes channel meanings by shader. For trees, macro alpha can carry lighting information; it is not necessarily transparency. For example, the vanilla `b_rosa_canina_1s` asset uses an `_mca` resource in a TreeAdv material and also has a separate `_ca` texture. Use the matching material to interpret the resource.

Self-illumination is configured through material properties such as `emmisive[]`; do not invent an `_li` stage in the Super shader.

### Naming Convention in Practice

A single item typically has multiple textures, all sharing a base name:

```
data/
  my_rifle_co.paa          <-- Base color (what you see)
  my_rifle_nohq.paa        <-- Normal map (surface bumps)
  my_rifle_smdi.paa         <-- Specular/metallic (shininess)
  my_rifle_as.paa           <-- Ambient shadow (baked AO)
  my_rifle_ca.paa           <-- Color with alpha (if transparency needed)
```

### The _smdi Channels

The SMDI texture stores specular data with diffuse derived from its inverse. The [HQ Normal Maps documentation](https://community.bistudio.com/wiki/HQ_Normal_Maps#Optimized_specular_map_onto_bit_depth) and installed `TexConvert.cfg` define the channels:

| Channel | Data | Range | Effect |
|---------|------|-------|--------|
| **R** | Constant | 255 | Set to white; the converter writes 1 here |
| **G** | Specular intensity | 0-255 | Controls the specular contribution |
| **B** | Specular power multiplier | 0-255 | Modulates the material specular power; white preserves the configured power |

### The _nohq Channels

Author normal maps with tangent-space RGB normals. This table describes source data, not the packed PAA bytes:

| Channel | Data |
|---------|------|
| **R** | X-axis normal (left-right) |
| **G** | Y-axis normal (up-down) |
| **B** | Z-axis normal (toward viewer) |
| **A** | Source opacity where the shader uses it; not specular power |

The installed `normalmap_hq` conversion rule writes `1-R` into output alpha and `1-A` into output red, while preserving green and blue. Do not paint a specular-power mask into `_nohq` alpha.

---

## Resolution Requirements

The Enfusion engine requires all textures to have **power-of-two dimensions**. Both width and height must independently be a power of 2, but they do not have to be equal (non-square textures are valid).

### Valid Dimensions

| Size | Typical Use |
|------|-------------|
| **64x64** | Tiny icons, UI elements |
| **128x128** | Small icons, inventory thumbnails |
| **256x256** | UI panels, small item textures |
| **512x512** | Standard item textures, clothing |
| **1024x1024** | Weapons, detailed clothing, vehicle parts |
| **2048x2048** | High-detail weapons, character models |
| **4096x4096** | Terrain textures, large vehicle textures |

### Non-Square Textures

Non-square power-of-two textures are valid:

```
256x512    -- Valid (both are powers of 2)
512x1024   -- Valid
1024x2048  -- Valid
300x512    -- INVALID (300 is not a power of 2)
```

### Resolution Guidelines

- **Weapons:** 2048x2048 for the main body, 1024x1024 for attachments.
- **Clothing:** 1024x1024 or 2048x2048 depending on surface area coverage.
- **UI icons:** 128x128 or 256x256 for inventory icons, 64x64 for HUD elements.
- **Terrain:** 4096x4096 for satellite maps, 512x512 or 1024x1024 for material tiles.
- **Normal maps:** Same resolution as the corresponding color texture.
- **SMDI maps:** Same resolution as the corresponding color texture.

> **Warning:** If a texture has non-power-of-two dimensions, the engine will either refuse to load it or display a magenta error texture. TexView2 will show a warning during conversion.

---

## Alpha Channel Support

The alpha channel in a texture carries additional data beyond color. How it is interpreted depends on the texture suffix and the material shader.

### Alpha Channel Roles

| Suffix | Alpha Interpretation |
|--------|---------------------|
| `_co` | Usually unused; if present, may define transparency for simple materials |
| `_ca` | Transparency mask (0 = fully transparent, 255 = fully opaque) |
| `_nohq` | Source opacity where the shader uses it; not specular power (see [The _nohq Channels](#the-nohq-channels)) |
| `_smdi` | Usually unused |
| `_mca` | Shader-dependent macro data; tree macro alpha can carry lighting, not a generic cutout mask |

### Creating Textures with Alpha

In your image editor (Photoshop, GIMP, Krita):

1. Create the RGB content as normal.
2. Add an alpha channel.
3. Paint white (255) where you want full opacity/effect, black (0) where you want none.
4. Export as 32-bit TGA or PNG.
5. Convert to PAA using TexView2 -- it will detect the alpha channel automatically.

### Verifying Alpha in TexView2

Open the PAA in TexView2 and use the channel display buttons:

- **RGBA** -- Shows the final composite
- **RGB** -- Shows color only
- **A** -- Shows alpha channel only (white = opaque, black = transparent)

---

## Converting Between Formats

### TexView2 (Primary Tool)

**TexView2** is included with DayZ Tools and is the standard texture conversion utility.

**Opening a file:**
1. Launch TexView2 from DayZ Tools or directly from `DayZ Tools\Bin\ImageToPAA\TexView.exe`.
2. Open your source file (TGA or PNG).
3. Verify the image looks correct and check dimensions.

**Converting to PAA:**
1. Open the source texture in TexView2.
2. Go to **File --> Save As**.
3. Select **PAA** as the output format.
4. Choose the compression type:
   - **DXT1** for opaque textures (no alpha needed)
   - **DXT5** for textures with alpha transparency
   - **ARGB4444** for small UI textures where file size matters
5. Click **Save**.

**Batch conversion via command line:**

```batch
REM ImageToPAA uses positional source and destination arguments.
"P:\DayZ Tools\Bin\ImageToPAA\ImageToPAA.exe" "source_co.tga" "output_co.paa"
```

### Binarize (Automated)

When Binarize processes your mod's source directory, it converts referenced source textures to PAA. AddonBuilder also offers `-binarizeAllTextures` to process TGA/PNG textures that are not referenced by a model or listed in `textures.lst`. Keep EDDS GUI resources in their own pipeline.

**Binarize conversion flow:**
```
source/mod_name/data/texture_co.tga
    --> Binarize detects TGA
        --> Converts to PAA with automatic compression selection
            --> Output: build/mod_name/data/texture_co.paa
```

### Manual Conversion Table

| From | To | Tool | Notes |
|------|----|------|-------|
| TGA / PNG | PAA | TexView 2 / ImageToPAA | Model/material workflow; retain the suffix |
| PAA | TGA / PNG | TexView 2 | Export for inspection; prefer original artwork for editing |
| PSD | TGA / PNG | Image editor | Export artwork before texture conversion |


---

## Texture Quality and Compression

### Compression Type Selection

| Scenario | Recommended Compression | Reason |
|----------|------------------------|--------|
| Opaque diffuse (`_co`) | DXT1 | Best ratio, no alpha needed |
| Transparent diffuse (`_ca`) | DXT5 | Full alpha support |
| Normal maps (`_nohq`) | DXT5 | Uses the normal-map channel packing in TexConvert.cfg |
| Specular maps (`_smdi`) | DXT1 | Usually opaque, RGB channels only |
| UI textures | ARGB4444 or DXT5 | Small size, clean edges |
| Vegetation macro (`_mca`) | Match the source resource | Shader-dependent data; not a generic cutout mask |

### Quality vs. File Size

```
Format        2048x2048 approx. size
-----------------------------------------
ARGB8888      21.3 MiB   (uncompressed, including mipmaps)
DXT5           5.3 MiB   (including mipmaps)
DXT1           2.7 MiB   (including mipmaps)
ARGB4444      10.7 MiB   (including mipmaps)
```

### In-Game Quality Settings

Players can adjust texture quality in DayZ's video settings. The engine selects lower mip levels when quality is reduced, so your textures will look progressively blurrier at lower settings. This is automatic -- you do not need to create separate quality levels.

---

## Real-World Examples

### Weapon Texture Set

A typical weapon mod contains these texture files:

```
MyMod_Weapons/data/weapons/m4a1/
  my_weapon_co.paa           <-- 2048x2048, DXT1, base color
  my_weapon_nohq.paa         <-- 2048x2048, DXT5, normal map
  my_weapon_smdi.paa          <-- 2048x2048, DXT1, specular / diffuse-inverse
  my_weapon_as.paa            <-- 1024x1024, DXT1, ambient shadow
```

The material file (`.rvmat`) references these textures and assigns them to shader stages.

### UI Texture (Imageset Source)

```
MyFramework/data/gui/icons/
  my_icons.edds             <-- GUI sprite atlas resource
```

UI textures are often packed into a single atlas (imageset) and referenced by name in layout files. Use a matching vanilla imageset as a template for texture resources and image rectangles.

### Terrain Textures

```
terrain/
  grass_green_co.paa         <-- 1024x1024, DXT1, tiling color
  grass_green_nohq.paa       <-- 1024x1024, DXT5, tiling normal
  grass_green_smdi.paa        <-- 1024x1024, DXT1, tiling specular
  grass_green_mc.paa          <-- 512x512, DXT1, macro variation
  grass_green_dt.paa          <-- 512x512, DXT1, detail tiling
```

Terrain textures tile across the landscape. The `_mc` macro texture adds large-scale color variation to prevent repetition.

---

## Common Mistakes

### 1. Non-Power-of-Two Dimensions

**Symptom:** Magenta texture in-game, TexView2 warnings.
**Fix:** Resize your source to the nearest power of 2 before converting.

### 2. Missing Suffix

**Symptom:** Material cannot find the texture, or it renders incorrectly.
**Fix:** Always include the proper suffix (`_co`, `_nohq`, etc.) in the filename.

### 3. Wrong Compression for Alpha

**Symptom:** Transparency looks blocky or binary (on/off with no gradient).
**Fix:** Use DXT5 instead of DXT1 for textures that need smooth alpha gradients.

### 4. Forgetting Mipmaps

**Symptom:** Texture looks fine up close but shimmers/sparkles at distance.
**Fix:** PAA files generated by TexView2 automatically include mipmaps. If you are using a non-standard tool, ensure mipmap generation is enabled.

### 5. Incorrect Normal Map Format

**Symptom:** Lighting on the model looks inverted or flat.
**Fix:** Ensure your normal map is in tangent-space format with DirectX-style Y-axis convention (green channel: up = lighter). Some tools export OpenGL-style (inverted Y) -- you need to invert the green channel.

### 6. Path Mismatch After Conversion

**Symptom:** Model or material shows magenta because it references a `.tga` path but the PBO contains `.paa`.
**Fix:** Materials should reference the final `.paa` path. Binarize handles path remapping automatically, but if you pack with `-packonly` (no binarization), you must ensure the paths match exactly.

---

## Best Practices

1. **Keep source files in version control.** Store TGA/PNG masters alongside your mod. PAA files are generated output.
2. **Match resolution to importance.** A rifle the player holds deserves 2048x2048. A can on a shelf can use 512x512.
3. **Always provide a normal map.** Even a flat normal map (128, 128, 255 solid fill) is better than none -- missing normal maps cause material errors.
4. **Name consistently.** One base name, multiple suffixes: `myitem_co.paa`, `myitem_nohq.paa`, `myitem_smdi.paa`.
5. **Follow the suffix-specific conversion rule.** DXT1 uses half the storage of DXT5, but normal maps and alpha textures need the appropriate channel packing and quality.
6. **Use atlas textures for UI icons.** Pack related icons into an atlas and reference named rectangles from an imageset.
7. **Create color variants via `hiddenSelectionsTextures[]`** instead of duplicating P3D models. Swap only the `_co.paa`.
8. **Watch VRAM usage.** A single 4096x4096 DXT5 texture uses ~21 MB of GPU memory with mipmaps. Prefer 1024 or 2048 for most items.
9. Two mods retexturing the same vanilla item via `hiddenSelectionsTextures[]` will conflict -- last loaded wins.

---

## Navigation

| Previous | Up | Next |
|----------|----|------|
| [Part 3: GUI System](../03-gui-system/07-styles-fonts.md) | [Part 4: File Formats & DayZ Tools](../04-file-formats/01-textures.md) | [4.2 3D Models](02-models.md) |
