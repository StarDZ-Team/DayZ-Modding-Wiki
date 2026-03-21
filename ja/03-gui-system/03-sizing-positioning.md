# 3.3 サイズとポジション

DayZ のレイアウトシステムは**二重座標モード**を使用します — すべての寸法が比率指定（親に対する相対値）またはピクセル指定（絶対的な画面ピクセル値）のどちらかになります。このシステムの誤解がレイアウトバグの最大の原因です。この章ではこれを徹底的に説明します。

---

## 核心概念：比率指定 vs ピクセル指定

Every widget has a position (`x, y`) and a size (`width, height`). Each of these four values can independently be either:

- **Proportional** (0.0 to 1.0) -- relative to the parent widget's dimensions
- **Pixel** (any positive number) -- absolute screen pixels

The mode for each axis is controlled by four flags:

| Flag | Controls | `0` = Proportional | `1` = Pixel |
|---|---|---|---|
| `hexactpos` | X position | Fraction of parent width | Pixels from left |
| `vexactpos` | Y position | Fraction of parent height | Pixels from top |
| `hexactsize` | Width | Fraction of parent width | Pixel width |
| `vexactsize` | Height | Fraction of parent height | Pixel height |

This means you can mix modes freely. For example, a widget can have proportional width but pixel height -- a very common pattern for rows and bars.

---

## 比率モードの理解

When a flag is `0` (proportional), the value represents a **fraction of the parent's dimension**:

- `size 1 1` with `hexactsize 0` and `vexactsize 0` means "100% of parent width, 100% of parent height" -- the child fills the parent.
- `size 0.5 0.3` means "50% of parent width, 30% of parent height."
- `position 0.5 0` with `hexactpos 0` means "start at 50% of parent width from the left."

比率モードは解像度に依存しません。 親のサイズが変わるとWidgetは自動的にスケールします またはゲームが異なる解像度で実行された場合。

```
// A widget that fills the left half of its parent
FrameWidgetClass LeftHalf {
 position 0 0
 size 0.5 1
 hexactpos 0
 vexactpos 0
 hexactsize 0
 vexactsize 0
}
```

---

## ピクセルモードの理解

When a flag is `1` (pixel/exact), the value is in **screen pixels**:

- `size 200 40` with `hexactsize 1` and `vexactsize 1` means "200 pixels wide, 40 pixels tall."
- `position 10 10` with `hexactpos 1` and `vexactpos 1` means "10 pixels from parent's left edge, 10 pixels from parent's top edge."

ピクセルモードは正確な制御を提供しますが、解像度に合わせた自動スケーリングは行いません。

```
// A fixed-size button: 120x30 pixels
ButtonWidgetClass MyButton {
 position 10 10
 size 120 30
 hexactpos 1
 vexactpos 1
 hexactsize 1
 vexactsize 1
 text "Click Me"
}
```

---

## モードの混在：最も一般的なパターン

真の力は比率モードとピクセルモードの混在から生まれます。 プロの DayZ Mod で最も一般的なパターンは：

**Proportional width, pixel height** -- for bars, rows, and headers.

```
// Full-width row, exactly 30 pixels tall
FrameWidgetClass Row {
 position 0 0
 size 1 30
 hexactpos 0
 vexactpos 0
 hexactsize 0        // Width: proportional (100% of parent)
 vexactsize 1        // Height: pixel (30px)
}
```

**Proportional width and height, pixel position** -- for centered panels offset by a fixed amount.

```
// 60% x 70% panel, offset 0px from center
FrameWidgetClass Dialog {
 position 0 0
 size 0.6 0.7
 halign center_ref
 valign center_ref
 hexactpos 1         // Position: pixel (0px offset from center)
 vexactpos 1
 hexactsize 0        // Size: proportional (60% x 70%)
 vexactsize 0
}
```

---

## 配置の基準点：halign と valign

The `halign` and `valign` attributes change the **reference point** for positioning:

| Value | Effect |
|---|---|
| `left_ref` (default) | Position is measured from parent's left edge |
| `center_ref` | Position is measured from parent's center |
| `right_ref` | Position is measured from parent's right edge |
| `top_ref` (default) | Position is measured from parent's top edge |
| `center_ref` | Position is measured from parent's center |
| `bottom_ref` | Position is measured from parent's bottom edge |

When combined with pixel position (`hexactpos 1`), alignment references make centering trivial:

```
// Centered on screen with no offset
FrameWidgetClass CenteredDialog {
 position 0 0
 size 0.4 0.5
 halign center_ref
 valign center_ref
 hexactpos 1
 vexactpos 1
 hexactsize 0
 vexactsize 0
}
```

With `center_ref`, a position of `0 0` means "centered in parent." A position of `10 0` means "10 pixels right of center."

### Right-Aligned Elements

```
// Icon pinned to the right edge, 5px from the edge
ImageWidgetClass StatusIcon {
 position 5 5
 size 24 24
 halign right_ref
 valign top_ref
 hexactpos 1
 vexactpos 1
 hexactsize 1
 vexactsize 1
}
```

### Bottom-Aligned Elements

```
// Status bar at the bottom of its parent
FrameWidgetClass StatusBar {
 position 0 0
 size 1 30
 halign left_ref
 valign bottom_ref
 hexactpos 1
 vexactpos 1
 hexactsize 0
 vexactsize 1
}
```

---

## 重要：負のサイズ値は使わないこと

**レイアウトファイルで Widget のサイズに負の値を使用しないでください。** 負のサイズは未定義動作を引き起こします -- Widget が非表示になったり、不正にレンダリングされたり、UIシステムがクラッシュする可能性があります。 If you need a widget to be hidden, use `visible 0` instead.

This is one of the most common layout mistakes. Widget が表示されない場合、誤って負のサイズ値を設定していないか確認してください。

---

## よくあるサイズ指定パターン

### Full Screen Overlay

```
FrameWidgetClass Overlay {
 position 0 0
 size 1 1
 hexactpos 0
 vexactpos 0
 hexactsize 0
 vexactsize 0
}
```

### Centered Dialog (60% x 70%)

```
FrameWidgetClass Dialog {
 position 0 0
 size 0.6 0.7
 halign center_ref
 valign center_ref
 hexactpos 1
 vexactpos 1
 hexactsize 0
 vexactsize 0
}
```

### Right-Aligned Side Panel (25% Width)

```
FrameWidgetClass SidePanel {
 position 0 0
 size 0.25 1
 halign right_ref
 hexactpos 1
 vexactpos 0
 hexactsize 0
 vexactsize 0
}
```

### Top Bar (Full Width, Fixed Height)

```
FrameWidgetClass TopBar {
 position 0 0
 size 1 40
 hexactpos 0
 vexactpos 0
 hexactsize 0
 vexactsize 1
}
```

### Bottom-Right Corner Badge

```
FrameWidgetClass Badge {
 position 10 10
 size 80 24
 halign right_ref
 valign bottom_ref
 hexactpos 1
 vexactpos 1
 hexactsize 1
 vexactsize 1
}
```

### Fixed-Size Centered Icon

```
ImageWidgetClass Icon {
 position 0 0
 size 64 64
 halign center_ref
 valign center_ref
 hexactpos 1
 vexactpos 1
 hexactsize 1
 vexactsize 1
}
```

---

## プログラムによるポジションとサイズ設定

In code, you can read and set position and size using both proportional and pixel (screen) coordinates:

```c
// Proportional coordinates (0-1 range)
float x, y, w, h;
widget.GetPos(x, y);           // Read proportional position
widget.SetPos(0.5, 0.1);      // Set proportional position
widget.GetSize(w, h);          // Read proportional size
widget.SetSize(0.3, 0.2);     // Set proportional size

// Pixel/screen coordinates
widget.GetScreenPos(x, y);     // Read pixel position
widget.SetScreenPos(100, 50);  // Set pixel position
widget.GetScreenSize(w, h);    // Read pixel size
widget.SetScreenSize(400, 300);// Set pixel size
```

To center a widget on screen programmatically:

```c
int screen_w, screen_h;
GetScreenSize(screen_w, screen_h);

float w, h;
widget.GetScreenSize(w, h);
widget.SetScreenPos((screen_w - w) / 2, (screen_h - h) / 2);
```

---

## The `scaled` Attribute

When `scaled 1` is set, the widget respects DayZ's UI scaling setting (Options > Video > HUD Size). This is important for HUD elements that should scale with the user's preference.

Without `scaled`, pixel-sized widgets will be the same physical size regardless of the UI scaling option.

---

## The `fixaspect` Attribute

Use `fixaspect` to maintain a widget's aspect ratio:

- `fixaspect fixwidth` -- Height adjusts to maintain aspect ratio based on width
- `fixaspect fixheight` -- Width adjusts to maintain aspect ratio based on height

This is primarily useful for `ImageWidget` to prevent image distortion.

---

## サイズの問題のデバッグ

When a widget is not appearing where you expect:

1. **Check exact flags** -- Is `hexactsize` set to `0` when you meant pixels? A value of `200` in proportional mode means 200x the parent width (way off screen).
2. **Check for negative sizes** -- Any negative value in `size` will cause problems.
3. **Check the parent size** -- A proportional child of a zero-size parent is zero-size.
4. **Check `visible`** -- Widgets default to visible, but if a parent is hidden, all children are too.
5. **Check `priority`** -- A widget with lower priority may be hidden behind another.
6. **Use `clipchildren`** -- If a parent has `clipchildren 1`, children outside its bounds are not visible.

---

## 次のステップ

- [3.4 Container Widgets](04-containers.md) -- How spacers and scroll widgets handle layout automatically
- [3.5 Programmatic Widget Creation](05-programmatic-widgets.md) -- Setting size and position from code
