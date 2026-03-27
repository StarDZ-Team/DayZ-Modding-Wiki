# Chapter 9.10: Mod 管理

[首页](../README.md) | [<< 上一章: 访问控制](09-access-control.md) | [下一章: 故障排除 >>](11-troubleshooting.md)

---

> **摘要:** 在 DayZ 专用服务器上安装、配置和维护第三方 mod。涵盖启动参数、Workshop 下载、签名密钥、加载顺序、仅服务器端与客户端必需的 mod、更新以及导致崩溃或玩家被踢的最常见错误。

---

## 目录

- [Mod 如何加载](#mod-如何加载)
- [启动参数格式](#启动参数格式)
- [Workshop Mod 安装](#workshop-mod-安装)
- [Mod 密钥 (.bikey)](#mod-密钥-bikey)
- [加载顺序与依赖关系](#加载顺序与依赖关系)
- [仅服务器端与客户端必需的 Mod](#仅服务器端与客户端必需的-mod)
- [更新 Mod](#更新-mod)
- [排查 Mod 冲突](#排查-mod-冲突)
- [常见错误](#常见错误)

---

## Mod 如何加载

DayZ 通过 `-mod=` 启动参数加载 mod。每个条目是一个包含 PBO 文件和 `config.cpp` 的文件夹路径。引擎读取每个 mod 文件夹中的每个 PBO，注册其类和脚本，然后继续到列表中的下一个 mod。

服务器和客户端必须在 `-mod=` 中有相同的 mod。如果服务器列出 `@CF;@MyMod` 但客户端只有 `@CF`，连接将因签名不匹配而失败。放在 `-servermod=` 中的仅服务器端 mod 是例外——客户端永远不需要这些。

---

## 启动参数格式

一个典型的 mod 服务器启动命令：

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| 参数 | 用途 |
|------|------|
| `-mod=` | 服务器和所有连接客户端都需要的 mod |
| `-servermod=` | 仅服务器端 mod（客户端不需要） |

规则：
- 路径以**分号分隔**，分号周围没有空格
- 每个路径相对于服务器根目录（例如 `@CF` 意味着 `<server_root>/@CF/`）
- 可以使用绝对路径：`-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **顺序很重要** -- 依赖项必须出现在需要它们的 mod 之前

---

## Workshop Mod 安装

### 步骤 1：下载 Mod

使用 SteamCMD 配合 DayZ **客户端** App ID (221100) 和 mod 的 Workshop ID：

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

下载的文件位于：

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### 步骤 2：创建符号链接或复制

Workshop 文件夹使用数字 ID，无法在 `-mod=` 中使用。创建命名符号链接（推荐）或复制文件夹：

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

使用 junction 意味着通过 SteamCMD 的更新会自动应用——无需重新复制。

### 步骤 3：复制 .bikey

见下一节。

---

## Mod 密钥 (.bikey)

每个已签名的 mod 都附带一个 `keys/` 文件夹，其中包含一个或多个 `.bikey` 文件。这些文件告诉 BattlEye 接受哪些 PBO 签名。

1. 打开 mod 文件夹（例如 `@CF/keys/`）
2. 将每个 `.bikey` 文件复制到服务器根目录的 `keys/` 目录

```
DayZServer/
  keys/
    dayz.bikey              # 原版 -- 始终存在
    cf.bikey                # 从 @CF/keys/ 复制
    vpp_admintools.bikey    # 从 @VPPAdminTools/keys/ 复制
```

没有正确的密钥，运行该 mod 的所有玩家都会收到：**"Player kicked: Modified data"**。

---

## 加载顺序与依赖关系

Mod 在 `-mod=` 参数中从左到右加载。Mod 的 `config.cpp` 声明其依赖：

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

如果 `MyMod` 依赖 `CF`，那么 `@CF` 必须在启动参数中出现在 `@MyMod` **之前**：

```
-mod=@CF;@MyMod          正确
-mod=@MyMod;@CF          错误 -- 崩溃或缺少类
```

**通用加载顺序模式：**

1. **框架 mod** -- CF, Community-Online-Tools
2. **库 mod** -- BuilderItems, 任何共享资源包
3. **功能 mod** -- 地图扩展、武器、载具
4. **依赖 mod** -- 将上述列为 `requiredAddons` 的任何 mod

如有疑问，查看 mod 的 Workshop 页面或文档。大多数 mod 作者会公布所需的加载顺序。

---

## 仅服务器端与客户端必需的 Mod

| 参数 | 谁需要 | 典型示例 |
|------|--------|----------|
| `-mod=` | 服务器 + 所有客户端 | 武器、载具、地图、UI mod、服装 |
| `-servermod=` | 仅服务器 | 经济管理器、日志工具、管理后台、调度脚本 |

规则很简单：如果 mod 包含**任何**客户端侧脚本、布局、纹理或模型，它必须放在 `-mod=` 中。如果它只运行服务器端逻辑且没有客户端会接触到的资源，使用 `-servermod=`。

将仅服务器端 mod 放在 `-mod=` 中会强制每个玩家下载它。将客户端必需的 mod 放在 `-servermod=` 中会导致客户端出现纹理缺失、UI 损坏或脚本错误。

---

## 更新 Mod

### 流程

1. **停止服务器** -- 在服务器运行时更新文件可能损坏 PBO
2. **重新下载** 通过 SteamCMD：
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **复制更新后的 .bikey 文件** -- mod 作者偶尔会轮换签名密钥。始终将新的 `.bikey` 从 mod 的 `keys/` 文件夹复制到服务器的 `keys/` 目录
4. **重启服务器**

如果你使用了符号链接（junction），步骤 2 会就地更新 mod 文件。如果你手动复制了文件，则需要再次复制。

### 客户端更新

在 Steam Workshop 上订阅了 mod 的玩家会自动收到更新。如果你在服务器上更新了 mod 但玩家有旧版本，他们会收到签名不匹配的提示，直到客户端更新后才能连接。

---

## 排查 Mod 冲突

### 检查 RPT 日志

打开 `profiles/` 中最新的 `.RPT` 文件。搜索：

- **"Cannot register"** -- 两个 mod 之间的类名冲突
- **"Missing addons"** -- 依赖项未加载（错误的加载顺序或缺少 mod）
- **"Signature verification failed"** -- `.bikey` 不匹配或缺少密钥

### 检查脚本日志

打开 `profiles/` 中最新的 `script_*.log`。查找：

- **"SCRIPT (E)"** 行 -- 脚本错误，通常由加载顺序或版本不匹配导致
- **"Definition of variable ... already exists"** -- 两个 mod 定义了相同的类

### 隔离问题

当你有很多 mod 且出了问题时，逐步测试：

1. 只启动框架 mod（`@CF`）
2. 一次添加一个 mod
3. 每次添加后启动并检查日志
4. 导致错误的 mod 就是问题所在

### 两个 Mod 编辑同一个类

如果两个 mod 都使用 `modded class PlayerBase`，**最后**加载的那个（`-mod=` 中最右边的）胜出。它的 `super` 调用会链接到另一个 mod 的版本。这通常可以工作，但如果一个 mod 在覆盖方法时没有调用 `super`，另一个 mod 的更改就会丢失。

---

## 常见错误

**加载顺序错误。** 服务器崩溃或记录"Missing addons"，因为依赖项尚未加载。修复：将依赖 mod 移到 `-mod=` 列表中更前面的位置。

**忘记将仅服务器端 mod 放在 `-servermod=` 中。** 玩家被迫下载他们不需要的 mod。修复：将仅服务器端 mod 从 `-mod=` 移到 `-servermod=`。

**Mod 更新后不更新 `.bikey` 文件。** 玩家被踢出并显示"Modified data"，因为服务器的密钥与 mod 的新 PBO 签名不匹配。修复：更新 mod 时始终重新复制 `.bikey` 文件。

**重新打包 mod PBO。** 重新打包 mod 的 PBO 文件会破坏其数字签名，导致每个玩家被 BattlEye 踢出，并违反大多数 mod 作者的条款。永远不要重新打包你未创建的 mod。

**混合使用 Workshop 路径和本地路径。** 对某些 mod 使用原始 Workshop 数字路径，对其他 mod 使用命名文件夹，在更新时会造成混乱。选择一种方法——符号链接是最整洁的。

**Mod 路径中有空格。** 类似 `-mod=@My Mod` 的路径会破坏解析。重命名 mod 文件夹以避免空格，或将整个参数用引号括起：`-mod="@My Mod;@CF"`。

**服务器上 mod 过期，客户端已更新（或反之）。** 版本不匹配导致无法连接。保持服务器和 Workshop 版本同步。同时更新所有 mod 和服务器。

---

[首页](../README.md) | [<< 上一章: 访问控制](09-access-control.md) | [下一章: 故障排除 >>](11-troubleshooting.md)
