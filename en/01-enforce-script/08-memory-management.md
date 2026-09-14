# Memory Management

> **Summary:** How Enforce Script's automatic reference counting works, when to use `ref` versus raw pointers, why reference cycles leak forever, and how the `Managed` base class makes weak references safe.

---

## Introduction

Enforce Script uses **automatic reference counting (ARC)** for memory management -- not garbage collection in the traditional sense. Understanding how `ref`, `autoptr`, and raw pointers work is essential for writing stable DayZ mods. Get it wrong and you will either leak memory (your server gradually consumes more RAM until it crashes) or access deleted objects (instant crash with no useful error message). This chapter explains every pointer type, when to use each, and how to avoid the most dangerous pitfall: reference cycles.

---

## The Three Pointer Types

Enforce Script has three ways to hold a reference to an object:

| Pointer Type | Keyword | Keeps Object Alive? | Zeroed on Delete? | Primary Use |
|-------------|---------|---------------------|-------------------|-------------|
| **Raw pointer** | *(none)* | No (weak reference) | Only if class extends `Managed` | Back-references, observers, caches |
| **Strong reference** | `ref` | Yes | Yes | Owned members, collections |
| **Auto pointer** | `autoptr` | Yes (strong reference) | Yes | Legacy keyword -- prefer `ref` |

### How ARC Works

Every object has a **reference count** -- the number of strong references (`ref`, `autoptr`, local variables, function arguments) pointing to it. When the count drops to zero, the object is automatically destroyed and its destructor is called.

**Weak references** (raw pointers) do NOT increase the reference count. They observe the object without keeping it alive.

Several examples in this chapter use this minimal class -- define it once and every snippet below is runnable as-is:

```c
class MyClass : Managed
{
    int m_Value;
}
```

---

## Raw Pointers (Weak References)

A raw pointer is any variable declared without `ref` or `autoptr`. For class members, this creates a **weak reference**: it points to the object but does NOT keep it alive.

```c
class Observer
{
    PlayerBase m_WatchedPlayer;  // Weak reference -- does NOT keep player alive

    void Watch(PlayerBase player)
    {
        m_WatchedPlayer = player;
    }

    void Report()
    {
        if (m_WatchedPlayer) // ALWAYS null-check weak references
        {
            Print("Watching: " + m_WatchedPlayer.GetIdentity().GetName());
        }
        else
        {
            Print("Player no longer exists");
        }
    }
}
```

### Managed vs Non-Managed classes

The safety of weak references depends on whether the object's class extends `Managed`:

- **Managed classes** (most DayZ gameplay classes): When the object is deleted, all weak references are automatically set to `null`. This is safe.
- **Non-Managed classes** (plain `class` without inheriting `Managed`): When the object is deleted, weak references become **dangling pointers** -- they still hold the old memory address. Accessing them causes a crash.

A note on sourcing: `Managed` itself is declared as an **empty marker class** in the vanilla script headers (`scripts/1_core/proto/enscript.c`) -- the auto-nulling of weak references is engine-side behavior described in Bohemia's Enforce Script documentation, not something you can read in the script sources. Treat it as a safety net, not as permission to skip null checks: **always null-check weak references before use**, whether or not the class is `Managed`.

```c
// SAFE -- Managed class, weak refs are zeroed
class SafeData : Managed
{
    int m_Value;
}

void TestManaged()
{
    SafeData data = new SafeData();
    SafeData weakRef = data;
    delete data;

    if (weakRef) // false -- weakRef was automatically set to null
    {
        Print(weakRef.m_Value); // Never reached
    }
}
```

```c
// DANGEROUS -- Non-Managed class, weak refs become dangling
class UnsafeData
{
    int m_Value;
}

void TestNonManaged()
{
    UnsafeData data = new UnsafeData();
    UnsafeData weakRef = data;
    delete data;

    if (weakRef) // TRUE -- weakRef still holds old address!
    {
        Print(weakRef.m_Value); // CRASH! Accessing deleted memory
    }
}
```

> **Rule:** If you are writing your own script-only classes, always extend `Managed` for safety. Game entities are already covered *by inheritance* -- you never write `: Managed` on them yourself (that is why [Variables and Types](01-variables-types.md#the-managed-base-class) lists entity classes under "do not manually extend `Managed`"), because they inherit it through the engine hierarchy: the vanilla scripts declare `IEntity: Managed` (`scripts/1_core/proto/enentity.c`), and the full chain is `EntityAI -> Entity -> ObjectTyped -> Object -> IEntity -> Managed` (each link is verifiable in `scripts/3_game/entities/`). So `EntityAI`, `ItemBase`, `PlayerBase`, and every other game entity **is** a `Managed` class, and raw pointers to them are auto-nulled when the entity is deleted -- but you still null-check every use.

---

## ref (Strong Reference)

The `ref` keyword marks a variable as a **strong reference**. The object stays alive as long as at least one strong reference exists. When the last strong reference is destroyed or overwritten, the object is deleted.

### Class members

Use `ref` for objects that your class **owns** and is responsible for creating and destroying.

```c
class LNT_Mission : Managed
{
    protected string m_Name;

    void LNT_Mission(string name)
    {
        m_Name = name;
    }
}

class LNT_MissionConfig : Managed
{
    string m_DisplayName;
    float m_Reward;
}

class LNT_MissionManager : Managed
{
    protected ref array<ref LNT_Mission> m_ActiveMissions;
    protected ref map<string, ref LNT_MissionConfig> m_Configs;

    void LNT_MissionManager()
    {
        m_ActiveMissions = new array<ref LNT_Mission>;
        m_Configs = new map<string, ref LNT_MissionConfig>;
    }

    // No destructor needed! When LNT_MissionManager is deleted:
    // 1. m_Configs ref is released -> map is deleted -> each LNT_MissionConfig is deleted
    // 2. m_ActiveMissions ref is released -> array is deleted -> each LNT_Mission is deleted
}
```

### Collections of owned objects

When you store objects in an array or map and want the collection to own them, use `ref` on both the collection AND the elements:

```c
class SafeZone : Managed
{
    protected vector m_Center;
    protected float m_Radius;

    void SafeZone(vector center, float radius)
    {
        m_Center = center;
        m_Radius = radius;
    }
}

class ZoneManager : Managed
{
    // The array is owned (ref), and each zone inside is owned (ref)
    protected ref array<ref SafeZone> m_Zones;

    void ZoneManager()
    {
        m_Zones = new array<ref SafeZone>;
    }

    void AddZone(vector center, float radius)
    {
        ref SafeZone zone = new SafeZone(center, radius);
        m_Zones.Insert(zone);
    }
}
```

**Critical distinction:** An `array<SafeZone>` holds **weak** references. An `array<ref SafeZone>` holds **strong** references. If you use the weak version, objects inserted into the array may be immediately deleted because no strong reference keeps them alive.

```c
// WRONG -- Objects are deleted immediately after insertion!
ref array<MyClass> weakArray = new array<MyClass>;
weakArray.Insert(new MyClass()); // Object created, inserted as weak ref,
                                  // no strong ref exists -> IMMEDIATELY deleted

// CORRECT -- Objects are kept alive by the array
ref array<ref MyClass> strongArray = new array<ref MyClass>;
strongArray.Insert(new MyClass()); // Object lives as long as it's in the array
```

---

## autoptr (Legacy Strong Reference)

Bohemia documents `autoptr` as destroying its target when the variable lifetime ends, giving function return or destruction of the containing class as examples. In the retained and council `1.29` probes, an `autoptr` declared inside nested braces remained alive through the statement after those braces and was destroyed as the function returned. That establishes this function's destruction order only; it does not establish universal equivalence with plain locals or safe use of a stale alias.

```c
void ProcessData()
{
    autoptr JsonSerializer serializer = new JsonSerializer();
    // Use serializer...

    // The documented variable-lifetime examples include function return.
}
```

The vanilla scripts use `autoptr` in only a handful of files -- for example, the private member maps in `scripts/3_game/analytics/scriptanalytics.c` -- and use `ref` everywhere else.

### `autoptr` and plain locals

The retained probe does not establish that `autoptr` and plain locals are universally equivalent. Prefer the ownership convention already used by your project, and use a narrow lifetime test before relying on a particular destruction point or alias state:

```c
void Example()
{
    MyClass a = new MyClass();         // Plain local
    autoptr MyClass b = new MyClass(); // Documented auto-destroy lifetime behavior

    // Do not infer matching block, alias, or destruction behavior from this snippet.
}
```

> **Convention in DayZ modding:** Most codebases use `ref` for class members and plain declarations for locals. Follow your project's convention consistently, but do not treat that convention as proof that `autoptr` has identical lifetime behavior in every context.

---

## notnull Parameter Modifier

The `notnull` modifier on a function parameter declares that null is never a valid argument. How it is enforced is not documented -- the keyword does not appear on Bohemia's Enforce Script syntax page -- so treat it as a contract the caller must honour rather than as a guarantee you can lean on inside the function.

```c
void ProcessPlayer(notnull PlayerBase player)
{
    // The caller is responsible for never passing null here
    string name = player.GetIdentity().GetName();
    Print("Processing: " + name);
}

void CallExample(PlayerBase maybeNull)
{
    if (maybeNull)
    {
        ProcessPlayer(maybeNull); // OK -- we checked first
    }

    // ProcessPlayer(null); // Never do this -- it violates the parameter's contract
}
```

Use `notnull` on parameters where null would always be a programming error: it documents the contract in the signature, and vanilla's own script relies on it (`array<T>.InsertAll` at `1_core/proto/enscript.c:449` dereferences its `notnull` parameter immediately). It is not a substitute for checking at the call site.

---

## Reference Cycles (MEMORY LEAK WARNING)

A reference cycle occurs when two objects hold strong references (`ref`) to each other. Neither object can ever be deleted because each one keeps the other alive. This is the most common source of memory leaks in DayZ mods.

### The problem

```c
class Parent
{
    ref Child m_Child; // Strong reference to Child
}

class Child
{
    ref Parent m_Parent; // Strong reference to Parent -- CYCLE!
}

void CreateCycle()
{
    ref Parent parent = new Parent();
    ref Child child = new Child();

    parent.m_Child = child;
    child.m_Parent = parent;

    // When this function exits:
    // - The local 'parent' ref is released, but child.m_Parent still holds parent alive
    // - The local 'child' ref is released, but parent.m_Child still holds child alive
    // NEITHER object is ever deleted! This is a permanent memory leak.
}
```

### The fix: One side must be a raw (weak) reference

Break the cycle by making one side a weak reference. The "child" should hold a weak reference to its "parent". Extend `Managed` so the child's raw back-pointer is nulled safely if the parent is ever deleted first:

```c
class Parent : Managed
{
    ref Child m_Child; // Strong -- parent OWNS the child
}

class Child : Managed
{
    Parent m_Parent; // Weak (raw) -- child OBSERVES the parent
}

void NoCycle()
{
    ref Parent parent = new Parent();
    ref Child child = new Child();

    parent.m_Child = child;
    child.m_Parent = parent;

    // When this function exits:
    // - Local 'parent' ref is released -> parent's ref count = 0 -> DELETED
    // - Parent destructor releases m_Child -> child's ref count = 0 -> DELETED
    // Both objects are properly cleaned up!
}
```

### Real-world example: UI panels

A common pattern in DayZ UI code is a panel that holds widgets, where widgets need a reference back to the panel. The panel owns the widgets (strong ref), and widgets observe the panel (weak ref).

```c
class AdminPanel : Managed
{
    protected ref array<ref AdminPanelTab> m_Tabs; // Owns the tabs

    void AdminPanel()
    {
        m_Tabs = new array<ref AdminPanelTab>;
    }

    void AddTab(string name)
    {
        ref AdminPanelTab tab = new AdminPanelTab(name, this);
        m_Tabs.Insert(tab);
    }
}

class AdminPanelTab : Managed
{
    protected string m_Name;
    protected AdminPanel m_Owner; // WEAK -- avoids cycle

    void AdminPanelTab(string name, AdminPanel owner)
    {
        m_Name = name;
        m_Owner = owner; // Weak reference back to parent
    }

    AdminPanel GetOwner()
    {
        return m_Owner; // May be null if panel was deleted
    }
}
```

### Reference Counting Lifecycle

```mermaid
sequenceDiagram
    participant Code as Your Code
    participant Obj as MyObject
    participant Eng as Engine (ARC)

    Code->>Obj: ref MyObject obj = new MyObject()
    Note over Obj: refcount = 1

    Code->>Obj: ref MyObject copy = obj
    Note over Obj: refcount = 2

    Code->>Obj: copy = null
    Note over Obj: refcount = 1

    Code->>Obj: obj = null
    Note over Obj: refcount = 0

    Obj->>Eng: ~MyObject() destructor called
    Eng->>Eng: Memory freed
```

### Reference Cycle (Memory Leak)

```mermaid
graph LR
    A[Object A<br/>ref m_B] -->|"strong ref"| B[Object B<br/>ref m_A]
    B -->|"strong ref"| A

    style A fill:#D94A4A,color:#fff
    style B fill:#D94A4A,color:#fff

    C["Neither can be freed!<br/>Both refcount = 1 forever"]

    style C fill:#FFD700,color:#000
```

---

## The delete Keyword

You can manually delete an object at any time using `delete`. This destroys the object **immediately**, regardless of its reference count. All references (both strong and weak, on Managed classes) are set to null.

```c
void ManualDelete()
{
    ref MyClass obj = new MyClass();
    ref MyClass anotherRef = obj;

    Print(obj != null);        // true
    Print(anotherRef != null); // true

    delete obj;

    Print(obj != null);        // false
    Print(anotherRef != null); // false (also nulled, on Managed classes)
}
```

### When to use delete

- When you need to release a resource **immediately** (not waiting for ARC)
- When cleaning up in a shutdown/destroy method
- When removing objects from the game world (`GetGame().ObjectDelete(obj)` for game entities)

### When NOT to use delete

- On objects owned by someone else (the owner's `ref` will become null unexpectedly)
- On objects still in use by other systems (timers, callbacks, UI)
- On engine-managed entities without going through proper channels

---

## Garbage Collection Behavior

Enforce Script does NOT have a traditional garbage collector that periodically scans for unreachable objects. Instead, it uses **deterministic reference counting:**

1. When a strong reference is created (assignment to `ref`, local variable, function argument), the object's reference count increases.
2. When a strong reference goes out of scope or is overwritten, the reference count decreases.
3. When the reference count reaches zero, the object is **immediately** destroyed (destructor is called, memory is freed).
4. `delete` bypasses the reference count and destroys the object immediately.

This means:
- Object lifetimes are predictable and deterministic
- There are no "GC pauses" or unpredictable delays
- Reference cycles are NEVER collected -- they are permanent leaks
- Order of destruction is well-defined: objects are destroyed in reverse order of their last reference being released

---

## Static State and Mission Lifecycle

Static state persisted across two calls in one callback in the `1.29` probe. Persistence and initializer behavior across reconnect, `#restart`, or a real mission reload have not yet been reproduced here. Reset mutable static state during mission teardown as defensive lifecycle design, but do not present cross-restart persistence as a tested fact.

```c
class MyLockCounter
{
    static int s_Count = 0;
    static void Acquire() { s_Count++; if (s_Count == 1) DoTheRealWork(); }
}
// The probe observed two calls in one callback: 1, then 2.
// Cross-restart behavior remains unverified.
```

As defensive lifecycle design, give any mod-level singleton, counter, cache, or registry with mutable `static` state an explicit `Cleanup()` called from mission teardown (`MissionGameplay.OnMissionFinish()` client-side, `MissionServer.OnMissionFinish()` server-side):

```c
static void Cleanup()
{
    s_Count = 0;      // reset scalars unconditionally
    s_Owners = null;
}
```

Reset state unconditionally as part of that defensive cleanup. The probe does not establish when a mission teardown occurs relative to every game lifecycle callback.

---

## `Object.IsDeleted()` Is Not Available in the Tested Mission Module

In the DayZ `1.29.0.163709` Mission module, `Object.IsDeleted()` is not an available instance call: the exact call compiled as `Undefined function 'Object.IsDeleted'`. This does not prove that no deletion-state facility exists anywhere in native code or on another type.

The extracted script declaration does show that `Object.IsAlive()` returns `!IsDamageDestroyed()`. Do not use `IsDamageDestroyed()` as a replacement deletion-state test; it answers damage state, not a generally established lifetime question:

```c
// This is a damage-state helper, not a tested deletion-state helper.
bool IsDamageDestroyed(EntityAI e) { return e.IsDamageDestroyed(); }
```

`IsDamageDestroyed()` is `true` for a **corpse** or a wrecked vehicle -- an object that still exists in the world. The probe does not establish that every raw reference becomes `null`, or that null is the only possible post-deletion signal; an entity deletion/alias runtime test is still needed.

```c
static void DespawnAndClean(EntityAI e)
{
    if (!e) return;             // no current reference to request deletion for
    GetGame().ObjectDelete(e);
}
```

Do not pair an invented `IsDeleted()`-style helper with `IsAlive()` as though they establish object lifetime. The `IsAlive()` script definition is damage-based, while post-deletion alias behavior remains unverified.

---

## Real-World Example: Proper Manager Class

Here is a complete example showing proper memory management patterns for a typical DayZ mod manager:

```c
class MyZoneManager : Managed
{
    // Singleton instance -- the only strong ref keeping this alive
    private static ref MyZoneManager s_Instance;

    // Owned collections -- manager is responsible for these
    protected ref array<ref MyZone> m_Zones;
    protected ref map<string, ref MyZoneConfig> m_Configs;

    // Weak reference to external system -- we don't own this
    protected PlayerBase m_LastEditor;

    void MyZoneManager()
    {
        m_Zones = new array<ref MyZone>;
        m_Configs = new map<string, ref MyZoneConfig>;
    }

    void ~MyZoneManager()
    {
        // Explicit cleanup (optional -- ARC handles it, but good practice)
        m_Zones.Clear();
        m_Configs.Clear();
        m_LastEditor = null;

        Print("[MyZoneManager] Destroyed");
    }

    static MyZoneManager GetInstance()
    {
        if (!s_Instance)
        {
            s_Instance = new MyZoneManager();
        }
        return s_Instance;
    }

    static void DestroyInstance()
    {
        s_Instance = null; // Releases the strong ref, triggers destructor
    }

    void CreateZone(string name, vector center, float radius, PlayerBase editor)
    {
        ref MyZoneConfig config = new MyZoneConfig(name, center, radius);
        m_Configs.Set(name, config);

        ref MyZone zone = new MyZone(config);
        m_Zones.Insert(zone);

        m_LastEditor = editor; // Weak reference -- we don't own the player
    }

    void RemoveZone(int index)
    {
        if (!m_Zones.IsValidIndex(index))
            return;

        MyZone zone = m_Zones.Get(index);
        string name = zone.GetName();

        m_Zones.RemoveOrdered(index); // Strong ref released, zone may be deleted
        m_Configs.Remove(name);       // Config ref released, config deleted
    }

    MyZone FindZoneAtPosition(vector pos)
    {
        foreach (MyZone zone : m_Zones)
        {
            if (zone.ContainsPosition(pos))
                return zone; // Return weak reference to caller
        }
        return null;
    }
}

class MyZone : Managed
{
    protected string m_Name;
    protected vector m_Center;
    protected float m_Radius;
    protected MyZoneConfig m_Config; // Weak -- config is owned by manager

    void MyZone(MyZoneConfig config)
    {
        m_Config = config; // Weak reference
        m_Name = config.GetName();
        m_Center = config.GetCenter();
        m_Radius = config.GetRadius();
    }

    string GetName() { return m_Name; }

    bool ContainsPosition(vector pos)
    {
        return vector.Distance(m_Center, pos) <= m_Radius;
    }
}

class MyZoneConfig : Managed
{
    protected string m_Name;
    protected vector m_Center;
    protected float m_Radius;

    void MyZoneConfig(string name, vector center, float radius)
    {
        m_Name = name;
        m_Center = center;
        m_Radius = radius;
    }

    string GetName() { return m_Name; }
    vector GetCenter() { return m_Center; }
    float GetRadius() { return m_Radius; }
}
```

### Memory ownership diagram for this example

```
MyZoneManager (singleton, owned by static s_Instance)
  |
  |-- ref array<ref MyZone>   m_Zones     [STRONG -> STRONG elements]
  |     |
  |     +-- MyZone
  |           |-- MyZoneConfig m_Config    [WEAK -- owned by m_Configs]
  |
  |-- ref map<string, ref MyZoneConfig> m_Configs  [STRONG -> STRONG elements]
  |     |
  |     +-- MyZoneConfig                   [OWNED here]
  |
  +-- PlayerBase m_LastEditor                [WEAK -- owned by engine]
```

When `DestroyInstance()` is called:
1. `s_Instance` is set to null, releasing the strong reference
2. `MyZoneManager` destructor runs
3. `m_Zones` is released -> array is deleted -> each `MyZone` is deleted
4. `m_Configs` is released -> map is deleted -> each `MyZoneConfig` is deleted
5. `m_LastEditor` is a weak reference, nothing to clean up
6. All memory is freed. No leaks.

---

## Best Practices

- Use `ref` for class members your class creates and owns; use raw pointers (no keyword) for back-references and external observations.
- Always extend `Managed` for pure-script classes -- it ensures weak references are zeroed on delete, preventing dangling pointer crashes.
- Break reference cycles by making the child hold a raw pointer to its parent: parent owns child (`ref`), child observes parent (raw).
- Use `array<ref MyClass>` when the collection owns its elements; `array<MyClass>` holds weak references that will not keep objects alive.
- Prefer ARC-driven cleanup over manual `delete` -- let the last `ref` release trigger the destructor naturally.

---

## Ownership Patterns in Practice

| Pattern | Where you see it | Detail |
|---------|------------------|--------|
| Parent `ref` + child raw back-pointer | UI code everywhere | A menu owns its tabs and handlers with `ref`; each tab holds a raw pointer back to its parent to avoid a cycle. Vanilla's `ScriptedWidgetEventHandler` is itself declared `: Managed` (`scripts/1_core/proto/enwidgets.c`), so raw back-pointers null out safely when the handler is deleted |
| `static ref` singleton + shutdown nulling | Framework manager classes | Setting `s_Instance = null` in a static shutdown method releases the last strong reference and triggers the whole destructor chain (see [Singletons](../07-patterns/01-singletons.md)) |
| `ref array<ref T>` for owned collections | Vanilla scripts throughout | Both the array and its elements are `ref` -- e.g. `private ref array<ref CallQueueContext> m_commands;` in `scripts/4_world/classes/contextmenu.c` |
| Raw pointers for engine entities (players, items) | Any script referencing world objects | Entity lifetime belongs to the engine: entities are spawned by the game world and destroyed via `GetGame().ObjectDelete()`. Scripts hold raw pointers, and because entities inherit `Managed` through `IEntity` (`scripts/1_core/proto/enentity.c`), those pointers are nulled when the entity despawns -- but you still null-check every use |

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| `autoptr` for local variables | Should auto-delete at scope exit | Documented variable-lifetime behavior and a probe showing destruction at function return do not establish universal equivalence with plain locals, block lifetime, or stale-alias safety |
| ARC handles all cleanup | Objects freed when refcount hits zero | Reference cycles are never collected -- they leak permanently until server restart |
| `delete` for immediate cleanup | Destroys the object right away | Can null out references held by other systems unexpectedly -- prefer letting ARC handle it |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Two objects with `ref` to each other | Reference cycle, permanent memory leak | One side must be a raw (weak) reference |
| `array<MyClass>` instead of `array<ref MyClass>` | Elements are weak references, objects may be deleted immediately | Use `array<ref MyClass>` for owned elements |
| Accessing a raw pointer after the object was deleted | Crash (dangling pointer on non-Managed classes) | Extend `Managed` and always null-check weak references |
| Not checking weak references for null | Crash when the referenced object has been deleted | Always: `if (weakRef) { weakRef.DoThing(); }` |
| Using `delete` on objects owned by another system | The owner's `ref` becomes null unexpectedly | Let the owner release the object through ARC |
| Storing `ref` to engine entities (players, items) | Can fight with engine lifetime management | Use raw pointers for engine entities |
| Forgetting `ref` on class member collections | Collection is a weak reference, may be collected | Always: `protected ref array<...> m_List;` |
| Circular parent-child with `ref` on both sides | Classic cycle; neither parent nor child is ever freed | Parent owns child (`ref`), child observes parent (raw) |

---

## Decision Guide: Which Pointer Type?

```
Is this a class member that this class CREATES and OWNS?
  -> YES: Use ref
  -> NO: Is this a back-reference or external observation?
    -> YES: Use raw pointer (no keyword), always null-check
    -> NO: Is this a local variable in a function?
      -> YES: Choose the ownership convention used by your project
      -> `autoptr` has documented variable-lifetime behavior; do not infer it is identical to a plain local in every context

Storing objects in a collection (array/map)?
  -> Objects OWNED by the collection: array<ref MyClass>
  -> Objects OBSERVED by the collection: array<MyClass>

Function parameter that must never be null?
  -> Use notnull modifier
```

---

## Quick Reference

```c
// Raw pointer (weak reference for class members)
MyClass m_Observer;              // Does NOT keep object alive
                                 // Set to null on delete (Managed only)

// Strong reference (keeps object alive)
ref MyClass m_Owned;             // Object lives until ref is released
ref array<ref MyClass> m_List;   // Array AND elements are strongly held

// Auto pointer (documented variable-lifetime behavior)
autoptr MyClass local;           // Do not infer plain-local or stale-alias behavior from this declaration

// notnull (contract: never pass null; enforcement undocumented)
void Func(notnull MyClass obj);  // Null-check at the call site

// Manual delete (immediate, bypasses ARC)
delete obj;                      // Destroys immediately, nulls all refs (Managed)

// Break reference cycles: one side must be weak
class Parent { ref Child m_Child; }      // Strong -- parent owns child
class Child  { Parent m_Parent; }        // Weak   -- child observes parent
```
