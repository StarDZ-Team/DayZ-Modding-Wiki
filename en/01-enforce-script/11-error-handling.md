# Error Handling

> **Summary:** Learn how to handle errors in a language with no try/catch. Master guard clauses, defensive coding, and structured logging patterns that keep your mod stable.

---

## Table of Contents

- [The Fundamental Rule: No try/catch](#the-fundamental-rule-no-try-catch)
- [Guard Clause Pattern](#guard-clause-pattern)
  - [Single Guard](#single-guard)
  - [Multiple Guards (Stacked)](#multiple-guards-stacked)
  - [Guard With Logging](#guard-with-logging)
- [Null Checking](#null-checking)
  - [Before Every Operation](#before-every-operation)
  - [Chained Null Checks](#chained-null-checks)
  - [The notnull Keyword](#the-notnull-keyword)
- [ErrorEx — Engine Error Reporting](#errorex-—-engine-error-reporting)
  - [Severity Levels](#severity-levels)
  - [When to Use Each Level](#when-to-use-each-level)
- [DumpStackString — Stack Traces](#dumpstackstring-—-stack-traces)
- [Debug Printing](#debug-printing)
  - [Basic Print](#basic-print)
  - [Conditional Debug with #ifdef](#conditional-debug-with-ifdef)
- [Structured Logging Patterns](#structured-logging-patterns)
  - [Simple Prefix Pattern](#simple-prefix-pattern)
  - [Level-Based Logger Class](#level-based-logger-class)
  - [Production Logger Pattern (LNT_Log)](#production-logger-pattern-lnt-log)
- [Worked Examples](#worked-examples)
  - [Safe Function With Multiple Guards](#safe-function-with-multiple-guards)
  - [Safe Config Loading](#safe-config-loading)
  - [Framework-Dependent RPC Handler Skeleton](#framework-dependent-rpc-handler-skeleton)
  - [Safe Inventory Operation](#safe-inventory-operation)
- [Defensive Patterns Summary](#defensive-patterns-summary)
- [Best Practices](#best-practices)
- [These Patterns in the Vanilla Scripts](#these-patterns-in-the-vanilla-scripts)
- [Theory vs Practice](#theory-vs-practice)
- [Common Mistakes](#common-mistakes)
- [Summary](#summary)

---

## The Fundamental Rule: No try/catch

Enforce Script has **no exception handling**. There is no `try`, no `catch`, no `throw`, no `finally`. If something goes wrong at runtime (null dereference, invalid cast, array out of bounds), the engine either:

1. **Crashes silently** — the function stops executing, no error message
2. **Logs a script error** — visible in the `.RPT` log file
3. **Crashes the server/client** — in severe cases

This means **every potential failure point must be guarded manually**. The primary defense is the **guard clause pattern**.

---

## Guard Clause Pattern

A guard clause checks a precondition at the top of a function and returns early if it fails. This keeps the "happy path" un-nested and readable.

### Single Guard

```c
void TeleportPlayer(PlayerBase player, vector destination)
{
    if (!player)
        return;

    player.SetPosition(destination);
}
```

### Multiple Guards (Stacked)

Stack guards at the top of the function — each checks one precondition:

```c
void GiveItemToPlayer(PlayerBase player, string className, int quantity)
{
    // Guard 1: player exists
    if (!player)
        return;

    // Guard 2: player is alive
    if (!player.IsAlive())
        return;

    // Guard 3: valid class name
    if (className == "")
        return;

    // Guard 4: valid quantity
    if (quantity <= 0)
        return;

    // All preconditions met — safe to proceed
    for (int i = 0; i < quantity; i++)
    {
        player.GetInventory().CreateInInventory(className);
    }
}
```

### Guard With Logging

In production code, always log why a guard triggered — silent failures are hard to debug:

```c
void StartMission(PlayerBase initiator, string missionId)
{
    if (!initiator)
    {
        Print("[Missions] ERROR: StartMission called with null initiator");
        return;
    }

    if (missionId == "")
    {
        Print("[Missions] ERROR: StartMission called with empty missionId");
        return;
    }

    if (!initiator.IsAlive())
    {
        Print("[Missions] WARN: Player " + initiator.GetIdentity().GetName() + " is dead, cannot start mission");
        return;
    }

    // Proceed with mission start
    Print("[Missions] Starting mission " + missionId);
    // ...
}
```

---

## Null Checking

Null references are the most common crash source in DayZ modding. Every reference type can be `null`.

### Before Every Operation

```c
// WRONG — crashes if player, identity, or name is null at any point
string name = player.GetIdentity().GetName();

// CORRECT — check at each step
if (!player)
    return;

PlayerIdentity identity = player.GetIdentity();
if (!identity)
    return;

string name = identity.GetName();
```

### Chained Null Checks

When you need to traverse a chain of references, check each link:

```c
void PrintHandItemName(PlayerBase player)
{
    if (!player)
        return;

    HumanInventory inv = player.GetHumanInventory();
    if (!inv)
        return;

    EntityAI handItem = inv.GetEntityInHands();
    if (!handItem)
        return;

    Print("Player is holding: " + handItem.GetType());
}
```

### The notnull Keyword

`notnull` is a parameter modifier declaring that `null` is never a valid argument. Bohemia does not document the keyword, so whether it is enforced at compile time, at runtime, or both is unresolved -- write the call site as if nothing will catch a null for you:

```c
void ProcessItem(notnull EntityAI item)
{
    // The caller has promised item is not null
    Print(item.GetType());
}

// Usage:
EntityAI item = GetSomeItem();
if (item)
{
    ProcessItem(item);  // OK -- the contract is satisfied
}
// ProcessItem(null);   // Violates the contract -- never write this
```

> **Limitation:** whatever `notnull` checks, it cannot prevent a variable that was non-null at check time from becoming null afterwards -- engine-side entity deletion is the classic case. Guard those reads yourself.

---

## ErrorEx — Engine Error Reporting

`ErrorEx` writes an error message to the script log (`.RPT` file). It does **not** stop execution or throw an exception.

```c
ErrorEx("Something went wrong");
```

### Severity Levels

`ErrorEx` accepts an optional second parameter of type `ErrorExSeverity`:

```c
// INFO — informational, not an error
ErrorEx("Config loaded successfully", ErrorExSeverity.INFO);

// WARNING — potential problem, execution continues
ErrorEx("Config file not found, using defaults", ErrorExSeverity.WARNING);

// ERROR — definite problem (default severity if omitted)
ErrorEx("Failed to create object: class not found");
ErrorEx("Critical failure in RPC handler", ErrorExSeverity.ERROR);
```

| Severity | When to Use |
|----------|-------------|
| `ErrorExSeverity.INFO` | Informational messages you want in the error log |
| `ErrorExSeverity.WARNING` | Recoverable problems (missing config, fallback used) |
| `ErrorExSeverity.ERROR` | Definite bugs or unrecoverable states |

### When to Use Each Level

```c
void LoadConfig(string path)
{
    if (!FileExist(path))
    {
        // WARNING — recoverable, we'll use defaults
        ErrorEx("Config not found at " + path + ", using defaults", ErrorExSeverity.WARNING);
        UseDefaultConfig();
        return;
    }

    MyConfig cfg = new MyConfig();
    string loadError;
    if (!JsonFileLoader<MyConfig>.LoadFile(path, cfg, loadError))
    {
        // ERROR — the file exists but could not be opened or parsed
        ErrorEx("Config load failed for " + path + ": " + loadError);
        UseDefaultConfig();
        return;
    }

    if (cfg.Version < EXPECTED_VERSION)
    {
        // INFO — not a problem, just noteworthy
        ErrorEx("Config version " + cfg.Version.ToString() + " is older than expected", ErrorExSeverity.INFO);
    }

    if (!cfg.Validate())
    {
        // ERROR — bad data that will cause problems
        ErrorEx("Config validation failed for " + path);
        UseDefaultConfig();
        return;
    }
}
```

---

## DumpStackString — Stack Traces

`DumpStackString` captures the current call stack as a string. The function signature is `proto void DumpStackString(out string stack)` -- it returns `void` and fills the `out` parameter. This is crucial for diagnosing where an unexpected state occurred:

```c
void OnUnexpectedState(string context)
{
    string stack;
    DumpStackString(stack);
    Print("[ERROR] Unexpected state in " + context);
    Print("[ERROR] Stack trace:");
    Print(stack);
}
```

Use it in guard clauses to trace the caller:

```c
void CriticalFunction(PlayerBase player)
{
    if (!player)
    {
        string stack;
        DumpStackString(stack);
        ErrorEx("CriticalFunction called with null player! Stack: " + stack);
        return;
    }

    // ...
}
```

---

## Debug Printing

### Basic Print

`Print()` writes to the script log file. It accepts any type:

```c
Print("Hello World");                    // string
Print(42);                               // int
Print(3.14);                             // float
Print(player.GetPosition());             // vector

// Formatted print
Print(string.Format("Player %1 at position %2 with %3 HP",
    player.GetIdentity().GetName(),
    player.GetPosition().ToString(),
    player.GetHealth("", "Health").ToString()
));
```

### Conditional Debug with #ifdef

Wrap debug prints in preprocessor guards so they compile out of release builds:

```c
void ProcessAI(DayZInfected zombie)
{
    #ifdef DIAG_DEVELOPER
        Print(string.Format("[AI DEBUG] Processing %1 at %2",
            zombie.GetType(),
            zombie.GetPosition().ToString()
        ));
    #endif

    // Actual logic...
}
```

For mod-specific debug flags, define your own symbol:

```c
// In your config.cpp:
// defines[] = { "MYMOD_DEBUG" };

#ifdef MYMOD_DEBUG
    Print("[MyMod] Debug: item spawned at " + pos.ToString());
#endif
```

---

## Structured Logging Patterns

### Simple Prefix Pattern

The simplest approach — prepend a tag to every Print call:

```c
class MissionManager
{
    static const string LOG_TAG = "[Missions] ";

    void Start()
    {
        Print(LOG_TAG + "Mission system starting");
    }

    void OnError(string msg)
    {
        Print(LOG_TAG + "ERROR: " + msg);
    }
}
```

### Level-Based Logger Class

A reusable logger with severity levels:

```c
class ModLogger
{
    protected string m_Prefix;

    void ModLogger(string prefix)
    {
        m_Prefix = "[" + prefix + "] ";
    }

    void Info(string msg)
    {
        Print(m_Prefix + "INFO: " + msg);
    }

    void Warning(string msg)
    {
        Print(m_Prefix + "WARN: " + msg);
        ErrorEx(m_Prefix + msg, ErrorExSeverity.WARNING);
    }

    void Error(string msg)
    {
        Print(m_Prefix + "ERROR: " + msg);
        ErrorEx(m_Prefix + msg, ErrorExSeverity.ERROR);
    }

    void Debug(string msg)
    {
        #ifdef DIAG_DEVELOPER
            Print(m_Prefix + "DEBUG: " + msg);
        #endif
    }
}

// Usage:
ref ModLogger g_MissionLog = new ModLogger("Missions");
g_MissionLog.Info("System started");
g_MissionLog.Error("Failed to load mission data");
```

### Production Logger Pattern (LNT_Log)

For production mods, a static logging class with level filtering and multiple output targets scales better than scattered `Print` calls. Here is `LNT_Log`, the logger of the wiki's constructed **Lantern** example framework (the full Lantern subsystems are built step by step in Part 7):

```c
// Enum for log levels
enum LNT_LogLevel
{
    TRACE   = 0,
    DEBUG   = 1,
    INFO    = 2,
    WARNING = 3,
    ERROR   = 4,
    NONE    = 5
};

class LNT_Log
{
    private static LNT_LogLevel s_FileMinLevel = LNT_LogLevel.DEBUG;
    private static LNT_LogLevel s_ConsoleMinLevel = LNT_LogLevel.INFO;

    // Usage: LNT_Log.Info("ModuleName", "Something happened");
    static void Info(string source, string message)
    {
        Log(LNT_LogLevel.INFO, source, message);
    }

    static void Warning(string source, string message)
    {
        Log(LNT_LogLevel.WARNING, source, message);
    }

    static void Error(string source, string message)
    {
        Log(LNT_LogLevel.ERROR, source, message);
    }

    private static void Log(LNT_LogLevel level, string source, string message)
    {
        if (level < s_ConsoleMinLevel && level < s_FileMinLevel)
            return;

        string levelName = typename.EnumToString(LNT_LogLevel, level);
        string line = string.Format("[Lantern] [%1] [%2] %3", levelName, source, message);

        if (level >= s_ConsoleMinLevel)
            Print(line);

        if (level >= s_FileMinLevel)
            WriteToFile(line);
    }

    private static void WriteToFile(string line)
    {
        // File I/O implementation...
    }
}
```

Usage across multiple modules:

```c
LNT_Log.Info("MissionServer", "Lantern Core initialized (server)");
LNT_Log.Warning("AdminRPC", "Unauthorized request from: " + sender.GetName());
LNT_Log.Error("ConfigManager", "Failed to load config: " + path);
```

---

## Worked Examples

The examples below use the `LNT_Log` class defined in the previous section.

### Safe Function With Multiple Guards

```c
void HealPlayer(PlayerBase player, float amount, string healerName)
{
    // Guard: null player
    if (!player)
    {
        LNT_Log.Error("HealSystem", "HealPlayer called with null player");
        return;
    }

    // Guard: player alive
    if (!player.IsAlive())
    {
        LNT_Log.Warning("HealSystem", "Cannot heal dead player: " + player.GetIdentity().GetName());
        return;
    }

    // Guard: valid amount
    if (amount <= 0)
    {
        LNT_Log.Warning("HealSystem", "Invalid heal amount: " + amount.ToString());
        return;
    }

    // Guard: not already at full health
    float currentHP = player.GetHealth("", "Health");
    float maxHP = player.GetMaxHealth("", "Health");
    if (currentHP >= maxHP)
    {
        LNT_Log.Info("HealSystem", player.GetIdentity().GetName() + " already at full health");
        return;
    }

    // All guards passed — perform the heal
    float newHP = Math.Min(currentHP + amount, maxHP);
    player.SetHealth("", "Health", newHP);

    LNT_Log.Info("HealSystem", string.Format("%1 healed %2 for %3 HP (%4 -> %5)",
        healerName,
        player.GetIdentity().GetName(),
        amount.ToString(),
        currentHP.ToString(),
        newHP.ToString()
    ));
}
```

### Safe Config Loading

```c
class MyConfig
{
    int MaxPlayers = 60;
    float SpawnRadius = 100.0;
    string WelcomeMessage = "Welcome!";
}

static MyConfig LoadConfigSafe(string path)
{
    // Guard: file exists
    if (!FileExist(path))
    {
        Print("[Config] File not found: " + path + " — creating defaults");
        MyConfig defaults = new MyConfig();
        string saveError;
        if (!JsonFileLoader<MyConfig>.SaveFile(path, defaults, saveError))
            Print("[Config] ERROR: Could not write defaults: " + saveError);
        return defaults;
    }

    // Attempt load. The deprecated JsonLoadFile()/JsonSaveFile() (still seen in older
    // mods) return void: they do nothing at all when the file is missing or cannot be
    // opened, and log a parse failure to the RPT via ErrorEx without telling the caller.
    // LoadFile()/SaveFile() return a bool and fill an out error message -- use these.
    MyConfig cfg = new MyConfig();
    string loadError;
    if (!JsonFileLoader<MyConfig>.LoadFile(path, cfg, loadError))
    {
        Print("[Config] ERROR: Failed to parse " + path + " — using defaults (" + loadError + ")");
        return new MyConfig();
    }

    // Guard: validate values
    if (cfg.MaxPlayers < 1 || cfg.MaxPlayers > 128)
    {
        Print("[Config] WARN: MaxPlayers out of range (" + cfg.MaxPlayers.ToString() + "), clamping");
        cfg.MaxPlayers = Math.Clamp(cfg.MaxPlayers, 1, 128);
    }

    if (cfg.SpawnRadius < 0)
    {
        Print("[Config] WARN: SpawnRadius negative, using default");
        cfg.SpawnRadius = 100.0;
    }

    return cfg;
}
```

### Framework-Dependent RPC Handler Skeleton

This callback signature and `CallType` come from Community Framework's RPC manager, not vanilla DayZ. Register the handler through that framework and declare the dependency. The skeleton is not safe to expose to untrusted clients until you provide a server-owned permission implementation, an explicit spawn-class allowlist, finite and server-bounded position validation, and per-sender rate limiting.

```c
void RPC_SpawnItem(CallType type, ParamsReadContext ctx, PlayerIdentity sender, Object target)
{
    // Guard: server only
    if (type != CallType.Server)
        return;

    // Guard: valid sender
    if (!sender)
    {
        Print("[RPC] SpawnItem: null sender identity");
        return;
    }

    // Guard: read params
    Param2<string, vector> data;
    if (!ctx.Read(data))
    {
        Print("[RPC] SpawnItem: failed to read params from " + sender.GetName());
        return;
    }

    string className = data.param1;
    vector position = data.param2;

    // Guard: valid class name
    if (className == "")
    {
        Print("[RPC] SpawnItem: empty className from " + sender.GetName());
        return;
    }

    // Guard: permission check
    if (!HasPermission(sender.GetPlainId(), "SpawnItem"))
    {
        Print("[RPC] SpawnItem: unauthorized by " + sender.GetName());
        return;
    }

    // Execute only after the allowlist, position bounds, and rate limit described above pass
    Object obj = GetGame().CreateObjectEx(className, position, ECE_PLACE_ON_SURFACE);
    if (!obj)
    {
        Print("[RPC] SpawnItem: CreateObjectEx returned null for " + className);
        return;
    }

    Print("[RPC] SpawnItem: " + sender.GetName() + " spawned " + className);
}
```

### Safe Inventory Operation

```c
bool TransferItem(PlayerBase fromPlayer, PlayerBase toPlayer, EntityAI item)
{
    // Guard: all references valid
    if (!fromPlayer || !toPlayer || !item)
    {
        Print("[Inventory] TransferItem: null reference");
        return false;
    }

    // Guard: both players alive
    if (!fromPlayer.IsAlive() || !toPlayer.IsAlive())
    {
        Print("[Inventory] TransferItem: one or both players are dead");
        return false;
    }

    // This operation is server-authoritative, and the source must own the item
    if (!GetGame().IsServer() || item.GetHierarchyRootPlayer() != fromPlayer)
        return false;

    // Guard: target has space
    InventoryLocation il = new InventoryLocation();
    if (!toPlayer.GetInventory().FindFreeLocationFor(item, FindInventoryLocationType.ANY, il))
    {
        Print("[Inventory] TransferItem: no free space in target inventory");
        return false;
    }

    // Execute transfer
    return toPlayer.GetInventory().TakeEntityToInventory(InventoryMode.SERVER, FindInventoryLocationType.ANY, item);
}
```

---

## Defensive Patterns Summary

| Pattern | Purpose | Example |
|---------|---------|---------|
| Guard clause | Early return on invalid input | `if (!player) return;` |
| Null check | Prevent null dereference | `if (obj) obj.DoThing();` |
| Cast + check | Safe downcast | `if (Class.CastTo(p, obj))` |
| Validate after load | Check data after JSON load | `if (cfg.Value < 0) cfg.Value = default;` |
| Validate before use | Range/bounds check | `if (arr.IsValidIndex(i))` |
| Log on failure | Trace where things went wrong | `Print("[Tag] Error: " + context);` |
| ErrorEx for engine | Write to .RPT file | `ErrorEx("msg", ErrorExSeverity.WARNING);` |
| DumpStackString | Capture call stack | `string s; DumpStackString(s); Print(s);` |

---

## Best Practices

- Use flat guard clauses (`if (!x) return;`) at the top of every function instead of deeply nested `if` blocks -- it keeps code readable and the happy path un-nested.
- Always log a message inside guard clauses -- silent `return` makes failures invisible and extremely hard to debug.
- Use `ErrorEx` with appropriate severity levels (`INFO`, `WARNING`, `ERROR`) for messages that should appear in `.RPT` logs; use `Print` for script-log output.
- Wrap heavy debug logging in `#ifdef DIAG_DEVELOPER` or a custom define so it compiles out of release builds and does not hurt performance.
- Check `JsonFileLoader<T>.LoadFile`'s `bool` return, then validate the data. The deprecated `JsonLoadFile` returns `void`, so it cannot tell you it failed at all.

---

## These Patterns in the Vanilla Scripts

Every pattern in this chapter is grounded in code you can read yourself in the vanilla script dump:

| Pattern | Where to Look | Detail |
|---------|---------------|--------|
| Stacked guard clauses in RPC handlers | `DayZGame.OnRPC()` in `3_game/dayzgame.c`; `PlayerBase.OnRPC()` in `4_world/entities/manbase/playerbase.c` | Vanilla RPC handlers switch on the RPC type and validate `ctx.Read()` results before acting on any payload |
| Static logger class with level filtering | `LNT_Log` in this chapter ([Production Logger Pattern](#production-logger-pattern-lnt-log)) | A single static class routes `Info`/`Warning`/`Error` through one `Log()` method with separate console and file thresholds |
| `DumpStackString()` in critical guards | `1_core/proto/endebug.c` | Declared as `proto void DumpStackString(out string stack)` — fills the `out` parameter with the current call stack |
| `#ifdef DIAG_DEVELOPER` around debug prints | Pervasive across the vanilla scripts (hundreds of occurrences, e.g. `4_world/systems/inventory/dayzplayerinventory.c`) | Diagnostic-only code is wrapped so it never compiles into release builds |

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| `try`/`catch` | Standard in most languages | Does not exist in Enforce Script -- every failure point must be guarded manually |
| `JsonFileLoader.JsonLoadFile` | Expected to return success/failure | Returns `void`, so it never signals the caller. It does nothing when the file is missing or cannot be opened, and on a deserialization failure it calls `ErrorEx(...)` -- an RPT line, not a return value (`jsonfileloader.c:129`). It is also deprecated (`//! DEPRECATED` at `jsonfileloader.c:99`). Use `JsonFileLoader<T>.LoadFile(path, out data, out errorMessage)` (`:7`), which returns `bool` and reports the error |
| `ErrorEx` | Sounds like it throws an error | It only writes to the `.RPT` log -- execution continues normally |

---

## Common Mistakes

### 1. Assuming a function ran successfully

```c
// WRONG — the deprecated JsonLoadFile returns void; it cannot report failure to you
MyConfig cfg = new MyConfig();
JsonFileLoader<MyConfig>.JsonLoadFile(path, cfg);
// If the file has bad JSON, cfg still has default values — no error

// BETTER — the non-deprecated LoadFile returns bool and an error message
string error;
if (!JsonFileLoader<MyConfig>.LoadFile(path, cfg, error))
{
    Print("[Config] Warning: failed to load " + path + " — " + error);
}
```

### 2. Deeply nested null checks instead of guards

```c
// WRONG — pyramid of doom
void Process(PlayerBase player)
{
    if (player)
    {
        if (player.GetIdentity())
        {
            if (player.IsAlive())
            {
                // Finally do something
            }
        }
    }
}

// CORRECT — flat guard clauses
void Process(PlayerBase player)
{
    if (!player) return;
    if (!player.GetIdentity()) return;
    if (!player.IsAlive()) return;

    // Do something
}
```

### 3. Forgetting to log in guard clauses

```c
// WRONG — silent failure, impossible to debug
if (!player) return;

// CORRECT — leaves a trail
if (!player)
{
    Print("[MyMod] Process: null player");
    return;
}
```

### 4. Using Print in hot paths

```c
// WRONG — Print every frame kills performance
override void OnUpdate(float timeslice)
{
    Print("Updating...");  // Called every frame!
}

// CORRECT — use debug guards or rate-limit
override void OnUpdate(float timeslice)
{
    #ifdef DIAG_DEVELOPER
        m_DebugTimer += timeslice;
        if (m_DebugTimer > 5.0)
        {
            Print("[DEBUG] Update tick: " + timeslice.ToString());
            m_DebugTimer = 0;
        }
    #endif
}
```

---

## Summary

| Tool | Purpose | Syntax |
|------|---------|--------|
| Guard clause | Early return on failure | `if (!x) return;` |
| Null check | Prevent crash | `if (obj) obj.Method();` |
| ErrorEx | Write to .RPT log | `ErrorEx("msg", ErrorExSeverity.WARNING);` |
| DumpStackString | Get call stack | `string s; DumpStackString(s);` |
| Print | Write to script log | `Print("message");` |
| string.Format | Formatted logging | `string.Format("P %1 at %2", a, b)` |
| #ifdef guard | Compile-time debug switch | `#ifdef DIAG_DEVELOPER` |
| notnull | Declares null is never valid (enforcement undocumented) | `void Fn(notnull Class obj)` |

**The golden rule:** In Enforce Script, assume everything can be null and every operation can fail. Check first, act second, log always.
