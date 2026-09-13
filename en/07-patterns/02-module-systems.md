# Module / Plugin Systems

> **Summary:** A module system splits a mod into self-contained units that a central manager drives through one shared lifecycle --- `OnInit`, `OnMissionStart`, `OnUpdate`, `OnMissionFinish`. This chapter teaches that universal contract, then shows three ways to realize it that you can actually use: the vanilla plugin system, framework-style layered managers, and a dependency-free static manager you build yourself.

---

## Introduction

Every serious DayZ mod eventually needs a way to organize code into self-contained units with defined lifecycle hooks. Rather than scattering initialization logic across modded mission classes, each unit registers itself with a central manager that dispatches lifecycle events --- `OnInit`, `OnMissionStart`, `OnUpdate`, `OnMissionFinish` --- to every unit in a predictable order.

The shape of that lifecycle is the same everywhere; only the machinery around it differs. This chapter starts with the lifecycle contract itself, then compares three concrete implementations: DayZ's built-in **plugin system** (`PluginBase` / `PluginManager`), the **layered module managers** that public frameworks provide, and a **custom static manager** you can build with zero dependencies. Understanding all three lets you choose the right pattern for your own mod or integrate cleanly with a framework a target server already runs.

---

## Table of Contents

- [Why Modules?](#why-modules)
- [The Vanilla Plugin System](#the-vanilla-plugin-system)
- [Framework Lifecycle Module Managers](#framework-lifecycle-module-managers)
- [Custom Static Module Manager](#custom-static-module-manager)
- [Module Lifecycle: The Universal Contract](#module-lifecycle-the-universal-contract)
- [Best Practices for Module Design](#best-practices-for-module-design)
- [Comparison Table](#comparison-table)

---

## Why Modules?

Without a module system, a DayZ mod typically ends up with a monolithic modded `MissionServer` or `MissionGameplay` class that grows until it becomes unmanageable:

```c
// BAD: Everything crammed into one modded class
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        InitLootSystem();
        InitVehicleTracker();
        InitBanManager();
        InitWeatherController();
        InitAdminPanel();
        InitKillfeedHUD();
        // ... 20 more systems
    }

    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);
        TickLootSystem(timeslice);
        TickVehicleTracker(timeslice);
        TickWeatherController(timeslice);
        // ... 20 more ticks
    }
};
```

A module system replaces this with a single, stable hook point. Here the modded mission delegates to a manager, and each `LNT_*Module` below is one of your own feature modules (the manager and its base classes are built later in this chapter):

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        LNT_ModuleManager.Register(new LNT_LootModule());
        LNT_ModuleManager.Register(new LNT_VehicleModule());
        LNT_ModuleManager.Register(new LNT_WeatherModule());
    }

    override void OnMissionStart()
    {
        super.OnMissionStart();
        LNT_ModuleManager.OnMissionStart();  // Dispatches to all modules
    }

    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);
        LNT_ModuleManager.OnServerUpdate(timeslice);  // Dispatches to server modules
    }
};
```

Each module is an independent class with its own file, its own state, and its own lifecycle hooks. Adding a new feature means adding a new module --- not editing a 3000-line mission class.

---

## The Vanilla Plugin System

Before reaching for any framework, know that DayZ already ships a module system: the **plugin** system in `4_World`. Vanilla uses it for everything from `PluginRepairing` to `PluginPlayerStatus`, and it is available on every server with no dependencies. Several community admin frameworks build their own plugin architecture by modding this exact class --- so learning the vanilla truth teaches you how those work too.

### The Building Blocks

Two classes drive the whole system:

- **`PluginBase`** --- the base every plugin extends. It defines `OnInit()`, `OnUpdate(float delta_time)`, and `OnDestroy()`, plus `GetModuleName()` (which returns the class name) and `GetModuleType()`.
- **`PluginManager`** --- the registry. It holds an `array<typename>` of registered plugin types and a `map<typename, ref PluginBase>` of live instances. It owns the `ref` to every plugin, so it controls their lifetime.

The engine creates the manager for you: `MissionBase`'s constructor calls the global `PluginManagerInit()`, which news the manager, runs `Init()` (registration), then `PluginsInit()` (instantiation + `OnInit()`). The manager also inserts its `MainOnUpdate` into the game update queue, so every registered plugin gets ticked each frame.

### How Registration Works

Inside `PluginManager.Init()`, each plugin is registered by **class name (a string)** plus two flags --- register on client, register on server:

```c
// Shape of the vanilla PluginManager.Init() (abridged)
class PluginManager
{
    void Init()
    {
        //              Class name              Client  Server
        RegisterPlugin("PluginRepairing",       true,   true);
        RegisterPlugin("PluginPlayerStatus",    true,   true);
        RegisterPlugin("PluginAdminLog",        false,  true);
        // ...
    }
}
```

`RegisterPlugin` converts the string to a `typename` with `.ToType()` and stores it. The client/server flags let the manager skip plugins that do not belong on the current side --- a `false` client flag means the plugin is never created on a multiplayer client. This is how the vanilla system stays listen-server safe: side selection happens once, at registration.

To add your own plugin, mod `PluginManager` and extend `Init()`. Because `RegisterPlugin` is `protected`, a modded subclass can call it directly:

```c
modded class PluginManager
{
    override void Init()
    {
        super.Init();  // keep all vanilla plugins
        //              Class name              Client  Server
        RegisterPlugin("LNT_AutoConfigPlugin",  false,  true);
    }
};
```

The manager instantiates the plugin itself (via `typename.Spawn()`) and calls its `OnInit()`. You never write a `new` call for a plugin.

### A Self-Loading Config Plugin

A common enhancement is a plugin that reads its own JSON settings on init. Here is an original `LNT_AutoConfigPlugin` that extends `PluginBase` and loads a config file with `JsonFileLoader`, writing defaults on first run:

```c
// Plain data class: the plugin's on-disk settings
class LNT_PatrolConfig
{
    int maxPatrols;
    float spawnInterval;
    ref array<string> patrolZones;

    void LNT_PatrolConfig()
    {
        // Defaults, used when no file exists yet
        maxPatrols = 4;
        spawnInterval = 300.0;
        patrolZones = new array<string>;
    }
}

// A vanilla plugin that self-loads JSON config on init
class LNT_AutoConfigPlugin : PluginBase
{
    protected ref LNT_PatrolConfig m_Config;

    override void OnInit()
    {
        super.OnInit();
        LoadConfig();
    }

    protected string GetConfigPath()
    {
        return "$profile:LanternAdmin/" + GetModuleName() + ".json";
    }

    protected void LoadConfig()
    {
        m_Config = new LNT_PatrolConfig();  // start from defaults
        string path = GetConfigPath();

        if (!FileExist(path))
        {
            SaveConfig();  // first run: write the defaults out
            return;
        }

        string error;
        if (!JsonFileLoader<LNT_PatrolConfig>.LoadFile(path, m_Config, error))
        {
            Print("[Lantern] Config load failed: " + error);
        }
    }

    void SaveConfig()
    {
        if (!FileExist("$profile:LanternAdmin"))
            MakeDirectory("$profile:LanternAdmin");

        string path = GetConfigPath();
        string error;
        if (!JsonFileLoader<LNT_PatrolConfig>.SaveFile(path, m_Config, error))
        {
            Print("[Lantern] Config save failed: " + error);
        }
    }

    LNT_PatrolConfig GetConfig()
    {
        return m_Config;
    }
};
```

Note the JSON call shape: the modern `JsonFileLoader<T>.LoadFile()` takes the destination object by reference and an `out` error string, and returns a `bool` --- it does **not** return the loaded data. (The older `JsonLoadFile()` returns `void` entirely; either way you pass in a live object to fill, never assign the return.) See [Config & Persistence](04-config-persistence.md) for the full config pattern.

### Retrieving a Running Plugin

To reach a plugin from elsewhere, use the global `GetPlugin(typename)` and cast, or go through `GetPluginManager().GetPluginByType()`:

```c
LNT_AutoConfigPlugin cfgPlugin;
if (Class.CastTo(cfgPlugin, GetPlugin(LNT_AutoConfigPlugin)))
{
    LNT_PatrolConfig cfg = cfgPlugin.GetConfig();
    // use cfg.maxPatrols, cfg.spawnInterval, ...
}
```

### Key Characteristics

- **Zero dependencies**: the plugin system is part of vanilla DayZ; nothing else needs to load.
- **String-name registration**: plugins are registered by class name in a modded `PluginManager.Init()`; the manager instantiates them.
- **Side flags**: the client/server flags at registration keep plugins off the wrong side.
- **Clear ownership**: the manager holds `ref` to every plugin and calls `OnDestroy()` on teardown.
- **Automatic ticking**: `MainOnUpdate` dispatches `OnUpdate(dt)` to every live plugin each frame.

---

## Framework Lifecycle Module Managers

Public modding frameworks offer a richer take on the same idea: **per-layer base classes** with an **opt-in event system**. Instead of one `OnUpdate`, a module can subscribe to a large menu of lifecycle events --- mission start/finish, per-frame update, and a whole family of player events (invoke-connect, client-new, client-respawn, client-ready, client-disconnect, client-logout) --- by calling small `Enable*()` methods in its `OnInit()`. It receives only the events it opted in to, and each handler is passed an event-args object carrying context. Modules are discovered automatically from config, so there is no manual registration list.

Frameworks typically provide three base classes, one per script layer, mirroring DayZ's compilation order:

| Layer | Typical Use |
|-------|-------------|
| Game (`3_Game`) | Early init, RPC registration, data classes |
| World (`4_World`) | Entity interaction, gameplay systems, player events |
| Mission (`5_Mission`) | UI, HUD, mission-level hooks |

A module written against such a framework looks like the sketch below. The identifiers `LNT_ModuleWorld`, the `Enable*()` calls, and the `LNT_EventArgs` type all stand in for whatever the framework you adopt actually names them --- **you write only the subclass body**; the framework supplies the base and the machinery:

```c
// Illustrative sketch. The base class, Enable*() methods, and event-args type
// are provided by the framework; you implement the subclass. A module opts in
// to just the events it needs, then receives context via the args object.
class LNT_LootRespawnModule : LNT_ModuleWorld
{
    override void OnInit()
    {
        super.OnInit();
        // Opt in — only these three events will fire on this module.
        EnableUpdate();
        EnableMissionStart();
        EnableMissionFinish();
    }

    override void OnMissionStart(Class sender, LNT_EventArgs args)
    {
        super.OnMissionStart(sender, args);
        // Load configs, spawn initial loot.
    }

    override void OnUpdate(Class sender, LNT_EventArgs args)
    {
        super.OnUpdate(sender, args);
        // Tick respawn timers.
    }

    override void OnMissionFinish(Class sender, LNT_EventArgs args)
    {
        super.OnMissionFinish(sender, args);
        // Save state, release resources.
    }
};
```

### Declarative Registration

Some frameworks remove the registration step entirely. Instead of listing modules in a mission hook, you mark the class itself --- with a registration annotation or a config-side declaration --- and the framework discovers it at startup by scanning loaded classes, instantiating each match before any lifecycle event fires. This trades a little indirection for zero boilerplate: the class declaring itself a module becomes the single source of truth, and you can find every module by searching for the marker. The cost is that discovery depends entirely on the framework's scan step, so it works only while that framework is loaded.

> **Concept credit.** Public frameworks such as [Community Framework](https://github.com/Jacob-Mango/DayZ-Community-Framework) pioneered the layered, opt-in module design described here. This wiki teaches the *pattern*; it uses no framework code or class names.

### Key Characteristics

- **Auto-discovery**: modules are found from config declarations --- no manual registration list.
- **Opt-in events**: a module receives only the lifecycle events it enables, including rich player events.
- **Event args**: handlers get a context object rather than bare parameters.
- **Framework dependency**: your mod requires the framework to be loaded, and its version pins your API.

---

## Custom Static Module Manager

When you want zero dependencies and full control, build the manager yourself. This is the approach the rest of this wiki's **Lantern** examples use: an explicit registration pattern backed by a purely **static** manager class --- no instance, no `GetInstance()`, just static methods over static storage. Everything below is defined here, so it runs inside a minimal mod as-is.

### Module Base Classes

The base declares the lifecycle; two typed subclasses split server from client. The base returns `true` from *both* `IsServer()` and `IsClient()`; each subclass narrows one to `false`. **Do not subclass the base directly** --- always extend `LNT_ServerModule` or `LNT_ClientModule` so the side is unambiguous:

```c
// Base: the lifecycle contract shared by every module
class LNT_ModuleBase : Managed
{
    // Base answers true to both — subclasses narrow this.
    bool IsServer()
    {
        return true;
    }

    bool IsClient()
    {
        return true;
    }

    string GetModuleName()
    {
        return ClassName();
    }

    void OnInit();
    void OnMissionStart();
    void OnMissionFinish();
}

// Server-side module: adds OnUpdate + player events
class LNT_ServerModule : LNT_ModuleBase
{
    override bool IsServer()
    {
        return true;
    }

    override bool IsClient()
    {
        return false;
    }

    void OnUpdate(float dt);
    void OnPlayerConnect(PlayerIdentity identity);
    void OnPlayerDisconnect(PlayerIdentity identity, string uid);
}

// Client-side module: adds OnUpdate
class LNT_ClientModule : LNT_ModuleBase
{
    override bool IsServer()
    {
        return false;
    }

    override bool IsClient()
    {
        return true;
    }

    void OnUpdate(float dt);
}
```

### The Manager

The manager keeps one static list of modules and dispatches each lifecycle stage to it. Update dispatch uses a **cast** to the typed subclass, so `OnServerUpdate` only ever ticks server modules and `OnClientUpdate` only client modules --- the split that keeps listen servers safe:

```c
class LNT_ModuleManager
{
    protected static ref array<ref LNT_ModuleBase> s_Modules = new array<ref LNT_ModuleBase>();

    // Register + init in one step (call during mission OnInit)
    static void Register(LNT_ModuleBase mod)
    {
        if (!mod)
        {
            return;
        }
        s_Modules.Insert(mod);
        mod.OnInit();
    }

    // Loose-coupling lookup by class name
    static LNT_ModuleBase GetModule(string moduleName)
    {
        foreach (LNT_ModuleBase mod : s_Modules)
        {
            if (mod.GetModuleName() == moduleName)
            {
                return mod;
            }
        }
        return null;
    }

    static void OnMissionStart()
    {
        foreach (LNT_ModuleBase mod : s_Modules)
        {
            mod.OnMissionStart();
        }
    }

    // Ticks only server modules — the cast fails for client modules
    static void OnServerUpdate(float dt)
    {
        foreach (LNT_ModuleBase mod : s_Modules)
        {
            LNT_ServerModule serverMod;
            if (Class.CastTo(serverMod, mod))
            {
                serverMod.OnUpdate(dt);
            }
        }
    }

    // Ticks only client modules
    static void OnClientUpdate(float dt)
    {
        foreach (LNT_ModuleBase mod : s_Modules)
        {
            LNT_ClientModule clientMod;
            if (Class.CastTo(clientMod, mod))
            {
                clientMod.OnUpdate(dt);
            }
        }
    }

    static void OnMissionFinish()
    {
        foreach (LNT_ModuleBase mod : s_Modules)
        {
            mod.OnMissionFinish();
        }
    }

    // Tear everything down — call from OnMissionFinish
    static void Cleanup()
    {
        s_Modules.Clear();
    }
}
```

### Registration

Modules register themselves explicitly, typically from modded mission classes. Every registered class must extend `LNT_ServerModule` or `LNT_ClientModule`:

```c
// In modded MissionServer.OnInit():
LNT_ModuleManager.Register(new LNT_LootModule());     // extends LNT_ServerModule
LNT_ModuleManager.Register(new LNT_CleanupModule());  // extends LNT_ServerModule
```

### Lifecycle Dispatch

The modded mission classes call into `LNT_ModuleManager` at each lifecycle point:

```c
modded class MissionServer
{
    override void OnMissionStart()
    {
        super.OnMissionStart();
        LNT_ModuleManager.OnMissionStart();
    }

    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);
        LNT_ModuleManager.OnServerUpdate(timeslice);
    }

    override void OnMissionFinish()
    {
        LNT_ModuleManager.OnMissionFinish();
        LNT_ModuleManager.Cleanup();
        super.OnMissionFinish();
    }
};
```

### Listen-Server Safety

On a listen server, both `MissionServer` and `MissionGameplay` run in the same process. `MissionServer.OnUpdate` calls `OnServerUpdate` (server modules only) and `MissionGameplay.OnUpdate` calls `OnClientUpdate` (client modules only). Because each dispatch casts to the typed subclass, a module is never ticked from both sides --- no double dispatch, no server logic running on the client half.

The base `LNT_ModuleBase` answers `true` to *both* `IsServer()` and `IsClient()`, which is exactly why you **do not subclass the base directly**: a bare base module would look like it belongs on both sides.

### Key Characteristics

- **Zero dependencies**: no external frameworks.
- **Static manager**: no `GetInstance()`; a purely static API.
- **Explicit registration**: full control over what gets registered and when.
- **Listen-server safe**: typed subclasses prevent double-dispatch.
- **Centralized cleanup**: `LNT_ModuleManager.Cleanup()` tears down all modules.

---

## Module Lifecycle: The Universal Contract

The following mission lifecycle is the contract of the custom managers in this chapter. Vanilla PluginBase supplies OnInit(), OnUpdate(), and OnDestroy(); mission-start and mission-finish forwarding requires your own integration.

```
┌─────────────────────────────────────────────────────┐
│  Registration / Discovery                            │
│  Module instance is created and registered            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  OnInit()                                            │
│  One-time setup: allocate collections, register RPCs │
│  Called once per module after registration            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  OnMissionStart()                                    │
│  Mission is live: load configs, start timers,        │
│  subscribe to events, spawn initial entities         │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  OnUpdate(float dt)         [repeating every frame]  │
│  Per-frame tick: process queues, update timers,      │
│  check conditions, advance state machines            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  OnMissionFinish()                                   │
│  Teardown: save state, unsubscribe events,           │
│  clear collections, null out references              │
└─────────────────────────────────────────────────────┘
```

### Rules

1. **OnInit comes before OnMissionStart, and the world is not ready yet.** For the vanilla plugin system specifically, `PluginManagerInit()` (which drives every `PluginBase.OnInit()`) runs from `MissionBase`'s constructor, before `InitialiseWorldData()` even executes -- so never spawn entities, touch `GetGame().GetWorld()`, or otherwise assume the world exists inside `OnInit()`. Loading configuration is a different story: it is plain file I/O with no world dependency, which is exactly why `LNT_AutoConfigPlugin` above loads its JSON config directly in `OnInit()`, and why [Best Practice 3](#_3-register-rpcs-in-oninit-not-onmissionstart) has you register RPC handlers there too. Treat `OnInit()` as safe for config/file loading and RPC registration, and unsafe for anything that expects the world or its entities to exist -- defer that to `OnMissionStart()`.
2. **OnUpdate receives delta time.** Always use `dt` for time-based logic, never assume a fixed frame rate.
3. **OnMissionFinish must clean up everything.** Every `ref` collection must be cleared. Every event subscription must be removed. Every singleton must be destroyed. This is the only reliable teardown point.
4. **Modules should not depend on each other's initialization order.** If Module A needs Module B, use lazy access (`GetModule()`) rather than assuming B was registered first.

---

## Best Practices for Module Design

### 1. One Module, One Responsibility

A module should own exactly one domain. If you find yourself writing `LNT_VehicleAndWeatherAndLootModule`, split it.

```c
// GOOD: Focused modules
class LNT_LootModule : LNT_ServerModule { }
class LNT_VehicleModule : LNT_ServerModule { }
class LNT_WeatherModule : LNT_ServerModule { }

// BAD: God module
class LNT_EverythingModule : LNT_ServerModule { }
```

### 2. Keep OnUpdate Cheap

`OnUpdate` runs every frame. If your module does expensive work (file I/O, world scans, pathfinding), do it on a timer or batch it across frames:

```c
class LNT_CleanupModule : LNT_ServerModule
{
    protected float m_CleanupTimer;
    protected const float CLEANUP_INTERVAL = 300.0;  // Every 5 minutes

    override void OnUpdate(float dt)
    {
        m_CleanupTimer += dt;
        if (m_CleanupTimer >= CLEANUP_INTERVAL)
        {
            m_CleanupTimer = 0;
            RunCleanup();
        }
    }

    protected void RunCleanup()
    {
        // Expensive work, safely off the per-frame path
    }
};
```

### 3. Register RPCs in OnInit, Not OnMissionStart

RPC handlers must be in place before any client can send a message. `OnInit()` runs during module registration, which happens early in mission setup. `OnMissionStart()` may be too late if clients connect fast.

```c
// The router keys handlers on mod name + function name and dispatches
// to LNT_RpcHandler.OnReceive --- see RPC Patterns for the full router.
class LNT_LootRpc : LNT_RpcHandler
{
    override void OnReceive(PlayerIdentity sender, Object target, ParamsReadContext ctx)
    {
        // Handle RPC
    }
}

class LNT_LootModule : LNT_ServerModule
{
    protected ref LNT_LootRpc m_Rpc = new LNT_LootRpc();

    override void OnInit()
    {
        super.OnInit();
        // Canonical 3-arg signature: mod name, function name, handler.
        LNT_RPC.Register("Lantern", "RPC_DoThing", m_Rpc);
    }
};
```

`LNT_RPC` is Lantern's string-routed RPC helper --- see [RPC Patterns](03-rpc-patterns.md).

### 4. Use the Module Manager for Cross-Module Access

Do not hold direct references to other modules. Use the manager's lookup:

```c
// GOOD: Loose coupling through the manager
LNT_ModuleBase mod = LNT_ModuleManager.GetModule("LNT_AIServerModule");
LNT_AIServerModule aiMod;
if (Class.CastTo(aiMod, mod))
{
    aiMod.PauseSpawning();
}

// BAD: Direct static reference creates hard coupling
LNT_AIServerModule.s_Instance.PauseSpawning();
```

### 5. Guard Against Missing Dependencies

Not every server runs every mod. If your module optionally integrates with another mod, use preprocessor checks:

```c
override void OnMissionStart()
{
    super.OnMissionStart();

    #ifdef LANTERN_AI
    LNT_EventBus.OnMissionStarted.Insert(OnAIMissionStarted);
    #endif
}
```

### 6. Log Module Lifecycle Events

Logging makes debugging straightforward. Every module should log when it initializes and shuts down:

```c
override void OnInit()
{
    super.OnInit();
    LNT_Log.Info("LNT_LootModule", "Initialized");
}

override void OnMissionFinish()
{
    LNT_Log.Info("LNT_LootModule", "Shutting down");
    // Cleanup...
}
```

---

## Comparison Table

| Feature | Vanilla PluginManager | Framework managers | LNT_ModuleManager (custom) |
|---------|-----------------------|--------------------|----------------------------|
| **Discovery** | `RegisterPlugin()` by class name in `Init()` | Config / attribute auto-discovery | Manual `Register(new ...)` |
| **Base classes** | `PluginBase` (roll your own variants) | Per-layer Game / World / Mission | `LNT_ServerModule` / `LNT_ClientModule` |
| **Dependencies** | None (built into DayZ) | Requires the framework | None |
| **Listen-server safe** | Client/server flags at registration | Framework handles it | Typed subclasses (cast on dispatch) |
| **Config integration** | Roll your own (`LNT_AutoConfigPlugin`) | Varies by framework | Via `LNT_ConfigManager` |
| **Update dispatch** | Manager's `MainOnUpdate` ticks all | Automatic, opt-in via `EnableUpdate()` | Manager's `OnServerUpdate` / `OnClientUpdate` |
| **Cleanup** | `OnDestroy` on manager teardown | Framework handles it | `LNT_ModuleManager.Cleanup()` |
| **Cross-mod access** | `GetPlugin(Type)` | Framework lookup | `LNT_ModuleManager.GetModule()` |

Choose the approach that matches your mod's dependency profile. For zero external dependencies and full control, build a static manager like `LNT_ModuleManager`. For lightweight, always-available registration, extend the vanilla `PluginManager`. If you already ship alongside a module framework and want its richer, opt-in lifecycle events, write your modules against it.

---

## Compatibility & Impact

- **Multi-Mod:** Multiple mods can each register their own modules with the same manager (the vanilla plugin manager, a framework, or a custom manager). Name collisions only happen if two mods register the same class type --- use unique class names prefixed with your mod tag.
- **Load Order:** Frameworks that auto-discover modules from config follow `requiredAddons` order. The vanilla plugin manager registers in a modded `Init()`, and a static manager registers in `OnInit()`, where the `modded class` chain determines order. Modules should not depend on registration order --- use lazy access patterns.
- **Listen Server:** On listen servers, both `MissionServer` and `MissionGameplay` run in the same process. If your manager dispatches `OnUpdate` from both without separating sides, modules receive double ticks. Use typed subclasses (`LNT_ServerModule` / `LNT_ClientModule`) or the vanilla client/server registration flags to prevent this.
- **Performance:** Module dispatch adds one loop iteration per registered module per lifecycle call. With 10--20 modules this is negligible. Ensure individual module `OnUpdate` methods are cheap (see [Performance](07-performance.md)).
- **Migration:** When upgrading DayZ versions, module systems stay stable as long as the base-class API (`PluginBase`, your manager, or a framework's module base) does not change. Pin any framework dependency to a known version to avoid breakage.

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing `OnMissionFinish` cleanup in a module | Collections, timers, and event subscriptions survive across mission restarts, causing stale data or crashes | Override `OnMissionFinish`, clear all `ref` collections, unsubscribe all events |
| Dispatching lifecycle events twice on listen servers | Server modules run client logic and vice versa; duplicate spawns, double RPC sends | Use `IsServer()` / `IsClient()` guards or typed module subclasses that enforce the split |
| Registering RPCs in `OnMissionStart` instead of `OnInit` | Clients that connect during mission setup can send RPCs before handlers are ready --- messages are silently dropped | Always register RPC handlers in `OnInit()`, which runs during module registration before any client connects |
| One "God module" handling everything | Impossible to debug, test, or extend; merge conflicts when multiple developers work on it | Split into focused modules with a single responsibility each |
| Holding direct `ref` to another module instance | Creates hard coupling and potential ref-cycle memory leaks | Use the manager's lookup (`GetModule()`, `GetPlugin()`) for cross-module access |

---

## Theory vs Practice

| Textbook Says | DayZ Reality |
|---------------|-------------|
| Module discovery should be automatic via reflection | Enforce Script reflection is limited; config-based discovery (as framework module systems do) or explicit `Register()` calls are the only reliable approaches |
| Modules should be hot-swappable at runtime | DayZ does not support hot-reloading scripts; modules live for the entire mission lifecycle |
| Use interfaces for module contracts | Enforce Script has no `interface` keyword; use base class virtual methods (`override`) instead |
| Dependency injection decouples modules | No DI framework exists; use manager lookups and `#ifdef` guards for optional cross-mod dependencies |
