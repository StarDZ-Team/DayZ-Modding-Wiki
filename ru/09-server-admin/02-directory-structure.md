# Глава 9.2: Структура каталогов и папка миссии

[Главная](../README.md) | [<< Назад: Установка сервера](01-server-setup.md) | **Структура каталогов** | [Далее: Справочник serverDZ.cfg >>](03-server-cfg.md)

---

> **Краткое содержание:** Полное описание каждого файла и папки в каталоге DayZ-сервера и папке миссии. Понимание назначения каждого файла -- и какие из них безопасно редактировать -- необходимо перед настройкой лут-экономики или добавлением модов.

---

## Содержание

- [Корневой каталог сервера](#корневой-каталог-сервера)
- [Папка addons/](#папка-addons)
- [Папка keys/](#папка-keys)
- [Папка profiles/](#папка-profiles)
- [Папка mpmissions/](#папка-mpmissions)
- [Структура папки миссии](#структура-папки-миссии)
- [Папка db/ -- ядро экономики](#папка-db----ядро-экономики)
- [Папка env/ -- территории животных](#папка-env----территории-животных)
- [Папка storage_1/ -- персистентность](#папка-storage_1----персистентность)
- [Файлы верхнего уровня миссии](#файлы-верхнего-уровня-миссии)
- [Какие файлы редактировать, а какие не трогать](#какие-файлы-редактировать-а-какие-не-трогать)

---

## Корневой каталог сервера

```
DayZServer/
  DayZServer_x64.exe          # Исполняемый файл сервера
  serverDZ.cfg                 # Основная конфигурация сервера (имя, пароль, моды, время)
  dayzsetting.xml              # Настройки рендеринга (не актуально для выделенных серверов)
  ban.txt                      # Заблокированные Steam64 ID, по одному на строку
  whitelist.txt                # Steam64 ID в белом списке, по одному на строку
  steam_appid.txt              # Содержит "221100" -- не редактировать
  dayz.gproj                   # Файл проекта Workbench -- не редактировать
  addons/                      # Ванильные игровые PBO
  battleye/                    # Файлы античита
  config/                      # Конфигурация Steam (config.vdf)
  dta/                         # Основные PBO движка (скрипты, GUI, графика)
  keys/                        # Ключи проверки подписей (файлы .bikey)
  logs/                        # Логи на уровне движка
  mpmissions/                  # Все папки миссий
  profiles/                    # Рантайм-вывод (скрипт-логи, БД игроков, дампы сбоев)
  server_manager/              # Утилиты управления сервером
```

---

## Папка addons/

Содержит всё ванильное игровое содержимое, упакованное в PBO-файлы. Каждый PBO имеет соответствующий файл подписи `.bisign`:

```
addons/
  ai.pbo                       # Скрипты поведения ИИ
  ai.pbo.dayz.bisign           # Подпись для ai.pbo
  animals.pbo                  # Определения животных
  characters_backpacks.pbo     # Модели/конфиги рюкзаков
  characters_belts.pbo         # Модели ременных предметов
  weapons_firearms.pbo         # Модели/конфиги оружия
  ... (100+ PBO-файлов)
```

**Никогда не редактируйте эти файлы.** Они перезаписываются при каждом обновлении сервера через SteamCMD. Моды переопределяют ванильное поведение через систему `modded` классов, а не через изменение PBO.

---

## Папка keys/

Содержит файлы публичных ключей `.bikey`, используемые для проверки подписей модов:

```
keys/
  dayz.bikey                   # Ванильный ключ подписи (всегда присутствует)
```

Когда вы добавляете мод, скопируйте его файл `.bikey` в эту папку. Сервер использует `verifySignatures = 2` в `serverDZ.cfg` для отклонения любого PBO, который не имеет соответствующего `.bikey` в этой папке.

Если игрок загружает мод, ключ которого отсутствует в вашей папке `keys/`, он получит кик **"Signature check failed"**.

---

## Папка profiles/

Создаётся при первом запуске сервера. Содержит рантайм-вывод:

```
profiles/
  BattlEye/                              # Логи и баны BE
  DataCache/                             # Кэшированные данные
  Users/                                 # Файлы настроек каждого игрока
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Лог администратора
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Отчёт движка (информация о сбоях, предупреждения)
  script_2026-03-08_11-34-35.log           # Скрипт-лог (ваш основной инструмент отладки)
```

**Скрипт-лог** -- самый важный файл здесь. Каждый вызов `Print()`, каждая скриптовая ошибка и каждое сообщение загрузки модов попадает сюда. Когда что-то ломается -- это первое место, куда нужно смотреть.

Файлы логов накапливаются со временем. Старые логи не удаляются автоматически.

---

## Папка mpmissions/

Содержит по одной подпапке на каждую карту:

```
mpmissions/
  dayzOffline.chernarusplus/    # Чернарусь (бесплатная)
  dayzOffline.enoch/            # Ливония (DLC)
  dayzOffline.sakhal/           # Сахаль (DLC)
```

Формат имени папки: `<missionName>.<terrainName>`. Значение `template` в `serverDZ.cfg` должно точно совпадать с одним из этих имён папок.

---

## Структура папки миссии

Папка миссии Чернаруси (`mpmissions/dayzOffline.chernarusplus/`) содержит:

```
dayzOffline.chernarusplus/
  init.c                         # Входной скрипт миссии
  db/                            # Основные файлы экономики
  env/                           # Определения территорий животных
  storage_1/                     # Данные персистентности (игроки, состояние мира)
  cfgeconomycore.xml             # Корневые классы экономики и настройки логирования
  cfgenvironment.xml             # Ссылки на файлы территорий животных
  cfgeventgroups.xml             # Определения групп событий
  cfgeventspawns.xml             # Точные позиции спавна для событий (техника и т.д.)
  cfgeffectarea.json             # Определения зон заражения
  cfggameplay.json               # Настройка геймплея (выносливость, урон, строительство)
  cfgignorelist.xml              # Предметы, полностью исключённые из экономики
  cfglimitsdefinition.xml        # Определения допустимых тегов категорий/использования/ценности
  cfglimitsdefinitionuser.xml    # Пользовательские определения тегов
  cfgplayerspawnpoints.xml       # Точки появления новых игроков
  cfgrandompresets.xml           # Переиспользуемые определения пулов лута
  cfgspawnabletypes.xml          # Предустановленные вложения и содержимое при спавне
  cfgundergroundtriggers.json    # Триггеры подземных областей
  cfgweather.xml                 # Конфигурация погоды
  areaflags.map                  # Данные флагов областей (двоичные)
  mapclusterproto.xml            # Прототипы кластеров карты
  mapgroupcluster.xml            # Определения кластеров групп зданий
  mapgroupcluster01.xml          # Данные кластеров (часть 1)
  mapgroupcluster02.xml          # Данные кластеров (часть 2)
  mapgroupcluster03.xml          # Данные кластеров (часть 3)
  mapgroupcluster04.xml          # Данные кластеров (часть 4)
  mapgroupdirt.xml               # Позиции наземного лута
  mapgrouppos.xml                # Позиции групп карты
  mapgroupproto.xml              # Определения прототипов для групп карты
```

---

## Папка db/ -- ядро экономики

Это сердце Центральной Экономики. Пять файлов определяют, что появляется, где и в каком количестве:

```
db/
  types.xml        # КЛЮЧЕВОЙ файл: определяет правила спавна каждого предмета
  globals.xml      # Глобальные параметры экономики (таймеры, лимиты, количества)
  events.xml       # Динамические события (животные, техника, вертолёты)
  economy.xml      # Переключатели подсистем экономики (лут, животные, техника)
  messages.xml     # Запланированные серверные сообщения игрокам
```

### types.xml

Определяет правила спавна для **каждого предмета** в игре. При объёме около 23 000 строк это безусловно самый большой файл экономики. Каждая запись указывает, сколько копий предмета должно существовать на карте, где он может появиться и как долго сохраняется. Подробности см. в [Главе 9.4](04-loot-economy.md).

### globals.xml

Глобальные параметры, влияющие на всю экономику: количество зомби, количество животных, таймеры очистки, диапазоны повреждений лута, время респавна. Всего 33 параметра. Полный справочник см. в [Главе 9.4](04-loot-economy.md).

### events.xml

Определяет события динамического спавна для животных и техники. Каждое событие задаёт номинальное количество, ограничения спавна и дочерние варианты. Например, событие `VehicleCivilianSedan` создаёт 8 седанов по всей карте в 3 цветовых вариантах.

### economy.xml

Главные переключатели для подсистем экономики:

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

| Флаг | Значение |
|------|---------|
| `init` | Создать предметы при первом запуске сервера |
| `load` | Загрузить сохранённое состояние из персистентности |
| `respawn` | Разрешить респавн предметов после очистки |
| `save` | Сохранять состояние в файлы персистентности |

### messages.xml

Запланированные сообщения, транслируемые всем игрокам. Поддерживает таймеры обратного отсчёта, интервалы повтора, сообщения при подключении и предупреждения о перезапуске:

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

Используйте `#name` для имени сервера и `#tmin` для оставшегося времени в минутах.

---

## Папка env/ -- территории животных

Содержит XML-файлы, определяющие, где может появляться каждый вид животных:

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

Эти файлы содержат сотни координатных точек, определяющих зоны территорий по всей карте. На них ссылается `cfgenvironment.xml`. Редактировать их нужно редко -- только если вы хотите изменить места появления животных или зомби географически.

---

## Папка storage_1/ -- персистентность

Хранит постоянное состояние сервера между перезапусками:

```
storage_1/
  players.db         # База данных SQLite всех персонажей игроков
  spawnpoints.bin    # Двоичные данные точек спавна
  backup/            # Автоматические резервные копии данных персистентности
  data/              # Состояние мира (размещённые предметы, базы, техника)
```

**Никогда не редактируйте `players.db` при работающем сервере.** Это база данных SQLite, заблокированная процессом сервера. Если вам нужно сбросить персонажей, сначала остановите сервер и удалите или переименуйте файл.

Для выполнения **полного вайпа персистентности** остановите сервер и удалите всю папку `storage_1/`. Сервер создаст её заново при следующем запуске с чистым миром.

Для выполнения **частичного вайпа** (сохранить персонажей, сбросить лут):
1. Остановите сервер
2. Удалите файлы в `storage_1/data/`, но сохраните `players.db`
3. Перезапустите

---

## Файлы верхнего уровня миссии

### cfgeconomycore.xml

Регистрирует корневые классы для экономики и настраивает логирование CE:

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

Установите `log_ce_lootspawn` в `"true"` при отладке проблем со спавном предметов. Это создаёт подробный вывод в RPT-логе, показывающий, какие предметы CE пытается создать и почему они появляются или нет.

### cfglimitsdefinition.xml

Определяет допустимые значения для элементов `<category>`, `<usage>`, `<value>` и `<tag>`, используемых в `types.xml`:

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

Если вы используете тег `<usage>` или `<value>` в `types.xml`, который не определён здесь, предмет молча не будет появляться.

### cfgignorelist.xml

Предметы, перечисленные здесь, полностью исключены из экономики, даже если у них есть записи в `types.xml`:

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

Это используется для предметов, которые существуют в коде игры, но не предназначены для естественного появления (незавершённые предметы, устаревший контент, сезонные предметы вне сезона).

### cfggameplay.json

JSON-файл, переопределяющий параметры геймплея. Управляет выносливостью, передвижением, уроном по базам, погодой, температурой, препятствиями для оружия, утоплением и прочим. Этот файл опционален -- если он отсутствует, сервер использует значения по умолчанию.

### cfgplayerspawnpoints.xml

Определяет, где на карте появляются только что созданные игроки, с ограничениями по расстоянию от заражённых, других игроков и зданий.

### cfgeventspawns.xml

Содержит точные мировые координаты, где могут появляться события (техника, крушения вертолётов и т.д.). У каждого имени события из `events.xml` есть список допустимых позиций:

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

Атрибут `a` -- это угол поворота в градусах.

---

## Какие файлы редактировать, а какие не трогать

| Файл / Папка | Безопасно ли редактировать? | Примечания |
|---------------|:---:|-------|
| `serverDZ.cfg` | Да | Основная конфигурация сервера |
| `db/types.xml` | Да | Правила спавна предметов -- ваша самая частая правка |
| `db/globals.xml` | Да | Параметры настройки экономики |
| `db/events.xml` | Да | События спавна техники/животных |
| `db/economy.xml` | Да | Переключатели подсистем экономики |
| `db/messages.xml` | Да | Широковещательные сообщения сервера |
| `cfggameplay.json` | Да | Настройка геймплея |
| `cfgspawnabletypes.xml` | Да | Пресеты вложений/содержимого |
| `cfgrandompresets.xml` | Да | Определения пулов лута |
| `cfglimitsdefinition.xml` | Да | Добавление пользовательских тегов usage/value |
| `cfgplayerspawnpoints.xml` | Да | Точки появления игроков |
| `cfgeventspawns.xml` | Да | Координаты спавна событий |
| `cfgignorelist.xml` | Да | Исключение предметов из экономики |
| `cfgweather.xml` | Да | Погодные паттерны |
| `cfgeffectarea.json` | Да | Зоны заражения |
| `init.c` | Да | Входной скрипт миссии |
| `addons/` | **Нет** | Перезаписывается при обновлении |
| `dta/` | **Нет** | Основные данные движка |
| `keys/` | Только добавление | Копируйте файлы `.bikey` модов сюда |
| `storage_1/` | Только удаление | Персистентность -- не редактировать вручную |
| `battleye/` | **Нет** | Античит -- не трогать |
| `mapgroup*.xml` | Осторожно | Позиции лута в зданиях -- только продвинутое редактирование |

---

**Назад:** [Установка сервера](01-server-setup.md) | [Главная](../README.md) | **Далее:** [Справочник serverDZ.cfg >>](03-server-cfg.md)
