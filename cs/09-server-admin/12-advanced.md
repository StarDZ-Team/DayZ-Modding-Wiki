# Chapter 9.12: Pokrocila temata serveru

[Domu](../README.md) | [<< Predchozi: Reseni problemu](11-troubleshooting.md) | [Cast 9 - domu](01-server-setup.md)

---

> **Shrnuti:** Pokrocile konfiguracni soubory, nastaveni vice map, rozdeleni ekonomiky, uzemi zvirat, dynamicke udalosti, ovladani pocasi, automaticke restarty a system zprav.

---

## Obsah

- [cfggameplay.json podrobne](#cfggameplayjson-podrobne)
- [Servery s vice mapami](#servery-s-vice-mapami)
- [Vlastni ladeni ekonomiky](#vlastni-ladeni-ekonomiky)
- [cfgenvironment.xml a uzemi zvirat](#cfgenvironmentxml-a-uzemi-zvirat)
- [Vlastni dynamicke udalosti](#vlastni-dynamicke-udalosti)
- [Automatizace restartu serveru](#automatizace-restartu-serveru)
- [cfgweather.xml](#cfgweatherxml)
- [System zprav](#system-zprav)

---

## cfggameplay.json podrobne

Soubor **cfggameplay.json** se nachazi ve slozce vasi mise a prepisuje zabudovane vychozi hodnoty gameplayu. Nejprve ho povolte v **serverDZ.cfg**:

```cpp
enableCfgGameplayFile = 1;
```

Vanilkova struktura:

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

- `version` -- musi odpovidat ocekavani vascho binarniho serveru. Nemente ji.
- `lightingConfig` -- `0` (vychozi) nebo `1` (svetlejsi noci).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 hodnot, jedna na mesic (leden-prosinec).
- `disablePersonalLight` -- odstrani slabe ambientni svetlo blizko novych hracu v noci.
- `staminaMax` a modifikatory sprintu ridi, jak daleko hraci mohou bezet pred vycerpanim.
- `use3DMap` -- prepne herní mapu na 3D variantu vykreslovanou terenem.

---

## Servery s vice mapami

DayZ podporuje vice map pres ruzne slozky misi uvnitr `mpmissions/`:

| Mapa | Slozka mise |
|-----|---------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonie | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Kazda mapa ma sve vlastni CE soubory (`types.xml`, `events.xml` atd.). Prepinani map pres `template` v **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Nebo spoustecim parametrem: `-mission=mpmissions/dayzOffline.enoch`

Pro soucasny provoz vice map pouzijte oddelene instance serveru s vlastni konfiguraci, adresarem profilu a rozsahem portu.

---

## Vlastni ladeni ekonomiky

### Rozdeleni types.xml

Rozdelte predmety do vice souboru a zaregistrujte je v **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

Server nacte a slouci vsechny soubory s `type="types"`.

### Vlastni kategorie a tagy

**cfglimitsdefinition.xml** definuje kategorie/tagy pro `types.xml`, ale je prepsany pri aktualizacich. Misto toho pouzijte **cfglimitsdefinitionuser.xml**:

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

## cfgenvironment.xml a uzemi zvirat

Soubor **cfgenvironment.xml** ve slozce vasi mise odkazuje na soubory uzemi v podadresari `env/`:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

Slozka `env/` obsahuje tyto soubory uzemi zvirat:

| Soubor | Zvírata |
|------|---------|
| **bear_territories.xml** | Hnedi medvedi |
| **wolf_territories.xml** | Vlci smecky |
| **fox_territories.xml** | Lisky |
| **hare_territories.xml** | Kralici/zajici |
| **hen_territories.xml** | Slepice |
| **pig_territories.xml** | Prasata |
| **red_deer_territories.xml** | Jeleni |
| **roe_deer_territories.xml** | Srnci |
| **sheep_goat_territories.xml** | Ovce/kozy |
| **wild_boar_territories.xml** | Divoci kanci |
| **cattle_territories.xml** | Kravy |

Zaznam uzemi definuje kruhove zony s pozici a poctem zvirat:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- stredove souradnice; `r` -- polomer v metrech
- `dmin`, `dmax` -- minimalni/maximalni pocet zvirat v zone
- `smin`, `smax` -- rezervovano (nastavte na `-1`)

---

## Vlastni dynamicke udalosti

Dynamicke udalosti (helikopterove zriceniny, konvoje) jsou definovany v **events.xml**. Pro vytvoreni vlastni udalosti:

**1. Definujte udalost** v **events.xml**:

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

**2. Pridejte pozice spawnu** v **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Pridejte infikovane straze** (volitelne) -- pridejte elementy `<secondary type="ZmbM_PatrolNormal_Autumn" />` do definice vasi udalosti.

**4. Skupinove spawny** (volitelne) -- definujte klustry v **cfgeventgroups.xml** a odkazujte na nazev skupiny ve vasi udalosti.

---

## Automatizace restartu serveru

DayZ nema vestaveny planovac restartu. Pouzijte automatizaci na urovni OS.

### Windows

Vytvorte **restart_server.bat** a spoustejte pres Windows Scheduled Task kazdych 4-6 hodin:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Vytvorte shell skript a pridejte do cronu (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Vzdy zalohujte `storage_1/` pred kazdym restartem. Poskozena persistence behem vypinani muze wipnout baze a vozidla hracu.

---

## cfgweather.xml

Soubor **cfgweather.xml** ve slozce vasi mise ridi vzory pocasi. Kazda mapa je dodavana se svymi vychozimi hodnotami:

Kazdy jev ma `min`, `max`, `duration_min` a `duration_max` (sekundy):

| Jev | Vychozi min | Vychozi max | Poznamky |
|------------|-------------|-------------|-------|
| `overcast` | 0.0 | 1.0 | Ridi hustotu mraku a pravdepodobnost deste |
| `rain` | 0.0 | 1.0 | Spusti se pouze nad prahem oblacnosti. Nastavte max na `0.0` pro zadny dest |
| `fog` | 0.0 | 0.3 | Hodnoty nad `0.5` produkuji temer nulovou viditelnost |
| `wind_magnitude` | 0.0 | 18.0 | Ovlivnuje balistiku a pohyb hrace |

---

## System zprav

Soubor **db/messages.xml** ve slozce vasi mise ridi planovane zpravy serveru a varovani pred vypnutim:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- minuty pred spustenim zpravy (pro zpravy vypnuti, minuty pred zastavenim serveru)
- `shutdown` -- `1` pro zpravy sekvence vypnuti, `0` pro bezne vysilani

System zprav nerestartuje server. Pouze zobrazuje varovani, kdyz je plan restartu nakonfigurovany externe.

---

[Domu](../README.md) | [<< Predchozi: Reseni problemu](11-troubleshooting.md) | [Cast 9 - domu](01-server-setup.md)
