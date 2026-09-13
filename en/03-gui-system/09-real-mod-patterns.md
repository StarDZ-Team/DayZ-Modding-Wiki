# Production UI Architecture Patterns

> **Summary:** The architecture patterns behind real DayZ admin tools, market menus, themed menu replacers, notification feeds, and map editors — taught here through original teaching implementations that you can adapt to your mod.

The `LNT_*` examples are teaching sketches: supply the referenced layouts, complete placeholder actions, and connect input or client/server messages in your mod. Keep cooperating UI classes in `5_Mission` so a lower script module does not reference classes defined above it.

For a concrete public implementation, compare Dabs Framework's [SliderPrefab handler](https://github.com/InclementDab/DayZ-Dabs-Framework/blob/fd859fd891f45a4a9c9089597db0c621ef3a9de5/DabsFramework/Scripts/3_Game/DabsFramework/_Legacy/Prefabs/SliderPrefab.c) with its [SliderPrefab layout](https://github.com/InclementDab/DayZ-Dabs-Framework/blob/fd859fd891f45a4a9c9089597db0c621ef3a9de5/DabsFramework/gui/Layouts/prefabs/SliderPrefab.layout). The layout binds `Value` and `CalculatedValue` through `ViewBinding`, and its `Relay_Command` values route to `OnButtonUp`/`OnButtonDown`; the handler clamps the value and notifies the controller. This is a framework-dependent legacy prefab at the linked revision, not a standalone vanilla API recipe.

---

## Table of Contents

- [Why Architecture Patterns Matter](#why-architecture-patterns-matter)
- [Module-Form-Window Admin Panels](#module-form-window-admin-panels)
- [A Mini Window Manager](#a-mini-window-manager)
- [Declarative Data Binding](#declarative-data-binding)
- [A Three-Layer Theme System](#a-three-layer-theme-system)
- [Multi-Type Notifications](#multi-type-notifications)
- [The Command Pattern](#the-command-pattern)
- [Common UI Architecture Patterns](#common-ui-architecture-patterns)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Which Pattern to Use When](#which-pattern-to-use-when)

---

## Why Architecture Patterns Matter

DayZ's documentation explains individual widgets and event callbacks, but it says nothing about the problems that appear the moment a UI grows past one panel:

- How to manage a dozen admin panels without code duplication
- How to build a draggable, focusable sub-window system inside a fullscreen menu
- How to theme an entire client without touching vanilla layout files
- How to keep a data-heavy panel in sync without rewriting widget code by hand
- How to structure an editor-style tool with undo/redo and keyboard shortcuts

These are *architecture* problems, and the DayZ modding community has converged on a handful of reusable solutions for each one. This chapter maps those solutions. Every example is written fresh against vanilla APIs and uses the wiki's teaching mod family, **Lantern** (the `LNT_` prefix; its full framework code lives in the Part 7 pattern chapters). Nothing here is copied from a shipped mod — each pattern is reconstructed from the concept up so you can adapt it to your own project.

---

## Module-Form-Window Admin Panels

The most scalable admin-tool architecture splits every tool into three cooperating layers so that adding a tool never touches existing code:

1. **Module** — declares metadata (title, layout path, access rule). Holds no UI logic.
2. **Form** — a `ScriptedWidgetEventHandler` that builds and reads the panel's widgets.
3. **Window** — a thin container that owns the widget tree and the title bar.

A single registry lists every module. Adding a new tool is one module class, one form class, one layout file, and one line in the registry.

### The Module

```c
// 5_Mission — keep this descriptor with the UI classes it references.
class LNT_PanelModule
{
    protected ref LNT_Window m_Window;
    protected ref LNT_Form m_Form;

    // Override these in each tool.
    string GetTitle()  { return "Panel"; }
    string GetLayout() { return "Lantern_Admin/GUI/layouts/panel.layout"; }

    // Gate visibility. Wire this to your permission system (see Part 7.5).
    bool HasAccess() { return true; }

    // Each module supplies the form that drives its layout.
    LNT_Form CreateForm() { return new LNT_Form(); }

    bool IsOpen() { return m_Window != null; }

    void Open()
    {
        if (!HasAccess())
            return;
        if (m_Window)
            return;

        m_Window = new LNT_Window();
        m_Form = CreateForm();
        m_Window.Load(GetLayout(), GetTitle(), m_Form);
    }

    void Close()
    {
        if (m_Window)
        {
            m_Window.Unload();
            m_Window = null;
            m_Form = null;
        }
    }

    void Toggle()
    {
        if (IsOpen())
            Close();
        else
            Open();
    }
}
```

### The Window

```c
// 5_Mission — owns the widget tree, sets the title, hands events to the form.
class LNT_Window
{
    protected Widget m_Root;

    void Load(string layout, string title, LNT_Form form)
    {
        m_Root = GetGame().GetWorkspace().CreateWidgets(layout);
        if (!m_Root)
            return;

        TextWidget titleWidget = TextWidget.Cast(m_Root.FindAnyWidget("TitleText"));
        if (titleWidget)
            titleWidget.SetText(title);

        form.Attach(m_Root);
    }

    void Unload()
    {
        if (m_Root)
        {
            m_Root.Unlink();
            m_Root = null;
        }
    }

    Widget GetRoot() { return m_Root; }
}
```

### The Form

```c
// 5_Mission — receives widget events and builds/reads the panel contents.
class LNT_Form : ScriptedWidgetEventHandler
{
    protected Widget m_Root;

    // Called by the window once the layout exists.
    void Attach(Widget root)
    {
        m_Root = root;
        m_Root.SetHandler(this);
        OnAttached();
    }

    // Override to cache child widgets and populate the panel.
    void OnAttached() {}

    override bool OnClick(Widget w, int x, int y, int button)
    {
        return false;
    }
}
```

### A Concrete Tool and the Registry

```c
class LNT_KickForm : LNT_Form
{
    protected ButtonWidget m_KickButton;

    override void OnAttached()
    {
        m_KickButton = ButtonWidget.Cast(m_Root.FindAnyWidget("KickButton"));
    }

    override bool OnClick(Widget w, int x, int y, int button)
    {
        if (w == m_KickButton)
        {
            // send your kick RPC here
            return true;
        }
        return false;
    }
}

class LNT_KickPanel : LNT_PanelModule
{
    override string GetTitle()     { return "Player Kick"; }
    override string GetLayout()    { return "Lantern_Admin/GUI/layouts/kick_panel.layout"; }
    override LNT_Form CreateForm() { return new LNT_KickForm(); }
}
```

```c
// A single place that lists every admin tool.
// Adding a tool = one line in RegisterPanels().
class LNT_PanelRegistry
{
    protected ref array<ref LNT_PanelModule> m_Panels;

    void LNT_PanelRegistry()
    {
        m_Panels = new array<ref LNT_PanelModule>();
        RegisterPanels();
    }

    void RegisterPanels()
    {
        m_Panels.Insert(new LNT_KickPanel());
        // m_Panels.Insert(new LNT_TeleportPanel());
        // m_Panels.Insert(new LNT_SpawnPanel());
    }

    array<ref LNT_PanelModule> GetPanels() { return m_Panels; }
}
```

**Key takeaway:** each tool is entirely self-contained. Because the registry is the only shared list and it grows by insertion, two people can add two tools without a merge conflict.

---

## A Mini Window Manager

Fullscreen admin HUDs often need several floating panels the operator can drag around, bring to the front, and maximize — a tiny window manager living inside one menu. The whole behavior rides on the title-bar widget and four `ScriptedWidgetEventHandler` overrides. The drag and double-click signatures below match the engine's handler interface exactly (`OnDrag`, `OnDragging`, `OnDoubleClick`, `OnMouseButtonDown`).

```c
// A draggable, maximizable sub-window. The title bar drives drag and maximize.
class LNT_SubWindow : ScriptedWidgetEventHandler
{
    protected Widget m_Root;
    protected Widget m_TitleBar;
    protected float m_DragOffsetX;
    protected float m_DragOffsetY;
    protected bool m_Maximized;
    protected float m_NormalW;
    protected float m_NormalH;

    // Shared counter so the last-focused window always sorts on top.
    static int s_TopSort = 100;

    void Attach(Widget root)
    {
        m_Root = root;
        m_Root.SetHandler(this);
        m_TitleBar = m_Root.FindAnyWidget("TitleBar");
        m_Root.GetSize(m_NormalW, m_NormalH);
    }

    // Raise this window above its siblings.
    void BringToFront()
    {
        s_TopSort = s_TopSort + 1;
        m_Root.SetSort(s_TopSort);
    }

    override bool OnMouseButtonDown(Widget w, int x, int y, int button)
    {
        BringToFront();
        return false;
    }

    // Drag begins: remember where inside the title bar the cursor grabbed.
    override bool OnDrag(Widget w, int x, int y)
    {
        if (w == m_TitleBar)
        {
            float px;
            float py;
            m_Root.GetScreenPos(px, py);
            m_DragOffsetX = x - px;
            m_DragOffsetY = y - py;
            return true;
        }
        return false;
    }

    // Drag in progress: move the window so the grab point tracks the cursor.
    override bool OnDragging(Widget w, int x, int y, Widget reciever)
    {
        if (w == m_TitleBar)
        {
            m_Root.SetScreenPos(x - m_DragOffsetX, y - m_DragOffsetY);
            return true;
        }
        return false;
    }

    // Double-click the title bar to toggle maximize.
    override bool OnDoubleClick(Widget w, int x, int y, int button)
    {
        if (button == MouseState.LEFT && w == m_TitleBar)
        {
            ToggleMaximize();
            return true;
        }
        return false;
    }

    void ToggleMaximize()
    {
        if (m_Maximized)
        {
            m_Root.SetSize(m_NormalW, m_NormalH);
            m_Maximized = false;
        }
        else
        {
            m_Root.SetSize(1.0, 1.0);
            m_Maximized = true;
        }
    }
}
```

**Key takeaway:** `SetSort()` is the whole z-order story — a monotonically increasing counter guarantees the clicked window jumps to the front without tracking every sibling. The drag math stores the grab offset once in `OnDrag`, then applies it every frame in `OnDragging`, so the panel never snaps to the cursor's corner.

---

## Declarative Data Binding

Manually calling `FindAnyWidget()` and `SetText()` for every value gets unmanageable fast. The binding concept flips it around: you store named values on a view-model and let it push each value to the widget that shares its name. Update the value, the widget follows.

The version below is deliberately minimal so the mechanism is visible in one screen. Mature community UI frameworks generalize this into two-way binding, list collections, and command relays — but they are all elaborations of this same name-matching idea.

```c
// A tiny view-model: hold named values, update the matching widget on change.
class LNT_ViewModel
{
    protected Widget m_Root;
    protected ref map<string, string> m_Text;

    void LNT_ViewModel(Widget root)
    {
        m_Root = root;
        m_Text = new map<string, string>();
    }

    // Set a named property and push it to the widget of the same name.
    void SetText(string name, string value)
    {
        m_Text.Set(name, value);
        NotifyPropertyChanged(name);
    }

    string GetText(string name)
    {
        if (m_Text.Contains(name))
            return m_Text.Get(name);
        return "";
    }

    // Find the widget whose name matches the property and write to it.
    void NotifyPropertyChanged(string name)
    {
        if (!m_Root)
            return;

        Widget w = m_Root.FindAnyWidget(name);
        if (!w)
            return;

        TextWidget textWidget = TextWidget.Cast(w);
        if (textWidget)
        {
            textWidget.SetText(GetText(name));
            return;
        }

        EditBoxWidget editWidget = EditBoxWidget.Cast(w);
        if (editWidget)
            editWidget.SetText(GetText(name));
    }

    // Re-push every property, e.g. right after the layout is created.
    void Refresh()
    {
        string key;
        for (int i = 0; i < m_Text.Count(); i++)
        {
            key = m_Text.GetKey(i);
            NotifyPropertyChanged(key);
        }
    }
}
```

Usage is one call — set a value and the label updates itself:

```c
LNT_ViewModel vm = new LNT_ViewModel(panelRoot);
vm.SetText("PlayerName", "Survivor_42");
vm.SetText("Health", "88%");
```

**Key takeaway:** the binding removes the busywork, not the control — when a value maps cleanly to a named widget the view-model handles it, and anything specialized (an item preview, a map marker) still gets a direct widget reference.

---

## A Three-Layer Theme System

To re-skin the client without editing vanilla files, separate *color* from *meaning* from *identity* into three layers. Server owners edit only the middle layer to recolor every menu at once.

```c
// Layer 1 - raw palette: named ARGB values, no UI meaning yet.
class LNT_Palette
{
    static int White()    { return ARGB(255, 255, 255, 255); }
    static int Slate()    { return ARGB(255, 130, 130, 130); }
    static int Amber()    { return ARGB(255, 255, 190, 60); }
    static int DeepBlue() { return ARGB(255, 12, 20, 40); }
    static int Danger()   { return ARGB(255, 190, 55, 55); }
}
```

```c
// Layer 2 - semantic scheme: map UI roles to palette entries.
// Change this layer to re-skin every menu at once.
class LNT_Scheme
{
    static int Brand()       { return LNT_Palette.Amber(); }
    static int PrimaryText() { return LNT_Palette.White(); }
    static int Background()  { return LNT_Palette.DeepBlue(); }
    static int Separator()   { return LNT_Palette.Amber(); }
    static int Warning()     { return LNT_Palette.Danger(); }
}
```

```c
// Layer 3 - branding: server identity (logo, links).
class LNT_Branding
{
    static string Logo()
    {
        return "Lantern_Core/GUI/textures/logo.edds";
    }

    static void ApplyLogo(ImageWidget widget)
    {
        if (!widget)
            return;
        widget.LoadImageFile(0, Logo());
        widget.SetFlags(WidgetFlags.STRETCH);
    }
}
```

This example tints the menu after vanilla initialization. If you replace its layout, you must also preserve the initialization and widget bindings that MainMenu.Init establishes; matching names alone does not initialize cached members.

```c
// Re-skin the vanilla main menu without editing vanilla files.
modded class MainMenu
{
    override Widget Init()
    {
        layoutRoot = super.Init(); // Preserve vanilla widget caching and setup

        Widget divider = layoutRoot.FindAnyWidget("MenuDivider");
        if (divider)
            divider.SetColor(LNT_Scheme.Separator());

        ImageWidget logo = ImageWidget.Cast(layoutRoot.FindAnyWidget("Logo"));
        LNT_Branding.ApplyLogo(logo);

        return layoutRoot;
    }
}
```

For different screen shapes, ship parallel layout folders that hold identical widget names at different sizes and pick one at runtime:

```
GUI/layouts/inventory/narrow/   -- small screens
GUI/layouts/inventory/medium/   -- standard 1080p
GUI/layouts/inventory/wide/     -- ultrawide
```

**Key takeaway:** you can retheme the entire client with only `modded class` overrides, replacement `.layout` files, and one central scheme — no server-side code required for a purely visual mod.

---

## Multi-Type Notifications

Vanilla ships one notification look through `NotificationSystem`:

```c
// Vanilla baseline: a single built-in style.
NotificationSystem.AddNotification(NotificationType.GENERIC_ERROR, 6, "Connection lost");

// From the server, target one player:
NotificationSystem.SendNotificationToPlayer(player, NotificationType.GENERIC_ERROR, 6, "Kicked for AFK");
```

To get several visually distinct styles — a corner toast, a wide banner, a killfeed line — map each *type* to its own layout and expose one static entry point that anything can call.

```c
// Each type maps to its own layout for a distinct look.
enum LNT_NoticeType
{
    TOAST,     // small corner popup
    BANNER,    // wide strip across the top
    KILLFEED   // combat log entry
}
```

```c
// A single notice: type, text, and lifetime.
class LNT_Notice
{
    LNT_NoticeType type;
    string title;
    string body;
    float seconds;

    void LNT_Notice(LNT_NoticeType noticeType, string noticeTitle, string noticeBody, float noticeSeconds)
    {
        type = noticeType;
        title = noticeTitle;
        body = noticeBody;
        seconds = noticeSeconds;
    }

    string GetLayout()
    {
        if (type == LNT_NoticeType.BANNER)
            return "Lantern_Core/GUI/layouts/notice_banner.layout";
        if (type == LNT_NoticeType.KILLFEED)
            return "Lantern_Core/GUI/layouts/notice_killfeed.layout";
        return "Lantern_Core/GUI/layouts/notice_toast.layout";
    }
}
```

```c
// Static entry point: build a notice from anywhere and queue it for display.
class LNT_Notifications
{
    protected static ref array<ref LNT_Notice> s_Queue;

    static void Init()
    {
        if (!s_Queue)
            s_Queue = new array<ref LNT_Notice>();
    }

    static void Create(LNT_NoticeType type, string title, string body, float seconds)
    {
        Init();
        LNT_Notice notice = new LNT_Notice(type, title, body, seconds);
        s_Queue.Insert(notice);
        // A display element (a HUD or UIScriptedMenu) reads s_Queue, builds the
        // layout from notice.GetLayout(), then removes it when its time expires.
    }
}
```

Call this UI helper on the client. A server event needs an RPC or the vanilla SendNotificationToPlayer API to reach that client:

```c
LNT_Notifications.Create(LNT_NoticeType.BANNER, "Airdrop Incoming", "Sector B4", 8);
```

**Key takeaway:** the type enum is the extension point. Adding a new visual style is a new enum value plus a new layout file — the `Create` API and the queue never change.

---

## The Command Pattern

Editor-style tools need actions that are decoupled from the buttons and keys that trigger them, that can enable or disable themselves, and that can be undone. Model each action as a command object; a manager registers them by type and keeps an undo stack.

```c
// Base command: an action decoupled from any button or key.
class LNT_Command
{
    // Do the work. Return true on success.
    bool Execute() { return true; }

    // Reverse the work if the command supports it.
    void Undo() {}
    bool SupportsUndo() { return false; }

    // Whether the command may run right now (drives button enable state).
    bool CanExecute() { return true; }

    string GetName() { return "Command"; }

    // Optional keyboard shortcut. An empty array means none.
    array<int> GetShortcut() { return new array<int>(); }
}
```

```c
class LNT_DeleteCommand : LNT_Command
{
    override bool SupportsUndo() { return true; }
    override bool Execute()
    {
        // remove the selection; push it onto your restore buffer
        return true;
    }

    override void Undo()
    {
        // re-create the object from the restore buffer
    }

    override string GetName() { return "Delete"; }
}

class LNT_UndoCommand : LNT_Command
{
    protected LNT_CommandManager m_Manager;

    void LNT_UndoCommand(LNT_CommandManager manager)
    {
        m_Manager = manager;
    }

    override bool Execute()
    {
        m_Manager.UndoLast();
        return true;
    }

    override bool CanExecute()
    {
        return m_Manager.CanUndo();
    }

    override string GetName() { return "Undo"; }

    // Ctrl+Z
    override array<int> GetShortcut()
    {
        array<int> keys = new array<int>();
        keys.Insert(KeyCode.KC_LCONTROL);
        keys.Insert(KeyCode.KC_Z);
        return keys;
    }
}
```

```c
// Registers commands by type and keeps an undo stack of executed commands.
class LNT_CommandManager
{
    protected ref map<typename, ref LNT_Command> m_Commands;
    protected ref array<ref LNT_Command> m_UndoStack;

    void LNT_CommandManager()
    {
        m_Commands = new map<typename, ref LNT_Command>();
        m_UndoStack = new array<ref LNT_Command>();
    }

    void Register(LNT_Command command)
    {
        m_Commands.Set(command.Type(), command);
    }

    LNT_Command Get(typename commandType)
    {
        if (m_Commands.Contains(commandType))
            return m_Commands.Get(commandType);
        return null;
    }

    // Run a command and, if it succeeded, remember it for undo.
    void Run(typename commandType)
    {
        LNT_Command command = Get(commandType);
        if (!command)
            return;
        if (!command.CanExecute())
            return;
        if (command.Execute() && command.SupportsUndo())
            m_UndoStack.Insert(command);
    }

    bool CanUndo()
    {
        return m_UndoStack.Count() > 0;
    }

    void UndoLast()
    {
        if (!CanUndo())
            return;

        int last = m_UndoStack.Count() - 1;
        LNT_Command command = m_UndoStack.Get(last);
        command.Undo();
        m_UndoStack.Remove(last);
    }
}
```

The deletion and restoration bodies are placeholders. Store a distinct restore record for each execution in your restore buffer; a shared command instance alone is not a history of object state. The Undo command is not itself inserted into the undo stack.

Wiring is one setup call. A toolbar button and a keybind can both fire `Run(LNT_DeleteCommand)` without knowing anything about deletion:

```c
void SetupCommands(LNT_CommandManager manager)
{
    manager.Register(new LNT_DeleteCommand());
    manager.Register(new LNT_UndoCommand(manager));
}
```

**Key takeaway:** because `CanExecute()` lives on the command, a toolbar can grey out a button by asking the command directly, and the same command answers to a keyboard shortcut and a menu item without duplication. Note the manager holds `LNT_UndoCommand` by `ref` while the undo command holds the manager as a **raw** reference — this one-sided ownership avoids a reference cycle.

---

## Common UI Architecture Patterns

These smaller patterns appear across many mods and complement the six above.

### Panel Manager (Show/Hide by Type)

Keep one registry of live panels keyed by typename so you never open a duplicate and always have a single point of control for visibility:

```c
UIScriptedMenu GetMenuByType(typename menuType)
{
    foreach (UIScriptedMenu menu : m_Instances)
    {
        if (menu && menu.Type() == menuType)
            return menu;
    }
    return null;
}

void ToggleShow()
{
    if (IsVisible())
        Close();
    else
        Open();
}
```

### Widget Recycling for Lists

For large lists (player lists, item catalogs, object browsers), never create and destroy widgets on every refresh. Maintain a pool: hide the excess, create only when the pool is too small, then update in place.

```c
void UpdatePlayerList(array<ref PlayerInfo> players)
{
    // Hide excess widgets
    for (int i = players.Count(); i < m_PlayerWidgets.Count(); i++)
        m_PlayerWidgets[i].Show(false);

    // Create new widgets only if needed
    while (m_PlayerWidgets.Count() < players.Count())
    {
        Widget w = GetGame().GetWorkspace().CreateWidgets(PLAYER_ENTRY_LAYOUT, m_ListParent);
        m_PlayerWidgets.Insert(w);
    }

    // Update the visible widgets with data
    for (int j = 0; j < players.Count(); j++)
    {
        m_PlayerWidgets[j].Show(true);
        SetPlayerData(m_PlayerWidgets[j], players[j]);
    }
}
```

### Lazy Widget Creation

Defer building a panel until its first show, so opening the admin HUD does not construct every tool that will never be used:

```c
override Widget Init()
{
    if (!m_Init)
    {
        layoutRoot = GetGame().GetWorkspace().CreateWidgets("Lantern_Admin/GUI/layouts/admin_hud.layout");
        m_Init = true;
        return layoutRoot;
    }
    // Subsequent calls skip creation
    return layoutRoot;
}
```

### Event Delegation Through Handler Chains

A parent handler can route an event to whichever child panel is active, keeping event wiring in one place:

```c
override bool OnClick(Widget w, int x, int y, int button)
{
    if (w == m_CloseButton)
    {
        Hide();
        return true;
    }

    // Delegate to the active tool panel
    if (m_ActivePanel)
        return m_ActivePanel.OnClick(w, x, y, button);

    return false;
}
```

### OnWidgetScriptInit as the Layout-to-Script Bridge

When a layout's root widget declares a `scriptclass`, the engine calls `OnWidgetScriptInit` on that class as soon as `CreateWidgets()` processes it. This is the standard place to cache child widgets:

```c
void OnWidgetScriptInit(Widget w)
{
    m_Root = w;
    m_Root.SetHandler(this);

    m_Button = ButtonWidget.Cast(m_Root.FindAnyWidget("button_name"));
    m_Text = TextWidget.Cast(m_Root.FindAnyWidget("text_name"));
}
```

---

## Anti-Patterns to Avoid

These mistakes appear in real mod code and cause stutter, leaks, or crashes.

### Creating Widgets Every Frame

```c
// BAD: creates new widgets on every Update call
override void Update(float dt)
{
    Widget label = GetGame().GetWorkspace().CreateWidgets("label.layout", m_Parent);
    TextWidget.Cast(label.FindAnyWidget("text")).SetText(m_Value);
}
```

Widget creation allocates memory and forces a layout recalculation. At 60 FPS this leaks 60 widgets per second. Create once, then update in place.

### Not Cleaning Up Event Handlers

```c
// BAD: Insert without a matching Remove
void OnInit()
{
    GetGame().GetUpdateQueue(CALL_CATEGORY_GUI).Insert(Update);
    LNT_EventBus.OnViewTypeChanged.Insert(OnViewTypeChanged);
}

// Missing from the destructor:
// GetGame().GetUpdateQueue(CALL_CATEGORY_GUI).Remove(Update);
// LNT_EventBus.OnViewTypeChanged.Remove(OnViewTypeChanged);
```

Every `Insert` on a `ScriptInvoker` or update queue needs a matching `Remove` in the destructor. Orphaned handlers keep calling into a deleted object and trigger null-access crashes.

### Hardcoding Pixel Positions

```c
// BAD: breaks at other resolutions
m_Panel.SetPos(540, 320);
m_Panel.SetSize(400, 300);
```

Use proportional (0.0-1.0) positioning or let container widgets do the layout. Absolute pixels only work at the resolution they were designed for.

### Deep Widget Nesting Without Purpose

```
Frame -> Panel -> Frame -> Panel -> Frame -> TextWidget
```

Every nesting level adds layout-calculation overhead. If an intermediate widget has no background, no sizing constraint, and no event handling, delete it and flatten the hierarchy.

### Ignoring Focus Management

```c
// BAD: shows the dialog but leaves focus behind it
void ShowDialog()
{
    m_Dialog.Show(true);
    // Missing: SetFocus(m_Dialog.GetLayoutRoot());
}
```

Without `SetFocus()`, keyboard events can still reach widgets behind the dialog. Set focus on show:

```c
override void OnShow()
{
    super.OnShow();
    SetActiveWindow(GetLayoutRoot(), true);
}
```

### Forgetting Widget Cleanup on Destruction

```c
// BAD: the widget tree leaks when the script object is destroyed
void ~LNT_Panel()
{
    // m_Root.Unlink() is missing!
}
```

If you create widgets with `CreateWidgets()`, you own them — call `Unlink()` on the root in your destructor. A `UIScriptedMenu` cleans up its own `layoutRoot` automatically, but a raw `ScriptedWidgetEventHandler` subclass must do it itself.

---

## Which Pattern to Use When

| Need | Pattern | Section |
|------|---------|---------|
| Multi-panel admin tool | Module + Form + Window, one-line registration | [Admin Panels](#module-form-window-admin-panels) |
| Draggable, focusable sub-windows | Title-bar drag + double-click maximize + `SetSort` z-order | [Mini Window Manager](#a-mini-window-manager) |
| Data-heavy panel that changes often | Name-matched view-model binding | [Data Binding](#declarative-data-binding) |
| Re-skin menus without editing vanilla | Palette / scheme / branding + `modded class` | [Theme System](#a-three-layer-theme-system) |
| Several notice styles from one API | Type enum + per-type layout + static `Create` | [Notifications](#multi-type-notifications) |
| Undo/redo, shortcuts, toolbar actions | Command objects + manager with undo stack | [Command Pattern](#the-command-pattern) |
| Show/hide panels without duplicates | Typename registry | [Common Patterns](#common-ui-architecture-patterns) |
| Large lists without churn | Widget recycling pool | [Common Patterns](#common-ui-architecture-patterns) |
| Bind a layout to a script class | `OnWidgetScriptInit` | [Common Patterns](#common-ui-architecture-patterns) |

### Decision Flow

1. **A one-off simple panel?** Use a `ScriptedWidgetEventHandler` with `OnWidgetScriptInit`. Build the layout in the editor, find widgets by name.
2. **Dynamic lists or frequently-changing data?** Use the [view-model binding](#declarative-data-binding) so you set values instead of rewriting widget code.
3. **Part of a multi-panel admin tool?** Use the [module-form-window](#module-form-window-admin-panels) pattern — each tool is self-contained and registration is one line.
4. **Replacing vanilla UI?** Use the [three-layer theme](#a-three-layer-theme-system) with `modded class` and a replacement layout that reuses vanilla widget names.
5. **Server-to-client data sync?** Combine any pattern above with RPC — manage loading states and a request/response cycle inside the panel's update loop.
6. **Undo/redo or complex interaction?** Use the [command pattern](#the-command-pattern): commands decouple actions from buttons, carry their own shortcuts, and answer `CanExecute()` for automatic enable/disable.
