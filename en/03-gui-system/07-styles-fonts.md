# Styles, Fonts & Images


---

This chapter covers the visual building blocks of DayZ UI: predefined styles, font usage, text sizing, image widgets with imageset references, and how to create custom imagesets for your mod.

---

## Styles

Styles are predefined visual appearances that can be applied to widgets via the `style` attribute in layout files. They control background rendering, borders, and overall look without requiring manual color and image configuration.

### Common Built-In Styles

| Style Name | Description |
|---|---|
| `blank` | No visual -- completely transparent background |
| `Empty` | No background rendering |
| `Default` | Default button/widget style with standard DayZ appearance |
| `Colorable` | Style that can be tinted using `SetColor()` |
| `rover_sim_colorable` | Colored panel style, commonly used for backgrounds |
| `rover_sim_black` | Dark panel background |
| `rover_sim_black_2` | Darker panel variant |
| `OutlineFilled` | Outline with a filled interior |
| `DayZDefaultPanelRight` | DayZ default right panel style |
| `DayZNormal` | DayZ normal text/widget style |
| `MenuDefault` | Standard menu button style |

### Using Styles in Layouts

```
ButtonWidgetClass MyButton {
 style Default
 text "Click Me"
 size 120 30
 hexactsize 1
 vexactsize 1
}

PanelWidgetClass Background {
 style rover_sim_colorable
 color 0.2 0.3 0.5 0.9
 size 1 1
}
```

### Style + Color Pattern

The `Colorable` and `rover_sim_colorable` styles are designed to be tinted. Set the `color` attribute in the layout or call `SetColor()` in code:

```
PanelWidgetClass TitleBar {
 style rover_sim_colorable
 color 0.4196 0.6471 1 0.9412
 size 1 30
 hexactsize 0
 vexactsize 1
}
```

```c
// Change color at runtime
Widget bar = Widget.Cast(root.FindAnyWidget("TitleBar"));
bar.SetColor(ARGB(240, 107, 165, 255));
```

### Styling a Dialog Container

A common pattern is to combine `OutlineFilled` with a wrap spacer so the dialog frame draws a bordered, filled background and sizes itself to its contents. `OutlineFilled` is one of the styles the vanilla `WrapSpacerWidget` style block defines (`gui/looknfeel/dayzwidgets.styles`), alongside `Colorable`, `dashed`, and `Outline`:

```
WrapSpacerWidgetClass LNT_ConfirmDialog {
 style OutlineFilled
 Padding 5
 "Size To Content V" 1

 {
 TextWidgetClass DialogText {
  text "Are you sure?"
  "text halign" center
 }

 ButtonWidgetClass ConfirmButton {
  style Default
  text "OK"
  size 120 30
  hexactsize 1
  vexactsize 1
 }
 }
}
```

Client theming mods use `rover_sim_colorable` extensively for themed panels, with the tint color controlled from a centralized theme class (see [Color Theme Pattern](#color-theme-pattern) below).

---

## Fonts

DayZ includes several built-in fonts. Font paths are specified in the `font` attribute.

### Built-In Font Paths

| Font Path | Description |
|---|---|
| `"gui/fonts/Metron"` | Standard UI font |
| `"gui/fonts/Metron28"` | Standard font, 28pt variant |
| `"gui/fonts/Metron-Bold"` | Bold variant |
| `"gui/fonts/Metron-Bold58"` | Bold 58pt variant |
| `"gui/fonts/sdf_MetronBook24"` | SDF (Signed Distance Field) font -- crisp at any size |

### Using Fonts in Layouts

```
TextWidgetClass Title {
 text "Mission Briefing"
 font "gui/fonts/Metron-Bold"
 "text halign" center
 "text valign" center
}

TextWidgetClass Body {
 text "Objective: Secure the airfield"
 font "gui/fonts/Metron"
}
```

### Using Fonts in Code

```c
TextWidget tw = TextWidget.Cast(root.FindAnyWidget("MyText"));
tw.SetText("Hello");
// Font is set in the layout, not changeable at runtime via script
```

### SDF Fonts

SDF (Signed Distance Field) fonts render crisply at any zoom level, making them ideal for UI elements that may appear at various sizes. The `sdf_MetronBook24` font is the best choice for text that needs to look sharp across different UI scale settings.

---

## Text Sizing: "exact text" vs. Proportional

DayZ text widgets support two sizing modes, controlled by the `"exact text"` attribute:

### Proportional Text (Default)

When `"exact text" 0` (the default), the font size is determined by the widget's height. The text scales with the widget. This is the default behavior.

```
TextWidgetClass ScalingText {
 size 1 0.05
 hexactsize 0
 vexactsize 0
 text "I scale with my parent"
}
```

### Exact Text Size

When `"exact text" 1`, the font size is a fixed pixel value set by `"exact text size"`:

```
TextWidgetClass FixedText {
 size 1 30
 hexactsize 0
 vexactsize 1
 text "I am always 16 pixels"
 "exact text" 1
 "exact text size" 16
}
```

### Which to Use?

| Scenario | Recommendation |
|---|---|
| HUD elements that scale with screen size | Proportional (default) |
| Menu text at a specific size | `"exact text" 1` with `"exact text size"` |
| Text that must match a specific font pixel size | `"exact text" 1` |
| Text inside spacers/grids | Often proportional, determined by cell height |

### Text-Related Size Attributes

| Attribute | Effect |
|---|---|
| `"size to text h" 1` | Widget width adjusts to fit the text |
| `"size to text v" 1` | Widget height adjusts to fit the text |
| `"text sharpness"` | Float value controlling rendering sharpness |
| `wrap 1` | Enable word wrapping for text that exceeds widget width |

The `"size to text"` attributes are useful for labels and tags where the widget should be exactly as large as its text content.

---

## Text Alignment

Control where text appears within its widget using alignment attributes:

```
TextWidgetClass CenteredLabel {
 text "Centered"
 "text halign" center
 "text valign" center
}
```

| Attribute | Values | Effect |
|---|---|---|
| `"text halign"` | `left`, `center`, `right` | Horizontal text position within widget |
| `"text valign"` | `top`, `center`, `bottom` | Vertical text position within widget |

---

## Text Outline

Add outlines to text for readability on busy backgrounds:

```c
TextWidget tw;
tw.SetOutline(1, ARGB(255, 0, 0, 0));   // 1px black outline

int size = tw.GetOutlineSize();           // Read outline size
int color = tw.GetOutlineColor();         // Read outline color (ARGB)
```

---

## ImageWidget

`ImageWidget` displays images from two sources: imageset references and dynamically loaded files.

### Imageset References

An imageset names rectangular regions and can reference one or more atlas texture resources.

In a layout file:

```
ImageWidgetClass MyIcon {
 image0 "set:dayz_gui image:icon_refresh"
 mode blend
 "src alpha" 1
 stretch 1
}
```

The format is `"set:<imageset_name> image:<image_name>"`. Both names come from the imageset's internal `Name` fields, not necessarily from filenames.

Common vanilla imagesets and images:

```
"set:dayz_gui image:icon_pin"           -- Map pin icon
"set:dayz_gui image:icon_refresh"       -- Refresh icon
"set:dayz_gui image:icon_x"            -- Close/X icon
"set:dayz_gui image:icon_engine_alert" -- Warning/alert icon
"set:dayz_gui image:iconHealth0"       -- Health/plus icon
"set:dayz_gui image:DayZLogo"          -- DayZ logo
"set:dayz_gui image:Expand"            -- Expand arrow
"set:dayz_gui image:Gradient"          -- Gradient strip
```

### Multiple Image Slots

A single `ImageWidget` can hold multiple images in different slots (`image0`, `image1`, etc.) and switch between them:

```
ImageWidgetClass StatusIcon {
 image0 "set:dayz_gui image:icon_engine_alert"
 image1 "set:dayz_gui image:iconHealth0"
}
```

```c
ImageWidget icon;
icon.SetImage(0);    // Show image0 (missing icon)
icon.SetImage(1);    // Show image1 (health icon)
```

### Loading Images from Files

Load images dynamically at runtime:

```c
ImageWidget img;
img.LoadImageFile(0, "MyMod/gui/textures/my_image.edds");
img.SetImage(0);
```

The path is relative to the mod's root directory. Supported formats include `.edds`, `.paa`, and `.tga` (though `.edds` is standard for DayZ).

### Image Blend Modes

The `mode` attribute controls how the image blends with what's behind it:

| Mode | Effect |
|---|---|
| `blend` | Standard alpha blending (most common) |
| `additive` | Colors add together (glow effects) |
| `opaque` | Opaque, ignores alpha entirely |

### Image Mask Transitions

`ImageWidget` supports mask-based reveal transitions:

```c
ImageWidget img;
img.LoadMaskTexture("gui/textures/mask_wipe.edds");
img.SetMaskProgress(0.5);  // 50% revealed
```

This is useful for loading bars, health displays, and reveal animations.

---

## ImageSet Format

An imageset file (`.imageset`) defines named regions within a sprite atlas texture. Use the native format shown below for DayZ GUI resources.

### DayZ Native Format

Extracted vanilla DayZ and the reviewed public mod resources use this brace-delimited format. Native support for an XML imageset schema is not established by this review.

```
ImageSetClass {
 Name "my_mod_icons"
 RefSize 1024 1024
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "<YOUR-COMPLETE-RESOURCE-REFERENCE>"
  }
 }
 Images {
  ImageSetDefClass icon_sword {
   Name "icon_sword"
   Pos 0 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass icon_shield {
   Name "icon_shield"
   Pos 64 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass icon_potion {
   Name "icon_potion"
   Pos 128 0
   Size 64 64
   Flags 0
  }
 }
 Groups {
 }
}
```

Key fields:
- `Name` -- Imageset name (used in `"set:<name>"`)
- `RefSize` -- Coordinate reference size for `Pos` and `Size`; it need not match every physical texture resource. For example, extracted `dayz_gui` uses `RefSize 1024 1024` with 1024×1024 and 2048×2048 resources.
- `path` -- Complete resource reference and virtual path to the texture resource. Replace the entire quoted placeholder value above with the reference recorded for your own resource.
- `mpix` -- Extracted files use values `0`, `1`, `2`, and `3`; `dayz_gui` pairs `0`/`1` with base/`@2x` resources, while `playstation_buttons` pairs `1`/`2`. The loader's selection, fallback, and quality behavior are not established here, so copy a matching shipped shape and validate the intended scale.
- Each image entry defines `Name`, `Pos` (x y in pixels), `Size` (width height in pixels), and `Flags` (for example, `0` or `ISVerticalTile` as on the vanilla `Gradient` image).


---

## Creating Custom Imagesets

To create your own imageset for a mod:

### Step 1: Create the Sprite Atlas Texture

Prepare an atlas and record the coordinate system you intend to use for its named rectangles. This review did not validate an EDDS creation, import, or conversion workflow; preserve the resource and virtual path named by your imageset when you package it.

### Step 2: Create the Imageset File

Create a `.imageset` file that maps named regions to positions in the texture:

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
  ImageSetDefClass icon_mission {
   Name "icon_mission"
   Pos 0 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass icon_waypoint {
   Name "icon_waypoint"
   Pos 64 0
   Size 64 64
   Flags 0
  }
 }
 Groups {
 }
}
```

Place this teaching fixture at `MyMod/GUI/imagesets/mymod_icons.imageset`. `<YOUR-COMPLETE-RESOURCE-REFERENCE>` is the entire quoted `path` value, not a prefix; replace it and the coordinates with values recorded for your own resource.

### Step 3: Register in config.cpp

To register a packaged mod's custom imageset through `CfgMods`, list its virtual `.imageset` path under `defs > imageSets > files[]`:

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
                files[] = { "MyMod/GUI/imagesets/mymod_icons.imageset" };
            };
            // ... script modules ...
        };
    };
};
```

### Step 4: Use in Layouts and Code

In layout files:

```
ImageWidgetClass MissionIcon {
 image0 "set:mymod_icons image:icon_mission"
 mode blend
 "src alpha" 1
}
```

In client-side UI code, after the widget exists:

```c
ImageWidget icon = ImageWidget.Cast(layoutRoot.FindAnyWidget("MissionIcon"));
if (icon && icon.LoadImageFile(0, "set:mymod_icons image:icon_mission"))
{
    icon.SetImage(0);
}
```

Reviewed Expansion and Editor sources register sets and consume their internal names without a repository call to `LoadWidgetImageSet`; this does not establish global scope or loader timing. This template has not been compiled, packed, or rendered in a DayZ client.

---

## Color Theme Pattern

Professional mods centralize their color definitions in a theme class, then apply colors at runtime. This makes it easy to restyle the entire UI by changing one file.

```c
class UIColor
{
    static int White()        { return ARGB(255, 255, 255, 255); }
    static int Black()        { return ARGB(255, 0, 0, 0); }
    static int Primary()      { return ARGB(255, 75, 119, 190); }
    static int Secondary()    { return ARGB(255, 60, 60, 60); }
    static int Accent()       { return ARGB(255, 100, 200, 100); }
    static int Danger()       { return ARGB(255, 200, 50, 50); }
    static int Transparent()  { return ARGB(0, 0, 0, 0); }
    static int SemiBlack()    { return ARGB(180, 0, 0, 0); }
}
```

Apply in code:

```c
titleBar.SetColor(UIColor.Primary());
statusText.SetColor(UIColor.Accent());
errorText.SetColor(UIColor.Danger());
```

This is a pattern used by client theming mods; the version above is this wiki's example implementation. It means changing the entire UI color scheme requires editing only the theme class.

---

## Summary of Visual Attributes by Widget Type

| Widget | Key Visual Attributes |
|---|---|
| Any widget | `color`, `visible`, `style`, `priority`, `inheritalpha` |
| TextWidget | `text`, `font`, `"text halign"`, `"text valign"`, `"exact text"`, `"exact text size"`, `"bold text"`, `wrap` |
| ImageWidget | `image0`, `mode`, `"src alpha"`, `stretch`, `"flip u"`, `"flip v"` |
| ButtonWidget | `text`, `style`, `switch once` |
| PanelWidget | `color`, `style` |
| SliderWidget | `"fill in"` |
| ProgressBarWidget | `style` |

---

## Best Practices

1. **Use internal names consistently** in `set:` and `image:` references.

2. **Use SDF fonts** (`sdf_MetronBook24`) for text that needs to look sharp at any scale.

3. **Use `"exact text" 1`** for UI text at specific pixel sizes; use proportional text for HUD elements that should scale.

4. **Centralize colors** in a theme class rather than hardcoding ARGB values throughout your code.

5. **Set `"src alpha" 1`** on image widgets to get proper transparency.

6. **Use the `CfgMods` registration shape** above when registering a packaged custom imageset through `CfgMods`.

7. **Validate your intended UI scale** after packaging; the reviewed sources do not establish general size or memory recommendations.

---

## Next Steps

- [3.8 Dialogs & Modals](08-dialogs-modals.md) -- Popup windows, confirmation prompts, and overlay panels
- [3.1 Widget Types](01-widget-types.md) -- Review the full widget catalog
- [3.6 Event Handling](06-event-handling.md) -- Make your styled widgets interactive

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| SDF fonts scale to any size | `sdf_MetronBook24` is crisp at all sizes | True for sizes above ~10px. Below that, SDF fonts can appear blurry compared to bitmap fonts at their native size |
| `"exact text" 1` gives pixel-perfect sizing | Font renders at the exact pixel size specified | DayZ applies internal scaling, so `"exact text size" 16` may render slightly differently across resolutions. Test on 1080p and 1440p |
| Built-in styles cover all needs | `Default`, `blank`, `Colorable` are sufficient | Most professional mods define their own `.styles` files because built-in styles have limited visual variety |
| Imageset resource format | Extracted vanilla `.imageset` files use brace-delimited `ImageSetClass` syntax | Use this format for DayZ imagesets. XML loader support and any parsing-speed difference are unverified. |
| `SetColor()` overrides layout color | Runtime color replaces the layout value | `SetColor()` tints the widget's existing visual. On styled widgets, the tint multiplies with the style's base color, producing unexpected results |

---

## Compatibility & Impact

- **Multi-Mod:** Style names are global. If two mods register a `.styles` file defining the same style name, the last-loaded mod wins. Prefix custom style names with your mod identifier (e.g., `MyMod_PanelDark`).
- **Imageset limits:** The reviewed sources do not establish startup timing, GPU residency, collision order, or general atlas-size limits. Validate those characteristics in the target client build.
