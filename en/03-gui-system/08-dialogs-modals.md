# Dialogs & Modals

> **Summary:** Dialogs are temporary overlay windows that demand user interaction -- confirmation prompts, alert messages, input forms, and settings panels. DayZ exposes four ways to build them; this chapter covers all four, their focus management, layout structure, and common pitfalls.

---

## Table of Contents

- [Modal vs. Modeless](#modal-vs-modeless)
- [The four dialog systems](#the-four-dialog-systems)
- [`UIScriptedMenu` -- the built-in menu stack](#uiscriptedmenu-the-built-in-system)
- [Built-in `ShowDialog` (native message boxes)](#built-in-showdialog-native-message-boxes)
- [Manual dialog pattern (`ScriptedWidgetEventHandler`)](#manual-dialog-pattern-without-uiscriptedmenu)
  - [Popup via `OnWidgetScriptInit`](#popup-via-onwidgetscriptinit)
- [Dialog layout structure](#dialog-layout-structure)
- [Confirmation dialog pattern](#confirmation-dialog-pattern)
- [Input dialog pattern](#input-dialog-pattern)
- [Focus management (the golden rule)](#focus-management)
- [Z-order and layering](#z-order-and-layering)
- [Common patterns](#common-patterns)
- [`UIScriptedWindow` -- floating windows](#uiscriptedwindow-floating-windows)
- [Common mistakes](#common-mistakes)
- [Summary](#summary)
- [Next Steps](#next-steps)

---

## Modal vs. Modeless

There are two fundamental types of dialog:

- **Modal** -- Blocks all interaction with content behind the dialog. The user must respond (confirm, cancel, close) before doing anything else. Examples: quit confirmation, delete warning, rename prompt.
- **Modeless** -- Allows the user to interact with content behind the dialog while it remains open. Examples: info panels, settings windows, tool palettes.

In DayZ, the distinction is controlled by whether you lock game input when the dialog opens. A modal dialog calls `ChangeGameFocus(1)` and shows the cursor; a modeless dialog may skip this or use a toggle approach.

---

## The four dialog systems

DayZ gives you four distinct ways to put a dialog on screen. Pick by how much control you need:

| System | Base | Focus handled for you? | Best for |
|--------|------|------------------------|----------|
| `UIScriptedMenu` | engine menu stack | Yes (`super.OnShow()`/`super.OnHide()`) | Full-screen menus and major dialogs |
| `ShowDialog()` | native message box | Yes | Simple Yes/No/OK prompts, no layout file |
| `ScriptedWidgetEventHandler` | raw widget tree | No -- you balance it yourself | In-panel popups, custom-styled dialogs |
| `UIScriptedWindow` | floating window | Via parent menu | Tool windows alongside an open menu |

The rest of this chapter walks through each, then covers the concerns they share: layout structure, focus management, and z-order.

---

## UIScriptedMenu -- The Built-in System

`UIScriptedMenu` is the engine-level base class for all menu screens in DayZ. It integrates with the `UIManager` menu stack, handles input locking automatically, and provides lifecycle hooks. Vanilla DayZ uses it for the in-game menu, logout dialog, respawn dialog, options menu, and many others.

### Class Hierarchy

```
UIMenuPanel          (base: menu stack, Close(), submenu management)
  UIScriptedMenu     (scripted menus: Init(), OnShow(), OnHide(), Update())
```

### Minimal UIScriptedMenu Dialog

```c
class MyDialog extends UIScriptedMenu
{
    protected ButtonWidget m_BtnConfirm;
    protected ButtonWidget m_BtnCancel;
    protected TextWidget   m_MessageText;

    override Widget Init()
    {
        layoutRoot = GetGame().GetWorkspace().CreateWidgets(
            "MyMod/GUI/layouts/my_dialog.layout");

        m_BtnConfirm  = ButtonWidget.Cast(
            layoutRoot.FindAnyWidget("BtnConfirm"));
        m_BtnCancel   = ButtonWidget.Cast(
            layoutRoot.FindAnyWidget("BtnCancel"));
        m_MessageText = TextWidget.Cast(
            layoutRoot.FindAnyWidget("MessageText"));

        return layoutRoot;
    }

    override void OnShow()
    {
        super.OnShow();
        // super.OnShow() calls LockControls() which handles:
        //   GetGame().GetInput().ChangeGameFocus(1);
        //   GetGame().GetUIManager().ShowUICursor(true);
    }

    override void OnHide()
    {
        super.OnHide();
        // super.OnHide() calls UnlockControls() which handles:
        //   GetGame().GetInput().ChangeGameFocus(-1);
        //   GetGame().GetUIManager().ShowUICursor(false);
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        super.OnClick(w, x, y, button);

        if (w == m_BtnConfirm)
        {
            // Do action
            Close();
            return true;
        }

        if (w == m_BtnCancel)
        {
            Close();
            return true;
        }

        return false;
    }

    override void Update(float timeslice)
    {
        super.Update(timeslice);

        // ESC to close
        if (GetUApi().GetInputByID(UAUIBack).LocalPress())
        {
            Close();
        }
    }
}
```

### Opening and Closing

```c
// Opening -- create the menu and push it onto the UIManager stack
MyDialog dialog = new MyDialog();
GetGame().GetUIManager().ShowScriptedMenu(dialog, null);

// Closing from outside
GetGame().GetUIManager().HideScriptedMenu(dialog);

// Closing from inside the dialog class
Close();
```

`ShowScriptedMenu()` pushes the menu onto the engine menu stack, triggers `Init()`, then `OnShow()`. `Close()` triggers `OnHide()`, pops it from the stack, and destroys the widget tree.

### Key Lifecycle Methods

| Method | When Called | Typical Use |
|--------|------------|-------------|
| `Init()` | Once, when menu is created | Create widgets, cache references |
| `OnShow()` | After menu becomes visible | Lock input, start timers |
| `OnHide()` | After menu is hidden | Unlock input, cancel timers |
| `Update(float timeslice)` | Every frame while visible | Poll input (ESC key), animations |
| `Cleanup()` | Before destruction | Release resources |

### LockControls / UnlockControls

`UIScriptedMenu` provides built-in methods that `OnShow()` and `OnHide()` call automatically:

```c
// Inside UIScriptedMenu (engine code, simplified):
void LockControls()
{
    g_Game.GetInput().ChangeGameFocus(1, INPUT_DEVICE_MOUSE);
    g_Game.GetUIManager().ShowUICursor(true);
    g_Game.GetInput().ChangeGameFocus(1, INPUT_DEVICE_KEYBOARD);
    g_Game.GetInput().ChangeGameFocus(1, INPUT_DEVICE_GAMEPAD);
}

void UnlockControls()
{
    g_Game.GetInput().ChangeGameFocus(-1, INPUT_DEVICE_MOUSE);
    g_Game.GetInput().ChangeGameFocus(-1, INPUT_DEVICE_KEYBOARD);
    g_Game.GetInput().ChangeGameFocus(-1, INPUT_DEVICE_GAMEPAD);
    // Cursor visibility depends on whether a parent menu exists
}
```

Because `UIScriptedMenu` handles focus management automatically in `OnShow()`/`OnHide()`, you rarely need to call `ChangeGameFocus()` yourself when using this base class. Simply call `super.OnShow()` and `super.OnHide()`.

---

## Built-in ShowDialog (Native Message Boxes)

The engine provides a native dialog system for simple confirmation prompts. It renders a platform-appropriate dialog box without requiring any layout file.

### Usage

```c
// Show a Yes/No confirmation dialog
const int MY_DIALOG_ID = 500;

g_Game.GetUIManager().ShowDialog(
    "Confirm Action",                  // caption
    "Are you sure you want to do this?", // text
    MY_DIALOG_ID,                      // custom ID to identify this dialog
    DBT_YESNO,                         // button configuration
    DBB_YES,                           // default button
    DMT_QUESTION,                      // icon type
    this                               // handler (receives OnModalResult)
);
```

### Receiving the Result

The handler (the `UIScriptedMenu` passed as the last argument) receives the result through `OnModalResult`:

```c
override bool OnModalResult(Widget w, int x, int y, int code, int result)
{
    if (code == MY_DIALOG_ID)
    {
        if (result == DBB_YES)
        {
            PerformAction();
        }
        // DBB_NO means user declined -- do nothing
        return true;
    }

    return false;
}
```

### Constants

**Button configurations** (`DBT_` -- DialogBoxType):

| Constant | Buttons Shown |
|----------|---------------|
| `DBT_OK` | OK |
| `DBT_YESNO` | Yes, No |
| `DBT_YESNOCANCEL` | Yes, No, Cancel |

**Button identifiers** (`DBB_` -- DialogBoxButton):

| Constant | Value | Meaning |
|----------|-------|---------|
| `DBB_NONE` | 0 | No default |
| `DBB_OK` | 1 | OK button |
| `DBB_YES` | 2 | Yes button |
| `DBB_NO` | 3 | No button |
| `DBB_CANCEL` | 4 | Cancel button |

**Message types** (`DMT_` -- DialogMessageType):

| Constant | Icon |
|----------|------|
| `DMT_NONE` | No icon |
| `DMT_INFO` | Info |
| `DMT_WARNING` | Warning |
| `DMT_QUESTION` | Question mark |
| `DMT_EXCLAMATION` | Exclamation |

### When to Use ShowDialog

Use `ShowDialog()` for simple alerts and confirmations that do not need custom styling. It is reliable and handles focus/cursor automatically. For branded or complex dialogs (custom layout, input fields, multiple options), build your own dialog class.

---

## Manual Dialog Pattern (Without UIScriptedMenu)

When you need a dialog that is not part of the engine menu stack -- for example, a popup inside an existing panel -- extend `ScriptedWidgetEventHandler` instead of `UIScriptedMenu`. This gives you full control but requires manual focus and lifecycle management.

### Basic Pattern

```c
class SimplePopup : ScriptedWidgetEventHandler
{
    protected Widget       m_Root;
    protected ButtonWidget m_BtnOk;
    protected ButtonWidget m_BtnCancel;
    protected TextWidget   m_Message;

    void Show(string message)
    {
        if (m_Root)
            return;
        m_Root = GetGame().GetWorkspace().CreateWidgets(
            "MyMod/GUI/layouts/simple_popup.layout");
        if (!m_Root)
            return;
        m_Root.SetHandler(this);

        m_BtnOk     = ButtonWidget.Cast(m_Root.FindAnyWidget("BtnOk"));
        m_BtnCancel = ButtonWidget.Cast(m_Root.FindAnyWidget("BtnCancel"));
        m_Message   = TextWidget.Cast(m_Root.FindAnyWidget("Message"));

        m_Message.SetText(message);

        // Lock game input so player cannot move/shoot
        GetGame().GetInput().ChangeGameFocus(1);
        GetGame().GetUIManager().ShowUICursor(true);
    }

    void Hide()
    {
        if (!m_Root)
            return;
        if (m_Root)
        {
            m_Root.Unlink();
            m_Root = null;
        }

        // Restore game input -- MUST match the +1 from Show()
        GetGame().GetInput().ChangeGameFocus(-1);
        GetGame().GetUIManager().ShowUICursor(false);
    }

    void ~SimplePopup()
    {
        Hide();
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        if (w == m_BtnOk)
        {
            OnConfirm();
            Hide();
            return true;
        }

        if (w == m_BtnCancel)
        {
            Hide();
            return true;
        }

        return false;
    }

    protected void OnConfirm()
    {
        // Override in subclasses or set a callback
    }
}
```

### Popup via OnWidgetScriptInit

`OnWidgetScriptInit()` is a common way to initialize a popup: the widget is created by a parent, and the script class is bound to it through the `scriptclass` attribute in the layout file. The engine calls `OnWidgetScriptInit()` on that class as soon as the widget exists, giving you a natural place to cache child references:

```c
class LNT_Popup : ScriptedWidgetEventHandler
{
    protected Widget       m_Root;
    protected ButtonWidget m_BtnClose;
    protected ButtonWidget m_BtnSave;
    protected EditBoxWidget m_NameInput;

    void OnWidgetScriptInit(Widget w)
    {
        m_Root = w;
        m_Root.SetHandler(this);

        m_BtnClose  = ButtonWidget.Cast(m_Root.FindAnyWidget("BtnClose"));
        m_BtnSave   = ButtonWidget.Cast(m_Root.FindAnyWidget("BtnSave"));
        m_NameInput = EditBoxWidget.Cast(m_Root.FindAnyWidget("NameInput"));

        // Push dialog above other widgets
        m_Root.SetSort(1024, true);
    }

    void ~LNT_Popup()
    {
        if (m_Root)
            m_Root.Unlink();
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        if (w == m_BtnClose)
        {
            delete this;
            return true;
        }

        if (w == m_BtnSave)
        {
            string name = m_NameInput.GetText();
            if (name != "")
            {
                SaveName(name);
                delete this;
            }
            return true;
        }

        return false;
    }

    protected void SaveName(string name)
    {
        // Process the input
    }
}
```

The parent creates the popup by creating the layout widget as a child:

```c
Widget popup = GetGame().GetWorkspace().CreateWidgets(
    "MyMod/GUI/layouts/popup.layout", parentWidget);
```

The engine automatically calls `OnWidgetScriptInit()` on the script class specified in the layout's `scriptclass` attribute.

---

## Dialog Layout Structure

A dialog layout typically has three layers: a full-screen root for click interception, a semi-transparent overlay for dimming, and the centered dialog panel.

### Layout File Example

```
FrameWidgetClass DialogRoot {
 size 1 1
 hexactsize 0
 vexactsize 0
 {
  PanelWidgetClass Overlay {
   size 1 1
   hexactsize 0
   vexactsize 0
   style rover_sim_colorable
   color 0 0 0 0.7
  }
  FrameWidgetClass DialogPanel {
   size 500 300
   halign center_ref
   valign center_ref
   hexactsize 1
   vexactsize 1
   {
    TextWidgetClass TitleText {
     size 1 30
     hexactsize 0
     vexactsize 1
     text "Dialog Title"
     font "gui/fonts/MetronBook22"
    }
    MultilineTextWidgetClass ContentText {
     position 0 35
     size 1 200
     hexactpos 1
     vexactpos 1
     hexactsize 0
     vexactsize 1
    }
    FrameWidgetClass ButtonRow {
     size 1 40
     valign bottom_ref
     hexactsize 0
     vexactsize 1
     {
      ButtonWidgetClass BtnConfirm {
       size 120 35
       hexactsize 1
       vexactsize 1
       text "Confirm"
      }
      ButtonWidgetClass BtnCancel {
       size 120 35
       halign right_ref
       hexactsize 1
       vexactsize 1
       text "Cancel"
      }
     }
    }
   }
  }
 }
}
```

### Key Layout Principles

1. **Full-screen root** -- The outermost widget covers the entire screen so clicks outside the dialog are intercepted.
2. **Semi-transparent overlay** -- An `ImageWidget` or panel with alpha (e.g., `color 0 0 0 0.7`) dims the background, visually indicating a modal state.
3. **Centered panel** -- Use `halign center_ref` and `valign center_ref` with exact pixel sizes for predictable dimensions.
4. **Button alignment** -- Place buttons in a horizontal container at the bottom of the dialog panel.

---

## Confirmation Dialog Pattern

This standalone example accepts a title, message and callback. Supply `confirm_dialog.layout` with `TitleText`, `ContentText`, `BtnYes` and `BtnNo`; rename the generic layout buttons above accordingly. Do not use its cursor cleanup unchanged inside a parent menu that owns the cursor.

### Implementation

```c
class ConfirmDialog : ScriptedWidgetEventHandler
{
    protected bool m_HasFocus;
    protected bool m_Closing;
    protected Widget          m_Root;
    protected TextWidget      m_TitleText;
    protected MultilineTextWidget m_ContentText;
    protected ButtonWidget    m_BtnYes;
    protected ButtonWidget    m_BtnNo;

    protected Class           m_CallbackTarget;
    protected string          m_CallbackFunc;

    void ConfirmDialog(string title, string message,
                       Class callbackTarget, string callbackFunc)
    {
        m_CallbackTarget = callbackTarget;
        m_CallbackFunc   = callbackFunc;

        m_Root = GetGame().GetWorkspace().CreateWidgets(
            "MyMod/GUI/layouts/confirm_dialog.layout");
        m_Root.SetHandler(this);

        m_TitleText   = TextWidget.Cast(
            m_Root.FindAnyWidget("TitleText"));
        m_ContentText = MultilineTextWidget.Cast(
            m_Root.FindAnyWidget("ContentText"));
        m_BtnYes      = ButtonWidget.Cast(
            m_Root.FindAnyWidget("BtnYes"));
        m_BtnNo       = ButtonWidget.Cast(
            m_Root.FindAnyWidget("BtnNo"));

        m_TitleText.SetText(title);
        m_ContentText.SetText(message);

        // Ensure dialog renders above other UI
        m_Root.SetSort(1024, true);

        m_HasFocus = true;
        GetGame().GetInput().ChangeGameFocus(1);
        GetGame().GetUIManager().ShowUICursor(true);
    }

    protected void ReleaseFocus()
    {
        if (!m_HasFocus)
            return;
        m_HasFocus = false;
        GetGame().GetInput().ChangeGameFocus(-1);
        GetGame().GetUIManager().ShowUICursor(false);
    }

    void ~ConfirmDialog()
    {
        GetGame().GetCallQueue(CALL_CATEGORY_GUI).Remove(DestroyDialog);
        ReleaseFocus();
        if (m_Root)
            m_Root.Unlink();
    }

    protected void SendResult(bool confirmed)
    {
        if (m_Closing)
            return;
        m_Closing = true;
        ReleaseFocus();

        // Call the callback function on the target object
        GetGame().GameScript.CallFunction(
            m_CallbackTarget, m_CallbackFunc, null, confirmed);

        // Clean up -- defer deletion to avoid issues
        GetGame().GetCallQueue(CALL_CATEGORY_GUI).CallLater(
            DestroyDialog, 0, false);
    }

    protected void DestroyDialog()
    {
        delete this;
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        if (w == m_BtnYes)
        {
            SendResult(true);
            return true;
        }

        if (w == m_BtnNo)
        {
            SendResult(false);
            return true;
        }

        return false;
    }
}
```

### Usage

```c
// In the calling class:
void AskDeleteItem()
{
    new ConfirmDialog(
        "Delete Item",
        "Are you sure you want to delete this item?",
        this,
        "OnDeleteConfirmed"
    );
}

void OnDeleteConfirmed(bool confirmed)
{
    if (confirmed)
    {
        DeleteSelectedItem();
    }
}
```

The callback uses `GameScript.CallFunction()` which invokes a function by name on the target object. This is one callback-routing option; other APIs use `func` callbacks or `ScriptInvoker`. Keep the target alive until the dialog finishes.

---

## Input Dialog Pattern

An input dialog adds an `EditBoxWidget` for text entry with validation. Supply `input_dialog.layout` with `TitleText`, `InputBox`, `BtnOk`, `BtnCancel` and `ErrorText`. As with the confirmation example, the code assumes a standalone dialog owns cursor visibility.

```c
class InputDialog : ScriptedWidgetEventHandler
{
    protected bool m_HasFocus;
    protected bool m_Closing;
    protected Widget         m_Root;
    protected TextWidget     m_TitleText;
    protected EditBoxWidget  m_InputBox;
    protected ButtonWidget   m_BtnOk;
    protected ButtonWidget   m_BtnCancel;
    protected TextWidget     m_ErrorText;

    protected Class          m_CallbackTarget;
    protected string         m_CallbackFunc;

    void InputDialog(string title, string defaultText,
                     Class callbackTarget, string callbackFunc)
    {
        m_CallbackTarget = callbackTarget;
        m_CallbackFunc   = callbackFunc;

        m_Root = GetGame().GetWorkspace().CreateWidgets(
            "MyMod/GUI/layouts/input_dialog.layout");
        m_Root.SetHandler(this);

        m_TitleText = TextWidget.Cast(
            m_Root.FindAnyWidget("TitleText"));
        m_InputBox  = EditBoxWidget.Cast(
            m_Root.FindAnyWidget("InputBox"));
        m_BtnOk     = ButtonWidget.Cast(
            m_Root.FindAnyWidget("BtnOk"));
        m_BtnCancel = ButtonWidget.Cast(
            m_Root.FindAnyWidget("BtnCancel"));
        m_ErrorText = TextWidget.Cast(
            m_Root.FindAnyWidget("ErrorText"));

        m_TitleText.SetText(title);
        m_InputBox.SetText(defaultText);
        m_ErrorText.Show(false);

        m_Root.SetSort(1024, true);
        m_HasFocus = true;
        GetGame().GetInput().ChangeGameFocus(1);
        GetGame().GetUIManager().ShowUICursor(true);
    }

    protected void ReleaseFocus()
    {
        if (!m_HasFocus)
            return;
        m_HasFocus = false;
        GetGame().GetInput().ChangeGameFocus(-1);
        GetGame().GetUIManager().ShowUICursor(false);
    }

    void ~InputDialog()
    {
        GetGame().GetCallQueue(CALL_CATEGORY_GUI).Remove(DeleteSelf);
        ReleaseFocus();
        if (m_Root)
            m_Root.Unlink();
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        if (m_Closing)
            return true;
        if (w == m_BtnOk)
        {
            string text = m_InputBox.GetText();
            text.TrimInPlace();

            if (text == "")
            {
                m_ErrorText.SetText("Name cannot be empty");
                m_ErrorText.Show(true);
                return true;
            }

            m_Closing = true;
            ReleaseFocus();

            // Send result as Param2: OK status + text
            GetGame().GameScript.CallFunctionParams(
                m_CallbackTarget, m_CallbackFunc, null,
                new Param2<bool, string>(true, text));

            GetGame().GetCallQueue(CALL_CATEGORY_GUI).CallLater(
                DeleteSelf, 0, false);
            return true;
        }

        if (w == m_BtnCancel)
        {
            m_Closing = true;
            ReleaseFocus();

            GetGame().GameScript.CallFunctionParams(
                m_CallbackTarget, m_CallbackFunc, null,
                new Param2<bool, string>(false, ""));

            GetGame().GetCallQueue(CALL_CATEGORY_GUI).CallLater(
                DeleteSelf, 0, false);
            return true;
        }

        return false;
    }

    override bool OnChange(Widget w, int x, int y, bool finished)
    {
        if (w == m_InputBox)
        {
            // Hide error when user starts typing
            m_ErrorText.Show(false);

            // Submit on Enter key
            if (finished)
            {
                OnClick(m_BtnOk, 0, 0, 0);
            }
            return true;
        }

        return false;
    }

    protected void DeleteSelf()
    {
        delete this;
    }
}
```

---

## Focus Management

Focus management is the most critical aspect of dialog implementation. DayZ uses a **reference-counted** focus system -- every `ChangeGameFocus(1)` must be balanced by a `ChangeGameFocus(-1)`.

### How It Works

```c
// Increment focus counter -- game input is suppressed while counter > 0
GetGame().GetInput().ChangeGameFocus(1);

// Show the mouse cursor
GetGame().GetUIManager().ShowUICursor(true);

// ... dialog interaction ...

// Decrement focus counter -- game input resumes when counter reaches 0
GetGame().GetInput().ChangeGameFocus(-1);

// Hide cursor (only if no other menus need it)
GetGame().GetUIManager().ShowUICursor(false);
```

### Rules

1. **Every +1 must have a matching -1.** If you call `ChangeGameFocus(1)` in `Show()`, you must call `ChangeGameFocus(-1)` in `Hide()`, with no exceptions.

2. **Call -1 even on error paths.** If the dialog is destroyed unexpectedly (player dies, server disconnect), the destructor must still decrement. Put cleanup in the destructor as a safety net.

3. **UIScriptedMenu handles this automatically.** If you extend `UIScriptedMenu` and call `super.OnShow()` / `super.OnHide()`, focus is managed for you. Only manage it manually when using `ScriptedWidgetEventHandler`.

4. **Per-device focus is optional.** The engine supports per-device focus locking (`INPUT_DEVICE_MOUSE`, `INPUT_DEVICE_KEYBOARD`, `INPUT_DEVICE_GAMEPAD`). For most mod dialogs, a single `ChangeGameFocus(1)` (no device argument) locks all input.

5. **ResetGameFocus() is a nuclear option.** It forces the counter to zero. Use it only in top-level cleanup (e.g., when closing an entire admin tool), never inside individual dialog classes.

### What Goes Wrong

| Mistake | Symptom |
|---------|---------|
| Forgot `ChangeGameFocus(-1)` on close | Player cannot move, shoot, or interact after dialog closes |
| Called `-1` twice | Focus counter goes negative; next menu that opens will not properly lock input |
| Forgot `ShowUICursor(false)` | Mouse cursor stays visible permanently |
| Called `ShowUICursor(false)` when parent menu is still open | Cursor disappears while parent menu is still active |

### Stacking Dialogs Safely

Open dialog A (`+1`), open dialog B (`+1`), then close B (`-1`): input correctly stays locked for A. Each dialog must remember whether it acquired focus so destruction cannot release it twice. Cursor visibility needs a shared owner too: a child must not hide the cursor while its parent still needs it. The following guard demonstrates a standalone dialog; use the menu stack or coordinate cursor ownership for nested dialogs.

```c
class SafeDialog : ScriptedWidgetEventHandler
{
    protected Widget m_Root;
    protected bool   m_HasFocus;

    void LockFocus()
    {
        if (!m_HasFocus)
        {
            GetGame().GetInput().ChangeGameFocus(1);
            GetGame().GetUIManager().ShowUICursor(true);
            m_HasFocus = true;
        }
    }

    void UnlockFocus()
    {
        if (m_HasFocus)
        {
            GetGame().GetInput().ChangeGameFocus(-1);
            GetGame().GetUIManager().ShowUICursor(false);
            m_HasFocus = false;
        }
    }

    void ~SafeDialog()
    {
        UnlockFocus();
        if (m_Root)
        {
            m_Root.Unlink();
            m_Root = null;
        }
    }
}
```

This is the single place in the chapter where the unbalanced-focus pitfall is worked through in full; the [Common Mistakes](#common-mistakes) list below points back here rather than repeating it.

---

## Z-Order and Layering

When a dialog opens on top of existing UI, it must render above everything else. DayZ provides two mechanisms:

### Widget Sort Order

```c
// Push widget above all siblings (sort value 1024)
m_Root.SetSort(1024, true);
```

The `SetSort()` method sets the rendering priority. Higher values render on top. The second parameter (`immedUpdate`) controls whether to immediately update rendering -- it is NOT a recursive flag. Signature: `proto native void SetSort(int sort, bool immedUpdate = true)`. A common convention is to reserve a high sort value (e.g. `1024`) for dialog boxes so they always sit above regular UI.

### Layout Priority (Static)

In layout files, you can set priority directly:

```
FrameWidgetClass DialogRoot {
    priority 999
    // Higher values render on top
    // Normal UI: 0-100
    // Overlay:   998
    // Dialog:    999
}
```

### Best Practices

- **Overlay background**: Use a high sort value (e.g., 998) for the semi-transparent background.
- **Dialog panel**: Use a higher sort value (e.g., 999 or 1024) for the dialog itself.
- **Stacking dialogs**: If your system supports nested dialogs, increment the sort value for each new dialog layer.

---

## Common Patterns

### Toggle Panel (Open/Close with Same Key)

```c
class TogglePanel : ScriptedWidgetEventHandler
{
    void ~TogglePanel()
    {
        if (m_IsVisible)
            Hide();
        if (m_Root)
            m_Root.Unlink();
    }

    protected Widget m_Root;
    protected bool   m_IsVisible;

    void Toggle()
    {
        if (m_IsVisible)
            Hide();
        else
            Show();
    }

    protected void Show()
    {
        if (!m_Root)
        {
            m_Root = GetGame().GetWorkspace().CreateWidgets(
                "MyMod/GUI/layouts/toggle_panel.layout");
            m_Root.SetHandler(this);
        }

        m_Root.Show(true);
        m_IsVisible = true;
        GetGame().GetInput().ChangeGameFocus(1);
        GetGame().GetUIManager().ShowUICursor(true);
    }

    protected void Hide()
    {
        if (m_Root)
            m_Root.Show(false);

        m_IsVisible = false;
        GetGame().GetInput().ChangeGameFocus(-1);
        GetGame().GetUIManager().ShowUICursor(false);
    }
}
```

### ESC to Close

Closing on the Back/ESC action follows the same key-handling rules as any other widget input -- see [3.6 Event Handling](06-event-handling.md) for how `OnKeyDown`, the `UAUIBack` input action, and the per-frame `Update()` poll differ. The two shapes a dialog uses:

```c
// Inside Update() of a UIScriptedMenu:
override void Update(float timeslice)
{
    super.Update(timeslice);

    if (GetUApi().GetInputByID(UAUIBack).LocalPress())
    {
        Close();
    }
}

// Inside a ScriptedWidgetEventHandler (no Update loop):
// You must poll from an external update source, or use OnKeyDown:
override bool OnKeyDown(Widget w, int x, int y, int key)
{
    if (key == KeyCode.KC_ESCAPE)
    {
        Hide();
        return true;
    }
    return false;
}
```

### Click Outside to Close

Make the full-screen overlay widget clickable. When clicked, close the dialog:

```c
class OverlayDialog : ScriptedWidgetEventHandler
{
    protected Widget m_Root;
    protected Widget m_Overlay;
    protected Widget m_Panel;

    void Show()
    {
        m_Root    = GetGame().GetWorkspace().CreateWidgets(
            "MyMod/GUI/layouts/overlay_dialog.layout");
        m_Overlay = m_Root.FindAnyWidget("Overlay");
        m_Panel   = m_Root.FindAnyWidget("DialogPanel");

        // Register handler on both overlay and panel widgets
        m_Root.SetHandler(this);
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        // If user clicked the overlay (not the panel), close
        if (w == m_Overlay)
        {
            Hide();
            return true;
        }

        return false;
    }
}
```

### Dialog Result Callbacks

For dialogs that need to return complex results, use `GameScript.CallFunctionParams()` with `Param` objects:

```c
// Sending a result with multiple values
GetGame().GameScript.CallFunctionParams(
    m_CallbackTarget,
    m_CallbackFunc,
    null,
    new Param2<int, string>(RESULT_OK, inputText)
);

// Receiving in the caller
void OnDialogResult(int result, string text)
{
    if (result == RESULT_OK)
    {
        ProcessInput(text);
    }
}
```

This example routes results by target object and method name. DayZ also exposes `func` callbacks and `ScriptInvoker`; choose the callback mechanism supported by the API you are using and keep callback targets alive until the dialog finishes.

---

## UIScriptedWindow -- Floating Windows

DayZ has a second built-in system: `UIScriptedWindow`, for floating windows that exist alongside a `UIScriptedMenu`. Unlike `UIScriptedMenu`, windows are tracked in a static map and their events are routed through the active menu.

The base class stores the window id through its own `UIScriptedWindow(int id)` constructor. Because Enforce Script has no explicit base-constructor call (no `super(args)`) and constructor signatures must stay compatible down the hierarchy, your subclass declares **no constructor of its own** -- the base constructor runs automatically with the id. Declaring your own `MyWindow(int id)` constructor would fail with `Overloaded function 'MyWindow' not compatible`. See [Constructor Rules](../01-enforce-script/03-classes-inheritance.md#constructor-rules-unique-to-enforce-script).

```c
class MyWindow extends UIScriptedWindow
{
    // No constructor here. The inherited UIScriptedWindow(int id)
    // constructor runs automatically and stores m_Id for you.

    override Widget Init()
    {
        m_WgtRoot = GetGame().GetWorkspace().CreateWidgets(
            "MyMod/GUI/layouts/my_window.layout");
        return m_WgtRoot;
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        // Handle clicks
        return false;
    }
}
```

The engine builds your window through the mission's `CreateScriptedWindow(int id)` hook, which is where the `id` reaches the base constructor:

```c
modded class MissionGameplay
{
    override UIScriptedWindow CreateScriptedWindow(int id)
    {
        if (id == MY_WINDOW_ID)
        {
            return new MyWindow(id);
        }

        return super.CreateScriptedWindow(id);
    }
}
```

Windows are opened and closed through the `UIManager`:

```c
// Open
GetGame().GetUIManager().OpenWindow(MY_WINDOW_ID);

// Close
GetGame().GetUIManager().CloseWindow(MY_WINDOW_ID);

// Check if open
GetGame().GetUIManager().IsWindowOpened(MY_WINDOW_ID);
```

In practice, most mod developers use `ScriptedWidgetEventHandler`-based popups rather than `UIScriptedWindow`, because the window system requires registering with the engine's switch-case in `MissionBase` and the events route through the active `UIScriptedMenu`. The manual pattern is simpler and more flexible.

---

## Common Mistakes

The single most common failure -- leaving game input locked after a dialog closes because a `ChangeGameFocus(1)` was never balanced -- is covered in full under [Focus Management](#focus-management), including the `SafeDialog` guard for overlapping dialogs. The mistakes below are the other recurring ones.

### 1. Not Unlinking Widgets on Close

**The problem:** Widget tree stays in memory, events keep firing, memory leaks accumulate.

```c
// WRONG -- just hiding
void Hide()
{
    m_Root.Show(false);  // Widget still exists and consumes memory
}

// CORRECT -- unlink destroys the widget tree
void Hide()
{
    if (m_Root)
    {
        m_Root.Unlink();
        m_Root = null;
    }
}
```

If you need to show/hide the same dialog repeatedly, keeping the widget and using `Show(true/false)` is fine -- just ensure you `Unlink()` in the destructor.

### 2. Dialog Renders Behind Other UI

**The problem:** Dialog is invisible or partially hidden because other widgets have higher rendering priority.

**The fix:** Use `SetSort()` to push the dialog above everything:

```c
m_Root.SetSort(1024, true);
```

### 3. Calling Close() or Delete in the Constructor

**The problem:** Calling `Close()` or `delete this` during construction causes crashes or undefined behavior because the object is not fully initialized.

**The fix:** Defer closure using `CallLater`:

```c
void MyDialog()
{
    // ...
    if (someErrorCondition)
    {
        // WRONG: Close(); or delete this;
        // CORRECT:
        GetGame().GetCallQueue(CALL_CATEGORY_GUI).CallLater(
            DeferredClose, 0, false);
    }
}

void DeferredClose()
{
    Close();  // or: delete this;
}
```

### 4. Not Checking for Null Before Widget Operations

**The problem:** Crash when accessing a widget that was already destroyed or never created.

```c
// WRONG
void UpdateMessage(string text)
{
    m_MessageText.SetText(text);  // Crash if m_MessageText is null
}

// CORRECT
void UpdateMessage(string text)
{
    if (m_MessageText)
        m_MessageText.SetText(text);
}
```

---

## Summary

| Approach | Base Class | Focus Management | Best For |
|----------|-----------|-----------------|----------|
| Engine menu stack | `UIScriptedMenu` | Automatic via `LockControls`/`UnlockControls` | Full-screen menus, major dialogs |
| Native dialog | `ShowDialog()` | Automatic | Simple Yes/No/OK prompts |
| Manual popup | `ScriptedWidgetEventHandler` | Manual `ChangeGameFocus` | In-panel popups, custom dialogs |
| Floating window | `UIScriptedWindow` | Via parent menu | Tool windows alongside a menu |

The golden rule: **every `ChangeGameFocus(1)` must be matched by a `ChangeGameFocus(-1)`.** Put focus cleanup in your destructor as a safety net, always `Unlink()` widgets when done, and use `SetSort()` to ensure your dialog renders on top.

---

## Next Steps

- [3.6 Event Handling](06-event-handling.md) -- Handle clicks, hover, keyboard events inside dialogs
- [3.5 Programmatic Widget Creation](05-programmatic-widgets.md) -- Build dialog content dynamically in code
