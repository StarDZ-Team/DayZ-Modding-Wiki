# Chapter 9.3: serverDZ.cfg 完整参考

[首页](../README.md) | [<< 上一章: 目录结构](02-directory-structure.md) | **serverDZ.cfg 参考** | [下一章: 战利品经济深入解析 >>](04-loot-economy.md)

---

> **摘要:** `serverDZ.cfg` 中每个参数的文档，包含其用途、有效值和默认行为。此文件控制服务器身份、网络设置、游戏规则、时间加速和任务选择。

---

## 目录

- [文件格式](#文件格式)
- [服务器身份](#服务器身份)
- [网络与安全](#网络与安全)
- [游戏规则](#游戏规则)
- [时间与天气](#时间与天气)
- [性能与登录队列](#性能与登录队列)
- [持久化与实例](#持久化与实例)
- [任务选择](#任务选择)
- [完整示例文件](#完整示例文件)
- [覆盖配置的启动参数](#覆盖配置的启动参数)

---

## 文件格式

`serverDZ.cfg` 使用 Bohemia 的配置格式（类似 C 语言）。规则如下：

- 每行参数赋值以**分号** `;` 结尾
- 字符串用**双引号** `""` 括起
- 注释使用 `//` 表示单行注释
- `class Missions` 块使用花括号 `{}`，以 `};` 结尾
- 文件必须是 UTF-8 或 ANSI 编码 -- 不带 BOM

缺少分号会导致服务器静默失败或忽略后续参数。

---

## 服务器身份

```cpp
hostname = "My DayZ Server";         // 浏览器中显示的服务器名称
password = "";                       // 连接密码（空 = 公开）
passwordAdmin = "";                  // 通过游戏内控制台登录管理员的密码
description = "";                    // 服务器浏览器详情中显示的描述
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `hostname` | string | `""` | 在服务器浏览器中显示。最多约 100 个字符。 |
| `password` | string | `""` | 留空表示公开服务器。玩家必须输入此密码才能加入。 |
| `passwordAdmin` | string | `""` | 与游戏内 `#login` 命令配合使用。**每台服务器都应设置此项。** |
| `description` | string | `""` | 不支持多行描述。请保持简短。 |

---

## 网络与安全

```cpp
maxPlayers = 60;                     // 最大玩家数
verifySignatures = 2;                // PBO 签名验证（仅支持 2）
forceSameBuild = 1;                  // 要求客户端/服务器版本匹配
enableWhitelist = 0;                 // 启用/禁用白名单
disableVoN = 0;                      // 禁用语音通信
vonCodecQuality = 20;               // VoN 音频质量（0-30）
guaranteedUpdates = 1;               // 网络协议（始终使用 1）
```

| 参数 | 类型 | 有效值 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `maxPlayers` | int | 1-60 | 60 | 影响内存使用。每个玩家增加约 50-100 MB。 |
| `verifySignatures` | int | 2 | 2 | 仅支持值 2。根据 `.bisign` 密钥验证 PBO 文件。 |
| `forceSameBuild` | int | 0, 1 | 1 | 设为 1 时，客户端必须与服务器的可执行文件版本完全匹配。始终保持为 1。 |
| `enableWhitelist` | int | 0, 1 | 0 | 设为 1 时，只有 `whitelist.txt` 中列出的 Steam64 ID 可以连接。 |
| `disableVoN` | int | 0, 1 | 0 | 设为 1 可完全禁用游戏内语音聊天。 |
| `vonCodecQuality` | int | 0-30 | 20 | 值越高音质越好，但带宽消耗越大。20 是一个较好的平衡点。 |
| `guaranteedUpdates` | int | 1 | 1 | 网络协议设置。始终使用 1。 |

### 分片 ID

```cpp
shardId = "123abc";                  // 六个字母数字字符，用于私有分片
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `shardId` | string | `""` | 用于私有 Hive 服务器。具有相同 `shardId` 的服务器共享角色数据。留空表示公共 Hive。 |

---

## 游戏规则

```cpp
disable3rdPerson = 0;               // 禁用第三人称视角
disableCrosshair = 0;               // 禁用准星
disablePersonalLight = 1;           // 禁用环境玩家灯光
lightingConfig = 0;                 // 夜间亮度（0 = 较亮，1 = 较暗）
```

| 参数 | 类型 | 有效值 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `disable3rdPerson` | int | 0, 1 | 0 | 设为 1 强制第一人称视角。这是最常见的"硬核"设置。 |
| `disableCrosshair` | int | 0, 1 | 0 | 设为 1 移除准星。通常与 `disable3rdPerson=1` 配合使用。 |
| `disablePersonalLight` | int | 0, 1 | 1 | "个人灯光"是夜间玩家周围的微弱光晕。大多数服务器出于真实性考虑禁用它（值为 1）。 |
| `lightingConfig` | int | 0, 1 | 0 | 0 = 较亮的夜晚（可见月光）。1 = 漆黑夜晚（需要手电筒/夜视仪）。 |

---

## 时间与天气

```cpp
serverTime = "SystemTime";                 // 初始时间
serverTimeAcceleration = 12;               // 时间速度倍率（0-24）
serverNightTimeAcceleration = 1;           // 夜间时间速度倍率（0.1-64）
serverTimePersistent = 0;                  // 在重启之间保存时间
```

| 参数 | 类型 | 有效值 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `serverTime` | string | `"SystemTime"` 或 `"YYYY/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` 使用机器的本地时钟。设置固定时间如 `"2024/9/15/12/0"` 可实现永久白天服务器。 |
| `serverTimeAcceleration` | int | 0-24 | 12 | 游戏内时间倍率。设为 12 时，完整的 24 小时周期需要 2 个现实小时。设为 1 时为实时。设为 24 时，一天在 1 小时内过完。 |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | 与 `serverTimeAcceleration` 相乘。在值为 4 且加速为 12 时，夜晚以 48 倍速度流逝（非常短的夜晚）。 |
| `serverTimePersistent` | int | 0, 1 | 0 | 设为 1 时，服务器将游戏内时钟保存到磁盘，重启后从该时间恢复。设为 0 时，每次重启都重置为 `serverTime`。 |

### 常见时间配置

**永久白天：**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**快速昼夜循环（2 小时白天，短夜晚）：**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**实时昼夜：**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## 性能与登录队列

```cpp
loginQueueConcurrentPlayers = 5;     // 登录时同时处理的玩家数
loginQueueMaxPlayers = 500;          // 最大登录队列大小
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `loginQueueConcurrentPlayers` | int | 5 | 同时加载的玩家数量。较低的值减少重启后的服务器负载峰值。如果你的硬件性能强劲且玩家抱怨队列时间过长，可提高到 10-15。 |
| `loginQueueMaxPlayers` | int | 500 | 如果已有这么多玩家在排队，新连接将被拒绝。500 对大多数服务器来说足够了。 |

---

## 持久化与实例

```cpp
instanceId = 1;                      // 服务器实例标识符
storageAutoFix = 1;                  // 自动修复损坏的持久化文件
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `instanceId` | int | 1 | 标识服务器实例。持久化数据存储在 `storage_<instanceId>/` 中。如果在同一台机器上运行多个服务器，请为每个服务器分配不同的 `instanceId`。 |
| `storageAutoFix` | int | 1 | 设为 1 时，服务器在启动时检查持久化文件，并用空文件替换损坏的文件。始终保持为 1。 |

---

## 任务选择

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

`template` 值必须与 `mpmissions/` 内的文件夹名称完全匹配。可用的原版任务：

| 模板 | 地图 | 需要 DLC |
|------|------|:---:|
| `dayzOffline.chernarusplus` | 切尔诺鲁斯 | 否 |
| `dayzOffline.enoch` | 利沃尼亚 | 是 |
| `dayzOffline.sakhal` | 萨哈林 | 是 |

自定义任务（例如来自 mod 或社区地图的任务）使用自己的模板名称。文件夹必须存在于 `mpmissions/` 中。

---

## 完整示例文件

以下是包含所有参数的完整默认 `serverDZ.cfg`：

```cpp
hostname = "EXAMPLE NAME";              // 服务器名称
password = "";                          // 连接服务器的密码
passwordAdmin = "";                     // 成为服务器管理员的密码

description = "";                       // 服务器浏览器描述

enableWhitelist = 0;                    // 启用/禁用白名单（值 0-1）

maxPlayers = 60;                        // 最大玩家数

verifySignatures = 2;                   // 根据 .bisign 文件验证 .pbo（仅支持 2）
forceSameBuild = 1;                     // 要求客户端/服务器版本匹配（值 0-1）

disableVoN = 0;                         // 启用/禁用语音通信（值 0-1）
vonCodecQuality = 20;                   // 语音通信编解码器质量（值 0-30）

shardId = "123abc";                     // 六个字母数字字符，用于私有分片

disable3rdPerson = 0;                   // 切换第三人称视角（值 0-1）
disableCrosshair = 0;                   // 切换准星（值 0-1）

disablePersonalLight = 1;              // 为所有客户端禁用个人灯光
lightingConfig = 0;                     // 0 表示较亮夜晚，1 表示较暗夜晚

serverTime = "SystemTime";             // 初始游戏内时间（"SystemTime" 或 "YYYY/MM/DD/HH/MM"）
serverTimeAcceleration = 12;           // 时间速度倍率（0-24）
serverNightTimeAcceleration = 1;       // 夜间时间速度倍率（0.1-64），同时与 serverTimeAcceleration 相乘
serverTimePersistent = 0;              // 在重启之间保存时间（值 0-1）

guaranteedUpdates = 1;                 // 网络协议（始终使用 1）

loginQueueConcurrentPlayers = 5;       // 登录时同时处理的玩家数
loginQueueMaxPlayers = 500;            // 最大登录队列大小

instanceId = 1;                        // 服务器实例 ID（影响存储文件夹命名）

storageAutoFix = 1;                    // 自动修复损坏的持久化数据（值 0-1）

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## 覆盖配置的启动参数

启动 `DayZServer_x64.exe` 时，某些设置可以通过命令行参数覆盖：

| 参数 | 覆盖的设置 | 示例 |
|------|-----------|------|
| `-config=` | 配置文件路径 | `-config=serverDZ.cfg` |
| `-port=` | 游戏端口 | `-port=2302` |
| `-profiles=` | Profiles 输出目录 | `-profiles=profiles` |
| `-mod=` | 客户端侧 mod（分号分隔） | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | 仅服务器端 mod | `-servermod=@MyServerMod` |
| `-BEpath=` | BattlEye 路径 | `-BEpath=battleye` |
| `-dologs` | 启用日志记录 | -- |
| `-adminlog` | 启用管理员日志记录 | -- |
| `-netlog` | 启用网络日志记录 | -- |
| `-freezecheck` | 冻结时自动重启 | -- |
| `-cpuCount=` | 使用的 CPU 核心数 | `-cpuCount=4` |
| `-noFilePatching` | 禁用文件补丁 | -- |

### 完整启动示例

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Mod 按照 `-mod=` 中指定的顺序加载。依赖顺序很重要：如果 Mod B 依赖 Mod A，请将 Mod A 列在前面。

---

**上一章：** [目录结构](02-directory-structure.md) | [首页](../README.md) | **下一章：** [战利品经济深入解析 >>](04-loot-economy.md)
