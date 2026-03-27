# Chapter 9.12: 高级服务器主题

[首页](../README.md) | [<< 上一章: 故障排除](11-troubleshooting.md) | [第 9 部分首页](01-server-setup.md)

---

> **摘要:** 深入配置文件、多地图设置、经济拆分、动物领地、动态事件、天气控制、自动重启和消息系统。

---

## 目录

- [cfggameplay.json 深入解析](#cfggameplayjson-深入解析)
- [多地图服务器](#多地图服务器)
- [自定义经济调优](#自定义经济调优)
- [cfgenvironment.xml 与动物领地](#cfgenvironmentxml-与动物领地)
- [自定义动态事件](#自定义动态事件)
- [服务器自动重启](#服务器自动重启)
- [cfgweather.xml](#cfgweatherxml)
- [消息系统](#消息系统)

---

## cfggameplay.json 深入解析

**cfggameplay.json** 文件位于你的任务文件夹中，覆盖硬编码的游戏默认值。首先在 **serverDZ.cfg** 中启用它：

```cpp
enableCfgGameplayFile = 1;
```

原版结构：

```json
{
  "version": 123,
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false,
    "disableRespawnDialog": false,
    "disableRespawnInUnconsciousness": false
  },
  "PlayerData": {
    "disablePersonalLight": false,
    "StaminaData": {
      "sprintStaminaModifierErc": 1.0, "sprintStaminaModifierCro": 1.0,
      "staminaWeightLimitThreshold": 6000.0, "staminaMax": 100.0,
      "staminaKg": 0.3, "staminaMin": 0.0,
      "staminaDepletionSpeed": 1.0, "staminaRecoverySpeed": 1.0
    },
    "ShockHandlingData": {
      "shockRefillSpeedConscious": 5.0, "shockRefillSpeedUnconscious": 1.0,
      "allowRefillSpeedModifier": true
    },
    "MovementData": {
      "timeToSprint": 0.45, "timeToJog": 0.0,
      "rotationSpeedJog": 0.3, "rotationSpeedSprint": 0.15
    },
    "DrowningData": {
      "staminaDepletionSpeed": 10.0, "healthDepletionSpeed": 3.0,
      "shockDepletionSpeed": 10.0
    },
    "WeaponObstructionData": { "staticMode": 1, "dynamicMode": 1 }
  },
  "WorldsData": {
    "lightingConfig": 0, "objectSpawnersArr": [],
    "environmentMinTemps": [-3, -2, 0, 4, 9, 14, 18, 17, 13, 11, 9, 0],
    "environmentMaxTemps": [3, 5, 7, 14, 19, 24, 26, 25, 18, 14, 10, 5]
  },
  "BaseBuildingData": { "canBuildAnywhere": false, "canCraftAnywhere": false },
  "UIData": {
    "use3DMap": false,
    "HitIndicationData": {
      "hitDirectionOverrideEnabled": false, "hitDirectionBehaviour": 1,
      "hitDirectionStyle": 0, "hitDirectionIndicatorColorStr": "0xffbb0a1e",
      "hitDirectionMaxDuration": 2.0, "hitDirectionBreakPointRelative": 0.2,
      "hitDirectionScatter": 10.0, "hitIndicationPostProcessEnabled": true
    }
  }
}
```

- `version` -- 必须与你的服务器二进制文件期望的值匹配。不要更改它。
- `lightingConfig` -- `0`（默认）或 `1`（更亮的夜晚）。
- `environmentMinTemps` / `environmentMaxTemps` -- 12 个值，每月一个（1 月到 12 月）。
- `disablePersonalLight` -- 移除新玩家夜间附近的微弱环境光。
- `staminaMax` 和冲刺修改器控制玩家在精疲力竭前能跑多远。
- `use3DMap` -- 将游戏内地图切换为地形渲染的 3D 版本。

---

## 多地图服务器

DayZ 通过 `mpmissions/` 内的不同任务文件夹支持多张地图：

| 地图 | 任务文件夹 |
|------|-----------|
| 切尔诺鲁斯 | `mpmissions/dayzOffline.chernarusplus/` |
| 利沃尼亚 | `mpmissions/dayzOffline.enoch/` |
| 萨哈林 | `mpmissions/dayzOffline.sakhal/` |

每张地图都有自己的 CE 文件（`types.xml`、`events.xml` 等）。通过 **serverDZ.cfg** 中的 `template` 切换地图：

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

或使用启动参数：`-mission=mpmissions/dayzOffline.enoch`

要同时运行多张地图，使用各自拥有独立配置、配置目录和端口范围的独立服务器实例。

---

## 自定义经济调优

### 拆分 types.xml

将物品拆分到多个文件中并在 **cfgeconomycore.xml** 中注册它们：

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

服务器加载并合并所有 `type="types"` 的文件。

### 自定义类别和标签

**cfglimitsdefinition.xml** 定义 `types.xml` 的类别/标签，但在更新时会被覆盖。改用 **cfglimitsdefinitionuser.xml**：

```xml
<lists>
    <categories>
        <category name="custom_rare" />
    </categories>
    <tags>
        <tag name="custom_event" />
    </tags>
</lists>
```

---

## cfgenvironment.xml 与动物领地

你任务文件夹中的 **cfgenvironment.xml** 文件链接到 `env/` 子目录中的领地文件：

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

`env/` 文件夹包含以下动物领地文件：

| 文件 | 动物 |
|------|------|
| **bear_territories.xml** | 棕熊 |
| **wolf_territories.xml** | 狼群 |
| **fox_territories.xml** | 狐狸 |
| **hare_territories.xml** | 兔子/野兔 |
| **hen_territories.xml** | 鸡 |
| **pig_territories.xml** | 猪 |
| **red_deer_territories.xml** | 马鹿 |
| **roe_deer_territories.xml** | 狍 |
| **sheep_goat_territories.xml** | 绵羊/山羊 |
| **wild_boar_territories.xml** | 野猪 |
| **cattle_territories.xml** | 牛 |

领地条目定义带有位置和动物数量的圆形区域：

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`、`z` -- 中心坐标；`r` -- 半径（米）
- `dmin`、`dmax` -- 区域内的最小/最大动物数量
- `smin`、`smax` -- 保留字段（设为 `-1`）

---

## 自定义动态事件

动态事件（直升机坠毁、车队）在 **events.xml** 中定义。要创建自定义事件：

**1. 在 **events.xml** 中定义事件：**

```xml
<event name="StaticMyCustomCrash">
    <nominal>3</nominal> <min>1</min> <max>5</max>
    <lifetime>1800</lifetime> <restock>600</restock>
    <saferadius>500</saferadius> <distanceradius>200</distanceradius> <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1" />
    <position>fixed</position> <limit>child</limit> <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_Mi8_Crashed" />
    </children>
</event>
```

**2. 在 **cfgeventspawns.xml** 中添加刷新位置：**

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. 添加感染者守卫**（可选）-- 在事件定义中添加 `<secondary type="ZmbM_PatrolNormal_Autumn" />` 元素。

**4. 分组刷新**（可选）-- 在 **cfgeventgroups.xml** 中定义集群，并在事件中引用组名称。

---

## 服务器自动重启

DayZ 没有内置的重启调度器。使用操作系统级自动化。

### Windows

创建 **restart_server.bat** 并通过 Windows 计划任务每 4-6 小时运行一次：

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

创建 shell 脚本并添加到 cron（`0 */4 * * *`）：

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

每次重启前始终备份 `storage_1/`。关闭过程中损坏的持久化数据可能清除玩家基地和载具。

---

## cfgweather.xml

你任务文件夹中的 **cfgweather.xml** 文件控制天气模式。每张地图都有自己的默认值：

每种天气现象都有 `min`、`max`、`duration_min` 和 `duration_max`（秒）：

| 天气现象 | 默认最小值 | 默认最大值 | 说明 |
|----------|-----------|-----------|------|
| `overcast` | 0.0 | 1.0 | 驱动云密度和降雨概率 |
| `rain` | 0.0 | 1.0 | 仅在阴天超过阈值时触发。将 max 设为 `0.0` 可禁用降雨 |
| `fog` | 0.0 | 0.3 | 值超过 `0.5` 产生接近零的能见度 |
| `wind_magnitude` | 0.0 | 18.0 | 影响弹道和玩家移动 |

---

## 消息系统

你任务文件夹中的 **db/messages.xml** 文件控制定时服务器消息和关服警告：

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- 消息触发前的分钟数（对于关服消息，是服务器停止前的分钟数）
- `shutdown` -- `1` 表示关服序列消息，`0` 表示常规广播

消息系统不会重启服务器。它只在外部配置了重启计划时显示警告。

---

[首页](../README.md) | [<< 上一章: 故障排除](11-troubleshooting.md) | [第 9 部分首页](01-server-setup.md)
