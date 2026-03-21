# Шпаргалка по Enforce Script

> Краткая справка на одной странице по Enforce Script для DayZ. Добавьте в закладки.

---

## Типы

| Тип | Описание | Значение по умолчанию | Пример |
|-----|----------|----------------------|--------|
| `int` | 32-битное знаковое целое | `0` | `int x = 42;` |
| `float` | 32-битное с плавающей точкой | `0.0` | `float f = 3.14;` |
| `bool` | Логический | `false` | `bool b = true;` |
| `string` | Неизменяемый тип-значение | `""` | `string s = "hello";` |
| `vector` | 3-компонентный float (x,y,z) | `"0 0 0"` | `vector v = "1 2 3";` |
| `typename` | Ссылка на тип | `null` | `typename t = PlayerBase;` |
| `Class` | Корень всех ссылочных типов | `null` | — |
| `void` | Нет возвращаемого значения | — | — |

**Пределы:** `int.MAX` = 2147483647, `int.MIN` = -2147483648, `float.MAX`, `float.MIN`

---

## Методы Array (`array<T>`)

| Метод | Возвращает | Примечания |
|-------|-----------|------------|
| `Insert(item)` | `int` (индекс) | Добавить в конец |
| `InsertAt(item, idx)` | `void` | Вставить на позицию |
| `Get(idx)` / `arr[idx]` | `T` | Доступ по индексу |
| `Set(idx, item)` | `void` | Замена по индексу |
| `Find(item)` | `int` | Индекс или -1 |
| `Count()` | `int` | Количество элементов |
| `IsValidIndex(idx)` | `bool` | Проверка границ |
| `Remove(idx)` | `void` | **Неупорядоченное** (меняет местами с последним!) |
| `RemoveOrdered(idx)` | `void` | Сохраняет порядок |
| `RemoveItem(item)` | `void` | Поиск + удаление (упорядоченное) |
| `Clear()` | `void` | Удалить все |
| `Sort()` / `Sort(true)` | `void` | По возрастанию / по убыванию |
| `ShuffleArray()` | `void` | Перемешать |
| `Invert()` | `void` | Перевернуть |
| `GetRandomElement()` | `T` | Случайный элемент |
| `InsertAll(other)` | `void` | Добавить все из другого |
| `Copy(other)` | `void` | Заменить копией |
| `Resize(n)` | `void` | Изменить размер (заполняет значениями по умолчанию) |
| `Reserve(n)` | `void` | Предварительно выделить ёмкость |

**Typedefs:** `TStringArray`, `TIntArray`, `TFloatArray`, `TBoolArray`, `TVectorArray`

---

## Методы Map (`map<K,V>`)

| Метод | Возвращает | Примечания |
|-------|-----------|------------|
| `Insert(key, val)` | `bool` | Добавить новый |
| `Set(key, val)` | `void` | Вставить или обновить |
| `Get(key)` | `V` | Возвращает значение по умолчанию, если не найден |
| `Find(key, out val)` | `bool` | Безопасное получение |
| `Contains(key)` | `bool` | Проверка наличия |
| `Remove(key)` | `void` | Удалить по ключу |
| `Count()` | `int` | Количество записей |
| `GetKey(idx)` | `K` | Ключ по индексу (O(n)) |
| `GetElement(idx)` | `V` | Значение по индексу (O(n)) |
| `GetKeyArray()` | `array<K>` | Все ключи |
| `GetValueArray()` | `array<V>` | Все значения |
| `Clear()` | `void` | Удалить все |

---

## Методы Set (`set<T>`)

| Метод | Возвращает |
|-------|-----------|
| `Insert(item)` | `int` (индекс) |
| `Find(item)` | `int` (индекс или -1) |
| `Get(idx)` | `T` |
| `Remove(idx)` | `void` |
| `RemoveItem(item)` | `void` |
| `Count()` | `int` |
| `Clear()` | `void` |

---

## Синтаксис классов

```c
class MyClass extends BaseClass
{
    protected int m_Value;                  // field
    private ref array<string> m_List;       // owned ref

    void MyClass() { m_List = new array<string>; }  // constructor
    void ~MyClass() { }                              // destructor

    override void OnInit() { super.OnInit(); }       // override
    static int GetCount() { return 0; }              // static method
};
```

**Доступ:** `private` | `protected` | (public по умолчанию)
**Модификаторы:** `static` | `override` | `ref` | `const` | `out` | `notnull`
**Modded:** `modded class MissionServer { override void OnInit() { super.OnInit(); } }`

---

## Управление потоком

```c
// if / else if / else
if (a > 0) { } else if (a == 0) { } else { }

// for
for (int i = 0; i < count; i++) { }

// foreach (значение)
foreach (string item : myArray) { }

// foreach (индекс + значение)
foreach (int i, string item : myArray) { }

// foreach (map: ключ + значение)
foreach (string key, int val : myMap) { }

// while
while (condition) { }

// switch (БЕЗ проваливания!)
switch (val) { case 0: Print("zero"); break; default: break; }
```

---

## Методы строк

| Метод | Возвращает | Пример |
|-------|-----------|--------|
| `s.Length()` | `int` | `"hello".Length()` = 5 |
| `s.Substring(start, len)` | `string` | `"hello".Substring(1,3)` = `"ell"` |
| `s.IndexOf(sub)` | `int` | -1 если не найдено |
| `s.LastIndexOf(sub)` | `int` | Поиск с конца |
| `s.Contains(sub)` | `bool` | |
| `s.Replace(old, new)` | `int` | Изменяет на месте, возвращает количество |
| `s.ToLower()` | `void` | **На месте!** |
| `s.ToUpper()` | `void` | **На месте!** |
| `s.TrimInPlace()` | `void` | **На месте!** |
| `s.Split(delim, out arr)` | `void` | Разделяет в TStringArray |
| `s.Get(idx)` | `string` | Один символ |
| `s.Set(idx, ch)` | `void` | Замена символа |
| `s.ToInt()` | `int` | Парсинг int |
| `s.ToFloat()` | `float` | Парсинг float |
| `s.ToVector()` | `vector` | Парсинг `"1 2 3"` |
| `string.Format(fmt, ...)` | `string` | Заполнители `%1`..`%9` |
| `string.Join(sep, arr)` | `string` | Объединить элементы array |

---

## Математические методы

| Метод | Описание |
|-------|----------|
| `Math.RandomInt(min, max)` | `[min, max)` max не включён |
| `Math.RandomIntInclusive(min, max)` | `[min, max]` |
| `Math.RandomFloat01()` | `[0, 1]` |
| `Math.RandomBool()` | Случайное true/false |
| `Math.Round(f)` / `Floor(f)` / `Ceil(f)` | Округление |
| `Math.AbsFloat(f)` / `AbsInt(i)` | Абсолютное значение |
| `Math.Clamp(val, min, max)` | Ограничить диапазоном |
| `Math.Min(a, b)` / `Max(a, b)` | Минимум/максимум |
| `Math.Lerp(a, b, t)` | Линейная интерполяция |
| `Math.InverseLerp(a, b, val)` | Обратная интерполяция |
| `Math.Pow(base, exp)` / `Sqrt(f)` | Степень/корень |
| `Math.Sin(r)` / `Cos(r)` / `Tan(r)` | Тригонометрия (радианы) |
| `Math.Atan2(y, x)` | Угол по компонентам |
| `Math.NormalizeAngle(deg)` | Привести к 0-360 |
| `Math.SqrFloat(f)` / `SqrInt(i)` | Квадрат |

**Константы:** `Math.PI`, `Math.PI2`, `Math.PI_HALF`, `Math.DEG2RAD`, `Math.RAD2DEG`

**Vector:** `vector.Distance(a,b)`, `vector.DistanceSq(a,b)`, `vector.Direction(a,b)`, `vector.Dot(a,b)`, `vector.Lerp(a,b,t)`, `v.Length()`, `v.Normalized()`

---

## Распространённые паттерны

### Безопасное приведение типа

```c
PlayerBase player;
if (Class.CastTo(player, obj))
{
    player.DoSomething();
}
```

### Инлайн-приведение

```c
PlayerBase player = PlayerBase.Cast(obj);
if (player) player.DoSomething();
```

### Проверка на null

```c
if (!player) return;
if (!player.GetIdentity()) return;
string name = player.GetIdentity().GetName();
```

### Проверка IsAlive (требуется EntityAI)

```c
EntityAI eai;
if (Class.CastTo(eai, obj) && eai.IsAlive()) { }
```

### Итерация по Map через foreach

```c
foreach (string key, int value : myMap)
{
    Print(key + " = " + value.ToString());
}
```

### Преобразование Enum

```c
string name = typename.EnumToString(EDamageState, state);
int val; typename.StringToEnum(EDamageState, "RUINED", val);
```

### Битовые флаги

```c
int flags = FLAG_A | FLAG_B;       // объединить
if (flags & FLAG_A) { }           // проверить
flags = flags & ~FLAG_B;          // убрать
```

---

## Чего НЕ существует

| Отсутствующая возможность | Обходное решение |
|--------------------------|-----------------|
| Тернарный `? :` | `if/else` |
| `do...while` | `while(true) { ... break; }` |
| `try/catch` | Защитные проверки + ранний return |
| Множественное наследование | Одиночное + композиция |
| Перегрузка операторов | Именованные методы (кроме `[]` через Get/Set) |
| Лямбды | Именованные методы |
| `nullptr` | `null` / `NULL` |
| `\\` / `\"` в строках | Избегать (CParser ломается) |
| `#include` | config.cpp `files[]` |
| Пространства имён | Префиксы имён (`My`, `VPP_`) |
| Интерфейсы / abstract | Пустые базовые методы |
| Проваливание switch | Каждый case независим |
| `#define` со значениями | Используйте `const` |
| Выражения в параметрах по умолчанию | Только литералы/NULL |
| Вариативные параметры | `string.Format` или arrays |
| Переобъявление переменных в else-if | Уникальные имена для каждой ветви |

---

## Создание виджетов (программное)

```c
// Get workspace
WorkspaceWidget ws = GetGame().GetWorkspace();

// Create from layout
Widget root = ws.CreateWidgets("MyMod/gui/layouts/MyPanel.layout");

// Find child widget
TextWidget title = TextWidget.Cast(root.FindAnyWidget("TitleText"));
if (title) title.SetText("Hello World");

// Show/hide
root.Show(true);
root.Show(false);
```

---

## Паттерн RPC

**Регистрация (сервер):**
```c
// In 3_Game or 4_World init:
GetGame().RPCSingleParam(null, MY_RPC_ID, null, true, identity);  // Engine RPC

// Or with string-routed RPC (MyRPC / CF):
GetRPCManager().AddRPC("MyMod", "RPC_Handler", this, 2);  // CF
MyRPC.Register("MyMod", "MyRoute", this, MyRPCSide.SERVER);  // MyMod
```

**Отправка (клиент на сервер):**
```c
Param2<string, int> data = new Param2<string, int>("itemName", 5);
GetGame().RPCSingleParam(null, MY_RPC_ID, data, true);
```

**Получение (обработчик на сервере):**
```c
void RPC_Handler(CallType type, ParamsReadContext ctx, PlayerIdentity sender, Object target)
{
    if (type != CallType.Server) return;
    if (!sender) return;

    Param2<string, int> data;
    if (!ctx.Read(data)) return;

    string itemName = data.param1;
    int quantity = data.param2;
    // Process...
}
```

---

## Обработка ошибок

```c
ErrorEx("message");                              // Default ERROR severity
ErrorEx("info", ErrorExSeverity.INFO);           // Info
ErrorEx("warning", ErrorExSeverity.WARNING);     // Warning
Print("debug output");                           // Script log
string stack = DumpStackString();                // Get call stack
```

---

## Файловый ввод-вывод

```c
// Paths: "$profile:", "$saves:", "$mission:", "$CurrentDir:"
bool exists = FileExist("$profile:MyMod/config.json");
MakeDirectory("$profile:MyMod");

// JSON
MyConfig cfg = new MyConfig();
JsonFileLoader<MyConfig>.JsonLoadFile(path, cfg);  // Returns VOID!
JsonFileLoader<MyConfig>.JsonSaveFile(path, cfg);

// Raw file
FileHandle fh = OpenFile(path, FileMode.WRITE);
if (fh != 0) { FPrintln(fh, "line"); CloseFile(fh); }
```

---

## Создание объектов

```c
// Basic
Object obj = GetGame().CreateObject("AK101", pos, false, false, true);

// With flags
Object obj = GetGame().CreateObjectEx("Barrel_Green", pos, ECE_PLACE_ON_SURFACE);

// In player inventory
player.GetInventory().CreateInInventory("BandageDressing");

// As attachment
weapon.GetInventory().CreateAttachment("ACOGOptic");

// Delete
GetGame().ObjectDelete(obj);
```

---

## Основные глобальные функции

```c
GetGame()                          // CGame instance
GetGame().GetPlayer()              // Local player (CLIENT only, null on server!)
GetGame().GetPlayers(out arr)      // All players (server)
GetGame().GetWorld()               // World instance
GetGame().GetTickTime()            // Server time (float)
GetGame().GetWorkspace()           // UI workspace
GetGame().SurfaceY(x, z)          // Terrain height
GetGame().IsServer()               // true on server
GetGame().IsClient()               // true on client
GetGame().IsMultiplayer()          // true if multiplayer
```

---

*Полная документация: [Вики по моддингу DayZ](../README.md) | [Ловушки](01-enforce-script/12-gotchas.md) | [Обработка ошибок](01-enforce-script/11-error-handling.md)*
