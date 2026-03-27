# Chapter 9.12: Zaawansowane tematy serwerowe

[Strona glowna](../README.md) | [<< Poprzedni: Rozwiazywanie problemow](11-troubleshooting.md) | [Strona glowna czesci 9](01-server-setup.md)

---

> **Podsumowanie:** Zaawansowane pliki konfiguracyjne, konfiguracje wielu map, dzielenie ekonomii, terytoria zwierzat, zdarzenia dynamiczne, kontrola pogody, automatyczne restarty i system wiadomosci.

---

## Spis tresci

- [Szczegolowe omowienie cfggameplay.json](#szczegolowe-omowienie-cfggameplayjson)
- [Serwery z wieloma mapami](#serwery-z-wieloma-mapami)
- [Niestandardowe dostrajanie ekonomii](#niestandardowe-dostrajanie-ekonomii)
- [cfgenvironment.xml i terytoria zwierzat](#cfgenvironmentxml-i-terytoria-zwierzat)
- [Niestandardowe zdarzenia dynamiczne](#niestandardowe-zdarzenia-dynamiczne)
- [Automatyzacja restartow serwera](#automatyzacja-restartow-serwera)
- [cfgweather.xml](#cfgweatherxml)
- [System wiadomosci](#system-wiadomosci)

---

## Szczegolowe omowienie cfggameplay.json

Plik **cfggameplay.json** znajduje sie w folderze misji i nadpisuje zakodowane na stalo domyslne wartosci rozgrywki. Najpierw wlacz go w **serverDZ.cfg**:

```cpp
enableCfgGameplayFile = 1;
```

Struktura vanillowa:

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

- `version` -- musi odpowiadac temu, czego oczekuje plik binarny twojego serwera. Nie zmieniaj tego.
- `lightingConfig` -- `0` (domyslnie) lub `1` (jasniejsze noce).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 wartosci, jedna na miesiac (sty-gru).
- `disablePersonalLight` -- usuwa delikatne swiatlo otoczenia w poblizu nowych graczy w nocy.
- `staminaMax` i modyfikatory sprintu kontroluja jak daleko gracze moga biec zanim sie zmecza.
- `use3DMap` -- przelacza mape w grze na wariant 3D renderowany z terenu.

---

## Serwery z wieloma mapami

DayZ obsluguje wiele map przez rozne foldery misji wewnatrz `mpmissions/`:

| Mapa | Folder misji |
|------|-------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Kazda mapa ma swoje wlasne pliki CE (`types.xml`, `events.xml` itp.). Zmien mape przez `template` w **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Lub parametrem uruchomienia: `-mission=mpmissions/dayzOffline.enoch`

Aby uruchamiac wiele map jednoczesnie, uzyj oddzielnych instancji serwera z wlasna konfiguracja, katalogiem profilu i zakresem portow.

---

## Niestandardowe dostrajanie ekonomii

### Dzielenie types.xml

Podziel przedmioty na wiele plikow i zarejestruj je w **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

Serwer laduje i laczy wszystkie pliki z `type="types"`.

### Niestandardowe kategorie i tagi

**cfglimitsdefinition.xml** definiuje kategorie/tagi dla `types.xml`, ale jest nadpisywany przy aktualizacjach. Zamiast tego uzyj **cfglimitsdefinitionuser.xml**:

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

## cfgenvironment.xml i terytoria zwierzat

Plik **cfgenvironment.xml** w folderze misji odnosi sie do plikow terytoriow w podkatalogu `env/`:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

Folder `env/` zawiera nastepujace pliki terytoriow zwierzat:

| Plik | Zwierzeta |
|------|-----------|
| **bear_territories.xml** | Niedzwiedzie brunatne |
| **wolf_territories.xml** | Stada wilkow |
| **fox_territories.xml** | Lisy |
| **hare_territories.xml** | Kroliki/zajace |
| **hen_territories.xml** | Kury |
| **pig_territories.xml** | Swinie |
| **red_deer_territories.xml** | Jelenie |
| **roe_deer_territories.xml** | Sarny |
| **sheep_goat_territories.xml** | Owce/kozy |
| **wild_boar_territories.xml** | Dziki |
| **cattle_territories.xml** | Krowy |

Wpis terytorium definiuje koliste strefy z pozycja i liczba zwierzat:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- wspolrzedne srodka; `r` -- promien w metrach
- `dmin`, `dmax` -- min/maks liczba zwierzat w strefie
- `smin`, `smax` -- zarezerwowane (ustaw na `-1`)

---

## Niestandardowe zdarzenia dynamiczne

Zdarzenia dynamiczne (rozbicia helikopterow, konwoje) sa zdefiniowane w **events.xml**. Aby stworzyc niestandardowe zdarzenie:

**1. Zdefiniuj zdarzenie** w **events.xml**:

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

**2. Dodaj pozycje spawnu** w **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Dodaj zarazonych straznikow** (opcjonalnie) -- dodaj elementy `<secondary type="ZmbM_PatrolNormal_Autumn" />` w definicji zdarzenia.

**4. Spawny grupowe** (opcjonalnie) -- zdefiniuj klastry w **cfgeventgroups.xml** i odwolaj sie do nazwy grupy w swoim zdarzeniu.

---

## Automatyzacja restartow serwera

DayZ nie ma wbudowanego planisty restartow. Uzyj automatyzacji na poziomie systemu operacyjnego.

### Windows

Utworz **restart_server.bat** i uruchamiaj go przez Zaplanowane zadanie Windows co 4-6 godzin:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Utworz skrypt powloki i dodaj go do crona (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Zawsze rob kopie zapasowa `storage_1/` przed kazdym restartem. Uszkodzona trwalosc podczas zamykania moze wyczyscic bazy i pojazdy graczy.

---

## cfgweather.xml

Plik **cfgweather.xml** w folderze misji kontroluje wzorce pogody. Kazda mapa jest dostarczana z wlasnymi domyslnymi wartosciami:

Kazde zjawisko ma `min`, `max`, `duration_min` i `duration_max` (sekundy):

| Zjawisko | Domyslne Min | Domyslne Max | Uwagi |
|----------|-------------|-------------|-------|
| `overcast` | 0.0 | 1.0 | Okresla gestosc chmur i prawdopodobienstwo deszczu |
| `rain` | 0.0 | 1.0 | Wlacza sie dopiero powyzej progu zachmurzenia. Ustaw max na `0.0` dla braku deszczu |
| `fog` | 0.0 | 0.3 | Wartosci powyzej `0.5` daja prawie zerowa widocznosc |
| `wind_magnitude` | 0.0 | 18.0 | Wplywa na balistyke i ruch gracza |

---

## System wiadomosci

Plik **db/messages.xml** w folderze misji kontroluje zaplanowane wiadomosci serwera i ostrzezenia o wylaczeniu:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- minuty przed wyzwoleniem wiadomosci (dla wiadomosci o wylaczeniu, minuty przed zatrzymaniem serwera)
- `shutdown` -- `1` dla wiadomosci sekwencji wylaczenia, `0` dla zwyklych ogloszen

System wiadomosci nie restartuje serwera. Wyswietla jedynie ostrzezenia, gdy harmonogram restartow jest skonfigurowany zewnetrznie.

---

[Strona glowna](../README.md) | [<< Poprzedni: Rozwiazywanie problemow](11-troubleshooting.md) | [Strona glowna czesci 9](01-server-setup.md)
