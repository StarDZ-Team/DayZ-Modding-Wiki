# Chapter 9.2: 目录结构与任务文件夹

[首页](../README.md) | [<< 上一章: 服务器搭建](01-server-setup.md) | **目录结构** | [下一章: serverDZ.cfg 参考 >>](03-server-cfg.md)

---

> **摘要:** DayZ 服务器目录和任务文件夹中每个文件和文件夹的完整介绍。了解每个文件的作用——以及哪些文件可以安全编辑——是修改战利品经济或添加 mod 之前必须掌握的基础知识。

---

## 目录

- [顶层服务器目录](#顶层服务器目录)
- [addons/ 文件夹](#addons-文件夹)
- [keys/ 文件夹](#keys-文件夹)
- [profiles/ 文件夹](#profiles-文件夹)
- [mpmissions/ 文件夹](#mpmissions-文件夹)
- [任务文件夹结构](#任务文件夹结构)
- [db/ 文件夹 -- 经济核心](#db-文件夹----经济核心)
- [env/ 文件夹 -- 动物领地](#env-文件夹----动物领地)
- [storage_1/ 文件夹 -- 持久化数据](#storage_1-文件夹----持久化数据)
- [任务顶层文件](#任务顶层文件)
- [哪些文件可以编辑，哪些不要动](#哪些文件可以编辑哪些不要动)

---

## 顶层服务器目录

```
DayZServer/
  DayZServer_x64.exe          # 服务器可执行文件
  serverDZ.cfg                 # 主服务器配置（名称、密码、mod、时间）
  dayzsetting.xml              # 渲染设置（专用服务器无需关注）
  ban.txt                      # 封禁的 Steam64 ID，每行一个
  whitelist.txt                # 白名单 Steam64 ID，每行一个
  steam_appid.txt              # 内容为 "221100" -- 不要编辑
  dayz.gproj                   # Workbench 项目文件 -- 不要编辑
  addons/                      # 原版游戏 PBO 文件
  battleye/                    # 反作弊文件
  config/                      # Steam 配置（config.vdf）
  dta/                         # 核心引擎 PBO（脚本、GUI、图形）
  keys/                        # 签名验证密钥（.bikey 文件）
  logs/                        # 引擎级日志
  mpmissions/                  # 所有任务文件夹
  profiles/                    # 运行时输出（脚本日志、玩家数据库、崩溃转储）
  server_manager/              # 服务器管理工具
```

---

## addons/ 文件夹

包含所有原版游戏内容，以 PBO 文件形式打包。每个 PBO 都有一个对应的 `.bisign` 签名文件：

```
addons/
  ai.pbo                       # AI 行为脚本
  ai.pbo.dayz.bisign           # ai.pbo 的签名
  animals.pbo                  # 动物定义
  characters_backpacks.pbo     # 背包模型/配置
  characters_belts.pbo         # 腰带物品模型
  weapons_firearms.pbo         # 武器模型/配置
  ... (100+ 个 PBO 文件)
```

**永远不要编辑这些文件。** 每次通过 SteamCMD 更新服务器时它们都会被覆盖。Mod 通过 `modded` 类系统覆盖原版行为，而不是修改 PBO。

---

## keys/ 文件夹

包含用于验证 mod 签名的 `.bikey` 公钥文件：

```
keys/
  dayz.bikey                   # 原版签名密钥（始终存在）
```

添加 mod 时，将其 `.bikey` 文件复制到此文件夹中。服务器使用 `serverDZ.cfg` 中的 `verifySignatures = 2` 来拒绝此文件夹中没有对应 `.bikey` 的任何 PBO。

如果玩家加载的 mod 的密钥不在你的 `keys/` 文件夹中，他们会被踢出并收到 **"Signature check failed"** 提示。

---

## profiles/ 文件夹

在服务器首次启动时创建。包含运行时输出：

```
profiles/
  BattlEye/                              # BE 日志和封禁记录
  DataCache/                             # 缓存数据
  Users/                                 # 每个玩家的偏好文件
  DayZServer_x64_2026-03-08_11-34-31.ADM  # 管理员日志
  DayZServer_x64_2026-03-08_11-34-31.RPT  # 引擎报告（崩溃信息、警告）
  script_2026-03-08_11-34-35.log           # 脚本日志（你最主要的调试工具）
```

**脚本日志**是这里最重要的文件。每个 `Print()` 调用、每个脚本错误和每条 mod 加载消息都记录在这里。出问题时，首先查看这个文件。

日志文件会随时间积累。旧日志不会自动删除。

---

## mpmissions/ 文件夹

每个地图包含一个子文件夹：

```
mpmissions/
  dayzOffline.chernarusplus/    # 切尔诺鲁斯（免费）
  dayzOffline.enoch/            # 利沃尼亚（DLC）
  dayzOffline.sakhal/           # 萨哈林（DLC）
```

文件夹名称格式为 `<missionName>.<terrainName>`。`serverDZ.cfg` 中的 `template` 值必须与这些文件夹名称之一完全匹配。

---

## 任务文件夹结构

切尔诺鲁斯任务文件夹（`mpmissions/dayzOffline.chernarusplus/`）包含：

```
dayzOffline.chernarusplus/
  init.c                         # 任务入口脚本
  db/                            # 核心经济文件
  env/                           # 动物领地定义
  storage_1/                     # 持久化数据（玩家、世界状态）
  cfgeconomycore.xml             # 经济根类和日志设置
  cfgenvironment.xml             # 动物领地文件链接
  cfgeventgroups.xml             # 事件组定义
  cfgeventspawns.xml             # 事件的精确刷新位置（载具等）
  cfgeffectarea.json             # 污染区定义
  cfggameplay.json               # 游戏玩法调整（体力、伤害、建造）
  cfgignorelist.xml              # 从经济系统中完全排除的物品
  cfglimitsdefinition.xml        # 有效的 category/usage/value 标签定义
  cfglimitsdefinitionuser.xml    # 用户自定义标签定义
  cfgplayerspawnpoints.xml       # 新生玩家出生点
  cfgrandompresets.xml           # 可复用的战利品池定义
  cfgspawnabletypes.xml          # 刷新实体的预装配件和货物
  cfgundergroundtriggers.json    # 地下区域触发器
  cfgweather.xml                 # 天气配置
  areaflags.map                  # 区域标记数据（二进制）
  mapclusterproto.xml            # 地图集群原型定义
  mapgroupcluster.xml            # 建筑群集群定义
  mapgroupcluster01.xml          # 集群数据（第 1 部分）
  mapgroupcluster02.xml          # 集群数据（第 2 部分）
  mapgroupcluster03.xml          # 集群数据（第 3 部分）
  mapgroupcluster04.xml          # 集群数据（第 4 部分）
  mapgroupdirt.xml               # 地面战利品位置
  mapgrouppos.xml                # 地图组位置
  mapgroupproto.xml              # 地图组原型定义
```

---

## db/ 文件夹 -- 经济核心

这是中央经济系统的核心。五个文件控制什么东西在哪里刷新以及刷新多少：

```
db/
  types.xml        # 关键文件：定义每个物品的刷新规则
  globals.xml      # 全局经济参数（计时器、限制、数量）
  events.xml       # 动态事件（动物、载具、直升机）
  economy.xml      # 经济子系统开关（战利品、动物、载具）
  messages.xml     # 定时向玩家广播的服务器消息
```

### types.xml

定义**每个物品**的刷新规则。大约有 23,000 行，是目前最大的经济文件。每个条目指定地图上应存在多少个该物品副本、可以在哪里刷新以及持续多长时间。详见 [Chapter 9.4](04-loot-economy.md) 的深入解析。

### globals.xml

影响整个经济系统的全局参数：僵尸数量、动物数量、清理计时器、战利品损坏范围、重生时间。共有 33 个参数。完整参考请见 [Chapter 9.4](04-loot-economy.md)。

### events.xml

定义动物和载具的动态刷新事件。每个事件指定名义数量、刷新约束和子变体。例如，`VehicleCivilianSedan` 事件会在地图上以 3 种颜色变体刷新 8 辆轿车。

### economy.xml

经济子系统的主开关：

```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```

| 标志 | 含义 |
|------|------|
| `init` | 在服务器首次启动时刷新物品 |
| `load` | 从持久化数据中加载已保存的状态 |
| `respawn` | 允许在清理后重新刷新物品 |
| `save` | 将状态保存到持久化文件中 |

### messages.xml

向所有玩家广播的定时消息。支持倒计时、重复间隔、连接时消息和关服警告：

```xml
<messages>
    <message>
        <deadline>600</deadline>
        <shutdown>1</shutdown>
        <text>#name will shutdown in #tmin minutes.</text>
    </message>
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>Welcome to #name</text>
    </message>
</messages>
```

使用 `#name` 表示服务器名称，`#tmin` 表示剩余分钟数。

---

## env/ 文件夹 -- 动物领地

包含定义每种动物可以刷新位置的 XML 文件：

```
env/
  bear_territories.xml
  cattle_territories.xml
  domestic_animals_territories.xml
  fox_territories.xml
  hare_territories.xml
  hen_territories.xml
  pig_territories.xml
  red_deer_territories.xml
  roe_deer_territories.xml
  sheep_goat_territories.xml
  wild_boar_territories.xml
  wolf_territories.xml
  zombie_territories.xml
```

这些文件包含数百个坐标点，定义了地图上的领地区域。它们被 `cfgenvironment.xml` 引用。除非你想更改动物或僵尸的地理刷新位置，否则通常不需要编辑这些文件。

---

## storage_1/ 文件夹 -- 持久化数据

保存服务器在重启之间的持久化状态：

```
storage_1/
  players.db         # 所有玩家角色的 SQLite 数据库
  spawnpoints.bin    # 二进制出生点数据
  backup/            # 持久化数据的自动备份
  data/              # 世界状态（放置的物品、基地建筑、载具）
```

**服务器运行时不要编辑 `players.db`。** 它是一个被服务器进程锁定的 SQLite 数据库。如果需要清除角色数据，请先停止服务器，然后删除或重命名该文件。

要进行**完全清档**，停止服务器并删除整个 `storage_1/` 文件夹。服务器在下次启动时会以全新世界重建它。

要进行**部分清档**（保留角色，重置战利品）：
1. 停止服务器
2. 删除 `storage_1/data/` 中的文件但保留 `players.db`
3. 重启

---

## 任务顶层文件

### cfgeconomycore.xml

注册经济系统的根类并配置 CE 日志记录：

```xml
<economycore>
    <classes>
        <rootclass name="DefaultWeapon" />
        <rootclass name="DefaultMagazine" />
        <rootclass name="Inventory_Base" />
        <rootclass name="HouseNoDestruct" reportMemoryLOD="no" />
        <rootclass name="SurvivorBase" act="character" reportMemoryLOD="no" />
        <rootclass name="DZ_LightAI" act="character" reportMemoryLOD="no" />
        <rootclass name="CarScript" act="car" reportMemoryLOD="no" />
        <rootclass name="BoatScript" act="car" reportMemoryLOD="no" />
    </classes>
    <defaults>
        <default name="log_ce_loop" value="false"/>
        <default name="log_ce_dynamicevent" value="false"/>
        <default name="log_ce_vehicle" value="false"/>
        <default name="log_ce_lootspawn" value="false"/>
        <default name="log_ce_lootcleanup" value="false"/>
        <default name="log_ce_lootrespawn" value="false"/>
        <default name="log_ce_statistics" value="false"/>
        <default name="log_ce_zombie" value="false"/>
        <default name="log_storageinfo" value="false"/>
        <default name="log_hivewarning" value="true"/>
        <default name="log_missionfilewarning" value="true"/>
        <default name="save_events_startup" value="true"/>
        <default name="save_types_startup" value="true"/>
    </defaults>
</economycore>
```

调试物品刷新问题时，将 `log_ce_lootspawn` 设为 `"true"`。它会在 RPT 日志中产生详细输出，显示 CE 尝试刷新哪些物品以及成功或失败的原因。

### cfglimitsdefinition.xml

定义 `types.xml` 中使用的 `<category>`、`<usage>`、`<value>` 和 `<tag>` 元素的有效值：

```xml
<lists>
    <categories>
        <category name="tools"/>
        <category name="containers"/>
        <category name="clothes"/>
        <category name="food"/>
        <category name="weapons"/>
        <category name="books"/>
        <category name="explosives"/>
        <category name="lootdispatch"/>
    </categories>
    <tags>
        <tag name="floor"/>
        <tag name="shelves"/>
        <tag name="ground"/>
    </tags>
    <usageflags>
        <usage name="Military"/>
        <usage name="Police"/>
        <usage name="Medic"/>
        <usage name="Firefighter"/>
        <usage name="Industrial"/>
        <usage name="Farm"/>
        <usage name="Coast"/>
        <usage name="Town"/>
        <usage name="Village"/>
        <usage name="Hunting"/>
        <usage name="Office"/>
        <usage name="School"/>
        <usage name="Prison"/>
        <usage name="Lunapark"/>
        <usage name="SeasonalEvent"/>
        <usage name="ContaminatedArea"/>
        <usage name="Historical"/>
    </usageflags>
    <valueflags>
        <value name="Tier1"/>
        <value name="Tier2"/>
        <value name="Tier3"/>
        <value name="Tier4"/>
        <value name="Unique"/>
    </valueflags>
</lists>
```

如果你在 `types.xml` 中使用了此处未定义的 `<usage>` 或 `<value>` 标签，该物品将静默地无法刷新。

### cfgignorelist.xml

此处列出的物品完全从经济系统中排除，即使它们在 `types.xml` 中有条目：

```xml
<ignore>
    <type name="Bandage"></type>
    <type name="CattleProd"></type>
    <type name="Defibrillator"></type>
    <type name="HescoBox"></type>
    <type name="StunBaton"></type>
    <type name="TransitBus"></type>
    <type name="Spear"></type>
    <type name="Mag_STANAGCoupled_30Rnd"></type>
    <type name="Wreck_Mi8"></type>
</ignore>
```

这用于存在于游戏代码中但不打算自然刷新的物品（未完成的物品、弃用内容、非当季的季节性物品）。

### cfggameplay.json

一个覆盖游戏玩法参数的 JSON 文件。控制体力、移动、基地伤害、天气、温度、武器遮挡、溺水等。此文件是可选的 -- 如果不存在，服务器使用默认值。

### cfgplayerspawnpoints.xml

定义新出生玩家在地图上出现的位置，包含与感染者、其他玩家和建筑物的距离约束。

### cfgeventspawns.xml

包含事件（载具、直升机坠毁等）可以刷新的精确世界坐标。`events.xml` 中每个事件名称都有一个有效位置列表：

```xml
<eventposdef>
    <event name="VehicleCivilianSedan">
        <pos x="12071.933594" z="9129.989258" a="317.953339" />
        <pos x="12302.375001" z="9051.289062" a="60.399284" />
        <pos x="10182.458985" z="1987.5271" a="29.172445" />
        ...
    </event>
</eventposdef>
```

`a` 属性是以度为单位的旋转角度。

---

## 哪些文件可以编辑，哪些不要动

| 文件/文件夹 | 可以编辑？ | 说明 |
|-------------|:---:|------|
| `serverDZ.cfg` | 是 | 主服务器配置 |
| `db/types.xml` | 是 | 物品刷新规则 -- 你最常编辑的文件 |
| `db/globals.xml` | 是 | 经济调整参数 |
| `db/events.xml` | 是 | 载具/动物刷新事件 |
| `db/economy.xml` | 是 | 经济子系统开关 |
| `db/messages.xml` | 是 | 服务器广播消息 |
| `cfggameplay.json` | 是 | 游戏玩法调整 |
| `cfgspawnabletypes.xml` | 是 | 配件/货物预设 |
| `cfgrandompresets.xml` | 是 | 战利品池定义 |
| `cfglimitsdefinition.xml` | 是 | 添加自定义 usage/value 标签 |
| `cfgplayerspawnpoints.xml` | 是 | 玩家出生位置 |
| `cfgeventspawns.xml` | 是 | 事件刷新坐标 |
| `cfgignorelist.xml` | 是 | 从经济系统中排除物品 |
| `cfgweather.xml` | 是 | 天气模式 |
| `cfgeffectarea.json` | 是 | 污染区 |
| `init.c` | 是 | 任务入口脚本 |
| `addons/` | **否** | 更新时会被覆盖 |
| `dta/` | **否** | 核心引擎数据 |
| `keys/` | 仅添加 | 将 mod 的 `.bikey` 文件复制到此处 |
| `storage_1/` | 仅删除 | 持久化数据 -- 不要手动编辑 |
| `battleye/` | **否** | 反作弊 -- 不要修改 |
| `mapgroup*.xml` | 谨慎 | 建筑战利品位置 -- 仅限高级编辑 |

---

**上一章：** [服务器搭建](01-server-setup.md) | [首页](../README.md) | **下一章：** [serverDZ.cfg 参考 >>](03-server-cfg.md)
