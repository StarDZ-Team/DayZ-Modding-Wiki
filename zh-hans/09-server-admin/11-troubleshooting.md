# Chapter 9.11: 服务器故障排除

[首页](../README.md) | [<< 上一章: Mod 管理](10-mod-management.md) | [下一章: 高级主题 >>](12-advanced.md)

---

> **摘要:** 诊断和修复最常见的 DayZ 服务器问题——启动失败、连接问题、崩溃、战利品和载具刷新、持久化和性能。这里的每个解决方案都来自数千条社区报告中的真实故障模式。

---

## 目录

- [服务器无法启动](#服务器无法启动)
- [玩家无法连接](#玩家无法连接)
- [崩溃和空指针](#崩溃和空指针)
- [战利品不刷新](#战利品不刷新)
- [载具不刷新](#载具不刷新)
- [持久化问题](#持久化问题)
- [性能问题](#性能问题)
- [读取日志文件](#读取日志文件)
- [快速诊断检查清单](#快速诊断检查清单)

---

## 服务器无法启动

### 缺少 DLL 文件

如果 `DayZServer_x64.exe` 立即崩溃并显示缺少 DLL 错误，从 Microsoft 官方网站安装最新的 **Visual C++ Redistributable for Visual Studio 2019** (x64) 并重启。

### 端口已被占用

另一个 DayZ 实例或应用程序占用了端口 2302。使用 `netstat -ano | findstr 2302`（Windows）或 `ss -tulnp | grep 2302`（Linux）检查。终止冲突进程或使用 `-port=2402` 更改端口。

### 缺少任务文件夹

服务器需要 `mpmissions/<template>/`，其中文件夹名称必须与 **serverDZ.cfg** 中的 `template` 值完全匹配。对于切尔诺鲁斯，即 `mpmissions/dayzOffline.chernarusplus/`，其中必须至少包含 **init.c**。

### 无效的 serverDZ.cfg

单个缺失的分号或错误的引号类型会导致启动静默失败。注意以下问题：

- 值行末尾缺少 `;`
- 使用了中文引号而非英文直引号
- `class` 条目周围缺少 `{};` 块

### 缺少 Mod 文件

`-mod=@CF;@VPPAdminTools;@MyMod` 中的每个路径都必须相对于服务器根目录存在，并包含带有 `.pbo` 文件的 **addons/** 文件夹。单个错误路径就会阻止启动。

---

## 玩家无法连接

### 端口转发

DayZ 需要以下端口在防火墙中转发和开放：

| 端口 | 协议 | 用途 |
|------|------|------|
| 2302 | UDP | 游戏流量 |
| 2303 | UDP | Steam 网络 |
| 2304 | UDP | Steam 查询（内部） |
| 27016 | UDP | Steam 服务器浏览器查询 |

如果你使用 `-port=` 更改了基础端口，所有其他端口按相同偏移量移动。

### 防火墙阻止

将 **DayZServer_x64.exe** 添加到操作系统防火墙例外中。在 Windows 上：`netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`。在 Linux 上，使用 `ufw` 或 `iptables` 开放端口。

### Mod 不匹配

客户端必须与服务器拥有完全相同的 mod 版本。如果玩家看到"Mod mismatch"，说明某一方版本过期。当任何 mod 收到 Workshop 更新时，同时更新两端。

### 缺少 .bikey 文件

每个 mod 的 `.bikey` 文件必须在服务器的 `keys/` 目录中。没有它，BattlEye 会拒绝客户端签名的 PBO。查看每个 mod 的 `keys/` 或 `key/` 文件夹。

### 服务器已满

检查 **serverDZ.cfg** 中的 `maxPlayers`（默认 60）。

---

## 崩溃和空指针

### 空指针访问

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- 最常见的脚本错误。某个 mod 在已删除或未初始化的对象上调用方法。这是 mod 的 bug，不是服务器配置错误。将完整的 RPT 日志发送给 mod 作者进行报告。

### 查找脚本错误

在 RPT 日志中搜索 `SCRIPT (E)`。错误中的类名和方法名告诉你哪个 mod 是罪魁祸首。RPT 位置：

- **服务器：** `$profiles/` 目录（如果未设置 `-profiles=` 则在服务器根目录）
- **客户端：** `%localappdata%\DayZ\`

### 重启时崩溃

如果服务器每次重启都崩溃，**storage_1/** 可能已损坏。停止服务器，备份 `storage_1/`，删除 `storage_1/data/events.bin`，然后重启。如果仍然失败，删除整个 `storage_1/` 目录（清除所有持久化数据）。

### Mod 更新后崩溃

回退到之前的 mod 版本。查看 Workshop 更新日志中的破坏性更改——重命名的类、删除的配置和更改的 RPC 格式是常见原因。

---

## 战利品不刷新

### types.xml 未注册

在 **types.xml** 中定义的物品不会刷新，除非该文件在 **cfgeconomycore.xml** 中注册：

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

如果你使用自定义 types 文件（例如 **types_custom.xml**），为其添加单独的 `<file>` 条目。

### 错误的 Category、Usage 或 Value 标签

你的 types.xml 中的每个 `<category>`、`<usage>` 和 `<value>` 标签必须与 **cfglimitsdefinition.xml** 中定义的名称匹配。像 `usage name="Military"`（大写 M）这样的拼写错误，当定义中写的是 `military`（小写）时，会导致物品静默地无法刷新。

### Nominal 设为零

如果 `nominal` 为 `0`，CE 永远不会刷新该物品。这对于应仅通过制作、事件或管理员放置获得的物品是有意的。如果你想让物品自然刷新，将 `nominal` 设为至少 `1`。

### 缺少地图组位置

物品需要建筑内部的有效刷新位置。如果自定义物品没有匹配的地图组位置（在 **mapgroupproto.xml** 中定义），CE 就没有地方放置它。将物品分配到地图上已有有效位置的 category 和 usage。

---

## 载具不刷新

载具使用事件系统，**不是** types.xml。

### events.xml 配置

载具刷新在 **events.xml** 中定义：

```xml
<event name="VehicleOffroadHatchback">
    <nominal>8</nominal>
    <min>5</min>
    <max>8</max>
    <lifetime>3888000</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="1" min="1" type="OffroadHatchback"/>
    </children>
</event>
```

### 缺少刷新位置

设置 `<position>fixed</position>` 的载具事件需要在 **cfgeventspawns.xml** 中有条目。没有定义坐标，事件就无处放置载具。

### 事件被禁用

如果 `<active>0</active>`，事件被完全禁用。设为 `1`。

### 损坏载具阻塞槽位

如果 `remove_damaged="0"`，被摧毁的载具永远留在世界中并占用刷新槽位。设置 `remove_damaged="1"` 以便 CE 清理残骸并刷新替代品。

---

## 持久化问题

### 基地消失

领地旗帜必须在计时器到期前刷新。默认的 `FlagRefreshFrequency` 是 `432000` 秒（5 天）。如果在该时间窗口内没有玩家与旗帜交互，旗帜和其半径内的所有物体都会被删除。

检查 **globals.xml** 中的值：

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

在低人口服务器上增加此值，因为那里的玩家登录频率较低。

### 重启后物品消失

每个物品在 **types.xml** 中都有一个 `lifetime`（秒）。当物品在没有玩家交互的情况下到期时，CE 会移除它。参考：`3888000` = 45 天，`604800` = 7 天，`14400` = 4 小时。容器内的物品继承容器的生命周期。

### storage_1/ 增长过大

如果你的 `storage_1/` 目录增长到数百 MB 以上，你的经济系统产生了太多物品。降低 types.xml 中的 `nominal` 值，特别是食物、服装和弹药等高数量物品。膨胀的持久化文件导致更长的重启时间。

### 玩家数据丢失

玩家背包和位置存储在 `storage_1/players/` 中。如果此目录被删除或损坏，所有玩家都会重新出生。定期备份 `storage_1/`。

---

## 性能问题

### 服务器 FPS 下降

DayZ 服务器的目标是 30+ FPS 以实现流畅的游戏体验。低服务器 FPS 的常见原因：

- **僵尸太多** -- 降低 **globals.xml** 中的 `ZombieMaxCount`（默认 800，尝试 400-600）
- **动物太多** -- 降低 `AnimalMaxCount`（默认 200，尝试 100）
- **战利品过多** -- 降低 types.xml 中的 `nominal` 值
- **基地物体过多** -- 拥有数百物品的大型基地给持久化带来压力
- **脚本密集型 mod** -- 一些 mod 运行昂贵的逐帧逻辑

### 不同步

玩家体验到橡皮筋效应、延迟操作或隐形僵尸是不同步的症状。这几乎总是意味着服务器 FPS 已降至 15 以下。修复根本的性能问题，而不是寻找专门针对不同步的设置。

### 重启时间过长

重启时间与 `storage_1/` 的大小成正比。如果重启超过 2-3 分钟，你有太多持久化物体。降低战利品 nominal 值并设置适当的生命周期。

---

## 读取日志文件

### 服务器 RPT 位置

RPT 文件在 `$profiles/`（如果使用 `-profiles=` 启动）或服务器根目录中。文件名格式：`DayZServer_x64_<date>_<time>.RPT`。

### 搜索内容

| 搜索词 | 含义 |
|--------|------|
| `SCRIPT (E)` | 脚本错误 -- 某个 mod 有 bug |
| `[ERROR]` | 引擎级错误 |
| `ErrorMessage` | 可能导致关闭的致命错误 |
| `Cannot open` | 缺少文件（PBO、配置、任务） |
| `Crash` | 应用级崩溃 |

### BattlEye 日志

BattlEye 日志在服务器根目录内的 `BattlEye/` 目录中。这些显示踢出和封禁事件。如果玩家报告被意外踢出，首先检查这里。

---

## 快速诊断检查清单

出问题时，按顺序完成此列表：

```
1. 检查服务器 RPT 中的 SCRIPT (E) 和 [ERROR] 行
2. 验证每个 -mod= 路径存在且包含 addons/*.pbo
3. 验证所有 .bikey 文件已复制到 keys/
4. 检查 serverDZ.cfg 中的语法错误（缺少分号）
5. 检查端口转发：2302 UDP + 27016 UDP
6. 验证任务文件夹与 serverDZ.cfg 中的 template 值匹配
7. 检查 storage_1/ 是否损坏（必要时删除 events.bin）
8. 先用零 mod 测试，然后逐个添加 mod
```

步骤 8 是最强大的技术。如果服务器在原版状态下正常工作但加 mod 后出问题，你可以通过二分法隔离问题 mod——添加一半的 mod，测试，然后缩小范围。

---

[首页](../README.md) | [<< 上一章: Mod 管理](10-mod-management.md) | [下一章: 高级主题 >>](12-advanced.md)
