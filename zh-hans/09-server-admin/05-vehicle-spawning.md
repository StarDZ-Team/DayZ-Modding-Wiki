# Chapter 9.5: 载具与动态事件刷新

[首页](../README.md) | [<< 上一章: 战利品经济](04-loot-economy.md) | [下一章: 玩家出生 >>](06-player-spawning.md)

---

> **摘要:** 载具和动态事件（直升机坠毁、车队、警车）**不使用** `types.xml`。它们使用一个独立的三文件系统：`events.xml` 定义刷新什么以及刷新多少，`cfgeventspawns.xml` 定义刷新位置，`cfgeventgroups.xml` 定义分组编队。本章用原版的真实数值介绍这三个文件。

---

## 目录

- [载具刷新的工作原理](#载具刷新的工作原理)
- [events.xml 载具条目](#eventsxml-载具条目)
- [载具事件字段参考](#载具事件字段参考)
- [cfgeventspawns.xml -- 刷新位置](#cfgeventspawnsxml----刷新位置)
- [直升机坠毁事件](#直升机坠毁事件)
- [军事车队](#军事车队)
- [警车](#警车)
- [cfgeventgroups.xml -- 分组刷新](#cfgeventgroupsxml----分组刷新)
- [cfgeconomycore.xml 载具根类](#cfgeconomycorexml-载具根类)
- [常见错误](#常见错误)

---

## 载具刷新的工作原理

载具**不在** `types.xml` 中定义。如果你将载具类添加到 `types.xml`，它不会刷新。载具使用专用的三文件管线：

1. **`events.xml`** -- 定义每个载具事件：地图上应存在多少辆（nominal）、可以刷新哪些变体（children），以及生命周期和安全半径等行为标志。

2. **`cfgeventspawns.xml`** -- 定义载具事件可以放置实体的物理世界位置。每个事件名称映射到一组包含 x、z 坐标和角度的 `<pos>` 条目。

3. **`cfgeventgroups.xml`** -- 定义分组刷新，其中多个物体以相对位置偏移一起刷新（例如火车残骸）。

CE 读取 `events.xml`，选取需要刷新的事件，在 `cfgeventspawns.xml` 中查找匹配位置，随机选择一个满足 `saferadius` 和 `distanceradius` 约束的位置，然后在该位置刷新一个随机选择的子实体。

这三个文件都位于 `mpmissions/<your_mission>/db/` 中。

---

## events.xml 载具条目

每种原版载具类型都有自己的事件条目。以下是所有的真实数值：

### 民用轿车

```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

### 所有原版载具事件

所有载具事件使用与上面轿车相同的结构。只是数值不同：

| 事件名称 | Nominal | Min | Max | Lifetime | 子项（变体） |
|----------|---------|-----|-----|----------|-------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`、`_Black`、`_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`、`_Blue`、`_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Hatchback02 变体 |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Sedan02 变体 |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | V3S 卡车变体 |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- 刷新较少 |
| `VehicleBoat` | 22 | 18 | 24 | 600 | 船只 -- 最高数量，更长生命周期 |

`VehicleOffroad02` 的 nominal（3）比其他陆地载具（8）低。`VehicleBoat` 同时拥有最高的 nominal（22）和更长的 lifetime（600 vs 300）。

---

## 载具事件字段参考

### 事件级字段

| 字段 | 类型 | 描述 |
|------|------|------|
| `name` | string | 事件标识符。当 `position="fixed"` 时，必须与 `cfgeventspawns.xml` 中的条目匹配。 |
| `nominal` | int | 地图上此事件活动实例的目标数量。 |
| `min` | int | 当数量降至此值以下时，CE 将尝试刷新更多。 |
| `max` | int | 硬上限。CE 永远不会超过此数量。 |
| `lifetime` | int | 重新刷新检查之间的秒数。对于载具，这**不是**载具的持久化生命周期——而是 CE 重新评估是否刷新或清理的间隔。 |
| `restock` | int | 重新刷新尝试之间的最少秒数。0 = 下一循环。 |
| `saferadius` | int | 距任何玩家的最小距离（米），事件才能刷新。防止载具出现在玩家面前。 |
| `distanceradius` | int | 同一事件两个实例之间的最小距离（米）。防止两辆轿车刷新在一起。 |
| `cleanupradius` | int | 如果玩家在此距离（米）内，事件实体不会被清理。 |

### 标志

| 标志 | 值 | 描述 |
|------|------|------|
| `deletable` | 0, 1 | CE 是否可以删除此事件实体。载具使用 0（CE 不可删除）。 |
| `init_random` | 0, 1 | 首次刷新时随机化初始位置。0 = 使用 `cfgeventspawns.xml` 中的固定位置。 |
| `remove_damaged` | 0, 1 | 当实体毁坏时移除。**对载具至关重要** -- 见[常见错误](#常见错误)。 |

### 其他字段

| 字段 | 值 | 描述 |
|------|------|------|
| `position` | `fixed`, `player` | `fixed` = 在 `cfgeventspawns.xml` 的位置刷新。`player` = 相对于玩家位置刷新。 |
| `limit` | `child`, `mixed`, `custom` | `child` = 按子类型执行 min/max。`mixed` = 所有子类型共享 min/max。`custom` = 引擎特定行为。 |
| `active` | 0, 1 | 启用或禁用此事件。0 = 事件被完全跳过。 |

### 子项字段

| 属性 | 描述 |
|------|------|
| `type` | 要刷新的实体类名。 |
| `min` | 此变体的最小实例数。 |
| `max` | 此变体的最大实例数。 |
| `lootmin` | 在实体内部/周围刷新的最少战利品数量。载具为 0（零件来自 `cfgspawnabletypes.xml`）。 |
| `lootmax` | 最多战利品数量。用于直升机坠毁和动态事件，不用于载具。 |

---

## cfgeventspawns.xml -- 刷新位置

此文件将事件名称映射到世界坐标。每个 `<event>` 块包含该事件类型的有效刷新位置列表。当 CE 需要刷新载具时，它从列表中随机选取一个满足 `saferadius` 和 `distanceradius` 约束的位置。

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... 更多位置 ... -->
</event>
```

每个 `<pos>` 有三个属性：

| 属性 | 描述 |
|------|------|
| `x` | 世界 X 坐标（地图上的东西方向位置）。 |
| `z` | 世界 Z 坐标（地图上的南北方向位置）。 |
| `a` | 角度，单位为度（0-360）。载具刷新时面朝的方向。 |

**关键规则：**

- 如果事件在 `cfgeventspawns.xml` 中没有匹配的 `<event>` 块，无论 `events.xml` 如何配置，它都**不会刷新**。
- 你需要的 `<pos>` 条目至少与 `nominal` 值一样多。如果设置 `nominal=8` 但只有 3 个位置，则只能刷新 3 辆。
- 位置应在道路或平坦地面上。在建筑内部或陡峭地形上的位置会导致载具刷新时被埋没或翻倒。
- `a`（角度）值决定载具的朝向。将其与道路方向对齐以获得自然的刷新效果。

---

## 直升机坠毁事件

直升机坠毁是动态事件，刷新一个残骸并附带军事战利品和周围的感染者。它们使用 `<secondary>` 标签定义坠毁点周围的环境僵尸刷新。

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>1</min>
    <max>3</max>
    <lifetime>2100</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="15" lootmin="10" max="3" min="1" type="Wreck_UH1Y"/>
    </children>
</event>
```

### 与载具事件的主要区别

- **`<secondary>InfectedArmy</secondary>`** -- 在坠毁点周围刷新军事僵尸。此标签引用一个感染者刷新组，CE 将其放置在附近。
- **`lootmin="10"` / `lootmax="15"`** -- 残骸刷新时带有 10-15 个动态事件战利品。这些是 `types.xml` 中标记为 `deloot="1"` 的物品（军事装备、稀有武器）。
- **`lifetime=2100`** -- 坠毁点持续 35 分钟，之后 CE 清理它并在其他地方刷新新的。
- **`saferadius=1000`** -- 坠毁点永远不会出现在距玩家 1 公里以内。
- **`remove_damaged=0`** -- 残骸本身就是"损坏的"，所以此值必须为 0，否则它会立即被清理。

---

## 军事车队

军事车队是静态的损坏载具组，附带军事战利品和感染者守卫。

```xml
<event name="StaticMilitaryConvoy">
    <nominal>5</nominal>
    <min>3</min>
    <max>5</max>
    <lifetime>1800</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="5" min="3" type="Wreck_V3S"/>
    </children>
</event>
```

车队的工作方式与直升机坠毁完全相同：`<secondary>` 标签在现场周围刷新 `InfectedArmy`，`deloot="1"` 的战利品物品出现在残骸上。设置 `nominal=5` 时，地图上最多同时存在 5 个车队点。每个持续 1800 秒（30 分钟），之后循环到新位置。

---

## 警车

警车事件刷新损坏的警用载具，附近有警察类型的感染者。它们**默认禁用**。

```xml
<event name="StaticPoliceCar">
    <nominal>10</nominal>
    <min>5</min>
    <max>10</max>
    <lifetime>2500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>200</distanceradius>
    <cleanupradius>100</cleanupradius>
    <secondary>InfectedPoliceHard</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>0</active>
    <children>
        <child lootmax="5" lootmin="3" max="10" min="5" type="Wreck_PoliceCar"/>
    </children>
</event>
```

**`active=0`** 表示此事件默认禁用——改为 `1` 即可启用。`<secondary>InfectedPoliceHard</secondary>` 标签刷新强化变体的警察僵尸（比普通感染者更强）。设置 `nominal=10` 和 `saferadius=500`，警车比直升机坠毁更多但价值更低。

---

## cfgeventgroups.xml -- 分组刷新

此文件定义多个物体以相对位置偏移一起刷新的事件。最常见的用途是废弃火车。

```xml
<event name="Train_Abandoned_Cherno">
    <children>
        <child type="Land_Train_Wagon_Tanker_Blue" x="0" z="0" a="0"/>
        <child type="Land_Train_Wagon_Box_Brown" x="0" z="15" a="0"/>
        <child type="Land_Train_Wagon_Flatbed_Green" x="0" z="30" a="0"/>
        <child type="Land_Train_Engine_Blue" x="0" z="45" a="0"/>
    </children>
</event>
```

第一个子项放置在 `cfgeventspawns.xml` 的位置上。后续子项相对于该原点按其 `x`、`z`、`a` 值偏移。在此示例中，火车车厢沿 z 轴间隔 15 米。

组中每个 `<child>` 有：

| 属性 | 描述 |
|------|------|
| `type` | 要刷新的物体类名。 |
| `x` | 相对于组原点的 X 偏移（米）。 |
| `z` | 相对于组原点的 Z 偏移（米）。 |
| `a` | 相对于组原点的角度偏移（度）。 |

组事件本身仍需要在 `events.xml` 中有一个匹配条目来控制 nominal 数量、生命周期和活动状态。

---

## cfgeconomycore.xml 载具根类

为了让 CE 将载具识别为可追踪的实体，它们必须在 `cfgeconomycore.xml` 中有根类声明：

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** 是 DayZ 中所有陆地载具的基类。
- **`BoatScript`** 是所有船只的基类。
- `act="car"` 属性告诉 CE 以载具特定的行为处理这些实体（持久化、基于事件的刷新）。

没有这些根类条目，CE 就不会追踪或管理载具实例。如果你添加的 mod 载具继承自不同的基类，你可能需要在此添加其根类。

---

## 常见错误

这些是服务器管理员最常遇到的载具刷新问题。

### 将载具放入 types.xml

**问题：** 你在 `types.xml` 中添加 `CivilianSedan` 并设置 nominal 为 10。没有轿车刷新。

**解决方法：** 从 `types.xml` 中移除载具。在 `events.xml` 中添加或编辑载具事件及适当的子项，并确保 `cfgeventspawns.xml` 中有匹配的刷新位置。载具使用事件系统，而不是物品刷新系统。

### cfgeventspawns.xml 中没有匹配的刷新位置

**问题：** 你在 `events.xml` 中创建了新的载具事件，但载具从未出现。

**解决方法：** 在 `cfgeventspawns.xml` 中添加匹配的 `<event name="YourEventName">` 块并包含足够的 `<pos>` 条目。两个文件中的事件 `name` 必须完全匹配。你需要的位置至少与 `nominal` 值一样多。

### 为可驾驶载具设置 remove_damaged=0

**问题：** 你为载具事件设置 `remove_damaged="0"`。随着时间推移，服务器充满了永远不会消失的毁坏载具，占用刷新位置并降低性能。

**解决方法：** 所有可驾驶载具（轿车、卡车、掀背车、船只）保持 `remove_damaged="1"`。这确保载具被摧毁时，CE 移除它并刷新一辆新的。只有对残骸物体（直升机坠毁、车队）设置 `remove_damaged="0"`，因为它们设计上就是损坏的。

### 忘记设置 active=1

**问题：** 你配置了载具事件但它从未刷新。

**解决方法：** 检查 `<active>` 标签。如果设为 `0`，事件被禁用。一些原版事件如 `StaticPoliceCar` 出厂时就是 `active=0`。设为 `1` 以启用刷新。

### 刷新位置不够 nominal 数量使用

**问题：** 你为载具事件设置 `nominal=15` 但 `cfgeventspawns.xml` 中只有 6 个位置。只有 6 辆载具会刷新。

**解决方法：** 添加更多 `<pos>` 条目。作为规则，包含至少 2-3 倍于 nominal 值的位置，以给 CE 足够的选项来满足 `saferadius` 和 `distanceradius` 约束。

### 载具刷新在建筑内部或地下

**问题：** 载具刷新时嵌入建筑或埋在地形中。

**解决方法：** 检查 `cfgeventspawns.xml` 中的 `<pos>` 坐标。在将位置添加到文件之前，使用管理员传送在游戏中测试位置。位置应在平坦的道路或空旷地面上，角度（`a`）应与道路方向对齐。

---

[首页](../README.md) | [<< 上一章: 战利品经济](04-loot-economy.md) | [下一章: 玩家出生 >>](06-player-spawning.md)
