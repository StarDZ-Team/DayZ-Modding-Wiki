# Functions & Methods

> **Summary:** How functions work in Enforce Script — declaration syntax, the parameter passing modes (`out`, `inout`, `notnull`), return values, default parameters, the 16-parameter limit, `proto native` engine bindings, method overriding, method overloading and the naming conventions vanilla prefers instead, `event` methods, `thread` coroutines, and deferred calls with `CallLater`.

---

## Introduction

Functions are the fundamental unit of behavior in Enforce Script. Every action a mod performs --- spawning an item, checking a player's health, sending an RPC, drawing a UI element --- lives inside a function. Understanding how to declare them, pass data in and out, and work with the engine's special modifiers is essential for writing correct DayZ mods.

This chapter covers function mechanics in depth: declaration syntax, parameter passing modes, return values, default parameters, proto native bindings, static vs instance methods, overriding, the `thread` keyword, and the `event` keyword. If [Classes & Inheritance](03-classes-inheritance.md) taught you where functions live, this chapter teaches you how they work.

---

## Table of Contents

- [Function Declaration Syntax](#function-declaration-syntax)
  - [Standalone Functions](#standalone-functions)
  - [Instance Methods](#instance-methods)
  - [Static Methods](#static-methods)
- [Parameter Passing Modes](#parameter-passing-modes)
  - [By Value (Default)](#by-value-default)
  - [out Parameters](#out-parameters)
  - [inout Parameters](#inout-parameters)
  - [notnull Parameters](#notnull-parameters)
- [Return Values](#return-values)
- [Default Parameter Values](#default-parameter-values)
- [Parameter Limit: 16 Maximum](#parameter-limit-16-maximum)
- [Proto Native Methods (Engine Bindings)](#proto-native-methods-engine-bindings)
- [Static vs Instance Methods](#static-vs-instance-methods)
- [Method Overriding](#method-overriding)
- [Method Overloading (Supported, Rarely Used)](#method-overloading-supported-rarely-used)
- [The event Keyword](#the-event-keyword)
- [Thread Methods (Coroutines)](#thread-methods-coroutines)
- [Deferred Calls with CallLater](#deferred-calls-with-calllater)
- [Best Practices](#best-practices)
- [Common Method Conventions](#common-method-conventions)
- [Theory vs Practice](#theory-vs-practice)
- [Common Mistakes](#common-mistakes)
- [Quick Reference Table](#quick-reference-table)

---

## Function Declaration Syntax

Every function has a return type, a name, and a parameter list. The body is enclosed in braces.

```
ReturnType FunctionName(ParamType paramName, ...)
{
    // body
}
```

### Standalone Functions

Standalone (global) functions exist outside any class. They are rare in DayZ modding --- nearly all code lives inside classes --- but you will encounter a few in the vanilla scripts.

```c
// Standalone function (global scope)
void PrintPlayerCount()
{
    array<Man> players = new array<Man>();
    GetGame().GetPlayers(players);
    int count = players.Count();
    Print(string.Format("Players online: %1", count));
}

// Standalone function with return value
string FormatTimestamp(int hours, int minutes)
{
    return string.Format("%1:%2", hours.ToStringLen(2), minutes.ToStringLen(2));
}
```

The vanilla engine defines several standalone utility functions:

```c
// From enscript.c — helper for string expressions
string String(string s)
{
    return s;
}
```

### Instance Methods

The vast majority of functions in DayZ mods are instance methods --- they belong to a class and operate on that instance's data.

```c
class LootSpawner
{
    protected vector m_Position;
    protected float m_Radius;

    void SetPosition(vector pos)
    {
        m_Position = pos;
    }

    float GetRadius()
    {
        return m_Radius;
    }

    bool IsNearby(vector testPos)
    {
        return vector.Distance(m_Position, testPos) <= m_Radius;
    }
}
```

Instance methods have implicit access to `this` --- a reference to the current object. You rarely need to write `this.` explicitly, but it can help disambiguate when a parameter has a similar name.

### Static Methods

Static methods belong to the class itself, not to any instance. Call them via `ClassName.Method()`. They cannot access instance fields or `this`.

```c
class MathHelper
{
    static float Clamp01(float value)
    {
        if (value < 0) return 0;
        if (value > 1) return 1;
        return value;
    }

    static float Lerp(float a, float b, float t)
    {
        return a + (b - a) * Clamp01(t);
    }
}

// Usage:
float result = MathHelper.Lerp(0, 100, 0.75);  // 75.0
```

Static methods are ideal for utility functions, factory methods, and singleton accessors. DayZ's vanilla code uses them extensively:

```c
// From DamageSystem (3_game/damagesystem.c)
class DamageSystem
{
    static bool GetDamageZoneMap(EntityAI entity, out DamageZoneMap zoneMap)
    {
        // ...
    }

    static string GetDamageDisplayName(EntityAI entity, string zone)
    {
        // ...
    }
}
```

---

## Parameter Passing Modes

Enforce Script supports four parameter passing modes. Understanding them is critical because the wrong mode leads to silent bugs where data never reaches the caller.

### By Value (Default)

When no modifier is specified, the parameter is passed **by value**. For primitives (`int`, `float`, `bool`, `string`, `vector`), a copy is made. Modifications inside the function do not affect the caller's variable.

```c
void DoubleValue(int x)
{
    x = x * 2;  // modifies local copy only
}

// Usage:
int n = 5;
DoubleValue(n);
Print(n);  // still 5 --- the original is unchanged
```

For class types (objects), by-value passing still passes a **reference to the object** --- but the reference itself is copied. You can modify the object's fields, but you cannot reassign the reference to point to a different object.

```c
void RenameZone(SpawnZone zone)
{
    zone.SetName("NewName");  // this WORKS --- modifies the same object
    zone = null;              // this does NOT affect the caller's variable
}
```

### out Parameters

The `out` keyword marks a parameter as **output-only**. The function writes a value into it, and the caller receives that value. The initial value of the parameter is undefined --- do not read it before writing.

```c
// out parameter — function fills the value
bool TryFindPlayer(string name, out PlayerBase player)
{
    array<Man> players = new array<Man>;
    GetGame().GetPlayers(players);

    for (int i = 0; i < players.Count(); i++)
    {
        PlayerBase pb = PlayerBase.Cast(players[i]);
        if (pb && pb.GetIdentity() && pb.GetIdentity().GetName() == name)
        {
            player = pb;
            return true;
        }
    }

    player = null;
    return false;
}

// Usage:
PlayerBase result;
if (TryFindPlayer("John", result))
{
    Print(result.GetIdentity().GetName());
}
```

The vanilla scripts use `out` extensively for engine-to-script data flow:

```c
// From DayZPlayer (3_game/dayzplayer.c)
proto native void GetCurrentCameraTransform(out vector position, out vector direction, out vector rotation);

// From AIWorld (3_game/ai/aiworld.c)
proto native bool RaycastNavMesh(vector from, vector to, PGFilter pgFilter, out vector hitPos, out vector hitNormal);

// Multiple out parameters for look limits
proto void GetLookLimits(out float pDown, out float pUp, out float pLeft, out float pRight);
```

### inout Parameters

The `inout` keyword marks a parameter that is **both read and written** by the function. The caller's value is available inside the function, and any modifications are visible to the caller afterward.

```c
// inout — the function reads the current value and modifies it
void ClampHealth(inout float health)
{
    if (health < 0)
        health = 0;
    if (health > 100)
        health = 100;
}

// Usage:
float hp = 150.0;
ClampHealth(hp);
Print(hp);  // 100.0
```

Vanilla examples of `inout`:

```c
// From enmath.c — smoothing function reads and writes velocity
proto static float SmoothCD(float val, float target, inout float velocity[],
    float smoothTime, float maxVelocity, float dt);

// From enscript.c — parsing modifies the input string
proto int ParseStringEx(inout string input, string token);

// From Pawn (3_game/entities/pawn.c) — transform is read and modified
event void GetTransform(inout vector transform[4])
```

### notnull Parameters

The `notnull` keyword declares that a parameter must never receive `null`. It is widely used in vanilla — 139 script files contain it — and it appears on both engine bindings and ordinary script functions.

**What its enforcement actually is, is not documented.** `notnull` is absent from Bohemia's Enforce Script syntax page: it appears in neither the function-modifier table nor the variable-modifier table, so there is no primary description of whether it is checked at compile time, at runtime, or both. Community references disagree on the point. This chapter does not resolve it.

What vanilla's own usage shows is that the engine treats the guarantee as real and does not re-check it. `array<T>.InsertAll` is plain script, not a native binding, and dereferences its parameter immediately:

```c
// 1_core/proto/enscript.c:449
void InsertAll(notnull array<T> from)
{
    int nFrom = from.Count();   // no null check — the modifier is the contract
    ...
}
```

**What to do, either way:** treat `notnull` as a contract you must honour at the call site, not as a safety net you can lean on.

```c
void ProcessEntity(notnull EntityAI entity)
{
    string name = entity.GetType();
    Print(name);
}

// Honour the contract at the call site:
if (entity)
    ProcessEntity(entity);
```

This matters most for references that can go null *between* your check and the call — engine-side entity deletion is the classic case. Marking a parameter `notnull` does not make that scenario safe under any of the candidate semantics, so guard it yourself. See [Error Handling](11-error-handling.md#the-notnull-keyword) and [Memory Management](08-memory-management.md#notnull-parameter-modifier).

Vanilla uses `notnull` heavily in engine-facing functions:

```c
// From envisual.c
proto native void SetBone(notnull IEntity ent, int bone, vector angles, vector trans, float scale);
proto native bool GetBoneMatrix(notnull IEntity ent, int bone, vector mat[4]);

// From DamageSystem
static bool GetDamageZoneFromComponentName(notnull EntityAI entity, string component, out string damageZone);
```

You can combine `notnull` with `out`:

```c
// From universaltemperaturesourcelambdabaseimpl.c
override void DryItemsInVicinity(UniversalTemperatureSourceSettings pSettings, vector position,
    out notnull array<EntityAI> nearestObjects);
```

---

## Return Values

### Single Return Value

Functions return a single value. The return type is declared before the function name.

```c
float GetDistanceBetween(vector a, vector b)
{
    return vector.Distance(a, b);
}
```

### void (No Return)

Use `void` for functions that perform an action without returning data.

```c
void LogMessage(string msg)
{
    Print(string.Format("[Lantern] %1", msg));
}
```

### Returning Objects

When a function returns an object, it returns a **reference** (not a copy). The caller receives a pointer to the same object in memory.

```c
EntityAI SpawnItem(string className, vector pos)
{
    EntityAI item = EntityAI.Cast(GetGame().CreateObject(className, pos, false, false, true));
    return item;  // caller gets a reference to the same object
}
```

### Multiple Return Values via out Parameters

When you need to return more than one value, use `out` parameters. This is a universal pattern in DayZ scripting.

```c
void GetTimeComponents(float totalSeconds, out int hours, out int minutes, out int seconds)
{
    hours = (int)(totalSeconds / 3600);
    minutes = (int)((totalSeconds % 3600) / 60);
    seconds = (int)(totalSeconds % 60);
}

// Usage:
int h, m, s;
GetTimeComponents(3725, h, m, s);
// h == 1, m == 2, s == 5
```

### GOTCHA: JsonFileLoader Returns void

A common trap: `JsonFileLoader<T>.JsonLoadFile()` returns `void`, not the loaded object. You must pass a pre-created object as a `ref` parameter.

```c
// WRONG — will not compile
MyConfig config = JsonFileLoader<MyConfig>.JsonLoadFile(path);

// CORRECT — pass a ref object
MyConfig config = new MyConfig;
JsonFileLoader<MyConfig>.JsonLoadFile(path, config);
```

---

## Default Parameter Values

Enforce Script supports default values for parameters. Parameters with defaults must come **after** all required parameters.

```c
void SpawnItem(string className, vector pos, float quantity = -1, bool withAttachments = true)
{
    // quantity defaults to -1 (full), withAttachments defaults to true
    ItemBase item = ItemBase.Cast(GetGame().CreateObject(className, pos, false, false, withAttachments));
    if (item && quantity >= 0)
        item.SetQuantity(quantity);
}

// All of these are valid calls:
SpawnItem("AKM", myPos);                   // uses both defaults
SpawnItem("AKM", myPos, 0.5);             // custom quantity, default attachments
SpawnItem("AKM", myPos, -1, false);        // must specify quantity to reach attachments
```

### Default Values From Vanilla

The vanilla scripts use default parameters extensively:

```c
// From Weather (3_game/weather.c)
proto native void Set(float forecast, float time = 0, float minDuration = 0);
proto native void SetDynVolFogDistanceDensity(float value, float time = 0);

// From UAInput (3_game/inputapi/uainput.c)
proto native float SyncedValue_ID(int action, bool check_focus = true);
proto native bool SyncedPress(string action, bool check_focus = true);

// From DbgUI (1_core/proto/dbgui.c)
static bool FloatOverride(string id, inout float value, float min, float max,
    int precision = 1000, bool sameLine = true);

// From InputManager (2_gamelib/inputmanager.c)
proto native external bool ActivateAction(string actionName, int duration = 0);
```

### Limitations

1. **Literal values only** --- you cannot use expressions, function calls, or other variables as defaults:

```c
// WRONG — no expressions in defaults
void MyFunc(float speed = Math.PI * 2)  // COMPILE ERROR

// CORRECT — use a literal
void MyFunc(float speed = 6.283)
```

2. **No named parameters** --- you cannot skip a parameter by name. To set the third default, you must provide all preceding parameters:

```c
void Configure(int a = 1, int b = 2, int c = 3) {}

Configure(1, 2, 10);  // must specify a and b to set c
// There is no syntax like Configure(c: 10)
```

3. **Default values for class types are restricted to `null` or `NULL`:**

```c
void DoWork(EntityAI target = null, string name = "")
{
    if (!target) return;
    // ...
}
```

---

## Parameter Limit: 16 Maximum

Enforce Script methods cannot have more than 16 parameters; a 17th parameter is a compile error.

Bohemia's 1.28 release notes list this under **MODDING → ADDED**: *"Enforce Script: Compiler error when script methods exceed the maximum amount of parameters: 16, this has always been a limitation, previously the game would continue with buffer overflows and random crashes"* ([Stable Update 1.28](https://forums.dayz.com/topic/266370-stable-update-128/) — *PC Stable 1.28 Update 1, Version 1.28.159992*, posted 2 June 2025 by merropa93 (DayZ Community Support); accessed 2026-09-11).

Two different dates live in that sentence. **The 16-parameter limit itself is longstanding** — Bohemia's words are "this has always been a limitation." **The compiler error is what 1.28 added.** Bohemia describes the pre-diagnostic behavior as the game continuing "with buffer overflows and random crashes"; that is their account of it, not a runtime observation by this audit, and no claim is made here about the native implementation:

```c
// COMPILE ERROR in 1.28+ — 17 parameters exceeds the limit
void TooManyParams(int a, int b, int c, int d, int e, int f, int g, int h,
                   int i, int j, int k, int l, int m, int n, int o, int p,
                   int q)
{
}
```

**Solution:** Pass a class or array instead of many individual parameters:

```c
class MyParams
{
    int a, b, c, d, e;
    float x, y, z;
    string name;
}

void ProcessData(MyParams params)
{
    // Access params.a, params.b, etc.
}
```

---

## Proto Native Methods (Engine Bindings)

Proto native methods are declared in script but **implemented in the C++ engine**. They form the bridge between your Enforce Script code and the DayZ game engine. You call them like normal methods, but you cannot see or modify their implementation.

### Modifier Reference

| Modifier | Meaning | Example |
|----------|---------|---------|
| `proto native` | Implemented in C++ engine code | `proto native void SetPosition(vector pos);` |
| `proto native owned` | Returns a value the caller owns (manages memory) | `proto native owned string GetType();` |
| `proto native external` | Defined in another module | `proto native external bool AddSettings(typename cls);` |
| `proto volatile` | Has side effects; compiler must not optimize away | `proto volatile int Call(Class inst, string fn, void parm);` |
| `proto` (without `native`) | Internal function, may or may not be native | `proto int ParseString(string input, out string tokens[]);` |

### proto native

The most common modifier. These are straightforward engine calls.

```c
// Setting/getting position (Object)
proto native void SetPosition(vector pos);
proto native vector GetPosition();

// AI pathfinding (AIWorld)
proto native bool FindPath(vector from, vector to, PGFilter pgFilter, out TVectorArray waypoints);
proto native bool SampleNavmeshPosition(vector position, float maxDistance, PGFilter pgFilter,
    out vector sampledPosition);
```

### proto native owned

The `owned` modifier means the return value is allocated by the engine and **ownership is transferred to the script**. This is primarily used for `string` returns, where the engine creates a new string that the script's garbage collector must later free.

```c
// From Class (enscript.c) — returns a string the script now owns
proto native owned external string ClassName();

// From Widget (enwidgets.c)
proto native owned string GetName();
proto native owned string GetTypeName();
proto native owned string GetStyleName();

// From Object (3_game/entities/object.c)
proto native owned string GetLODName(LOD lod);
proto native owned string GetActionComponentName(int componentIndex, string geometry = "");
```

### proto native external

The `external` modifier indicates the function is defined in a different script module. This allows cross-module method declarations.

```c
// From Settings (2_gamelib/settings.c)
proto native external bool AddSettings(typename settingsClass);

// From InputManager (2_gamelib/inputmanager.c)
proto native external bool RegisterAction(string actionName);
proto native external float LocalValue(string actionName);
proto native external bool ActivateAction(string actionName, int duration = 0);

// From Workbench API (1_core/workbenchapi.c)
proto native external bool SetOpenedResource(string filename);
proto native external bool Save();
```

### proto volatile

The `volatile` modifier tells the compiler the function may have **side effects** or may **call back into script** (creating re-entrancy). The compiler must preserve full context when calling these.

```c
// From ScriptModule (enscript.c) — dynamic function calls that may invoke script
proto volatile int Call(Class inst, string function, void parm);
proto volatile int CallFunction(Class inst, string function, out void returnVal, void parm);

// From typename (enconvert.c) — creates a new instance dynamically
proto volatile Class Spawn();

// Yielding control
proto volatile void Idle();
```

### Calling Proto Native Methods

You call them like any other method. The key rule: **never try to override or redefine a proto native method**. They are fixed engine bindings.

```c
// Calling proto native methods — no different from script methods
Object obj = GetGame().CreateObject("AKM", pos, false, false, true);
vector position = obj.GetPosition();
string typeName = obj.GetType();     // script wrapper over g_Game.ObjectGetType()
obj.SetPosition(newPos);             // native void — no return
```

---

## Static vs Instance Methods

### When to Use Static

Use static methods when the function does not need any instance data:

```c
class StringUtils
{
    // Pure utility — no state needed
    static bool IsNullOrEmpty(string s)
    {
        return s == "" || s.Length() == 0;
    }

    static string PadLeft(string s, int totalWidth, string padChar = "0")
    {
        while (s.Length() < totalWidth)
            s = padChar + s;
        return s;
    }
}
```

**Common static use cases:**
- **Utility functions** --- math helpers, string formatters, validation checks
- **Factory methods** --- `Create()` that returns a new configured instance
- **Singleton accessors** --- `GetInstance()` that returns the single instance
- **Constants/lookups** --- `Init()` + `Cleanup()` for static data tables

### Singleton Pattern (Static + Instance)

Many DayZ managers combine static and instance:

```c
class NotificationManager
{
    private static ref NotificationManager s_Instance;

    static NotificationManager GetInstance()
    {
        if (!s_Instance)
            s_Instance = new NotificationManager;
        return s_Instance;
    }

    // Instance methods for actual work
    void ShowNotification(string text, float duration)
    {
        // ...
    }
}

// Usage:
NotificationManager.GetInstance().ShowNotification("Hello", 5.0);
```

### When to Use Instance

Use instance methods when the function needs access to the object's state:

```c
class SupplyDrop
{
    protected vector m_DropPosition;
    protected float m_DropRadius;
    protected ref array<string> m_LootTable;

    // Needs m_DropPosition, m_DropRadius — must be instance
    bool IsInDropZone(vector testPos)
    {
        return vector.Distance(m_DropPosition, testPos) <= m_DropRadius;
    }

    // Needs m_LootTable — must be instance
    string GetRandomItem()
    {
        return m_LootTable.GetRandomElement();
    }
}
```

---

## Method Overriding

When a child class needs to change the behavior of a parent method, it uses the `override` keyword.

### Basic Override

```c
class BaseModule
{
    void OnInit()
    {
        Print("[BaseModule] Initialized");
    }

    void OnUpdate(float dt)
    {
        // default: do nothing
    }
}

class CombatModule extends BaseModule
{
    override void OnInit()
    {
        super.OnInit();  // call parent first
        Print("[CombatModule] Combat system ready");
    }

    override void OnUpdate(float dt)
    {
        super.OnUpdate(dt);
        // custom combat logic
        CheckCombatState();
    }
}
```

### Rules for Overriding

1. **`override` keyword is required** --- on DayZDiag `1.29.0.163709`, omitting it from a same-signature child method emits `Overriding function '<name>' but not marked as 'override'` and prevents the Mission module from compiling.

2. **Signature must match exactly** --- same return type, same parameter types, same parameter count.

3. **`super.MethodName()` calls the parent** --- use this to extend behavior rather than completely replace it.

4. **Private methods cannot be overridden** --- they are invisible to child classes.

5. **Protected methods can be overridden** --- child classes see and can override them.

```c
class Parent
{
    private void SecretMethod() {}    // cannot be overridden
    protected void InternalWork() {}  // can be overridden by children
    void PublicWork() {}              // can be overridden by anyone
}

class Child extends Parent
{
    // override void SecretMethod() {}   // COMPILE ERROR — private
    override void InternalWork() {}      // OK — protected is visible
    override void PublicWork() {}        // OK — public
}
```

### GOTCHA: Forgetting override

On DayZDiag `1.29.0.163709`, a child method with the same signature as a parent method must be marked `override`. Omitting the keyword emits `Overriding function '<name>' but not marked as 'override'` and prevents the Mission module from compiling. A positive probe showed base-typed dispatch selecting the child method when it was explicitly marked `override`.

```c
class Animal
{
    void Speak() { Print("..."); }
}

class Dog extends Animal
{
    // BAD: uncommenting this produces the omitted-override compiler error.
    // void Speak() { Print("Woof!"); }

    // GOOD: Properly overrides
    override void Speak() { Print("Woof!"); }
}
```

---

## Method Overloading (Supported, Rarely Used)

**The compiler does resolve overloads.** An earlier version of this chapter said otherwise; shipped vanilla code disproves it.

`class InputUtils` in `3_game/tools/inpututils.c` declares the same method twice inside one class body, differing only in the type of the first parameter:

```c
// 3_game/tools/inpututils.c:118
static void GetImagesetAndIconFromInputAction(notnull UAInput pInput, int pInputDeviceType,
    out array<string> pImageSet, out array<string> pIconName)
{ /* ... */ }

// 3_game/tools/inpututils.c:160 — same name, same arity, different first parameter type
static void GetImagesetAndIconFromInputAction(string pInputAction, int pInputDeviceType,
    out array<string> pImageSet, out array<string> pIconName)
{
    UAInput inp = GetUApi().GetInputByName(pInputAction);
    InputUtils.GetImagesetAndIconFromInputAction(inp, pInputDeviceType, pImageSet, pIconName);  // :164
}
```

`GetRichtextButtonIconFromInputAction` is overloaded the same way at `:167` and `:198`. Overloading by **arity** also works in shipping community code — Community Online Tools declares `_Sleep(int, out int)` at `JMESPModule.c:720` and `_Sleep(int, out int, inout int)` at `:726`, and calls both.

**Why the workarounds below still matter.** Vanilla almost never overloads. The three patterns that follow are the dominant idiom across the 2,800-file script tree, and code written that way reads the way the rest of the API reads. Prefer them for style, not because the alternative fails to compile.

> **Not established here:** these examples prove overload resolution works for a distinct-type first parameter and for differing arity. They do not establish how the compiler resolves an ambiguous case — two overloads whose parameter types are mutually convertible, for instance. If you overload, keep the signatures obviously distinct.

### Pattern 1: Different Method Names

The most common approach is to use descriptive names:

```c
class Calculator
{
    int AddInt(int a, int b) { return a + b; }
    float AddFloat(float a, float b) { return a + b; }
}
```

### Pattern 2: The Ex() Convention

DayZ vanilla and mods follow a naming convention where an extended version of a method appends `Ex` to the name:

```c
// From DayZGame — base version vs extended version
void ExplosionEffects(Object source, Object directHit, int componentIndex, string surface,
    vector pos, vector surfNormal, float energyFactor, float explosionFactor, bool isWater,
    string ammoType);
void ExplosionEffectsEx(Object source, Object directHit, int componentIndex,
    float energyFactor, float explosionFactor, HitInfo hitInfo);

// From SEffectManager
static void EffectUnregister(int id);
static void EffectUnregisterEx(Effect effect);

// Base is on ItemBase; the Ex variant is declared on EntityAI
void SplitIntoStackMax(EntityAI destination_entity, int slot_id, PlayerBase player);
void SplitIntoStackMaxEx(EntityAI destination_entity, int slot_id);
```

### Pattern 3: Default Parameters

If the difference is just optional parameters, use defaults instead:

```c
class Spawner
{
    // Instead of overloads, use defaults
    void SpawnAt(vector pos, float radius = 0, string filter = "")
    {
        // one method handles all cases
    }
}
```

---

## The event Keyword

The `event` keyword marks a method as an **engine event handler** --- a function that the C++ engine calls at specific moments (entity creation, animation events, physics callbacks, etc.). It is a hint for tooling (like Workbench) that the method should be exposed as a script event.

```c
// From Pawn (3_game/entities/pawn.c)
protected event void OnPossess()
{
    // called by engine when a controller possesses this pawn
}

protected event void OnUnPossess()
{
    // called by engine when the controller releases this pawn
}

// Event methods that supply data for networking
protected event void ObtainMove(PawnMove pMove)
{
    // called by engine to gather movement input
}
```

Event signatures are engine-defined and must be verified on the exact parent class and build feature set before overriding them. For example, `PawnMove.GetTransform` exists only when both `FEATURE_NETWORK_RECONCILIATION` and `DIAG_DEVELOPER` expose the relevant classes:

```c
#ifdef FEATURE_NETWORK_RECONCILIATION
#ifdef DIAG_DEVELOPER
class MyMove extends PawnMove
{
    override event void GetTransform(inout vector transform[4])
    {
        super.GetTransform(transform);
    }
}
#endif
#endif
```

The key takeaway: `event` is a declaration modifier, not something you invoke. The engine calls event methods at the appropriate time.

---

## Thread Methods (Coroutines)

The `thread` keyword starts a function asynchronously: it runs, can pause itself with `Sleep()`, and resumes later without blocking the caller.

**How parallel is it?** Bohemia's keyword table says `thread` "runs the function on a new thread", and the engine doc block on `ScriptModule.Call` notes that the call "creates new thread, so it's legal to use sleep/wait" while `CallFunction` "do not create new thread" (`1_core/proto/enscript.c:137,144`). In practice these routines behave like cooperative coroutines that yield at `Sleep()`, which is the common community reading and matches how mods use them --- but the underlying scheduling is not documented, and this chapter does not establish it. Whichever model is correct, the rule for your code is the same: **never rely on two pieces of script running in parallel, and never use `thread` in place of proper synchronisation.**

### Declaring and Starting a Thread

You start a thread by calling a function with the `thread` keyword preceding the call:

```c
class Monitor
{
    void Start()
    {
        thread MonitorLoop();
    }

    void MonitorLoop()
    {
        while (true)
        {
            CheckStatus();
            Sleep(1000);  // yield for 1000 milliseconds
        }
    }
}
```

The `thread` keyword goes on the **call**, not the function declaration. The function itself is a normal function --- what makes it a coroutine is how you invoke it.

### Sleep() and Yielding

Inside a thread function, `Sleep(milliseconds)` pauses execution and yields to other code. When the sleep time elapses, the thread resumes from where it left off.

> **Note:** `Sleep()` is an engine built-in (intrinsic) --- there is no `proto` declaration for it anywhere in the script files, and it takes an `int` in milliseconds. Vanilla never calls it; community frameworks call it only from inside functions started with `thread` (for example `_Sleep` in Community Online Tools' `JMESPModule.c:720`). Use it only in a threaded context. What happens when it is called outside one is not documented, and is not established here.

### Killing Threads

You can terminate a running thread with `KillThread()`:

```c
// From enscript.c
proto native int KillThread(Class owner, string name);

// Usage:
KillThread(this, "MonitorLoop");  // stops the MonitorLoop coroutine
```

The `owner` is the object that started the thread (or `null` for global threads). The `name` is the function name.

### When to Use Threads (and When Not To)

**Prefer `CallLater` and timers over threads.** Thread coroutines have limitations:
- They are harder to debug (stack traces are less clear)
- They consume a coroutine slot that persists until completion or kill
- They cannot be serialized or transferred across network boundaries

Use threads only when you genuinely need a long-running loop with intermediate yields. For one-shot delayed actions, use `CallLater` (see below). For the full comparison of threads, managed `Timer` objects, and the CallQueue, see [Timers & CallQueue](../06-engine-api/07-timers.md).

---

## Deferred Calls with CallLater

`CallLater` schedules a function call to execute after a delay. It is the primary alternative to thread coroutines and is used extensively in vanilla DayZ.

### Syntax

```c
// Declaration on ScriptCallQueue (2_gamelib/tools.c) — abbreviated:
// proto void CallLater(func fn, int delay = 0, bool repeat = false,
//     void param1 = NULL, /* ... */ void param9 = NULL);

g_Game.GetCallQueue(CALL_CATEGORY_SYSTEM).CallLater(FunctionToCall, delayMs, repeat);
```

| Parameter | Type | Description |
|-----------|------|-------------|
| Function | `func` | The method to call |
| Delay | `int` | Milliseconds before calling (default `0`) |
| Repeat | `bool` | `true` to repeat at interval, `false` for one-shot (default) |
| Extra args | `void` (9 optional slots) | Forwarded to the target function when the call fires |

> **Isn't that variadic?** Enforce Script has no variadic parameters — your own functions cannot declare `...` (see [No Variadic Parameters](12-gotchas.md#no-variadic-parameters)). `CallLater` only *looks* variadic: its engine-side `proto` declaration takes nine optional `void`-typed parameters defaulting to `NULL`, so the call site accepts up to nine extra arguments of any type. You cannot write this shape in script yourself — the `void` parameter type is only usable in engine `proto` declarations.

### Call Categories

| Category | Purpose |
|----------|---------|
| `CALL_CATEGORY_SYSTEM` | General-purpose, runs every frame |
| `CALL_CATEGORY_GUI` | UI-related callbacks |
| `CALL_CATEGORY_GAMEPLAY` | Gameplay logic callbacks |

### Examples from Vanilla

```c
// One-shot delayed call (3_game/entities/entityai.c)
g_Game.GetCallQueue(CALL_CATEGORY_SYSTEM).CallLater(DeferredInit, 34);

// Repeated call — login countdown every 1 second (3_game/dayzgame.c)
GetCallQueue(CALL_CATEGORY_SYSTEM).CallLater(this.LoginTimeCountdown, 1000, true);

// Delayed deletion with parameter (4_world/entities/explosivesbase)
g_Game.GetCallQueue(CALL_CATEGORY_SYSTEM).CallLater(DeleteSafe, delayFor * 1000, false);

// UI delayed callback (3_game/gui/hints/uihintpanel.c)
m_Game.GetCallQueue(CALL_CATEGORY_GUI).CallLater(SlideshowThread, m_SlideShowDelay);
```

### Removing Queued Calls

To cancel a scheduled call before it fires:

```c
g_Game.GetCallQueue(CALL_CATEGORY_SYSTEM).Remove(FunctionToCall);
```

The CallQueue is covered in depth — alongside managed `Timer` objects — in [Timers & CallQueue](../06-engine-api/07-timers.md).

---

## Best Practices

1. **Keep functions short** --- aim for under 50 lines. If a function is longer, extract helper methods.

2. **Use guard clauses for early return** --- check preconditions at the top and return early. This reduces nesting and makes the "happy path" easier to read.

```c
void ProcessPlayer(PlayerBase player)
{
    if (!player) return;
    if (!player.IsAlive()) return;
    if (!player.GetIdentity()) return;

    // actual logic here, unnested
    string name = player.GetIdentity().GetName();
    // ...
}
```

3. **Prefer out parameters over complex return types** --- when a function needs to communicate success/failure plus data, use a `bool` return with `out` parameters.

4. **Use static for stateless utilities** --- if a method does not access `this`, make it `static`. This documents intent and allows calling without an instance.

5. **Document proto native limitations** --- when wrapping a proto native call, note in comments what the engine function can and cannot do.

6. **Prefer CallLater over thread coroutines** --- `CallLater` is simpler, easier to cancel, and less error-prone.

7. **Always call super in overrides** --- unless you intentionally want to completely replace the parent behavior. DayZ's deep inheritance chains depend on `super` calls propagating through the hierarchy.

---

## Common Method Conventions

These conventions appear throughout the vanilla scripts and across the community mod ecosystem. Adopting them makes your code instantly readable to other DayZ modders.

| Pattern | Grounding | Detail |
|---------|-----------|--------|
| `TryGet...()` returning `bool` with an `out` param | Widespread community practice | For lookups that can fail: return `true`/`false` and fill the `out` parameter on success, instead of returning a nullable object |
| `...Ex()` suffix for extended signatures | Vanilla (`ExplosionEffectsEx`, `SEffectManager.EffectUnregisterEx`) | When an API needs more parameters, add an `Ex` variant rather than breaking existing callers |
| Static `Init()` + `Cleanup()` pairs | Vanilla (`AmmoEffects`, `PPERequesterBank` in `3_game`) | Manager classes build static data in `Init()` and release it in `Cleanup()`, called from the game/mission lifecycle (`MissionServer.OnInit()` loads data, `MissionGameplay.OnMissionFinish()` tears down) |
| Null-guarding the game instance at method start | Vanilla (`SEffectManager` checks `g_Game` before use in `3_game/effectmanager.c`) | Methods that can run during startup or shutdown open with guard clauses to avoid crashes |
| Singleton `GetInstance()` with lazy creation | See [Singletons](../07-patterns/01-singletons.md) | Managers expose a `private static ref` instance behind a static accessor, created on first access |

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| Method overloading | Standard OOP feature | Supported (vanilla `InputUtils` overloads by parameter type), but vanilla style is distinct names, the `Ex()` suffix or default parameters |
| `thread` creates OS threads | Bohemia's keyword table does say it "runs the function on a new thread" | In practice threaded routines behave as cooperative coroutines yielding at `Sleep()`. The scheduling model is undocumented either way --- write code that never depends on parallel execution |
| `out` parameters are write-only | Should not read initial value | Some vanilla code reads the `out` param before writing; safer to always treat as `inout` defensively |
| `override` is optional | Could be inferred | On DayZDiag `1.29.0.163709`, omitting it for a same-signature child method prevents the Mission module from compiling; always include it |
| Default parameter expressions | Should support function calls | Literals, NULL, and supported compile-time constants such as enum members are allowed; runtime function calls are not |

---

## Common Mistakes

### 1. Forgetting override When Replacing a Parent Method

On DayZDiag `1.29.0.163709`, a child method with the same signature as a parent method must be marked `override`. Omitting the keyword emits `Overriding function '<name>' but not marked as 'override'` and prevents the Mission module from compiling.

```c
class CustomPlayer extends PlayerBase
{
    // BAD: uncommenting this produces the omitted-override compiler error.
    // void OnConnect() { Print("Custom!"); }

    // GOOD: properly overrides.
    override void OnConnect() { Print("Custom!"); }
}
```

### 2. Expecting out Parameters to Be Pre-initialized

An `out` parameter has no guaranteed initial value. Never read it before writing.

```c
// BAD — reading out param before it's set
void GetData(out int value)
{
    if (value > 0)  // WRONG — value is undefined here
        return;
    value = 42;
}

// GOOD — always write first, then read
void GetData(out int value)
{
    value = 42;
}
```

### 3. Overloading Where a Name Would Read Better

Overloading compiles (see [Method Overloading](#method-overloading-supported-rarely-used)), but it is not how vanilla is written, and a reader scanning for `Process` has to check every declaration to know which one runs.

```c
// Compiles, but unusual in DayZ script
void Process(int id) {}
void Process(string name) {}

// Vanilla idiom — self-describing at the call site
void ProcessById(int id) {}
void ProcessByName(string name) {}
```

### 4. Assigning the Return of a void Function

Some functions (notably `JsonFileLoader.JsonLoadFile`) return `void`. Trying to assign their result causes a compile error.

```c
// COMPILE ERROR — JsonLoadFile returns void
MyConfig cfg = JsonFileLoader<MyConfig>.JsonLoadFile(path);

// CORRECT
MyConfig cfg = new MyConfig;
JsonFileLoader<MyConfig>.JsonLoadFile(path, cfg);
```

### 5. Using Expressions in Default Parameters

Default parameter values may use literals, NULL, and supported compile-time constants such as enum members; runtime function calls are not valid defaults.

```c
// COMPILE ERROR — expression in default
void SetTimeout(float seconds = GetDefaultTimeout()) {}
void SetAngle(float rad = Math.PI) {}

// CORRECT — literal values only
void SetTimeout(float seconds = 30.0) {}
void SetAngle(float rad = 3.14159) {}
```

### 6. Forgetting super in Override Chains

DayZ's class hierarchies are deep. Omitting `super` in an override can break functionality several layers up the chain that you never even knew existed.

```c
// BAD — breaks parent initialization
class MyMission extends MissionServer
{
    override void OnInit()
    {
        // forgot super.OnInit() — vanilla initialization never runs!
        Print("My mission started");
    }
}

// GOOD
class MyMission extends MissionServer
{
    override void OnInit()
    {
        super.OnInit();  // let vanilla + other mods initialize first
        Print("My mission started");
    }
}
```

---

## Quick Reference Table

| Feature | Syntax | Notes |
|---------|--------|-------|
| Instance method | `void DoWork()` | Has access to `this` |
| Static method | `static void DoWork()` | Called via `ClassName.DoWork()` |
| By-value param | `void Fn(int x)` | Copy for primitives; ref copy for objects |
| `out` param | `void Fn(out int x)` | Write-only; caller receives value |
| `inout` param | `void Fn(inout float x)` | Read + write; caller sees changes |
| `notnull` param | `void Fn(notnull EntityAI e)` | Declares "null is a programming error here". Enforcement is undocumented — null-check at the call site regardless |
| Default value | `void Fn(int x = 5)` | Literals, NULL, and supported compile-time constants such as enum members; no runtime function calls |
| Override | `override void Fn()` | Must match parent signature |
| Call parent | `super.Fn()` | Inside override body |
| Proto native | `proto native void Fn()` | Implemented in C++ |
| Owned return | `proto native owned string Fn()` | Script manages returned memory |
| External | `proto native external void Fn()` | Defined in another module |
| Volatile | `proto volatile void Fn()` | May callback into script |
| Event | `event void Fn()` | Engine-invoked callback |
| Thread start | `thread MyFunc()` | Starts coroutine (not OS thread) |
| Kill thread | `KillThread(owner, "FnName")` | Stops a running coroutine |
| Deferred call | `CallLater(Fn, delay, repeat)` | Preferred over threads |
| `Ex()` convention | `void FnEx(...)` | Extended version of `Fn` |
| Parameter limit | 16 parameters max | Compile error past that (diagnostic added in 1.28; the limit itself is longstanding); use a class for more |
