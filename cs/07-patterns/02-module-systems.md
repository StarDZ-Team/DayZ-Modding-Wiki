# Chapter 7.2: Module / Plugin Systems

[Domů](../../README.md) | [<< Předchozí: Vzor Singleton](01-singletons.md) | **Module / Plugin Systems** | [Další: Vzory RPC >>](03-rpc-patterns.md)

---

## Úvod

Every serious DayZ mod framework uses a module or plugin system to organize code into self-contained units with defined lifecycle hooks. Rather than scattering initialization logic across modded mission classes, modules register themselves with a central manager that dispatches lifecycle dokoncets --- `OnInit`, `OnMissionStart`, `OnUpdate`, `OnMissionFinish` --- to každý module in a predictable order.

This chapter examines four real-world approaches: Community Framework's `CF_ModuleCore`, VPP's `PluginBase` / `ConfigurablePlugin`, Dabs Framework's attribute-based registration, and a vlastní statická module manager. Each solves the stejný problem odlišnýly; understanding all four will help you choose the right pattern for your own mod or integrate cleanly with an existing framework.

---

## Obsah

- [Why Modules?](#why-modules)
- [CF_ModuleCore (COT / Expansion)](#cf_modulecore-cot--expansion)
- [VPP PluginBase / ConfigurablePlugin](#vpp-pluginbase--configurableplugin)
- [Dabs Attribute-Based Registration](#dabs-attribute-based-registration)
- [Custom Static Module Manager](#vlastní-statická-module-manager)
- [Module Lifecycle: The Universal Contract](#module-lifecycle-the-universal-contract)
- [Best Practices for Module Design](#best-practices-for-module-design)
- [Comparison Table](#comparison-table)

---

## Why Modules?

Bez a module system, a DayZ mod typicky ends up with a monolithic modded `MissionServer` or `MissionGameplay` class that grows until it becomes unmanageable:

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

A module system replaces this with a jeden, stable hook point:

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        MyModuleManager.Register(new LootModule());
        MyModuleManager.Register(new VehicleModule());
        MyModuleManager.Register(new WeatherModule());
    }

    override void OnMissionStart()
    {
        super.OnMissionStart();
        MyModuleManager.OnMissionStart();  // Dispatches to all modules
    }

    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);
        MyModuleManager.OnServerUpdate(timeslice);  // Dispatches to all modules
    }
};
```

Each module is an nezávislý class with its own file, its own state, and its own lifecycle hooks. Adding a nový feature means adding a nový module --- not editing a 3000-line mission class.

---

## CF_ModuleCore (COT / Expansion)

Community Framework (CF) provides the většina widely-used module system in the DayZ modding ecosystem. Oba COT and Expansion build on it.

### Jak to funguje

1. You declare a module class that extends one of CF's module base classes
2. You register it in `config.cpp` under `CfgPatches` / `CfgMods`
3. CF's `CF_ModuleCoreManager` auto-discovers and instantiates all registered module classes při startu
4. Lifecycle dokoncets are dispatched automatickýally

### Module Base Classes

CF provides three base classes corresponding to DayZ's script layers:

| Base Class | Layer | Typical Use |
|-----------|-------|-------------|
| `CF_ModuleGame` | 3_Game | Early init, RPC registration, data classes |
| `CF_ModuleWorld` | 4_World | Entity interaction, gameplay systems |
| `CF_ModuleMission` | 5_Mission | UI, HUD, mission-level hooks |

### Example: A CF Module

```c
class MyLootModule : CF_ModuleWorld
{
    // CF calls this once during module initialization
    override void OnInit()
    {
        super.OnInit();
        // Register RPC handlers, allocate data structures
    }

    // CF calls this when the mission starts
    override void OnMissionStart(Class sender, CF_EventArgs args)
    {
        super.OnMissionStart(sender, args);
        // Load configs, spawn initial loot
    }

    // CF calls this every frame on the server
    override void OnUpdate(Class sender, CF_EventArgs args)
    {
        super.OnUpdate(sender, args);
        // Tick loot respawn timers
    }

    // CF calls this when the mission ends
    override void OnMissionFinish(Class sender, CF_EventArgs args)
    {
        super.OnMissionFinish(sender, args);
        // Save state, release resources
    }
};
```

### Accessing a CF Module

```c
// Get a reference to a running module by type
MyLootModule lootMod;
CF_Modules<MyLootModule>.Get(lootMod);
if (lootMod)
{
    lootMod.ForceRespawn();
}
```

### Key Characteristics

- **Auto-discovery**: modules are instantiated by CF based on `config.cpp` declarations --- no manual `new` calls
- **Event args**: lifecycle hooks receive `CF_EventArgs` with context data
- **Dependency on CF**: your mod requires Community Framework as a dependency
- **Widely podporovaný**: if your mod targets servers that již run COT or Expansion, CF is již present

---

## VPP PluginBase / ConfigurablePlugin

VPP Admin Tools uses a plugin architecture where každý admin přílišl is a plugin class registered with a central manager.

### Plugin Base

```c
// VPP pattern (simplified)
class PluginBase : Managed
{
    void OnInit();
    void OnUpdate(float dt);
    void OnDestroy();

    // Plugin identity
    string GetPluginName();
    bool IsServerOnly();
};
```

### ConfigurablePlugin

VPP extends the base with a config-aware variant that automatickýally loads/saves settings:

```c
class ConfigurablePlugin : PluginBase
{
    // VPP auto-loads this from JSON on init
    ref PluginConfigBase m_Config;

    override void OnInit()
    {
        super.OnInit();
        LoadConfig();
    }

    void LoadConfig()
    {
        string path = "$profile:VPPAdminTools/" + GetPluginName() + ".json";
        if (FileExist(path))
        {
            JsonFileLoader<PluginConfigBase>.JsonLoadFile(path, m_Config);
        }
    }

    void SaveConfig()
    {
        string path = "$profile:VPPAdminTools/" + GetPluginName() + ".json";
        JsonFileLoader<PluginConfigBase>.JsonSaveFile(path, m_Config);
    }
};
```

### Registration

VPP registers plugins in the modded `MissionServer.OnInit()`:

```c
// VPP pattern
GetPluginManager().RegisterPlugin(new VPPESPPlugin());
GetPluginManager().RegisterPlugin(new VPPTeleportPlugin());
GetPluginManager().RegisterPlugin(new VPPWeatherPlugin());
```

### Key Characteristics

- **Manual registration**: každý plugin is explicitly `new`-ed and registered
- **Config integration**: `ConfigurablePlugin` merges config management with the module lifecycle
- **Self-contained**: no dependency on CF; VPP's plugin manager is its own system
- **Clear ownership**: the plugin manager holds `ref` to all plugins, controlling their lifetime

---

## Dabs Attribute-Based Registration

The Dabs Framework (used in Dabs Framework Admin Tools) uses a more modern approach: C#-style attributes for auto-registration.

### The Concept

Instead of ručně registering modules, you annotate a class with an attribute, and the framework discovers it při startu using reflection:

```c
// Dabs pattern (conceptual)
[CF_RegisterModule(DabsAdminESP)]
class DabsAdminESP : CF_ModuleWorld
{
    override void OnInit()
    {
        super.OnInit();
        // ...
    }
};
```

The `CF_RegisterModule` attribute tells CF's module manager to instantiate tato třída automatickýally. No manual `Register()` call needed.

### How Discovery Works

At startup, CF scans all loaded script classes for the registration attribute. For každý match, it creates an instance and adds it to the module manager. This happens before `OnInit()` is called on jakýkoli module.

### Key Characteristics

- **Zero boilerplate**: no registration code in mission classes
- **Declarative**: třída itself declares that it is a module
- **Relies on CF**: pouze works with Community Framework's attribute processing
- **Discoverability**: můžete find all modules by searching for the attribute in the codebase

---

## Custom Static Module Manager

This approach uses an explicit registration pattern with a statická manager class. There is no instance of the manager --- it is celýly statická methods and statická storage. This is užitečný when chcete zero dependencies on externí frameworks.

### Module Base Classes

```c
// Base: lifecycle hooks
class MyModuleBase : Managed
{
    bool IsServer();       // Override in subclass
    bool IsClient();       // Override in subclass
    string GetModuleName();
    void OnInit();
    void OnMissionStart();
    void OnMissionFinish();
};

// Server-side module: adds OnUpdate + player events
class MyServerModule : MyModuleBase
{
    void OnUpdate(float dt);
    void OnPlayerConnect(PlayerIdentity identity);
    void OnPlayerDisconnect(PlayerIdentity identity, string uid);
};

// Client-side module: adds OnUpdate
class MyClientModule : MyModuleBase
{
    void OnUpdate(float dt);
};
```

### Registration

Modules register themselves explicitly, typicky from modded mission classes:

```c
// In modded MissionServer.OnInit():
MyModuleManager.Register(new MyMissionServerModule());
MyModuleManager.Register(new MyAIServerModule());
```

### Lifecycle Dispatch

The modded mission classes call into `MyModuleManager` at každý lifecycle point:

```c
modded class MissionServer
{
    override void OnMissionStart()
    {
        super.OnMissionStart();
        MyModuleManager.OnMissionStart();
    }

    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);
        MyModuleManager.OnServerUpdate(timeslice);
    }

    override void OnMissionFinish()
    {
        MyModuleManager.OnMissionFinish();
        MyModuleManager.Cleanup();
        super.OnMissionFinish();
    }
};
```

### Listen-Server Safety

The vlastní module system's module base classes enforce a critical invariant: `MyServerModule` returns `true` from `IsServer()` and `false` from `IsClient()`, while `MyClientModule` does the opposite. The manager uses these flags to avoid dispatching lifecycle dokoncets twice on listen servers (where oba `MissionServer` and `MissionGameplay` run in the stejný process).

The base `MyModuleBase` returns `true` from oba --- which is why the codebase warns against subclassing it přímo.

### Key Characteristics

- **Zero dependencies**: no CF, no externí frameworks
- **Static manager**: no `GetInstance()` needed; purely statická API
- **Explicit registration**: plný control over what gets registered and when
- **Listen-server safe**: typed subclasses prevent double-dispatch
- **Centralized cleanup**: `MyModuleManager.Cleanup()` tears down all modules and core timers

---

## Module Lifecycle: The Universal Contract

Despite implementation differences, all four frameworks follow the stejný lifecycle contract:

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

### Pravidla

1. **OnInit comes before OnMissionStart.** Nikdy load configs or spawn entities in `OnInit()` --- the world may not be ready yet.
2. **OnAktualizujte receives delta time.** Vždy use `dt` for time-based logic, nikdy assume a fixed snímková frekvence.
3. **OnMissionFinish must clean up každýthing.** Every `ref` collection must be cleared. Every dokoncet subscription must be removed. Every jedenton must be destroyed. Toto je pouze reliable teardown point.
4. **Modules should not depend on každý jiný's initialization order.** If Module A needs Module B, use lazy access (`GetModule()`) spíše než assuming B was registered first.

---

## Osvědčené postupy for Module Design

### 1. One Module, One Responsibility

A module should own exactly one domain. Pokud find yourself writing `VehicleAndWeatherAndLootModule`, split it.

```c
// GOOD: Focused modules
class MyLootModule : MyServerModule { ... }
class MyVehicleModule : MyServerModule { ... }
class MyWeatherModule : MyServerModule { ... }

// BAD: God module
class MyEverythingModule : MyServerModule { ... }
```

### 2. Udržujte OnAktualizujte Cheap

`OnUpdate` runs každý frame. Pokud váš module does expensive work (file I/O, world scans, pathfinding), do it on a timer or batch it across frames:

```c
class MyCleanupModule : MyServerModule
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
};
```

### 3. Register RPCs in OnInit, Not OnMissionStart

RPC handlers must be in place before jakýkoli client can send a message. `OnInit()` runs during module registration, which happens early in the mission setup. `OnMissionStart()` may be příliš late if clients connect fast.

```c
class MyModule : MyServerModule
{
    override void OnInit()
    {
        super.OnInit();
        MyRPC.Register("MyMod", "RPC_DoThing", this, MyRPCSide.SERVER);
    }

    void RPC_DoThing(PlayerIdentity sender, Object target, ParamsReadContext ctx)
    {
        // Handle RPC
    }
};
```

### 4. Use the Module Manager for Cross-Module Access

Do not hold direct references to jiný modules. Use the manager's lookup:

```c
// GOOD: Loose coupling through the manager
MyModuleBase mod = MyModuleManager.GetModule("MyAIServerModule");
MyAIServerModule aiMod;
if (Class.CastTo(aiMod, mod))
{
    aiMod.PauseSpawning();
}

// BAD: Direct static reference creates hard coupling
MyAIServerModule.s_Instance.PauseSpawning();
```

### 5. Guard Against Missing Dependencies

Not každý server runs každý mod. Pokud váš module volitelnýly integrates with další mod, use preprocessor checks:

```c
override void OnMissionStart()
{
    super.OnMissionStart();

    #ifdef MYMOD_AI
    MyEventBus.OnMissionStarted.Insert(OnAIMissionStarted);
    #endif
}
```

### 6. Log Module Lifecycle Events

Logging makes debugging straightforward. Every module should log when it initializes and shuts down:

```c
override void OnInit()
{
    super.OnInit();
    MyLog.Info("MyModule", "Initialized");
}

override void OnMissionFinish()
{
    MyLog.Info("MyModule", "Shutting down");
    // Cleanup...
}
```

---

## Comparison Table

| Feature | CF_ModuleCore | VPP Plugin | Dabs Attribute | Custom Module |
|---------|--------------|------------|----------------|---------------|
| **Discovery** | config.cpp + auto | Manual `Register()` | Attribute scan | Manual `Register()` |
| **Base classes** | Game / World / Mission | PluginBase / ConfigurablePlugin | CF_ModuleWorld + attribute | ServerModule / ClientModule |
| **Dependencies** | Requires CF | Self-contained | Requires CF | Self-contained |
| **Listen-server safe** | CF handles it | Manual check | CF handles it | Typed subclasses |
| **Config integration** | Separate | Built into ConfigurablePlugin | Separate | Via MyConfigManager |
| **Aktualizujte dispatch** | Automatic | Manager calls `OnUpdate` | Automatic | Manager calls `OnUpdate` |
| **Cleanup** | CF handles it | Manual `OnDestroy` | CF handles it | `MyModuleManager.Cleanup()` |
| **Cross-mod access** | `CF_Modules<T>.Get()` | `GetPluginManager().Get()` | `CF_Modules<T>.Get()` | `MyModuleManager.GetModule()` |

Choose the approach that matches your mod's dependency profile. Pokud již depend on CF, use `CF_ModuleCore`. If chcete zero externí dependencies, build your own system following the vlastní manager or VPP pattern.

---

## Kompatibilita a dopad

- **Více modů:** Multiple mods can každý register their own modules with the stejný manager (CF, VPP, or vlastní). Name collisions pouze happen if two mods register the stejný class type --- use unique class names prefixed with your mod tag.
- **Pořadí načítání:** CF auto-discovers modules from `config.cpp`, so load order follows `requiredAddons`. Custom managers register modules in `OnInit()`, where the `modded class` chain determines order. Modules should not depend on registration order --- use lazy access patterns.
- **Listen Server:** On listen servers, oba `MissionServer` and `MissionGameplay` run in the stejný process. Pokud váš module manager dispatches `OnUpdate` from oba, modules receive double ticks. Use typed subclasses (`ServerModule` / `ClientModule`) that return `IsServer()` or `IsClient()` to prevent this.
- **Výkon:** Module dispatch adds one loop iteration per registered module per lifecycle call. With 10--20 modules this is negligible. Zajistěte individual module `OnUpdate` methods are cheap (viz Chapter 7.7).
- **Migration:** When upgrading DayZ versions, module systems are stable as long as the base class API (`CF_ModuleWorld`, `PluginBase`, etc.) ne change. Pin your CF dependency version to avoid breakage.

---

## Časté chyby

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing `OnMissionFinish` cleanup in a module | Collections, timers, and dokoncet subscriptions survive across mission restarts, causing stale data or crashes | Override `OnMissionFinish`, clear all `ref` collections, unsubscribe all dokoncets |
| Dispatching lifecycle dokoncets twice on listen servers | Server modules run client logic and vice versa; duplicate spawns, double RPC sends | Use `IsServer()` / `IsClient()` guards or typed module subclasses that enforce the split |
| Registering RPCs in `OnMissionStart` místo `OnInit` | Clients that connect during mission setup can send RPCs before handlers are ready --- messages are tiše dropped | Vždy register RPC handlers in `OnInit()`, which runs during module registration before jakýkoli client connects |
| One "God module" handling každýthing | Impossible to debug, test, or extend; merge conflicts when více developers work on it | Split into focused modules with a jeden responsibility každý |
| Holding direct `ref` to další module instance | Creates hard coupling and potential ref-cycle memory leaks | Use the module manager's lookup (`GetModule()`, `CF_Modules<T>.Get()`) for cross-module access |

---

## Teorie vs praxe

| Textbook Says | DayZ Reality |
|---------------|-------------|
| Module discovery should be automatický via reflection | Enforce Script reflection is limited; `config.cpp`-based discovery (CF) or explicit `Register()` calls are the pouze reliable approaches |
| Modules should be hot-swappable za běhu | DayZ ne support hot-reloading scripts; modules live for the celý mission lifecycle |
| Use interfaces for module contracts | Enforce Script has no `interface` keyword; use base class virtual methods (`override`) místo toho |
| Dependency injection decouples modules | No DI framework exists; use manager lookups and `#ifdef` guards for volitelný cross-mod dependencies |

---

[Domů](../../README.md) | [<< Předchozí: Vzor Singleton](01-singletons.md) | **Module / Plugin Systems** | [Další: Vzory RPC >>](03-rpc-patterns.md)
