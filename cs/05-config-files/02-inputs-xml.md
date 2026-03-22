# Chapter 5.2: inputs.xml --- Custom Keybindings

[Domů](../../README.md) | [<< Předchozí: stringtable.csv](01-stringtable.md) | **inputs.xml** | [Další: Credits.json >>](03-credits-json.md)

---

> **Shrnutí:** The `inputs.xml` file lets your mod register vlastní keybindings that appear in hráč's Controls settings menu. Players can view, rebind, and toggle these inputs jen like vanilla actions. Toto je standard mechanism for adding hotkeys to DayZ mods.

---

## Obsah

- [Overview](#overview)
- [File Location](#file-location)
- [Complete XML Structure](#complete-xml-structure)
- [Actions Block](#actions-block)
- [Sorting Block](#sorting-block)
- [Preset Block (Default Keybindings)](#preset-block-výchozí-keybindings)
- [Modifier Combos](#modifier-combos)
- [Hidden Inputs](#hidden-inputs)
- [Multiple Default Keys](#multiple-výchozí-keys)
- [Accessing Inputs in Script](#accessing-inputs-in-script)
- [Input Methods Reference](#input-methods-reference)
- [Suppressing and Disabling Inputs](#suppressing-and-disabling-inputs)
- [Key Names Reference](#key-names-reference)
- [Real Examples](#real-examples)
- [Běžné Mistakes](#common-mistakes)

---

## Přehled

When your mod needs hráč to press a key --- opening a menu, toggling a feature, commanding an AI unit --- you register a vlastní input action in `inputs.xml`. Engine reads tento soubor při startu and integrates your actions into the universal input system. Players viz your keybindings in the game's Settings > Controls menu, grouped under a heading you define.

Custom inputs are identified by a unique action name (conventionally prefixed with `UA` for "User Action") and can have výchozí keybindings that hráči can rebind at will.

---

## Umístění souboru

Place `inputs.xml` inside a `data` subfolder of your Scripts directory:

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

Some mods place it přímo in the `Scripts/` folder. Obě umístění fungují. Engine discovers soubor automatickýally --- no config.cpp registration is needed.

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

All three sections --- `<actions>`, `<sorting>`, and `<preset>` --- work together but serve odlišný purposes.

---

## Actions Block

The `<actions>` block declares každý input action your mod provides. Each action is a jeden `<input>` element.

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
| `loc` | No | Stringtable key for the display name in the Controls menu. **No `#` prefix** --- systém adds it. |
| `visible` | No | Nastavte to `"false"` to hide from the Controls menu. Defaults to `true`. |

### Naming Convention

Action names must be globálníly unique across all loaded mods. Use your mod prefix:

```xml
<input name="UAMyModAdminPanel" loc="STR_MYMOD_INPUT_ADMIN_PANEL" />
<input name="UAExpansionBookToggle" loc="STR_EXPANSION_BOOK_TOGGLE" />
<input name="eAICommandMenu" loc="STR_EXPANSION_AI_COMMAND_MENU" />
```

The `UA` prefix is conventional but not enforced. Expansion AI uses `eAI` as its prefix, which také works.

---

## Sorting Block

The `<sorting>` block controls how your inputs appear in hráč's Controls settings. It defines a named group (which becomes a section header) and lists the inputs in display order.

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

In the Controls settings, hráč sees:

```
[MyMod]                          <-- from the sorting loc
  Open Menu .............. [Y]   <-- from the input loc + preset
  Toggle HUD ............. [H]   <-- from the input loc + preset
```

Only inputs listed in the `<sorting>` block appear in the settings menu. Inputs defined in `<actions>` but not listed in `<sorting>` are tiše registered but invisible to hráč (even if `visible` is not explicitly set to `false`).

---

## Preset Block (Default Keybindings)

The `<preset>` block assigns výchozí keys to your actions. These are klíčs hráč starts with before jakýkoli vlastníization.

### Simple Key Binding

```xml
<preset>
    <input name="UAMyModOpenMenu">
        <btn name="kY"/>
    </input>
</preset>
```

This binds the `Y` key as the výchozí for `UAMyModOpenMenu`.

### No Default Key

Pokud omit an action from the `<preset>` block, it has no výchozí binding. The player must ručně assign a key in Settings > Controls. This is appropriate for volitelný or advanced bindings.

---

## Modifier Combos

To require a modifier key (Ctrl, Shift, Alt), nest `<btn>` elements:

### Ctrl + Left Mouse Button

```xml
<input name="eAISetWaypoint">
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

- The **outer** `<btn>` is vždy the modifier (held down)
- The **inner** `<btn>` is the trigger (pressed while modifier is held)
- Only one level of nesting is typical; deeper nesting is untested and not doporučený

---

## Hidden Inputs

Use `visible="false"` to register an input that hráč cannot viz or rebind in the Controls menu. This is užitečný for interní inputs used by your mod's code that should not be player-configurable.

```xml
<actions>
    <input name="eAITestInput" visible="false" />
    <input name="UAExpansionConfirm" loc="" visible="false" />
</actions>
```

Hidden inputs can stále have výchozí key assignments in the `<preset>` block:

```xml
<preset>
    <input name="eAITestInput">
        <btn name="kY"/>
    </input>
</preset>
```

---

## Multiple Default Keys

An action can have více výchozí keys. List více `<btn>` elements as siblings:

```xml
<input name="UAExpansionConfirm">
    <btn name="kReturn" />
    <btn name="kNumpadEnter" />
</input>
```

Oba `Enter` and `Numpad Enter` will trigger `UAExpansionConfirm`. This is užitečný for actions where více physical keys should map to the stejný logical action.

---

## Accessing Inputs in Script

### Getting the Input API

All input access goes through `GetUApi()`, which vrací globální User Action API:

```c
UAInput input = GetUApi().GetInputByName("UAMyModOpenMenu");
```

### Polling in OnUpdate

Custom inputs are typicky polled in `MissionGameplay.OnUpdate()` or similar per-frame zpětné volánís:

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

Many mods check inputs inline using the `UAInputAPI` methods with string names:

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

The `false` parameter in `LocalPress("name", false)` indicates that the check should not consume the input dokoncet.

---

## Input Methods Reference

Once you have a `UAInput` reference (from `GetUApi().GetInputByName()`), or are using the `Input` class přímo, these methods detect odlišný input states:

| Method | Returns | When True |
|--------|---------|-----------|
| `LocalPress()` | `bool` | The key was pressed **this frame** (single trigger on key-down) |
| `LocalRelease()` | `bool` | The key was released **this frame** (single trigger on key-up) |
| `LocalClick()` | `bool` | The key was pressed and released quickly (tap) |
| `LocalHold()` | `bool` | The key has been held down for a threshold duration |
| `LocalDoubleClick()` | `bool` | The key was tapped twice quickly |
| `LocalValue()` | `float` | Current analog value (0.0 or 1.0 for digital keys; variable for analog axes) |

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
if (input.LocalPress("eAICommandMenu", false))
{
    ShowCommandWheel();
}

if (input.LocalRelease("eAICommandMenu", false) || input.LocalValue("eAICommandMenu", false) == 0)
{
    HideCommandWheel();
}
```

**Double-tap action:**
```c
if (input.LocalDoubleClick("UAMyModSpecial", false))
{
    PerformSpecialAction();
}
```

**Hold for extended action:**
```c
if (input.LocalHold("UAExpansionGPSToggle"))
{
    ToggleGPSMode();
}
```

---

## Suppressing and Disabling Inputs

### ForceDisable

Temporarily disables a specifický input. Commonly used when opening menus to prevent game actions from firing while a UI is active:

```c
// Disable the input while menu is open
GetUApi().GetInputByName("UAMyModToggle").ForceDisable(true);

// Re-enable when menu closes
GetUApi().GetInputByName("UAMyModToggle").ForceDisable(false);
```

### SupressNextFrame

Suppresses all input processing for the next frame. Used during input context transitions (e.g., closing menus) to prevent one-frame input bleed:

```c
GetUApi().SupressNextFrame(true);
```

### UpdateControls

Po modifying input states, call `UpdateControls()` to apply changes okamžitě:

```c
GetUApi().GetInputByName("UAExpansionBookToggle").ForceDisable(false);
GetUApi().UpdateControls();
```

### Input Excludes

The vanilla mission system provides exclude groups. Když menu is active, můžete exclude categories of inputs:

```c
// Suppress gameplay inputs while inventory is open
AddActiveInputExcludes({"inventory"});

// Restore when closing
RemoveActiveInputExcludes({"inventory"});
```

---

## Key Names Reference

Key names used in the `<btn name="">` attribute follow a specifický naming convention. Here is the complete reference.

### Keyboard Keys

| Category | Key Names |
|----------|-----------|
| Letters | `kA`, `kB`, `kC`, `kD`, `kE`, `kF`, `kG`, `kH`, `kI`, `kJ`, `kK`, `kL`, `kM`, `kN`, `kO`, `kP`, `kQ`, `kR`, `kS`, `kT`, `kU`, `kV`, `kW`, `kX`, `kY`, `kZ` |
| Numbers (top row) | `k0`, `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9` |
| Function keys | `kF1`, `kF2`, `kF3`, `kF4`, `kF5`, `kF6`, `kF7`, `kF8`, `kF9`, `kF10`, `kF11`, `kF12` |
| Modifiers | `kLControl`, `kRControl`, `kLShift`, `kRShift`, `kLAlt`, `kRAlt` |
| Navigation | `kUp`, `kDown`, `kLeft`, `kRight`, `kHome`, `kEnd`, `kPageUp`, `kPageDown` |
| Editing | `kReturn`, `kBackspace`, `kDelete`, `kInsert`, `kSpace`, `kTab`, `kEscape` |
| Numpad | `kNumpad0` ... `kNumpad9`, `kNumpadEnter`, `kNumpadPlus`, `kNumpadMinus`, `kNumpadMultiply`, `kNumpadDivide`, `kNumpadDecimal` |
| Punctuation | `kMinus`, `kEquals`, `kLBracket`, `kRBracket`, `kBackslash`, `kSemicolon`, `kApostrophe`, `kComma`, `kPeriod`, `kSlash`, `kGrave` |
| Locks | `kCapsLock`, `kNumLock`, `kScrollLock` |

### Mouse Buttons

| Name | Button |
|------|--------|
| `mBLeft` | Left mouse button |
| `mBRight` | Right mouse button |
| `mBMiddle` | Middle mouse button (scroll wheel click) |
| `mBExtra1` | Mouse button 4 (side button back) |
| `mBExtra2` | Mouse button 5 (side button forward) |

### Mouse Axes

| Name | Axis |
|------|------|
| `mAxisX` | Mouse horizontal movement |
| `mAxisY` | Mouse vertical movement |
| `mWheelUp` | Scroll wheel up |
| `mWheelDown` | Scroll wheel down |

### Naming Pattern

- **Keyboard**: `k` prefix + key name (e.g., `kT`, `kF5`, `kLControl`)
- **Mouse buttons**: `mB` prefix + button name (e.g., `mBLeft`, `mBRight`)
- **Mouse axes**: `m` prefix + axis name (e.g., `mAxisX`, `mWheelUp`)

---

## Reálné příklady

### DayZ Expansion AI

A well-structured inputs.xml with visible keybindings, hidden debug inputs, and modifier combos:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="eAICommandMenu" loc="STR_EXPANSION_AI_COMMAND_MENU"/>
            <input name="eAISetWaypoint" loc="STR_EXPANSION_AI_SET_WAYPOINT"/>
            <input name="eAITestInput" visible="false" />
            <input name="eAITestLRIncrease" visible="false" />
            <input name="eAITestLRDecrease" visible="false" />
            <input name="eAITestUDIncrease" visible="false" />
            <input name="eAITestUDDecrease" visible="false" />
        </actions>

        <sorting name="expansion" loc="STR_EXPANSION_LABEL">
            <input name="eAICommandMenu" />
            <input name="eAISetWaypoint" />
            <input name="eAITestInput" />
            <input name="eAITestLRIncrease" />
            <input name="eAITestLRDecrease" />
            <input name="eAITestUDIncrease" />
            <input name="eAITestUDDecrease" />
        </sorting>
    </inputs>
    <preset>
        <input name="eAICommandMenu">
            <btn name="kT"/>
        </input>
        <input name="eAISetWaypoint">
            <btn name="kLControl">
                <btn name="mBLeft"/>
            </btn>
        </input>
        <input name="eAITestInput">
            <btn name="kY"/>
        </input>
        <input name="eAITestLRIncrease">
            <btn name="kRight"/>
        </input>
        <input name="eAITestLRDecrease">
            <btn name="kLeft"/>
        </input>
        <input name="eAITestUDIncrease">
            <btn name="kUp"/>
        </input>
        <input name="eAITestUDDecrease">
            <btn name="kDown"/>
        </input>
    </preset>
</modded_inputs>
```

Key observations:
- `eAICommandMenu` bound to `T` --- visible in settings, player can rebind
- `eAISetWaypoint` uses a **Ctrl + Left Click** modifier combo
- Testujte inputs are `visible="false"` --- hidden from hráči but accessible in code

### DayZ Expansion Market

A minimal inputs.xml for a hidden utility input with více výchozí keys:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="UAExpansionConfirm" loc="" visible="false" />
        </actions>
    </inputs>
    <preset>
        <input name="UAExpansionConfirm">
            <btn name="kReturn" />
            <btn name="kNumpadEnter" />
        </input>
    </preset>
</modded_inputs>
```

Key observations:
- Hidden input (`visible="false"`) with prázdný `loc` --- nikdy shown in settings
- Two výchozí keys: oba Enter and Numpad Enter trigger the stejný action
- No `<sorting>` block --- not needed since the input is hidden

### Complete Starter Template

A minimal but complete template for a nový mod:

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

## Časté chyby

### Using `#` in the loc Attribute

```xml
<!-- WRONG -->
<input name="UAMyAction" loc="#STR_MYMOD_ACTION" />

<!-- CORRECT -->
<input name="UAMyAction" loc="STR_MYMOD_ACTION" />
```

The input system prepends `#` interníly. Adding it yourself causes a double-prefix and the lookup fails.

### Action Name Collisions

Pokud dva mods define `UAOpenMenu`, pouze one will work. Vždy use your mod prefix:

```xml
<input name="UAMyModOpenMenu" />     <!-- Good -->
<input name="UAOpenMenu" />          <!-- Risky -->
```

### Missing Sorting Entry

Pokud define an action in `<actions>` but forget to list it in `<sorting>`, the action works in code but is invisible in the Controls menu. The player has no way to rebind it.

### Forgetting to Define in Actions

Pokud list an input in `<sorting>` or `<preset>` but nikdy define it in `<actions>`, engine tiše ignores it.

### Binding Conflicting Keys

Choosing keys that conflict with vanilla bindings (like `W`, `A`, `S`, `D`, `Tab`, `I`) causes oba your action and the vanilla action to fire současně. Use less common keys (F5-F12, numpad keys) or modifier combos for safety.

---

## Osvědčené postupy

- Vždy prefix action names with `UA` + your mod name (e.g., `UAMyModOpenMenu`). Generic names like `UAOpenMenu` will collide with jiný mods.
- Provide a `loc` attribute for každý visible input and define the corresponding stringtable key. Bez it, the Controls menu shows the raw action name.
- Choose uncommon výchozí keys (F5-F12, numpad) or modifier combos (Ctrl+key) to minimize conflicts with vanilla and popular mod keybindings.
- Vždy list visible inputs in the `<sorting>` block. An input defined in `<actions>` but chybějící from `<sorting>` is invisible to hráč and nemůže být rebound.
- Cache the `UAInput` reference from `GetUApi().GetInputByName()` in a member variable spíše než calling it každý frame in `OnUpdate`. The string lookup has overhead.

---

## Teorie vs praxe

> What the documentation says versus how things actually work za běhu.

| Concept | Theory | Reality |
|---------|--------|---------|
| `visible="false"` hides from Controls menu | Input is registered but invisible | Hidden inputs stále appear in the `<sorting>` block listing in některé DayZ versions. Omitting from `<sorting>` is the reliable way to hide inputs |
| `LocalPress()` fires once per key-down | Single trigger on the frame klíč is pressed | Pokud game hitches (low FPS), `LocalPress()` can be missed celýly. For critical actions, také check `LocalValue() > 0` as a fallback |
| Modifier combos via nested `<btn>` | Outer is modifier, inner is trigger | The modifier key alone také registers as a press on its own input (e.g., `kLControl` is také vanilla crouch). Players holding Ctrl+Klikněte will také crouch |
| `ForceDisable(true)` suppresses input | Input is zcela ignored | `ForceDisable` persists until explicitly re-enabled. Pokud váš mod crashes or the UI closes without calling `ForceDisable(false)`, the input stays disabled until game restart |
| Multiple `<btn>` siblings | Oba keys trigger the stejný action | Works správně, but the Controls menu pouze displays the first key. The player can viz and rebind the first key but may not realize the second výchozí exists |

---

## Kompatibilita a dopad

- **Více modů:** Action name collisions are the primary risk. Pokud dva mods define `UAOpenMenu`, pouze one works and the conflict is silent. There is no engine warning for duplicate action names across mods.
- **Výkon:** Input polling via `GetUApi().GetInputByName()` involves řetězec hash lookup. Polling 5-10 inputs per frame is negligible, but caching the `UAInput` reference is stále doporučený for mods with mnoho inputs.
- **Verze:** The `inputs.xml` format and `<modded_inputs>` structure have been stable since DayZ 1.0. The `visible` attribute was added later (around 1.08) -- on older versions, all inputs are vždy visible in the Controls menu.

---

## Pozorováno v reálných modech

| Vzor | Mod | Detail |
|---------|-----|--------|
| Modifier combo `Ctrl+Click` | Expansion AI | `eAISetWaypoint` uses nested `<btn name="kLControl"><btn name="mBLeft"/>` for Ctrl+Left Klikněte to place AI waypoints |
| Hidden utility inputs | Expansion Market | `UAExpansionConfirm` is `visible="false"` with dual keys (Enter + Numpad Enter) for interní confirmation logic |
| `ForceDisable` during menu open | COT, VPP | Admin panels call `ForceDisable(true)` on gameplay inputs when the panel opens, and `ForceDisable(false)` on close to prevent character movement while typing |
| Cached `UAInput` in member variable | DabsFramework | Stores `GetUApi().GetInputByName()` result in a class field during init, polls the cached reference in `OnUpdate` to avoid per-frame string lookup |
