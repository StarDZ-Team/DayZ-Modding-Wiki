# inputs.xml --- Custom Keybindings


---

> **Summary:** The `inputs.xml` file lets your mod register custom keybindings that appear in the player's Controls settings menu. Players can view, rebind, and toggle these inputs just like vanilla actions. This is the standard mechanism for adding hotkeys to DayZ mods.

---

## Table of Contents

- [Overview](#overview)
- [File Location](#file-location)
- [Complete XML Structure](#complete-xml-structure)
- [Actions Block](#actions-block)
- [Sorting Block](#sorting-block)
- [Preset Block (Default Keybindings)](#preset-block-default-keybindings)
- [Modifier Combos](#modifier-combos)
- [Hidden Inputs](#hidden-inputs)
- [Multiple Default Keys](#multiple-default-keys)
- [Accessing Inputs in Script](#accessing-inputs-in-script)
- [Input Methods Reference](#input-methods-reference)
- [Suppressing and Disabling Inputs](#suppressing-and-disabling-inputs)
- [Key Names Reference](#key-names-reference)
- [Worked Examples](#worked-examples)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)
- [Theory vs Practice](#theory-vs-practice)
- [Compatibility & Impact](#compatibility--impact)
- [Patterns in the Wild](#patterns-in-the-wild)

---

## Overview

When your mod needs the player to press a key --- opening a menu, toggling a feature, commanding an AI unit --- you register a custom input action in `inputs.xml`. The engine reads this file at startup and integrates your actions into the universal input system. Players see your keybindings in the game's Settings > Controls menu, grouped under a heading you define.

Custom inputs are identified by a unique action name (conventionally prefixed with `UA` for "User Action") and can have default keybindings that players can rebind at will.

---

## File Location

You can place `inputs.xml` anywhere inside your mod's PBO. A common layout is a `data` subfolder of your Scripts directory:

```
@MyMod/
  Addons/
    MyMod_Scripts.pbo
      Scripts/
        data/
          inputs.xml        <-- Here
        3_Game/
        4_World/
        5_Mission/
```

The file's location is not fixed by convention; the engine does not auto-discover it. You must register the file by pointing the `inputs` property of your `config.cpp` `CfgMods` block at it, for example `inputs = "MyMod/Scripts/data/inputs.xml";`. The path is arbitrary --- the engine loads the file from wherever you specify.

---

## Complete XML Structure

An `inputs.xml` file has three sections, all wrapped in a `<modded_inputs>` root element:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <!-- Action definitions go here -->
        </actions>

        <sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
            <!-- Sort order for the settings menu -->
        </sorting>
    </inputs>
    <preset>
        <!-- Default keybinding assignments go here -->
    </preset>
</modded_inputs>
```

All three sections --- `<actions>`, `<sorting>`, and `<preset>` --- work together but serve different purposes.

---

## Actions Block

The `<actions>` block declares every input action your mod provides. Each action is a single `<input>` element.

### Syntax

```xml
<actions>
    <input name="UAMyModOpenMenu" loc="STR_MYMOD_INPUT_OPEN_MENU" />
    <input name="UAMyModToggleHUD" loc="STR_MYMOD_INPUT_TOGGLE_HUD" />
</actions>
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Unique action identifier. Convention: prefix with `UA` (User Action). Used in scripts to poll this input. |
| `loc` | No | Stringtable key for the display name in the Controls menu. **No `#` prefix** --- the system adds it. |
| `visible` | No | Set to `"false"` to hide from the Controls menu. Defaults to `true`. |

### Naming Convention

Action names must be globally unique across all loaded mods. Use your mod prefix:

```xml
<input name="UAMyModAdminPanel" loc="STR_MYMOD_INPUT_ADMIN_PANEL" />
<input name="UALNTConfirm" loc="STR_LNT_INPUT_CONFIRM" />
<input name="LNTCommandMenu" loc="STR_LNT_INPUT_COMMAND_MENU" />
```

The `UA` prefix is conventional but not enforced. The Lantern examples in this wiki use a bare `LNT` prefix for some actions, which also works --- the engine only cares that the name is unique.

---

## Sorting Block

The `<sorting>` block controls how your inputs appear in the player's Controls settings. It defines a named group (which becomes a section header) and lists the inputs in display order.

### Syntax

```xml
<sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
    <input name="UAMyModOpenMenu" />
    <input name="UAMyModToggleHUD" />
    <input name="UAMyModSpecialAction" />
</sorting>
```

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Internal identifier for this sorting group |
| `loc` | Yes | Stringtable key for the group header displayed in Settings > Controls |

### How It Appears

In the Controls settings, the player sees:

```
[MyMod]                          <-- from the sorting loc
  Open Menu .............. [Y]   <-- from the input loc + preset
  Toggle HUD ............. [H]   <-- from the input loc + preset
```

Only inputs listed in the `<sorting>` block appear in the settings menu. Inputs defined in `<actions>` but not listed in `<sorting>` are silently registered but invisible to the player (even if `visible` is not explicitly set to `false`).

---

## Preset Block (Default Keybindings)

The `<preset>` block assigns default keys to your actions. These are the keys the player starts with before any customization.

### Simple Key Binding

```xml
<preset>
    <input name="UAMyModOpenMenu">
        <btn name="kY"/>
    </input>
</preset>
```

This binds the `Y` key as the default for `UAMyModOpenMenu`.

### No Default Key

If you omit an action from the `<preset>` block, it has no default binding. The player must manually assign a key in Settings > Controls. This is appropriate for optional or advanced bindings.

---

## Modifier Combos

To require a modifier key (Ctrl, Shift, Alt), nest `<btn>` elements:

### Ctrl + Left Mouse Button

```xml
<input name="LNTSetWaypoint">
    <btn name="kLControl">
        <btn name="mBLeft"/>
    </btn>
</input>
```

The outer `<btn>` is the modifier; the inner `<btn>` is the primary key. The player must hold the modifier and then press the primary key.

### Shift + Key

```xml
<input name="UAMyModQuickAction">
    <btn name="kLShift">
        <btn name="kQ"/>
    </btn>
</input>
```

### Nesting Rules

- The **outer** `<btn>` is always the modifier (held down)
- The **inner** `<btn>` is the trigger (pressed while modifier is held)
- Only one level of nesting is typical; deeper nesting is untested and not recommended

---

## Hidden Inputs

Use `visible="false"` to register an input that the player cannot see or rebind in the Controls menu. This is useful for internal inputs used by your mod's code that should not be player-configurable.

```xml
<actions>
    <input name="LNTTestInput" visible="false" />
    <input name="UALNTConfirm" loc="" visible="false" />
</actions>
```

Hidden inputs can still have default key assignments in the `<preset>` block:

```xml
<preset>
    <input name="LNTTestInput">
        <btn name="kY"/>
    </input>
</preset>
```

---

## Multiple Default Keys

An action can have multiple default keys. List multiple `<btn>` elements as siblings:

```xml
<input name="UALNTConfirm">
    <btn name="kReturn" />
    <btn name="kNumpadEnter" />
</input>
```

Both `Enter` and `Numpad Enter` will trigger `UALNTConfirm`. This is useful for actions where multiple physical keys should map to the same logical action.

---

## Accessing Inputs in Script

### Getting the Input API

All input access goes through `GetUApi()`, which returns the global User Action API:

```c
UAInput input = GetUApi().GetInputByName("UAMyModOpenMenu");
```

### Polling in OnUpdate

Custom inputs are typically polled in `MissionGameplay.OnUpdate()` or similar per-frame callbacks:

```c
modded class MissionGameplay
{
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);

        UAInput input = GetUApi().GetInputByName("UAMyModOpenMenu");

        if (input.LocalPress())
        {
            // Key was just pressed this frame
            OpenMyModMenu();
        }
    }
}
```

### Alternative: Using the Input Name Directly

Many mods check inputs inline using the `Input` class (from `GetGame().GetInput()`), which exposes string-keyed overloads instead of a `UAInput` object:

```c
override void OnUpdate(float timeslice)
{
    super.OnUpdate(timeslice);

    Input input = GetGame().GetInput();

    if (input.LocalPress("UAMyModOpenMenu", false))
    {
        OpenMyModMenu();
    }
}
```

The `false` parameter in `LocalPress("name", false)` is the `check_focus` argument. Passing `false` evaluates the input even when the game window is unfocused; when it is `true` (the default), an unfocused game returns `false`. It does not control input consumption.

---

## Input Methods Reference

DayZ exposes **two distinct APIs** for reading an input's state, and their method sets are not identical:

- **`UAInput`** --- obtained via `GetUApi().GetInputByName("ActionName")`. Its state methods take **no arguments**; they always query the input object they were called on (`scripts/3_game/inputapi/uainput.c`).
- **`Input`** --- obtained via `GetGame().GetInput()`. Its state methods take the action name as a **string**, plus an optional `check_focus` bool (default `true`) (`scripts/3_game/tools/input.c`).

| `UAInput` method (no args) | `Input` method (string, bool) | Returns | When True |
|---|---|---------|-----------|
| `LocalPress()` | `LocalPress(name, check_focus)` | `bool` | The key was pressed **this frame** (single trigger on key-down) |
| `LocalRelease()` | `LocalRelease(name, check_focus)` | `bool` | The key was released **this frame** (single trigger on key-up) |
| `LocalClick()` | *(no equivalent on `Input`)* | `bool` | The key was pressed and released quickly (tap) --- only queryable through a `UAInput` reference |
| `LocalHold()` | `LocalHold(name, check_focus)` | `bool` | The key has been held down for a threshold duration |
| `LocalDoubleClick()` | `LocalDbl(name, check_focus)` | `bool` | The key was tapped twice quickly --- note the method is named `LocalDoubleClick` on `UAInput` but `LocalDbl` on `Input` |
| `LocalValue()` | `LocalValue(name, check_focus)` | `float` | Current analog value (0.0 or 1.0 for digital keys; variable for analog axes) |

`UAInput` additionally exposes `LocalHoldBegin()` (no `Input` equivalent), which fires once when a hold begins rather than repeatedly while held.

### Usage Patterns

**Toggle on press:**
```c
if (input.LocalPress("UAMyModToggle", false))
{
    m_IsEnabled = !m_IsEnabled;
}
```

**Hold to activate, release to deactivate:**
```c
if (input.LocalPress("LNTCommandMenu", false))
{
    ShowCommandWheel();
}

if (input.LocalRelease("LNTCommandMenu", false) || input.LocalValue("LNTCommandMenu", false) == 0)
{
    HideCommandWheel();
}
```

**Double-tap action:**
```c
if (input.LocalDbl("UAMyModSpecial", false))
{
    PerformSpecialAction();
}
```

**Hold for extended action:**
```c
if (input.LocalHold("UAMyModMapToggle"))
{
    ToggleMapMode();
}
```

---

## Suppressing and Disabling Inputs

### ForceDisable / ForceEnable

`UAInput` declares a matched pair (`scripts/3_game/inputapi/uainput.c`), both taking a bool:

```c
proto native void ForceEnable(bool bEnable);   // force enable on/off
proto native void ForceDisable(bool bEnable);  // force disable on/off
```

`ForceDisable` temporarily disables a specific input --- commonly used when opening menus to prevent game actions from firing while a UI is active:

```c
// Disable the input while menu is open
GetUApi().GetInputByName("UAMyModToggle").ForceDisable(true);

// Re-enable when menu closes
GetUApi().GetInputByName("UAMyModToggle").ForceDisable(false);
```

`ForceEnable(true)` is the separate "force on" override, not the undo for `ForceDisable(true)` --- to undo a disable, pass `false` to the same method you used.

### SupressNextFrame

```c
proto native void SupressNextFrame(bool bForce);
```

Suppresses inputs for the next frame. The vanilla comment is more specific than the name suggests: it suppresses *"for nextframe (until key release - call this when leaving main menu and alike - to avoid button collision after character control returned)"*. So the suppression persists until the key is released, not strictly for one frame --- which is exactly what you want when handing control back after a menu closes:

```c
GetUApi().SupressNextFrame(true);
```

Note the spelling: one `p`, as in the engine declaration.

### UpdateControls

```c
proto native void UpdateControls();   // "call this on each change of exclusion"
```

The vanilla comment scopes this to exclusion changes. Call it after modifying input states so the change applies immediately:

```c
GetUApi().GetInputByName("UAMyModToggle").ForceDisable(false);
GetUApi().UpdateControls();
```

### Input Excludes

The vanilla mission system provides exclude groups. `AddActiveInputExcludes()` / `RemoveActiveInputExcludes()` are methods on `Mission` (`scripts/3_game/gameplay.c`), so call them either from inside a `Mission`/`MissionGameplay`-derived class or through `GetGame().GetMission()`. When a menu is active, you can exclude categories of inputs (vanilla itself uses groups such as `"inventory"`, `"map"`, and `"swimming"`):

```c
// Suppress gameplay inputs while inventory is open
GetGame().GetMission().AddActiveInputExcludes({"inventory"});

// Restore when closing
GetGame().GetMission().RemoveActiveInputExcludes({"inventory"});
```

---

## Key Names Reference

Key names used in the `<btn name="">` attribute follow a specific naming convention. Here is the complete reference.

### Keyboard Keys

| Category | Key Names |
|----------|-----------|
| Letters | `kA`, `kB`, `kC`, `kD`, `kE`, `kF`, `kG`, `kH`, `kI`, `kJ`, `kK`, `kL`, `kM`, `kN`, `kO`, `kP`, `kQ`, `kR`, `kS`, `kT`, `kU`, `kV`, `kW`, `kX`, `kY`, `kZ` |
| Numbers (top row) | `k0`, `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9` |
| Function keys | `kF1`, `kF2`, `kF3`, `kF4`, `kF5`, `kF6`, `kF7`, `kF8`, `kF9`, `kF10`, `kF11`, `kF12` |
| Modifiers | `kLControl`, `kRControl`, `kLShift`, `kRShift`, `kLMenu` (Left Alt), `kRMenu` (Right Alt) |
| Navigation | `kUp`, `kDown`, `kLeft`, `kRight`, `kHome`, `kEnd`, `kPrior` (Page Up), `kNext` (Page Down) |
| Editing | `kReturn`, `kBackspace`, `kDelete`, `kInsert`, `kSpace`, `kTab`, `kEscape` |
| Numpad | `kNumpad0` ... `kNumpad9`, `kNumpadEnter`, `kAdd` (numpad +), `kSubstract` (numpad -, note engine spelling), `kMultiply` (numpad *), `kDivide` (numpad /), `kDecimal` (numpad .) |
| Punctuation | `kMinus`, `kEquals`, `kLBracket`, `kRBracket`, `kBackslash`, `kSemicolon`, `kApostrophe`, `kComma`, `kPeriod`, `kSlash`, `kGrave` |
| Locks | `kCapital` (Caps Lock), `kNumlock` (note lowercase `l`), `kScrollLock` |

### Mouse Buttons

| Name | Button |
|------|--------|
| `mBLeft` | Left mouse button |
| `mBRight` | Right mouse button |
| `mBMiddle` | Middle mouse button (scroll wheel click) |
| `mB4` | Mouse button 4 (side button back) |
| `mB5` | Mouse button 5 (side button forward) |
| `mB6`, `mB7`, `mB8` | Additional mouse buttons |

### Mouse Movement and Wheel

| Name | Direction |
|------|-----------|
| `mLeft` | Mouse moved left |
| `mRight` | Mouse moved right |
| `mUp` | Mouse moved up |
| `mDown` | Mouse moved down |
| `mWheelUp` | Scroll wheel up |
| `mWheelDown` | Scroll wheel down |

### Naming Pattern

- **Keyboard**: `k` prefix + key name (e.g., `kT`, `kF5`, `kLControl`)
- **Mouse buttons**: `mB` prefix + button name (e.g., `mBLeft`, `mBRight`)
- **Mouse movement/wheel**: `m` prefix + direction name (e.g., `mLeft`, `mWheelUp`)

---

## Worked Examples

> The examples below use **Lantern**, this wiki's constructed teaching mod (see the Part 7 chapters for its full framework code). It is not a real published mod.

### Lantern AI Command Menu

A well-structured inputs.xml with visible keybindings, hidden debug inputs, and a modifier combo. This is the input file for Lantern's fictional AI squad-command feature:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="LNTCommandMenu" loc="STR_LNT_INPUT_COMMAND_MENU"/>
            <input name="LNTSetWaypoint" loc="STR_LNT_INPUT_SET_WAYPOINT"/>
            <input name="LNTTestInput" visible="false" />
            <input name="LNTDebugCamLeft" visible="false" />
            <input name="LNTDebugCamRight" visible="false" />
            <input name="LNTDebugCamUp" visible="false" />
            <input name="LNTDebugCamDown" visible="false" />
        </actions>

        <sorting name="lantern" loc="STR_LNT_INPUT_GROUP">
            <input name="LNTCommandMenu" />
            <input name="LNTSetWaypoint" />
        </sorting>
    </inputs>
    <preset>
        <input name="LNTCommandMenu">
            <btn name="kT"/>
        </input>
        <input name="LNTSetWaypoint">
            <btn name="kLControl">
                <btn name="mBLeft"/>
            </btn>
        </input>
        <input name="LNTTestInput">
            <btn name="kY"/>
        </input>
        <input name="LNTDebugCamLeft">
            <btn name="kLeft"/>
        </input>
        <input name="LNTDebugCamRight">
            <btn name="kRight"/>
        </input>
        <input name="LNTDebugCamUp">
            <btn name="kUp"/>
        </input>
        <input name="LNTDebugCamDown">
            <btn name="kDown"/>
        </input>
    </preset>
</modded_inputs>
```

Key observations:
- `LNTCommandMenu` bound to `T` --- visible in settings, player can rebind
- `LNTSetWaypoint` uses a **Ctrl + Left Click** modifier combo
- Debug inputs are `visible="false"` **and** omitted from `<sorting>` --- hidden from players but accessible in code (see [Theory vs Practice](#theory-vs-practice) for why both matter)

### Hidden Confirm Input

A minimal inputs.xml for a hidden utility input with multiple default keys --- the kind of internal "confirm" action a trading or dialog UI polls for:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="UALNTConfirm" loc="" visible="false" />
        </actions>
    </inputs>
    <preset>
        <input name="UALNTConfirm">
            <btn name="kReturn" />
            <btn name="kNumpadEnter" />
        </input>
    </preset>
</modded_inputs>
```

Key observations:
- Hidden input (`visible="false"`) with empty `loc` --- never shown in settings
- Two default keys: both Enter and Numpad Enter trigger the same action
- No `<sorting>` block --- not needed since the input is hidden

### Complete Starter Template

A minimal but complete template for a new mod:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="UAMyModOpenMenu" loc="STR_MYMOD_INPUT_OPEN_MENU" />
            <input name="UAMyModQuickAction" loc="STR_MYMOD_INPUT_QUICK_ACTION" />
        </actions>

        <sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
            <input name="UAMyModOpenMenu" />
            <input name="UAMyModQuickAction" />
        </sorting>
    </inputs>
    <preset>
        <input name="UAMyModOpenMenu">
            <btn name="kF6"/>
        </input>
        <!-- UAMyModQuickAction has no default key; player must bind it -->
    </preset>
</modded_inputs>
```

With a corresponding stringtable.csv:

```csv
"Language","original","english"
"STR_MYMOD_INPUT_GROUP","My Mod","My Mod"
"STR_MYMOD_INPUT_OPEN_MENU","Open Menu","Open Menu"
"STR_MYMOD_INPUT_QUICK_ACTION","Quick Action","Quick Action"
```

---

## Common Mistakes

### Using `#` in the loc Attribute

```xml
<!-- WRONG -->
<input name="UAMyAction" loc="#STR_MYMOD_ACTION" />

<!-- CORRECT -->
<input name="UAMyAction" loc="STR_MYMOD_ACTION" />
```

The input system prepends `#` internally. Adding it yourself causes a double-prefix and the lookup fails.

### Action Name Collisions

If two mods define `UAOpenMenu`, only one will work. Always use your mod prefix:

```xml
<input name="UAMyModOpenMenu" />     <!-- Good -->
<input name="UAOpenMenu" />          <!-- Risky -->
```

### Missing Sorting Entry

If you define an action in `<actions>` but forget to list it in `<sorting>`, the action works in code but is invisible in the Controls menu. The player has no way to rebind it.

### Forgetting to Define in Actions

If you list an input in `<sorting>` or `<preset>` but never define it in `<actions>`, the engine silently ignores it.

### Binding Conflicting Keys

Choosing keys that conflict with vanilla bindings (like `W`, `A`, `S`, `D`, `Tab`, `I`) causes both your action and the vanilla action to fire simultaneously. Use less common keys (F5-F12, numpad keys) or modifier combos for safety.

---

## Best Practices

- Always prefix action names with `UA` + your mod name (e.g., `UAMyModOpenMenu`). Generic names like `UAOpenMenu` will collide with other mods.
- Provide a `loc` attribute for every visible input and define the corresponding stringtable key. Without it, the Controls menu shows the raw action name.
- Choose uncommon default keys (F5-F12, numpad) or modifier combos (Ctrl+key) to minimize conflicts with vanilla and popular mod keybindings.
- Always list visible inputs in the `<sorting>` block. An input defined in `<actions>` but missing from `<sorting>` is invisible to the player and cannot be rebound.
- Cache the `UAInput` reference from `GetUApi().GetInputByName()` in a member variable rather than calling it every frame in `OnUpdate`. The string lookup has overhead.

---

## Theory vs Practice

> What the documentation says versus how things actually work at runtime.

| Concept | Theory | Reality |
|---------|--------|---------|
| `visible="false"` hides from Controls menu | Input is registered but invisible | Omitting the action from `<sorting>` is the reliable way to hide it. Rely on that rather than `visible="false"` alone if a hidden input ever appears in the list |
| `LocalPress()` fires once per key-down | Single trigger on the frame the key is pressed | Only for an unlimited input. The vanilla doc on `Input.LocalPress()` states: *"if the input is limited (click, hold, doubleclick), 'Press' event is limited as well, and reacts to the limiter only!"* --- so on an action bound as a hold or double-click, `LocalPress()` fires when the **limiter** is satisfied, not on the raw key-down. For critical actions you can also check `LocalValue() > 0` as a fallback |
| Modifier combos via nested `<btn>` | Outer is modifier, inner is trigger | The modifier key alone also registers as a press on its own input -- vanilla's default binding maps `kLControl` to Hold Breath and `kC` to the crouch/stance action. Players holding Ctrl+Click will also trigger Hold Breath |
| `ForceDisable(true)` suppresses input | Input is completely ignored | `ForceDisable` has no automatic re-enable; if your mod fails to call `ForceDisable(false)` (a crash, an early return), the input stays disabled for the rest of the session. Always pair the disable with a guaranteed re-enable path (a `finally`-style cleanup or an `OnUpdate` safety check) |
| Multiple `<btn>` siblings | Both keys trigger the same action | Works correctly, but the Controls menu only displays the first key. The player can see and rebind the first key but may not realize the second default exists |

---

## Compatibility & Impact

- **Multi-Mod:** Action name collisions are the primary risk. If two mods define `UAOpenMenu`, only one works and the conflict is silent. There is no engine warning for duplicate action names across mods.
- **Performance:** Polling 5-10 inputs per frame via `GetUApi().GetInputByName()` is unlikely to be a bottleneck, but caching the `UAInput` reference in a member variable and reusing it in `OnUpdate` avoids a repeated per-frame name lookup and is the pattern used by established frameworks.
- **Version:** The `inputs.xml` / `<modded_inputs>` structure and the `visible` attribute are both present in the current vanilla input definitions (`bin/constants.xml`, e.g. `visible="false"` on `UAHoldBreathToggle`) and in use by current-generation mods; `visible` is an inputs-XML attribute, not a member of the `UAInput`/`UAInputAPI` script surface declared in `scripts/3_game/inputapi/uainput.c`.

---

## Patterns in the Wild

Recurring `inputs.xml` patterns you will see across published mods:

| Pattern | Detail |
|---------|--------|
| Modifier combo `Ctrl+Click` | AI and building mods bind "place waypoint/object" style actions with nested `<btn name="kLControl"><btn name="mBLeft"/>` so a plain left click keeps its vanilla meaning |
| Hidden utility inputs | Trading and dialog UIs register a `visible="false"` confirm action with dual keys (Enter + Numpad Enter) for internal confirmation logic |
| `ForceDisable` during menu open | Admin panels call `ForceDisable(true)` on gameplay inputs when the panel opens, and `ForceDisable(false)` on close to prevent character movement while typing |
| Cached `UAInput` in member variable | UI frameworks store the `GetUApi().GetInputByName()` result in a class field during init, then poll the cached reference in `OnUpdate` to avoid the per-frame string lookup |
