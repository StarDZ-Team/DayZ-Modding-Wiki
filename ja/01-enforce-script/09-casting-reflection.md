# Chapter 1.9: Casting & Reflection

[Home](../../README.md) | [<< Previous: Memory Management](08-memory-management.md) | **Casting & Reflection** | [Next: Enums & Preprocessor >>](10-enums-preprocessor.md)

---

## 目次

- [Why Casting Matters](#why-casting-matters)
- [Class.CastTo — Safe Downcasting](#classcastto--safe-downcasting)
- [Type.Cast — Alternative Casting](#typecast--alternative-casting)
- [CastTo vs Type.Cast — When to Use Which](#castto-vs-typecast--when-to-use-which)
- [obj.IsInherited — Runtime Type Checking](#obisinherited--runtime-type-checking)
- [obj.IsKindOf — String-Based Type Checking](#obiskindof--string-based-type-checking)
- [obj.Type — Get Runtime Type](#objtype--get-runtime-type)
- [typename — Storing Type References](#typename--storing-type-references)
- [Reflection API](#reflection-api)
  - [Inspecting Variables](#inspecting-variables)
  - [EnScript.GetClassVar / SetClassVar](#enscriptgetclassvar--setclassvar)
- [Real-World Examples](#real-world-examples)
  - [Finding All Vehicles in the World](#finding-all-vehicles-in-the-world)
  - [Safe Object Helper With Cast](#safe-object-helper-with-cast)
  - [Reflection-Based Config System](#reflection-based-config-system)
  - [Type-Safe Event Dispatch](#type-safe-event-dispatch)
- [Common Mistakes](#common-mistakes)
- [Summary](#summary)
- [Navigation](#navigation)

---

## キャストが重要な理由

DayZ のエンティティ階層は深いです。ほとんどのエンジン API は汎用的な基底型（`Object`、`Man`、`Class`）を返しますが、特殊なメソッドにアクセスするには特定の型（`PlayerBase`、`ItemBase`、`CarScript`）が必要です。キャストは基底参照を派生参照に安全に変換します。

```
Class (root)
  └─ Object
       └─ Entity
            └─ EntityAI
                 ├─ InventoryItem → ItemBase
                 ├─ DayZCreatureAI
                 │    ├─ DayZInfected
                 │    └─ DayZAnimal
                 └─ Man
                      └─ DayZPlayer → PlayerBase
```

Calling a method that doesn't exist on the base type causes a **runtime crash** — there is no compiler error because Enforce Script resolves virtual calls at runtime.

---

## Class.CastTo — 安全なダウンキャスト

`Class.CastTo` は DayZ で**推奨される**キャスト方法です。 結果を `out` パラメータに書き込み `bool` を返す静的メソッドです。

```c
// Signature:
// static bool Class.CastTo(out Class target, Class source)

Object obj = GetSomeObject();
PlayerBase player;

if (Class.CastTo(player, obj))
{
    // Cast succeeded — player is valid
    string name = player.GetIdentity().GetName();
    Print("Found player: " + name);
}
else
{
    // Cast failed — obj is not a PlayerBase
    // player is null here
}
```

**推奨される理由：**
- Returns `false` on failure instead of crashing
- The `out` parameter is set to `null` on failure — safe to check
- Works across the entire class hierarchy (not just `Object`)

### Pattern: Cast-and-Continue

In loops, use cast failure to skip irrelevant objects:

```c
array<Object> nearObjects = new array<Object>;
array<CargoBase> proxyCargos = new array<CargoBase>;
GetGame().GetObjectsAtPosition(pos, 50.0, nearObjects, proxyCargos);

foreach (Object obj : nearObjects)
{
    EntityAI entity;
    if (!Class.CastTo(entity, obj))
        continue;  // Skip non-EntityAI objects (buildings, terrain, etc.)

    // Now safe to call EntityAI methods
    if (entity.IsAlive())
    {
        Print(entity.GetType() + " is alive at " + entity.GetPosition().ToString());
    }
}
```

---

## Type.Cast — 代替キャスト

すべてのクラスにはキャスト結果を直接返す（失敗時は `null`）静的 `Cast` メソッドがあります。

```c
// Syntax: TargetType.Cast(source)

Object obj = GetSomeObject();
PlayerBase player = PlayerBase.Cast(obj);

if (player)
{
    player.DoSomething();
}
```

This is a one-liner that combines cast and assignment, but you **must** still null-check the result.

### Casting Primitives and Params

`Type.Cast` is also used with `Param` classes (used heavily in RPCs and events):

```c
override void OnEvent(EventType eventTypeId, Param params)
{
    if (eventTypeId == ClientReadyEventTypeID)
    {
        Param2<PlayerIdentity, Man> readyParams = Param2<PlayerIdentity, Man>.Cast(params);
        if (readyParams)
        {
            PlayerIdentity identity = readyParams.param1;
            Man player = readyParams.param2;
        }
    }
}
```

---

## CastTo と Type.Cast の使い分け

| Feature | `Class.CastTo` | `Type.Cast` |
|---------|----------------|-------------|
| Return type | `bool` | Target type or `null` |
| Null on failure | Yes (out param set to null) | Yes (returns null) |
| Best for | if-blocks with branching logic | One-liner assignments |
| Used in DayZ vanilla | Everywhere | Everywhere |
| Works with non-Object | Yes (any `Class`) | Yes (any `Class`) |

**経験則：** Use `Class.CastTo` when you branch on success/failure. Use `Type.Cast` when you just need the typed reference and will null-check later.

```c
// CastTo — branch on result
PlayerBase player;
if (Class.CastTo(player, obj))
{
    // handle player
}

// Type.Cast — assign and check later
PlayerBase player = PlayerBase.Cast(obj);
if (!player) return;
```

---

## obj.IsInherited — Runtime Type Checking

`IsInherited` はキャストを**行わずに**オブジェクトが指定された型のインスタンスかどうかをチェックします。 It takes a `typename` argument.

```c
Object obj = GetSomeObject();

if (obj.IsInherited(PlayerBase))
{
    Print("This is a player!");
}

if (obj.IsInherited(DayZInfected))
{
    Print("This is a zombie!");
}

if (obj.IsInherited(CarScript))
{
    Print("This is a vehicle!");
}
```

`IsInherited` returns `true` for the exact type **and** any parent types in the hierarchy. A `PlayerBase` object returns `true` for `IsInherited(Man)`, `IsInherited(EntityAI)`, `IsInherited(Object)`, etc.

---

## obj.IsKindOf — String-Based Type Checking

`IsKindOf` は同じチェックを **string** のクラス名で行います。 型名をデータとして持っている場合（設定ファイルからなど）に便利です。

```c
Object obj = GetSomeObject();

if (obj.IsKindOf("ItemBase"))
{
    Print("This is an item");
}

if (obj.IsKindOf("DayZAnimal"))
{
    Print("This is an animal");
}
```

**重要：** `IsKindOf` checks the full inheritance chain, just like `IsInherited`. A `Mag_STANAG_30Rnd` returns `true` for `IsKindOf("Magazine_Base")`, `IsKindOf("InventoryItem")`, `IsKindOf("EntityAI")`, etc.

### IsInherited vs IsKindOf

| Feature | `IsInherited(typename)` | `IsKindOf(string)` |
|---------|------------------------|---------------------|
| Argument | Compile-time type | String name |
| Speed | Faster (type comparison) | Slower (string lookup) |
| Use when | You know the type at compile time | Type comes from data/config |

---

## obj.Type — Get Runtime Type

`Type()` returns the `typename` of an object's actual runtime class — not the declared variable type.

```c
Object obj = GetSomeObject();
typename t = obj.Type();

Print(t.ToString());  // e.g., "PlayerBase", "AK101", "LandRover"
```

Use this for logging, debugging, or comparing types dynamically:

```c
void ProcessEntity(EntityAI entity)
{
    typename t = entity.Type();
    Print("Processing entity of type: " + t.ToString());

    if (t == PlayerBase)
    {
        Print("It's a player");
    }
}
```

---

## typename — Storing Type References

`typename` は Enforce Script のファーストクラス型です。 変数に格納し、パラメータとして渡し、比較できます。

```c
// Declare a typename variable
typename playerType = PlayerBase;
typename vehicleType = CarScript;

// Compare
typename objType = obj.Type();
if (objType == playerType)
{
    Print("Match!");
}

// Use in collections
array<typename> allowedTypes = new array<typename>;
allowedTypes.Insert(PlayerBase);
allowedTypes.Insert(DayZInfected);
allowedTypes.Insert(DayZAnimal);

// Check membership
foreach (typename t : allowedTypes)
{
    if (obj.IsInherited(t))
    {
        Print("Object matches allowed type: " + t.ToString());
        break;
    }
}
```

### Creating Instances from typename

You can create objects from a `typename` at runtime:

```c
typename t = PlayerBase;
Class instance = t.Spawn();  // Creates a new instance

// Or use the string-based approach:
Class instance2 = GetGame().CreateObjectEx("AK101", pos, ECE_PLACE_ON_SURFACE);
```

> **注意：** `typename.Spawn()` only works for classes with a parameterless constructor. For DayZ entities, use `GetGame().CreateObject()` or `CreateObjectEx()`.

---

## リフレクション API

Enforce Script は基本的なリフレクション機能を提供します — コンパイル時に型を知らなくても実行時にオブジェクトのプロパティを検査・変更する機能です。

### Inspecting Variables

Every object's `Type()` returns a `typename` that exposes variable metadata:

```c
void InspectObject(Class obj)
{
    typename t = obj.Type();

    int varCount = t.GetVariableCount();
    Print("Class: " + t.ToString() + " has " + varCount.ToString() + " variables");

    for (int i = 0; i < varCount; i++)
    {
        string varName = t.GetVariableName(i);
        typename varType = t.GetVariableType(i);

        Print("  [" + i.ToString() + "] " + varName + " : " + varType.ToString());
    }
}
```

**Available reflection methods on `typename`:**

| メソッド | 戻り値 | Description |
|--------|---------|-------------|
| `GetVariableCount()` | `int` | Number of member variables |
| `GetVariableName(int index)` | `string` | Variable name at index |
| `GetVariableType(int index)` | `typename` | Variable type at index |
| `ToString()` | `string` | Class name as string |

### EnScript.GetClassVar / SetClassVar

`EnScript.GetClassVar` and `EnScript.SetClassVar` let you read/write member variables by **name** at runtime. This is Enforce Script's equivalent of dynamic property access.

```c
// Signature:
// static void EnScript.GetClassVar(Class instance, string varName, int index, out T value)
// static bool EnScript.SetClassVar(Class instance, string varName, int index, T value)
// 'index' is the array element index — use 0 for non-array fields.

class MyConfig
{
    int MaxSpawns = 10;
    float SpawnRadius = 100.0;
    string WelcomeMsg = "Hello!";
}

void DemoReflection()
{
    MyConfig cfg = new MyConfig();

    // Read values by name
    int maxVal;
    EnScript.GetClassVar(cfg, "MaxSpawns", 0, maxVal);
    Print("MaxSpawns = " + maxVal.ToString());  // "MaxSpawns = 10"

    float radius;
    EnScript.GetClassVar(cfg, "SpawnRadius", 0, radius);
    Print("SpawnRadius = " + radius.ToString());  // "SpawnRadius = 100"

    string msg;
    EnScript.GetClassVar(cfg, "WelcomeMsg", 0, msg);
    Print("WelcomeMsg = " + msg);  // "WelcomeMsg = Hello!"

    // Write values by name
    EnScript.SetClassVar(cfg, "MaxSpawns", 0, 50);
    EnScript.SetClassVar(cfg, "SpawnRadius", 0, 250.0);
    EnScript.SetClassVar(cfg, "WelcomeMsg", 0, "Welcome!");
}
```

> **警告：** `GetClassVar`/`SetClassVar` silently fail if the variable name is wrong or the type doesn't match. Always validate variable names before use.

---

## 実践的な例

### Finding All Vehicles in the World

```c
static array<CarScript> FindAllVehicles()
{
    array<CarScript> vehicles = new array<CarScript>;
    array<Object> allObjects = new array<Object>;
    array<CargoBase> proxyCargos = new array<CargoBase>;

    // Search a large area (or use mission-specific logic)
    vector center = "7500 0 7500";
    GetGame().GetObjectsAtPosition(center, 15000.0, allObjects, proxyCargos);

    foreach (Object obj : allObjects)
    {
        CarScript car;
        if (Class.CastTo(car, obj))
        {
            vehicles.Insert(car);
        }
    }

    Print("Found " + vehicles.Count().ToString() + " vehicles");
    return vehicles;
}
```

### Safe Object Helper With Cast

This pattern is used throughout DayZ modding — a utility function that safely checks if an `Object` is alive by casting to `EntityAI`:

```c
// Object.IsAlive() does NOT exist on the base Object class!
// You must cast to EntityAI first.

static bool IsObjectAlive(Object obj)
{
    if (!obj)
        return false;

    EntityAI eai;
    if (Class.CastTo(eai, obj))
    {
        return eai.IsAlive();
    }

    return false;  // Non-EntityAI objects (buildings, etc.) — treat as "not alive"
}
```

### Reflection-Based Config System

This pattern (used in MyFramework) builds a generic config system where fields are read/written by name, enabling admin panels to edit any config without knowing its specific class:

```c
class ConfigBase
{
    // Find a member variable index by name
    protected int FindVarIndex(string fieldName)
    {
        typename t = Type();
        int count = t.GetVariableCount();
        for (int i = 0; i < count; i++)
        {
            if (t.GetVariableName(i) == fieldName)
                return i;
        }
        return -1;
    }

    // Get any field value as string
    string GetFieldValue(string fieldName)
    {
        if (FindVarIndex(fieldName) == -1)
            return "";

        int iVal;
        EnScript.GetClassVar(this, fieldName, 0, iVal);
        return iVal.ToString();
    }

    // Set any field value from string
    void SetFieldValue(string fieldName, string value)
    {
        if (FindVarIndex(fieldName) == -1)
            return;

        int iVal = value.ToInt();
        EnScript.SetClassVar(this, fieldName, 0, iVal);
    }
}

class MyModConfig : ConfigBase
{
    int MaxPlayers = 60;
    int RespawnTime = 300;
}

void AdminPanelSave(ConfigBase config, string fieldName, string newValue)
{
    // Works for ANY config subclass — no type-specific code needed
    config.SetFieldValue(fieldName, newValue);
}
```

### Type-Safe Event Dispatch

Use `typename` to build a dispatcher that routes events to the correct handler:

```c
class EventDispatcher
{
    protected ref map<typename, ref array<ref EventHandler>> m_Handlers;

    void EventDispatcher()
    {
        m_Handlers = new map<typename, ref array<ref EventHandler>>;
    }

    void Register(typename eventType, EventHandler handler)
    {
        if (!m_Handlers.Contains(eventType))
        {
            m_Handlers.Insert(eventType, new array<ref EventHandler>);
        }

        m_Handlers.Get(eventType).Insert(handler);
    }

    void Dispatch(EventBase event)
    {
        typename eventType = event.Type();

        array<ref EventHandler> handlers;
        if (m_Handlers.Find(eventType, handlers))
        {
            foreach (EventHandler handler : handlers)
            {
                handler.Handle(event);
            }
        }
    }
}
```

---

## よくある間違い

### 1. Forgetting to null-check after cast

```c
// WRONG — crashes if obj is not a PlayerBase
PlayerBase player = PlayerBase.Cast(obj);
player.GetIdentity();  // CRASH if cast failed!

// CORRECT
PlayerBase player = PlayerBase.Cast(obj);
if (player)
{
    player.GetIdentity();
}
```

### 2. Calling IsAlive() on base Object

```c
// WRONG — Object.IsAlive() does not exist
Object obj = GetSomeObject();
if (obj.IsAlive())  // Compile error or runtime crash!

// CORRECT
EntityAI eai;
if (Class.CastTo(eai, obj) && eai.IsAlive())
{
    // Safe
}
```

### 3. Using reflection with wrong variable name

```c
// SILENT FAILURE — no error, just returns zero/empty
int val;
EnScript.GetClassVar(obj, "NonExistentField", 0, val);
// val is 0, no error thrown
```

Always validate with `FindVarIndex` or `GetVariableCount`/`GetVariableName` first.

### 4. Confusing Type() with typename literal

```c
// Type() — returns the RUNTIME type of an instance
typename t = myObj.Type();  // e.g., PlayerBase

// typename literal — a compile-time type reference
typename t = PlayerBase;    // Always PlayerBase

// They are comparable
if (myObj.Type() == PlayerBase)  // true if myObj IS a PlayerBase
```

---

## まとめ

| 操作 | 構文 | 戻り値 |
|-----------|--------|---------|
| Safe downcast | `Class.CastTo(out target, source)` | `bool` |
| Inline cast | `TargetType.Cast(source)` | Target or `null` |
| Type check (typename) | `obj.IsInherited(typename)` | `bool` |
| Type check (string) | `obj.IsKindOf("ClassName")` | `bool` |
| Get runtime type | `obj.Type()` | `typename` |
| Variable count | `obj.Type().GetVariableCount()` | `int` |
| Variable name | `obj.Type().GetVariableName(i)` | `string` |
| Variable type | `obj.Type().GetVariableType(i)` | `typename` |
| Read property | `EnScript.GetClassVar(obj, name, 0, out val)` | `void` |
| Write property | `EnScript.SetClassVar(obj, name, 0, val)` | `bool` |

---

## ナビゲーション

| 前 | 上 | 次 |
|----------|----|------|
| [1.8 Memory Management](08-memory-management.md) | [Part 1: Enforce Script](../README.md) | [1.10 Enums & Preprocessor](10-enums-preprocessor.md) |
