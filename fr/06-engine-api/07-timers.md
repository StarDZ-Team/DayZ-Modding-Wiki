# Chapitre 6.7: Timers & CallQueue

[Accueil](../../README.md) | [<< Précédent : Notifications](06-notifications.md) | **Timers & CallQueue** | [Suivant : File I/O & JSON >>](08-file-io.md)

---

## Introduction

DayZ provides several mechanisms for deferred and repeating function calls: `ScriptCallQueue` (the primary system), `Timer`, `ScriptInvoker`, and `WidgetFadeTimer`. These are essential for scheduling delayed logic, creating update loops, and managing timed events without blocking the main thread. Ce chapitre couvre each mechanism with full API signatures and usage patterns.

---

## Catégories d'appel

All timer and call queue systems require a **call category** that determines when the deferred call executes within the frame:

```c
const int CALL_CATEGORY_SYSTEM   = 0;   // System-level operations
const int CALL_CATEGORY_GUI      = 1;   // UI updates
const int CALL_CATEGORY_GAMEPLAY = 2;   // Gameplay logic
const int CALL_CATEGORY_COUNT    = 3;   // Total number of categories
```

Access the queue for a category:

```c
ScriptCallQueue  queue   = GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY);
ScriptInvoker    updater = GetGame().GetUpdateQueue(CALL_CATEGORY_GAMEPLAY);
TimerQueue       timers  = GetGame().GetTimerQueue(CALL_CATEGORY_GAMEPLAY);
```

---

## ScriptCallQueue

**Fichier :** `3_Game/tools/utilityclasses.c`

The primary mechanism for deferred function calls. Supports one-shot delays, repeating calls, and immediate next-frame execution.

### CallLater

```c
void CallLater(func fn, int delay = 0, bool repeat = false,
               void param1 = NULL, void param2 = NULL,
               void param3 = NULL, void param4 = NULL);
```

| Paramètre | Description |
|-----------|-------------|
| `fn` | The function to call (method reference: `this.MyMethod`) |
| `delay` | Delay in milliseconds (0 = next frame) |
| `repeat` | `true` = call repeatedly at `delay` intervals; `false` = call once |
| `param1..4` | Optional parameters passed to the function |

**Exemple --- one-shot delay:**

```c
// Appeler MyFunction une fois after 5 seconds
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(this.MyFunction, 5000, false);
```

**Exemple --- repeating call:**

```c
// Appeler UpdateLoop toutes les 1 second, repeating
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(this.UpdateLoop, 1000, true);
```

**Exemple --- with parameters:**

```c
void ShowMessage(string text, int color)
{
    Print(text);
}

// Appeler avec des paramètres after 2 seconds
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(
    this.ShowMessage, 2000, false, "Hello!", ARGB(255, 255, 0, 0)
);
```

### Call

```c
void Call(func fn, void param1 = NULL, void param2 = NULL,
          void param3 = NULL, void param4 = NULL);
```

Executes the function on the next frame (delay = 0, no repeat). Shorthand for `CallLater(fn, 0, false)`.

**Exemple:**

```c
// Exécuter à la prochaine frame
GetGame().GetCallQueue(CALL_CATEGORY_SYSTEM).Call(this.Initialize);
```

### CallByName

```c
void CallByName(Class obj, string fnName, int delay = 0, bool repeat = false,
                Param par = null);
```

Call a method by its string name. Useful when the method reference is not directly available.

**Exemple:**

```c
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallByName(
    myObject, "OnTimerExpired", 3000, false
);
```

### Remove

```c
void Remove(func fn);
```

Removes a scheduled call. Essential for stopping repeating calls and preventing calls on destroyed objects.

**Exemple:**

```c
// Arrêter un appel répétitif
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

Called internally by le moteur each frame. You should never need to call this manually.

---

## Timer

**Fichier :** `3_Game/tools/utilityclasses.c`

A class-based timer with explicit start/stop lifecycle. Cleaner for long-lived timers that need to be paused or restarted.

### Constructor

```c
void Timer(int category = CALL_CATEGORY_SYSTEM);
```

### Run

```c
void Run(float duration, Class obj, string fn_name, Param params = null, bool loop = false);
```

| Paramètre | Description |
|-----------|-------------|
| `duration` | Time in seconds (not milliseconds!) |
| `obj` | The object whose method will be called |
| `fn_name` | Method name as string |
| `params` | Optional `Param` object with parameters |
| `loop` | `true` = repeat after each duration |

**Exemple --- one-shot timer:**

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

**Exemple --- repeating timer:**

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

### IsPaused

```c
bool IsPaused();
```

Returns `true` if the timer is currently paused.

**Exemple --- pause and resume:**

```c
ref Timer m_Timer;

void StartTimer()
{
    m_Timer = new Timer(CALL_CATEGORY_GAMEPLAY);
    m_Timer.Run(10.0, this, "OnTimerComplete", null, false);
}

void TogglePause()
{
    if (m_Timer.IsPaused())
        m_Timer.Continue();
    else
        m_Timer.Pause();
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

**Fichier :** `3_Game/tools/utilityclasses.c`

An event/delegate system. `ScriptInvoker` holds a list of callback functions and invokes all of them when `Invoke()` is called. This is DayZ's equivalent of C# events or the observer pattern.

### Insert

```c
void Insert(func fn);
```

Register a callback function.

### Remove

```c
void Remove(func fn);
```

Unregister a callback function.

### Invoke

```c
void Invoke(void param1 = NULL, void param2 = NULL,
            void param3 = NULL, void param4 = NULL);
```

Call all registered functions with the provided parameters.

### Count

```c
int Count();
```

Number of registered callbacks.

### Clear

```c
void Clear();
```

Remove all registered callbacks.

**Exemple --- custom event system:**

```c
class MyModule
{
    ref ScriptInvoker m_OnMissionComplete = new ScriptInvoker();

    void CompleteMission()
    {
        // Do completion logic...

        // Notifier tous les écouteurs
        m_OnMissionComplete.Invoke("MissionAlpha", 1500);
    }
}

class MyUI
{
    void Init(MyModule module)
    {
        // S'abonner à l'événement
        module.m_OnMissionComplete.Insert(this.OnMissionComplete);
    }

    void OnMissionComplete(string name, int reward)
    {
        Print(string.Format("Mission %1 complete! Reward: %2", name, reward));
    }

    void Cleanup(MyModule module)
    {
        // Toujours se désabonner to prevent dangling references
        module.m_OnMissionComplete.Remove(this.OnMissionComplete);
    }
}
```

### Update Queue

Le moteur provides per-frame `ScriptInvoker` queues:

```c
ScriptInvoker updater = GetGame().GetUpdateQueue(CALL_CATEGORY_GAMEPLAY);
updater.Insert(this.OnFrame);

// Remove when done
updater.Remove(this.OnFrame);
```

Functions registered on the update queue are called every frame with no parameters. This is useful for per-frame logic without using `EntityEvent.FRAME`.

---

## WidgetFadeTimer

**Fichier :** `3_Game/tools/utilityclasses.c`

A specialized timer for fading widgets in and out.

```c
class WidgetFadeTimer
{
    void FadeIn(Widget w, float time, bool continue_from_current = false);
    void FadeOut(Widget w, float time, bool continue_from_current = false);
    bool IsFading();
    void Stop();
}
```

| Paramètre | Description |
|-----------|-------------|
| `w` | The widget to fade |
| `time` | Duration of the fade in seconds |
| `continue_from_current` | If `true`, start from current alpha; otherwise start from 0 (fade in) or 1 (fade out) |

**Exemple:**

```c
ref WidgetFadeTimer m_FadeTimer;
Widget m_NotificationPanel;

void ShowNotification()
{
    m_NotificationPanel.Show(true);
    m_FadeTimer = new WidgetFadeTimer;
    m_FadeTimer.FadeIn(m_NotificationPanel, 0.3);

    // Masquer automatiquement après 5 seconds
    GetGame().GetCallQueue(CALL_CATEGORY_GUI).CallLater(this.HideNotification, 5000, false);
}

void HideNotification()
{
    m_FadeTimer.FadeOut(m_NotificationPanel, 0.5);
}
```

---

## GetRemainingTime (CallQueue)

The `ScriptCallQueue` also provides a way to query how much time is left on a scheduled `CallLater`:

```c
float GetRemainingTime(Class obj, string fnName);
```

**Exemple:**

```c
// Get how much time is left on a CallLater
float remaining = GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).GetRemainingTime(this, "MyCallback");
if (remaining > 0)
    Print(string.Format("Callback fires in %1 ms", remaining));
```

---

## Patrons courants

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

        // Logique limitée ici
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
        // Travail périodique
    }
}
```

### One-Shot Delayed Init

A common pattern for initializing systems after le monde is fully loaded:

```c
void OnMissionStart()
{
    // Retarder l'init de 1 second to ensure everything is loaded
    GetGame().GetCallQueue(CALL_CATEGORY_SYSTEM).CallLater(this.DelayedInit, 1000, false);
}

void DelayedInit()
{
    // Sûr d'accéder aux world objects now
}
```

---

## Résumé

| Mécanisme | Cas d'utilisation | Unité de temps |
|-----------|----------|-----------|
| `CallLater` | One-shot or repeating deferred calls | Milliseconds |
| `Call` | Execute next frame | N/A (immediate) |
| `Timer` | Class-based timer with start/stop/remaining | Seconds |
| `ScriptInvoker` | Event/delegate (observer pattern) | N/A (manual invoke) |
| `WidgetFadeTimer` | Widget fade-in/fade-out | Seconds |
| `GetUpdateQueue()` | Per-frame callback registration | N/A (every frame) |

| Concept | Point clé |
|---------|-----------|
| Categories | `CALL_CATEGORY_SYSTEM` (0), `GUI` (1), `GAMEPLAY` (2) |
| Remove calls | Always `Remove()` in destructor to prevent dangling references |
| Timer vs CallLater | Timer is seconds + class-based; CallLater is milliseconds + functional |
| ScriptInvoker | Insert/Remove callbacks, Invoke to fire all |

---

## Bonnes pratiques

- **Always `Remove()` scheduled `CallLater` calls in your destructor.** If the owning object is destroyed while a `CallLater` is still pending, le moteur will call a method on a deleted object and crash. Every `CallLater` must have a matching `Remove()` in the destructor.
- **Use `Timer` (seconds) for long-lived timers with pause/resume, `CallLater` (milliseconds) for fire-and-forget delays.** Mixing them up leads to off-by-1000x timing bugs since `Timer.Run()` uses seconds but `CallLater` uses milliseconds.
- **Throttle `OnUpdate` with a timer accumulator instead of registering a repeating `CallLater`.** A `CallLater` with repeat creates a separate tracked entry in the queue, while an accumulator pattern (`m_Acc += timeslice; if (m_Acc >= INTERVAL)`) has zero overhead and is easier to tune.
- **Unsubscribe `ScriptInvoker` callbacks before the listener is destroyed.** Forgetting to call `Remove()` on a `ScriptInvoker` leaves a dangling function reference that crashes when `Invoke()` fires.
- **Never call `Tick()` manually on `ScriptCallQueue`.** Le moteur calls it automatically each frame. Manual calls double-fire all pending callbacks.

---

## Compatibilité et impact

> **Compatibilité des mods :** Timer systems are per-instance, so mods rarely conflict on timers directly. The risk is in shared `ScriptInvoker` events where multiple mods register callbacks.

- **Ordre de chargement :** Timer and CallQueue systems are load-order independent. Each mod manages its own timers.
- **Conflits de classes moddées :** No direct conflicts, but if two mods both override `OnUpdate()` on the same class (e.g., `MissionServer`) and one forgets `super`, the other's accumulator-based timers stop working.
- **Impact sur la performance :** Each active `CallLater` with `repeat = true` is checked every frame. Hundreds of repeating calls degrade server tick rate. Prefer fewer timers with longer intervals, or use the accumulator pattern in `OnUpdate`.
- **Serveur/Client :** `CallLater` and `Timer` work on both sides. Use `CALL_CATEGORY_GAMEPLAY` for game logic, `CALL_CATEGORY_GUI` for UI updates (client only), and `CALL_CATEGORY_SYSTEM` for low-level operations.

---

## Observé dans les mods réels

> Ces patrons ont été confirmés par l'étude du code source de mods DayZ professionnels.

| Patron | Mod | Fichier/Emplacement |
|---------|-----|---------------|
| Destructor `Remove()` cleanup for every `CallLater` registration | COT | Module manager lifecycle |
| `ScriptInvoker` event bus for cross-module notifications | Expansion | `ExpansionEventBus` |
| `Timer` with `Pause()`/`Continue()` for logout countdown | Vanilla | `MissionServer` logout system |
| Accumulator pattern in `OnUpdate` for 5-second periodic checks | Dabs Framework | Module tick scheduling |

---

[<< Précédent : Notifications](06-notifications.md) | **Timers & CallQueue** | [Suivant : File I/O & JSON >>](08-file-io.md)
