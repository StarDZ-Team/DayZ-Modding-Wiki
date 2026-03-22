# Chapitre 3.1: Widget Types

[Accueil](../../README.md) | **Widget Types** | [Suivant : Layout Files >>](02-layout-files.md)

---

DayZ's GUI system is built on widgets -- reusable UI components that range from simple containers to complex interactive controls. Every visible element on screen is a widget, and understanding the full catalog is essential for building mod UIs.

Ce chapitre fournit a complete reference of all widget types available in Enforce Script.

---

## Fonctionnement des widgets

Every widget in DayZ inherits from the `Widget` base class. Widgets are organized in a parent-child tree, where the root is typically a `WorkspaceWidget` obtained via `GetGame().GetWorkspace()`.

Each widget type has three associated identifiers:

| Identifiant | Exemple | Utilisé pour |
|---|---|---|
| **Script class** | `TextWidget` | Code references, casting |
| **Layout class** | `TextWidgetClass` | `.layout` file declarations |
| **TypeID constant** | `TextWidgetTypeID` | Programmatic creation with `CreateWidget()` |

In `.layout` files you always use the layout class name (ending in `Class`). In scripts you work with the script class name.

---

## Widgets conteneur / layout

Container widgets hold and organize child widgets. They do not display content themselves (except `PanelWidget`, which draws a colored rectangle).

| Classe script | Classe layout | Objectif |
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

**Méthodes principales :**
- All base `Widget` methods (position, size, color, children, flags)

**Quand utiliser :** Almost everywhere. Wrap groups of related widgets. Use as the root of dialogs, panels, and HUD elements.

```c
// Find a frame widget by name
FrameWidget panel = FrameWidget.Cast(root.FindAnyWidget("MyPanel"));
panel.Show(true);
```

### PanelWidget

A visible rectangle with a solid color. Unlike `FrameWidget`, a `PanelWidget` actually draws something on screen.

**Méthodes principales :**
- `SetColor(int argb)` -- Set the background color
- `SetAlpha(float alpha)` -- Set transparency

**Quand utiliser :** Backgrounds behind text, colored dividers, overlay rectangles, tint layers.

```c
PanelWidget bg = PanelWidget.Cast(root.FindAnyWidget("Background"));
bg.SetColor(ARGB(200, 0, 0, 0));  // Semi-transparent black
```

### WrapSpacerWidget

Automatically arranges children in a flow layout. Children are placed one after another, wrapping to the next line when space runs out.

**Attributs de layout principaux :**
- `Padding` -- Inner padding (pixels)
- `Margin` -- Outer margin (pixels)
- `"Size To Content H" 1` -- Resize width to fit children
- `"Size To Content V" 1` -- Resize height to fit children
- `content_halign` -- Horizontal alignment of content (`left`, `center`, `right`)
- `content_valign` -- Vertical alignment of content (`top`, `center`, `bottom`)

**Quand utiliser :** Dynamic lists, tag clouds, button rows, any layout where children have varying sizes.

### GridSpacerWidget

Arranges children in a fixed grid. Each cell has equal size.

**Attributs de layout principaux :**
- `Columns` -- Number of columns
- `Rows` -- Number of rows
- `Margin` -- Space between cells
- `"Size To Content V" 1` -- Resize height to fit content

**Quand utiliser :** Inventory grids, icon galleries, settings panels with uniform rows.

### ScrollWidget

Provides a scrollable viewport for content that exceeds the visible area.

**Attributs de layout principaux :**
- `"Scrollbar V" 1` -- Enable vertical scrollbar
- `"Scrollbar H" 1` -- Enable horizontal scrollbar

**Méthodes principales :**
- `VScrollToPos(float pos)` -- Scroll to a vertical position
- `GetVScrollPos()` -- Get current vertical scroll position
- `GetContentHeight()` -- Get total content height
- `VScrollStep(int step)` -- Scroll by step amount

**Quand utiliser :** Long lists, configuration panels, chat windows, log viewers.

---

## Widgets d'affichage

Display widgets show content to the user but are not interactive.

| Classe script | Classe layout | Objectif |
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

**Méthodes principales :**
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

**Attributs de layout principaux :** `text`, `font`, `"text halign"`, `"text valign"`, `"exact text"`, `"exact text size"`, `"bold text"`, `"size to text h"`, `"size to text v"`, `wrap`.

### MultilineTextWidget

Displays multiple lines of read-only text. Text wraps automatically based on widget width.

**Quand utiliser :** Description panels, help text, log displays.

### RichTextWidget

Supports inline images embedded within text using `<image>` tags. Also supports text wrapping.

**Attributs de layout principaux :**
- `wrap 1` -- Enable word wrapping

**Usage in text:**
```
"Health: <image set:dayz_gui image:iconHealth0 /> OK"
```

**Quand utiliser :** Status text with icons, formatted messages, chat with inline images.

### ImageWidget

Displays images from imageset sprite sheets or loaded from file paths.

**Méthodes principales :**
```c
ImageWidget iw;
iw.SetImage(int index);                    // Switch between image0, image1, etc.
iw.LoadImageFile(int slot, string path);   // Load image from file
iw.LoadMaskTexture(string path);           // Load a mask texture
iw.SetMaskProgress(float progress);        // 0-1 for wipe/reveal transitions
```

**Attributs de layout principaux :**
- `image0 "set:dayz_gui image:icon_refresh"` -- Image from an imageset
- `mode blend` -- Blend mode (`blend`, `additive`, `stretch`)
- `"src alpha" 1` -- Use source alpha channel
- `stretch 1` -- Stretch image to fill widget
- `"flip u" 1` -- Flip horizontally
- `"flip v" 1` -- Flip vertically

**Quand utiliser :** Icons, logos, backgrounds, map markers, status indicators.

### CanvasWidget

A drawing surface where you can render lines programmatically.

**Méthodes principales :**
```c
CanvasWidget cw;
cw.DrawLine(float x1, float y1, float x2, float y2, float width, int color);
cw.Clear();
```

**Quand utiliser :** Custom graphs, connection lines between nodes, debug overlays.

### MapWidget

The full interactive world map. Supports panning, zooming, and coordinate conversion.

**Méthodes principales :**
```c
MapWidget mw;
mw.SetMapPos(vector pos);              // Center on world position
mw.GetMapPos();                        // Current center position
mw.SetScale(float scale);             // Zoom level
mw.GetScale();                        // Current zoom
mw.MapToScreen(vector world_pos);     // World coords to screen coords
mw.ScreenToMap(vector screen_pos);    // Screen coords to world coords
```

**Quand utiliser :** Mission maps, GPS systems, location pickers.

### ItemPreviewWidget

Renders a 3D preview of any DayZ inventory item.

**Quand utiliser :** Inventory screens, loot previews, shop interfaces.

### PlayerPreviewWidget

Renders a 3D preview of le joueur character model.

**Quand utiliser :** Character creation screens, equipment preview, wardrobe systems.

### RTTextureWidget

Renders its children to a texture surface rather than directly to the screen.

**Quand utiliser :** Minimap rendering, picture-in-picture effects, offscreen UI composition.

---

## Widgets interactifs

Interactive widgets respond to user input and fire events.

| Classe script | Classe layout | Objectif |
|---|---|---|
| `ButtonWidget` | `ButtonWidgetClass` | Clickable button |
| `CheckBoxWidget` | `CheckBoxWidgetClass` | Boolean checkbox |
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

**Méthodes principales :**
```c
ButtonWidget bw;
bw.SetText("Click Me");
bw.GetState();              // Returns bool (toggle buttons only)
bw.SetState(bool state);    // Set toggle state
```

**Attributs de layout principaux :**
- `text "Label"` -- Button label text
- `switch toggle` -- Make it a toggle button
- `style Default` -- Visual style

**Événements déclenchés :** `OnClick(Widget w, int x, int y, int button)`

### CheckBoxWidget

A boolean toggle control.

**Méthodes principales :**
```c
CheckBoxWidget cb;
cb.IsChecked();                 // Returns bool
cb.SetChecked(bool checked);    // Set state
```

**Événements déclenchés :** `OnChange(Widget w, int x, int y, bool finished)`

### EditBoxWidget

A single-line text input field.

**Méthodes principales :**
```c
EditBoxWidget eb;
eb.GetText();               // Returns string
eb.SetText("default");      // Set text content
```

**Événements déclenchés :** `OnChange(Widget w, int x, int y, bool finished)` -- `finished` is `true` when Enter is pressed.

### SliderWidget

A horizontal slider for numeric values.

**Méthodes principales :**
```c
SliderWidget sw;
sw.GetCurrent();            // Returns float (0-1)
sw.SetCurrent(float val);   // Set position
```

**Attributs de layout principaux :**
- `"fill in" 1` -- Show filled track behind handle
- `"listen to input" 1` -- Respond to mouse input

**Événements déclenchés :** `OnChange(Widget w, int x, int y, bool finished)` -- `finished` is `true` when the user releases the slider.

### XComboBoxWidget

A dropdown selection list.

**Méthodes principales :**
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

**Méthodes principales :**
```c
TextListboxWidget tlb;
tlb.AddItem("Row text", null, 0);   // text, userData, column
tlb.GetSelectedRow();               // Returns int (-1 if none)
tlb.SetRow(int row);                // Select a row
tlb.RemoveRow(int row);
tlb.ClearItems();
```

**Événements déclenchés :** `OnItemSelected`

### ProgressBarWidget

Displays a progress indicator.

**Méthodes principales :**
```c
ProgressBarWidget pb;
pb.SetCurrent(float value);    // 0-100
```

**Quand utiliser :** Loading bars, health bars, mission progress, cooldown indicators.

---

## Référence complète des TypeID

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

## Choisir le bon widget

| J'ai besoin de... | Utiliser ce widget |
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
| Show le joueur model | `PlayerPreviewWidget` |
| Show le monde map | `MapWidget` |
| Draw custom lines/shapes | `CanvasWidget` |
| Render to a texture | `RTTextureWidget` |

---

## Prochaines étapes

- [3.2 Layout File Format](02-layout-files.md) -- Learn how to define widget trees in `.layout` files
- [3.5 Programmatic Widget Creation](05-programmatic-widgets.md) -- Create widgets from code instead of layout files

---

## Bonnes pratiques

- Use `FrameWidget` as your default container. Only use `PanelWidget` when you need a visible colored background.
- Prefer `RichTextWidget` over `TextWidget` when you might need inline icons later -- switching types in an existing layout is tedious.
- Always null-check after `FindAnyWidget()` and `Cast()`. Missing widget names silently return `null` and cause crashes on the next method call.
- Use `WrapSpacerWidget` for dynamic lists and `GridSpacerWidget` for fixed grids. Do not manually position children in a flow layout.
- Avoid `CanvasWidget` for production UI -- it redraws every frame and has no batching. Use it only for debug overlays.

---

## Théorie vs Pratique

| Concept | Théorie | Réalité |
|---------|--------|---------|
| `ScrollWidget` auto-scrolls to content | Scrollbar appears when content exceeds bounds | You must call `VScrollToPos()` manually to scroll to new content; the widget does not auto-scroll on child addition |
| `SliderWidget` fires continuous events | `OnChange` fires on every pixel of drag | `finished` parameter is `false` during drag and `true` on release; update heavy logic only when `finished == true` |
| `XComboBoxWidget` supports many items | Dropdown works with any count | Performance degrades noticeably with 100+ items; use `TextListboxWidget` for long lists instead |
| `ItemPreviewWidget` shows any item | Pass any classname for 3D preview | The widget requires the item's `.p3d` model to be loaded; modded items need their Data PBO present |
| `MapWidget` is a simple display | Just shows the map | It intercepts all mouse input by default; you must manage `IGNOREPOINTER` flags carefully or it blocks clicks on overlapping widgets |

---

## Compatibilité et impact

- **Multi-Mod :** Widget type IDs are engine constants shared across all mods. Two mods creating widgets with the same name under the same parent will collide. Use unique widget names with your mod prefix.
- **Performance :** `TextListboxWidget` and `ScrollWidget` with hundreds of children cause frame drops. Pool and recycle widgets for lists exceeding 50 items.
