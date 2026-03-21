# Полное руководство по моддингу DayZ

> Самая подробная документация по моддингу DayZ. От нуля до опубликованного мода.

[![English](https://flagsapi.com/US/flat/48.png)](../en/README.md) [![Português](https://flagsapi.com/BR/flat/48.png)](../pt/README.md) [![Deutsch](https://flagsapi.com/DE/flat/48.png)](../de/README.md) [![Русский](https://flagsapi.com/RU/flat/48.png)](README.md) [![Čeština](https://flagsapi.com/CZ/flat/48.png)](../cs/README.md) [![Polski](https://flagsapi.com/PL/flat/48.png)](../pl/README.md) [![Magyar](https://flagsapi.com/HU/flat/48.png)](../hu/README.md) [![Italiano](https://flagsapi.com/IT/flat/48.png)](../it/README.md) [![Español](https://flagsapi.com/ES/flat/48.png)](../es/README.md) [![Français](https://flagsapi.com/FR/flat/48.png)](../fr/README.md) [![中文](https://flagsapi.com/CN/flat/48.png)](../zh/README.md) [![日本語](https://flagsapi.com/JP/flat/48.png)](../ja/README.md)

---

## Содержание

### Часть 1: Язык Enforce Script
Изучите скриптовый язык DayZ с нуля.

| Глава | Тема | Статус |
|-------|------|--------|
| [1.1](01-enforce-script/01-variables-types.md) | Переменные и типы | ✅ |
| [1.2](01-enforce-script/02-arrays-maps-sets.md) | Arrays, Maps и Sets | ✅ |
| [1.3](01-enforce-script/03-classes-inheritance.md) | Классы и наследование | ✅ |
| [1.4](01-enforce-script/04-modded-classes.md) | Modded-классы | ✅ |
| [1.5](01-enforce-script/05-control-flow.md) | Управление потоком выполнения | ✅ |
| [1.6](01-enforce-script/06-strings.md) | Операции со строками | ✅ |
| [1.7](01-enforce-script/07-math-vectors.md) | Математика и векторы | ✅ |
| [1.8](01-enforce-script/08-memory-management.md) | Управление памятью | ✅ |
| [1.9](01-enforce-script/09-casting-reflection.md) | Casting и Reflection | ✅ |
| [1.10](01-enforce-script/10-enums-preprocessor.md) | Enums и препроцессор | ✅ |
| [1.11](01-enforce-script/11-error-handling.md) | Обработка ошибок | ✅ |
| [1.12](01-enforce-script/12-gotchas.md) | Чего НЕ существует | ✅ |

### Часть 2: Структура мода
Разберитесь, как организованы моды DayZ.

| Глава | Тема | Статус |
|-------|------|--------|
| [2.1](02-mod-structure/01-five-layers.md) | 5-уровневая иерархия скриптов | ✅ |
| [2.2](02-mod-structure/02-config-cpp.md) | config.cpp подробно | ✅ |
| [2.3](02-mod-structure/03-mod-cpp.md) | mod.cpp и Workshop | ✅ |
| [2.4](02-mod-structure/04-minimum-viable-mod.md) | Ваш первый мод | ✅ |
| [2.5](02-mod-structure/05-file-organization.md) | Организация файлов | ✅ |

### Часть 3: Система GUI и Layout
Создавайте пользовательские интерфейсы для DayZ.

| Глава | Тема | Статус |
|-------|------|--------|
| [3.1](03-gui-system/01-widget-types.md) | Типы виджетов | ✅ |
| [3.2](03-gui-system/02-layout-files.md) | Формат файлов Layout | ✅ |
| [3.3](03-gui-system/03-sizing-positioning.md) | Размеры и позиционирование | ✅ |
| [3.4](03-gui-system/04-containers.md) | Виджеты-контейнеры | ✅ |
| [3.5](03-gui-system/05-programmatic-widgets.md) | Программное создание | ✅ |
| [3.6](03-gui-system/06-event-handling.md) | Обработка событий | ✅ |
| [3.7](03-gui-system/07-styles-fonts.md) | Стили, шрифты и изображения | ✅ |

### Часть 4: Форматы файлов и инструменты
Работа с конвейером ресурсов DayZ.

| Глава | Тема | Статус |
|-------|------|--------|
| [4.1](04-file-formats/01-textures.md) | Текстуры (.paa, .edds, .tga) | ✅ |
| [4.2](04-file-formats/02-models.md) | 3D-модели (.p3d) | ✅ |
| [4.3](04-file-formats/03-materials.md) | Материалы (.rvmat) | ✅ |
| [4.4](04-file-formats/04-audio.md) | Аудио (.ogg, .wss) | ✅ |
| [4.5](04-file-formats/05-dayz-tools.md) | Рабочий процесс DayZ Tools | ✅ |
| [4.6](04-file-formats/06-pbo-packing.md) | Упаковка PBO | ✅ |

### Часть 5: Файлы конфигурации
Основные конфигурационные файлы для каждого мода.

| Глава | Тема | Статус |
|-------|------|--------|
| [5.1](05-config-files/01-stringtable.md) | stringtable.csv (13 языков) | ✅ |
| [5.2](05-config-files/02-inputs-xml.md) | Inputs.xml (привязки клавиш) | ✅ |
| [5.3](05-config-files/03-credits-json.md) | Credits.json | ✅ |
| [5.4](05-config-files/04-imagesets.md) | Формат ImageSet | ✅ |

### Часть 6: Справочник API движка
API движка DayZ для разработчиков модов.

| Глава | Тема | Статус |
|-------|------|--------|
| [6.1](06-engine-api/01-entity-system.md) | Система сущностей | ✅ |
| [6.2](06-engine-api/02-vehicles.md) | Система транспорта | ✅ |
| [6.3](06-engine-api/03-weather.md) | Система погоды | ✅ |
| [6.4](06-engine-api/04-cameras.md) | Система камер | ✅ |
| [6.5](06-engine-api/05-ppe.md) | Эффекты постобработки | ✅ |
| [6.6](06-engine-api/06-notifications.md) | Система уведомлений | ✅ |
| [6.7](06-engine-api/07-timers.md) | Таймеры и CallQueue | ✅ |
| [6.8](06-engine-api/08-file-io.md) | Файловый ввод-вывод и JSON | ✅ |
| [6.9](06-engine-api/09-networking.md) | Сетевое взаимодействие и RPC | ✅ |
| [6.10](06-engine-api/10-central-economy.md) | Центральная экономика | ✅ |

### Часть 7: Паттерны и лучшие практики
Проверенные в бою паттерны из профессиональных модов.

| Глава | Тема | Статус |
|-------|------|--------|
| [7.1](07-patterns/01-singletons.md) | Паттерн Singleton | ✅ |
| [7.2](07-patterns/02-module-systems.md) | Системы модулей/плагинов | ✅ |
| [7.3](07-patterns/03-rpc-patterns.md) | Коммуникация через RPC | ✅ |
| [7.4](07-patterns/04-config-persistence.md) | Персистентность конфигураций | ✅ |
| [7.5](07-patterns/05-permissions.md) | Системы разрешений | ✅ |
| [7.6](07-patterns/06-events.md) | Событийная архитектура | ✅ |
| [7.7](07-patterns/07-performance.md) | Оптимизация производительности | ✅ |

### Часть 8: Руководства
Пошаговые руководства.

| Глава | Тема | Статус |
|-------|------|--------|
| [8.1](08-tutorials/01-first-mod.md) | Ваш первый мод (Hello World) | ✅ |
| [8.2](08-tutorials/02-custom-item.md) | Создание пользовательского предмета | ✅ |
| [8.3](08-tutorials/03-admin-panel.md) | Создание админ-панели | ✅ |
| [8.4](08-tutorials/04-chat-commands.md) | Добавление команд чата | ✅ |

---

## Поддерживаемые языки

| Язык | Код | Статус |
|------|-----|--------|
| English | `en` | ✅ Основной |
| Português | `pt` | ✅ Переведено |
| Deutsch | `de` | Запланировано |
| Русский | `ru` | ✅ Переведено |
| Čeština | `cs` | Запланировано |
| Polski | `pl` | Запланировано |
| Magyar | `hu` | Запланировано |
| Italiano | `it` | Запланировано |
| Español | `es` | Запланировано |
| Français | `fr` | Запланировано |
| 中文 | `zh` | Запланировано |
| 日本語 | `ja` | Запланировано |
| 简体中文 | `zh-hans` | Запланировано |

---

## Быстрая справка

- [Шпаргалка по Enforce Script](cheatsheet.md)
- [Справочник типов виджетов](03-gui-system/01-widget-types.md)
- [Краткий справочник API](06-engine-api/quick-reference.md)
- [Типичные ловушки](01-enforce-script/12-gotchas.md)

---

## Участие в проекте

Эта документация была составлена на основе изучения:
- 10+ профессиональных модов DayZ (COT, VPP, Expansion, Dabs Framework, DayZ Editor, Colorful UI)
- 15 официальных примеров модов Bohemia Interactive
- 2800+ файлов ванильных скриптов DayZ
- Исходного кода Community Framework

Pull request'ы приветствуются! Ознакомьтесь с [CONTRIBUTING.md](../CONTRIBUTING.md) для получения рекомендаций.

---

## Благодарности

- **Bohemia Interactive** -- Движок DayZ и официальные примеры
- **Jacob_Mango** -- Community Framework и Community Online Tools
- **InclementDab** -- Dabs Framework и DayZ Editor
- **DaOne & GravityWolf** -- VPP Admin Tools
- **DayZ Expansion Team** -- Expansion Scripts
- **MyMod Team** -- Составление и документирование

## Лицензия

Эта документация лицензирована под [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Примеры кода лицензированы под [MIT](https://opensource.org/licenses/MIT).
