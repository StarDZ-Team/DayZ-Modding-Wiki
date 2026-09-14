# ImageSet Format


---

> **Summary:** ImageSets define named rectangular regions in an atlas coordinate space. Reviewed DayZ GUI resources use them from layouts and `ImageWidget.LoadImageFile()` through internal set and image names.

---

## Table of Contents

- [Overview](#overview)
- [How ImageSets Work](#how-imagesets-work)
- [DayZ Native ImageSet Format](#dayz-native-imageset-format)
- [Registering ImageSets in config.cpp](#registering-imagesets-in-config-cpp)
- [Referencing Images in Layouts](#referencing-images-in-layouts)
- [Referencing Images in Scripts](#referencing-images-in-scripts)
- [Image Flags](#image-flags)
- [Multi-Resolution Textures](#multi-resolution-textures)
- [Creating Custom Icon Sets](#creating-custom-icon-sets)
- [Icon Font Atlas Pattern](#icon-font-atlas-pattern)
- [Worked Examples](#worked-examples)
- [Common Mistakes](#common-mistakes)

---

## Overview

A texture atlas contains smaller icons arranged in a grid or freeform layout. An imageset maps human-readable names to rectangular regions and can reference one or more atlas texture resources.

For example, a 1024x1024 texture might contain 64 icons at 64x64 pixels each. The imageset file says "the icon named `arrow_down` is at position (128, 64) and is 64x64 pixels." Your layout files and scripts reference `arrow_down` by name, and the engine extracts the correct sub-rectangle from the atlas at render time.

The reviewed source excerpts establish the resource syntax and named-region mapping, not general GPU, draw-call, or memory behavior.

---

## How ImageSets Work

The data flow:

1. **Texture atlas resources** (`.edds` in the reviewed imagesets) --- one or more resources containing the named regions
2. **ImageSet definition** (`.imageset` file) --- maps names to regions in the atlas
3. **Optional `CfgMods` registration** --- a supported way to list a packaged mod's custom imageset
4. **Layout/script reference** --- uses `set:name image:iconName` syntax to render a specific icon

The pinned [DayZ Expansion configuration](https://github.com/salutesh/DayZ-Expansion-Scripts/blob/6dacd00f6d943ebbd99e0cf1baad93f470d96419/DayZExpansion/Core/Scripts/config.cpp#L40-L54) registers imagesets, and its [layout](https://github.com/salutesh/DayZ-Expansion-Scripts/blob/6dacd00f6d943ebbd99e0cf1baad93f470d96419/DayZExpansion/GUI/layouts/expansion_loading.layout#L44-L76) consumes internal names without a repository call to `LoadWidgetImageSet`. That observation does not establish scope, timing, or failure behavior.

---

## DayZ Native ImageSet Format

Extracted vanilla DayZ and the reviewed public mod resources use the native brace-delimited format below. Native support for the XML schema formerly shown on this page is not established.

### Structure

```
ImageSetClass {
 Name "my_icons"
 RefSize 1024 1024
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "<YOUR-COMPLETE-RESOURCE-REFERENCE>"
  }
 }
 Images {
  ImageSetDefClass icon_name {
   Name "icon_name"
   Pos 0 0
   Size 64 64
   Flags 0
  }
 }
 Groups {
 }
}
```

This is an observed brace-format shape. The intended definition placement is `MyMod/GUI/imagesets/my_icons.imageset`; `<YOUR-COMPLETE-RESOURCE-REFERENCE>` replaces the entire quoted `path` value. `Groups {}` is consistently observed in the reviewed brace resources, not proven required grammar.

### Top-Level Fields

| Field | Description |
|-------|-------------|
| `Name` | The set name. Used in the `set:` part of image references. |
| `RefSize` | Coordinate reference dimensions for `Pos` and `Size`. It need not equal every physical texture resource. |
| `Textures` | Contains one or more observed `ImageSetTextureClass` entries. |

### Texture Entry Fields

| Field | Description |
|-------|-------------|
| `mpix` | Extracted sets use values `0`, `1`, `2`, and `3`; their selection and fallback semantics are not documented by the sources reviewed here. See [Multi-Resolution Textures](#multi-resolution-textures) for observed pairings. |
| `path` | Complete resource reference and virtual path. Reviewed extracted/pinned files use GUID-prefixed virtual paths, while StarDZ beta sets also contain plain paths; this review does not establish whether either spelling is mandatory or interchangeable. Preserve the reference and virtual path recorded for your own resource. |

### Image Entry Fields

Each image is an `ImageSetDefClass` inside the `Images` block:

| Field | Description |
|-------|-------------|
| Class name | Reviewed examples use the same class name and `Name` value. |
| `Name` | The image identifier. Used in the `image:` part of references. |
| `Pos` | Top-left corner position in the atlas (x y), in pixels |
| `Size` | Dimensions (width height), in pixels |
| `Flags` | Tiling behavior flags (see [Image Flags](#image-flags)) |

### Full Example (DayZ Vanilla)

```
ImageSetClass {
 Name "dayz_gui"
 RefSize 1024 1024
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "{534691EE0479871C}Gui/imagesets/dayz_gui.edds"
  }
  ImageSetTextureClass {
   mpix 1
   path "{C139E49FD0ECAF9E}Gui/imagesets/dayz_gui@2x.edds"
  }
 }
 Images {
  ImageSetDefClass Gradient {
   Name "Gradient"
   Pos 0 317
   Size 75 5
   Flags ISVerticalTile
  }
  ImageSetDefClass Expand {
   Name "Expand"
   Pos 121 257
   Size 20 20
   Flags 0
  }
 }
 Groups {
 }
}
```

---

## Registering ImageSets in config.cpp

To register a packaged mod's custom imageset through `CfgMods`, list its virtual `.imageset` path under `CfgMods > defs > imageSets > files[]`. This is a supported registration mechanism, not a complete native loader contract: `LoadWidgetImageSet(string filename)` also exists, but its accepted grammar and runtime behavior are not documented by the declaration.

### Syntax

```cpp
class CfgMods
{
    class MyMod
    {
        // ... other fields ...
        class defs
        {
            class imageSets
            {
                files[] =
                {
                    "MyMod/GUI/imagesets/my_icons.imageset",
                    "MyMod/GUI/imagesets/my_other_icons.imageset"
                };
            };
        };
    };
};
```

### Example: A Framework With Several Sets

A framework can split its graphics across a few purpose-built sets --- one for standalone HUD icons, one for reusable UI primitives, and one for its icon-font atlas. The constructed Lantern framework used throughout this wiki registers three:

```cpp
class defs
{
    class imageSets
    {
        files[] =
        {
            "Lantern_Core/GUI/imagesets/lnt_icons.imageset",
            "Lantern_Core/GUI/imagesets/lnt_hud.imageset",
            "Lantern_Core/GUI/imagesets/lnt_prefabs.imageset"
        };
    };
};
```

### Example: A Single-Atlas Mod

A single-atlas configuration uses one entry:

```cpp
class defs
{
    class imageSets
    {
        files[] =
        {
            "NightPatrol/GUI/imagesets/np_weapon_icons.imageset"
        };
    };
};
```

---

## Referencing Images in Layouts

In `.layout` files, use the `image0` property with the `set:name image:imageName` syntax:

```
ImageWidgetClass MyIcon {
 size 32 32
 hexactsize 1
 vexactsize 1
 image0 "set:dayz_gui image:icon_refresh"
}
```

### Syntax Breakdown

```
set:SETNAME image:IMAGENAME
```

- `SETNAME` --- the `Name` field from the imageset definition (e.g., `dayz_gui`, `lnt_icons`, `lnt_solid`)
- `IMAGENAME` --- the `Name` field from a specific `ImageSetDefClass` entry (e.g., `icon_refresh`, `arrow_down`)

### Multiple Image States

Some widgets support multiple image states (normal, hover, pressed):

```
ImageWidgetClass icon {
 image0 "set:solid image:circle"
}

ButtonWidgetClass btn {
 image0 "set:dayz_gui image:icon_expand"
}
```

### Example References

```
image0 "set:lnt_regular image:arrow_down_short_wide"  -- icon-font regular set (custom atlas)
image0 "set:dayz_gui image:icon_minus"                -- vanilla DayZ icon
image0 "set:dayz_gui image:icon_collapse"             -- vanilla DayZ icon
image0 "set:dayz_gui image:circle"                    -- vanilla DayZ shape
image0 "set:lnt_icons image:icon_settings"            -- custom mod icon
```

---

## Referencing Images in Scripts

In Enforce Script, use `ImageWidget.LoadImageFile()` or set image properties on widgets:

### LoadImageFile

```c
ImageWidget icon = ImageWidget.Cast(layoutRoot.FindAnyWidget("MyIcon"));
icon.LoadImageFile(0, "set:solid image:circle");
```

The `0` parameter is the image index (corresponding to `image0` in layouts).

### Multiple States via Index

```c
ImageWidget collapseIcon;
collapseIcon.LoadImageFile(0, "set:regular image:square_plus");    // Normal state
collapseIcon.LoadImageFile(1, "set:solid image:square_minus");     // Toggled state
```

Switch between states using `SetImage(index)`:

```c
if (isExpanded)
{
    collapseIcon.SetImage(1);
}
else
{
    collapseIcon.SetImage(0);
}
```

### Using String Variables

```c
string icon = "set:lnt_icons image:icon_search";
searchBarIcon.LoadImageFile(0, icon);

// Later, change dynamically
searchBarIcon.LoadImageFile(0, "set:dayz_gui image:icon_x");
```

---

## Image Flags

The `Flags` field in native-format imageset entries controls tiling behavior when the image is stretched beyond its natural size.

| Flag | Value | Description |
|------|-------|-------------|
| `0` | 0 | No tiling. The image stretches to fill the widget. |
| `ISHorizontalTile` | 1 | Tiles horizontally when the widget is wider than the image. |
| `ISVerticalTile` | 2 | Tiles vertically when the widget is taller than the image. |
| Both | 3 | Tiles in both directions (`ISHorizontalTile` + `ISVerticalTile`). |

The field accepts either the symbolic name or the number: `dayz_gui.imageset` uses `Flags 0`, `Flags ISHorizontalTile`, `Flags ISVerticalTile` and the bare `Flags 3` (both) in the same file. The individual bit values are inferred from that combined `3`, not from published documentation --- if you need a specific tiling result, check it visually.

### Usage

```
ImageSetDefClass Gradient {
 Name "Gradient"
 Pos 0 317
 Size 75 5
 Flags ISVerticalTile
}
```

This `Gradient` image is 75x5 pixels. When used in a widget taller than 5 pixels, it tiles vertically to fill the height, creating a repeating gradient stripe.

Most icons use `Flags 0` (no tiling). Tiling flags are primarily for UI elements like borders, dividers, and repeating patterns.

---

## Multi-Resolution Textures

Extracted native imagesets can contain multiple texture entries. The sources reviewed here show their values and file pairings, but do not define selection, ordering, fallback, DPI, or quality-setting behavior.

```
Textures {
 ImageSetTextureClass {
  mpix 0
  path "Gui/imagesets/dayz_gui.edds"
 }
 ImageSetTextureClass {
  mpix 1
  path "Gui/imagesets/dayz_gui@2x.edds"
 }
}
```

The vanilla sets in `gui/imagesets/` use four different values, and the observed base/`@2x` pairings are not identical from set to set:

| Imageset | `mpix` values present | Notes |
|----------|----------------------|-------|
| `dayz_gui` | `0`, `1` | `0` = base `.edds`, `1` = `@2x` |
| `dayz_additional_gui` | `0`, `1` | same pairing as above |
| `playstation_buttons` | `1`, `2` | `1` = base, `2` = `@2x` --- a different pair of numbers for the same idea |
| `xbox_buttons` | `1`, `2` | same as above |
| `bleedingdrops`, `map2d_ui` | `0` | single texture |
| `console_toolbar`, `dayz_inventory` | `1` | single texture |
| `ccgui_enforce`, `dayz_crosshairs`, `rover_imageset` | `3` | single texture |

Use the pairing in a matching shipped resource only as a starting point, and validate the intended scale in your target client. These observations do not establish a general rule for single-texture values or an `@2x` naming requirement.

---

## Creating Custom Icon Sets

### Teaching Template

Place a custom definition at `MyMod/GUI/imagesets/mymod_icons.imageset`, preserve the `.edds` resource and virtual path it names, and map your own named regions in its coordinate reference space. The fixture below is a teaching template only: its resource-reference marker and coordinates must be replaced, and it has not been compiled, packed, or rendered in a DayZ client.

```
ImageSetClass {
 Name "mymod_icons"
 RefSize 512 512
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "<YOUR-COMPLETE-RESOURCE-REFERENCE>"
  }
 }
 Images {
  ImageSetDefClass settings {
   Name "settings"
   Pos 0 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass player {
   Name "player"
   Pos 64 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass map_marker {
   Name "map_marker"
   Pos 128 0
   Size 64 64
   Flags 0
  }
 }
 Groups {
 }
}
```

`<YOUR-COMPLETE-RESOURCE-REFERENCE>` is deliberately non-literal and replaces the entire quoted `path` value. Use the complete reference recorded for your own resource; do not reuse a sample GUID.

### Register the Teaching Template

To register this packaged custom imageset through `CfgMods`, use its virtual `.imageset` path:

```cpp
class CfgMods
{
    class MyMod
    {
        class defs
        {
            class imageSets
            {
                files[] = { "MyMod/GUI/imagesets/mymod_icons.imageset" };
            };
        };
    };
};
```

### Use in a Client Layout and Script

```
ImageWidgetClass SettingsIcon {
 image0 "set:mymod_icons image:settings"
 size 32 32
 hexactsize 1
 vexactsize 1
}
```

After the client-side widget exists, check the documented `LoadImageFile` return value before selecting the slot:

```c
ImageWidget settingsIcon = ImageWidget.Cast(layoutRoot.FindAnyWidget("SettingsIcon"));
if (settingsIcon && settingsIcon.LoadImageFile(0, "set:mymod_icons image:settings"))
{
    settingsIcon.SetImage(0);
}
```

Reviewed Expansion and Editor repositories use registered-set references without a repository call to `LoadWidgetImageSet`. That does not prove scope, startup timing, resource residency, or failure behavior.

---

## Icon Font Atlas Pattern

An icon-font atlas pattern uses atlas resources derived from an **icon font** (a font whose glyphs are pictograms rather than letters). It can provide a consistent library of named icons, subject to the font's license and an independently validated asset pipeline.

### How It Works

1. Each glyph in the icon font is rendered to a texture atlas at a fixed grid size (e.g. 64x64 per icon)
2. Each font weight gets its own imageset: for example `lnt_solid`, `lnt_regular`, `lnt_light`, `lnt_brands`
3. Icon names in the imageset match the font's glyph names (e.g. `circle`, `arrow_down`, `gear`), so the same name resolves across every weight
4. A mod can list the imagesets through the bounded `CfgMods` registration mechanism described above

### Per-Weight Icon Sets

```
Lantern_Core/GUI/icons/
  lnt_solid.imageset       -- Filled icons
  lnt_regular.imageset     -- Outlined icons
  lnt_light.imageset       -- Light-weight outlined icons
  lnt_brands.imageset      -- Logo glyphs
```

### Usage in Layouts

```
image0 "set:lnt_solid image:circle"
image0 "set:lnt_solid image:gear"
image0 "set:lnt_regular image:arrow_down_short_wide"
```

### Usage in Scripts

Because the glyph name is identical across weights, swapping states is just a set-name change:

```c
collapseIcon.LoadImageFile(1, "set:lnt_solid image:square_minus");
collapseIcon.LoadImageFile(0, "set:lnt_regular image:square_plus");
```

### Why This Pattern Works Well

- **Large icon library**: Hundreds of icons available without any artwork creation
- **Consistent style**: All icons share the same visual weight and construction
- **Multiple weights**: Choose solid, regular, or light for different visual contexts
- **Name parity**: The same glyph name resolves across every weight, so switching states is a one-word change

### Licensing Note

Icon fonts carry their own licenses. Before you render one to a texture atlas and ship it inside a PBO, check the font's license and honor its terms --- some require attribution, some restrict redistribution, and some are free for any use. For example, Font Awesome Free is distributed under **CC BY 4.0**, which permits redistribution as long as you credit the source. Treat the atlas you generate as a redistribution of the original artwork.

### The Atlas Structure

A per-weight set is simply a large atlas with icons arranged at a fixed interval. For example, a solid-weight set with icons on a 64-pixel grid:

```
ImageSetClass {
 Name "lnt_solid"
 RefSize 1024 1024
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "<YOUR-COMPLETE-RESOURCE-REFERENCE>"
  }
 }
 Images {
  ImageSetDefClass circle {
   Name "circle"
   Pos 0 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass gear {
   Name "gear"
   Pos 64 0
   Size 64 64
   Flags 0
  }
 }
 Groups {
 }
}
```

---

## Worked Examples

> The examples below use the wiki's constructed teaching mods (Lantern, NightPatrol). They are illustrations, not dumps of any shipped mod. Each resource-reference marker is deliberately non-literal and replaces the entire quoted `path` value; each coordinate is illustrative. Replace them with values recorded for your own resource. None of these fixtures has been compiled, packed, or rendered in a DayZ client.

### Freeform Admin Atlas

A large full-screen atlas that packs admin-panel icons wherever they fit --- freeform positioning rather than a strict grid --- to maximize texture space. Note the varied positions and a non-power-of-two `RefSize` matched to a 1920x1080 canvas:

```
ImageSetClass {
 Name "lnt_admin_icons"
 RefSize 1920 1080
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "<YOUR-COMPLETE-RESOURCE-REFERENCE>"
  }
 }
 Images {
  ImageSetDefClass icon_cloud {
   Name "icon_cloud"
   Pos 1206 108
   Size 62 62
   Flags 0
  }
  ImageSetDefClass icon_players {
   Name "icon_players"
   Pos 391 112
   Size 62 62
   Flags 0
  }
 }
 Groups {
 }
}
```

Referenced in layouts as:
```
image0 "set:lnt_admin_icons image:icon_cloud"
```

### Weapon Inventory Icons (Varied Sizes)

A content mod's weapon and attachment icons packed into a large atlas. Inventory icons are much larger than UI icons because they show detail in the inventory grid --- this set mixes 300x300 entries, while a HUD set would typically use 64x64:

```
ImageSetClass {
 Name "np_weapon_icons"
 RefSize 2048 2048
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "<YOUR-COMPLETE-RESOURCE-REFERENCE>"
  }
 }
 Images {
  ImageSetDefClass np_foregrip {
   Name "np_foregrip"
   Pos 123 19
   Size 300 300
   Flags 0
  }
  ImageSetDefClass np_optic_scope {
   Name "np_optic_scope"
   Pos 426 20
   Size 300 300
   Flags 0
  }
 }
 Groups {
 }
}
```

This shows that icons do not need to be uniform size --- inventory icons use 300x300 while UI icons typically use 64x64.

### UI Primitives (Spaces in Names)

UI primitives --- rounded corners and single-pixel alpha swatches used to tint panels --- packed into a small 256x256 atlas:

```
ImageSetClass {
 Name "lnt_prefabs"
 RefSize 256 256
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "<YOUR-COMPLETE-RESOURCE-REFERENCE>"
  }
 }
 Images {
  ImageSetDefClass Round_Outline_TopLeft {
   Name "Round_Outline_TopLeft"
   Pos 24 21
   Size 8 8
   Flags 0
  }
  ImageSetDefClass "Alpha 10" {
   Name "Alpha 10"
   Pos 0 15
   Size 1 1
   Flags 0
  }
 }
 Groups {
 }
}
```

Notable: image names can contain spaces when quoted (e.g. `"Alpha 10"`). However, referencing these in layouts requires the exact name including the space.

---

## Common Mistakes

### Forgetting config.cpp Registration

When your fixture uses `CfgMods` registration, confirm that its virtual `.imageset` path appears under `defs > imageSets > files[]` and then test the packaged client result. The reviewed sources do not establish a universal failure mode when that entry is absent.

### Wrong Texture Path

Preserve the complete resource reference and virtual path recorded for the `.edds` resource named by your imageset. The reviewed data does not establish that GUID-prefixed and plain spelling are interchangeable.

### Mismatched RefSize

`RefSize` defines the coordinate reference space for `Pos` and `Size`; it need not equal every physical texture variant. Extracted `dayz_gui` keeps `RefSize 1024 1024` while its two referenced resources are 1024×1024 and 2048×2048. Validate your own coordinates at the intended scale.

### Pos Coordinates Off by One

`Pos` is the top-left corner of the icon region. If your icons are at 64-pixel intervals but you accidentally offset by 1 pixel, icons will have a thin slice of the adjacent icon visible.

### Assuming a Conversion Recipe

Reviewed imagesets reference `.edds`, but this review did not validate a Workbench, Mikero, or other conversion/import procedure. Do not assume that a generic DDS export, renamed file, or untested conversion is a usable DayZ EDDS resource.

### Spaces in Image Names

If you use a name with spaces, keep the exact internal `Name` in the reference and validate it in the intended layout or script context.

---

## Best Practices

- Use a clear, mod-specific internal set name and keep `set:`/`image:` references aligned with the resource's internal `Name` fields.
- Preserve the `.edds` resource and complete virtual path named by the imageset when packaging your mod.
- Include the observed `Groups {}` block in a brace-format fixture, without treating its presence as a proven grammar requirement.
- Treat the teaching templates as starting points: substitute the resource reference and coordinates, then compile, pack, and render-test them before shipping.

---

## Theory vs Practice

> What the documentation says versus how things actually work at runtime.

| Concept | Theory | Reality |
|---------|--------|---------|
| `CfgMods` registration | A packaged custom imageset can be listed in `defs > imageSets > files[]` | This is a supported registration mechanism, not the only native loader route or a documented failure contract. |
| `RefSize` maps coordinates | Coordinates are in `RefSize` space | It is a coordinate reference size and need not equal every physical texture variant. |
| Multiple `mpix` entries | Extracted sets contain several values and pairings | The reviewed sources do not define selection, fallback, DPI, or quality-setting behavior. |

---

## Compatibility & Impact

- **Runtime limits:** The reviewed sources do not establish collision order, silent-failure behavior, global scope, startup timing, GPU residency, or general performance characteristics. Test those properties in the target client build.
- **Version evidence:** The native `ImageSetClass` resource shape and `set:name image:name` syntax are present in the extracted DayZ GUI files and the reviewed pinned public mod sources. This page makes no claim about when the format was introduced.

---

## Patterns Seen in Practice

| Pattern | Detail |
|---------|--------|
| Icon-font atlases | An icon font is rendered to large per-weight atlases (see the [Icon Font Atlas Pattern](#icon-font-atlas-pattern) above), providing hundreds of consistent icons via sets like `set:lnt_solid`, `set:lnt_regular` |
| Freeform atlas layout | Icons arranged non-uniformly on a full-screen atlas with varying sizes, maximizing texture-space usage |
| Per-feature small atlases | Each sub-module can have its own imageset rather than one large shared teaching example |
| 300x300 inventory icons | Large icon sizes for weapon/attachment inventory slots where detail matters, unlike 64x64 UI icons |
