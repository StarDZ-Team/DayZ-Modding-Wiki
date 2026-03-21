# 3.1 Widget Types

DayZ's GUI system is built on widgets -- reusable UI components that range from simple containers to complex interactive controls. Every visible element on screen is a widget, and understanding the full catalog is essential for building mod UIs.

This chapter provides a complete reference of all widget types available in Enforce Script.

---

## How Widgets Work

Every widget in DayZ inherits from the `Widget` base class. Widgets are organized in a parent-child tree, where the root is typically a `WorkspaceWidget` obtained via `GetGame().GetWorkspace()`.

Each widget type has three associated identifiers:

| Identifikátor | Příklad | Použití |
|---|---|---|
| **Script class** | `TextWidget` | Code references, casting |
| **Layout class** | `TextWidgetClass` | `.layout` file declarations |
| **TypeID constant** | `TextWidgetTypeID` | Programmatic creation with `CreateWidget()` |

In `.layout` files you always use the layout class name (ending in `Class`). In scripts you work with the script class name.

---

## Container / Layout Widgets

Container widgets hold and organize child widgets. They do not display content themselves (except `PanelWidget`, which draws a colored rectangle).

| Skriptová třída | Layoutová třída | Účel |
|---|---|---|
| `Widget` | `WidgetClass` | Abstract base class for all widgets. Never instantiate directly. |
| `WorkspaceWidget` | `WorkspaceWidgetClass` | Root workspace. Obtained via `GetGame().GetWorkspace()`. Used to create widgets programmatically. |
| `FrameWidget` | `FrameWidgetClass` | General-purpose container. The most commonly used widget in DayZ. |
| `PanelWidget` | `PanelWidgetClass` | Solid colored rectangle. Use for backgrounds, dividers, separators. |
| `WrapSpacerWidget` | `WrapSpacerWidgetClass` | Flow layout. Arranges children sequentially with wrapping, padding, and margins. |
| `GridSpacerWidget` | `GridSpacerWidgetClass` | Grid layout. Arranges children in a grid defined by `Columns` and `Rows`. |
| `ScrollWidget` | `ScrollWidgetClass` | Scrollable viewport. Enables vertical/horizontal scrolling of child content. |
| `SpacerBaseWidget` | -- | Abstract base class for `WrapSpacerWidget` and `GridSpacerWidget`. |

### FrameWidget

The workhorse of DayZ UI. Use `FrameWidget` as your default container when you need to group widgets together. It has no visual appearance -- it is purely structural.

**Klíčové metody:**
- All base `Widget` methods (position, size, color, children, flags)

**Kdy použít:** Almost everywhere. Wrap groups of related widgets. Use as the root of dialogs, panels, and HUD elements.

```c
// Find a frame widget by name
FrameWidget panel = FrameWidget.Cast(root.FindAnyWidget("MyPanel"));
panel.Show(true);
```

### PanelWidget

A visible rectangle with a solid color. Unlike `FrameWidget`, a `PanelWidget` actually draws something on screen.

**Klíčové metody:**
- `SetColor(int argb)` -- Set the background color
- `SetAlpha(float alpha)` -- Set transparency

**Kdy použít:** Backgrounds behind text, colored dividers, overlay rectangles, tint layers.

```c
PanelWidget bg = PanelWidget.Cast(root.FindAnyWidget("Background"));
bg.SetColor(ARGB(200, 0, 0, 0));  // Semi-transparent black
```

### WrapSpacerWidget

Automatically arranges children in a flow layout. Children are placed one after another, wrapping to the next line when space runs out.

**Klíčové atributy layoutu:**
- `Padding` -- Inner padding (pixels)
- `Margin` -- Outer margin (pixels)
- `"Size To Content H" 1` -- Resize width to fit children
- `"Size To Content V" 1` -- Resize height to fit children
- `content_halign` -- Horizontal alignment of content (`left`, `center`, `right`)
- `content_valign` -- Vertical alignment of content (`top`, `center`, `bottom`)

**Kdy použít:** Dynamic lists, tag clouds, button rows, any layout where children have varying sizes.

### GridSpacerWidget

Arranges children in a fixed grid. Each cell has equal size.

**Klíčové atributy layoutu:**
- `Columns` -- Number of columns
- `Rows` -- Number of rows
- `Margin` -- Space between cells
- `"Size To Content V" 1` -- Resize height to fit content

**Kdy použít:** Inventory grids, icon galleries, settings panels with uniform rows.

### ScrollWidget

Provides a scrollable viewport for content that exceeds the visible area.

**Klíčové atributy layoutu:**
- `"Scrollbar V" 1` -- Enable vertical scrollbar
- `"Scrollbar H" 1` -- Enable horizontal scrollbar

**Klíčové metody:**
- `VScrollToPos(float pos)` -- Scroll to a vertical position
- `GetVScrollPos()` -- Get current vertical scroll position
- `GetContentHeight()` -- Get total content height
- `VScrollStep(int step)` -- Scroll by step amount

**Kdy použít:** Long lists, configuration panels, chat windows, log viewers.

---

## Display Widgets

Display widgets show content to the user but are not interactive.

| Skriptová třída | Layoutová třída | Účel |
|---|---|---|
| `TextWidget` | `TextWidgetClass` | Single-line text display |
| `MultilineTextWidget` | `MultilineTextWidgetClass` | Multi-line read-only text |
| `RichTextWidget` | `RichTextWidgetClass` | Text with embedded images (`<image>` tags) |
| `ImageWidget` | `ImageWidgetClass` | Image display (from imagesets or files) |
| `CanvasWidget` | `CanvasWidgetClass` | Programmable drawing surface |
| `VideoWidget` | `VideoWidgetClass` | Video file playback |
| `RTTextureWidget` | `RTTextureWidgetClass` | Render-to-texture surface |
| `RenderTargetWidget` | `RenderTargetWidgetClass` | 3D scene render target |
| `ItemPreviewWidget` | `ItemPreviewWidgetClass` | 3D DayZ item preview |
| `PlayerPreviewWidget` | `PlayerPreviewWidgetClass` | 3D player character preview |
| `MapWidget` | `MapWidgetClass` | Interactive world map |

### TextWidget

The most common display widget. Shows a single line of text.

**Klíčové metody:**
```c
TextWidget tw;
tw.SetText("Hello World");
tw.GetText();                           // Returns string
tw.GetTextSize(out int w, out int h);   // Pixel dimensions of rendered text
tw.SetTextExactSize(float size);        // Set font size in pixels
tw.SetOutline(int size, int color);     // Add text outline
tw.GetOutlineSize();                    // Returns int
tw.GetOutlineColor();                   // Returns int (ARGB)
tw.SetColor(int argb);                  // Text color
```

**Klíčové atributy layoutu:** `text`, `font`, `"text halign"`, `"text valign"`, `"exact text"`, `"exact text size"`, `"bold text"`, `"size to text h"`, `"size to text v"`, `wrap`.

### MultilineTextWidget

Displays multiple lines of read-only text. Text wraps automatically based on widget width.

**Kdy použít:** Description panels, help text, log displays.

### RichTextWidget

Supports inline images embedded within text using `<image>` tags. Also supports text wrapping.

**Klíčové atributy layoutu:**
- `wrap 1` -- Enable word wrapping

**Usage in text:**
```
"Health: <image set:dayz_gui image:iconHealth0 /> OK"
```

**Kdy použít:** Status text with icons, formatted messages, chat with inline images.

### ImageWidget

Displays images from imageset sprite sheets or loaded from file paths.

**Klíčové metody:**
```c
ImageWidget iw;
iw.SetImage(int index);                    // Switch between image0, image1, etc.
iw.LoadImageFile(int slot, string path);   // Load image from file
iw.LoadMaskTexture(string path);           // Load a mask texture
iw.SetMaskProgress(float progress);        // 0-1 for wipe/reveal transitions
```

**Klíčové atributy layoutu:**
- `image0 "set:dayz_gui image:icon_refresh"` -- Image from an imageset
- `mode blend` -- Blend mode (`blend`, `additive`, `stretch`)
- `"src alpha" 1` -- Use source alpha channel
- `stretch 1` -- Stretch image to fill widget
- `"flip u" 1` -- Flip horizontally
- `"flip v" 1` -- Flip vertically

**Kdy použít:** Icons, logos, backgrounds, map markers, status indicators.

### CanvasWidget

A drawing surface where you can render lines programmatically.

**Klíčové metody:**
```c
CanvasWidget cw;
cw.DrawLine(float x1, float y1, float x2, float y2, float width, int color);
cw.Clear();
```

**Kdy použít:** Custom graphs, connection lines between nodes, debug overlays.

### MapWidget

The full interactive world map. Supports panning, zooming, and coordinate conversion.

**Klíčové metody:**
```c
MapWidget mw;
mw.SetMapPos(vector pos);              // Center on world position
mw.GetMapPos();                        // Current center position
mw.SetScale(float scale);             // Zoom level
mw.GetScale();                        // Current zoom
mw.MapToScreen(vector world_pos);     // World coords to screen coords
mw.ScreenToMap(vector screen_pos);    // Screen coords to world coords
```

**Kdy použít:** Mission maps, GPS systems, location pickers.

### ItemPreviewWidget

Renders a 3D preview of any DayZ inventory item.

**Kdy použít:** Inventory screens, loot previews, shop interfaces.

### PlayerPreviewWidget

Renders a 3D preview of the player character model.

**Kdy použít:** Character creation screens, equipment preview, wardrobe systems.

### RTTextureWidget

Renders its children to a texture surface rather than directly to the screen.

**Kdy použít:** Minimap rendering, picture-in-picture effects, offscreen UI composition.

---

## Interactive Widgets

Interactive widgets respond to user input and fire events.

| Skriptová třída | Layoutová třída | Účel |
|---|---|---|
| `ButtonWidget` | `ButtonWidgetClass` | Clickable button |
| `CheckBoxWidget` | `CheckBoxWidgetClass` | Booleovský checkbox |
| `EditBoxWidget` | `EditBoxWidgetClass` | Single-line text input |
| `MultilineEditBoxWidget` | `MultilineEditBoxWidgetClass` | Multi-line text input |
| `PasswordEditBoxWidget` | `PasswordEditBoxWidgetClass` | Masked password input |
| `SliderWidget` | `SliderWidgetClass` | Horizontal slider control |
| `XComboBoxWidget` | `XComboBoxWidgetClass` | Dropdown selection |
| `TextListboxWidget` | `TextListboxWidgetClass` | Selectable row list |
| `ProgressBarWidget` | `ProgressBarWidgetClass` | Progress indicator |
| `SimpleProgressBarWidget` | `SimpleProgressBarWidgetClass` | Minimal progress indicator |

### ButtonWidget

The primary interactive control. Supports both momentary click and toggle modes.

**Klíčové metody:**
```c
ButtonWidget bw;
bw.SetText("Click Me");
bw.GetState();              // Returns bool (toggle buttons only)
bw.SetState(bool state);    // Set toggle state
```

**Klíčové atributy layoutu:**
- `text "Label"` -- Button label text
- `switch toggle` -- Make it a toggle button
- `style Default` -- Visual style

**Vyvolávané události:** `OnClick(Widget w, int x, int y, int button)`

### CheckBoxWidget

A boolean toggle control.

**Klíčové metody:**
```c
CheckBoxWidget cb;
cb.IsChecked();                 // Returns bool
cb.SetChecked(bool checked);    // Set state
```

**Vyvolávané události:** `OnChange(Widget w, int x, int y, bool finished)`

### EditBoxWidget

A single-line text input field.

**Klíčové metody:**
```c
EditBoxWidget eb;
eb.GetText();               // Returns string
eb.SetText("default");      // Set text content
```

**Vyvolávané události:** `OnChange(Widget w, int x, int y, bool finished)` -- `finished` is `true` when Enter is pressed.

### SliderWidget

A horizontal slider for numeric values.

**Klíčové metody:**
```c
SliderWidget sw;
sw.GetCurrent();            // Returns float (0-1)
sw.SetCurrent(float val);   // Set position
```

**Klíčové atributy layoutu:**
- `"fill in" 1` -- Show filled track behind handle
- `"listen to input" 1` -- Respond to mouse input

**Vyvolávané události:** `OnChange(Widget w, int x, int y, bool finished)` -- `finished` is `true` when the user releases the slider.

### XComboBoxWidget

A dropdown selection list.

**Klíčové metody:**
```c
XComboBoxWidget xcb;
xcb.AddItem("Option A");
xcb.AddItem("Option B");
xcb.SetCurrentItem(0);         // Select by index
xcb.GetCurrentItem();          // Returns selected index
xcb.ClearAll();                // Remove all items
```

### TextListboxWidget

A scrollable list of text rows. Supports selection and multi-column data.

**Klíčové metody:**
```c
TextListboxWidget tlb;
tlb.AddItem("Row text", null, 0);   // text, userData, column
tlb.GetSelectedRow();               // Returns int (-1 if none)
tlb.SetRow(int row);                // Select a row
tlb.RemoveRow(int row);
tlb.ClearItems();
```

**Vyvolávané události:** `OnItemSelected`

### ProgressBarWidget

Displays a progress indicator.

**Klíčové metody:**
```c
ProgressBarWidget pb;
pb.SetCurrent(float value);    // 0-100
```

**Kdy použít:** Loading bars, health bars, mission progress, cooldown indicators.

---

## Complete TypeID Reference

Use these constants with `GetGame().GetWorkspace().CreateWidget()` for programmatic widget creation:

```
FrameWidgetTypeID
TextWidgetTypeID
MultilineTextWidgetTypeID
MultilineEditBoxWidgetTypeID
RichTextWidgetTypeID
RenderTargetWidgetTypeID
ImageWidgetTypeID
VideoWidgetTypeID
RTTextureWidgetTypeID
ButtonWidgetTypeID
CheckBoxWidgetTypeID
SimpleProgressBarWidgetTypeID
ProgressBarWidgetTypeID
SliderWidgetTypeID
TextListboxWidgetTypeID
EditBoxWidgetTypeID
PasswordEditBoxWidgetTypeID
WorkspaceWidgetTypeID
GridSpacerWidgetTypeID
WrapSpacerWidgetTypeID
ScrollWidgetTypeID
```

---

## Choosing the Right Widget

| Potřebuji... | Použít tento widget |
|---|---|
| Group widgets together (invisible) | `FrameWidget` |
| Draw a colored rectangle | `PanelWidget` |
| Show text | `TextWidget` |
| Show multi-line text | `MultilineTextWidget` or `RichTextWidget` with `wrap 1` |
| Show text with inline icons | `RichTextWidget` |
| Display an image/icon | `ImageWidget` |
| Create a clickable button | `ButtonWidget` |
| Create a toggle (on/off) | `CheckBoxWidget` or `ButtonWidget` with `switch toggle` |
| Accept text input | `EditBoxWidget` |
| Accept multi-line text input | `MultilineEditBoxWidget` |
| Accept a password | `PasswordEditBoxWidget` |
| Let user pick a number | `SliderWidget` |
| Let user pick from a list | `XComboBoxWidget` (dropdown) or `TextListboxWidget` (visible list) |
| Show progress | `ProgressBarWidget` or `SimpleProgressBarWidget` |
| Arrange children in a flow | `WrapSpacerWidget` |
| Arrange children in a grid | `GridSpacerWidget` |
| Make content scrollable | `ScrollWidget` |
| Show a 3D item model | `ItemPreviewWidget` |
| Show the player model | `PlayerPreviewWidget` |
| Show the world map | `MapWidget` |
| Draw custom lines/shapes | `CanvasWidget` |
| Render to a texture | `RTTextureWidget` |

---

## Next Steps

- [3.2 Layout File Format](02-layout-files.md) -- Learn how to define widget trees in `.layout` files
- [3.5 Programmatic Widget Creation](05-programmatic-widgets.md) -- Create widgets from code instead of layout files
