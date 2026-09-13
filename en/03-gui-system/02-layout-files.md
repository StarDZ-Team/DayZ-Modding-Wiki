# Layout File Format (.layout)


---

DayZ uses a custom text-based format for UI layout files. These `.layout` files are **NOT XML** -- they use a brace-delimited format similar to config.cpp. The DayZ Workbench editor generates them, but understanding the format lets you hand-edit layouts and debug problems.

---

## Basic Structure

A `.layout` file defines a tree of widgets. Every file has exactly one root widget, which contains nested children.

```
WidgetTypeClass WidgetName {
 attribute value
 attribute "quoted value"
 {
  ChildWidgetTypeClass ChildName {
   attribute value
  }
 }
}
```

Key rules:

1. The root element is always a single widget (typically `FrameWidgetClass`).
2. Widget type names use the **layout class** name, which always ends with `Class` (e.g., `FrameWidgetClass`, `TextWidgetClass`, `ButtonWidgetClass`).
3. Each widget has a unique name following its type class.
4. Attributes are `key value` pairs, one per line.
5. Attribute names containing spaces must be quoted: `"text halign" center`.
6. String values are quoted: `text "Hello World"`.
7. Numeric values are unquoted: `size 0.5 0.3`.
8. Children are nested inside `{ }` blocks after the parent's attributes.

---

## Attribute Reference

### Positioning & Sizing

| Attribute | Values | Description |
|---|---|---|
| `position` | `x y` | Widget position (proportional 0-1 or pixel values) |
| `size` | `w h` | Widget dimensions (proportional 0-1 or pixel values) |
| `halign` | `left`, `center_ref`, `right_ref` | Horizontal alignment reference point |
| `valign` | `top`, `center_ref`, `bottom_ref` | Vertical alignment reference point |
| `hexactpos` | `0` or `1` | 0 = proportional X position, 1 = pixel X position |
| `vexactpos` | `0` or `1` | 0 = proportional Y position, 1 = pixel Y position |
| `hexactsize` | `0` or `1` | 0 = proportional width, 1 = pixel width |
| `vexactsize` | `0` or `1` | 0 = proportional height, 1 = pixel height |
| `fixaspect` | `none`, `fixwidth`, `inside`, `outside` | Keep the widget's aspect ratio (see [fixaspect Values](#fixaspect-values)) |
| `scaled` | `0` or `1` | Scale with DayZ UI scaling setting |
| `priority` | integer | Z-order (higher values render on top) |

The `hexactpos`, `vexactpos`, `hexactsize`, and `vexactsize` flags are the most important attributes in the entire layout system. They control whether each dimension uses proportional (0.0 - 1.0 relative to parent) or pixel (absolute screen pixels) units. See [3.3 Sizing & Positioning](03-sizing-positioning.md) for a thorough explanation.

### Visual Attributes

| Attribute | Values | Description |
|---|---|---|
| `visible` | `0` or `1` | Initial visibility (0 = hidden) |
| `color` | `r g b a` | Color as four floats, each 0.0 to 1.0 |
| `style` | style name | Predefined visual style (e.g., `Default`, `Colorable`) |
| `draggable` | `0` or `1` | Widget can be dragged by the user |
| `clipchildren` | `0` or `1` | Clip child widgets to this widget's bounds |
| `inheritalpha` | `0` or `1` | Children inherit this widget's alpha value |
| `keepsafezone` | `0` or `1` | Keep widget within screen safe zone |

### Behavioral Attributes

| Attribute | Values | Description |
|---|---|---|
| `ignorepointer` | `0` or `1` | Widget ignores mouse input (clicks pass through) |
| `disabled` | `0` or `1` | Widget is disabled |
| `"no focus"` | `0` or `1` | Widget cannot receive keyboard focus |

### Text Attributes

These apply to `TextWidgetClass`, `RichTextWidgetClass`, `MultilineTextWidgetClass`, `ButtonWidgetClass`, and other text-bearing widgets.

| Attribute | Values | Description |
|---|---|---|
| `text` | `"string"` | Default text content |
| `font` | `"path/to/font"` | Font file path |
| `"text halign"` | `left`, `center`, `right` | Horizontal text alignment within the widget |
| `"text valign"` | `top`, `center`, `bottom` | Vertical text alignment within the widget |
| `"bold text"` | `0` or `1` | Bold rendering |
| `"italic text"` | `0` or `1` | Italic rendering |
| `"exact text"` | `0` or `1` | Use exact pixel font size instead of proportional |
| `"exact text size"` | integer | Font size in pixels (requires `"exact text" 1`) |
| `"size to text h"` | `0` or `1` | Resize widget width to fit text |
| `"size to text v"` | `0` or `1` | Resize widget height to fit text |
| `"text sharpness"` | float | Text rendering sharpness |
| `wrap` | `0` or `1` | Enable word wrapping |

### Image Attributes

These apply to `ImageWidgetClass`.

| Attribute | Values | Description |
|---|---|---|
| `image0` | `"set:name image:name"` | Primary image from an imageset |
| `mode` | `blend`, `additive`, `opaque` | Image blend mode |
| `"src alpha"` | `0` or `1` | Use the source alpha channel |
| `stretch` | `0` or `1` | Stretch image to fill widget |
| `filter` | `0` or `1` | Enable texture filtering |
| `"flip u"` | `0` or `1` | Flip image horizontally |
| `"flip v"` | `0` or `1` | Flip image vertically |
| `"clamp mode"` | `clamp`, `wrap`, `border` | Texture edge behavior |
| `"stretch mode"` | `none`, `stretch_w_h`, `fit_w_center` | Stretch mode |

### Spacer Attributes

These apply to `WrapSpacerWidgetClass` and `GridSpacerWidgetClass`.

| Attribute | Values | Description |
|---|---|---|
| `Padding` | integer | Inner padding in pixels |
| `Margin` | integer | Space between child items in pixels |
| `"Size To Content H"` | `0` or `1` | Resize width to match children |
| `"Size To Content V"` | `0` or `1` | Resize height to match children |
| `content_halign` | `left`, `center`, `right` | Child content horizontal alignment |
| `content_valign` | `top`, `center`, `bottom` | Child content vertical alignment |
| `Columns` | integer | Grid columns (GridSpacer only) |
| `Rows` | integer | Grid rows (GridSpacer only) |

### Button Attributes

| Attribute | Values | Description |
|---|---|---|
| `switch` | `normal`, `once` | Both values occur in vanilla layouts; manage persistent on/off state explicitly with `CheckBoxWidget`, `IsChecked()` and `SetChecked()` |
| `style` | style name | Visual style for the button |

### fixaspect Values

The values below are used in shipped layouts. Copy a matching vanilla pattern and test resizing; this list is not an exhaustive declaration of every native parser value.

The `fixaspect` attribute keeps a widget's aspect ratio constant when the screen aspect ratio or the parent size would otherwise distort it. The value is a **keyword**, not a number:

| Value | Behavior |
|-------|----------|
| `none` | No aspect ratio constraint (default) |
| `fixwidth` | Width stays as authored; **height** is recalculated to keep the aspect ratio |
| `inside` | Widget fits entirely inside its authored rectangle while keeping the ratio (letterbox) |
| `outside` | Widget fills its authored rectangle while keeping the ratio (content may extend past the edges) |

By far the most common use is `fixaspect fixwidth` on an `ImageWidgetClass` with a square proportional size -- without it, an icon that is square at 16:9 becomes stretched at 21:9. Vanilla HUD icon layouts include this pattern; inspect the specific image you are adapting. `inside` is the vanilla choice for radial menus (a square menu letterboxed into any screen), and `outside` for full-screen background art that must cover the whole frame.

See [Sizing & Positioning](03-sizing-positioning.md#the-fixaspect-attribute) for how `fixaspect` interacts with the four exact-size flags.

### Slider Attributes

| Attribute | Values | Description |
|---|---|---|
| `"fill in"` | `0` or `1` | Fill the slider track with color up to the thumb position |
| `"listen to input"` | `0` or `1` | Whether the slider responds to input |

In script, configure the slider range and value:

```c
SliderWidget slider;
slider.SetMinMax(0, 100);
slider.SetCurrent(50);
float val = slider.GetCurrent();
```

### Scroll Attributes

| Attribute | Values | Description |
|---|---|---|
| `"Scrollbar V"` | `0` or `1` | Show vertical scrollbar |
| `"Scrollbar H"` | `0` or `1` | Show horizontal scrollbar |

---

## Script Integration

### The `scriptclass` Attribute

The `scriptclass` attribute binds a widget to an Enforce Script class by name. When the layout is loaded, the engine creates one instance of that class per widget and calls its `OnWidgetScriptInit(Widget w)` method after the widget tree exists.

```
FrameWidgetClass MyPanel {
 size 1 1
 scriptclass "MyPanelHandler"
}
```

Inherit from `ScriptedWidgetEventHandler` and call `SetHandler(this)` inside `OnWidgetScriptInit` -- that is the vanilla pattern (for example, `ScrollBarContainer` initializes its root handler this way). `SetHandler` routes the widget's UI events (`OnClick`, `OnMouseEnter`, `OnChildAdd`, ...) to the same object, so one class both configures the widget and reacts to it:

```c
class MyPanelHandler : ScriptedWidgetEventHandler
{
    protected Widget m_Root;

    void OnWidgetScriptInit(Widget w)
    {
        m_Root = w;
        m_Root.SetHandler(this);
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        return false;
    }
}
```

Technically any script class works as a `scriptclass` (`OnWidgetScriptInit` is found by name), but without `ScriptedWidgetEventHandler` and `SetHandler` you get no event callbacks.

### The ScriptParamsClass Block

A layout can pass per-widget parameters to its `scriptclass` through a `ScriptParamsClass` block. The block lives in its own `{ }` brace block; when the widget also has children, the params block is a **second** brace block after the children block.

```
ImageWidgetClass AlertIcon {
 size 32 32
 hexactsize 1
 vexactsize 1
 image0 "set:lnt_icons image:alert"
 scriptclass "LNT_FadeIn"
 {
  ScriptParamsClass {
   Start_Alpha 0.25
   Log_Label "AlertIcon"
  }
 }
}
```

On the script side, each parameter maps to a member variable declared with the **`reference`** keyword. The engine fills these members **before** calling `OnWidgetScriptInit`, matching by name -- `Start_Alpha 0.25` in the layout fills `reference float Start_Alpha;` in the class:

```c
class LNT_FadeIn : ScriptedWidgetEventHandler
{
    // Filled from the layout's ScriptParamsClass block, matched by name
    reference float Start_Alpha;
    reference string Log_Label;

    protected Widget m_Root;

    void OnWidgetScriptInit(Widget w)
    {
        m_Root = w;
        m_Root.SetHandler(this);
        m_Root.SetAlpha(Start_Alpha);
        Print("Layout handler initialized for: " + Log_Label);
    }
}
```

Supported `reference` member types are `bool`, `int`, `float`, and `string`. In the layout, booleans are written as `0`/`1` and strings are quoted.

### Framework-Defined scriptclass Parameters

Because `ScriptParamsClass` values arrive before any script runs, UI frameworks use this mechanism to make layouts **declarative**: the framework ships one reusable `scriptclass`, and each layout instance configures it with its own parameters -- no per-widget code required.

Parameters in such a design fall into three kinds:

| Kind | Layout syntax | Typical use |
|---|---|---|
| Numeric / flag | `Tooltip_Delay 0.5`, `Two_Way 1` | Timings, thresholds, feature switches |
| Literal string | `Tooltip_Text "Repairs the item"` | Display text, style names |
| Name reference | `Target_Widget "RepairIcon"` | A string the framework resolves at runtime -- a widget name, a property name, a function name |

Here is a tooltip-handler skeleton showing the attribute-binding pattern; implement timer scheduling and tooltip display where indicated. The class is written once; every widget that wants a tooltip declares it in the layout with its own text and delay:

```c
class LNT_TooltipHandler : ScriptedWidgetEventHandler
{
    // Declared per-widget in the layout, filled before OnWidgetScriptInit
    reference string Tooltip_Text;
    reference float Tooltip_Delay;

    protected Widget m_Root;

    void OnWidgetScriptInit(Widget w)
    {
        m_Root = w;
        m_Root.SetHandler(this);
    }

    override bool OnMouseEnter(Widget w, int x, int y)
    {
        // A full implementation starts a Tooltip_Delay timer here,
        // then shows a tooltip widget containing Tooltip_Text.
        Print("Tooltip requested: " + Tooltip_Text);
        return true;
    }

    override bool OnMouseLeave(Widget w, Widget enterW, int x, int y)
    {
        return true;
    }
}
```

```
ButtonWidgetClass RepairButton {
 size 200 30
 hexactsize 1
 vexactsize 1
 text "Repair"
 scriptclass "LNT_TooltipHandler"
 {
  ScriptParamsClass {
   Tooltip_Text "Repairs the selected item"
   Tooltip_Delay 0.5
  }
 }
}
```

Community UI frameworks take this idea much further -- for example, [Dabs Framework](https://github.com/InclementDab/DayZ-Dabs-Framework) uses the same declare-in-layout / read-in-script mechanism to implement full MVC-style data binding between widgets and controller properties.

---

## Children Nesting

Children are placed inside a `{ }` block after the parent's attributes. Multiple children can exist in the same block.

```
FrameWidgetClass Parent {
 size 1 1
 {
  TextWidgetClass Child1 {
   position 0 0
   size 1 0.1
   text "First"
  }
  TextWidgetClass Child2 {
   position 0 0.1
   size 1 0.1
   text "Second"
  }
 }
}
```

Children are always positioned relative to their parent. A child with `position 0 0` and `size 1 1` (proportional) fills its parent completely.

---

## Complete Annotated Example

Here is a fully annotated layout file for a notification panel -- the kind of UI you might build for a mod:

```
// Root container -- invisible frame that covers 30% of screen width
// Centered horizontally, positioned at top of screen
FrameWidgetClass NotificationPanel {

 // Start hidden (script will show it)
 visible 0

 // Don't block mouse clicks on things behind this panel
 ignorepointer 1

 // Blue tint color (R=0.2, G=0.6, B=1.0, A=0.9)
 color 0.2 0.6 1.0 0.9

 // Position: 0 pixels from left, 0 pixels from top
 position 0 0
 hexactpos 1
 vexactpos 1

 // Size: 30% of parent width, 30 pixels tall
 size 0.3 30
 hexactsize 0
 vexactsize 1

 // Center horizontally within parent
 halign center_ref

 // Children block
 {
  // Text label fills the entire notification panel
  TextWidgetClass NotificationText {

   // Also ignore mouse input
   ignorepointer 1

   // Position at origin relative to parent
   position 0 0
   hexactpos 1
   vexactpos 1

   // Fill parent completely (proportional)
   size 1 1
   hexactsize 0
   vexactsize 0

   // Center the text both ways
   "text halign" center
   "text valign" center

   // Use a vanilla font (see gui/fonts in the game data)
   font "gui/fonts/sdf_MetronBook24"

   // Default text (will be overridden by script)
   text "Notification"
  }
 }
}
```

And here is a more complex example -- a dialog with a title bar, scrollable content, and a close button:

```
WrapSpacerWidgetClass MyDialog {
 clipchildren 1
 color 0.7059 0.7059 0.7059 0.7843
 size 0.35 0
 halign center_ref
 valign center_ref
 priority 998
 Padding 5
 "Size To Content H" 1
 "Size To Content V" 1
 content_halign center
 {
  // Title bar row
  FrameWidgetClass TitleBarRow {
   size 1 26
   hexactsize 0
   vexactsize 1
   draggable 1
   {
    PanelWidgetClass TitleBar {
     color 0.4196 0.6471 1 0.9412
     size 1 25
     style ColorablePanel
     {
      TextWidgetClass TitleText {
       size 0.85 0.9
       text "My Dialog"
       font "gui/fonts/Metron"
       "text halign" center
       "text valign" center
      }
      ButtonWidgetClass CloseBtn {
       size 0.15 0.9
       halign right_ref
       text "X"
      }
     }
    }
   }
  }

  // Scrollable content area
  ScrollWidgetClass ContentScroll {
   size 0.97 235
   hexactsize 0
   vexactsize 1
   "Scrollbar V" 1
   {
    WrapSpacerWidgetClass ContentItems {
     size 1 0
     hexactsize 0
     "Size To Content V" 1
    }
   }
  }
 }
}
```

---

## Copy-Paste Templates

Starter skeletons for the three layout shapes you will build most often. Save each as its own `.layout` file and load it with `GetGame().GetWorkspace().CreateWidgets("MyMod/GUI/layouts/my_panel.layout")`.

### Centered Fixed-Size Panel

A pixel-sized panel centered on screen -- the base for popups and HUD widgets:

```
FrameWidgetClass CenteredPanel {
 visible 1
 position 0 0
 hexactpos 1
 vexactpos 1
 size 400 300
 hexactsize 1
 vexactsize 1
 halign center_ref
 valign center_ref
 {
  PanelWidgetClass PanelBackground {
   color 0 0 0 0.8
   size 1 1
   hexactsize 0
   vexactsize 0
   style ColorablePanel
  }
 }
}
```

### Auto-Sizing Dialog

A `WrapSpacerWidgetClass` root that grows to fit whatever you put inside it (see the annotated dialog above for a filled-in version):

```
WrapSpacerWidgetClass AutoDialog {
 size 0.35 0
 halign center_ref
 valign center_ref
 priority 998
 clipchildren 1
 Padding 5
 "Size To Content H" 1
 "Size To Content V" 1
 content_halign center
 {
  // Add rows here -- each child stacks vertically
 }
}
```

### Scrollable List

A scroll container with an auto-growing content spacer. Insert row widgets into `ListContent` from script:

```
ScrollWidgetClass ListScroll {
 size 1 300
 hexactsize 0
 vexactsize 1
 clipchildren 1
 "Scrollbar V" 1
 {
  WrapSpacerWidgetClass ListContent {
   size 1 0
   hexactsize 0
   vexactsize 1
   "Size To Content V" 1
  }
 }
}
```

---

## Common Mistakes

1. **Forgetting the `Class` suffix** -- In layouts, write `TextWidgetClass`, not `TextWidget`.
2. **Mixing proportional and pixel values** -- If `hexactsize 0`, the size values are 0.0-1.0 proportional. If `hexactsize 1`, they are pixel values. Using `300` with proportional mode means 300x the parent width.
3. **Not quoting multi-word attributes** -- Write `"text halign" center`, not `text halign center`. An unquoted multi-word attribute is silently ignored.
4. **Placing ScriptParamsClass inside the children block** -- `ScriptParamsClass` sits in its own `{ }` brace block. When the widget has children, the params block is a second brace block *after* the children block, never inside it.
5. **Writing numeric `fixaspect` values** -- `fixaspect` takes keywords (`none`, `fixwidth`, `inside`, `outside`), not numbers.

---

## Gotchas

Engine behaviors that surprise people -- none of these produce an error message:

- If the `scriptclass` name does not match any compiled script class, the layout still loads; the widget simply has no handler. Nothing is written to the log.
- A plain class works as a `scriptclass`, but only a `ScriptedWidgetEventHandler` that calls `SetHandler(this)` receives UI events. Forgetting `SetHandler` is the usual reason `OnClick` never fires.
- `ScriptParamsClass` values bind only to `reference` members of type `bool`, `int`, `float`, or `string`. Nested blocks or arrays are not supported, and a param with no matching `reference` member is silently dropped.
- `scriptclass` resolves by global class name, and Enforce Script class names are global across every loaded mod. Prefix your handler classes (`LNT_TooltipHandler`, not `TooltipHandler`) -- two mods declaring the same class name break script compilation at server start.
- Some widget types ignore the alpha channel in `color`. You may need `inheritalpha 1` on the parent for transparency to propagate.
- Attribute defaults vary per widget type. Always set all four exact flags (`hexactpos`, `vexactpos`, `hexactsize`, `vexactsize`) explicitly instead of relying on defaults.
- `"no focus"` also prevents gamepad selection, which can break controller navigation if set on interactive widgets.
- Each widget is a real engine object. Layouts with 500+ widgets cause measurable frame drops.

---

## Best Practices

- Use `WrapSpacerWidgetClass` as the dialog root with `"Size To Content H"`/`"Size To Content V"` for auto-sizing dialogs.
- Use `priority 998-999` for modal overlays that must render above all other UI.
- Split list rows into their own `.layout` file and instantiate them into a WrapSpacer from script -- this enables reuse and widget pooling for large lists.
- Use `scriptclass` sparingly -- only on widgets that genuinely need script-driven behavior.
- Name widgets descriptively (`PlayerListScroll`, `TitleBarClose`). `FindAnyWidget()` looks up widgets by name, and duplicate names cause silent wrong-widget bugs.
- Keep layout files small and focused. Split complex UIs into multiple `.layout` files composed with `CreateWidgets()`.

---

## Next Steps

- [3.3 Sizing & Positioning](03-sizing-positioning.md) -- Master the proportional vs. pixel coordinate system
- [3.4 Container Widgets](04-containers.md) -- Deep dive into spacer and scroll widgets
