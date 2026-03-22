# Chapter 7.1: Singleton Pattern

[Domů](../../README.md) | **Vzor Singleton** | [Další: Systémy modulů >>](02-module-systems.md)

---

## Úvod

The jedenton pattern guarantees that a class has exactly one instance, accessible globálníly. In DayZ modding it is the většina common architectural pattern --- virtually každý manager, cache, registry, and subsystem uses it. COT, VPP, Expansion, Dabs Framework, and jinýs all rely on jedentons to coordinate state across engine's script layers.

This chapter covers the canonical implementation, lifecycle management, when the pattern is appropriate, and where it goes wrong.

---

## Obsah

- [The Canonical Implementation](#the-canonical-implementation)
- [Lazy vs Eager Initialization](#lazy-vs-eager-initialization)
- [Lifecycle Management](#lifecycle-management)
- [When to Use Singletons](#when-to-use-singletons)
- [Real-World Examples](#real-world-examples)
- [Thread Safety Considerations](#thread-safety-considerations)
- [Anti-Patterns](#anti-patterns)
- [Alternative: Static-Only Classes](#alternative-statická-only-classes)
- [Checklist](#checklist)

---

## Kanonická implementace

The standard DayZ jedenton follows a simple formula: a `private statická ref` field, a statická `GetInstance()` accessor, and a statická `DestroyInstance()` for cleanup.

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

### Why `private statická ref`?

| Keyword | Purpose |
|---------|---------|
| `private` | Prevents jiný classes from setting `s_Instance` to null or replacing it |
| `statická` | Shared across all code --- no instance needed to access it |
| `ref` | Strong reference --- keeps the object alive as long as `s_Instance` is non-null |

Bez `ref`, the instance would be a weak reference and could be garbage-collected while stále in use.

---

## Lazy vs Eager Initialization

### Lazy Initialization (Recommended Default)

The `GetInstance()` method creates the instance on first access. Toto je approach used by většina DayZ mods.

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
- No dependency on initialization order mezi mods
- Safe if the jedenton je volitelný (some server configurations may nikdy call it)

**Disadvantage:**
- First caller pays the construction cost (usually negligible)

### Eager Initialization

Some jedentons are created explicitly during mission startup, typicky from `MissionServer.OnInit()` or a module's `OnMissionStart()`.

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
- The jedenton loads data from disk (configs, JSON files) and chcete load errors to surface při startu
- The jedenton registers RPC handlers that must be in place before jakýkoli client connects
- Initialization order matters and potřebujete to control it explicitly

---

## Lifecycle Management

The většina common source of jedenton bugs in DayZ is failing to clean up on mission end. DayZ servers can restart missions without restarting the process, which means statická fields survive across mission restarts. Pokud ne null out `s_Instance` in `OnMissionFinish`, you carry stale references, dead objects, and orphaned zpětné volánís into the next mission.

### Kontrakt životního cyklu

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

Vždy pair your jedenton with a `DestroyInstance()` method and call it during shutdown:

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
        s_Instance = null;  // Drops the ref, destructor runs
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

A framework mod can consolidate all jedenton cleanup into `MyFramework.ShutdownAll()`, which is called from the modded `MissionServer.OnMissionFinish()`. This prevents the common mistake of forgetting one jedenton:

```c
// Conceptual pattern (centralized shutdown):
static void ShutdownAll()
{
    MyRPC.Cleanup();
    MyEventBus.Cleanup();
    MyModuleManager.Cleanup();
    MyConfigManager.DestroyInstance();
    MyPermissions.DestroyInstance();
}
```

---

## Kdy použít singletony

### Good Candidates

| Use Case | Why Singleton Works |
|----------|-------------------|
| **Manager classes** (LootManager, VehicleManager) | Exactly one coordinator for a domain |
| **Caches** (CfgVehicles cache, icon cache) | Single source of truth avoids redundant computation |
| **Registries** (RPC handler registry, module registry) | Central lookup must be globálníly accessible |
| **Config holders** (server settings, permissions) | One config per mod, loaded once from disk |
| **RPC dispatchers** | Single entry point for all incoming RPCs |

### Poor Candidates

| Use Case | Why Not |
|----------|---------|
| **Per-player data** | One instance per player, not one globální instance |
| **Temporary computations** | Create, use, discard --- no globální state needed |
| **UI views / dialogs** | Multiple can coexist; use the view stack místo toho |
| **Entity components** | Attached to individual objects, not globální |

---

## Příklady z praxe

### COT (Community Online Tools)

COT uses a module-based jedenton pattern through the CF framework. Each přílišl is a `JMModuleBase` jedenton registered při startu:

```c
// COT pattern: CF auto-instantiates modules declared in config.cpp
class JM_COT_ESP : JMModuleBase
{
    // CF manages the singleton lifecycle
    // Access via: JM_COT_ESP.Cast(GetModuleManager().GetModule(JM_COT_ESP));
}
```

### VPP Admin Tools

VPP uses explicit `GetInstance()` on manager classes:

```c
// VPP pattern (simplified)
class VPPATBanManager
{
    private static ref VPPATBanManager m_Instance;

    static VPPATBanManager GetInstance()
    {
        if (!m_Instance)
            m_Instance = new VPPATBanManager();
        return m_Instance;
    }
}
```

### Expansion

Expansion declares jedentons for každý subsystem and hooks into the mission lifecycle for cleanup:

```c
// Expansion pattern (simplified)
class ExpansionMarketModule : CF_ModuleWorld
{
    // CF_ModuleWorld is itself a singleton managed by the CF module system
    // ExpansionMarketModule.Cast(CF_ModuleCoreManager.Get(ExpansionMarketModule));
}
```

---

## Thread Safety Considerations

Enforce Script is jeden-threaded. All script execution happens on the main thread within the Enfusion engine's game loop. This means:

- Existují **no race conditions** mezi concurrent threads
- You do **not** need mutexes, locks, or atomic operations
- `GetInstance()` with lazy initialization is vždy safe

Nicméně **re-entrancy** can stále cause problems. If `GetInstance()` triggers code that calls `GetInstance()` again during construction, můžete get a partially-initialized jedenton:

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

The fix is to assign `s_Instance` before running jakýkoli initialization that might re-enter:

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

Or better yet, avoid circular initialization celýly.

---

## Anti-Patterns

### 1. Global Mutable State Bez Encapsulation

The jedenton pattern gives you globální access. That ne mean the data should be globálníly writable.

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

Pokud forget cleanup, the jedenton persists across mission restarts with stale data:

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

Když jedenton accumulates příliš mnoho responsibilities, it becomes a "God object" that is impossible to reason about:

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

Split into focused jedentons: `LootManager`, `VehicleManager`, `WeatherManager`, `BanManager`. Každý one is small, testable, and has a clear domain.

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

Some "singletons" ne need an instance at all. If třída holds no instance state and pouze has statická methods and statická fields, skip the `GetInstance()` ceremony celýly:

```c
// No instance needed — all static
class MyLog
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

Toto je approach used by `MyLog`, `MyRPC`, `MyEventBus`, and `MyModuleManager` in a framework mod. It is simpler, avoids the `GetInstance()` null-check overhead, and makes the intent clear: there is no instance, pouze shared state.

**Use a statická-only class when:**
- All methods are stateless or operate on statická fields
- There is no meaningful constructor/destructor logic
- You nikdy need to pass the "instance" as a parameter

**Use a true jedenton when:**
- The class has instance state that benefits from encapsulation (`protected` fields)
- You need polymorphism (a base class with overridden methods)
- The object needs to be passed to jiný systems by reference

---

## Checklist

Před shipping a jedenton, verify:

- [ ] `s_Instance` is declared `private statická ref`
- [ ] `GetInstance()` handles the null case (lazy init) or you have an explicit `Create()` call
- [ ] `DestroyInstance()` exists and sets `s_Instance = null`
- [ ] `DestroyInstance()` is called from `OnMissionFinish()` or a centralized shutdown method
- [ ] The destructor cleans up owned collections (`.Clear()`, set to `null`)
- [ ] No public fields --- all mutation goes through methods
- [ ] The constructor ne call `GetInstance()` on jiný jedentons (defer to `OnInit()`)

---

## Kompatibilita a dopad

- **Více modů:** Multiple mods každý defining their own jedentons coexist safely --- každý has its own `s_Instance`. Conflicts pouze arise if two mods define the stejný class name, which Enforce Script will flag as a redefinition error at load time.
- **Pořadí načítání:** Lazy singletons are unaffected by mod load order. Eager singletons created in `OnInit()` depend on the `modded class` chain order, which follows `config.cpp` `requiredAddons`.
- **Listen Server:** Static fields are shared mezi client and server contexts in the stejný process. A jedenton that should pouze exist server-side must guard construction with `GetGame().IsServer()`, or it will be accessible (and potentially initialized) from client code as well.
- **Výkon:** Singleton access is a statická null check + method call --- negligible overhead. The cost is in what the jedenton *does*, not in accessing it.
- **Migration:** Singletons survive DayZ version updates as long as the APIs they call (e.g., `GetGame()`, `JsonFileLoader`) remain stable. No special migration is needed for the pattern itself.

---

## Časté chyby

| Mistake | Impact | Fix |
|---------|--------|-----|
| Missing `DestroyInstance()` call in `OnMissionFinish` | Stale data and dead entity references carry over across mission restarts, causing crashes or ghost state | Vždy call `DestroyInstance()` from `OnMissionFinish` or a centralized `ShutdownAll()` |
| Calling `GetInstance()` inside další jedenton's constructor | Triggers re-entrant construction; `s_Instance` is stále null, so a second instance is created | Defer cross-singleton access to an `Initialize()` method called after construction |
| Using `public statická ref` místo `private statická ref` | Any code can set `s_Instance = null` or replace it, breaking the jeden-instance guarantee | Vždy declare `s_Instance` as `private statická ref` |
| Not guarding eager init on listen servers | Singleton is constructed twice (once from server path, once from client path) if `Create()` lacks a null check | Vždy check `if (!s_Instance)` inside `Create()` |
| Accumulating state without bounds (unbounded caches) | Memory grows indefinitely on long-running servers; dokoncetual OOM or severe lag | Cap collections with a max size or periodic eviction in `OnUpdate` |

---

## Teorie vs praxe

| Textbook Says | DayZ Reality |
|---------------|-------------|
| Singletons are an anti-pattern; use dependency injection | Enforce Script has no DI container. Singletons are the standard approach for globální managers across all major mods. |
| Lazy initialization is vždy sufficient | RPC handlers must be registered before jakýkoli client connects, so eager init in `OnInit()` is často nutný. |
| Singletons should nikdy be destroyed | DayZ missions restart without restarting server process; jedentons *must* be destroyed and recreated on každý mission cycle. |

---

[Domů](../../README.md) | **Vzor Singleton** | [Další: Systémy modulů >>](02-module-systems.md)
