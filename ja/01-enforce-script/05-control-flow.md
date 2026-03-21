# 第1.5章：制御フロー

[<< 1.4: Modded Classes](04-modded-classes.md) | [ホーム](../../README.md) | [1.6: String Operations >>](06-strings.md)

---

## はじめに

制御フローはコードの実行順序を決定します。Enforce Script はおなじみの `if/else`、`for`、`while`、`foreach`、`switch` 構文を提供しますが、C/C++ との重要な違いがいくつかあり、準備していないと不意を突かれます。この章では、DayZ のスクリプトエンジン固有の落とし穴を含む、すべての制御フローメカニズムを扱います。

---

## if / else / else if

The `if` statement evaluates a boolean expression and executes a block of code when the result is `true`. You can chain conditions with `else if` and provide a fallback with `else`.

```c
void CheckHealth(PlayerBase player)
{
    float health = player.GetHealth("", "Health");

    if (health > 75)
    {
        Print("Player is healthy");
    }
    else if (health > 25)
    {
        Print("Player is wounded");
    }
    else
    {
        Print("Player is critical");
    }
}
```

### Null チェック

In Enforce Script, object references evaluate to `false` when null. これが null アクセスを防ぐ標準的な方法です：

```c
void ProcessItem(EntityAI item)
{
    if (!item)
        return;

    string name = item.GetType();
    Print("Processing: " + name);
}
```

### 論理演算子

条件を以下で組み合わせます： `&&` (AND) and `||` (OR). 短絡評価が適用されます： `&&` の左辺が `false` の場合、右辺は評価されません。

```c
void CheckPlayerState(PlayerBase player)
{
    if (player && player.IsAlive())
    {
        // Safe -- player is checked for null before calling IsAlive()
        Print("Player is alive");
    }

    if (player.GetHealth("", "Blood") < 3000 || player.GetHealth("", "Health") < 25)
    {
        Print("Player is in danger");
    }
}
```

### PITFALL: Variable redeclaration in else-if blocks

これは Enforce Script で最も一般的なエラーの1つです。 ほとんどの言語では、`if` ブランチ内で宣言された変数は兄弟の `else` ブランチの変数と独立しています。 **Enforce Script では違います。** Declaring the same variable name in sibling `if`/`else if`/`else` blocks causes a **multiple declaration error** at compile time.

```c
// WRONG -- Compile error!
void BadExample(Object obj)
{
    if (obj.IsKindOf("Car"))
    {
        Car vehicle = Car.Cast(obj);
        vehicle.GetSpeedometer();
    }
    else if (obj.IsKindOf("ItemBase"))
    {
        ItemBase item = ItemBase.Cast(obj);    // OK -- different name
        item.GetQuantity();
    }
    else
    {
        string msg = "Unknown object";         // First declaration of msg
        Print(msg);
    }
}
```

Wait -- that looks fine, right? The problem occurs when you use the **same variable name** in two branches:

```c
// WRONG -- Compile error: multiple declaration of 'result'
void ProcessObject(Object obj)
{
    if (obj.IsKindOf("Car"))
    {
        string result = "It's a car";
        Print(result);
    }
    else
    {
        string result = "It's something else";  // ERROR! Same name as in the if block
        Print(result);
    }
}
```

**修正方法：** if 文の**前**で変数を宣言するか、ブランチごとに一意な名前を使用します。

```c
// CORRECT -- Declare before the if
void ProcessObject(Object obj)
{
    string result;

    if (obj.IsKindOf("Car"))
    {
        result = "It's a car";
    }
    else
    {
        result = "It's something else";
    }

    Print(result);
}
```

---

## for ループ

`for` ループは C スタイルの構文と同一です： 初期化子、条件、インクリメント。

```c
// Print numbers 0 through 9
void CountToTen()
{
    for (int i = 0; i < 10; i++)
    {
        Print(i);
    }
}
```

### Iterating over an array with for

```c
void ListInventory(PlayerBase player)
{
    array<EntityAI> items = new array<EntityAI>;
    player.GetInventory().EnumerateInventory(InventoryTraversalType.PREORDER, items);

    for (int i = 0; i < items.Count(); i++)
    {
        EntityAI item = items.Get(i);
        if (item)
        {
            Print(string.Format("[%1] %2", i, item.GetType()));
        }
    }
}
```

### Nested for loops

```c
// Spawn a grid of objects
void SpawnGrid(vector origin, int rows, int cols, float spacing)
{
    for (int r = 0; r < rows; r++)
    {
        for (int c = 0; c < cols; c++)
        {
            vector pos = origin;
            pos[0] = pos[0] + (c * spacing);
            pos[2] = pos[2] + (r * spacing);
            pos[1] = GetGame().SurfaceY(pos[0], pos[2]);

            GetGame().CreateObject("Barrel_Green", pos, false, false, true);
        }
    }
}
```

> **注意：** Do not redeclare the loop variable `i` if there is already a variable named `i` in the enclosing scope. Enforce Script treats this as a multiple declaration error, even in nested scopes.

---

## while ループ

`while` ループは条件が `true` の間、ブロックを繰り返します。 条件は各反復の**前**に評価されます。

```c
// Remove all dead zombies from a tracking list
void CleanupDeadZombies(array<DayZInfected> zombieList)
{
    int i = 0;
    while (i < zombieList.Count())
    {
        EntityAI eai;
        if (Class.CastTo(eai, zombieList.Get(i)) && !eai.IsAlive())
        {
            zombieList.RemoveOrdered(i);
            // Do NOT increment i -- the next element has shifted into this index
        }
        else
        {
            i++;
        }
    }
}
```

### WARNING: There is NO do...while in Enforce Script

`do...while` キーワードは存在しません。 コンパイラは拒否します。 If you need a loop that always executes at least once, use the flag pattern described below.

```c
// WRONG -- This will NOT compile
do
{
    // body
}
while (someCondition);
```

---

## フラグによる do...while のシミュレーション

The standard workaround is to use a `bool` flag that is `true` on the first iteration:

```c
void SimulateDoWhile()
{
    bool first = true;
    int attempts = 0;
    vector spawnPos;

    while (first || !IsPositionSafe(spawnPos))
    {
        first = false;
        attempts++;
        spawnPos = GetRandomPosition();

        if (attempts > 100)
            break;
    }

    Print(string.Format("Found safe position after %1 attempts", attempts));
}
```

An alternative approach using `break`:

```c
void AlternativeDoWhile()
{
    while (true)
    {
        // Body executes at least once
        DoSomething();

        // Check the exit condition at the END
        if (!ShouldContinue())
            break;
    }
}
```

---

## foreach

`foreach` 文は array、map、静的配列を反復処理する最もクリーンな方法です。 2つの形式があります。

### Simple foreach (value only)

```c
void AnnounceItems(array<string> itemNames)
{
    foreach (string name : itemNames)
    {
        Print("Found item: " + name);
    }
}
```

### foreach with index

When iterating over arrays, the first variable receives the index:

```c
void ListPlayers(array<Man> players)
{
    foreach (int idx, Man player : players)
    {
        Print(string.Format("Player #%1: %2", idx, player.GetIdentity().GetName()));
    }
}
```

### foreach over maps

For maps, the first variable receives the key and the second receives the value:

```c
void PrintScoreboard(map<string, int> scores)
{
    foreach (string playerName, int score : scores)
    {
        Print(string.Format("%1: %2 kills", playerName, score));
    }
}
```

You can also iterate over maps with just the value:

```c
void SumScores(map<string, int> scores)
{
    int total = 0;
    foreach (int score : scores)
    {
        total += score;
    }
    Print("Total kills: " + total);
}
```

### foreach over static arrays

```c
void PrintStaticArray()
{
    int numbers[] = {10, 20, 30, 40, 50};

    foreach (int value : numbers)
    {
        Print(value);
    }
}
```

---

## switch / case

`switch` 文は値を `case` ラベルのリストと照合します。 `int`、`string`、enum 値、定数で動作します。

### Important: NO fall-through

C/C++ と異なり、Enforce Script の `switch/case` はあるケースから次のケースへ**フォールスルーしません**。 各 `case` は独立しています。 明確さのために `break` を含めることはできますが、フォールスルー防止のために必須ではありません。

```c
void HandleCommand(string command)
{
    switch (command)
    {
        case "heal":
            HealPlayer();
            break;

        case "kill":
            KillPlayer();
            break;

        case "teleport":
            TeleportPlayer();
            break;

        default:
            Print("Unknown command: " + command);
            break;
    }
}
```

### switch with enums

```c
enum EDifficulty
{
    EASY = 0,
    MEDIUM,
    HARD
};

void SetDifficulty(EDifficulty difficulty)
{
    float zombieMultiplier;

    switch (difficulty)
    {
        case EDifficulty.EASY:
            zombieMultiplier = 0.5;
            break;

        case EDifficulty.MEDIUM:
            zombieMultiplier = 1.0;
            break;

        case EDifficulty.HARD:
            zombieMultiplier = 2.0;
            break;

        default:
            zombieMultiplier = 1.0;
            break;
    }

    Print(string.Format("Zombie multiplier: %1", zombieMultiplier));
}
```

### switch with integer constants

```c
void DescribeWeaponSlot(int slotId)
{
    const int SLOT_SHOULDER = 0;
    const int SLOT_MELEE = 1;
    const int SLOT_PISTOL = 2;

    switch (slotId)
    {
        case SLOT_SHOULDER:
            Print("Primary weapon");
            break;

        case SLOT_MELEE:
            Print("Melee weapon");
            break;

        case SLOT_PISTOL:
            Print("Sidearm");
            break;

        default:
            Print("Unknown slot");
            break;
    }
}
```

> **Remember:** Because there is no fall-through, you cannot stack cases to share a handler the way you would in C. Each case must have its own body.

---

## break と continue

### break

`break` は最も内側のループ（または switch case）を即座に抜けます。

```c
// Find the first player within 100 meters
void FindNearbyPlayer(vector origin, array<Man> players)
{
    foreach (Man player : players)
    {
        float dist = vector.Distance(origin, player.GetPosition());
        if (dist < 100)
        {
            Print("Found nearby player: " + player.GetIdentity().GetName());
            break; // Stop searching
        }
    }
}
```

### continue

`continue` は現在の反復の残りをスキップし、次の反復に進みます。

```c
// Process only alive players
void HealAllPlayers(array<Man> players)
{
    foreach (Man man : players)
    {
        PlayerBase player;
        if (!Class.CastTo(player, man))
            continue; // Not a PlayerBase, skip

        if (!player.IsAlive())
            continue; // Dead, skip

        player.SetHealth("", "Health", 100);
        Print("Healed: " + player.GetIdentity().GetName());
    }
}
```

### Nested loops with break

`break` は最も内側のループのみを抜けます。 ネストされたループを抜けるにはフラグ変数を使用します：

```c
void FindItemInGrid(array<array<string>> grid, string target)
{
    bool found = false;

    for (int row = 0; row < grid.Count(); row++)
    {
        for (int col = 0; col < grid.Get(row).Count(); col++)
        {
            if (grid.Get(row).Get(col) == target)
            {
                Print(string.Format("Found '%1' at [%2, %3]", target, row, col));
                found = true;
                break; // Only exits inner loop
            }
        }

        if (found)
            break; // Exits outer loop
    }
}
```

---

## よくある間違い

| 間違い | 問題 | 修正方法 |
|---------|---------|-----|
| Using `do...while` | Does not exist in Enforce Script | Use `while` with a `bool first = true` flag |
| Declaring same variable in `if` and `else` blocks | Multiple declaration error | Declare the variable before the `if` |
| Redeclaring loop variable `i` in nested scope | Multiple declaration error | Use different names (`i`, `j`, `k`) or declare outside |
| Expecting `switch` fall-through | Cases are independent, no fall-through | Each case needs its own complete handler |
| Modifying array while iterating with `foreach` | Undefined behavior, potential crash | Use index-based `for` loop when removing elements |
| Infinite `while` loop without `break` | Server freeze / client hang | Always ensure the condition will eventually be `false`, or use `break` |

---

## クイックリファレンス

```c
// if / else if / else
if (condition) { } else if (other) { } else { }

// for loop
for (int i = 0; i < count; i++) { }

// while loop
while (condition) { }

// Simulate do...while
bool first = true;
while (first || condition) { first = false; /* body */ }

// foreach (value only)
foreach (Type value : collection) { }

// foreach (index + value)
foreach (int i, Type value : array) { }

// foreach (key + value on map)
foreach (KeyType key, ValueType val : someMap) { }

// switch/case (no fall-through)
switch (value) { case X: /* ... */ break; default: break; }
```

---

[<< 1.4: Modded Classes](04-modded-classes.md) | [ホーム](../../README.md) | [1.6: String Operations >>](06-strings.md)
