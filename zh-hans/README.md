# DayZ Mod 开发百科全书（简体中文版）

> 本文档从英文版翻译而来。代码示例保持原样，技术术语保留英文。

---

## 目录

### 第一部分：Enforce Script 语言

| 章节 | 主题 | 说明 |
|------|------|------|
| [1.1](01-enforce-script/01-variables-types.md) | 变量与类型 | 基本类型、声明、类型转换 |
| [1.2](01-enforce-script/02-arrays-maps-sets.md) | 数组、映射与集合 | `array<T>`、`map<K,V>`、`set<T>` |
| [1.3](01-enforce-script/03-classes-inheritance.md) | 类与继承 | 类声明、继承、访问修饰符 |
| [1.4](01-enforce-script/04-modded-classes.md) | Modded 类 | DayZ Mod 开发的核心机制 |
| [1.5](01-enforce-script/05-control-flow.md) | 控制流 | if/else、for、while、foreach、switch |
| [1.6](01-enforce-script/06-strings.md) | 字符串操作 | 完整的字符串方法参考 |
| [1.7](01-enforce-script/07-math-vectors.md) | 数学与向量 | Math 类、vector 类型、3D 运算 |
| [1.8](01-enforce-script/08-memory-management.md) | 内存管理 | ref、autoptr、引用计数、循环引用 |
| [1.9](01-enforce-script/09-casting-reflection.md) | 类型转换与反射 | CastTo、IsInherited、反射 API |
| [1.10](01-enforce-script/10-enums-preprocessor.md) | 枚举与预处理器 | enum、#ifdef、条件编译 |
| [1.11](01-enforce-script/11-error-handling.md) | 错误处理 | 守卫子句、ErrorEx、日志记录 |
| [1.12](01-enforce-script/12-gotchas.md) | 陷阱大全 | 30 个常见"坑"与解决方案 |

### 第二部分：Mod 结构

| 章节 | 主题 | 说明 |
|------|------|------|
| [2.1](02-mod-structure/01-five-layers.md) | 五层脚本层次结构 | 1_Core 到 5_Mission 的编译层级 |
| [2.2](02-mod-structure/02-config-cpp.md) | config.cpp 深入解析 | CfgPatches、CfgMods、脚本模块 |
| [2.3](02-mod-structure/03-mod-cpp.md) | mod.cpp 与 Workshop | 启动器元数据、Workshop 发布 |
| [2.4](02-mod-structure/04-minimum-viable-mod.md) | 你的第一个 Mod | 从零开始的最小可行 Mod |
| [2.5](02-mod-structure/05-file-organization.md) | 文件组织最佳实践 | 目录结构、命名规范、PBO 组织 |

### 第三部分：GUI 系统

| 章节 | 主题 | 说明 |
|------|------|------|
| [3.1](03-gui-system/01-widget-types.md) | Widget 类型 | 所有 Widget 类型参考 |
| [3.2](03-gui-system/02-layout-files.md) | 布局文件 | .layout XML 格式 |
| [3.3](03-gui-system/03-sizing-positioning.md) | 尺寸与定位 | 锚点、对齐、尺寸模式 |
| [3.4](03-gui-system/04-containers.md) | 容器 | 面板布局、滚动、网格 |
| [3.5](03-gui-system/05-programmatic-widgets.md) | 代码创建 Widget | 代码中创建和操作 Widget |
| [3.6](03-gui-system/06-event-handling.md) | 事件处理 | 输入事件、回调、焦点 |
| [3.7](03-gui-system/07-styles-fonts.md) | 样式与字体 | .styles 文件、字体、主题 |

### 第四部分：文件格式

| 章节 | 主题 | 说明 |
|------|------|------|
| [4.1](04-file-formats/01-textures.md) | 纹理 | .paa、.edds 格式、TexView2 |
| [4.2](04-file-formats/02-models.md) | 模型 | .p3d 格式、Object Builder |
| [4.3](04-file-formats/03-materials.md) | 材质 | .rvmat 格式、着色器 |
| [4.4](04-file-formats/04-audio.md) | 音频 | .ogg 格式、CfgSoundSets |
| [4.5](04-file-formats/05-dayz-tools.md) | DayZ Tools | 工具套件概览 |
| [4.6](04-file-formats/06-pbo-packing.md) | PBO 打包 | 打包、签名、部署 |

### 第五部分：配置文件

| 章节 | 主题 | 说明 |
|------|------|------|
| [5.1](05-config-files/01-stringtable.md) | 字符串表 | stringtable.csv 本地化 |
| [5.2](05-config-files/02-inputs-xml.md) | 输入绑定 | Inputs.xml 按键绑定 |
| [5.3](05-config-files/03-credits-json.md) | Credits.json | 作者署名文件 |
| [5.4](05-config-files/04-imagesets.md) | ImageSets | 图标集与纹理图集 |

### 第六部分：引擎 API

| 章节 | 主题 | 说明 |
|------|------|------|
| [6.1](06-engine-api/01-entity-system.md) | 实体系统 | Object、EntityAI、生命周期 |
| [6.2](06-engine-api/02-vehicles.md) | 载具 | CarScript、引擎、物理 |
| [6.3](06-engine-api/03-weather.md) | 天气 | Weather API、雾、风、雨 |
| [6.4](06-engine-api/04-cameras.md) | 摄像机 | 摄像机类型、自定义视角 |
| [6.5](06-engine-api/05-ppe.md) | 后处理效果 | PPE 材质、模糊、色调 |
| [6.6](06-engine-api/06-notifications.md) | 通知 | 通知系统 API |
| [6.7](06-engine-api/07-timers.md) | 定时器 | CallLater、Timer、调度 |
| [6.8](06-engine-api/08-file-io.md) | 文件 I/O | 文件读写、JSON、路径 |
| [6.9](06-engine-api/09-networking.md) | 网络 | RPC、同步变量、复制 |
| [6.10](06-engine-api/10-central-economy.md) | 中央经济 | types.xml、生成系统 |

### 第七部分：设计模式

| 章节 | 主题 | 说明 |
|------|------|------|
| [7.1](07-patterns/01-singletons.md) | 单例模式 | 全局管理器模式 |
| [7.2](07-patterns/02-module-systems.md) | 模块系统 | 模块注册与生命周期 |
| [7.3](07-patterns/03-rpc-patterns.md) | RPC 模式 | 远程过程调用最佳实践 |
| [7.4](07-patterns/04-config-persistence.md) | 配置持久化 | JSON 配置加载/保存 |
| [7.5](07-patterns/05-permissions.md) | 权限系统 | 权限检查与管理 |
| [7.6](07-patterns/06-events.md) | 事件系统 | 事件总线、发布/订阅 |
| [7.7](07-patterns/07-performance.md) | 性能优化 | 性能陷阱与优化技巧 |

### 第八部分：教程

| 章节 | 主题 | 说明 |
|------|------|------|
| [8.1](08-tutorials/01-first-mod.md) | 第一个 Mod | 完整的入门教程 |
| [8.2](08-tutorials/02-custom-item.md) | 自定义物品 | 创建自定义游戏物品 |
| [8.3](08-tutorials/03-admin-panel.md) | 管理面板 | 构建管理员面板 |
| [8.4](08-tutorials/04-chat-commands.md) | 聊天命令 | 实现聊天命令系统 |

### 速查表

| 页面 | 说明 |
|------|------|
| [速查表](cheatsheet.md) | 单页 Enforce Script 快速参考 |

---

> 翻译说明：所有代码示例保持英文原样。技术术语（如 `modded class`、`override`、`ref` 等）保留英文，并在首次出现时给出中文解释。导航链接指向中文版页面。
