# Chapter 9.9: 访问控制

[首页](../README.md) | [<< 上一章: 性能调优](08-performance.md) | [下一章: Mod 管理 >>](10-mod-management.md)

---

> **摘要:** 配置谁可以连接你的 DayZ 服务器、封禁如何工作、如何启用远程管理，以及 mod 签名验证如何阻止未授权内容。本章涵盖服务器运营者可用的所有访问控制机制。

---

## 目录

- [通过 serverDZ.cfg 进行管理员访问](#通过-serverdzcfg-进行管理员访问)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [BattlEye 反作弊](#battleye-反作弊)
- [RCON（远程控制台）](#rcon远程控制台)
- [签名验证](#签名验证)
- [keys/ 目录](#keys-目录)
- [游戏内管理工具](#游戏内管理工具)
- [常见错误](#常见错误)

---

## 通过 serverDZ.cfg 进行管理员访问

**serverDZ.cfg** 中的 `passwordAdmin` 参数设置服务器的管理员密码：

```cpp
passwordAdmin = "YourSecretPassword";
```

此密码有两种使用方式：

1. **游戏内** -- 打开聊天并输入 `#login YourSecretPassword` 以获得该会话的管理员权限。
2. **RCON** -- 使用 BattlEye RCON 客户端通过此密码连接（见下面的 RCON 部分）。

保持管理员密码长且唯一。拥有此密码的任何人都可以完全控制运行中的服务器。

---

## ban.txt

**ban.txt** 文件位于你的服务器配置目录中（你用 `-profiles=` 设置的路径）。它每行包含一个 SteamID64：

```
76561198012345678
76561198087654321
```

- 每行是一个纯粹的 17 位 SteamID64 -- 没有名称、没有注释、没有密码。
- SteamID 出现在此文件中的玩家在加入时被拒绝连接。
- 你可以在服务器运行时编辑此文件；更改在下次连接尝试时生效。

---

## whitelist.txt

**whitelist.txt** 文件位于同一配置目录中。当你启用白名单时，只有此文件中列出的 SteamID 才能连接：

```
76561198012345678
76561198087654321
```

格式与 **ban.txt** 相同 -- 每行一个 SteamID64，没有其他内容。

白名单适用于私人社区、测试服务器或需要受控玩家列表的活动。

---

## BattlEye 反作弊

BattlEye 是集成在 DayZ 中的反作弊系统。其文件位于服务器目录内的 `BattlEye/` 文件夹中：

| 文件 | 用途 |
|------|------|
| **BEServer_x64.dll** | BattlEye 反作弊引擎二进制文件 |
| **beserver_x64.cfg** | 配置文件（RCON 端口、RCON 密码） |
| **bans.txt** | BattlEye 特有的封禁（基于 GUID，不是 SteamID） |

BattlEye 默认启用。你使用 `DayZServer_x64.exe` 启动服务器，BattlEye 自动加载。要显式禁用它（不推荐用于生产环境），使用 `-noBE` 启动参数。

`BattlEye/` 文件夹中的 **bans.txt** 文件使用 BattlEye GUID，这与 SteamID64 不同。通过 RCON 或 BattlEye 命令发出的封禁会自动写入此文件。

---

## RCON（远程控制台）

BattlEye RCON 让你无需在游戏中即可远程管理服务器。在 `BattlEye/beserver_x64.cfg` 中配置：

```
RConPassword yourpassword
RConPort 2306
```

默认 RCON 端口是游戏端口加 4。如果你的服务器运行在端口 `2302`，RCON 默认为 `2306`。

### 可用的 RCON 命令

| 命令 | 效果 |
|------|------|
| `kick <player> [reason]` | 将玩家从服务器踢出 |
| `ban <player> [minutes] [reason]` | 封禁玩家（写入 BattlEye bans.txt） |
| `say -1 <message>` | 向所有玩家广播消息 |
| `#shutdown` | 正常关闭服务器 |
| `#lock` | 锁定服务器（不接受新连接） |
| `#unlock` | 解锁服务器 |
| `players` | 列出已连接的玩家 |

你使用 BattlEye RCON 客户端连接到 RCON（有多个免费工具可用）。连接需要 IP、RCON 端口和 **beserver_x64.cfg** 中的密码。

---

## 签名验证

**serverDZ.cfg** 中的 `verifySignatures` 参数控制服务器是否检查 mod 签名：

```cpp
verifySignatures = 2;
```

| 值 | 行为 |
|------|------|
| `0` | 禁用 -- 任何人可以携带任何 mod 加入，不进行签名检查 |
| `2` | 完全验证 -- 客户端加载的所有 mod 必须有有效签名（默认） |

在生产服务器上始终使用 `verifySignatures = 2`。设为 `0` 允许玩家携带修改过的或未签名的 mod 加入，这是严重的安全风险。

---

## keys/ 目录

服务器根目录中的 `keys/` 目录保存 **.bikey** 文件。每个 `.bikey` 对应一个 mod，告诉服务器"此 mod 的签名是可信的。"

当 `verifySignatures = 2` 时：

1. 服务器检查连接客户端加载的每个 mod。
2. 对于每个 mod，服务器在 `keys/` 中查找匹配的 `.bikey`。
3. 如果缺少匹配的密钥，玩家被踢出。

你在服务器上安装的每个 mod 都附带一个 `.bikey` 文件（通常在 mod 的 `Keys/` 或 `Key/` 子文件夹中）。你将该文件复制到服务器的 `keys/` 目录中。

```
DayZServer/
├── keys/
│   ├── dayz.bikey              <- 原版（始终存在）
│   ├── MyMod.bikey             <- 从 @MyMod/Keys/ 复制
│   └── AnotherMod.bikey        <- 从 @AnotherMod/Keys/ 复制
```

如果你添加了新 mod 但忘记复制其 `.bikey`，运行该 mod 的每个玩家在连接时都会被踢出。

---

## 游戏内管理工具

在聊天中使用 `#login <password>` 登录后，你可以访问管理工具：

- **玩家列表** -- 查看所有已连接玩家及其 SteamID。
- **踢出/封禁** -- 直接从玩家列表中移除或封禁玩家。
- **传送** -- 使用管理地图传送到任何位置。
- **管理日志** -- 服务器端的玩家操作日志（击杀、连接、断开连接），写入配置目录中的 `*.ADM` 文件。
- **自由摄像机** -- 从你的角色脱离并在地图上飞行。

这些工具内置在原版游戏中。第三方 mod（如 Community Online Tools）显著扩展了管理功能。

---

## 常见错误

这些是服务器运营者最常遇到的问题：

| 错误 | 症状 | 修复 |
|------|------|------|
| `keys/` 中缺少 `.bikey` | 玩家加入时被踢出，显示签名错误 | 将 mod 的 `.bikey` 文件复制到服务器的 `keys/` 目录 |
| 在 **ban.txt** 中放入名称或密码 | 封禁不起作用；随机错误 | 只使用纯粹的 SteamID64 值，每行一个 |
| RCON 端口冲突 | RCON 客户端无法连接 | 确保 RCON 端口未被其他服务使用；检查防火墙规则 |
| 生产环境中 `verifySignatures = 0` | 任何人可以携带篡改过的 mod 加入 | 在任何面向公众的服务器上设为 `2` |
| 忘记在防火墙中开放 RCON 端口 | RCON 客户端超时 | 在防火墙中开放 RCON UDP 端口（默认 2306） |
| 用 SteamID 编辑 `BattlEye/` 中的 **bans.txt** | 封禁不起作用 | BattlEye 的 **bans.txt** 使用 GUID，不是 SteamID；使用配置目录中的 **ban.txt** 进行 SteamID 封禁 |

---

[首页](../README.md) | [<< 上一章: 性能调优](08-performance.md) | [下一章: Mod 管理 >>](10-mod-management.md)
