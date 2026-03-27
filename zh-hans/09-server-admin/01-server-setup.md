# Chapter 9.1: 服务器搭建与首次启动

[首页](../README.md) | **服务器搭建** | [下一章: 目录结构 >>](02-directory-structure.md)

---

> **摘要:** 从零开始使用 SteamCMD 安装 DayZ 独立版专用服务器，以最简配置启动它，验证其出现在服务器浏览器中，并以玩家身份连接。本章涵盖从硬件要求到修复最常见的首次启动问题的所有内容。

---

## 目录

- [前提条件](#前提条件)
- [安装 SteamCMD](#安装-steamcmd)
- [安装 DayZ 服务器](#安装-dayz-服务器)
- [安装后的目录结构](#安装后的目录结构)
- [使用最简配置首次启动](#使用最简配置首次启动)
- [验证服务器是否运行](#验证服务器是否运行)
- [以玩家身份连接](#以玩家身份连接)
- [常见的首次启动问题](#常见的首次启动问题)

---

## 前提条件

### 硬件

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 4 核, 2.4 GHz | 6+ 核, 3.5 GHz |
| 内存 | 8 GB | 16 GB |
| 硬盘 | 20 GB SSD | 40 GB NVMe SSD |
| 网络 | 10 Mbps 上行 | 50+ Mbps 上行 |
| 操作系统 | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

DayZ 服务器的游戏逻辑是单线程的。主频比核心数更重要。

### 软件

- **SteamCMD** -- 用于安装专用服务器的 Steam 命令行客户端
- **Visual C++ Redistributable 2019** (Windows) -- `DayZServer_x64.exe` 所需
- **DirectX Runtime** (Windows) -- 通常已预装
- 路由器/防火墙上转发 **2302-2305 UDP** 端口

---

## 安装 SteamCMD

### Windows

1. 从 https://developer.valvesoftware.com/wiki/SteamCMD 下载 SteamCMD
2. 将 `steamcmd.exe` 解压到一个固定文件夹，例如 `C:\SteamCMD\`
3. 运行一次 `steamcmd.exe` -- 它会自动更新自身

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## 安装 DayZ 服务器

DayZ 服务器的 Steam App ID 是 **223350**。安装时无需登录拥有 DayZ 的 Steam 账号。

### 一行命令安装 (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### 一行命令安装 (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### 更新脚本

创建一个脚本，每次有补丁时都可以重新运行：

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Update complete.
pause
```

`validate` 参数会检查每个文件是否损坏。全新安装大约需要下载 2-3 GB。

---

## 安装后的目录结构

安装完成后，服务器根目录结构如下：

```
DayZServer/
  DayZServer_x64.exe        # 服务器可执行文件
  serverDZ.cfg               # 主服务器配置文件
  dayzsetting.xml            # 渲染/视频设置（专用服务器无需关注）
  addons/                    # 原版 PBO 文件（ai.pbo, animals.pbo 等）
  battleye/                  # BattlEye 反作弊（BEServer_x64.dll）
  dta/                       # 核心引擎数据（bin.pbo, scripts.pbo, gui.pbo）
  keys/                      # 签名密钥（原版为 dayz.bikey）
  logs/                      # 引擎日志（连接、内容、音频）
  mpmissions/                # 任务文件夹
    dayzOffline.chernarusplus/   # 切尔诺鲁斯任务
    dayzOffline.enoch/           # 利沃尼亚任务（DLC）
    dayzOffline.sakhal/          # 萨哈林任务（DLC）
  profiles/                  # 运行时输出：RPT 日志、脚本日志、玩家数据库
  ban.txt                    # 封禁玩家列表（Steam64 ID）
  whitelist.txt              # 白名单玩家（Steam64 ID）
  steam_appid.txt            # 内容为 "221100"
```

关键要点：
- **需要编辑的文件**：`serverDZ.cfg` 和 `mpmissions/` 内的文件。
- **不要编辑的文件**：`addons/` 或 `dta/` 中的文件 -- 每次更新都会被覆盖。
- **Mod PBO 文件** 放在服务器根目录或子文件夹中（后续章节会介绍）。
- **`profiles/`** 在首次启动时创建，包含脚本日志和崩溃转储。

---

## 使用最简配置首次启动

### 步骤 1：编辑 serverDZ.cfg

用文本编辑器打开 `serverDZ.cfg`。首次测试使用最简配置：

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### 步骤 2：启动服务器

在服务器目录中打开命令提示符并运行：

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| 参数 | 用途 |
|------|------|
| `-config=serverDZ.cfg` | 配置文件路径 |
| `-port=2302` | 主游戏端口（同时使用 2303-2305） |
| `-profiles=profiles` | 日志和玩家数据的输出文件夹 |
| `-dologs` | 启用服务器日志记录 |
| `-adminlog` | 记录管理员操作 |
| `-netlog` | 记录网络事件 |
| `-freezecheck` | 检测到冻结时自动重启 |

### 步骤 3：等待初始化

服务器需要 30-90 秒才能完全启动。观察控制台输出。当看到如下信息时：

```
BattlEye Server: Initialized (v1.xxx)
```

...服务器已准备好接受连接。

---

## 验证服务器是否运行

### 方法 1：脚本日志

检查 `profiles/` 中是否有类似 `script_YYYY-MM-DD_HH-MM-SS.log` 的文件。打开它并查找：

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

这些行确认经济系统已初始化，任务已加载。

### 方法 2：RPT 文件

`profiles/` 中的 `.RPT` 文件显示引擎级输出。查找：

```
Dedicated host created.
BattlEye Server: Initialized
```

### 方法 3：Steam 服务器浏览器

打开 Steam，进入 **查看 > 游戏服务器 > 收藏**，点击 **添加服务器**，输入 `127.0.0.1:2302`（或你的公网 IP），然后点击 **在此地址查找游戏**。如果服务器出现，说明它正在运行且可访问。

### 方法 4：查询端口

使用外部工具（如 https://www.battlemetrics.com/）或 `gamedig` npm 包查询端口 27016（Steam 查询端口 = 游戏端口 + 24714）。

---

## 以玩家身份连接

### 从同一台机器连接

1. 启动 DayZ（不是 DayZ Server -- 是普通游戏客户端）
2. 打开 **服务器浏览器**
3. 转到 **局域网** 标签页或 **收藏** 标签页
4. 将 `127.0.0.1:2302` 添加到收藏
5. 点击 **连接**

如果在同一台机器上运行客户端和服务器，请使用 `DayZDiag_x64.exe`（诊断客户端）而不是零售版客户端。启动命令：

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### 从其他机器连接

根据客户端是否在同一网络上，使用服务器的 **公网 IP** 或 **局域网 IP**。端口 2302-2305 UDP 必须已转发。

---

## 常见的首次启动问题

### 服务器启动后立即关闭

**原因：** 缺少 Visual C++ Redistributable 或 `serverDZ.cfg` 中有语法错误。

**解决方法：** 安装 VC++ Redist 2019 (x64)。检查 `serverDZ.cfg` 中是否缺少分号 -- 每行参数都必须以 `;` 结尾。

### "BattlEye initialization failed"

**原因：** `battleye/` 文件夹丢失或杀毒软件阻止了 `BEServer_x64.dll`。

**解决方法：** 通过 SteamCMD 重新验证服务器文件。为整个服务器文件夹添加杀毒软件例外。

### 服务器运行但不显示在浏览器中

**原因：** 端口未转发，或 Windows 防火墙阻止了可执行文件。

**解决方法：**
1. 为 `DayZServer_x64.exe` 添加 Windows 防火墙入站规则（允许所有 UDP）
2. 在路由器上转发 **2302-2305 UDP** 端口
3. 使用外部端口检查工具确认公网 IP 上的 2302 UDP 端口已开放

### 连接时"版本不匹配"

**原因：** 服务器和客户端的版本不同。

**解决方法：** 两端都更新。为服务器运行 SteamCMD 更新命令。客户端通过 Steam 自动更新。

### 没有物资刷新

**原因：** `init.c` 文件丢失或 Hive 初始化失败。

**解决方法：** 验证 `mpmissions/dayzOffline.chernarusplus/init.c` 是否存在并包含 `CreateHive()`。检查脚本日志中的错误。

### 服务器占用一个 CPU 核心 100%

这是正常现象。DayZ 服务器是单线程的。不要在同一个核心上运行多个服务器实例 -- 使用处理器亲和性或不同的机器。

### 玩家以乌鸦形态出生 / 卡在加载界面

**原因：** `serverDZ.cfg` 中的任务模板名称与 `mpmissions/` 中的现有文件夹不匹配。

**解决方法：** 检查 template 值。它必须与文件夹名称完全匹配：

```cpp
template = "dayzOffline.chernarusplus";  // 必须匹配 mpmissions/ 文件夹名称
```

---

**[首页](../README.md)** | **下一章：** [目录结构 >>](02-directory-structure.md)
