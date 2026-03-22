# Chapter 4.1: Textures (.paa, .edds, .tga)

[Domů](../../README.md) | **Textury** | [Další: 3D modely >>](02-models.md)

---

## Úvod

Every surface you viz in DayZ -- weapon skins, clothing, terrain, UI icons -- is defined by texture files. Engine uses a proprietary compressed format called **PAA** za běhu, but during development you work with several zdrojový formáts that are converted during the build process. Understanding these formats, the naming conventions that bind them to materials, and the resolution rules engine enforces is fundamental to creating visual content for DayZ mods.

This chapter covers každý texture format you will encounter, the suffix naming system that tells engine how to interpret každý texture, resolution and alpha channel requirements, and the practical workflow for converting mezi formats.

---

## Obsah

- [Texture Formats Overview](#texture-formats-overview)
- [PAA Format](#paa-format)
- [EDDS Format](#edds-format)
- [TGA Format](#tga-format)
- [PNG Format](#png-format)
- [Texture Naming Conventions](#texture-naming-conventions)
- [Resolution Requirements](#resolution-requirements)
- [Alpha Channel Support](#alpha-channel-support)
- [Converting Mezi Formats](#converting-between-formats)
- [Texture Quality and Compression](#texture-quality-and-compression)
- [Real-World Examples](#real-world-examples)
- [Běžné Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Přehled formátů textur

DayZ uses four texture formats at odlišný stages of the development pipeline:

| Format | Extension | Role | Alpha Support | Used At |
|--------|-----------|------|---------------|---------|
| **PAA** | `.paa` | Runtime game format (compressed) | Yes | Final build, shipped in PBOs |
| **EDDS** | `.edds` | Editor/intermediate DDS variant | Yes | Object Builder preview, auto-converts |
| **TGA** | `.tga` | Uncompressed source artwork | Yes | Artist workspace, Photoshop/GIMP export |
| **PNG** | `.png` | Portable zdrojový formát | Yes | UI textures, externí přílišls |

Obecný pracovní postup je: **Source (TGA/PNG) --> DayZ Tools conversion --> PAA (game-ready)**.

---

## Formát PAA

**PAA** (PAcked Arma) is the native compressed texture format used by the Enfusion engine za běhu. Every texture that ships in a PBO must be in PAA format (or will be converted to it during binarization).

### Vlastnosti

- **Compressed:** Uses DXT1, DXT5, or ARGB8888 compression interníly depending on alpha channel presence and quality settings.
- **Mipmapped:** PAA files contain a plný mipmap chain, generated automatickýally during conversion. This is critical for rendering performance -- engine selects the appropriate mip level based on distance.
- **Power-of-two dimensions:** Engine requires PAA textures to have dimensions that are powers of 2 (256, 512, 1024, 2048, 4096).
- **Read-only za běhu:** Engine loads PAA files přímo from PBOs. You nikdy edit a PAA file -- you edit the source and re-convert.

### Interní typy komprese

| Type | Alpha | Quality | Use Case |
|------|-------|---------|----------|
| **DXT1** | No (1-bit) | Good, 6:1 ratio | Opaque textures, terrain |
| **DXT5** | Full 8-bit | Good, 4:1 ratio | Textures with smooth alpha (glass, foliage) |
| **ARGB4444** | Full 4-bit | Medium | UI textures, small icons |
| **ARGB8888** | Full 8-bit | Lossless | Debug, highest quality (large velikost souboru) |
| **AI88** | Grayscale + alpha | Good | Normal maps, grayscale masks |

### When You Viz PAA Files

- Inside unpacked vanilla game data (`dta/` and addon PBOs)
- As the output of TexView2 conversion
- As the output of Binarize when processing source textures
- In your mod's final PBO after building

---

## Formát EDDS

**EDDS** is an intermediate texture format used primarily by DayZ's **Object Builder** and the editor přílišls. It is essentially a variant of the standard DirectDraw Surface (DDS) format with engine-specific metadata.

### Vlastnosti

- **Preview format:** Object Builder can display EDDS textures přímo, making them užitečný during model creation.
- **Auto-converts to PAA:** Když run Binarize or AddonBuilder (without `-packonly`), EDDS files in your source tree are automatickýally converted to PAA.
- **Larger than PAA:** Soubory EDDS nejsou optimalizovány pro distribuci -- existují pro pohodlí editoru.
- **DayZ-Samples format:** Oficiální DayZ-Samples poskytované Bohemií používají EDDS textury rozsáhle.

### Pracovní postup s EDDS

```
Artist creates TGA/PNG source
    --> Photoshop DDS plugin exports EDDS for preview
        --> Object Builder displays EDDS on model
            --> Binarize converts EDDS to PAA for PBO
```

> **Tip:** You can skip EDDS celýly if you prefer. Convert your source textures přímo to PAA using TexView2 and reference the PAA paths in your materials. EDDS is a convenience, not a requirement.

---

## Formát TGA

**TGA** (Truevision TGA / Targa) is the traditional uncompressed zdrojový formát for DayZ texture work. Many vanilla DayZ textures were originally authored as TGA files.

### Vlastnosti

- **Uncompressed:** No quality loss, plný color depth (24-bit or 32-bit with alpha).
- **Large velikost souborus:** A 2048x2048 TGA with alpha is approximately 16 MB.
- **Alpha in dedicated channel:** TGA supports a proper 8-bit alpha channel (32-bit TGA), which maps přímo to transparency in PAA.
- **TexView2 compatible:** TexView2 can open TGA files přímo and convert them to PAA.

### Kdy použít TGA

- As your master zdrojový soubor for textures you author od nuly.
- When exporting from Substance Painter or Photoshop for DayZ.
- Když DayZ-Samples documentation or community tutorials specify TGA as the zdrojový formát.

### Nastavení exportu TGA

When exporting TGA for DayZ conversion:

- **Bit depth:** 32-bit (if alpha is needed) or 24-bit (opaque textures)
- **Compression:** None (uncompressed)
- **Orientation:** Bottom-left origin (standard TGA orientation)
- **Resolution:** Must be mocnina 2 (viz [Resolution Requirements](#resolution-requirements))

---

## Formát PNG

**PNG** (Portable Network Graphics) is widely podporovaný and lze použít as an alternative zdrojový formát, konkrétníly for UI textures.

### Vlastnosti

- **Lossless compression:** Smaller than TGA but retains plný quality.
- **Full alpha channel:** 32-bit PNG supports 8-bit alpha.
- **TexView2 compatible:** TexView2 can open and convert PNG to PAA.
- **UI-friendly:** Many UI imagesets and icons in mods use PNG as their zdrojový formát.

### Kdy použít PNG

- **UI textures and icons:** PNG is the practical choice for imagesets and HUD elements.
- **Simple retextures:** Když pouze need a color/diffuse map with no complex alpha.
- **Cross-tool workflows:** PNG is universally podporovaný across image editors, web přílišls, and scripts.

> **Poznámka:** PNG is not an official Bohemia zdrojový formát -- they prefer TGA. Nicméně the conversion přílišls handle PNG without issues and mnoho modders use it úspěšně.

---

## Konvence pojmenování textur

DayZ uses a strict suffix system to identify the role of každý texture. Engine and materials reference textures by filename, and the suffix tells oba engine and jiný modders what type of data the texture contains.

### Povinné přípony

| Suffix | Full Name | Purpose | Typical Format |
|--------|-----------|---------|----------------|
| `_co` | **Color / Diffuse** | The base color (albedo) of a surface | RGB, volitelný alpha |
| `_nohq` | **Normal Map (High Quality)** | Surface detail normals, defines bumps and grooves | RGB (tangent-space normal) |
| `_smdi` | **Specular / Metallic / Detail Index** | Controls shininess and metallic properties | RGB channels encode oddělený data |
| `_ca` | **Color with Alpha** | Color texture where the alpha channel carries meaningful data (transparency, mask) | RGBA |
| `_as` | **Ambient Shadow** | Ambient occlusion / shadow bake | Grayscale |
| `_mc` | **Macro** | Large-scale color variation visible at distance | RGB |
| `_li` | **Light / Emissive** | Self-illumination map (glowing parts) | RGB |
| `_no` | **Normal Map (Standard)** | Lower quality normal map variant | RGB |
| `_mca` | **Macro with Alpha** | Macro texture with alpha channel | RGBA |
| `_de` | **Detail** | Tiling detail texture for close-up surface variation | RGB |

### Konvence pojmenování v praxi

A jeden item typicky has více textures, all sharing a base name:

```
data/
  my_rifle_co.paa          <-- Base color (what you see)
  my_rifle_nohq.paa        <-- Normal map (surface bumps)
  my_rifle_smdi.paa         <-- Specular/metallic (shininess)
  my_rifle_as.paa           <-- Ambient shadow (baked AO)
  my_rifle_ca.paa           <-- Color with alpha (if transparency needed)
```

### The _smdi Channels

Textura specular/metallic/detail balí tři datové toky do jednoho RGB obrázku:

| Channel | Data | Range | Effect |
|---------|------|-------|--------|
| **R** | Metallic | 0-255 | 0 = non-metal, 255 = plný metal |
| **G** | Roughness (inverted specular) | 0-255 | 0 = rough/matte, 255 = smooth/glossy |
| **B** | Detail index / AO | 0-255 | Detail tiling or ambient occlusion |

### The _nohq Channels

Normálové mapy v DayZ používají tangent-space kódování:

| Channel | Data |
|---------|------|
| **R** | X-axis normal (left-right) |
| **G** | Y-axis normal (up-down) |
| **B** | Z-axis normal (toward viewer) |
| **A** | Specular power (volitelný, depends on material) |

---

## Požadavky na rozlišení

The Enfusion engine requires all textures to have **rozměry mocnin dvou**. Oba width and height must nezávisle be a mocnina 2, but they ne have to be equal (non-square textures jsou platné).

### Platné rozměry

| Size | Typical Use |
|------|-------------|
| **64x64** | Tiny icons, UI elements |
| **128x128** | Small icons, inventory thumbnails |
| **256x256** | UI panels, small item textures |
| **512x512** | Standard item textures, clothing |
| **1024x1024** | Weapons, detailed clothing, vehicle parts |
| **2048x2048** | High-detail weapons, character models |
| **4096x4096** | Terrain textures, large vehicle textures |

### Netvercové textury

Non-square mocnina dvou textures jsou platné:

```
256x512    -- Valid (both are powers of 2)
512x1024   -- Valid
1024x2048  -- Valid
300x512    -- INVALID (300 is not a power of 2)
```

### Doporučení pro rozlišení

- **Weapons:** 2048x2048 for the main body, 1024x1024 for attachments.
- **Clothing:** 1024x1024 or 2048x2048 depending on surface area coverage.
- **UI icons:** 128x128 or 256x256 for inventory icons, 64x64 for HUD elements.
- **Terrain:** 4096x4096 for satellite maps, 512x512 or 1024x1024 for material tiles.
- **Normal maps:** Same resolution as the corresponding color texture.
- **SMDI maps:** Same resolution as the corresponding color texture.

> **Varování:** Pokud texture has non-rozměry mocnin dvou, engine will either refuse to load it or display a magenta error texture. TexView2 will show a warning during conversion.

---

## Podpora alfa kanálu

Alfa kanál v textuře nese další data nad rámec barvy. Jak je interpretován, závisí na příponě textury a shaderu materiálu.

### Role alfa kanálu

| Suffix | Alpha Interpretation |
|--------|---------------------|
| `_co` | Usually unused; if present, may define transparency for simple materials |
| `_ca` | Transparency mask (0 = plnýy transparent, 255 = plnýy opaque) |
| `_nohq` | Specular power map (higher = sharper specular highlight) |
| `_smdi` | Usually unused |
| `_li` | Emissive intensity mask |

### Vytváření textur s alfou

Ve vašem editoru obrázků (Photoshop, GIMP, Krita):

1. Vytvořte the RGB content as normal.
2. Přidejte an alpha channel.
3. Paint white (255) where chcete plný opacity/effect, black (0) where chcete none.
4. Export as 32-bit TGA or PNG.
5. Convert to PAA using TexView2 -- it will detect the alpha channel automatickýally.

### Ověření alfy v TexView2

Otevřete the PAA in TexView2 and use the channel display buttons:

- **RGBA** -- Shows the final composite
- **RGB** -- Shows color pouze
- **A** -- Shows alpha channel pouze (white = opaque, black = transparent)

---

## Converting Mezi Formats

### TexView2 (primární nástroj)

**TexView2** je součástí DayZ Tools a je standardním nástrojem pro konverzi textur.

**Opening a file:**
1. Spusťte TexView2 from DayZ Tools or přímo from `DayZ Tools\Bin\TexView2\TexView2.exe`.
2. Otevřete your zdrojový soubor (TGA, PNG, or EDDS).
3. Ověřte the image looks correct and check dimensions.

**Converting to PAA:**
1. Otevřete the source texture in TexView2.
2. Go to **File --> Uložte As**.
3. Vyberte **PAA** as the output format.
4. Choose the compression type:
   - **DXT1** for opaque textures (no alpha needed)
   - **DXT5** for textures with alpha transparency
   - **ARGB4444** for small UI textures where velikost souboru matters
5. Klikněte **Save**.

**Batch conversion via command line:**

```bash
# Convert a single TGA to PAA
"P:\DayZ Tools\Bin\TexView2\TexView2.exe" -i "source.tga" -o "output.paa"

# TexView2 will auto-select compression based on alpha channel presence
```

### Binarize (automatizovaný)

When Binarize processes your mod's source directory, it automatickýally converts all recognized texture formats (TGA, PNG, EDDS) to PAA. This happens as part of the AddonBuilder pipeline.

**Binarize conversion flow:**
```
source/mod_name/data/texture_co.tga
    --> Binarize detects TGA
        --> Converts to PAA with automatic compression selection
            --> Output: build/mod_name/data/texture_co.paa
```

### Tabulka manuální konverze

| From | To | Tool | Notes |
|------|----|------|-------|
| TGA --> PAA | TexView2 | Standard workflow |
| PNG --> PAA | TexView2 | Works identicky to TGA |
| EDDS --> PAA | TexView2 or Binarize | Automatic during build |
| PAA --> TGA | TexView2 (Uložte As TGA) | For editing existing textures |
| PAA --> PNG | TexView2 (Uložte As PNG) | For extracting to portable format |
| PSD --> TGA/PNG | Photoshop/GIMP | Export from editor, then convert |

---

## Kvalita a komprese textur

### Výběr typu komprese

| Scenario | Recommended Compression | Reason |
|----------|------------------------|--------|
| Opaque diffuse (`_co`) | DXT1 | Best ratio, no alpha needed |
| Transparent diffuse (`_ca`) | DXT5 | Full alpha support |
| Normal maps (`_nohq`) | DXT5 | Alpha channel carries specular power |
| Specular maps (`_smdi`) | DXT1 | Usually opaque, RGB channels pouze |
| UI textures | ARGB4444 or DXT5 | Small size, clean edges |
| Emissive maps (`_li`) | DXT1 or DXT5 | DXT5 if alpha carries intensity |

### Kvalita vs. velikost souboru

```
Format        2048x2048 approx. size
-----------------------------------------
ARGB8888      16.0 MB    (uncompressed)
DXT5           5.3 MB    (4:1 compression)
DXT1           2.7 MB    (6:1 compression)
ARGB4444       8.0 MB    (2:1 compression)
```

### Nastavení kvality ve hře

Players can adjust texture quality in DayZ's video settings. Engine selects lower mip levels when quality is reduced, so your textures will look progressively blurrier at lower settings. This is automatický -- you ne need to create oddělený quality levels.

---

## Příklady z praxe

### Sada textur zbraně

Typický mod zbraní obsahuje tyto soubory textur:

```
MyMod_Weapons/data/weapons/m4a1/
  my_weapon_co.paa           <-- 2048x2048, DXT1, base color
  my_weapon_nohq.paa         <-- 2048x2048, DXT5, normal map
  my_weapon_smdi.paa          <-- 2048x2048, DXT1, specular/metallic
  my_weapon_as.paa            <-- 1024x1024, DXT1, ambient shadow
```

Soubor materiálu (`.rvmat`) odkazuje na tyto textury a přiřazuje je fázím shaderu.

### UI textura (zdroj imagesetu)

```
MyFramework/data/gui/icons/
  my_icons_co.paa           <-- 512x512, ARGB4444, sprite atlas
```

UI textures are často packed into a jeden atlas (imageset) and referenced by name in layout files. ARGB4444 compression is common for UI protože it preserves clean edges while keeping velikost souborus small.

### Textury terénu

```
terrain/
  grass_green_co.paa         <-- 1024x1024, DXT1, tiling color
  grass_green_nohq.paa       <-- 1024x1024, DXT5, tiling normal
  grass_green_smdi.paa        <-- 1024x1024, DXT1, tiling specular
  grass_green_mc.paa          <-- 512x512, DXT1, macro variation
  grass_green_de.paa          <-- 512x512, DXT1, detail tiling
```

Terrain textures tile across the landscape. The `_mc` macro texture adds large-scale color variation to prevent repetition.

---

## Časté chyby

### 1. Non-Power-of-Two Dimensions

**Symptom:** Magenta texture ve hře, TexView2 warnings.
**Fix:** Resize your source to the nearest mocnina 2 before converting.

### 2. Missing Suffix

**Symptom:** Material cannot find the texture, or it renders insprávně.
**Fix:** Vždy include the proper suffix (`_co`, `_nohq`, etc.) in souborname.

### 3. Wrong Compression for Alpha

**Symptom:** Transparency looks blocky or binary (on/off with no gradient).
**Fix:** Use DXT5 místo DXT1 for textures that need smooth alpha gradients.

### 4. Forgetting Mipmaps

**Symptom:** Texture looks fine up close but shimmers/sparkles at distance.
**Fix:** PAA files generated by TexView2 automatickýally include mipmaps. Pokud are using a non-standard přílišl, ensure mipmap generation is enabled.

### 5. Incorrect Normal Map Format

**Symptom:** Lighting on the model looks inverted or flat.
**Fix:** Zajistěte your normal map is in tangent-space format with DirectX-style Y-axis convention (green channel: up = lighter). Some přílišls export OpenGL-style (inverted Y) -- potřebujete to invert the green channel.

### 6. Path Mismatch Po Conversion

**Symptom:** Model or material shows magenta protože it references a `.tga` path but the PBO contains `.paa`.
**Fix:** Materials should reference the final `.paa` path. Binarize handles path remapping automatickýally, but if you pack with `-packonly` (no binarization), musíte ensure cestas match exactly.

---

## Osvědčené postupy

1. **Udržujte zdrojový soubors in version control.** Store TGA/PNG masters alongside your mod. The PAA files are generated output -- the sources are what matter.

2. **Match resolution to importance.** A rifle hráč stares at for hours deserves 2048x2048. A can of beans in the back of a shelf can use 512x512.

3. **Vždy provide a normal map.** Even a flat normal map (128, 128, 255 solid fill) is better than none -- chybějící normal maps cause material errors.

4. **Name konzistentně.** One base name, více suffixes: `myitem_co.paa`, `myitem_nohq.paa`, `myitem_smdi.paa`. Nikdy mix naming schemes.

5. **Preview in TexView2 before building.** Otevřete your PAA output and verify it looks correct. Zkontrolujte každý channel individually.

6. **Use DXT1 by výchozí, DXT5 pouze when alpha is needed.** DXT1 is half the velikost souboru of DXT5 and looks identical for opaque textures.

7. **Testujte at low quality settings.** What looks great at Ultra may be unreadable at Low protože engine drops mip levels aggressively.

---

## Pozorováno v reálných modech

| Vzor | Mod | Detail |
|---------|-----|--------|
| Atlas `_co` textures for icon grids | Colorful UI | Packs více UI icons into a jeden 512x512 `_co.paa` atlas referenced by imagesets |
| Market icon sprite sheets | Expansion Market | Uses large atlas PAA textures with dozens of item thumbnails for the trader UI |
| hiddenSelections retexture without nový P3D | DayZ-Samples (Test_ClothingRetexture) | Swaps `_co.paa` via `hiddenSelectionsTextures[]` to create color variants from one model |
| ARGB4444 for small HUD elements | VPP Admin Tools | Uses ARGB4444-compressed 64x64 PAA files for přílišlbar and panel icons to minimize velikost souboru |

---

## Kompatibilita a dopad

- **Více modů:** Texture path collisions are rare protože každý mod uses its own PBO prefix, but two mods retexturing the stejný vanilla item via `hiddenSelectionsTextures[]` will conflict -- last loaded wins.
- **Výkon:** A jeden 4096x4096 DXT5 texture uses ~21 MB of GPU memory with mipmaps. Overuse of large textures across mnoho mod items can exhaust VRAM on lower-end hardware. Preferujte 1024 or 2048 for většina items.
- **Verze:** The PAA format and TexView2 pipeline have been stable since DayZ 1.0. No breaking changes have occurred mezi DayZ versions.

---

## Navigace

| Previous | Up | Next |
|----------|----|------|
| [Part 3: GUI System](../03-gui-system/07-styles-fonts.md) | [Part 4: File Formats & DayZ Tools](../04-file-formats/01-textures.md) | [4.2 3D Models](02-models.md) |
