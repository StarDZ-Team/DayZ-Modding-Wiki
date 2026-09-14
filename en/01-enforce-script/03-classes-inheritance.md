# Classes & Inheritance

> **Summary:** How to declare classes, initialize them safely, inherit with `extends`, override methods with `override` and `super`, and use static members and singletons — including the constructor rules that are unique to Enforce Script.

---

## Table of Contents

- [Introduction](#introduction)
- [Declaring a Class](#declaring-a-class)
- [Constructors and Destructors](#constructors-and-destructors)
- [Access Modifiers](#access-modifiers)
- [Inheritance](#inheritance)
- [Overriding Methods](#overriding-methods)
- [Proto Methods (Engine Bindings)](#proto-methods-engine-bindings)
- [Parameter Modifiers](#parameter-modifiers)
- [Static Methods and Fields](#static-methods-and-fields)
- [Worked Example: Custom Item Class](#worked-example-custom-item-class)
- [The DayZ Class Hierarchy](#the-dayz-class-hierarchy)
- [Best Practices](#best-practices)
- [Observed in the Vanilla Scripts](#observed-in-the-vanilla-scripts)
- [Theory vs Practice](#theory-vs-practice)
- [Common Mistakes](#common-mistakes)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)

---

## Introduction

Everything in DayZ is a class. Every weapon, vehicle, zombie, UI panel, config manager, and player is an instance of a class. Understanding how to declare, extend, and work with classes in Enforce Script is the foundation of all DayZ modding.

Enforce Script's class system is single-inheritance, object-oriented, with access modifiers, constructors, destructors, static members, and method overriding. If you know C# or Java, the concepts are familiar --- but the syntax has its own flavor, and there are important differences covered in this chapter.

---

## Declaring a Class

A class groups related data (fields) and behavior (methods) together.

```c
class ZombieTracker
{
    // Fields (member variables)
    int m_ZombieCount;
    float m_SpawnRadius;
    string m_ZoneName;
    bool m_IsActive;
    vector m_CenterPos;

    // Methods (member functions)
    void Activate(vector center, float radius)
    {
        m_CenterPos = center;
        m_SpawnRadius = radius;
        m_IsActive = true;
    }

    bool IsActive()
    {
        return m_IsActive;
    }

    float GetDistanceToCenter(vector pos)
    {
        return vector.Distance(m_CenterPos, pos);
    }
}
```

### Class Naming Conventions

DayZ modding follows these conventions:
- Class names: `PascalCase` (e.g., `PlayerTracker`, `LootManager`)
- Member fields: `m_PascalCase` prefix (e.g., `m_Health`, `m_PlayerList`)
- Static fields: `s_PascalCase` prefix (e.g., `s_Instance`, `s_Counter`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_HEALTH`, `DEFAULT_RADIUS`)
- Methods: `PascalCase` (e.g., `GetPosition()`, `SetHealth()`)
- Local variables: `camelCase` (e.g., `playerCount`, `nearestDist`)

### Creating and Using Instances

```c
void Example()
{
    // Create an instance with 'new'
    ZombieTracker tracker = new ZombieTracker;

    // Call methods
    tracker.Activate(Vector(5000, 0, 8000), 200.0);

    if (tracker.IsActive())
    {
        float dist = tracker.GetDistanceToCenter(Vector(5050, 0, 8050));
        Print(string.Format("Distance: %1", dist));
    }

    // Destroy an instance with 'delete' (usually not needed; see Memory section)
    delete tracker;
}
```

---

## Constructors and Destructors

Constructors initialize an object when it is created. Destructors clean up when it is destroyed. In Enforce Script, both use the class name --- the destructor is prefixed with `~`.

### Constructor

```c
class SpawnZone
{
    protected string m_Name;
    protected vector m_Position;
    protected float m_Radius;
    protected ref array<string> m_AllowedTypes;

    // Constructor: same name as the class
    void SpawnZone(string name, vector pos, float radius)
    {
        m_Name = name;
        m_Position = pos;
        m_Radius = radius;
        m_AllowedTypes = new array<string>;

        Print(string.Format("[SpawnZone] Created: %1 at %2, radius %3", m_Name, m_Position, m_Radius));
    }

    // Destructor: ~ prefix
    void ~SpawnZone()
    {
        Print(string.Format("[SpawnZone] Destroyed: %1", m_Name));
        // m_AllowedTypes is a ref, it will be deleted automatically
    }

    void AddAllowedType(string typeName)
    {
        m_AllowedTypes.Insert(typeName);
    }
}
```

### Default Constructor (No Parameters)

If you do not define a constructor, the class gets an implicit default constructor that initializes all fields to their default values (`0`, `0.0`, `false`, `""`, `null`).

```c
class SimpleConfig
{
    int m_MaxPlayers;      // initialized to 0
    float m_SpawnDelay;    // initialized to 0.0
    string m_ServerName;   // initialized to ""
    bool m_PvPEnabled;     // initialized to false
}

void Test()
{
    SimpleConfig cfg = new SimpleConfig;
    // All fields are at their defaults
    Print(cfg.m_MaxPlayers);  // 0
}
```

A parameterized constructor like `SpawnZone`'s is fine on a class that nothing extends. The rules change as soon as inheritance is involved — see the next two subsections.

### Constructor Rules Unique to Enforce Script

Two rules trip up everyone coming from C# or Java:

1. **There is no `super(args)`.** You cannot call the parent's constructor explicitly — not as `super(...)`, and not by writing `ParentClassName(...)` as a statement inside the child's constructor body. The parent constructor always runs automatically, before the child's.
2. **Constructor signatures must stay compatible down the hierarchy.** If a base class declares a parameterized constructor and a subclass declares a constructor with a different parameter list, the module fails to compile with an error like:

```
SCRIPT (E): Overloaded function 'ChildClassName' not compatible
```

Do not rely on constructor overloading (multiple constructors with different parameter lists) either — the same "Overloaded function" compatibility check bites you. Declare **one** constructor per class and move parameterized setup into ordinary methods.

### The Init() Pattern

The reliable way to give a class hierarchy parameterized initialization:

1. Give the base class a **parameterless** constructor.
2. Put the parameterized setup in a normal method (`InitSomething(...)`).
3. Each subclass declares its own parameterless constructor and calls that method as its first statement. `protected` fields of the base are accessible to both.

```c
class PatrolAction
{
    protected int m_Id;
    protected string m_Name;
    protected float m_Cost;

    // Parameterless constructor: keeps every subclass compatible
    void PatrolAction()
    {
    }

    // Parameterized setup lives in a normal method instead
    void InitAction(int id, string name, float cost)
    {
        m_Id = id;
        m_Name = name;
        m_Cost = cost;
    }

    string GetName()
    {
        return m_Name;
    }
}

class PatrolAction_Idle extends PatrolAction
{
    void PatrolAction_Idle()
    {
        // First statement: parameterized init through the method
        InitAction(0, "Idle", 1.0);
    }
}

class PatrolAction_Search extends PatrolAction
{
    void PatrolAction_Search()
    {
        InitAction(1, "Search", 2.5);
    }
}
```

Vanilla DayZ uses exactly this shape: `PlayerBase`'s constructor is literally `void PlayerBase() { Init(); }`, and `Init()` does all the real setup (`4_world/entities/manbase/playerbase.c`).

---

## Access Modifiers

Access modifiers control who can see and use fields and methods.

| Modifier | Accessible From | Syntax |
|----------|----------------|--------|
| `private` | Only the declaring class | `private int m_Secret;` |
| `protected` | Declaring class + all subclasses | `protected int m_Health;` |
| *(none)* | Everywhere (public) | `int m_Value;` |

There is no explicit `public` keyword --- everything without `private` or `protected` is public by default.

```c
class BaseVehicle
{
    // Public: anyone can access
    string m_DisplayName;

    // Protected: this class and subclasses only
    protected float m_Fuel;
    protected float m_MaxFuel;

    // Private: only this exact class
    private int m_InternalState;

    void BaseVehicle()
    {
        m_InternalState = 0;
    }

    // Parameterized setup via the Init() pattern (see the Constructors section)
    void InitVehicle(string name, float maxFuel)
    {
        m_DisplayName = name;
        m_MaxFuel = maxFuel;
        m_Fuel = maxFuel;
    }

    // Public method
    float GetFuelPercent()
    {
        return (m_Fuel / m_MaxFuel) * 100.0;
    }

    // Protected method: subclasses can call this
    protected void ConsumeFuel(float amount)
    {
        m_Fuel = Math.Clamp(m_Fuel - amount, 0, m_MaxFuel);
    }

    // Private method: only this class
    private void UpdateInternalState()
    {
        m_InternalState++;
    }
}
```

### Best Practice: Encapsulation

Expose fields through methods (getters/setters) rather than making them public. This lets you add validation, logging, or side effects later without breaking code that uses the class.

```c
class VitalsTracker
{
    protected float m_Health;
    protected float m_MaxHealth;

    void VitalsTracker(float maxHealth)
    {
        m_MaxHealth = maxHealth;
        m_Health = maxHealth;
    }

    // Getter
    float GetHealth()
    {
        return m_Health;
    }

    // Setter with validation
    void SetHealth(float value)
    {
        m_Health = Math.Clamp(value, 0, m_MaxHealth);
    }

    // Convenience methods
    void TakeDamage(float amount)
    {
        SetHealth(m_Health - amount);
    }

    void Heal(float amount)
    {
        SetHealth(m_Health + amount);
    }

    bool IsAlive()
    {
        return m_Health > 0;
    }
}
```

---

## Inheritance

Inheritance lets you create a new class based on an existing one. The child class inherits all fields and methods from the parent, and can add new ones or override existing behavior.

### Syntax: `extends` or `:`

Enforce Script supports two syntaxes for inheritance. Both are equivalent:

```c
// Syntax 1: extends keyword (preferred, more readable)
class DeliveryVan extends BaseVehicle
{
}

// Syntax 2: colon (C++ style, also common in DayZ code)
class TowTruck : BaseVehicle
{
}
```

> **Naming tip:** avoid reusing vanilla class names (`Car`, `Animal`, `Shape`, `PlayerStats`, ...) for your own classes — a second declaration of an existing class fails to compile. Prefix or qualify your names.

### Basic Inheritance Example

```c
class PetBase
{
    protected string m_Name;
    protected float m_Health;

    // Parameterless constructor: subclasses stay compatible (see Constructor Rules above)
    void PetBase()
    {
        m_Health = 100.0;
    }

    void InitPet(string name, float health)
    {
        m_Name = name;
        m_Health = health;
    }

    string GetName()
    {
        return m_Name;
    }

    void Speak()
    {
        Print(m_Name + " makes a sound");
    }
}

class Dog extends PetBase
{
    protected string m_Breed;

    // The parent constructor runs automatically before this one.
    // Parameterized setup goes through Init methods, never through constructor arguments.
    void InitDog(string name, string breed)
    {
        InitPet(name, 100.0);
        m_Breed = breed;
    }

    string GetBreed()
    {
        return m_Breed;
    }

    // New method only in Dog
    void Fetch()
    {
        Print(m_Name + " fetches the stick!");
    }
}

void Test()
{
    Dog rex = new Dog();
    rex.InitDog("Rex", "German Shepherd");

    rex.Speak();         // Inherited from PetBase: "Rex makes a sound"
    rex.Fetch();         // Dog's own method: "Rex fetches the stick!"
    Print(rex.GetName()); // Inherited: "Rex"
    Print(rex.GetBreed()); // Dog's own: "German Shepherd"
}
```

### Single Inheritance Only

Enforce Script supports **single inheritance only**. A class can extend exactly one parent. There is no multiple inheritance, no interfaces, and no mixins.

```c
class A { }
class B extends A { }     // OK: single parent
// class C extends A, B { }  // ERROR: multiple inheritance not supported
class D extends B { }     // OK: B extends A, D extends B (inheritance chain)
```

### The `sealed` Keyword

A class marked `sealed` cannot be inherited from. A method marked `sealed` cannot be overridden. Bohemia's 1.28 release notes list `Enforce Script: 'sealed' keyword` under **MODDING → ADDED** ([Stable Update 1.28](https://forums.dayz.com/topic/266370-stable-update-128/) — *PC Stable 1.28 Update 1, Version 1.28.159992*, posted 2 June 2025 by merropa93 (DayZ Community Support); accessed 2026-09-11). Vanilla ships sealed classes — `Contact` and `PhysicsWorld` in `1_core/physics/` (`contact.c:9`, `physicsworld.c:9`).

```c
sealed class FinalClass
{
    void DoWork()
    {
        // This class cannot be extended
    }
}

class ChildAttempt : FinalClass  // COMPILE ERROR: cannot inherit from sealed class
{
}
```

Methods can also be sealed individually:

```c
class PartiallySealedBase
{
    sealed void LockedMethod()
    {
        // Cannot be overridden in child classes
    }

    void OpenMethod()
    {
        // Can be overridden normally
    }
}
```

> **Migration note:** If you update to DayZ 1.28 or later and get a compile error about inheriting a sealed class, you must refactor. Use composition (wrap the class as a member) instead of inheritance.

`sealed` is rarely used in DayZ modding since extensibility is the primary goal.

---

## Overriding Methods

When a subclass needs to change the behavior of an inherited method, it uses the `override` keyword. The compiler checks that the method signature matches a method in the parent class.

```c
class WeaponProfile
{
    protected string m_Name;
    protected float m_Damage;

    void WeaponProfile()
    {
    }

    void InitProfile(string name, float damage)
    {
        m_Name = name;
        m_Damage = damage;
    }

    float CalculateDamage(float distance)
    {
        // Base damage, no falloff
        return m_Damage;
    }

    string GetInfo()
    {
        return string.Format("%1 (Dmg: %2)", m_Name, m_Damage);
    }
}

class RifleProfile extends WeaponProfile
{
    protected float m_MaxRange;

    void InitRifleProfile(string name, float damage, float maxRange)
    {
        InitProfile(name, damage);
        m_MaxRange = maxRange;
    }

    // Override: change damage calculation to include distance falloff
    override float CalculateDamage(float distance)
    {
        float falloff = Math.Clamp(1.0 - (distance / m_MaxRange), 0.1, 1.0);
        return m_Damage * falloff;
    }

    // Override: add range info
    override string GetInfo()
    {
        return string.Format("%1 (Dmg: %2, Range: %3m)", m_Name, m_Damage, m_MaxRange);
    }
}
```

### The `super` Keyword

`super` refers to the parent class. Use it to call the parent's version of a method, then add your own logic on top. This is critical --- especially in [modded classes](04-modded-classes.md).

```c
class BaseLogger
{
    void Log(string message)
    {
        Print("[LOG] " + message);
    }
}

class TimestampLogger extends BaseLogger
{
    override void Log(string message)
    {
        // Call parent's Log first
        super.Log(message);

        // Then add timestamp logging
        int hour, minute, second;
        GetHourMinuteSecond(hour, minute, second);
        Print(string.Format("[%1:%2:%3] %4", hour, minute, second, message));
    }
}
```

### `this` Keyword

`this` refers to the current object instance. It is usually implicit (you do not need to write it), but can be useful for clarity or when passing the current object to another function.

```c
class HandlerRegistry
{
    void Register(Managed handler) { /* ... */ }
}

class KillFeedHandler : Managed
{
    void Init(HandlerRegistry registry)
    {
        // Pass 'this' (the current KillFeedHandler instance) to the registry
        registry.Register(this);
    }
}
```

---

## Proto Methods (Engine Bindings)

Enforce Script uses `proto` to declare methods that are implemented in the C++ engine:

```c
// proto native — direct C++ binding, most common
proto native void SetPosition(vector pos);
proto native vector GetPosition();
proto native float GetHealth(string zoneName, string healthType);

// proto native owned — caller owns the returned object
proto native owned external string ClassName();

// proto volatile — function may yield/sleep (used by engine internals)
proto volatile int Call(Class inst, string func, void param);

// proto native external — binding detail for cross-module calls
proto native external void DoSomething();
```

You cannot implement `proto` methods --- they are engine-provided. You can only **call** them.

---

## Parameter Modifiers

In addition to access modifiers on fields and methods, Enforce Script has parameter-level modifiers that control how arguments are passed to functions:

```c
// out — parameter is output only (written by the function)
bool TryGetValue(out int result)
{
    result = 42;
    return true;
}

// inout — parameter is both input and output
void ModifyArray(inout array<int> arr)
{
    arr.Insert(99);  // modifies the caller's array
}

// notnull — declares that null is never a valid argument here
void Process(notnull EntityAI entity)
{
    // The caller is responsible for not passing null (see 1.13)
}
```

| Modifier | Meaning |
|----------|---------|
| `out` | Callee writes the value; caller reads it after the call |
| `inout` | Caller passes a value in; callee may modify it |
| `notnull` | Declares the argument is never `null`; enforcement is undocumented (see [1.13](13-functions-methods.md#notnull-parameters)) |

These modifiers appear frequently in vanilla DayZ methods and engine API signatures.

---

## Static Methods and Fields

Static members belong to the class itself, not to any instance. They are accessed using the class name, not an object variable.

### Static Fields

```c
class GameConfig
{
    // Static fields: shared across all instances (and accessible without an instance)
    static int s_MaxPlayers = 60;
    static float s_TickRate = 30.0;
    static string s_ServerName = "My Server";

    // Regular (instance) field
    protected bool m_IsLoaded;
}

void UseStaticFields()
{
    // Access without creating an instance
    Print(GameConfig.s_MaxPlayers);     // 60
    Print(GameConfig.s_ServerName);     // "My Server"

    // Modify
    GameConfig.s_MaxPlayers = 40;
}
```

### Static Methods

```c
class MathUtils
{
    static float MetersToKilometers(float meters)
    {
        return meters / 1000.0;
    }

    static string FormatDistance(float meters)
    {
        if (meters >= 1000)
            return string.Format("%1 km", (meters / 1000.0));
        else
            return string.Format("%1 m", Math.Round(meters));
    }

    static bool IsInCircle(vector point, vector center, float radius)
    {
        return vector.Distance(point, center) <= radius;
    }
}

void Test()
{
    float km = MathUtils.MetersToKilometers(2500);     // 2.5
    string display = MathUtils.FormatDistance(750);      // "750 m"
    bool inside = MathUtils.IsInCircle("100 0 200", "150 0 250", 100);
}
```

### The Singleton Pattern

The most common use of static fields in DayZ mods is the singleton pattern: a class that has exactly one instance, accessible globally.

```c
class LNT_ZoneManager
{
    // Static reference to the single instance
    private static ref LNT_ZoneManager s_Instance;

    protected bool m_Initialized;
    protected ref array<string> m_Zones;

    void LNT_ZoneManager()
    {
        m_Initialized = false;
        m_Zones = new array<string>;
    }

    // Static getter for the singleton
    static LNT_ZoneManager GetInstance()
    {
        if (!s_Instance)
            s_Instance = new LNT_ZoneManager;

        return s_Instance;
    }

    void Init()
    {
        if (m_Initialized)
            return;

        m_Initialized = true;
        Print("[Lantern] Zone manager initialized");
    }

    // Static cleanup
    static void Destroy()
    {
        s_Instance = null;
    }
}

// Usage from anywhere:
void SomeFunction()
{
    LNT_ZoneManager.GetInstance().Init();
}
```

Vanilla uses the same idea for its plugin system: a global `ref PluginManager g_Plugins;` created lazily by `GetPluginManager()`, with `GetPlugin(typename)` as the convenience accessor (`4_world/plugins/pluginmanager.c`). The `LNT_` prefix belongs to the wiki's fictional Lantern teaching mod — the full singleton discussion, including teardown and listen-server pitfalls, lives in [Singletons](../07-patterns/01-singletons.md).

---

## Worked Example: Custom Item Class

Here is a complete example showing a custom item class hierarchy in the style of DayZ modding. This demonstrates everything covered in this chapter.

```c
// Base class for all custom medical items
class CustomMedicalBase extends ItemBase
{
    protected float m_HealAmount;
    protected float m_UseTime;      // seconds to use
    protected bool m_RequiresBandage;

    void CustomMedicalBase()
    {
        m_HealAmount = 0;
        m_UseTime = 3.0;
        m_RequiresBandage = false;
    }

    float GetHealAmount()
    {
        return m_HealAmount;
    }

    float GetUseTime()
    {
        return m_UseTime;
    }

    bool RequiresBandage()
    {
        return m_RequiresBandage;
    }

    // Can be overridden by subclasses
    void OnApplied(PlayerBase player)
    {
        if (!player)
            return;

        player.AddHealth("", "Health", m_HealAmount);
        Print(string.Format("[Medical] %1 applied, healed %2", GetType(), m_HealAmount));
    }
}

// Specific medical item: Bandage
class CustomBandage extends CustomMedicalBase
{
    void CustomBandage()
    {
        m_HealAmount = 25.0;
        m_UseTime = 2.0;
    }

    override void OnApplied(PlayerBase player)
    {
        super.OnApplied(player);

        // Additional bandage-specific effect: stop bleeding
        // (simplified example)
        Print("[Medical] Bleeding stopped");
    }
}

// Specific medical item: First Aid Kit (heals more, takes longer)
class CustomFirstAidKit extends CustomMedicalBase
{
    private int m_UsesRemaining;

    void CustomFirstAidKit()
    {
        m_HealAmount = 75.0;
        m_UseTime = 8.0;
        m_UsesRemaining = 3;
    }

    int GetUsesRemaining()
    {
        return m_UsesRemaining;
    }

    override void OnApplied(PlayerBase player)
    {
        if (m_UsesRemaining <= 0)
        {
            Print("[Medical] First Aid Kit is empty!");
            return;
        }

        super.OnApplied(player);
        m_UsesRemaining--;

        Print(string.Format("[Medical] Uses remaining: %1", m_UsesRemaining));
    }
}
```

### Where the config.cpp Side Lives

A script class that extends `ItemBase` only becomes a spawnable item when a matching class hierarchy is declared in `config.cpp` — with `scope = 0` on the abstract base and `scope = 2` on spawnable items. That side of the story is covered in [config.cpp Deep Dive](../02-mod-structure/02-config-cpp.md), and the [Custom Item tutorial](../08-tutorials/02-custom-item.md) walks through it end to end.

---

## The DayZ Class Hierarchy

Everything you script against in DayZ hangs off one inheritance chain: `Class` → `Managed` / `IEntity` → `Object` → `EntityAI` → `ItemBase`, `Man` → `PlayerBase`, and so on. The full annotated hierarchy — including which base class to extend for items, weapons, clothing, vehicles, and UI — lives in [Entity System](../06-engine-api/01-entity-system.md).

---

## Best Practices

- Always call `super.MethodName()` in overrides unless you intentionally want to replace the parent behavior entirely -- DayZ's deep inheritance chains depend on it.
- Use `protected` for member fields and expose them via getter/setter methods -- this lets you add validation or logging later without breaking callers.
- Prefer composition over deep inheritance when combining unrelated behaviors (e.g., a flight controller inside a vehicle, not a FlyingCar multi-inherit attempt).
- Mark owned object members with `ref` at declaration -- without it, the object may be garbage collected while your class still expects it.
- Use the singleton pattern (`static ref` + `GetInstance()`) for manager classes that must have exactly one instance.

---

## Observed in the Vanilla Scripts

Every pattern in this chapter appears in the vanilla game code — worth reading in your extracted scripts:

| Pattern | Vanilla example | Detail |
|---------|-----------------|--------|
| Global singleton with a lazy accessor | `PluginManager` | A global `ref PluginManager g_Plugins;` plus `GetPluginManager()` that creates it on first use, and `GetPlugin(typename)` as the lookup helper (`4_world/plugins/pluginmanager.c`) |
| Parameterless constructor + `Init()` | `PlayerBase` | The constructor is literally `void PlayerBase() { Init(); }`, and `Init()` creates every `ref` collection (`m_Recipes = new array<int>;`) (`4_world/entities/manbase/playerbase.c`) |
| `override` + `super` on every lifecycle method | `MissionServer` | `OnInit()` and `OnMissionStart()` call `super` first, then add server-side behavior (`5_mission/mission/missionserver.c`) |
| Abstract base with `scope=0` in config.cpp | Vanilla item configs | Config classes that exist only to be inherited from are declared `scope=0` (cannot spawn); concrete, spawnable items get `scope=2` |

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| Omitting `override` keyword | Might create a distinct child method | On DayZDiag `1.29.0.163709`, the compiler emits `Overriding function '<name>' but not marked as 'override'` and prevents the Mission module from compiling |
| Multiple constructors (overloading) | Standard OOP feature | Do not rely on it -- mismatched constructor signatures across a hierarchy fail with `Overloaded function '<Class>' not compatible`; use one parameterless constructor plus an `Init()` method |
| `sealed` classes/methods | Prevents inheritance or override (compile-time error); keyword listed under MODDING → ADDED in the 1.28 release notes | Almost never used in DayZ modding because extensibility is the whole point |

---

## Common Mistakes

### 1. Forgetting `ref` for Owned Objects

When a class owns another object (creates it, responsible for its lifetime), declare the field as `ref`. Without `ref`, the object may be garbage collected unexpectedly.

```c
// BAD: m_Data might be garbage collected
class BadManager
{
    array<string> m_Data;  // raw pointer, no ownership

    void BadManager()
    {
        m_Data = new array<string>;  // object might get collected
    }
}

// GOOD: ref ensures the manager keeps m_Data alive
class GoodManager
{
    ref array<string> m_Data;  // strong reference, owns the object

    void GoodManager()
    {
        m_Data = new array<string>;
    }
}
```

### 2. Forgetting `override` Keyword

On DayZDiag `1.29.0.163709`, a child method with the same signature as a parent method must be marked `override`. Omitting the keyword emits `Overriding function '<name>' but not marked as 'override'` and prevents the Mission module from compiling.

```c
class Parent
{
    void DoWork() { Print("Parent"); }
}

class Child extends Parent
{
    // BAD: uncommenting this produces the omitted-override compiler error.
    // void DoWork() { Print("Child"); }

    // GOOD: properly overrides
    override void DoWork() { Print("Child"); }
}
```

### 3. Not Calling `super` in Overrides

When you override a method, the parent's code is NOT automatically called. If you skip `super`, you lose the parent's behavior --- which can break functionality, especially in DayZ's deep inheritance chains.

```c
class Parent
{
    void Init()
    {
        // Critical initialization happens here
        Print("Parent.Init()");
    }
}

class Child extends Parent
{
    // BAD: Parent.Init() never runs
    override void Init()
    {
        Print("Child.Init()");
    }

    // GOOD: Parent.Init() runs first, then child adds behavior
    override void Init()
    {
        super.Init();
        Print("Child.Init()");
    }
}
```

### 4. Ref Cycles Cause Memory Leaks

If object A holds a `ref` to object B, and object B holds a `ref` back to object A, neither can ever be freed — one side must hold a plain (non-`ref`) reference. This mistake, and the full rules for `ref`, ownership, and breaking cycles, are covered in [Memory Management](08-memory-management.md).

### 5. Trying to Call the Base Constructor

There is no `super(args)` in Enforce Script, and writing the base class name as a statement inside the child constructor does not call the base constructor — it fails to compile.

```c
class TaskBase
{
    protected int m_Priority;

    void TaskBase()
    {
    }

    void InitTask(int priority)
    {
        m_Priority = priority;
    }
}

// BAD: there is no explicit base-constructor call
class PatrolTask extends TaskBase
{
    void PatrolTask()
    {
        // TaskBase(5);  // COMPILE ERROR: Overloaded function not compatible
    }
}

// GOOD: the base constructor runs automatically; call an Init method for parameters
class GuardTask extends TaskBase
{
    void GuardTask()
    {
        InitTask(5);
    }
}
```

### 6. Trying to Use Multiple Inheritance

Enforce Script does not support multiple inheritance. If you need to share behavior across unrelated classes, use composition (hold a reference to a helper object) or static utility methods.

```c
// CANNOT DO THIS:
// class FlyingCar extends Car, Aircraft { }  // ERROR

// Instead, use composition:
class FlightController
{
    void NavigateTo(vector destination)
    {
        // flight logic here
    }
}

class FlyingCar extends BaseVehicle
{
    protected ref FlightController m_Flight;

    void FlyingCar()
    {
        m_Flight = new FlightController;
    }

    void Fly(vector destination)
    {
        m_Flight.NavigateTo(destination);
    }
}
```

### 7. A `static` Method With the Same Name as an Inherited One

Enforce Script does not overload on `static` -- a method name is the whole key within a class hierarchy, so adding a `static` method whose name matches one already declared *anywhere up the inheritance chain* is a duplicate declaration, not a new overload. Worse, this failure is not confined to your file: **it fails the entire script module you added it to** -- one bad name in one class can take down every mod's `5_Mission` files (or `4_World`, or `3_Game`), not just your own.

```c
// Looks completely self-contained:
class MyMenu extends UIScriptedMenu
{
    // A static convenience API so other code can close the menu without an instance
    static void Close()          // ERROR: Multiple declaration of function 'Close'
    {
        GetGame().GetUIManager().CloseMenu(MENU_MY_MENU);
    }
}
```

The error message names only *your* line -- `UIScriptedMenu`'s parent class `UIMenuPanel` already declares `proto native void Close();`, but the compiler never tells you that; it just reports a "multiple declaration" against a class you wrote yourself, with no mention of the base class you never opened. The names most likely to collide are exactly the generic ones you would naturally pick for a menu helper: `Close`, `Init`, `Refresh`, `Cleanup`, `Update`, `OnShow`, `OnHide`.

**Fix:** rename the static to something that cannot collide, and use the inherited instance method for its intended purpose:

```c
class MyMenu extends UIScriptedMenu
{
    //! For code that has no menu instance to call Close() on.
    static void CloseIfOpen()
    {
        UIManager uiMgr = GetGame().GetUIManager();
        if (uiMgr && uiMgr.IsMenuOpen(MENU_MY_MENU))
            uiMgr.CloseMenu(MENU_MY_MENU);   // by ID -- see the note below
    }

    void OnSomeEvent()
    {
        Close();   // the inherited instance method -- correct here
    }
}
```

Before adding any method to a class that `extends` an engine type, it is worth checking the base class you are extending for a method of the same name -- inheritance reserves every name in the whole chain, silently, whether you read that chain or not.

> **Related pitfall:** if your static helper used to close the menu with `UIManager.Back()` instead of `CloseMenu(id)`, be aware `Back()` closes whatever menu is currently on **top** of the stack -- not necessarily yours. If anything else opened above your menu, a caller asking to close *your* screen silently closes someone else's instead. `CloseMenu(id)` walks the parent chain and closes the menu you actually asked for.

---

## Practice Exercises

### Exercise 1: Shape Hierarchy
Create a base class `ShapeBase` with a method `float GetArea()` (do not name it `Shape` — that class already exists in vanilla). Create subclasses `Circle` (radius), `Rectangle` (width, height), and `Triangle` (base, height) that override `GetArea()`. Give `ShapeBase` a parameterless constructor and set dimensions through Init methods. Print the area of each.

### Exercise 2: Logger System
Create a `Logger` class with a `Log(string message)` method that prints to console. Create `FileLogger` that extends it and also writes to a conceptual file (just print with a `[FILE]` prefix). Create `DiscordLogger` that extends `Logger` and adds a `[DISCORD]` prefix. Each should call `super.Log()`.

### Exercise 3: Inventory Item
Create a class `CustomItem` with protected fields for `m_Weight`, `m_Value`, and `m_Condition` (float 0-1). Include:
- A parameterless constructor plus an `InitItem(...)` method that sets all three values (remember: subclasses cannot declare constructors with different signatures)
- Getters for each field
- A method `Degrade(float amount)` that reduces condition (clamped to 0)
- A method `GetEffectiveValue()` that returns `m_Value * m_Condition`

Then create `CustomWeaponItem` that extends it, adding `m_Damage` and an override of `GetEffectiveValue()` that factors in damage.

### Exercise 4: Singleton Manager
Implement a `SessionManager` singleton that tracks player join/leave events. It should store join times in a map and provide methods:
- `OnPlayerJoin(string uid, string name)`
- `OnPlayerLeave(string uid)`
- `int GetOnlineCount()`
- `float GetSessionDuration(string uid)` (in seconds)

### Exercise 5: Chain of Command
Create an abstract `Handler` class with `protected Handler m_Next` and methods `SetNext(Handler next)` and `void Handle(string request)`. Create three concrete handlers (`AuthHandler`, `PermissionHandler`, `ActionHandler`) that either handle the request or pass it to `m_Next`. Demonstrate the chain.

---

## Summary

| Concept | Syntax | Notes |
|---------|--------|-------|
| Class declaration | `class Name { }` | Public members by default |
| Inheritance | `class Child extends Parent` | Single inheritance only; also `: Parent` |
| Constructor | `void ClassName()` | Same name as class; one per class |
| Base constructor call | *(not available)* | No `super(args)`; parent ctor runs automatically -- use a parameterless base ctor + `Init()` method |
| Destructor | `void ~ClassName()` | Called on deletion |
| Private | `private int m_Field;` | This class only |
| Protected | `protected int m_Field;` | This class + subclasses |
| Public | `int m_Field;` | No keyword needed (default) |
| Override | `override void Method()` | Must match parent signature |
| Super call | `super.Method()` | Calls parent's version |
| Static field | `static int s_Count;` | Shared across all instances |
| Static method | `static void DoThing()` | Called via `ClassName.DoThing()` |
| `ref` | `ref MyClass m_Obj;` | Strong reference (owns the object) |
| Sealed class | `sealed class Name { }` | Cannot be inherited (compile error); keyword added in 1.28 |
| Sealed method | `sealed void Method()` | Cannot be overridden in child classes |
| Proto native | `proto native void Func();` | Engine-implemented method |
| `out` param | `void Func(out int val)` | Output-only parameter |
| `inout` param | `void Func(inout array<int> a)` | Input + output parameter |
| `notnull` param | `void Func(notnull EntityAI e)` | Contract: never pass null; check at the call site |
