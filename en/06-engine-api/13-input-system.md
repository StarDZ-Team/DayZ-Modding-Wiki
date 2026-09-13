# Input System

> **Summary:** The DayZ input system maps keyboard, mouse, and gamepad hardware to named actions declared in inputs.xml, and exposes the UAInput API so scripts can query presses, releases, holds, and analog values at runtime.

---

## Introduction

The DayZ input system connects hardware inputs --- keyboard, mouse, and gamepad --- to named actions that scripts can query. It operates in two layers:

1. **inputs.xml** (config layer) --- declares named actions, assigns default keybindings, and organizes them into groups for the player's Controls settings menu. See [Chapter 5.2: inputs.xml](../05-config-files/02-inputs-xml.md) for full coverage.

2. **UAInput API** (script layer) --- queries input state at runtime. This is what your scripts call every frame to detect presses, releases, holds, and analog values.

This chapter covers the script layer: the classes, methods, and patterns you use to read and control inputs from Enforce Script.

---

## Core Classes

The input system is built on three main classes:

```
UAInputAPI         Global singleton (accessed via GetUApi())
├── UAInput        Represents a single named input action
└── Input          Lower-level input access (accessed via GetGame().GetInput())
```

| Class | Source File | Purpose |
|-------|-----------|---------|
| `UAInputAPI` | `3_Game/inputapi/uainput.c` | Global input manager. Retrieves inputs by name/ID, manages excludes, presets, and backlit. |
| `UAInput` | `3_Game/inputapi/uainput.c` | Single input action. Provides state queries (press, hold, release) and control (disable, suppress, lock). |
| `Input` | `3_Game/tools/input.c` | Engine-level input class. String-based state queries, device management, game focus control. |
| `InputUtils` | `3_Game/tools/inpututils.c` | Static helper class. Button name/icon resolution for UI display. |

---

## Accessing the Input API

### UAInputAPI (Recommended)

The primary way to access inputs. `GetUApi()` is a global function that returns the `UAInputAPI` singleton:

```c
// Get the global input API
UAInputAPI inputAPI = GetUApi();

// Get a specific input action by its name (as defined in inputs.xml)
UAInput input = inputAPI.GetInputByName("UAMyAction");

// Get a specific input action by its numeric ID
UAInput input = inputAPI.GetInputByID(someID);
```

### Input Class (Alternative)

The `Input` class provides string-based state queries directly, without needing a `UAInput` reference first:

```c
// Get the Input instance
Input input = GetGame().GetInput();

// Query by action name string
if (input.LocalPress("UAMyAction", false))
{
    // Key was just pressed
}
```

The `bool check_focus` parameter (second argument) controls whether the check respects game focus. Pass `true` (default) to return false when the game window is unfocused. Pass `false` to always return the raw input state.

### When to Use Which

- **`GetUApi().GetInputByName()`** --- Use when you need to query the same input multiple times, suppress/disable it, or inspect its bindings. You get a `UAInput` object you can reuse.
- **`GetGame().GetInput().LocalPress()`** --- Use for one-off checks where you do not need to manipulate the input itself. Simpler syntax but slightly less efficient for repeated queries.

---

## Reading Input State --- UAInput Methods

Once you have a `UAInput` reference, these methods query its current state:

```c
UAInput input = GetUApi().GetInputByName("UAMyAction");

// Frame-precise checks
bool justPressed   = input.LocalPress();        // True on the FIRST frame the key goes down
bool justReleased  = input.LocalRelease();       // True on the FIRST frame the key comes up
bool holdStarted   = input.LocalHoldBegin();     // True on the first frame hold threshold is met
bool isHeld        = input.LocalHold();          // True EVERY frame while key is held past threshold
bool clicked       = input.LocalClick();         // True on press-and-release before hold threshold
bool doubleClicked = input.LocalDoubleClick();   // True when a double-tap is detected

// Analog value
float value = input.LocalValue();                // 0.0 or 1.0 for digital; 0.0-1.0 for analog axes
```

---

## Reading Input State --- Input Class Methods

The `Input` class (from `GetGame().GetInput()`) offers equivalent string-based methods:

```c
Input input = GetGame().GetInput();

bool pressed  = input.LocalPress("UAMyAction", false);
bool released = input.LocalRelease("UAMyAction", false);
bool held     = input.LocalHold("UAMyAction", false);
bool dblClick = input.LocalDbl("UAMyAction", false);
float value   = input.LocalValue("UAMyAction", false);
```

Note the slight naming difference: `LocalDoubleClick()` on `UAInput` vs `LocalDbl()` on `Input`.

The `Input` class also provides `_ID` variants that accept integer action IDs instead of strings (e.g., `LocalPress_ID(int action, bool check_focus = true)`). `UAInput` has no `_ID` overloads; its methods (`LocalPress()`, etc.) take no parameters.

---

## Input Query Methods Reference

### UAInput Methods

| Method | Returns | When True | Use Case |
|--------|---------|-----------|----------|
| `LocalPress()` | `bool` | First frame the key goes down | Toggle actions, one-shot triggers |
| `LocalRelease()` | `bool` | First frame the key comes up | End continuous actions |
| `LocalClick()` | `bool` | Key pressed and released before hold timer | Quick tap detection |
| `LocalHoldBegin()` | `bool` | First frame hold threshold is reached | Start hold-based actions |
| `LocalHold()` | `bool` | Every frame while held past threshold | Continuous hold actions |
| `LocalDoubleClick()` | `bool` | Double-tap detected | Special/alternate actions |
| `LocalValue()` | `float` | Always (returns current value) | Mouse axes, gamepad triggers, analog input |

### Input Class Methods

| Method | Returns | Signature | Equivalent UAInput Method |
|--------|---------|-----------|--------------------------|
| `LocalPress()` | `bool` | `LocalPress(string action, bool check_focus = true)` | `UAInput.LocalPress()` |
| `LocalRelease()` | `bool` | `LocalRelease(string action, bool check_focus = true)` | `UAInput.LocalRelease()` |
| `LocalHold()` | `bool` | `LocalHold(string action, bool check_focus = true)` | `UAInput.LocalHold()` |
| `LocalDbl()` | `bool` | `LocalDbl(string action, bool check_focus = true)` | `UAInput.LocalDoubleClick()` |
| `LocalValue()` | `float` | `LocalValue(string action, bool check_focus = true)` | `UAInput.LocalValue()` |

### Important Timing Notes

- **`LocalPress()`** fires on exactly **one frame** --- the frame the key transitions from up to down. If you check it on any other frame, it returns false.
- **`LocalClick()`** fires when the key is pressed and released quickly (before the hold timer kicks in). It is NOT the same as `LocalPress()`. Use `LocalPress()` for immediate key-down detection.
- **`LocalHold()`** does NOT fire immediately. It waits for the engine's hold threshold to be met first. Use `LocalPress()` if you need instant response.
- **`LocalHoldBegin()`** fires once when the hold threshold is first met. `LocalHold()` then fires every subsequent frame.

---

## Checking Inputs in OnUpdate

The standard pattern for polling custom inputs is inside `MissionGameplay.OnUpdate()`:

```c
modded class MissionGameplay
{
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);

        // Guard: need a live player
        PlayerBase player = PlayerBase.Cast(GetGame().GetPlayer());
        if (!player)
            return;

        // Guard: no input while a menu is open
        if (GetGame().GetUIManager().GetMenu())
            return;

        UAInput myInput = GetUApi().GetInputByName("UAMyModOpenMenu");
        if (myInput && myInput.LocalPress())
        {
            OpenMyModMenu();
        }
    }
}
```

### Using the Input Class Instead

```c
modded class MissionGameplay
{
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);

        Input input = GetGame().GetInput();

        if (input.LocalPress("UAMyModOpenMenu", false))
        {
            OpenMyModMenu();
        }
    }
}
```

### Where Else Can You Check Inputs?

Inputs can technically be checked in any per-frame callback, but `MissionGameplay.OnUpdate()` is the canonical location. Other valid places include:

- `PlayerBase.CommandHandler(float pDt, int pCurrentCommandID, bool pCurrentCommandFinished)` --- the engine header describes it as "updated each tick". Note that it runs for **every** simulated `DayZPlayer`, on the server as well as the client, not only for the local player. A `GetUApi()` query placed here is only meaningful on the client for the player you actually control, so guard it. Vanilla itself reads synced input in this callback through `GetInputController()` (a `HumanInputController`), not through `UAInput`.
- `ScriptedWidgetEventHandler.OnUpdate(Widget w)` --- for UI-specific input (but prefer widget event handlers)
- `PluginBase.OnUpdate(float delta_time)` --- for plugin-scoped input

Avoid checking inputs in server-side code, entity constructors, or one-off event handlers where frame timing is not guaranteed.

---

## Alternative: OnKeyPress and OnKeyRelease

For simple hardcoded key detection, the base `Mission` class (`3_Game/gameplay.c`)
declares `OnKeyPress(int key)` and `OnKeyRelease(int key)`, which `MissionGameplay`
overrides. `DayZGame.OnKeyPress()` forwards every raw key event to the active
mission, so overriding them in `MissionGameplay` works:

```c
modded class MissionGameplay
{
    override void OnKeyPress(int key)
    {
        super.OnKeyPress(key);

        if (key == KeyCode.KC_F5)
        {
            // F5 was pressed --- not rebindable!
            ToggleDebugOverlay();
        }
    }

    override void OnKeyRelease(int key)
    {
        super.OnKeyRelease(key);

        if (key == KeyCode.KC_F5)
        {
            // F5 was released
        }
    }
}
```

### UAInput vs OnKeyPress: When to Use Which

| Feature | UAInput (GetUApi) | OnKeyPress |
|---------|-------------------|------------|
| Player can rebind | Yes | No |
| Supports modifiers | Yes (Ctrl+Key combos via inputs.xml) | Manual checking required |
| Gamepad support | Yes | No |
| Appears in Controls menu | Yes | No |
| Analog values | Yes | No |
| Simplicity | Requires inputs.xml setup | Just check KeyCode |
| Best for | All player-facing actions | Debug tools, hardcoded dev shortcuts |

**Rule of thumb:** If a player will ever press this key, use UAInput with inputs.xml. Only use OnKeyPress for internal debug tools or prototype testing.

> **UA button names and raw `KeyCode` constants are different namespaces.** UA bindings use names such as `kLMenu`, `kRMenu`, and `kBackspace`; raw-key APIs use `KeyCode.KC_LMENU`, `KeyCode.KC_RMENU`, and `KeyCode.KC_BACK`. In the inspected build's `bin/constants.xml` button table, the corresponding UA button IDs are 505, 567, and 463. Prefer the names in XML and `BindCombo()` calls, and verify numeric IDs against the installed build before storing them.

---

## KeyCode Reference

The `KeyCode` enum is defined in `1_Core/proto/ensystem.c`. These constants are used with `OnKeyPress()`, `OnKeyRelease()`, `KeyState()`, and `DisableKey()`.

### Commonly Used Keys

| Category | Constants |
|----------|-----------|
| Escape | `KC_ESCAPE` |
| Function keys | `KC_F1` through `KC_F12` |
| Number row | `KC_1`, `KC_2`, `KC_3`, `KC_4`, `KC_5`, `KC_6`, `KC_7`, `KC_8`, `KC_9`, `KC_0` |
| Letters | `KC_A` through `KC_Z` (e.g., `KC_Q`, `KC_W`, `KC_E`, `KC_R`, `KC_T`) |
| Modifiers | `KC_LSHIFT`, `KC_RSHIFT`, `KC_LCONTROL`, `KC_RCONTROL`, `KC_LMENU` (left Alt), `KC_RMENU` (right Alt) |
| Navigation | `KC_UP`, `KC_DOWN`, `KC_LEFT`, `KC_RIGHT` |
| Editing | `KC_SPACE`, `KC_RETURN`, `KC_TAB`, `KC_BACK` (Backspace), `KC_DELETE`, `KC_INSERT` |
| Page control | `KC_HOME`, `KC_END`, `KC_PRIOR` (Page Up), `KC_NEXT` (Page Down) |
| Numpad | `KC_NUMPAD0` through `KC_NUMPAD9`, `KC_NUMPADENTER`, `KC_ADD`, `KC_SUBTRACT`, `KC_MULTIPLY`, `KC_DIVIDE`, `KC_DECIMAL` |
| Locks | `KC_CAPITAL` (Caps Lock), `KC_NUMLOCK`, `KC_SCROLL` (Scroll Lock) |
| Punctuation | `KC_MINUS`, `KC_EQUALS`, `KC_LBRACKET`, `KC_RBRACKET`, `KC_SEMICOLON`, `KC_APOSTROPHE`, `KC_GRAVE`, `KC_BACKSLASH`, `KC_COMMA`, `KC_PERIOD`, `KC_SLASH` |

"Through" above lists names, not a contiguous numeric range. `KeyCode` follows the
classic DirectInput scan-code order, so the values are **not** sequential in the way the
names suggest: `KC_F11` and `KC_F12` sit far after `KC_F10`, and the numpad block runs
`7, 8, 9, SUBTRACT, 4, 5, 6, ADD, 1, 2, 3, 0`. Never loop over a key range with
`for (int k = KeyCode.KC_F1; k <= KeyCode.KC_F12; k++)`; name the constants you want.

### MouseState Enum

For raw mouse button state checking (not through the UAInput system):

```c
enum MouseState
{
    LEFT,
    RIGHT,
    MIDDLE,
    X,        // Horizontal axis
    Y,        // Vertical axis
    WHEEL     // Scroll wheel
};

// Usage: the documented test for "button is currently down"
if (GetMouseState(MouseState.LEFT) & MB_PRESSED_MASK)
{
    // Left mouse button is pressed
}
```

`GetMouseState()` returns a combination of press/release edge counts and the
`MB_PRESSED_MASK` flag. The engine header documents the mask idiom above but does
*not* publish the mask's numeric value --- its `const int MB_PRESSED_MASK`
declaration is commented out in `1_Core/proto/ensystem.c` and the value is supplied
by the engine. Do not hardcode a bit index: vanilla's own
`3_Game/tools/tools.c` tests `GetMouseState(MouseState.LEFT) & 0x80000000`, while
`4_World/classes/weapondebug.c` and `5_Mission/gui/scriptconsoleweathertab.c` use the
named `MB_PRESSED_MASK` constant. Use the named constant.

### Low-Level Key State

```c
// Raw key state. Engine doc (1_Core/proto/ensystem.c):
//   0         = not pressed
//   bit 15    = set while the key is down
//   bits 0-14 = number of press edges since the last read
int state = KeyState(KeyCode.KC_LSHIFT);

// Clear the key state (prevents auto-repeat until next physical press)
ClearKey(KeyCode.KC_RETURN);

// Disable a key for the rest of this frame
GetGame().GetInput().DisableKey(KeyCode.KC_RETURN);
```

Because the low bits carry an edge count, a non-zero return does **not** on its own
mean "the key is down right now". Vanilla is inconsistent here: `pluginkeybinding.c`
and `weapondebug.c` compare against `1`, while `scriptconsoletabbase.c` and
`scriptconsolecameratab.c` treat any non-zero value as pressed. If you specifically
need "currently held", test the documented pressed bit rather than `!= 0`.

---

## Suppressing and Disabling Inputs

### Suppress (Per-Input, One Frame)

Suppresses the input's press event. The engine header (`3_Game/inputapi/uainput.c`)
documents it as "supress press event for next frame (while not pressed ATM ---
otherwise until release)": if the bound key is *not* currently held, the suppression
lasts one frame; if it *is* held, the input stays suppressed until the player
releases it. Useful during transitions (closing a menu) to prevent input bleed:

```c
UAInput input = GetUApi().GetInputByName("UAMyAction");
input.Supress();  // Note: single 's' in the method name
```

### Suppress All Inputs (Global, One Frame)

Suppresses inputs for the next frame --- and, per the engine header comment, until a
held key is released. The header's own guidance is to "call this when leaving main menu
and alike --- to avoid button collision after character control returned":

```c
GetUApi().SupressNextFrame(true);
```

Vanilla calls it from `MissionGameplay.RemoveActiveInputExcludes()`, passing that
method's `bForceSupress` argument straight through.

### ForceDisable (Per-Input, Persistent)

Completely disables a specific input until re-enabled. The input will not fire any events while disabled:

```c
// Disable while menu is open
GetUApi().GetInputByName("UAMyAction").ForceDisable(true);

// Re-enable when menu closes
GetUApi().GetInputByName("UAMyAction").ForceDisable(false);
```

### Lock / Unlock (Per-Input, Persistent)

Similar to ForceDisable but uses a different mechanism. Be cautious --- if multiple systems lock/unlock the same input, they can interfere with each other:

```c
UAInput input = GetUApi().GetInputByName("UAMyAction");
input.Lock();    // Disable until Unlock() is called
input.Unlock();  // Re-enable

bool locked = input.IsLocked();  // Check state
```

A comment directly above these methods in `3_Game/inputapi/uainput.c` warns: "take care
when using these locking methods, if two or more systems un/lock the same input, there is
a chance off cross-un/locking it from a wrong place! Use exclude groups instead."

`UAInput` also exposes `ForceEnable(bool bEnable)` alongside `ForceDisable(bool bEnable)`.
Vanilla uses it in **both** directions on the same input: `MissionGameplay` calls
`GetUApi().GetInputByID(UAWalkRunForced).ForceEnable(true)` when it *applies* the inventory
and map input restrictions (`missiongameplay.c:1010`, `1022`), and `ForceEnable(false)` when
it lifts them (`missiongameplay.c:951`, `956`). `MissionServer` mirrors the same pair at
`missionserver.c:874`/`879` and `933`/`945`. The boolean is the forced state you want, not an
enable/clear toggle.

### ForceDisable All Inputs (Bulk)

When opening a full-screen UI, disable all game inputs except the ones your UI needs. This is the standard pattern in admin and menu mods:

```c
void DisableAllInputs(bool state)
{
    TIntArray inputIDs = new TIntArray;
    GetUApi().GetActiveInputs(inputIDs);

    // Inputs to keep active even while UI is open
    TIntArray skipIDs = new TIntArray;
    skipIDs.Insert(GetUApi().GetInputByName("UAUIBack").ID());

    foreach (int inputID : inputIDs)
    {
        if (skipIDs.Find(inputID) == -1)
        {
            GetUApi().GetInputByID(inputID).ForceDisable(state);
        }
    }

    GetUApi().UpdateControls();
}
```

**Important:** Call `GetUApi().UpdateControls()` after modifying input states in bulk. The
engine header documents this as the flush to call *"on each change of exclusion"*
(`uainput.c:197`), and every vanilla call site follows an exclusion or restriction change
(`missionbase.c:50`, `missiongameplay.c:1055`/`1077`, `missionserver.c:978`/`1000`,
`plugindayzinfecteddebug.c:169`/`184`). Community code applies the same call after bulk
`ForceDisable()` changes; note that `ForceDisable()` has **no call site anywhere in the
vanilla scripts** --- only its declaration at `uainput.c:84` --- so vanilla never
demonstrates that pairing, and the flush is a defensive convention here rather than a
documented requirement.

### Input Exclude Groups

The mission system activates named exclude groups. In the supplied extraction the
vanilla groups are declared in `bin/specific.xml` (root element `<inputs>`), which
defines `gestures`, `hotkey`, `aiming`, `movement`, `stances`, `optics`, `actions`,
`actionslite`, `inventory`, `inspect`, `menu`, `map`, `gamepaddisconnect`,
`radialmenu`, `loopedactions`, `vehicledriving`, `swimming`, `ladderclimbing`,
`actonViewOpticExcl` and `sprintExcl`. When activated, a group disables every input
listed inside it:

```c
// Suppress gameplay inputs while a menu is open
GetGame().GetMission().AddActiveInputExcludes({"menu"});

// Restore inputs when closing
GetGame().GetMission().RemoveActiveInputExcludes({"menu"}, true);
```

Method signatures on the `Mission` class:

```c
void AddActiveInputExcludes(array<string> excludes);
void RemoveActiveInputExcludes(array<string> excludes, bool bForceSupress = false);
void EnableAllInputs(bool bForceSupress = false);
bool IsInputExcludeActive(string exclude);
```

`MissionGameplay.RemoveActiveInputExcludes()` always ends with
`GetUApi().SupressNextFrame(bForceSupress)`, passing your argument through as the
`bForce` flag --- that is what prevents input bleed when the excludes are lifted.
`AddActiveInputExcludes()` and `RemoveActiveInputExcludes()` only queue the change and
call `RefreshExcludes()`; the queued groups are applied on the next mission update,
which re-runs `ActivateExclude()` for every active group and then `UpdateControls()`.

`ActivateExclude()` plus `UpdateControls()` can also be called directly, which is what
`PluginDayZInfectedDebug` does with the vanilla `"menu"` group:

```c
GetUApi().ActivateExclude("menu");
GetUApi().UpdateControls();
```

**Unverified:** whether a mod can *declare a new* exclude group of its own is not
demonstrated by any source checked for this chapter. Vanilla declares excludes only in
`bin/specific.xml`, and none of the mod input files inspected --- the official
`DayZ-Samples/Test_Inputs/my_new_inputs.xml`, Community Online Tools, or the DayZ
Expansion modules --- contains an `<exclude>` element; they use `<modded_inputs>` with
only `<actions>`, `<sorting>` and `<preset>`. Treat activating one of the vanilla group
names as the supported path, and test any custom group before relying on it. See
[Chapter 5.2: inputs.xml](../05-config-files/02-inputs-xml.md) for the file format.

---

## Linking inputs.xml to Script

The connection between the XML config layer and the script layer is the **action name string**.

```mermaid
flowchart LR
    A[Key Press] --> B[Engine Input Layer]
    B --> C[inputs.xml mapping]
    C --> D[UAInput object]
    D --> E{Query in OnUpdate}
    E -->|LocalPress| F[Single frame trigger]
    E -->|LocalHold| G[Continuous while held]
    E -->|LocalRelease| H[Single frame on release]
    E -->|LocalValue| I[Analog 0.0-1.0]
```

### The Flow

```
inputs.xml                              Script
──────────────                          ──────────────────────────────
<input name="UAMyModOpenMenu" />   -->  GetUApi().GetInputByName("UAMyModOpenMenu")
       │                                         │
       │  Engine loads at startup                │  Returns UAInput object
       │  Registers in UAInputAPI                │  with bound keys from XML
       ▼                                         ▼
Player sees in Settings > Controls       input.LocalPress() returns true
and can rebind the key                   when player hits the bound key
```

1. At startup, the engine reads all `inputs.xml` files from loaded mods
2. Each `<input name="...">` is registered as a `UAInput` in the global `UAInputAPI`
3. Default key bindings from `<preset>` are applied (unless the player has customized them)
4. In script, `GetUApi().GetInputByName("UAMyModOpenMenu")` retrieves the registered input
5. Calling `LocalPress()` etc. checks against whatever key the player has bound

The name string must match **exactly** (case-sensitive) between the XML and the script call.

For complete inputs.xml syntax, see [Chapter 5.2: inputs.xml](../05-config-files/02-inputs-xml.md).

### Runtime Registration (Advanced)

Inputs can also be registered at runtime from script, without an inputs.xml file:

```c
// Register a new group
GetUApi().RegisterGroup("mymod", "My Mod");

// Register a new input in that group
UAInput input = GetUApi().RegisterInput("UAMyModAction", "STR_MYMOD_ACTION", "mymod");

// Later, if needed:
GetUApi().DeRegisterInput("UAMyModAction");
GetUApi().DeRegisterGroup("mymod");
```

This is rarely used. The inputs.xml approach is preferred because it integrates properly with the Controls settings menu and preset system.

---

## Common Patterns

### Toggle Panel Open/Close

```c
modded class MissionGameplay
{
    protected bool m_MyPanelOpen;

    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);

        if (!GetGame().GetPlayer())
            return;

        UAInput input = GetUApi().GetInputByName("UAMyModPanel");
        if (input && input.LocalPress())
        {
            if (m_MyPanelOpen)
                CloseMyPanel();
            else
                OpenMyPanel();
        }
    }

    void OpenMyPanel()
    {
        m_MyPanelOpen = true;
        // Show UI...

        // Disable gameplay inputs while panel is open
        GetGame().GetMission().AddActiveInputExcludes({"menu"});
    }

    void CloseMyPanel()
    {
        m_MyPanelOpen = false;
        // Hide UI...

        // Restore gameplay inputs
        GetGame().GetMission().RemoveActiveInputExcludes({"menu"}, true);
    }
}
```

### Hold-to-Activate, Release-to-Deactivate

```c
override void OnUpdate(float timeslice)
{
    super.OnUpdate(timeslice);

    Input input = GetGame().GetInput();

    if (input.LocalPress("UAMyModSprint", false))
    {
        StartSprinting();
    }

    if (input.LocalRelease("UAMyModSprint", false))
    {
        StopSprinting();
    }
}
```

### Modifier + Key Combo Check

If you defined a Ctrl+Key combo in inputs.xml, the UAInput system handles it automatically. But if you need to check modifier state manually alongside a UAInput:

```c
override void OnUpdate(float timeslice)
{
    super.OnUpdate(timeslice);

    UAInput input = GetUApi().GetInputByName("UAMyModAction");
    if (input && input.LocalPress())
    {
        // Check if Shift is held via raw KeyState.
        // Bit 15 is the "currently down" flag; bits 0-14 are an edge count,
        // so mask rather than testing != 0.
        bool shiftHeld = (KeyState(KeyCode.KC_LSHIFT) & 0x8000) != 0;

        if (shiftHeld)
            PerformAlternateAction();
        else
            PerformNormalAction();
    }
}
```

### Suppress Input When UI Consumes It

When your UI handles a key press, suppress the underlying game action to prevent both from firing:

```c
class MyMenuHandler extends ScriptedWidgetEventHandler
{
    override bool OnClick(Widget w, int x, int y, int button)
    {
        if (w == m_ConfirmButton)
        {
            DoConfirm();

            // Suppress the game input that might share this key
            GetUApi().GetInputByName("UAFire").Supress();
            return true;
        }
        return false;
    }
}
```

### Getting the Display Name of a Bound Key

To show the player what key is bound to an action (for UI prompts):

```c
UAInput input = GetUApi().GetInputByName("UAMyModAction");
string keyName = InputUtils.GetButtonNameFromInput("UAMyModAction", EUAINPUT_DEVICE_KEYBOARDMOUSE);
// Returns localized key name like "F5", "Left Ctrl", etc.
```

For controller icons and rich-text formatting:

```c
string richText = InputUtils.GetRichtextButtonIconFromInputAction("UAMyModAction", "Open Menu", EUAINPUT_DEVICE_CONTROLLER);
// Returns image tag + label for UI display
```

---

## Game Focus

The `Input` class provides game focus management, which controls whether inputs are processed when the game window is not focused:

```c
Input input = GetGame().GetInput();

// Add to focus counter (positive = unfocused, inputs suppressed)
input.ChangeGameFocus(1);

// Remove from focus counter
input.ChangeGameFocus(-1);

// Reset focus counter to 0 (fully focused)
input.ResetGameFocus();

// Check if game currently has focus (counter == 0)
bool hasFocus = input.HasGameFocus();
```

This is a reference-counted system. Multiple systems can request focus changes, and inputs resume only when all of them release.

All three methods take an optional trailing device argument ---
`ChangeGameFocus(int add, int input_device = -1)`,
`ResetGameFocus(int input_device = -1)` and `HasGameFocus(int input_device = -1)`.
The default `-1` acts globally across every device; pass an `INPUT_DEVICE_*` value to scope
the call to a single device.

The doc comments on those methods point at an engine-side `constants.h`, but you do not need
it: the constants are **declared in script, with values**, at
`scripts/1_core/constants.c:23-29`.

| Constant | Value |
|---|---|
| `INPUT_DEVICE_KEYBOARD` | `0x00000000` |
| `INPUT_DEVICE_MOUSE` | `0x00100000` |
| `INPUT_DEVICE_STICK` | `0x00200000` |
| `INPUT_DEVICE_XINPUT` | `0x00300000` |
| `INPUT_DEVICE_TRACKIR` | `0x00400000` |
| `INPUT_DEVICE_GAMEPAD` | `0x00500000` |
| `INPUT_DEVICE_CHEAT` | `0x00600000` |

Do not confuse these with `EUAINPUT_DEVICE_*`, which is a different set: it appears in the
extraction only as commented-out names at `scripts/3_game/inputapi/uainput.c:7-11` and is
genuinely engine-supplied, with no script-side values.

---

## Common Mistakes

### Polling Input on the Server

Inputs are **client-only**. The server has no concept of keyboard, mouse, or gamepad state. If you call `GetUApi().GetInputByName()` on the server, the result is meaningless.

```c
// WRONG --- this runs on the server, inputs do not exist here
modded class MissionServer
{
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);
        UAInput input = GetUApi().GetInputByName("UAMyAction");
        if (input.LocalPress())  // Always false on server!
        {
            DoSomething();
        }
    }
}

// CORRECT --- check input on client, send RPC to server
modded class MissionGameplay  // Client-side mission class
{
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);
        UAInput input = GetUApi().GetInputByName("UAMyAction");
        if (input && input.LocalPress())
        {
            // Send RPC to server to perform the action
            GetGame().RPCSingleParam(null, MY_RPC_ID, null, true);
        }
    }
}
```

### Using OnKeyPress for Player-Facing Actions

```c
// WRONG --- hardcoded key, player cannot rebind
override void OnKeyPress(int key)
{
    super.OnKeyPress(key);
    if (key == KeyCode.KC_Y)
        OpenMyMenu();
}

// CORRECT --- uses inputs.xml, player can rebind in Settings
override void OnUpdate(float timeslice)
{
    super.OnUpdate(timeslice);
    UAInput input = GetUApi().GetInputByName("UAMyModOpenMenu");
    if (input && input.LocalPress())
        OpenMyMenu();
}
```

### Not Suppressing Input When UI Is Open

When your mod opens a UI panel, the player's WASD keys will still move the character, the mouse will still aim, and clicking will fire the weapon --- unless you disable game inputs:

```c
// WRONG --- character walks around behind the menu
void OpenMenu()
{
    m_MenuWidget.Show(true);
}

// CORRECT --- disable movement while menu is open
void OpenMenu()
{
    m_MenuWidget.Show(true);
    GetGame().GetMission().AddActiveInputExcludes({"menu"});
    GetGame().GetUIManager().ShowCursor(true);
}

void CloseMenu()
{
    m_MenuWidget.Show(false);
    GetGame().GetMission().RemoveActiveInputExcludes({"menu"}, true);
    GetGame().GetUIManager().ShowCursor(false);
}
```

### Forgetting That LocalPress Fires Only ONE Frame

`LocalPress()` returns `true` for exactly one frame --- the frame the key transitions from released to pressed. If your code path does not execute on that exact frame, you miss the event.

```c
// WRONG --- if DoExpensiveCheck() takes time or skips frames, you miss the press
void SomeCallback()
{
    if (GetUApi().GetInputByName("UAMyAction").LocalPress())
    {
        // This might never fire if SomeCallback is not called every frame
    }
}

// CORRECT --- always check in a per-frame callback
override void OnUpdate(float timeslice)
{
    super.OnUpdate(timeslice);
    if (GetUApi().GetInputByName("UAMyAction").LocalPress())
    {
        DoAction();
    }
}
```

### Confusing LocalClick and LocalPress

`LocalClick()` is NOT the same as `LocalPress()`. `LocalClick()` fires when a key is pressed AND released quickly (before the hold threshold). `LocalPress()` fires immediately on key-down. Most mods want `LocalPress()`.

```c
// Might not fire if player holds the key too long
if (input.LocalClick())  // Requires quick tap

// Fires immediately on key-down, regardless of hold duration
if (input.LocalPress())  // Usually what you want
```

### Forgetting UpdateControls After Bulk Changes

When you `ForceDisable()` multiple inputs, you must call `UpdateControls()` for the changes to take effect:

```c
// WRONG --- changes may not apply immediately
GetUApi().GetInputByName("UAFire").ForceDisable(true);
GetUApi().GetInputByName("UAMoveForward").ForceDisable(true);

// CORRECT --- flush the changes
GetUApi().GetInputByName("UAFire").ForceDisable(true);
GetUApi().GetInputByName("UAMoveForward").ForceDisable(true);
GetUApi().UpdateControls();
```

### Misspelling Supress

The engine method is `Supress()` with a single 's' (not `Suppress`). The global method `SupressNextFrame()` also uses a single 's'. This is a quirk of the engine API:

```c
// WRONG --- will not compile
input.Suppress();

// CORRECT --- single 's'
input.Supress();
GetUApi().SupressNextFrame(true);
```

---

## Quick Reference

```c
// === Getting inputs ===
UAInputAPI api = GetUApi();
UAInput input = api.GetInputByName("UAMyAction");
Input rawInput = GetGame().GetInput();

// === State queries (UAInput) ===
input.LocalPress()        // Key just went down (one frame)
input.LocalRelease()      // Key just came up (one frame)
input.LocalClick()        // Quick tap detected
input.LocalHoldBegin()    // Hold threshold just reached (one frame)
input.LocalHold()         // Held past threshold (every frame)
input.LocalDoubleClick()  // Double-tap detected
input.LocalValue()        // Analog value (float)

// === State queries (Input, string-based) ===
rawInput.LocalPress("UAMyAction", false)
rawInput.LocalRelease("UAMyAction", false)
rawInput.LocalHold("UAMyAction", false)
rawInput.LocalDbl("UAMyAction", false)
rawInput.LocalValue("UAMyAction", false)

// === Suppressing ===
input.Supress()                    // This input, next frame
api.SupressNextFrame(true)         // All inputs, next frame

// === Disabling ===
input.ForceDisable(true)           // Disable persistently
input.ForceDisable(false)          // Re-enable
input.Lock()                       // Lock (use excludes instead)
input.Unlock()                     // Unlock
api.UpdateControls()               // Flush changes

// === Exclude groups ===
GetGame().GetMission().AddActiveInputExcludes({"menu"});
GetGame().GetMission().RemoveActiveInputExcludes({"menu"}, true);
GetGame().GetMission().EnableAllInputs(true);

// === Raw key state ===
int state = KeyState(KeyCode.KC_LSHIFT);
GetGame().GetInput().DisableKey(KeyCode.KC_RETURN);

// === Display helpers ===
string name = InputUtils.GetButtonNameFromInput("UAMyAction", EUAINPUT_DEVICE_KEYBOARDMOUSE);
```

---

*This chapter covers the script-side Input System API. For the XML configuration that registers keybindings, see [Chapter 5.2: inputs.xml](../05-config-files/02-inputs-xml.md).*

---

## Best Practices

- **Always use `UAInput` via inputs.xml for player-facing keybindings.** This allows players to rebind keys, shows actions in the Controls menu, and supports gamepad input. Reserve `OnKeyPress` for debug shortcuts only.
- **Call `AddActiveInputExcludes({"menu"})` when opening full-screen UI.** Without this, player movement keys (WASD), mouse aiming, and weapon firing remain active behind your menu, causing accidental actions.
- **Check inputs only in per-frame callbacks like `OnUpdate()`.** `LocalPress()` returns true for exactly one frame. Checking it in event handlers or callbacks that do not run every frame will miss key presses.
- **Call `GetUApi().UpdateControls()` after bulk `ForceDisable()` changes.** The header
  documents `UpdateControls()` as the flush to call on each change of *exclusion*
  (`uainput.c:197`), and that is the only mechanism vanilla states. No vanilla call site pairs
  it with `ForceDisable()` --- that method has zero call sites in the extracted scripts --- so
  treat the pairing as a community convention, not as documented engine timing behaviour.
- **Remember that `Supress()` uses a single "s".** The engine API spells it `Supress()` and `SupressNextFrame()`. Using the correct English spelling `Suppress` will not compile.

---

## Compatibility & Impact

- **Multi-Mod:** Input action names are global. Two mods registering the same `UAInput` name (e.g., `"UAOpenMenu"`) will collide. Always prefix with your mod name: `"UAMyModOpenMenu"`. Input exclude groups are shared -- one mod activating `"menu"` excludes affects all mods.
- **Performance:** `GetInputByName()` is a `proto native` call whose implementation lives in the engine, so its cost cannot be read from the script dump --- treat "it is just a hash lookup" as folklore rather than fact; no measurement was made for this chapter. What the headers *do* show is a supported way to avoid repeated by-name lookups: `UAInput.GetPersistentWrapper()` returns a `UAIDWrapper` whose `InputP()` resolves back to the input, which is the engine's own idiom for holding on to an input across frames.
- **Server/Client:** Inputs exist only on the client. The server has no keyboard, mouse, or gamepad state. Always detect input on the client and send RPCs to the server for authoritative actions.
