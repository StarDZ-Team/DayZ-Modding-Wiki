# Variables & Types

> **Summary:** The Enforce Script primitive types (`int`, `float`, `bool`, `string`, `vector`, `typename`), how to declare variables and constants, how type conversion works, and the scoping rules that differ from C-family languages. An `auto` keyword exists for local type inference, but the vanilla scripts almost never use it --- write the explicit type unless you have a specific reason not to.

---

## Table of Contents

- [Primitive Types](#primitive-types)
- [Declaring Variables](#declaring-variables)
- [Working with `int`](#working-with-int)
- [Working with `float`](#working-with-float)
- [Working with `bool`](#working-with-bool)
- [Strings at a Glance](#strings-at-a-glance)
- [Vectors at a Glance](#vectors-at-a-glance)
- [Working with `typename`](#working-with-typename)
- [The `Managed` Base Class](#the-managed-base-class)
- [Type Conversion](#type-conversion)
- [Variable Scope](#variable-scope)
- [Operator Precedence](#operator-precedence)
- [Common Mistakes](#common-mistakes)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)

---

## Primitive Types

Enforce Script has a small, fixed set of primitive types. You cannot define new value types --- only classes (covered in [Classes & Inheritance](03-classes-inheritance.md)).

| Type | Size | Default Value | Description |
|------|------|---------------|-------------|
| `int` | 32-bit signed | `0` | Whole numbers from -2,147,483,648 to 2,147,483,647 |
| `float` | 32-bit IEEE 754 | `0.0` | Floating-point numbers |
| `bool` | 1 bit logical | `false` | `true` or `false` |
| `string` | Variable | `""` (empty) | Text. Value type --- copied on assignment, not shared by reference |
| `vector` | 3x float | `"0 0 0"` | Three-component float (x, y, z). Passed by value |
| `typename` | Engine ref | `null` | A reference to a type itself, used for reflection |
| `void` | N/A | N/A | Used only as a return type to indicate "returns nothing" |

### Type Hierarchy Diagram

```mermaid
graph TD
    subgraph "Value Types (passed by copy)"
        INT[int<br/>32-bit signed]
        FLOAT[float<br/>32-bit IEEE 754]
        BOOL[bool<br/>true / false]
        STRING[string<br/>text, copied on assignment]
        VECTOR[vector<br/>3x float xyz]
    end

    subgraph "Reference Types (passed by reference)"
        CLASS[Class<br/>root of all ref types]
        MANAGED[Managed<br/>weak refs zeroed on delete]
        TYPENAME[typename<br/>type reflection]
    end

    CLASS --> MANAGED
    CLASS --> ENTITYAI[EntityAI]
    ENTITYAI --> ITEMBASE[ItemBase]
    ENTITYAI --> MANBASE[ManBase / PlayerBase]
    MANAGED --> SCRIPTHANDLER[ScriptedWidgetEventHandler]
    MANAGED --> CUSTOMCLASS[Your Custom Classes]

    style INT fill:#4A90D9,color:#fff
    style FLOAT fill:#4A90D9,color:#fff
    style BOOL fill:#4A90D9,color:#fff
    style STRING fill:#4A90D9,color:#fff
    style VECTOR fill:#4A90D9,color:#fff
    style CLASS fill:#D94A4A,color:#fff
    style MANAGED fill:#D97A4A,color:#fff
```

### Type Constants

Several types expose useful constants (defined in the engine's `enconvert.c`):

```c
// int bounds
int maxInt = int.MAX;    // 2147483647
int minInt = int.MIN;    // -2147483648

// float bounds
float smallest = float.MIN;     // smallest positive float (~1.175e-38)
float largest  = float.MAX;     // largest float (~3.403e+38)
float lowest   = float.LOWEST;  // most negative float (-3.403e+38)
```

---

## Declaring Variables

Variables are declared by writing the type followed by the name. You can declare and assign in one statement or separately.

```c
void MyFunction()
{
    // Declaration only (initialized to default value)
    int health;          // health == 0
    float speed;         // speed == 0.0
    bool isAlive;        // isAlive == false
    string name;         // name == ""

    // Declaration with initialization
    int maxPlayers = 60;
    float gravity = 9.81;
    bool debugMode = true;
    string serverName = "My DayZ Server";
}
```

### The `auto` Keyword Exists, But Explicit Types Are the Vanilla Idiom

Older community write-ups claim DayZ's Enforce Script has no `auto` keyword and that it fails with `Unknown type 'auto'`. That claim is outdated: the vanilla scripts use `auto` for local type inference in 32 compiling declarations, including with generic template types --- for example `auto p = new Param10<string,int, float, float, int, int, float, float, bool, bool>(...)` (`4_world/plugins/pluginbase/plugindeveloper.c`), `auto param = new Param2<bool, EntityAI>(enabled, g_Game.GetPlayer())` (`4_world/plugins/pluginbase/plugindiagmenu/plugindiagmenuclient.c`), and `auto vehicle = CarScript.Cast(vehCommand.GetTransport())` (`4_world/classes/useractionscomponent/actions/continuous/vehicles/actionstartengine.c`) --- and all of these compile as part of the shipped game.

Bohemia documents the keyword under *Automatic type detection*: "the variable type will be detected automatically at compile time when the keyword `auto` is used as placeholder", with primitives among the worked examples --- `auto variable1 = 1;` gives an `int`, `auto variablePi = 3.14;` gives a `float`, `auto variableInst = new MyCustomClass();` gives the class type.

```c
void Example()
{
    auto count = 10;                        // Inferred as int (per Bohemia's own example)
    int count2 = 10;                        // Equivalent, explicit form

    auto p = new Param2<string, int>("kills", 5);   // Inferred as Param2<string, int>
}
```

Because the type is detected *from the initializer*, a bare `auto x;` has nothing to infer from. Note also that `auto` is a keyword, so it cannot double as an identifier --- no vanilla declaration uses `auto` as a variable or member name.

Two caveats worth keeping in mind. First, every one of the 32 compiling vanilla uses infers a **reference** type --- from a `new X(...)` or from a `.Cast()`; the primitive form above is documented by Bohemia but has no vanilla precedent. Second, vanilla reaches for `auto` in only two shapes: boxing values into `ParamN<...>` types before an RPC or event call, and short-lived `.Cast()` results.

Outside those, thousands of vanilla declarations spell out the explicit type. Treat this chapter's explicit-type style as the idiomatic default --- not because `auto` is broken, but because a visible type is easier to read at the declaration site, especially for collections.

### Constants

Use the `const` keyword for values that should never change after initialization:

```c
const int MAX_SQUAD_SIZE = 8;
const float SPAWN_RADIUS = 150.0;
const string MOD_PREFIX = "[MyMod]";

void Example()
{
    int a = MAX_SQUAD_SIZE;  // OK: reading a constant
    MAX_SQUAD_SIZE = 10;     // ERROR: cannot assign to a constant
}
```

Constants are typically declared at file scope (outside any function) or as class members. Naming convention: `UPPER_SNAKE_CASE`.

---

## Working with `int`

Integers are the workhorse type. DayZ uses them for item counts, player IDs, health values (when discretized), enum values, bitflags, and more.

```c
void IntExamples()
{
    int count = 5;
    int total = count + 10;     // 15
    int doubled = count * 2;    // 10
    int remainder = 17 % 5;     // 2 (modulo)

    // Increment and decrement
    count++;    // count is now 6
    count--;    // count is now 5 again

    // Compound assignment
    count += 3;  // count is now 8
    count -= 2;  // count is now 6
    count *= 4;  // count is now 24
    count /= 6;  // count is now 4

    // Integer division truncates (no rounding)
    int result = 7 / 2;    // result == 3, not 3.5

    // Bitwise operations (used for flags)
    int flags = 0;
    flags = flags | 0x01;   // set bit 0
    flags = flags | 0x04;   // set bit 2
    bool hasBit0 = (flags & 0x01) != 0;  // true
}
```

### Real-World Example: Player Count

```c
void PrintPlayerCount()
{
    array<Man> players = new array<Man>;
    GetGame().GetPlayers(players);
    int count = players.Count();
    Print(string.Format("Players online: %1", count));
}
```

---

## Working with `float`

Floats represent decimal numbers. DayZ uses them extensively for positions, distances, health percentages, damage values, and timers.

```c
void FloatExamples()
{
    float health = 100.0;
    float damage = 25.5;
    float remaining = health - damage;   // 74.5

    // DayZ-specific: damage multiplier
    float headMultiplier = 3.0;
    float actualDamage = damage * headMultiplier;  // 76.5

    // Float division gives decimal results
    float ratio = 7.0 / 2.0;   // 3.5

    // Useful math (full Math class reference in Math & Vector Operations)
    float dist = 150.7;
    float rounded = Math.Round(dist);    // 151
    float floored = Math.Floor(dist);    // 150
    float ceiled  = Math.Ceil(dist);     // 151
    float clamped = Math.Clamp(dist, 0.0, 100.0);  // 100
}
```

Note that `Math.Round()`, `Math.Floor()`, and `Math.Ceil()` all *return* `float`, not `int` --- assign the result to an `int` variable when you need a whole number (the implicit conversion is safe because the value is already whole).

### Real-World Example: Distance Check

```c
bool IsPlayerNearby(PlayerBase player, vector targetPos, float radius)
{
    if (!player)
        return false;

    vector playerPos = player.GetPosition();
    float distance = vector.Distance(playerPos, targetPos);
    return distance <= radius;
}
```

---

## Working with `bool`

Booleans hold `true` or `false`. They are used in conditions, flags, and state tracking.

```c
void BoolExamples()
{
    bool isAdmin = true;
    bool isBanned = false;

    // Logical operators
    bool canPlay = isAdmin || !isBanned;    // true (OR, NOT)
    bool isSpecial = isAdmin && !isBanned;  // true (AND)

    // Negation
    bool notAdmin = !isAdmin;   // false

    // Comparison results are bool
    int health = 50;
    bool isLow = health < 25;       // false
    bool isHurt = health < 100;     // true
    bool isDead = health == 0;      // false
    bool isAlive = health != 0;     // true
}
```

### Conditions and Non-`bool` Values

Two non-`bool` shortcuts are safe and idiomatic --- the vanilla scripts use both constantly:

**Object references.** A `null` reference is false; a valid reference is true. This is *the* standard null-check pattern:

```c
void SafeCheck(PlayerBase player)
{
    // These two are equivalent:
    if (player != null)
        Print("Player exists");

    if (player)
        Print("Player exists");

    // And these two:
    if (player == null)
        Print("No player");

    if (!player)
        Print("No player");
}
```

**Plain `int` variables and return values.** Zero is false, non-zero is true. Vanilla code uses this for count checks, e.g. `if (m_Arrows.Count())`:

```c
void CountCheck(array<string> names)
{
    if (names.Count())
    {
        Print("List is not empty");
    }
}
```

**For everything else, compare explicitly.** Do not rely on bare truthiness for strings or floats --- the vanilla scripts always write the comparison out (`if (attachment_type != "")`, `if (particleName == string.Empty)`), and you should too:

```c
void ExplicitChecks(string itemType, float temperature)
{
    if (itemType != "")           // NOT: if (itemType)
        Print("Type is set");

    if (temperature > 0)          // NOT: if (temperature)
        Print("Above freezing");
}
```

One related trap: applying `!` directly to an *array element* (`if (!list[1])`) does not compile even though the element is an `int` --- use `if (list[1] == 0)`. See [What Does NOT Exist (Gotchas)](12-gotchas.md) for the full list of expression forms the parser rejects.

---

## Strings at a Glance

Strings in Enforce Script are **value types** --- they are copied when assigned or passed to functions, just like `int` or `float`. This is different from C# or Java, where strings are reference types.

Two facts are worth carrying from this chapter; the rest lives in [String Operations](06-strings.md):

- **`+` concatenates and converts numbers automatically.** `"HP: " + health` produces `"HP: 75"` when `health` is `75`. The vanilla scripts do this constantly (for example `Print("cnt=" + cnt)`).
- **`string.Format()` is preferred for multi-value messages.** It uses 1-indexed placeholders (`%1`, `%2`, ...) and avoids a chain of intermediate copies.

```c
void StringExamples()
{
    string name = "Survivor";
    int health = 75;

    string status = "HP: " + health;   // "HP: 75" -- + converts the number for you

    // Preferred when a message mixes several values:
    string formatted = string.Format("Player %1 has %2 health", name, health);
    // Result: "Player Survivor has 75 health"

    bool same = (name == "Survivor");   // comparison yields bool
}
```

The full string method reference --- searching, splitting, replacing, case conversion, substrings, in-place modification, and the supported escape sequences (`\n` `\r` `\t` `\\` `\"`) --- lives in [String Operations](06-strings.md).

---

## Vectors at a Glance

The `vector` type holds three `float` components (x, y, z). It is DayZ's fundamental type for positions, directions, rotations, and velocities. Like strings and primitives, vectors are **value types** --- they are copied on assignment.

```c
void VectorBasics()
{
    // Two ways to initialize
    vector pos1 = "100.5 0 200.3";          // space-separated string (NOT commas)
    vector pos2 = Vector(100.5, 0, 200.3);  // Vector() constructor

    vector empty;                           // default is "0 0 0"

    // Component access is array-style
    float x = pos1[0];   // East(+)  / West(-)
    float y = pos1[1];   // Up(+)    / Down(-), altitude above sea level
    float z = pos1[2];   // North(+) / South(-)

    pos1[1] = 50.0;      // writing a single component
}
```

**Important:** the string form uses **spaces** as separators, not commas. `"1 2 3"` is valid; `"1,2,3"` is not.

Everything else --- `vector.Distance()`, `Normalized()`, `Length()`, `vector.Direction()`, `vector.Lerp()`, `vector.Dot()`, the static constants (`vector.Zero`, `vector.Up`, `vector.Aside`, `vector.Forward`), rotation, and transformation matrices --- is covered in depth in [Math & Vector Operations](07-math-vectors.md).

---

## Working with `typename`

The `typename` type holds a reference to a type itself. It is used for reflection --- inspecting and working with types at runtime. You will encounter it when writing generic systems, config loaders, and factory patterns.

```c
void TypenameExamples()
{
    // Get the typename of a class
    typename t = PlayerBase;

    // Get a typename from a string
    string typeStr = "PlayerBase";
    typename t2 = typeStr.ToType();

    // Compare types
    if (t == PlayerBase)
        Print("It's PlayerBase!");

    // Convert typename to string
    string name = t.ToString();  // "PlayerBase"

    // Create an instance from a typename (factory pattern)
    Class instance = t2.Spawn();
}

void InheritanceCheck(PlayerBase player)
{
    if (!player)
        return;

    // Get the typename of an object instance
    typename objType = player.Type();

    // Check inheritance
    bool isMan = objType.IsInherited(Man);
}
```

### Enum Conversion with typename

```c
enum DamageType
{
    MELEE = 0,
    BULLET = 1,
    EXPLOSION = 2
};

void EnumConvert()
{
    // Enum to string
    string name = typename.EnumToString(DamageType, DamageType.BULLET);
    // name == "BULLET"

    // String to enum (returns int, -1 on failure)
    int value = typename.StringToEnum(DamageType, "EXPLOSION");
    // value == 2
}
```

Deeper reflection --- enumerating variables, reading fields by name, `Class.CastTo()` internals --- is covered in [Casting & Reflection](09-casting-reflection.md).

---

## The `Managed` Base Class

`Managed` is a special base class for script-side objects. Its practical effect concerns *weak references*: when an object of a `Managed` class is deleted, every plain (non-`ref`) variable that still pointed at it is automatically set to `null`. For a class that does not extend `Managed`, those variables become dangling pointers --- reading them crashes the game.

```c
class MyScriptHandler : Managed
{
    // Weak references to instances of this class are zeroed on delete
}
```

Most script-only classes (that don't represent game entities) should extend `Managed`. Entity classes like `PlayerBase` and `ItemBase` belong to the `EntityAI` hierarchy, whose lifetime the engine controls --- you never choose a base class for those.

### When to Use Managed

| Use `Managed` for... | Do NOT use `Managed` for... |
|----------------------|-----------------------------|
| Config data classes | Items (`ItemBase`) |
| Manager singletons | Weapons (`Weapon_Base`) |
| UI controllers | Vehicles (`CarScript`) |
| Event handler objects | Players (`PlayerBase`) |
| Helper/utility classes | Any class that extends `EntityAI` |

If your class does not represent a physical entity in the game world, it should almost certainly extend `Managed`. The full story --- `ref` counting, weak vs strong references, and leak patterns --- is in [Memory Management](08-memory-management.md).

---

## Type Conversion

Enforce Script supports both implicit and explicit conversions between types.

### Implicit Conversions

Numeric conversions happen automatically:

```c
void ImplicitConversions()
{
    // int to float (large integer values can lose precision)
    int count = 42;
    float fCount = count;    // 42.0

    // float to int (TRUNCATES, does not round!)
    float precise = 3.99;
    int truncated = precise;  // 3, NOT 4
}
```

The vanilla scripts rely on the float-to-int conversion when storing rounded values, e.g. `int mask = Math.Round(floats.Get(index));` --- `Math.Round()` returns a `float`, and assigning it to an `int` is fine because the value is already whole.

### Explicit Conversions (Parsing)

To convert between strings and numeric types, use parsing methods:

```c
void ExplicitConversions()
{
    // String to int
    string numStr = "42";
    int num = numStr.ToInt();         // 42

    string badStr = "hello";
    int bad = badStr.ToInt();         // 0 (fails silently)

    // String to float
    string floatStr = "3.14";
    float f = floatStr.ToFloat();     // 3.14

    // String to vector
    string vecStr = "100 25 200";
    vector v = vecStr.ToVector();     // <100, 25, 200>

    // Number to string (using Format)
    string s1 = string.Format("%1", 42);       // "42"
    string s2 = string.Format("%1", 3.14);     // "3.14"

    // int to string via ToString()
    int score = 42;
    string s3 = score.ToString();     // "42"
}
```

### Object Casting

For class types, use `Class.CastTo()` or `ClassName.Cast()`. This is covered in detail in [Classes & Inheritance](03-classes-inheritance.md) and [Casting & Reflection](09-casting-reflection.md), but here is the essential pattern:

```c
void CastExample(Object obj)
{
    // Safe cast (preferred)
    PlayerBase player;
    if (Class.CastTo(player, obj))
    {
        // player is valid and safe to use
        Print(player.GetType());
    }

    // Alternative cast syntax
    PlayerBase player2 = PlayerBase.Cast(obj);
    if (player2)
    {
        // player2 is valid
    }
}
```

---

## Variable Scope

Variables exist only within the code block (curly braces) where they are declared. Enforce Script does **not** allow redeclaring a variable name within nested scopes.

```c
void ScopeExample()
{
    int x = 10;

    if (true)
    {
        // int x = 20;  // ERROR: redeclaration of 'x' in nested scope
        x = 20;         // OK: modifying the outer x
        int y = 30;     // OK: new variable in this scope
    }

    // y is NOT accessible here (declared in inner scope)
    // Print(y);  // ERROR: undeclared identifier 'y'

    // IMPORTANT: this also applies to for loops
    for (int i = 0; i < 5; i++)
    {
        // i exists here
    }
    // for (int i = 0; i < 3; i++)  // ERROR in DayZ: 'i' already declared
    // Use a different name:
    for (int j = 0; j < 3; j++)
    {
        // j exists here
    }
}
```

The same restriction hits *sibling* scopes too: declaring the same variable name in an `if` block and its `else` block is a compile error. That trap, and the pattern for avoiding it, is covered with the rest of the branching rules in [Control Flow](05-control-flow.md).

---

## Operator Precedence

From highest to lowest precedence:

| Priority | Operator | Description | Associativity |
|----------|----------|-------------|---------------|
| 1 | `()` `[]` `.` | Grouping, array access, member access | Left to right |
| 2 | `!` `-` (unary) `~` | Logical NOT, negation, bitwise NOT | Right to left |
| 3 | `*` `/` `%` | Multiplication, division, modulo | Left to right |
| 4 | `+` `-` | Addition, subtraction | Left to right |
| 5 | `<<` `>>` | Bitwise shift | Left to right |
| 6 | `<` `<=` `>` `>=` | Relational | Left to right |
| 7 | `==` `!=` | Equality | Left to right |
| 8 | `&` | Bitwise AND | Left to right |
| 9 | `^` | Bitwise XOR | Left to right |
| 10 | `\|` | Bitwise OR | Left to right |
| 11 | `&&` | Logical AND | Left to right |
| 12 | `\|\|` | Logical OR | Left to right |
| 13 | `=` `+=` `-=` `*=` `/=` `%=` `&=` `\|=` `^=` `<<=` `>>=` | Assignment | Right to left |

> **Tip:** When in doubt, use parentheses. Enforce Script follows C-like precedence rules, but explicit grouping prevents bugs and improves readability.

---

## Common Mistakes

### 1. Uninitialized Variables Used in Logic

Primitives get default values (`0`, `0.0`, `false`, `""`), but relying on this makes code fragile and hard to read. Always initialize explicitly.

```c
// BAD: relying on implicit zero
int count;
if (count > 0)  // This works because count == 0, but intent is unclear
    DoThing();

// GOOD: explicit initialization
int count = 0;
if (count > 0)
    DoThing();
```

### 2. Float-to-Int Truncation

Float-to-int conversion truncates (rounds toward zero), not rounds to nearest:

```c
float f = 3.99;
int i = f;         // i == 3, NOT 4

// If you want rounding:
int rounded = Math.Round(f);  // 4
```

### 3. Float Precision in Comparisons

Never compare floats for exact equality:

```c
float a = 0.1 + 0.2;
// BAD: may fail due to floating-point representation
if (a == 0.3)
    Print("Equal");

// GOOD: use a tolerance (epsilon)
if (Math.AbsFloat(a - 0.3) < 0.001)
    Print("Close enough");
```

### 4. Testing Strings with Bare Truthiness

Object references and plain `int` values can be tested directly in a condition, but do not extend that habit to strings. Compare explicitly against `""`:

```c
void CheckItemType(string itemType)
{
    // BAD: do not rely on truthiness for strings
    // if (itemType) ...

    // GOOD: explicit comparison, exactly as the vanilla scripts do
    if (itemType != "")
        Print("Type is set");
}
```

### 5. Vector String Format

Vector string initialization requires spaces, not commas:

```c
vector good = "100 25 200";     // CORRECT
// vector bad = "100, 25, 200"; // WRONG: commas are not parsed correctly
// vector bad2 = "100,25,200";  // WRONG
```

### 6. Forgetting that Strings and Vectors are Value Types

Unlike class objects, strings and vectors are copied on assignment. Modifying a copy does not affect the original:

```c
vector posA = "10 20 30";
vector posB = posA;       // posB is a COPY
posB[1] = 99;             // Only posB changes
// posA is still "10 20 30"
```

### 7. Reaching for `auto` by Habit

`auto` compiles, but relying on it makes long generic declarations harder to read at a glance, and it is not how vanilla code is written. Prefer the explicit type, especially for collection types where the type itself is documentation:

```c
// COMPILES, but obscures the type at the declaration site:
auto data = new map<string, ref array<int>>;

// PREFERRED: the type is visible without reading the initializer
map<string, ref array<int>> data = new map<string, ref array<int>>;
```

---

## Practice Exercises

### Exercise 1: Variable Basics
Declare variables to store:
- A player's name (string)
- Their health percentage (float, 0-100)
- Their kill count (int)
- Whether they are an admin (bool)
- Their world position (vector)

Print a formatted summary using `string.Format()`.

### Exercise 2: Temperature Converter
Write a function `float CelsiusToFahrenheit(float celsius)` and its inverse `float FahrenheitToCelsius(float fahrenheit)`. Test with boiling point (100C = 212F) and freezing point (0C = 32F).

### Exercise 3: Distance Calculator
Write a function that takes two vectors and returns:
- The 3D distance between them
- The 2D distance (ignoring height/Y axis)
- The height difference

Hint: For 2D distance, create new vectors with `[1]` set to `0` before calculating distance.

### Exercise 4: Type Juggling
Given the string `"42"`, convert it to:
1. An `int`
2. A `float`
3. Back to a `string` using `string.Format()`

### Exercise 5: Ground Position
Write a function `vector SnapToGround(vector pos)` that takes any position and returns it with the Y component set to the terrain height at that X,Z location. Use `GetGame().SurfaceY()`.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Types | `int`, `float`, `bool`, `string`, `vector`, `typename`, `void` |
| Defaults | `0`, `0.0`, `false`, `""`, `"0 0 0"`, `null` |
| `auto` | Exists for local type inference, but vanilla code almost never uses it --- prefer an explicit type |
| Constants | `const` keyword, `UPPER_SNAKE_CASE` convention |
| Strings | Value type; `+` converts numbers automatically; full reference in [String Operations](06-strings.md) |
| Vectors | Init with `"x y z"` string or `Vector(x,y,z)`, access with `[0]`, `[1]`, `[2]`; math in [Math & Vector Operations](07-math-vectors.md) |
| Conditions | Bare truthiness for object refs and plain `int` only; compare strings and floats explicitly |
| Scope | Variables scoped to `{}` blocks; no redeclaration in nested scopes; sibling trap in [Control Flow](05-control-flow.md) |
| Conversion | `float`-to-`int` truncates; use `.ToInt()`, `.ToFloat()`, `.ToVector()` for string parsing |
| Formatting | Use `string.Format()` for multi-value messages |
