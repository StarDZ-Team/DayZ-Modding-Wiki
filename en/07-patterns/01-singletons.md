# Singleton Pattern


---

The singleton pattern guarantees that a class has exactly one instance, accessible globally. In DayZ modding it is the most common architectural pattern --- virtually every manager, cache, registry, and subsystem uses it.

This chapter covers the canonical implementation, lifecycle management, when the pattern is appropriate, and where it goes wrong.

---

## Table of Contents

- [The Canonical Implementation](#the-canonical-implementation)
- [Lazy vs Eager Initialization](#lazy-vs-eager-initialization)
- [Lifecycle Management](#lifecycle-management)
- [When to Use Singletons](#when-to-use-singletons)
- [Singleton Variants in Practice](#singleton-variants-in-practice)
- [Thread Safety Considerations](#thread-safety-considerations)
- [Anti-Patterns](#anti-patterns)
- [Alternative: Static-Only Classes](#alternative-static-only-classes)
- [Checklist](#checklist)

---

## The Canonical Implementation

The standard DayZ singleton follows a simple formula: a `private static ref` field, a static `GetInstance()` accessor, and a static `DestroyInstance()` for cleanup.

```c
class LootManager
{
    // The single instance. 'ref' keeps it alive; 'private' prevents external tampering.
    private static ref LootManager s_Instance;

    // Private data owned by the singleton
    protected ref map<string, int> m_SpawnCounts;

    // Constructor — called exactly once
    void LootManager()
    {
        m_SpawnCounts = new map<string, int>();
    }

    // Destructor — called when s_Instance is set to null
    void ~LootManager()
    {
        m_SpawnCounts = null;
    }

    // Lazy accessor: creates on first call
    static LootManager GetInstance()
    {
        if (!s_Instance)
        {
            s_Instance = new LootManager();
        }
        return s_Instance;
    }

    // Explicit teardown
    static void DestroyInstance()
    {
        s_Instance = null;
    }

    // --- Public API ---

    void RecordSpawn(string className)
    {
        int count = 0;
        m_SpawnCounts.Find(className, count);
        m_SpawnCounts.Set(className, count + 1);
    }

    int GetSpawnCount(string className)
    {
        int count = 0;
        m_SpawnCounts.Find(className, count);
        return count;
    }
};
```

### Why `private static ref`?

| Keyword | Purpose |
|---------|---------|
| `private` | Prevents other classes from setting `s_Instance` to null or replacing it |
| `static` | Shared across all code --- no instance needed to access it |
| `ref` | Strong reference --- keeps the object alive as long as `s_Instance` is non-null |

Enforce Script uses automatic reference counting, not a tracing garbage collector, and class members are weak references unless marked `ref`. Without `ref`, `s_Instance` would not keep the object alive: as soon as the last strong reference went away the object would be destroyed, and `s_Instance` would be set to `NULL` underneath you.

---

## Lazy vs Eager Initialization

### Lazy Initialization (Recommended Default)

The `GetInstance()` method creates the instance on first access. This is the approach used by most DayZ mods.

```c
static LootManager GetInstance()
{
    if (!s_Instance)
    {
        s_Instance = new LootManager();
    }
    return s_Instance;
}
```

**Advantages:**
- No work done until actually needed
- No dependency on initialization order between mods
- Safe if the singleton is optional (some server configurations may never call it)

**Disadvantage:**
- First caller pays the construction cost (usually negligible)

### Eager Initialization

Some singletons are created explicitly during mission startup, typically from `MissionServer.OnInit()` or a module's `OnMissionStart()`.

```c
// In your modded MissionServer.OnInit():
void OnInit()
{
    super.OnInit();
    LootManager.Create();  // Eager: constructed now, not on first use
}

// In LootManager:
static void Create()
{
    if (!s_Instance)
    {
        s_Instance = new LootManager();
    }
}
```

**When to prefer eager:**
- The singleton loads data from disk (configs, JSON files) and you want load errors to surface at startup
- The singleton registers RPC handlers that must be in place before any client connects
- Initialization order matters and you need to control it explicitly

---

## Lifecycle Management

The most common source of singleton bugs in DayZ is failing to clean up on mission end, and the mission lifecycle genuinely does cycle inside a single running process.

The engine exposes `PlayMission`, `CreateMission` and `AbortMission` as `proto native` methods on `CGame` (`3_game/global/game.c:1102-1110`), and `DayZGame` drives them -- `PlayMission` at `dayzgame.c:2335`, `2353` and `2562`, `AbortMission` at `1693` and `2763` -- while tracking `MISSION_STATE_MAINMENU` / `MISSION_STATE_GAME` / `MISSION_STATE_FINNISH` on the game object that outlives every mission (`dayzgame.c:912-914`). Both vanilla missions tear themselves down in `OnMissionFinish()`: `MissionGameplay` destroys its menus, chat and HUD root (`5_mission/mission/missiongameplay.c:257`) and `MissionMainMenu` cleans up its menu (`missionmainmenu.c:93`). A client therefore moves between the main-menu mission and a gameplay mission without relaunching. That transition creates a cleanup boundary for static references: do not assume a static field resets or persists without evidence for its script module and transition. Stale `s_Instance` values, dead objects and orphaned callbacks are therefore lifecycle risks.

Dedicated-server lifetime remains narrower. In DayZDiag `1.29.0.163709` PID `33556`, a scheduled `MissionServer` callback called `GetGame().RestartMission()`: the tested Mission-module static reset from its initializer and reached `101` again, while the tested World-module static advanced from `201` to `202` after the Mission module reloaded. The process then exited with `0xC0000005` before either the callback's return marker or its planned clean-exit marker, so this is evidence for those two fields in that failed direct-restart probe only -- not a healthy restart, a general static-lifetime guarantee, or evidence about administrator `#restart`, client reconnects, or game-layer fields. Many hosts still schedule a full process restart between sessions, and when the process dies, static state is wiped for you. Wiring `DestroyInstance()` into `OnMissionFinish` remains a defensive cleanup step: it releases owned references when the field survives the transition and makes shutdown ownership explicit even when a later process exit clears static state.

> **What you are actually overriding.** Vanilla `MissionServer` has no `OnMissionFinish` of its own. The only overrides in the vanilla mission module are `MissionGameplay`'s and `MissionMainMenu`'s, and neither of those chains `super`; the base `Mission.OnMissionFinish()` is an empty body (`3_game/gameplay.c:702`). So a `modded class MissionServer` override is extending an inherited empty method, not wrapping vanilla server teardown -- which means nothing vanilla depends on your call to `super`, but every *other* mod that modded the same class does. Call it anyway.

### The Lifecycle Contract

```
Server Process Start
  └─ MissionServer.OnInit()
       └─ Create singletons (eager) or let them self-create (lazy)
  └─ MissionServer.OnMissionStart()
       └─ Singletons begin operation
  └─ ... server runs ...
  └─ MissionServer.OnMissionFinish()
       └─ DestroyInstance() on every singleton
       └─ All static refs set to null
  └─ (Mission may restart)
       └─ Fresh singletons created again
```

### Cleanup Pattern

Always pair your singleton with a `DestroyInstance()` method and call it during shutdown:

```c
class VehicleRegistry
{
    private static ref VehicleRegistry s_Instance;
    protected ref array<ref VehicleData> m_Vehicles;

    static VehicleRegistry GetInstance()
    {
        if (!s_Instance) s_Instance = new VehicleRegistry();
        return s_Instance;
    }

    static void DestroyInstance()
    {
        s_Instance = null;  // Releases this strong reference; destruction waits until no strong references remain.
    }

    void ~VehicleRegistry()
    {
        if (m_Vehicles) m_Vehicles.Clear();
        m_Vehicles = null;
    }
};

// In your modded MissionServer:
modded class MissionServer
{
    override void OnMissionFinish()
    {
        VehicleRegistry.DestroyInstance();
        super.OnMissionFinish();
    }
};
```

### Centralized Shutdown Pattern

A framework mod can consolidate all singleton cleanup into a single entry point that is called from the modded `MissionServer.OnMissionFinish()`. This prevents the common mistake of forgetting one singleton. The example below uses **Lantern**, the constructed teaching framework used throughout Part 7 — `LanternCore` is its global entry point and the `LNT_` classes are its subsystems:

```c
// LanternCore centralizes teardown for every Lantern subsystem:
class LanternCore
{
    static void ShutdownAll()
    {
        LNT_RPC.Cleanup();
        LNT_EventBus.Cleanup();
        LNT_ModuleManager.Cleanup();
        LNT_ConfigManager.DestroyInstance();
        LNT_Permissions.DestroyInstance();
    }
};
```

---

## When to Use Singletons

### Good Candidates

| Use Case | Why Singleton Works |
|----------|-------------------|
| **Manager classes** (LootManager, VehicleManager) | Exactly one coordinator for a domain |
| **Caches** (CfgVehicles cache, icon cache) | Single source of truth avoids redundant computation |
| **Registries** (RPC handler registry, module registry) | Central lookup must be globally accessible |
| **Config holders** (server settings, permissions) | One config per mod, loaded once from disk |
| **RPC dispatchers** | Single entry point for all incoming RPCs |

### Poor Candidates

| Use Case | Why Not |
|----------|---------|
| **Per-player data** | One instance per player, not one global instance |
| **Temporary computations** | Create, use, discard --- no global state needed |
| **UI views / dialogs** | Multiple can coexist; use the view stack instead |
| **Entity components** | Attached to individual objects, not global |

---

## Singleton Variants in Practice

There is no single "correct" singleton — the shape you pick depends on who owns the lifecycle. Three variants cover almost every case in DayZ. The first two use **Lantern**, the constructed teaching framework whose full code lives in the Part 7 chapters; the third is a genuine vanilla idiom you can lean on with no framework at all.

### Variant A: Manager-Owned Singleton

Instead of each subsystem storing its own `s_Instance`, a central module manager keeps the one instance and hands it out by type. The subsystem itself has no static accessor — you fetch it from the manager. This is how Lantern's module system works (see [Module Systems](02-module-systems.md)):

```c
// A Lantern module. It does NOT own a static instance —
// the module manager constructs it and stores the single copy.
class LNT_BountyModule : LNT_ModuleBase
{
    protected ref map<string, int> m_Bounties;

    void LNT_BountyModule()
    {
        m_Bounties = new map<string, int>();
    }

    void SetBounty(string playerId, int amount)
    {
        m_Bounties.Set(playerId, amount);
    }

    int GetBounty(string playerId)
    {
        int amount = 0;
        m_Bounties.Find(playerId, amount);
        return amount;
    }
};

// Access it anywhere by asking the manager for its type:
void ExampleUsage()
{
    LNT_BountyModule bounty = LNT_BountyModule.Cast(LNT_ModuleManager.GetModule("LNT_BountyModule"));
    if (bounty)
    {
        bounty.SetBounty("76561198000000000", 500);
    }
}
```

The single-instance guarantee lives in the manager's registry (one entry per type), so the module never needs `private static ref` at all. The trade-off is a lookup on every access instead of a direct static field.

### Variant B: Classic `GetInstance` / `DestroyInstance`

The self-contained static-ref singleton — the canonical form from the top of this chapter, applied to a real subsystem. Lantern's ban list uses it because it owns disk-backed state and wants explicit teardown:

```c
class LNT_BanManager
{
    private static ref LNT_BanManager s_Instance;
    protected ref array<string> m_BannedIds;

    void LNT_BanManager()
    {
        m_BannedIds = new array<string>();
    }

    void ~LNT_BanManager()
    {
        if (m_BannedIds) m_BannedIds.Clear();
        m_BannedIds = null;
    }

    static LNT_BanManager GetInstance()
    {
        if (!s_Instance)
        {
            s_Instance = new LNT_BanManager();
        }
        return s_Instance;
    }

    static void DestroyInstance()
    {
        s_Instance = null;
    }

    bool IsBanned(string playerId)
    {
        return m_BannedIds.Find(playerId) != -1;
    }
};
```

### Variant C: Vanilla Plugin Singletons

DayZ's own engine ships a singleton-access idiom you can use without any framework: the **plugin system**. Vanilla registers each `PluginBase` subclass once in `PluginManager`, and the global `GetPlugin(typename)` function returns that single instance. `PluginAdminLog` — the server admin-log plugin — is a real example:

```c
// Fetch the one PluginAdminLog instance the engine created:
void LogPlacement(PlayerBase player)
{
    PluginAdminLog adminLog = PluginAdminLog.Cast(GetPlugin(PluginAdminLog));
    if (adminLog)
    {
        adminLog.DirectAdminLogPrint(player.GetType() + " placed an object");
    }
}
```

`GetPlugin()` is defined in `pluginmanager.c` and returns `PluginBase`; you cast it to the concrete plugin type. The manager holds exactly one instance per registered `typename`, so this is a true singleton lookup — the same shape as Variant A, but provided by the engine. If you only need one long-lived server-side service, subclassing `PluginBase` gets you singleton lifecycle for free, with no static ref to manage.

---

## Thread Safety Considerations

Enforce Script is single-threaded. All script execution happens on the main thread within the Enfusion engine's game loop. This means:

- There are **no race conditions** between concurrent threads
- You do **not** need mutexes, locks, or atomic operations
- `GetInstance()` with lazy initialization is always safe

However, **re-entrancy** can still cause problems. If `GetInstance()` triggers code that calls `GetInstance()` again during construction, you can get a partially-initialized singleton:

```c
// DANGEROUS: re-entrant singleton construction
class BadManager
{
    private static ref BadManager s_Instance;

    void BadManager()
    {
        // This calls GetInstance() during construction!
        OtherSystem.Register(BadManager.GetInstance());
    }

    static BadManager GetInstance()
    {
        if (!s_Instance)
        {
            // s_Instance is still null here during construction
            s_Instance = new BadManager();
        }
        return s_Instance;
    }
};
```

The fix is to assign `s_Instance` before running any initialization that might re-enter:

```c
static BadManager GetInstance()
{
    if (!s_Instance)
    {
        s_Instance = new BadManager();  // Assign first
        s_Instance.Initialize();         // Then run initialization that may call GetInstance()
    }
    return s_Instance;
}
```

Or better yet, avoid circular initialization entirely.

---

## Anti-Patterns

### 1. Global Mutable State Without Encapsulation

The singleton pattern gives you global access. That does not mean the data should be globally writable.

```c
// BAD: Public fields invite uncontrolled mutation
class GameState
{
    private static ref GameState s_Instance;
    int PlayerCount;         // Anyone can write this
    bool ServerLocked;       // Anyone can write this
    string CurrentWeather;   // Anyone can write this

    static GameState GetInstance() { ... }
};

// Any code can do:
GameState.GetInstance().PlayerCount = -999;  // Chaos
```

```c
// GOOD: Controlled access through methods
class GameState
{
    private static ref GameState s_Instance;
    protected int m_PlayerCount;
    protected bool m_ServerLocked;

    int GetPlayerCount() { return m_PlayerCount; }

    void IncrementPlayerCount()
    {
        m_PlayerCount++;
    }

    static GameState GetInstance() { ... }
};
```

### 2. Missing DestroyInstance

If cleanup is missing, stale state is a lifecycle risk. A direct `GetGame().RestartMission()` probe in DayZDiag `1.29.0.163709` PID `33556` reloaded the Mission module: its tested static reached `101` in both `OnInit()` calls, while a tested World-module static advanced from `201` to `202`. Because that process crashed with `0xC0000005` before the restart call returned or the planned clean exit, do not generalize this two-field observation into a healthy-restart result or a rule for other fields, `#restart`, reconnects, or game-layer state:

```c
// BAD: No cleanup path
class ZombieTracker
{
    private static ref ZombieTracker s_Instance;
    ref array<Object> m_TrackedZombies;  // These objects get deleted on mission end!

    static ZombieTracker GetInstance() { ... }
    // No DestroyInstance() — m_TrackedZombies now holds dead references
};
```

### 3. Singletons That Own Everything

When a singleton accumulates too many responsibilities, it becomes a "God object" that is impossible to reason about:

```c
// BAD: One singleton doing everything
class ServerManager
{
    // Manages loot AND vehicles AND weather AND spawns AND bans AND...
    ref array<Object> m_Loot;
    ref array<Object> m_Vehicles;
    ref WeatherData m_Weather;
    ref array<string> m_BannedPlayers;

    void SpawnLoot() { ... }
    void DespawnVehicle() { ... }
    void SetWeather() { ... }
    void BanPlayer() { ... }
    // 2000 lines later...
};
```

Split into focused singletons: `LootManager`, `VehicleManager`, `WeatherManager`, `BanManager`. Each one is small, testable, and has a clear domain.

### 4. Accessing Singletons in Constructors of Other Singletons

This creates hidden initialization-order dependencies:

```c
// BAD: Constructor depends on another singleton
class ModuleA
{
    void ModuleA()
    {
        // What if ModuleB hasn't been created yet?
        ModuleB.GetInstance().Register(this);
    }
};
```

Defer cross-singleton registration to `OnInit()` or `OnMissionStart()`, where initialization order is controlled.

---

## Alternative: Static-Only Classes

Some "singletons" do not need an instance at all. If the class holds no instance state and only has static methods and static fields, skip the `GetInstance()` ceremony entirely:

```c
// No instance needed — all static
class LNT_Log
{
    private static FileHandle s_LogFile;
    private static int s_LogLevel;

    static void Info(string tag, string msg)
    {
        WriteLog("INFO", tag, msg);
    }

    static void Error(string tag, string msg)
    {
        WriteLog("ERROR", tag, msg);
    }

    static void Cleanup()
    {
        if (s_LogFile) CloseFile(s_LogFile);
        s_LogFile = null;
    }

    private static void WriteLog(string level, string tag, string msg)
    {
        // ...
    }
};
```

This is the approach used by `LNT_Log`, `LNT_RPC`, `LNT_EventBus`, and `LNT_ModuleManager` in the Lantern framework. It is simpler, avoids the `GetInstance()` null-check overhead, and makes the intent clear: there is no instance, only shared state.

**Use a static-only class when:**
- All methods are stateless or operate on static fields
- There is no meaningful constructor/destructor logic
- You never need to pass the "instance" as a parameter

**Use a true singleton when:**
- The class has instance state that benefits from encapsulation (`protected` fields)
- You need polymorphism (a base class with overridden methods)
- The object needs to be passed to other systems by reference

---

## Checklist

Before shipping a singleton, verify:

- [ ] `s_Instance` is declared `private static ref`
- [ ] `GetInstance()` handles the null case (lazy init) or you have an explicit `Create()` call
- [ ] `DestroyInstance()` exists and sets `s_Instance = null`
- [ ] `DestroyInstance()` is called from `OnMissionFinish()` or a centralized shutdown method
- [ ] The destructor cleans up owned collections (`.Clear()`, set to `null`)
- [ ] No public fields --- all mutation goes through methods
- [ ] The constructor does not call `GetInstance()` on other singletons (defer to `OnInit()`)

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing `DestroyInstance()` call in `OnMissionFinish` | Mutable state may outlive the lifecycle your design expects; one failed direct-restart probe reinitialized its tested Mission static while its tested World static persisted, but behavior beyond those fields is unverified | As defensive design, call `DestroyInstance()` from `OnMissionFinish` or a centralized `ShutdownAll()` |
| Calling `GetInstance()` inside another singleton's constructor | Triggers re-entrant construction; `s_Instance` is still null, so a second instance is created | Defer cross-singleton access to an `Initialize()` method called after construction |
| Using `public static ref` instead of `private static ref` | Any code can set `s_Instance = null` or replace it, breaking the single-instance guarantee | Always declare `s_Instance` as `private static ref` |
| Not guarding eager init on listen servers | Singleton is constructed twice (once from server path, once from client path) if `Create()` lacks a null check | Always check `if (!s_Instance)` inside `Create()` |
| Accumulating state without bounds (unbounded caches) | Memory grows indefinitely on long-running servers; eventual OOM or severe lag | Cap collections with a max size or periodic eviction in `OnUpdate` |

---

## Multi-Mod Considerations

- Multiple mods each defining their own singletons coexist safely --- each has its own `s_Instance`. Conflicts only arise if two mods define the same class name.
- Lazy singletons are unaffected by mod load order. Eager singletons created in `OnInit()` depend on the `modded class` chain order, which follows `config.cpp` `requiredAddons`.
- On listen servers, static fields are shared between client and server contexts. A server-only singleton must guard construction with `GetGame().IsServer()`.
- Enforce Script has no built-in dependency-injection container, but you can still pass dependencies explicitly through constructors or initialization methods. Singletons are one option, not a language requirement.
- RPC handlers must be registered before any client connects, so eager init in `OnInit()` is often necessary.
- Missions cycle within one process -- the client alone moves between the main-menu mission and a gameplay mission -- so singletons **must** be destroyed and recreated on each mission cycle. A server host that schedules a full process restart wipes static state anyway; `DestroyInstance()` in `OnMissionFinish` is what covers the case where it does not. See [Lifecycle Management](#lifecycle-management).
