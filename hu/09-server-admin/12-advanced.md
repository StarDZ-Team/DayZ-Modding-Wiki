# Chapter 9.12: Haladó szerver témák

[Kezdőlap](../README.md) | [<< Előző: Hibaelhárítás](11-troubleshooting.md) | [9. rész kezdőlap](01-server-setup.md)

---

> **Összefoglaló:** Mélyebb konfigurációs fájlok, több-térképes beállítások, gazdaság felosztás, állat területek, dinamikus események, időjárás vezérlés, automatikus újraindítások és az üzenet rendszer.

---

## Tartalomjegyzék

- [cfggameplay.json részletes áttekintés](#cfggameplayjson-részletes-áttekintés)
- [Több-térképes szerverek](#több-térképes-szerverek)
- [Egyedi gazdaság hangolás](#egyedi-gazdaság-hangolás)
- [cfgenvironment.xml és állat területek](#cfgenvironmentxml-és-állat-területek)
- [Egyedi dinamikus események](#egyedi-dinamikus-események)
- [Szerver újraindítás automatizálás](#szerver-újraindítás-automatizálás)
- [cfgweather.xml](#cfgweatherxml)
- [Üzenet rendszer](#üzenet-rendszer)

---

## cfggameplay.json részletes áttekintés

A **cfggameplay.json** fájl a küldetés mappádban található és felülírja a beégetett játékmenet alapértékeket. Először engedélyezd a **serverDZ.cfg**-ben:

```cpp
enableCfgGameplayFile = 1;
```

Vanilla struktúra:

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

- `version` -- meg kell egyeznie azzal, amit a szerver bináris vár. Ne változtasd meg.
- `lightingConfig` -- `0` (alapértelmezett) vagy `1` (világosabb éjszakák).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 érték, hónaponként egy (január-december).
- `disablePersonalLight` -- eltávolítja a halvány környezeti fényt az új játékosok közelében éjszaka.
- `staminaMax` és sprint módosítók szabályozzák, meddig futhat egy játékos a kimerülés előtt.
- `use3DMap` -- átváltja a játékon belüli térképet a terep-renderelt 3D változatra.

---

## Több-térképes szerverek

A DayZ több térképet támogat az `mpmissions/` mappán belüli különböző küldetés mappákon keresztül:

| Térkép | Küldetés mappa |
|--------|---------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Minden térképnek saját CE fájljai vannak (`types.xml`, `events.xml`, stb.). Térkép váltás a **serverDZ.cfg** `template` értékén keresztül:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Vagy indítási paraméterrel: `-mission=mpmissions/dayzOffline.enoch`

Több térkép egyidejű futtatásához használj különálló szerver példányokat saját konfigurációval, profil könyvtárral és porttartománnyal.

---

## Egyedi gazdaság hangolás

### types.xml felosztás

Oszd el a tárgyakat több fájlba és regisztráld őket a **cfgeconomycore.xml**-ben:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

A szerver betölti és összefésüli az összes `type="types"` jelölésű fájlt.

### Egyedi kategóriák és tagek

A **cfglimitsdefinition.xml** definiálja a `types.xml` kategóriáit/tagjeit, de frissítéskor felülíródik. Használd helyette a **cfglimitsdefinitionuser.xml** fájlt:

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

## cfgenvironment.xml és állat területek

A **cfgenvironment.xml** fájl a küldetés mappádban az `env/` alkönyvtárban lévő terület fájlokra hivatkozik:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

Az `env/` mappa tartalmazza ezeket az állat terület fájlokat:

| Fájl | Állatok |
|------|---------|
| **bear_territories.xml** | Barna medvék |
| **wolf_territories.xml** | Farkascsoportok |
| **fox_territories.xml** | Rókák |
| **hare_territories.xml** | Nyulak |
| **hen_territories.xml** | Tyúkok |
| **pig_territories.xml** | Disznók |
| **red_deer_territories.xml** | Gímszarvasok |
| **roe_deer_territories.xml** | Őzek |
| **sheep_goat_territories.xml** | Juhok/kecskék |
| **wild_boar_territories.xml** | Vaddisznók |
| **cattle_territories.xml** | Tehenek |

Egy terület bejegyzés kör alakú zónákat definiál pozícióval és állat számmal:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- középpont koordináták; `r` -- sugár méterben
- `dmin`, `dmax` -- minimális/maximális állat szám a zónában
- `smin`, `smax` -- fenntartott (állítsd `-1`-re)

---

## Egyedi dinamikus események

A dinamikus események (helikopter roncsok, konvojok) az **events.xml**-ben vannak definiálva. Egyedi esemény létrehozásához:

**1. Definiáld az eseményt** az **events.xml**-ben:

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

**2. Adj hozzá spawn pozíciókat** a **cfgeventspawns.xml**-ben:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Adj hozzá fertőzött őröket** (opcionális) -- adj hozzá `<secondary type="ZmbM_PatrolNormal_Autumn" />` elemeket az esemény definíciódban.

**4. Csoportos spawnok** (opcionális) -- definiálj klasztereket a **cfgeventgroups.xml**-ben és hivatkozz a csoport nevére az eseményedben.

---

## Szerver újraindítás automatizálás

A DayZ-nek nincs beépített újraindítás ütemezője. Használj OS szintű automatizálást.

### Windows

Hozz létre egy **restart_server.bat** fájlt és futtasd a Windows Ütemezett Feladatok segítségével 4-6 óránként:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Hozz létre egy shell szkriptet és add hozzá a cron-hoz (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Mindig mentsd le a `storage_1/` mappát minden újraindítás előtt. A leállítás közbeni sérült perzisztencia eltörölheti a játékos bázisokat és járműveket.

---

## cfgweather.xml

A **cfgweather.xml** fájl a küldetés mappádban szabályozza az időjárási mintákat. Minden térképhez saját alapértékek tartoznak:

Minden jelenségnek van `min`, `max`, `duration_min` és `duration_max` (másodperc) értéke:

| Jelenség | Alapértelmezett Min | Alapértelmezett Max | Megjegyzések |
|----------|---------------------|---------------------|--------------|
| `overcast` | 0.0 | 1.0 | Felhősűrűséget és eső valószínűséget vezérli |
| `rain` | 0.0 | 1.0 | Csak egy borultsági küszöb felett aktiválódik. Állítsd a max-ot `0.0`-ra eső nélküli időjáráshoz |
| `fog` | 0.0 | 0.3 | `0.5` feletti értékek közel nulla látótávolságot eredményeznek |
| `wind_magnitude` | 0.0 | 18.0 | Hatással van a ballisztikára és a játékos mozgásra |

---

## Üzenet rendszer

A **db/messages.xml** fájl a küldetés mappádban szabályozza az ütemezett szerver üzeneteket és leállítási figyelmeztetéseket:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- percek, mielőtt az üzenet aktiválódik (leállítási üzeneteknél percek a szerver leállása előtt)
- `shutdown` -- `1` a leállítási sorozat üzeneteihez, `0` a rendszeres közleményekhez

Az üzenet rendszer nem indítja újra a szervert. Csak figyelmeztetéseket jelenít meg, amikor az újraindítási ütemezés kívülről van konfigurálva.

---

[Kezdőlap](../README.md) | [<< Előző: Hibaelhárítás](11-troubleshooting.md) | [9. rész kezdőlap](01-server-setup.md)
