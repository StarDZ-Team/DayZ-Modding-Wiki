# Chapter 9.7: 世界状态与持久化

[首页](../README.md) | [<< 上一章: 玩家出生](06-player-spawning.md) | [下一章: 性能调优 >>](08-performance.md)

DayZ 的持久化系统在重启之间保持世界的存活状态。了解其工作原理可以帮助你管理基地、规划清档和避免数据损坏。

## 目录

- [持久化的工作原理](#持久化的工作原理)
- [storage_1/ 目录](#storage_1-目录)
- [globals.xml 持久化参数](#globalsxml-持久化参数)
- [领地旗帜系统](#领地旗帜系统)
- [囤积物品](#囤积物品)
- [cfggameplay.json 持久化设置](#cfggameplayjson-持久化设置)
- [服务器清档流程](#服务器清档流程)
- [备份策略](#备份策略)
- [常见错误](#常见错误)

---

## 持久化的工作原理

DayZ 将世界状态存储在服务器配置文件夹内的 `storage_1/` 目录中。循环过程很简单：

1. 服务器定期保存世界状态（默认每约 30 分钟一次），并在正常关闭时保存。
2. 重启时，服务器读取 `storage_1/` 并恢复所有持久化的物体——载具、基地、帐篷、桶、玩家背包。
3. 没有持久化的物品（大多数地面战利品）由中央经济系统在每次重启时重新生成。

如果启动时 `storage_1/` 不存在，服务器会创建一个全新的世界，没有玩家数据也没有已建造的建筑。

---

## storage_1/ 目录

你的服务器配置文件夹包含 `storage_1/`，其中有以下子目录和文件：

| 路径 | 内容 |
|------|------|
| `data/` | 保存世界物体的二进制文件——基地部件、放置的物品、载具位置 |
| `players/` | 按 SteamID64 索引的每玩家 **.save** 文件。每个文件存储位置、背包、血量、状态效果 |
| `snapshot/` | 保存操作期间使用的世界状态快照 |
| `events.bin` / `events.xy` | 动态事件状态——追踪直升机坠毁位置、车队位置和其他已刷新的事件 |

`data/` 文件夹是持久化的主体。它包含服务器在启动时读取以重建世界的序列化物体数据。

---

## globals.xml 持久化参数

你任务文件夹中的 **globals.xml** 文件控制清理计时器和旗帜行为。以下是与持久化相关的值：

```xml
<!-- 领地旗帜刷新 -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 天（秒） -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 天（秒） -->

<!-- 清理计时器 -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- 默认清理时间（秒） -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- 死亡玩家尸体：1 小时 -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- 死亡动物：20 分钟 -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- 死亡僵尸：5.5 分钟 -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- 毁坏物品：5.5 分钟 -->

<!-- 清理行为 -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- 每个周期清理的最大物品数 -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- 在玩家 100 米内跳过清理 -->
```

`CleanupAvoidance` 值防止服务器清除活跃玩家附近的物体。如果死亡尸体在任何玩家 100 米范围内，它会一直保留直到玩家离开或计时器重置。

---

## 领地旗帜系统

领地旗帜是 DayZ 中基地持久化的核心。以下是两个关键值的交互方式：

- **FlagRefreshFrequency**（`432000` 秒 = 5 天）— 你必须与旗帜交互以保持其活跃的频率。走到旗帜前使用"刷新"操作。
- **FlagRefreshMaxDuration**（`3456000` 秒 = 40 天）— 最大累积保护时间。每次刷新最多增加 FlagRefreshFrequency 等值的时间，但总计不能超过此上限。

当旗帜的计时器耗尽时：

1. 旗帜本身变为可清理状态。
2. 所有附属于该旗帜的基地建筑部件失去持久化保护。
3. 在下一个清理周期中，未受保护的部件开始消失。

如果降低 FlagRefreshFrequency，玩家必须更频繁地访问基地。如果提高 FlagRefreshMaxDuration，基地在两次访问之间存活更长时间。根据你的服务器游戏风格同时调整这两个值。

---

## 囤积物品

在 **cfgspawnabletypes.xml** 中，某些容器被标记为 `<hoarder/>`。这将它们标记为可藏匿的物品，在中央经济系统中计入每玩家的存储限制。

原版的囤积物品有：

| 物品 | 类型 |
|------|------|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | 存储桶 |
| CarTent, LargeTent, MediumTent, PartyTent | 帐篷 |
| SeaChest | 水下存储 |
| SmallProtectorCase | 小型可锁箱子 |
| UndergroundStash | 地下藏匿点 |
| WoodenCrate | 可制作的存储箱 |

来自 **cfgspawnabletypes.xml** 的示例：

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

服务器追踪每个玩家放置了多少囤积物品。当达到限制时，新的放置要么失败，要么最旧的物品消失（取决于服务器配置）。

---

## cfggameplay.json 持久化设置

你任务文件夹中的 **cfggameplay.json** 文件包含影响基地和容器耐久性的设置：

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| 设置 | 默认值 | 效果 |
|------|--------|------|
| `disableBaseDamage` | `false` | 设为 `true` 时，基地建筑部件（墙壁、大门、瞭望塔）不可被损坏。这实际上禁用了突袭。 |
| `disableContainerDamage` | `false` | 设为 `true` 时，存储容器（帐篷、桶、箱子）不会受到伤害。内部物品保持安全。 |

将两者都设为 `true` 可创建 PvE 友好的服务器，基地和存储不可摧毁。大多数 PvP 服务器保持两者为 `false`。

---

## 服务器清档流程

有四种类型的清档，每种针对 `storage_1/` 的不同部分。**在执行任何清档前务必停止服务器。**

### 完全清档

删除整个 `storage_1/` 文件夹。服务器在下次启动时创建全新世界。所有基地、载具、帐篷、玩家数据和事件状态都会消失。

### 经济清档（保留玩家）

删除 `storage_1/data/` 但保留 `storage_1/players/`。玩家保留角色和背包，但所有放置的物体（基地、帐篷、桶、载具）被移除。

### 玩家清档（保留世界）

删除 `storage_1/players/`。所有玩家角色重置为新生。基地和放置的物体保留在世界中。

### 天气/事件重置

从 `storage_1/` 中删除 `events.bin` 或 `events.xy`。这会重置动态事件位置（直升机坠毁、车队）。服务器在下次启动时生成新的事件位置。

---

## 备份策略

持久化数据一旦丢失就无法恢复。遵循以下做法：

- **在停止状态下备份。** 在服务器未运行时复制整个 `storage_1/` 文件夹。在运行时复制可能捕获到不完整或损坏的状态。
- **在重启前安排备份。** 如果你运行自动重启（每 4-6 小时），在重启脚本中添加一个备份步骤，在服务器进程启动前复制 `storage_1/`。
- **保留多个版本。** 轮换备份以保持至少 3 个最近的副本。如果最新的备份已损坏，你可以回滚到更早的版本。
- **异机存储。** 将备份复制到单独的驱动器或云存储。服务器机器的硬盘故障会同时带走位于同一驱动器上的备份。

一个最简备份脚本（在服务器启动前运行）：

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## 常见错误

这些是服务器管理社区中反复出现的问题：

| 错误 | 后果 | 预防措施 |
|------|------|----------|
| 服务器运行时删除 `storage_1/` | 数据损坏。服务器写入不再存在的文件，导致崩溃或下次启动时状态不完整。 | 始终先停止服务器。 |
| 清档前不备份 | 如果意外删除了错误的文件夹或清档出了问题，将无法恢复。 | 每次清档前备份 `storage_1/`。 |
| 将天气重置与完全清档混淆 | 删除 `events.xy` 只会重置动态事件位置。它不会重置战利品、基地或玩家。 | 了解哪些文件控制什么（见上面的目录表）。 |
| 旗帜未及时刷新 | 40 天（FlagRefreshMaxDuration）后，旗帜过期，所有附属的基地部件变为可清理状态。玩家失去整个基地。 | 提醒玩家刷新间隔。在低人口服务器上降低 FlagRefreshMaxDuration。 |
| 服务器运行时编辑 globals.xml | 更改直到重启才会生效。更糟的是，服务器可能在关闭时覆盖你的编辑。 | 只在服务器停止时编辑配置文件。 |

---

[首页](../README.md) | [<< 上一章: 玩家出生](06-player-spawning.md) | [下一章: 性能调优 >>](08-performance.md)
