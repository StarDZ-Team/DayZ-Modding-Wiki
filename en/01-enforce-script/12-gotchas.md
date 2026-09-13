# What Does NOT Exist (Gotchas)


---

> **Summary:** A catalog of features you expect from C++, C#, Java, or Python that are **missing** or **different** in Enforce Script, grouped by theme. Gotchas that another chapter covers in depth appear here as a short entry with a link to the full treatment.

---

## Table of Contents

- [Missing Language Features](#missing-language-features)
- [Parser (CParser) Traps](#parser-cparser-traps)
- [Engine & Runtime Quirks](#engine--runtime-quirks)
- [Sealed Classes, Parameter Limits, and the Obsolete Attribute](#sealed-classes-parameter-limits-and-the-obsolete-attribute)
- [Build & Log Diagnostics](#build--log-diagnostics)
- [Coming From C++](#coming-from-c)
- [Coming From C#](#coming-from-c-1)
- [Coming From Java](#coming-from-java)
- [Coming From Python](#coming-from-python)
- [Quick Reference Table](#quick-reference-table)

---

## Missing Language Features

Constructs that simply do not exist in the language. Trying any of them produces a compile error. One entry below — method overloading — is a correction rather than an absence; it is kept in place because the "it does not exist" version still circulates.

### No Ternary Operator

`int x = cond ? a : b;` does not compile — the `? :` operator does not exist, and that includes ternaries inside variable declarations. Write an `if`/`else` and assign in each branch.

Full coverage: [Control Flow](05-control-flow.md).

### No do...while Loop

The `do` keyword does not exist. Use `while (true)` with a `break` condition, or a first-iteration flag (`bool first = true; while (first || HasMore()) { first = false; ... }`).

Full coverage: [Control Flow](05-control-flow.md).

### No try/catch/throw

The keywords `try`, `catch`, and `throw` do not exist. Use guard clauses with early return, and `ErrorEx()` for reporting (`proto void ErrorEx(string err, ErrorExSeverity severity = ErrorExSeverity.ERROR)` in `1_core/proto/endebug.c`).

Full patterns: [Error Handling](11-error-handling.md).

### No Multiple Inheritance

`class MyClass extends BaseA, BaseB` does not compile — only single inheritance is supported. Inherit from one class and hold the other as a `ref` member (composition).

Full coverage: [Classes & Inheritance](03-classes-inheritance.md).

### Method Overloading — Supported, but Against the House Style

This chapter previously listed overloading as a compile error. The extraction disproves it. `class InputUtils` (`3_game/tools/inpututils.c`) declares `GetImagesetAndIconFromInputAction` twice — line 118 taking `notnull UAInput`, line 160 taking `string`, same arity — inside one class body, and the `string` overload calls the `UAInput` one at line 164. `GetRichtextButtonIconFromInputAction` is overloaded the same way at lines 167 and 198. Community code also overloads by arity: `_Sleep` in Community Online Tools (`JMESPModule.c:720` and `:726`) has two- and three-parameter forms, both called.

So the compiler does resolve overloads by parameter type and by arity. What is true is that vanilla almost never uses it: distinct names (`AddInt`/`AddFloat`), the `Ex()` suffix convention and default parameter values are the dominant idiom, and matching that idiom keeps your code readable to anyone who learned the API from vanilla. Treat overloading as available but unusual, not as forbidden.

Full coverage: [Functions & Methods](13-functions-methods.md).

### No Operator Overloading (Except Index)

**What you would write:**
```c
Vector3 operator+(Vector3 a, Vector3 b) { ... }
bool operator==(MyClass other) { ... }
```

**What happens:** Compile error. Custom operators cannot be defined.

**Correct solution:** Use named methods:
```c
class MyVector
{
    float x, y, z;

    MyVector Add(MyVector other)
    {
        MyVector result = new MyVector();
        result.x = x + other.x;
        result.y = y + other.y;
        result.z = z + other.z;
        return result;
    }

    bool Equals(MyVector other)
    {
        return (x == other.x && y == other.y && z == other.z);
    }
}
```

**Exception:** The index operator `[]` can be overloaded via `Get(index)` and `Set(index, value)` methods:
```c
class MyContainer
{
    int data[10];

    int Get(int index) { return data[index]; }
    void Set(int index, int value) { data[index] = value; }
}

MyContainer c = new MyContainer();
c[3] = 42;        // Calls Set(3, 42)
int v = c[3];     // Calls Get(3)
```

### No Lambdas / Anonymous Functions

**What you would write:**
```c
array.Sort((a, b) => a.name.CompareTo(b.name));
button.OnClick += () => { DoSomething(); };
```

**What happens:** Compile error. Lambda syntax does not exist.

**Correct solution:** Define a named method and pass a **method reference**. Engine callback APIs such as `CallLater()` take a `func` parameter (`proto void CallLater(func fn, int delay = 0, bool repeat = false, ...)` in `2_gamelib/tools.c`) — a reference to the method, not a string:

```c
class LNT_DelayedGreeter
{
    void Start()
    {
        // Method reference passed as the func parameter — not a string
        GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(this.SayHello, 1000, false);
    }

    void SayHello()
    {
        Print("Hello after one second");
    }
}
```

See also [Functions & Methods](13-functions-methods.md).

### No Delegates / Function Pointers (Native)

**What you would write:**
```c
delegate void MyCallback(int value);
MyCallback cb = SomeFunction;
cb(42);
```

**What happens:** Compile error. The `delegate` keyword does not exist.

**Correct solution:** Use `ScriptCaller` (a single wrapped method reference) or `ScriptInvoker` (an event with multiple subscribers) — both defined in `2_gamelib/tools.c`:

```c
class LNT_AlarmSystem
{
    ref ScriptInvoker m_OnAlarm;

    void LNT_AlarmSystem()
    {
        m_OnAlarm = new ScriptInvoker();
        m_OnAlarm.Insert(FlashLights);
        m_OnAlarm.Insert(PlaySiren);
    }

    void Trigger()
    {
        m_OnAlarm.Invoke();  // calls every registered handler
    }

    void FlashLights()
    {
        Print("Lights flashing");
    }

    void PlaySiren()
    {
        Print("Siren on");
    }
}
```

### No Default Parameter Expressions

Default parameter values may use literals, NULL, and supported compile-time constants such as enum members; runtime function calls are not valid defaults. For computed defaults, add a parameterless wrapper that calls the full version.

Full coverage: [Functions & Methods](13-functions-methods.md).

### No Variadic Parameters

`params object[]` and C-style `...` do not exist. `string.Format()` accepts up to 9 positional arguments; for variable-count data, pass an `array<T>`:

```c
void LogMultiple(string tag, array<string> messages)
{
    foreach (string msg : messages)
    {
        Print("[" + tag + "] " + msg);
    }
}
```

### No Interfaces / Abstract Classes (Enforced)

**What you would write:**
```c
interface ISerializable
{
    void Serialize();
    void Deserialize();
}

abstract class BaseProcessor
{
    abstract void Process();
}
```

**What happens:** The `interface` and `abstract` keywords do not exist.

**Correct solution:** Use regular classes with empty base methods:
```c
// "Interface" — base class with empty methods
class ISerializable
{
    void Serialize() {}     // Override in subclass
    void Deserialize() {}   // Override in subclass
}

// "Abstract" class — same pattern
class BaseProcessor
{
    void Process()
    {
        ErrorEx("BaseProcessor.Process() must be overridden!", ErrorExSeverity.ERROR);
    }
}

class ConcreteProcessor extends BaseProcessor
{
    override void Process()
    {
        // Actual implementation
    }
}
```

The compiler does NOT enforce that subclasses override the base methods. Forgetting to override silently uses the empty base implementation.

### No Generics Constraints

**What you would write:**
```c
class Container<T> where T : EntityAI  // Constrain T to EntityAI
```

**What happens:** Compile error. The `where` clause does not exist. Template parameters accept any type.

**Correct solution:** Validate at runtime:
```c
class EntityContainer<Class T>
{
    void Add(T item)
    {
        // Runtime type check instead of compile-time constraint
        EntityAI eai;
        if (!Class.CastTo(eai, item))
        {
            ErrorEx("EntityContainer only accepts EntityAI subclasses");
            return;
        }
        // proceed
    }
}
```

### No Nested Class Declarations

Classes cannot be declared inside other classes. Declare everything at the top level and use naming to show the relationship:

```c
class LNT_ZoneSettings
{
    int m_Radius;
}

class LNT_Zone
{
    ref LNT_ZoneSettings m_Settings;
}
```

### No #define Value Substitution

Enforce Script `#define` only creates existence flags for `#ifdef` checks — `#define MAX_PLAYERS 60` followed by `int max = MAX_PLAYERS;` does not compile. Use `const int` / `const string` for constants and reserve `#define` for conditional-compilation flags.

Full coverage: [Enums & Preprocessor](10-enums-preprocessor.md).

### No Namespaces

**What you would write:**
```c
namespace MyMod { class Config { } }
```

**What happens:** Compile error. The `namespace` keyword does not exist. All classes share a single global scope.

**Correct solution:** Use naming prefixes to avoid conflicts:
```c
class LNT_Config { }       // Lantern Core prefix
class LNT_AIConfig { }     // Lantern AI subsystem
class NP_PatrolRoute { }   // NightPatrol content mod prefix
```

### No nullptr — Use NULL or null

**What you would write:**
```c
if (obj == nullptr)
```

**What happens:** Compile error. The `nullptr` keyword does not exist.

**Correct solution:**
```c
Object obj = null;   // lowercase works; NULL (uppercase) also works

if (!obj)            // idiomatic null check (preferred)
{
    Print("obj is not set");
}
```

### No RAII for Engine Handles

Objects *are* cleaned up at end of scope: Bohemia documents `autoptr` as destroying its target "upon end of variable lifetime (end of scope or deletion of class which contains it)", and automatic reference counting destroys an object when its last strong reference goes away — local variables and function arguments being strong by default. [Memory Management](08-memory-management.md) covers both.

What gets no such treatment is an opaque engine handle. A `FileHandle` is an integer, not a managed object, so it stays open until you call `CloseFile()` yourself:

```c
FileHandle fh = OpenFile("$profile:Lantern/data.txt", FileMode.WRITE);
if (fh != 0)
{
    FPrintln(fh, "data");
    CloseFile(fh);  // must close manually
}
```

For object lifetime and ownership rules, see [Memory Management](08-memory-management.md).

### No #include — Everything via config.cpp

There is no `#include` directive. Script files load through your mod's `CfgMods` entry in `config.cpp`, in layer order (`3_Game` → `4_World` → `5_Mission`) and alphabetically within each layer.

Full coverage: [config.cpp Explained](../02-mod-structure/02-config-cpp.md).

---

## Parser (CParser) Traps

Code that looks valid but confuses the script parser — often with a misleading error message, sometimes with a crash.

### Multiline Function Calls Are Supported

Function calls may span lines. Keep delimiters and argument expressions balanced; line breaks alone do not cause a compile error.

```c
string msg = string.Format(
    "Player %1 at %2",
    name,
    pos
);
```

### Not a Trap: `\\` and `\"` in String Literals

Earlier revisions of this chapter listed escaped backslashes and escaped double quotes as a parser defect. That was wrong, and it is corrected here because the claim circulates widely.

Bohemia's Enforce Script syntax page states that strings "can contain standardised escape sequences; these are supported: `\n` `\r` `\t` `\\` `\"`". Vanilla relies on both:

```c
// 3_game/objectspawner.c:4 - escaped backslashes inside an ordinary string literal
protected static const ref TStringArray VALID_PATHS = {
    "DZ\\plants", "DZ\\plants_bliss", "DZ\\plants_sakhal",
    ...
};

// 3_game/tools/jsonfileloader.c:14 - escaped double quotes inside a format string
errorMessage = string.Format("Cannot open file \"%1\" for reading", filename);

// 3_game/tools/keystouielements.c:89 - a single escaped backslash as a literal character
RegisterKeyToUIElement(KeyCode.KC_BACKSLASH, "\\", false);
```

Both forms compile in shipped game code, so neither breaks CParser.

What remains true is a **convention**, not a parser limit: prefer forward slashes for in-game resource paths. Vanilla itself accepts both delimiters for object spawner paths (`objectspawner.c:4-7` lists `DZ\\plants` and `DZ/plants` side by side), and the particle registry warns when a registered path uses `\` instead of `/`:

```c
// 3_game/particles/particlelist.c:391-393 (DIAG_DEVELOPER build only)
if (fullPath.Replace("\\", "/") > 0)
{
    ErrorEx(string.Format("Using wrong path delimiter for particle registering! Use '/' instead of '\\'. fullPath=%1", fullPath), ErrorExSeverity.WARNING);
}
```

Follow the convention for resource paths. Do not avoid the escape sequences themselves.

### No Variable Redeclaration in else-if Blocks

Declaring the same variable name in sibling `if` / `else if` / `else` blocks fails with "multiple declaration of variable" — sibling branches share one scope. Use unique names per branch, or declare the variable once before the chain and only assign inside it.

Full coverage: [Control Flow](05-control-flow.md).

### Array Element Boolean Negation Fails

Direct boolean negation of an array element does not compile — use an explicit comparison:

```c
array<int> list = {0, 1, 2};

// DOES NOT COMPILE:
// if (!list[1]) { }

// Works — explicit comparison:
if (list[1] == 0)
{
    Print("second element is zero");
}
```

### Complex Expression in Array Assignment Crashes

Assigning a complex expression directly into an array element has been reported to cause a segmentation fault at runtime. Store the result in a local variable first:

```c
class LNT_RangeCache
{
    ref array<bool> m_Values = new array<bool>;

    void Store(int index, vector posA, vector posB, float distSq)
    {
        // CRASH REPORTED — complex expression assigned straight into an array element:
        // m_Values[index] = vector.DistanceSq(posA, posB) <= distSq;

        // SAFE — intermediate variable first
        bool inRange = vector.DistanceSq(posA, posB) <= distSq;
        m_Values[index] = inRange;
    }
}
```

This also matches the general rule: keep expressions simple and single-line — the parser and VM reward it.

### foreach on a Method Return Value

Iterating a method call that returns a **temporary** array (one that nothing owns after the call) has been reported to crash mid-iteration — the temporary can be released while the loop is still using it:

```c
class LNT_NameProvider
{
    array<string> BuildNames()
    {
        array<string> names = new array<string>;
        names.Insert("Aurora");
        names.Insert("Borealis");
        return names;  // freshly allocated — nothing owns it after return
    }

    void Iterate()
    {
        // RISKY — iterating the temporary directly:
        // foreach (string n : BuildNames()) { Print(n); }

        // SAFE — anchor the result in a local variable first
        array<string> names = BuildNames();
        foreach (string n : names)
        {
            Print(n);
        }
    }
}
```

Vanilla code does iterate method returns when the returned collection is **owned elsewhere** — for example `foreach (KeybindingElementNew element : m_KeyWidgetElements.Get(index))` in `5_mission/gui/newui/keybindings/keybindingscontainer.c`, where the map still owns the array. The safe rule of thumb: store the result in a local variable first.

### Empty #ifdef / #ifndef Blocks

Preprocessor blocks that contain no executable statement — including blocks with only comments — have been reported to crash the compiler:

```c
#ifdef LANTERN_DEBUG
    // a comment-only block like this has caused segfaults
#endif
```

Always include at least one executable statement, or remove the block entirely.

---

## Engine & Runtime Quirks

Behavior that compiles fine but does something different from what you expect.

### switch/case DOES Fall Through

`switch`/`case` falls through when `break` is omitted, exactly like C/C++ — vanilla even relies on it (`3_game/services/biossessionservice.c:182`: "Intentionally no break, fall through to connecting"). The gotcha is *forgetting* `break` when you did not want fall-through, and printing two cases instead of one. Always end each case with `break` unless the fall-through is intentional and commented.

Full coverage: [Control Flow](05-control-flow.md).

### JsonFileLoader.JsonLoadFile Returns void (and Is Deprecated)

`JsonFileLoader<T>.JsonLoadFile()` is declared `static void JsonLoadFile(string filename, out T data)` (`3_game/tools/jsonfileloader.c:105`, marked `//! DEPRECATED` in the vanilla source) — it fills an object you pass in. Assigning its return value does not compile:

```c
class LNT_ServerSettings
{
    int m_MaxPlayers = 60;
}

void LoadSettings()
{
    string path = "$profile:Lantern/settings.json";
    LNT_ServerSettings cfg = new LNT_ServerSettings();          // create with defaults first
    JsonFileLoader<LNT_ServerSettings>.JsonLoadFile(path, cfg); // populates cfg in place
}
```

The newer `JsonFileLoader<T>.LoadFile(string filename, out T data, out string errorMessage)` returns `bool` (`jsonfileloader.c:7`) if you need success/failure. See also [Functions & Methods](13-functions-methods.md).

### No Enum Validation

Any `int` can be assigned to an enum variable — out-of-range values compile and run without error. Range-check every enum value you read from a config file or the network before using it.

Full coverage: [Enums & Preprocessor](10-enums-preprocessor.md).

### Static Arrays Are Fixed-Size

`int arr[size]` with a runtime `size` does not compile — static array sizes must be compile-time constants (`const int BUFFER_SIZE = 64; int arr[BUFFER_SIZE];`). For runtime sizing use `array<T>` and `Resize()`.

Full coverage: [Arrays, Maps & Sets](02-arrays-maps-sets.md).

### array.Remove Is Unordered

`Remove(index)` swaps the element with the **last** element, then drops the last — order is NOT preserved (`{"A","B","C","D"}` minus index 1 becomes `{"A","D","C"}`). Use `RemoveOrdered(index)` or `RemoveItem(value)` (which calls `RemoveOrdered` internally — see `1_core/proto/enscript.c`) when order matters.

Full coverage: [Arrays, Maps & Sets](02-arrays-maps-sets.md).

### String Methods Modify In-Place

`ToUpper()` and `ToLower()` modify the string **in place** and return `int` (the new length), not a new string — `proto int ToLower();` and `proto int ToUpper();` in `1_core/proto/enstring.c`. Copy the string first if you need the original preserved. `TrimInPlace()` behaves the same way.

Full coverage: [String Operations](06-strings.md).

### ref Cycles Cause Memory Leaks

Two objects holding `ref` references to each other are never freed — the reference counts never reach zero. One side must hold a raw (non-`ref`) reference: the owner uses `ref`, the child points back with a plain reference.

Full coverage: [Memory Management](08-memory-management.md).

### No Destructor Guarantee on Server Shutdown

**What you would write (expecting cleanup):**
```c
void ~MyManager()
{
    SaveData();  // Expect this runs on shutdown
}
```

**What happens:** Server shutdown may kill the process before destructors run. Your save never happens.

**Correct solution:** Save proactively at regular intervals and on known lifecycle events:
```c
class LNT_StatTracker
{
    protected float m_SaveTimer;

    void OnMissionFinish()  // called before shutdown
    {
        SaveData();  // reliable save point
    }

    void OnUpdate(float dt)
    {
        m_SaveTimer += dt;
        if (m_SaveTimer > 300.0)  // every 5 minutes
        {
            SaveData();
            m_SaveTimer = 0;
        }
    }

    void SaveData()
    {
        // write to a $profile: path here
    }
}
```

### GetGame().GetPlayer() Returns null on Server

**What you would write:**
```c
PlayerBase player = PlayerBase.Cast(GetGame().GetPlayer());
player.SetHealth("", "", 0);  // CRASH on server!
```

**What happens:** `GetGame().GetPlayer()` returns the **local** player. On a dedicated server, there is no local player — it returns `null`.

**Correct solution:** On the server, iterate the connected players — `proto native void GetPlayers(out array<Man> players)` (`3_game/global/game.c:947`):
```c
// Server code — iterate the player list
array<Man> players = new array<Man>;
GetGame().GetPlayers(players);
foreach (Man man : players)
{
    PlayerBase player;
    if (Class.CastTo(player, man))
    {
        Print(player.GetPosition());
    }
}
```

```c
// Client code — the local player exists here
PlayerBase local = PlayerBase.Cast(GetGame().GetPlayer());
if (local)
{
    Print(local.GetPosition());
}
```

### Bitwise vs Comparison Operator Precedence

Operator priority follows C rules (per the official Enforce Script syntax reference), so bitwise operators bind **lower** than comparisons:

```c
int flags = 5;
int mask = 4;

// WRONG: parsed as flags & (mask == mask)
// if (flags & mask == mask) { }

// CORRECT: always parenthesize bitwise operations
if ((flags & mask) == mask)
{
    Print("mask bits set");
}
```

### int.MIN Comparisons

`int.MIN` is `-2147483648` (`const int MIN` in `1_core/proto/enconvert.c:28`). Vanilla uses it extensively as an **equality sentinel** for "not set" — e.g. `if (m_PersistentPairID == int.MIN)` in `3_game/remotelyactivateditembehaviour.c` — and that usage is safe.

The community-reported bug affects **ordering** comparisons against the minimum value:

```c
int val = 1;
if (val < int.MIN)  // reported to evaluate TRUE — mathematically impossible
{
    // this block should never run, but has been observed to
}
```

Follow vanilla's lead: use `int.MIN` only with `==` / `!=` as a sentinel, never in `<` / `>` comparisons (nothing can be smaller than `int.MIN` anyway), and avoid spelling out the raw literal `-2147483648`.

---

## Sealed Classes, Parameter Limits, and the Obsolete Attribute

Three constructs that exist in vanilla. Bohemia's own 1.28 release notes list all three under **MODDING → ADDED**, and that post is the source for the release framing below: [Stable Update 1.28](https://forums.dayz.com/topic/266370-stable-update-128/) — *PC Stable 1.28 Update 1, Version 1.28.159992 (Release on 03.06.2025)*, posted 2 June 2025 by merropa93 (DayZ Community Support); accessed 2026-09-11.

Read the release notes as Bohemia's report of its own change, which is what they are. Where they describe behavior — such as what happened before the parameter limit was diagnosed — that is Bohemia's description, not a runtime measurement by this audit, and nothing here infers how any of it is implemented natively.

### sealed Prevents Inheritance

The `sealed` keyword marks a class that cannot be extended or a method that cannot be overridden. The 1.28 release notes list `Enforce Script: 'sealed' keyword` under **MODDING → ADDED** ([Stable Update 1.28](https://forums.dayz.com/topic/266370-stable-update-128/), accessed 2026-09-11). Vanilla ships sealed classes — `Contact` and `PhysicsWorld` in `1_core/physics/` (`contact.c:9`, `physicsworld.c:9`). If you need different behavior, wrap the class (composition) instead of inheriting.

Full coverage: [Classes & Inheritance](03-classes-inheritance.md).

### Method Parameter Limit: 16 Maximum

Enforce Script methods cannot have more than 16 parameters; a 17th parameter is a compile error. The 1.28 release notes list, under **MODDING → ADDED**:

> Enforce Script: Compiler error when script methods exceed the maximum amount of parameters: 16, this has always been a limitation, previously the game would continue with buffer overflows and random crashes

— [Stable Update 1.28](https://forums.dayz.com/topic/266370-stable-update-128/), accessed 2026-09-11.

Read that sentence precisely, because the two halves have different dates. **The 16-parameter limit is longstanding** — Bohemia says it "has always been a limitation." **What 1.28 added is the compiler error that reports it.** Before that diagnostic existed, Bohemia describes the game as continuing past the limit "with buffer overflows and random crashes"; that is Bohemia's account of the old behavior, not something this audit reproduced, and it says nothing about how the limit is enforced natively. Refactor long parameter lists into a class or an array.

Full coverage: [Functions & Methods](13-functions-methods.md).

### Obsolete Attribute Warnings

The 1.28 release notes list `Enforce Script: 'Obsolete' attribute for functions and classes` under **MODDING → ADDED** ([Stable Update 1.28](https://forums.dayz.com/topic/266370-stable-update-128/), accessed 2026-09-11). The engine's own doc block (`1_core/proto/enscript.c:344-365`) describes what it does: marking a method `[Obsolete("...")]` makes the compiler throw a compile-time warning while the method is still called normally. It appears 53 times in the extraction.

**The message is a free-form string.** The engine declares the attribute as `class Obsolete: Managed { string m_Msg; void Obsolete(string msg = "") { m_Msg = msg; } }` — one string, stored verbatim, with no version parsing of any kind. Some annotations happen to begin with a version token (`entityai.c:74` carries `"1.30: No replacement"`, `:4727` carries `"1.30: Use NotifyPlayerInventoryLoadChanged instead"`), but nothing in the engine gives that token a defined meaning, so **no release floor or ceiling for the build you are reading can be inferred from an `[Obsolete]` string.** Treat it as the warning text it is. Check your build output for these warnings and migrate to the recommended replacement.

---

## Build & Log Diagnostics

These gotchas are about diagnosing builds and reading logs rather than the language itself. The full treatment lives in the [Troubleshooting Guide](../troubleshooting.md).

- **`GetGame().IsClient()` returns false during the client loading phase** — and `IsServer()` returns true, even on clients. For side checks that must be correct during load, use `GetGame().IsDedicatedServer()` (used throughout vanilla, e.g. `3_game/effect.c`). Caveat: it also returns false on listen servers, so it is not a substitute for `IsServer()` in multiplayer logic.
- **Compile error messages can report the wrong file** — an undefined class or naming conflict is often reported at the end of the **last successfully parsed file**, not at the real error location. If the error points at a file you never touched, look at the file parsed just after it.
- **`crash_*.log` files are not crashes** — despite the name, they contain runtime script exceptions, not engine crashes. Actual engine crashes produce `.mdmp` dumps.

---

## Coming From C++

If you are a C++ developer, here are the biggest adjustments:

| C++ Feature | Enforce Script Equivalent |
|-------------|--------------------------|
| `std::vector` | `array<T>` |
| `std::map` | `map<K,V>` |
| `std::unique_ptr` | `ref` / `autoptr` |
| `dynamic_cast<T*>` | `Class.CastTo()` or `T.Cast()` |
| `try/catch` | Guard clauses |
| `operator+` | Named methods (`Add()`) |
| `namespace` | Name prefixes (`LNT_`, `NP_`) |
| `#include` | config.cpp `files[]` |
| RAII | `ref`/`autoptr` for objects; manual cleanup for engine handles |
| Multiple inheritance | Single inheritance + composition |
| `nullptr` | `null` / `NULL` |
| Templates with constraints | Templates without constraints + runtime checks |
| `do...while` | `while (true) { ... if (!cond) break; }` |

---

## Coming From C#

| C# Feature | Enforce Script Equivalent |
|-------------|--------------------------|
| `interface` | Base class with empty methods |
| `abstract` | Base class + ErrorEx in base methods |
| `delegate` / `event` | `ScriptInvoker` |
| Lambda `=>` | Named methods |
| `?.` null conditional | Manual null checks |
| `??` null coalescing | `if (!x) x = default;` |
| `try/catch` | Guard clauses |
| `using` (IDisposable) | Manual cleanup |
| Properties `{ get; set; }` | Public fields or explicit getter/setter methods |
| LINQ | Manual loops |
| `nameof()` | Hardcoded strings |
| `async/await` | CallLater / timers |
| Method overloading | Supported, but vanilla prefers distinct names / `Ex()` convention |

---

## Coming From Java

| Java Feature | Enforce Script Equivalent |
|-------------|--------------------------|
| `interface` | Base class with empty methods |
| `try/catch/finally` | Guard clauses |
| Garbage collection | `ref` + reference counting (no GC for cycles) |
| `@Override` | `override` keyword |
| `instanceof` | `obj.IsInherited(typename)` |
| `package` | Name prefixes |
| `import` | config.cpp `files[]` |
| `enum` with methods | `enum` (int-only) + helper class |
| `final` | `const` (for variables only) |
| Annotations | Not available |

---

## Coming From Python

| Python Feature | Enforce Script Equivalent |
|-------------|--------------------------|
| Dynamic typing | Static typing (all variables typed) |
| `try/except` | Guard clauses |
| `lambda` | Named methods |
| List comprehension | Manual loops |
| `**kwargs` / `*args` | Fixed parameters |
| Duck typing | `IsInherited()` / `Class.CastTo()` |
| `__init__` | Constructor (same name as class) |
| `__del__` | Destructor (`~ClassName()`) |
| `import` | config.cpp `files[]` |
| Multiple inheritance | Single inheritance + composition |
| `None` | `null` / `NULL` |
| Indentation-based blocks | `{ }` braces |
| f-strings | `string.Format("text %1 %2", a, b)` |

---

## Quick Reference Table

| Feature | Exists? | Workaround |
|---------|---------|------------|
| Ternary `? :` | No | if/else |
| `do...while` | No | while + break |
| `try/catch` | No | Guard clauses |
| Multiple inheritance | No | Composition |
| Method overloading | Yes (by type and arity) | Vanilla style is distinct names / `Ex()` / default params |
| Operator overloading | Index only | Named methods |
| Lambdas | No | Named methods |
| Delegates | No | `ScriptInvoker` / `ScriptCaller` |
| `\\` / `\"` in strings | Yes | Supported escapes; forward slashes for resource paths are a convention, not a parser limit |
| Variable redeclaration | Broken in else-if | Unique names or declare before if |
| Multiline function calls | Unreliable parsing | Keep calls on one line |
| `nullptr` | No | `null` / `NULL` |
| switch fall-through | Yes (like C/C++) | Always use `break` unless intentional |
| Default param expressions | No | Literals or NULL only |
| `#define` values | No | `const` |
| Interfaces | No | Empty base class |
| Generic constraints | No | Runtime type checks |
| Enum validation | No | Manual range check |
| Variadic params | No | `string.Format` or arrays |
| Nested classes | No | Top-level with prefixed names |
| Variable-size static arrays | No | `array<T>` |
| `#include` | No | config.cpp `files[]` |
| Namespaces | No | Name prefixes |
| RAII for engine handles (`FileHandle`) | No | Close explicitly (`CloseFile`) |
| `GetGame().GetPlayer()` on server | Returns null | Iterate `GetPlayers()` |
| `sealed` class inheritance (keyword added in 1.28) | Compile error | Use composition instead |
| 17+ method parameters (limit longstanding; compiler error added in 1.28) | Compile error | Pass a class or array |
| `[Obsolete]` APIs (attribute added in 1.28) | Compiler warning | Migrate to replacement API |
| `int.MIN` ordering comparisons | Incorrect results | Equality-sentinel only |
| `!array[i]` negation | Compile error | Use `array[i] == 0` |
| Complex expr in array assign | Crash reported | Use intermediate variable |
| `foreach` on method return | Crash reported | Store in local variable first |
| Bitwise vs comparison precedence | C rules | Always use parentheses |
| Empty `#ifdef` blocks | Crash reported | Include a statement or remove block |
| `IsClient()` during load | Returns false | Use `IsDedicatedServer()` |
| Compile error wrong file | Misleading location | Check file parsed after reported one |
| `crash_*.log` files | Not actual crashes | They are runtime script exceptions |
