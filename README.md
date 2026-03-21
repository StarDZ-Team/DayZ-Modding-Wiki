# DayZ Modding Complete Guide

> The most comprehensive DayZ modding documentation available. From zero to published mod.

[![English](https://flagsapi.com/US/flat/48.png)](en/README.md) [![Português](https://flagsapi.com/BR/flat/48.png)](pt/README.md) [![Deutsch](https://flagsapi.com/DE/flat/48.png)](de/README.md) [![Русский](https://flagsapi.com/RU/flat/48.png)](ru/README.md) [![Čeština](https://flagsapi.com/CZ/flat/48.png)](cs/README.md) [![Polski](https://flagsapi.com/PL/flat/48.png)](pl/README.md) [![Magyar](https://flagsapi.com/HU/flat/48.png)](hu/README.md) [![Italiano](https://flagsapi.com/IT/flat/48.png)](it/README.md) [![Español](https://flagsapi.com/ES/flat/48.png)](es/README.md) [![Français](https://flagsapi.com/FR/flat/48.png)](fr/README.md) [![中文](https://flagsapi.com/CN/flat/48.png)](zh/README.md) [![日本語](https://flagsapi.com/JP/flat/48.png)](ja/README.md) [![简体中文](https://flagsapi.com/CN/flat/48.png)](zh-hans/README.md)

---

## Table of Contents

### Part 1: Enforce Script Language
Learn DayZ's scripting language from the ground up.

| Chapter | Topic | Status |
|---------|-------|--------|
| [1.1](en/01-enforce-script/01-variables-types.md) | Variables & Types | ✅ |
| [1.2](en/01-enforce-script/02-arrays-maps-sets.md) | Arrays, Maps & Sets | ✅ |
| [1.3](en/01-enforce-script/03-classes-inheritance.md) | Classes & Inheritance | ✅ |
| [1.4](en/01-enforce-script/04-modded-classes.md) | Modded Classes | ✅ |
| [1.5](en/01-enforce-script/05-control-flow.md) | Control Flow | ✅ |
| [1.6](en/01-enforce-script/06-strings.md) | String Operations | ✅ |
| [1.7](en/01-enforce-script/07-math-vectors.md) | Math & Vectors | ✅ |
| [1.8](en/01-enforce-script/08-memory-management.md) | Memory Management | ✅ |
| [1.9](en/01-enforce-script/09-casting-reflection.md) | Casting & Reflection | ✅ |
| [1.10](en/01-enforce-script/10-enums-preprocessor.md) | Enums & Preprocessor | ✅ |
| [1.11](en/01-enforce-script/11-error-handling.md) | Error Handling | ✅ |
| [1.12](en/01-enforce-script/12-gotchas.md) | What Does NOT Exist | ✅ |

### Part 2: Mod Structure
Understand how DayZ mods are organized.

| Chapter | Topic | Status |
|---------|-------|--------|
| [2.1](en/02-mod-structure/01-five-layers.md) | The 5-Layer Script Hierarchy | ✅ |
| [2.2](en/02-mod-structure/02-config-cpp.md) | config.cpp Deep Dive | ✅ |
| [2.3](en/02-mod-structure/03-mod-cpp.md) | mod.cpp & Workshop | ✅ |
| [2.4](en/02-mod-structure/04-minimum-viable-mod.md) | Your First Mod | ✅ |
| [2.5](en/02-mod-structure/05-file-organization.md) | File Organization | ✅ |

### Part 3: GUI & Layout System
Build user interfaces for DayZ.

| Chapter | Topic | Status |
|---------|-------|--------|
| [3.1](en/03-gui-system/01-widget-types.md) | Widget Types | ✅ |
| [3.2](en/03-gui-system/02-layout-files.md) | Layout File Format | ✅ |
| [3.3](en/03-gui-system/03-sizing-positioning.md) | Sizing & Positioning | ✅ |
| [3.4](en/03-gui-system/04-containers.md) | Container Widgets | ✅ |
| [3.5](en/03-gui-system/05-programmatic-widgets.md) | Programmatic Creation | ✅ |
| [3.6](en/03-gui-system/06-event-handling.md) | Event Handling | ✅ |
| [3.7](en/03-gui-system/07-styles-fonts.md) | Styles, Fonts & Images | ✅ |

### Part 4: File Formats & Tools
Working with DayZ asset pipeline.

| Chapter | Topic | Status |
|---------|-------|--------|
| [4.1](en/04-file-formats/01-textures.md) | Textures (.paa, .edds, .tga) | ✅ |
| [4.2](en/04-file-formats/02-models.md) | 3D Models (.p3d) | ✅ |
| [4.3](en/04-file-formats/03-materials.md) | Materials (.rvmat) | ✅ |
| [4.4](en/04-file-formats/04-audio.md) | Audio (.ogg, .wss) | ✅ |
| [4.5](en/04-file-formats/05-dayz-tools.md) | DayZ Tools Workflow | ✅ |
| [4.6](en/04-file-formats/06-pbo-packing.md) | PBO Packing | ✅ |

### Part 5: Configuration Files
Essential configuration files for every mod.

| Chapter | Topic | Status |
|---------|-------|--------|
| [5.1](en/05-config-files/01-stringtable.md) | stringtable.csv (13 Languages) | ✅ |
| [5.2](en/05-config-files/02-inputs-xml.md) | Inputs.xml (Keybindings) | ✅ |
| [5.3](en/05-config-files/03-credits-json.md) | Credits.json | ✅ |
| [5.4](en/05-config-files/04-imagesets.md) | ImageSet Format | ✅ |

### Part 6: Engine API Reference
DayZ engine APIs for mod developers.

| Chapter | Topic | Status |
|---------|-------|--------|
| [6.1](en/06-engine-api/01-entity-system.md) | Entity System | ✅ |
| [6.2](en/06-engine-api/02-vehicles.md) | Vehicle System | ✅ |
| [6.3](en/06-engine-api/03-weather.md) | Weather System | ✅ |
| [6.4](en/06-engine-api/04-cameras.md) | Camera System | ✅ |
| [6.5](en/06-engine-api/05-ppe.md) | Post-Process Effects | ✅ |
| [6.6](en/06-engine-api/06-notifications.md) | Notification System | ✅ |
| [6.7](en/06-engine-api/07-timers.md) | Timers & CallQueue | ✅ |
| [6.8](en/06-engine-api/08-file-io.md) | File I/O & JSON | ✅ |
| [6.9](en/06-engine-api/09-networking.md) | Networking & RPC | ✅ |
| [6.10](en/06-engine-api/10-central-economy.md) | Central Economy | ✅ |

### Part 7: Patterns & Best Practices
Battle-tested patterns from professional mods.

| Chapter | Topic | Status |
|---------|-------|--------|
| [7.1](en/07-patterns/01-singletons.md) | Singleton Pattern | ✅ |
| [7.2](en/07-patterns/02-module-systems.md) | Module/Plugin Systems | ✅ |
| [7.3](en/07-patterns/03-rpc-patterns.md) | RPC Communication | ✅ |
| [7.4](en/07-patterns/04-config-persistence.md) | Config Persistence | ✅ |
| [7.5](en/07-patterns/05-permissions.md) | Permission Systems | ✅ |
| [7.6](en/07-patterns/06-events.md) | Event-Driven Architecture | ✅ |
| [7.7](en/07-patterns/07-performance.md) | Performance Optimization | ✅ |

### Part 8: Tutorials
Step-by-step guides.

| Chapter | Topic | Status |
|---------|-------|--------|
| [8.1](en/08-tutorials/01-first-mod.md) | Your First Mod (Hello World) | ✅ |
| [8.2](en/08-tutorials/02-custom-item.md) | Creating a Custom Item | ✅ |
| [8.3](en/08-tutorials/03-admin-panel.md) | Building an Admin Panel | ✅ |
| [8.4](en/08-tutorials/04-chat-commands.md) | Adding Chat Commands | ✅ |
| [8.5](en/08-tutorials/05-mod-template.md) | Using the DayZ Mod Template | ✅ |

---

## Supported Languages

| | Language | Code | Pages | Status |
|:-:|----------|------|-------|--------|
| [![](https://flagsapi.com/US/flat/24.png)](en/README.md) | [English](en/README.md) | `en` | 56 | ✅ Complete |
| [![](https://flagsapi.com/BR/flat/24.png)](pt/README.md) | [Português (BR)](pt/README.md) | `pt` | 57 | ✅ Complete |
| [![](https://flagsapi.com/DE/flat/24.png)](de/README.md) | [Deutsch](de/README.md) | `de` | 57 | ✅ Complete |
| [![](https://flagsapi.com/RU/flat/24.png)](ru/README.md) | [Русский](ru/README.md) | `ru` | 57 | ✅ Complete |
| [![](https://flagsapi.com/CZ/flat/24.png)](cs/README.md) | [Čeština](cs/README.md) | `cs` | 56 | ✅ Complete |
| [![](https://flagsapi.com/PL/flat/24.png)](pl/README.md) | [Polski](pl/README.md) | `pl` | 57 | ✅ Complete |
| [![](https://flagsapi.com/HU/flat/24.png)](hu/README.md) | [Magyar](hu/README.md) | `hu` | 57 | ✅ Complete |
| [![](https://flagsapi.com/IT/flat/24.png)](it/README.md) | [Italiano](it/README.md) | `it` | 57 | ✅ Complete |
| [![](https://flagsapi.com/ES/flat/24.png)](es/README.md) | [Español](es/README.md) | `es` | 57 | ✅ Complete |
| [![](https://flagsapi.com/FR/flat/24.png)](fr/README.md) | [Français](fr/README.md) | `fr` | 57 | ✅ Complete |
| [![](https://flagsapi.com/CN/flat/24.png)](zh/README.md) | [中文](zh/README.md) | `zh` | 57 | ✅ Complete |
| [![](https://flagsapi.com/JP/flat/24.png)](ja/README.md) | [日本語](ja/README.md) | `ja` | 57 | ✅ Complete |
| [![](https://flagsapi.com/CN/flat/24.png)](zh-hans/README.md) | [简体中文](zh-hans/README.md) | `zh-hans` | 57 | ✅ Complete |

---

## Quick Reference

- [Enforce Script Cheat Sheet](en/cheatsheet.md)
- [Widget Type Reference](en/03-gui-system/01-widget-types.md)
- [API Quick Reference](en/06-engine-api/quick-reference.md)
- [Common Gotchas](en/01-enforce-script/12-gotchas.md)

---

## Contributing

This documentation was compiled by studying:
- 10+ professional DayZ mods (COT, VPP, Expansion, Dabs Framework, DayZ Editor, Colorful UI)
- 15 official Bohemia Interactive sample mods
- 2,800+ vanilla DayZ script files
- Community Framework source code

Pull requests welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Credits

This documentation was made possible by studying the work of these incredible developers and their open-source projects:

| Developer | GitHub | Projects | Contribution |
|-----------|--------|----------|--------------|
| **Jacob_Mango** | [@Jacob-Mango](https://github.com/Jacob-Mango) | Community Framework, Community Online Tools | Module system, RPC patterns, permissions, ESP, vehicle management |
| **InclementDab** | [@InclementDab](https://github.com/InclementDab) | Dabs Framework, DayZ Editor, Mod Template | MVC architecture, ViewBinding, widget patterns, editor UI |
| **salutesh** | [@salutesh](https://github.com/salutesh) | DayZ Expansion Scripts | Market system, party system, map markers, notification system, vehicle modules |
| **Arkensor** | [@Arkensor](https://github.com/Arkensor) | DayZ Expansion Scripts | Central economy, settings versioning, anti-cheat patterns |
| **DaOne** | [@Da0ne](https://github.com/Da0ne) | VPP Admin Tools | Player management, chat commands, webhook system, ESP tools |
| **GravityWolf** | [@GravityWolfNotAmused](https://github.com/GravityWolfNotAmused) | VPP Admin Tools | Permission system, server management, teleport system |
| **Bohemia Interactive** | [@BohemiaInteractive](https://github.com/BohemiaInteractive/) | DayZ Engine & Official Samples | Enforce Script engine, vanilla scripts, DayZ Tools, sample mods |
| **StarDZ Team** | [@StarDZ-Team](https://github.com/StarDZ-Team) | — | Documentation compilation, translation & organization |

## License

This documentation is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Code examples are licensed under [MIT](https://opensource.org/licenses/MIT).
