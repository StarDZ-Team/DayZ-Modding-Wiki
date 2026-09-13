# Timers & CallQueue


---

## Introduction

DayZ provides several mechanisms for deferred and repeating function calls: `ScriptCallQueue` (the primary system), `Timer`, `ScriptInvoker`, and `WidgetFadeTimer`. These are essential for scheduling delayed logic, creating update loops, and managing timed events without blocking the main thread. This chapter covers each mechanism with full API signatures and usage patterns.

---

## Call Categories

All timer and call queue systems require a **call category** that determines when the deferred call executes within the frame:

```c
const int CALL_CATEGORY_SYSTEM   = 0;   // Runs always
const int CALL_CATEGORY_GUI      = 1;   // Runs always (on client)
const int CALL_CATEGORY_GAMEPLAY = 2;   // Runs unless the ingame menu is opened
const int CALL_CATEGORY_COUNT    = 3;   // Total number of categories
```

The distinction that matters in practice: a `CALL_CATEGORY_GAMEPLAY` call pauses while the player has the ingame menu open, while `CALL_CATEGORY_SYSTEM` and `CALL_CATEGORY_GUI` keep ticking regardless.

Access the queue for a category:

```c
ScriptCallQueue  queue   = GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY);
ScriptInvoker    updater = GetGame().GetUpdateQueue(CALL_CATEGORY_GAMEPLAY);
TimerQueue       timers  = GetGame().GetTimerQueue(CALL_CATEGORY_GAMEPLAY);
```

---

## ScriptCallQueue

**File:** `2_GameLib/tools.c`

The primary mechanism for deferred function calls. Supports one-shot delays, repeating calls, and immediate next-frame execution.

### CallLater

```c
void CallLater(func fn, int delay = 0, bool repeat = false,
               void param1 = NULL, void param2 = NULL,
               void param3 = NULL, void param4 = NULL,
               void param5 = NULL, void param6 = NULL,
               void param7 = NULL, void param8 = NULL, void param9 = NULL);
```

Up to nine optional parameters are supported (`param1`..`param9`); most calls only need the first few.

| Parameter | Description |
|-----------|-------------|
| `fn` | The function to call (method reference: `this.MyMethod`) |
| `delay` | Delay in milliseconds (0 = next frame) |
| `repeat` | `true` = call repeatedly at `delay` intervals; `false` = call once |
| `param1..4` | Optional parameters passed to the function |

**Example --- one-shot delay:**

```c
// Call MyFunction once after 5 seconds
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(this.MyFunction, 5000, false);
```

**Example --- repeating call:**

```c
// Call UpdateLoop every 1 second, repeating
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(this.UpdateLoop, 1000, true);
```

**Example --- with parameters:**

```c
void ShowMessage(string text, int color)
{
    Print(text);
}

// Call with parameters after 2 seconds
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(
    this.ShowMessage, 2000, false, "Hello!", ARGB(255, 255, 0, 0)
);
```

### Call

```c
void Call(func fn, void param1 = NULL, void param2 = NULL,
          void param3 = NULL, void param4 = NULL,
          void param5 = NULL, void param6 = NULL,
          void param7 = NULL, void param8 = NULL, void param9 = NULL);
```

Executes the function on the next frame (delay = 0, no repeat). Shorthand for `CallLater(fn, 0, false)`. Like `CallLater`, it accepts up to nine parameters.

**Example:**

```c
// Execute next frame
GetGame().GetCallQueue(CALL_CATEGORY_SYSTEM).Call(this.Initialize);
```

### CallByName

```c
void CallByName(Class obj, string fnName, Param params = NULL);
```

Call a method by its string name on the next frame. Useful when the method reference is not directly available. For a delayed or repeating by-name call, use `CallLaterByName` instead:

```c
void CallLaterByName(Class obj, string fnName, int delay = 0, bool repeat = false,
                     Param params = NULL);
```

**Example:**

```c
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLaterByName(
    myObject, "OnTimerExpired", 3000, false
);
```

### Remove

```c
void Remove(func fn);
```

Removes a scheduled call. Essential for stopping repeating calls and preventing calls on destroyed objects.

**Example:**

```c
// Stop a repeating call
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).Remove(this.UpdateLoop);
```

### RemoveByName

```c
void RemoveByName(Class obj, string fnName);
```

Remove a call scheduled via `CallByName`.

### Tick

```c
void Tick(float timeslice);
```

Called internally by the engine each frame. You should never need to call this manually.

---

## Timer

**File:** `3_Game/tools/tools.c`

A class-based timer with explicit start/stop lifecycle. Cleaner for long-lived timers that need to be paused or restarted.

### Constructor

```c
void Timer(int category = CALL_CATEGORY_SYSTEM);
```

### Run

```c
void Run(float duration, Managed obj, string fn_name, Param params = NULL, bool loop = false);
```

| Parameter | Description |
|-----------|-------------|
| `duration` | Time in seconds (not milliseconds!) |
| `obj` | The object whose method will be called |
| `fn_name` | Method name as string |
| `params` | Optional `Param` object with parameters |
| `loop` | `true` = repeat after each duration |

**Example --- one-shot timer:**

```c
ref Timer m_Timer;

void StartTimer()
{
    m_Timer = new Timer(CALL_CATEGORY_GAMEPLAY);
    m_Timer.Run(5.0, this, "OnTimerComplete", null, false);
}

void OnTimerComplete()
{
    Print("Timer finished!");
}
```

**Example --- repeating timer:**

```c
ref Timer m_UpdateTimer;

void StartUpdateLoop()
{
    m_UpdateTimer = new Timer(CALL_CATEGORY_GAMEPLAY);
    m_UpdateTimer.Run(1.0, this, "OnUpdate", null, true);  // Every 1 second
}

void StopUpdateLoop()
{
    if (m_UpdateTimer && m_UpdateTimer.IsRunning())
        m_UpdateTimer.Stop();
}
```

### Stop

```c
void Stop();
```

Stops the timer. Can be restarted with another `Run()` call.

### IsRunning

```c
bool IsRunning();
```

Returns `true` if the timer is currently active.

### Pause

```c
void Pause();
```

Pauses a running timer, preserving the remaining time. The timer can be resumed with `Continue()`.

### Continue

```c
void Continue();
```

Resumes a paused timer from where it left off.

**Example --- pause and resume:**

`Timer` has no `IsPaused()` method. Since `IsRunning()` returns `true` only while the timer is active (and `false` once paused or stopped), use it to decide whether to pause or continue:

```c
ref Timer m_Timer;

void StartTimer()
{
    m_Timer = new Timer(CALL_CATEGORY_GAMEPLAY);
    m_Timer.Run(10.0, this, "OnTimerComplete", null, false);
}

void TogglePause()
{
    if (m_Timer.IsRunning())
        m_Timer.Pause();
    else
        m_Timer.Continue();
}
```

### GetRemaining

```c
float GetRemaining();
```

Returns the remaining time in seconds.

### GetDuration

```c
float GetDuration();
```

Returns the total duration set by `Run()`.

---

## ScriptInvoker

**File:** `2_GameLib/tools.c`

An event/delegate system. `ScriptInvoker` holds a list of callback functions and invokes all of them when `Invoke()` is called. This is DayZ's equivalent of C# events or the observer pattern.

### Insert

```c
bool Insert(func fn, int flags = EScriptInvokerInsertFlags.IMMEDIATE);
```

Register a callback function. The optional `flags` argument accepts `EScriptInvokerInsertFlags.IMMEDIATE` (default) or `EScriptInvokerInsertFlags.UNIQUE`. Returns `true` on success.

### Remove

```c
bool Remove(func fn, int flags = EScriptInvokerRemoveFlags.ALL);
```

Unregister a callback function. The optional `flags` argument defaults to `EScriptInvokerRemoveFlags.ALL`. Returns `true` on success.

### Invoke

```c
void Invoke(void param1 = NULL, void param2 = NULL,
            void param3 = NULL, void param4 = NULL,
            void param5 = NULL, void param6 = NULL,
            void param7 = NULL, void param8 = NULL, void param9 = NULL);
```

Call all registered functions with the provided parameters (up to nine).

### Count

```c
int Count(func fn);
```

Returns how many times the given function `fn` is currently registered in the invoker (not a total count of all callbacks).

### Clear

```c
void Clear();
```

Remove all registered callbacks.

**Example --- custom event system:**

```c
class MyModule
{
    ref ScriptInvoker m_OnMissionComplete = new ScriptInvoker();

    void CompleteMission()
    {
        // Do completion logic...

        // Notify all listeners
        m_OnMissionComplete.Invoke("MissionAlpha", 1500);
    }
}

class MyUI
{
    void Init(MyModule module)
    {
        // Subscribe to the event
        module.m_OnMissionComplete.Insert(this.OnMissionComplete);
    }

    void OnMissionComplete(string name, int reward)
    {
        Print(string.Format("Mission %1 complete! Reward: %2", name, reward));
    }

    void Cleanup(MyModule module)
    {
        // Always unsubscribe to prevent dangling references
        module.m_OnMissionComplete.Remove(this.OnMissionComplete);
    }
}
```

### Update Queue

The engine provides per-frame `ScriptInvoker` queues:

```c
ScriptInvoker updater = GetGame().GetUpdateQueue(CALL_CATEGORY_GAMEPLAY);
updater.Insert(this.OnFrame);

// Remove when done
updater.Remove(this.OnFrame);

void OnFrame(float timeslice)
{
    // timeslice = seconds since the previous frame
}
```

`DayZGame.OnUpdate()` drives these queues with `GetUpdateQueue(category).Invoke(timeslice)`, so a registered function receives **one float argument**: the frame delta in seconds. Declare it. Vanilla listeners such as `RadialProgressBar.Update(float tDelta)` and `PluginManager.MainOnUpdate(float delta_time)` do exactly that. This is useful for per-frame logic without using `EntityEvent.FRAME`.

Note the gating, which differs per category (`3_Game/dayzgame.c:2979-3057`, `OnUpdate()` in the supplied extraction): the `CALL_CATEGORY_SYSTEM` queue is ticked unconditionally; the `CALL_CATEGORY_GUI` queue sits inside `#ifndef NO_GUI` and is additionally skipped while the loading screen or the static login-time screen is up; the `CALL_CATEGORY_GAMEPLAY` queue sits **outside** `#ifndef NO_GUI` and is gated only by `if (gameIsRunning)` (true when the mission exists, simulation is enabled, and it is not paused) --- so `GAMEPLAY` still ticks on a `NO_GUI` build.

---

## WidgetFadeTimer

**File:** `3_Game/tools/tools.c`

A specialized timer for fading widgets in and out. `WidgetFadeTimer` extends `TimerBase`, so it inherits `Stop()` and `IsRunning()`.

```c
class WidgetFadeTimer extends TimerBase
{
    void FadeIn(Widget w, float time, bool continue_ = false);
    void FadeOut(Widget w, float time, bool continue_ = false);
    // Stop() and IsRunning() are inherited from TimerBase
}
```

| Parameter | Description |
|-----------|-------------|
| `w` | The widget to fade |
| `time` | Duration of the fade in seconds |
| `continue_` | If `true`, start from current alpha; otherwise start from 0 (fade in) or 1 (fade out) |

Use the inherited `IsRunning()` to check whether a fade is currently in progress.

**Example:**

```c
ref WidgetFadeTimer m_FadeTimer;
Widget m_NotificationPanel;

void ShowNotification()
{
    m_NotificationPanel.Show(true);
    m_FadeTimer = new WidgetFadeTimer;
    m_FadeTimer.FadeIn(m_NotificationPanel, 0.3);

    // Auto-hide after 5 seconds
    GetGame().GetCallQueue(CALL_CATEGORY_GUI).CallLater(this.HideNotification, 5000, false);
}

void HideNotification()
{
    m_FadeTimer.FadeOut(m_NotificationPanel, 0.5);
}
```

---

## GetRemainingTime (CallQueue)

The `ScriptCallQueue` also provides a way to query how much time is left (in milliseconds) on a scheduled call. There are two variants --- one keyed by function reference and one keyed by name:

```c
int GetRemainingTime(func fn);
int GetRemainingTimeByName(Class obj, string fnName);
```

**Example:**

```c
// Get how much time is left on a call scheduled by name
int remaining = GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).GetRemainingTimeByName(this, "MyCallback");
if (remaining > 0)
    Print(string.Format("Callback fires in %1 ms", remaining));
```

---

## Common Patterns

### Timer Accumulator (Throttled OnUpdate)

When you have a per-frame callback but want to run logic at a slower rate:

```c
class MyModule
{
    protected float m_UpdateAccumulator;
    protected const float UPDATE_INTERVAL = 2.0;  // Every 2 seconds

    void OnUpdate(float timeslice)
    {
        m_UpdateAccumulator += timeslice;
        if (m_UpdateAccumulator < UPDATE_INTERVAL)
            return;
        m_UpdateAccumulator = 0;

        // Throttled logic here
        DoPeriodicWork();
    }
}
```

### Cleanup Pattern

Always remove scheduled calls when your object is destroyed to prevent crashes:

```c
class MyManager
{
    void MyManager()
    {
        GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(this.Tick, 1000, true);
    }

    void ~MyManager()
    {
        GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).Remove(this.Tick);
    }

    void Tick()
    {
        // Periodic work
    }
}
```

### One-Shot Delayed Init

A common pattern for initializing systems after the world is fully loaded:

```c
void OnMissionStart()
{
    // Delay init by 1 second to ensure everything is loaded
    GetGame().GetCallQueue(CALL_CATEGORY_SYSTEM).CallLater(this.DelayedInit, 1000, false);
}

void DelayedInit()
{
    // Safe to access world objects now
}
```

---

## Summary

| Mechanism | Use Case | Time Unit |
|-----------|----------|-----------|
| `CallLater` | One-shot or repeating deferred calls | Milliseconds |
| `Call` | Execute next frame | N/A (immediate) |
| `Timer` | Class-based timer with start/stop/remaining | Seconds |
| `ScriptInvoker` | Event/delegate (observer pattern) | N/A (manual invoke) |
| `WidgetFadeTimer` | Widget fade-in/fade-out | Seconds |
| `GetUpdateQueue()` | Per-frame callback registration | N/A (every frame) |

| Concept | Key Point |
|---------|-----------|
| Categories | `CALL_CATEGORY_SYSTEM` (0), `GUI` (1), `GAMEPLAY` (2) |
| Remove calls | Always `Remove()` in destructor to prevent dangling references |
| Timer vs CallLater | Timer is seconds + class-based; CallLater is milliseconds + functional |
| ScriptInvoker | Insert/Remove callbacks, Invoke to fire all |

---

## Best Practices

- **Always `Remove()` scheduled `CallLater` calls in your destructor.** If the owning object is destroyed while a `CallLater` is still pending, the engine will call a method on a deleted object and crash. Every `CallLater` must have a matching `Remove()` in the destructor.
- **Use `Timer` (seconds) for long-lived timers with pause/resume, `CallLater` (milliseconds) for fire-and-forget delays.** Mixing them up leads to off-by-1000x timing bugs since `Timer.Run()` uses seconds but `CallLater` uses milliseconds.
- **Throttle `OnUpdate` with a timer accumulator instead of registering a repeating `CallLater`.** A `CallLater` with repeat creates a separate tracked entry in the queue, while an accumulator pattern (`m_Acc += timeslice; if (m_Acc >= INTERVAL)`) has zero overhead and is easier to tune.
- **Unsubscribe `ScriptInvoker` callbacks before the listener is destroyed.** Forgetting to call `Remove()` on a `ScriptInvoker` leaves a dangling function reference that crashes when `Invoke()` fires.
- **Never call `Tick()` manually on `ScriptCallQueue`.** The engine calls it automatically each frame. Manual calls double-fire all pending callbacks.

---

## Compatibility & Impact

> **Mod Compatibility:** Timer systems are per-instance, so mods rarely conflict on timers directly. The risk is in shared `ScriptInvoker` events where multiple mods register callbacks.

- **Load Order:** Timer and CallQueue systems are load-order independent. Each mod manages its own timers.
- **Modded Class Conflicts:** No direct conflicts, but if two mods both override `OnUpdate()` on the same class (e.g., `MissionServer`) and one forgets `super`, the other's accumulator-based timers stop working.
- **Performance Impact:** Each active `CallLater` with `repeat = true` is checked every frame. Hundreds of repeating calls degrade server tick rate. Prefer fewer timers with longer intervals, or use the accumulator pattern in `OnUpdate`.
- **Server/Client:** `CallLater` and `Timer` work on both sides. Use `CALL_CATEGORY_GAMEPLAY` for game logic, `CALL_CATEGORY_GUI` for UI updates (client only), and `CALL_CATEGORY_SYSTEM` for low-level operations.

---

## Where These Patterns Show Up

These mechanisms recur across framework and content mods. The table maps each to the pattern that makes it reliable:

| Pattern | Where it applies | Reference |
|---------|------------------|-----------|
| Destructor `Remove()` cleanup for every `CallLater` registration | Any manager that schedules a repeating tick | See [Cleanup Pattern](#cleanup-pattern) above |
| `ScriptInvoker`-backed event bus for cross-module notifications | Frameworks that decouple producers from listeners | The Lantern example builds one in [7.6 Event Bus](../07-patterns/06-events.md) |
| `Timer` with `Pause()`/`Continue()` for a countdown that must survive interruptions | Logout / respawn / capture timers | Vanilla `MissionServer` logout system |
| Accumulator pattern in `OnUpdate` for periodic checks | Per-frame update hooks throttled to a slower rate | See [Timer Accumulator](#timer-accumulator-throttled-onupdate) above |
