# Глава 9.12: Продвинутые темы серверного администрирования

[Главная](../README.md) | [<< Назад: Устранение неполадок](11-troubleshooting.md) | [Часть 9: Главная](01-server-setup.md)

---

> **Краткое содержание:** Углублённые конфигурационные файлы, мультикартовые установки, разделение экономики, территории животных, динамические события, управление погодой, автоматизация перезапусков и система сообщений.

---

## Содержание

- [Подробный разбор cfggameplay.json](#подробный-разбор-cfggameplayjson)
- [Мультикартовые серверы](#мультикартовые-серверы)
- [Пользовательская настройка экономики](#пользовательская-настройка-экономики)
- [cfgenvironment.xml и территории животных](#cfgenvironmentxml-и-территории-животных)
- [Пользовательские динамические события](#пользовательские-динамические-события)
- [Автоматизация перезапуска сервера](#автоматизация-перезапуска-сервера)
- [cfgweather.xml](#cfgweatherxml)
- [Система сообщений](#система-сообщений)

---

## Подробный разбор cfggameplay.json

Файл **cfggameplay.json** находится в вашей папке миссии и переопределяет жёстко заданные значения геймплея. Сначала включите его в **serverDZ.cfg**:

```cpp
enableCfgGameplayFile = 1;
```

Ванильная структура:

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

- `version` -- должна совпадать с ожиданием вашего бинарника сервера. Не меняйте.
- `lightingConfig` -- `0` (по умолчанию) или `1` (более светлые ночи).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 значений, по одному на каждый месяц (январь-декабрь).
- `disablePersonalLight` -- убирает слабый окружающий свет вблизи новых игроков ночью.
- `staminaMax` и модификаторы спринта управляют тем, как далеко игроки могут бежать до истощения.
- `use3DMap` -- переключает внутриигровую карту на 3D-вариант с рендерингом рельефа.

---

## Мультикартовые серверы

DayZ поддерживает несколько карт через различные папки миссий внутри `mpmissions/`:

| Карта | Папка миссии |
|-----|---------------|
| Чернарусь | `mpmissions/dayzOffline.chernarusplus/` |
| Ливония | `mpmissions/dayzOffline.enoch/` |
| Сахаль | `mpmissions/dayzOffline.sakhal/` |

У каждой карты собственные файлы CE (`types.xml`, `events.xml` и т.д.). Переключайте карты через `template` в **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Или с параметром запуска: `-mission=mpmissions/dayzOffline.enoch`

Для одновременного запуска нескольких карт используйте отдельные экземпляры сервера с собственными конфигурациями, каталогами профилей и диапазонами портов.

---

## Пользовательская настройка экономики

### Разделение types.xml

Разделите предметы на несколько файлов и зарегистрируйте их в **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

Сервер загружает и объединяет все файлы с `type="types"`.

### Пользовательские категории и теги

**cfglimitsdefinition.xml** определяет категории/теги для `types.xml`, но перезаписывается при обновлениях. Используйте **cfglimitsdefinitionuser.xml** вместо этого:

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

## cfgenvironment.xml и территории животных

Файл **cfgenvironment.xml** в вашей папке миссии ссылается на файлы территорий в подкаталоге `env/`:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

Папка `env/` содержит следующие файлы территорий животных:

| Файл | Животные |
|------|---------|
| **bear_territories.xml** | Бурые медведи |
| **wolf_territories.xml** | Стаи волков |
| **fox_territories.xml** | Лисы |
| **hare_territories.xml** | Кролики/зайцы |
| **hen_territories.xml** | Куры |
| **pig_territories.xml** | Свиньи |
| **red_deer_territories.xml** | Благородные олени |
| **roe_deer_territories.xml** | Косули |
| **sheep_goat_territories.xml** | Овцы/козы |
| **wild_boar_territories.xml** | Кабаны |
| **cattle_territories.xml** | Коровы |

Запись территории определяет круговые зоны с позицией и количеством животных:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- координаты центра; `r` -- радиус в метрах
- `dmin`, `dmax` -- минимальное/максимальное количество животных в зоне
- `smin`, `smax` -- зарезервировано (установите `-1`)

---

## Пользовательские динамические события

Динамические события (крушения вертолётов, конвои) определяются в **events.xml**. Для создания пользовательского события:

**1. Определите событие** в **events.xml**:

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

**2. Добавьте позиции спавна** в **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Добавьте заражённых охранников** (опционально) -- добавьте элементы `<secondary type="ZmbM_PatrolNormal_Autumn" />` в определение события.

**4. Групповой спавн** (опционально) -- определите кластеры в **cfgeventgroups.xml** и сошлитесь на имя группы в вашем событии.

---

## Автоматизация перезапуска сервера

В DayZ нет встроенного планировщика перезапусков. Используйте автоматизацию на уровне ОС.

### Windows

Создайте **restart_server.bat** и запускайте его через Планировщик заданий Windows каждые 4-6 часов:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Создайте shell-скрипт и добавьте его в cron (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Всегда делайте резервную копию `storage_1/` перед каждым перезапуском. Повреждение персистентности при завершении работы может стереть базы и транспорт игроков.

---

## cfgweather.xml

Файл **cfgweather.xml** в вашей папке миссии управляет погодными паттернами. Каждая карта поставляется со своими значениями по умолчанию:

Каждое явление имеет `min`, `max`, `duration_min` и `duration_max` (секунды):

| Явление | Min по умолчанию | Max по умолчанию | Примечания |
|------------|-------------|-------------|-------|
| `overcast` | 0.0 | 1.0 | Определяет плотность облаков и вероятность дождя |
| `rain` | 0.0 | 1.0 | Включается только при превышении порога облачности. Установите max в `0.0` для отключения дождя |
| `fog` | 0.0 | 0.3 | Значения выше `0.5` дают почти нулевую видимость |
| `wind_magnitude` | 0.0 | 18.0 | Влияет на баллистику и передвижение игрока |

---

## Система сообщений

Файл **db/messages.xml** в вашей папке миссии управляет запланированными серверными сообщениями и предупреждениями о перезапуске:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- минуты до срабатывания сообщения (для сообщений о перезапуске -- минуты до остановки сервера)
- `shutdown` -- `1` для сообщений последовательности перезапуска, `0` для обычных трансляций

Система сообщений не перезапускает сервер. Она только отображает предупреждения, когда расписание перезапуска настроено внешне.

---

[Главная](../README.md) | [<< Назад: Устранение неполадок](11-troubleshooting.md) | [Часть 9: Главная](01-server-setup.md)
