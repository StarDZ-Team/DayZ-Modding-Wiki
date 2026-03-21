# 第 1.1 章：变量与类型

[Home](../../README.md) | **变量与类型** | [下一章：数组、映射与集合 >>](02-arrays-maps-sets.md)

---

## 简介

Enforce Script 是 Enfusion 引擎的脚本语言，用于 DayZ 独立版。它是一种具有类 C 语法的面向对象语言，在很多方面类似于 C#，但拥有自己独特的类型集、规则和限制。如果你有 C#、Java 或 C++ 的经验，你会很快上手——但请密切关注差异之处，因为 Enforce Script 与这些语言不同的地方正是 Bug 隐藏的地方。

本章涵盖基本构建模块：基本类型、如何声明和初始化变量，以及类型转换的工作方式。每一行 DayZ Mod 代码都从这里开始。

---

## 基本类型

Enforce Script 有一组固定的基本类型。你无法定义新的值类型——只能定义类（在[第 1.3 章](03-classes-inheritance.md)中介绍）。

| 类型 | 大小 | 默认值 | 说明 |
|------|------|---------------|-------------|
| `int` | 32-bit signed | `0` | Whole numbers from -2,147,483,648 to 2,147,483,647 |
| `float` | 32-bit IEEE 754 | `0.0` | Floating-point numbers |
| `bool` | 1 bit logical | `false` | `true` or `false` |
| `string` | Variable | `""` (empty) | Text. Immutable value type --- passed by value, not reference |
| `vector` | 3x float | `"0 0 0"` | Three-component float (x, y, z). Passed by value |
| `typename` | Engine ref | `null` | A reference to a type itself, used for reflection |
| `void` | N/A | N/A | Used only as a return type to indicate "returns nothing" |

### 类型常量

一些类型提供了有用的常量：

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

## 声明变量

变量通过先写类型、后写名称来声明。你可以在一条语句中同时声明和赋值，也可以分开进行。

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

### `auto` 关键字

当右侧的类型显而易见时，你可以使用 `auto` 让编译器推断类型：

```c
void Example()
{
    auto count = 10;           // int
    auto ratio = 0.75;         // float
    auto label = "Hello";      // string
    auto player = GetGame().GetPlayer();  // DayZPlayer (or whatever GetPlayer returns)
}
```

这纯粹是为了方便——编译器在编译时确定类型。没有性能差异。

### 常量

使用 `const` 关键字声明初始化后不应更改的值：

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

常量通常在文件作用域（任何函数之外）或作为类成员声明。命名规范：`UPPER_SNAKE_CASE`。

---

## 使用 `int`

整数是最常用的类型。DayZ 用它来表示物品数量、玩家 ID、生命值（离散化时）、枚举值、位标志等。

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

## 使用 `float`

浮点数表示小数。DayZ 大量使用浮点数来表示位置、距离、生命值百分比、伤害值和计时器。

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

    // Useful math
    float dist = 150.7;
    float rounded = Math.Round(dist);    // 151
    float floored = Math.Floor(dist);    // 150
    float ceiled  = Math.Ceil(dist);     // 151
    float clamped = Math.Clamp(dist, 0.0, 100.0);  // 100
}
```

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

## 使用 `bool`

布尔值保存 `true` 或 `false`。它们用于条件判断、标志和状态跟踪。

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

### 条件中的真值判定

在 Enforce Script 中，你可以在条件中使用非 bool 值。以下值被视为 `false`：
- `0` (int)
- `0.0` (float)
- `""` (empty string)
- `null` (null object reference)

其他所有值都是 `true`。这通常用于空值检查：

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

---

## 使用 `string`

Enforce Script 中的字符串是**值类型**——它们在赋值或传递给函数时被复制，就像 `int` 或 `float` 一样。这与 C# 或 Java 中字符串是引用类型不同。

```c
void StringExamples()
{
    string greeting = "Hello";
    string name = "Survivor";

    // Concatenation with +
    string message = greeting + ", " + name + "!";  // "Hello, Survivor!"

    // String formatting (1-indexed placeholders)
    string formatted = string.Format("Player %1 has %2 health", name, 75);
    // Result: "Player Survivor has 75 health"

    // Length
    int len = message.Length();    // 17

    // Comparison
    bool same = (greeting == "Hello");  // true

    // Conversion from other types
    string fromInt = "Score: " + 42;     // does NOT work -- must convert explicitly
    string correct = "Score: " + 42.ToString();  // "Score: 42"

    // Using Format is the preferred approach
    string best = string.Format("Score: %1", 42);  // "Score: 42"
}
```

### 转义序列

字符串支持标准转义序列：

| 序列 | 含义 |
|----------|---------|
| `\n` | Newline |
| `\r` | Carriage return |
| `\t` | Tab |
| `\\` | Literal backslash |
| `\"` | Literal double quote |

**警告：** While these are documented, backslash (`\\`) and escaped quotes (`\"`) are known to cause issues with the CParser in some contexts, especially in JSON-related operations. When working with file paths or JSON strings, avoid backslashes when possible. Use forward slashes for paths --- DayZ accepts them on all platforms.

### Real-World Example: Chat Message

```c
void SendAdminMessage(string adminName, string text)
{
    string msg = string.Format("[ADMIN] %1: %2", adminName, text);
    Print(msg);
}
```

---

## 使用 `vector`

`vector` 类型包含三个 `float` 分量（x、y、z）。它是 DayZ 用于位置、方向、旋转和速度的基本类型。与字符串和基本类型一样，向量是**值类型**——在赋值时会被复制。

### 初始化

向量可以通过两种方式初始化：

```c
void VectorInit()
{
    // Method 1: String initialization (three space-separated numbers)
    vector pos1 = "100.5 0 200.3";

    // Method 2: Vector() constructor function
    vector pos2 = Vector(100.5, 0, 200.3);

    // Default value is "0 0 0"
    vector empty;   // empty == <0, 0, 0>
}
```

**重要：** The string initialization format uses **spaces** as separators, not commas. `"1 2 3"` is valid; `"1,2,3"` is not.

### 分量访问

使用数组风格的索引访问各分量：

```c
void VectorComponents()
{
    vector pos = Vector(100.5, 25.0, 200.3);

    // Reading components
    float x = pos[0];   // 100.5  (East/West)
    float y = pos[1];   // 25.0   (Up/Down, altitude)
    float z = pos[2];   // 200.3  (North/South)

    // Writing components
    pos[1] = 50.0;      // Change altitude to 50
}
```

DayZ 坐标系：
- `[0]` = X = East(+) / West(-)
- `[1]` = Y = 上级(+) / Down(-) (altitude above sea level)
- `[2]` = Z = North(+) / South(-)

### 静态常量

```c
vector zero    = vector.Zero;      // "0 0 0"
vector up      = vector.Up;        // "0 1 0"
vector right   = vector.Aside;     // "1 0 0"
vector forward = vector.Forward;   // "0 0 1"
```

### 常用向量运算

```c
void VectorOps()
{
    vector pos1 = Vector(100, 0, 200);
    vector pos2 = Vector(150, 0, 250);

    // Distance between two points
    float dist = vector.Distance(pos1, pos2);

    // Squared distance (faster, good for comparisons)
    float distSq = vector.DistanceSq(pos1, pos2);

    // Direction from pos1 to pos2
    vector dir = vector.Direction(pos1, pos2);

    // Normalize a vector (make length = 1)
    vector norm = dir.Normalized();

    // Length of a vector
    float len = dir.Length();

    // Linear interpolation (50% between pos1 and pos2)
    vector midpoint = vector.Lerp(pos1, pos2, 0.5);

    // Dot product
    float dot = vector.Dot(dir, vector.Up);
}
```

### Real-World Example: Spawn Position

```c
// Get a position on the ground at given X,Z coordinates
vector GetGroundPosition(float x, float z)
{
    vector pos = Vector(x, 0, z);
    pos[1] = GetGame().SurfaceY(x, z);  // Set Y to terrain height
    return pos;
}

// Get a random position within a radius of a center point
vector GetRandomPositionAround(vector center, float radius)
{
    float angle = Math.RandomFloat(0, Math.PI2);
    float dist = Math.RandomFloat(0, radius);

    vector offset = Vector(Math.Cos(angle) * dist, 0, Math.Sin(angle) * dist);
    vector pos = center + offset;
    pos[1] = GetGame().SurfaceY(pos[0], pos[2]);
    return pos;
}
```

---

## 使用 `typename`

`typename` 类型持有对类型本身的引用。它用于反射——在运行时检查和操作类型。编写通用系统、配置加载器和工厂模式时会用到它。

```c
void TypenameExamples()
{
    // Get the typename of a class
    typename t = PlayerBase;

    // Get typename from a string
    typename t2 = t.StringToEnum(PlayerBase, "PlayerBase");

    // Compare types
    if (t == PlayerBase)
        Print("It's PlayerBase!");

    // Get the typename of an object instance
    PlayerBase player;
    // ... assume player is valid ...
    typename objType = player.Type();

    // Check inheritance
    bool isMan = objType.IsInherited(Man);

    // Convert typename to string
    string name = t.ToString();  // "PlayerBase"

    // Create an instance from typename (factory pattern)
    Class instance = t.Spawn();
}
```

### 使用 typename 进行枚举转换

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

    // String to enum
    int value;
    typename.StringToEnum(DamageType, "EXPLOSION", value);
    // value == 2
}
```

---

## 类型转换

Enforce Script 支持类型之间的隐式和显式转换。

### 隐式转换

一些转换会自动发生：

```c
void ImplicitConversions()
{
    // int to float (always safe, no data loss)
    int count = 42;
    float fCount = count;    // 42.0

    // float to int (TRUNCATES, does not round!)
    float precise = 3.99;
    int truncated = precise;  // 3, NOT 4

    // int/float to bool
    bool fromInt = 5;      // true (non-zero)
    bool fromZero = 0;     // false
    bool fromFloat = 0.1;  // true (non-zero)

    // bool to int
    int fromBool = true;   // 1
    int fromFalse = false; // 0
}
```

### 显式转换（解析）

要在字符串和数值类型之间转换，请使用解析方法：

```c
void ExplicitConversions()
{
    // String to int
    int num = "42".ToInt();           // 42
    int bad = "hello".ToInt();        // 0 (fails silently)

    // String to float
    float f = "3.14".ToFloat();       // 3.14

    // String to vector
    vector v = "100 25 200".ToVector();  // <100, 25, 200>

    // Number to string (using Format)
    string s1 = string.Format("%1", 42);       // "42"
    string s2 = string.Format("%1", 3.14);     // "3.14"

    // int/float .ToString()
    string s3 = (42).ToString();     // "42"
}
```

### 对象转型

对于类类型，使用 `Class.CastTo()` 或 `ClassName.Cast()`。这在[第 1.3 章](03-classes-inheritance.md)中有详细介绍，以下是基本模式：

```c
void CastExample()
{
    Object obj = GetSomeObject();

    // Safe cast (preferred)
    PlayerBase player;
    if (Class.CastTo(player, obj))
    {
        // player is valid and safe to use
        string name = player.GetIdentity().GetName();
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

## 变量作用域

变量仅存在于声明它们的代码块（花括号）中。Enforce Script **不允许**在嵌套或兄弟作用域中重新声明同名变量。

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

### 兄弟作用域陷阱

这是 Enforce Script 最臭名昭著的怪癖之一。在 `if` 和 `else` 块中声明同名变量会导致编译错误：

```c
void SiblingTrap()
{
    if (someCondition)
    {
        int result = 10;    // Declared here
        Print(result);
    }
    else
    {
        // int result = 20; // ERROR: multiple declaration of 'result'
        // Even though this is a sibling scope, not the same scope
    }

    // FIX: declare above the if/else
    int result;
    if (someCondition)
    {
        result = 10;
    }
    else
    {
        result = 20;
    }
}
```

---

## 常见错误

### 1. Uninitialized Variables Used in Logic

基本类型会获得默认值（`0`、`0.0`、`false`、`""`），但依赖这一点会使代码脆弱且难以阅读。始终显式初始化。

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

浮点数转整数会截断（向零取整），而不是四舍五入：

```c
float f = 3.99;
int i = f;         // i == 3, NOT 4

// If you want rounding:
int rounded = Math.Round(f);  // 4
```

### 3. Float Precision in Comparisons

永远不要比较浮点数的精确相等：

```c
float a = 0.1 + 0.2;
// BAD: may fail due to floating-point representation
if (a == 0.3)
    Print("Equal");

// GOOD: use a tolerance (epsilon)
if (Math.AbsFloat(a - 0.3) < 0.001)
    Print("Close enough");
```

### 4. String Concatenation with Numbers

你不能简单地用 `+` 将数字连接到字符串。请使用 `string.Format()`：

```c
int kills = 5;
// Potentially problematic:
// string msg = "Kills: " + kills;

// CORRECT: use Format
string msg = string.Format("Kills: %1", kills);
```

### 5. Vector String Format

向量字符串初始化需要空格，而不是逗号：

```c
vector good = "100 25 200";     // CORRECT
// vector bad = "100, 25, 200"; // WRONG: commas are not parsed correctly
// vector bad2 = "100,25,200";  // WRONG
```

### 6. Forgetting that Strings and Vectors are Value Types

与类对象不同，字符串和向量在赋值时会被复制。修改副本不会影响原始值：

```c
vector posA = "10 20 30";
vector posB = posA;       // posB is a COPY
posB[1] = 99;             // Only posB changes
// posA is still "10 20 30"
```

---

## 练习题

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
4. A `bool` (should be `true` since the int value is non-zero)

### Exercise 5: Ground Position
Write a function `vector SnapToGround(vector pos)` that takes any position and returns it with the Y component set to the terrain height at that X,Z location. Use `GetGame().SurfaceY()`.

---

## 总结

| 概念 | 要点 |
|---------|-----------|
| Types | `int`, `float`, `bool`, `string`, `vector`, `typename`, `void` |
| Defaults | `0`, `0.0`, `false`, `""`, `"0 0 0"`, `null` |
| Constants | `const` keyword, `UPPER_SNAKE_CASE` convention |
| Vectors | Init with `"x y z"` string or `Vector(x,y,z)`, access with `[0]`, `[1]`, `[2]` |
| Scope | Variables scoped to `{}` blocks; no redeclaration in nested/sibling blocks |
| Conversion | `float`-to-`int` truncates; use `.ToInt()`, `.ToFloat()`, `.ToVector()` for string parsing |
| Formatting | Always use `string.Format()` for building strings from mixed types |

---

[Home](../../README.md) | **变量与类型** | [下一章：数组、映射与集合 >>](02-arrays-maps-sets.md)
