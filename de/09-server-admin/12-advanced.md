# Kapitel 9.12: Fortgeschrittene Server-Themen

[Home](../README.md) | [<< Zurueck: Fehlerbehebung](11-troubleshooting.md) | [Teil 9 Startseite](01-server-setup.md)

---

> **Zusammenfassung:** Erweiterte Konfigurationsdateien, Multi-Map-Setups, Wirtschafts-Splitting, Tierterritorien, dynamische Events, Wettersteuerung, automatisierte Neustarts und das Nachrichtensystem.

---

## Inhaltsverzeichnis

- [cfggameplay.json im Detail](#cfggameplayjson-im-detail)
- [Multi-Map-Server](#multi-map-server)
- [Benutzerdefinierte Wirtschaftsanpassung](#benutzerdefinierte-wirtschaftsanpassung)
- [cfgenvironment.xml und Tierterritorien](#cfgenvironmentxml-und-tierterritorien)
- [Benutzerdefinierte dynamische Events](#benutzerdefinierte-dynamische-events)
- [Automatisierung des Server-Neustarts](#automatisierung-des-server-neustarts)
- [cfgweather.xml](#cfgweatherxml)
- [Nachrichtensystem](#nachrichtensystem)

---

## cfggameplay.json im Detail

Die Datei **cfggameplay.json** befindet sich in Ihrem Missionsordner und ueberschreibt hartcodierte Gameplay-Standardwerte. Aktivieren Sie sie zuerst in **serverDZ.cfg**:

```cpp
enableCfgGameplayFile = 1;
```

Vanilla-Struktur:

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

- `version` -- muss mit dem uebereinstimmen, was Ihre Server-Binaerdatei erwartet. Nicht aendern.
- `lightingConfig` -- `0` (Standard) oder `1` (hellere Naechte).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 Werte, einer pro Monat (Jan-Dez).
- `disablePersonalLight` -- entfernt das schwache Umgebungslicht bei neuen Spielern nachts.
- `staminaMax` und Sprint-Modifikatoren steuern, wie weit Spieler rennen koennen, bevor sie erschoepft sind.
- `use3DMap` -- wechselt die In-Game-Karte zur gelaendegerenderten 3D-Variante.

---

## Multi-Map-Server

DayZ unterstuetzt mehrere Karten ueber verschiedene Missionsordner in `mpmissions/`:

| Karte | Missionsordner |
|-------|---------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Jede Karte hat ihre eigenen CE-Dateien (`types.xml`, `events.xml` usw.). Wechseln Sie die Karte ueber `template` in **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Oder mit einem Startparameter: `-mission=mpmissions/dayzOffline.enoch`

Um mehrere Karten gleichzeitig zu betreiben, verwenden Sie separate Server-Instanzen mit eigener Konfiguration, eigenem Profilverzeichnis und eigenem Portbereich.

---

## Benutzerdefinierte Wirtschaftsanpassung

### types.xml aufteilen

Teilen Sie Items in mehrere Dateien auf und registrieren Sie sie in **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

Der Server laedt und vereint alle Dateien mit `type="types"`.

### Benutzerdefinierte Kategorien und Tags

**cfglimitsdefinition.xml** definiert Kategorien/Tags fuer `types.xml`, wird aber bei Updates ueberschrieben. Verwenden Sie stattdessen **cfglimitsdefinitionuser.xml**:

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

## cfgenvironment.xml und Tierterritorien

Die Datei **cfgenvironment.xml** in Ihrem Missionsordner verlinkt zu Territoriumsdateien im `env/`-Unterverzeichnis:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

Der `env/`-Ordner enthaelt diese Tierterritorium-Dateien:

| Datei | Tiere |
|-------|-------|
| **bear_territories.xml** | Braunbaeren |
| **wolf_territories.xml** | Wolfsrudel |
| **fox_territories.xml** | Fuechse |
| **hare_territories.xml** | Kaninchen/Hasen |
| **hen_territories.xml** | Huehner |
| **pig_territories.xml** | Schweine |
| **red_deer_territories.xml** | Rothirsche |
| **roe_deer_territories.xml** | Rehe |
| **sheep_goat_territories.xml** | Schafe/Ziegen |
| **wild_boar_territories.xml** | Wildschweine |
| **cattle_territories.xml** | Kuehe |

Ein Territoriumseintrag definiert kreisfoermige Zonen mit Position und Tieranzahl:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- Mittelpunktkoordinaten; `r` -- Radius in Metern
- `dmin`, `dmax` -- minimale/maximale Tieranzahl in der Zone
- `smin`, `smax` -- reserviert (auf `-1` setzen)

---

## Benutzerdefinierte dynamische Events

Dynamische Events (Heliabstuerze, Konvois) werden in **events.xml** definiert. Um ein benutzerdefiniertes Event zu erstellen:

**1. Event definieren** in **events.xml**:

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

**2. Spawn-Positionen hinzufuegen** in **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Infizierte Wachen hinzufuegen** (optional) -- fuegen Sie `<secondary type="ZmbM_PatrolNormal_Autumn" />`-Elemente in Ihre Event-Definition ein.

**4. Gruppierte Spawns** (optional) -- definieren Sie Cluster in **cfgeventgroups.xml** und referenzieren Sie den Gruppennamen in Ihrem Event.

---

## Automatisierung des Server-Neustarts

DayZ hat keinen eingebauten Neustart-Scheduler. Verwenden Sie Automatisierung auf Betriebssystemebene.

### Windows

Erstellen Sie **restart_server.bat** und fuehren Sie es ueber eine geplante Windows-Aufgabe alle 4-6 Stunden aus:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Erstellen Sie ein Shell-Skript und fuegen Sie es zu cron hinzu (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Erstellen Sie immer ein Backup von `storage_1/` vor jedem Neustart. Beschaedigte Persistenz waehrend des Herunterfahrens kann Spielerbasen und Fahrzeuge loeschen.

---

## cfgweather.xml

Die Datei **cfgweather.xml** in Ihrem Missionsordner steuert Wettermuster. Jede Karte wird mit eigenen Standardwerten ausgeliefert:

Jedes Phaenomen hat `min`, `max`, `duration_min` und `duration_max` (Sekunden):

| Phaenomen | Standard Min | Standard Max | Hinweise |
|-----------|-------------|-------------|----------|
| `overcast` | 0.0 | 1.0 | Steuert Wolkendichte und Regenwahrscheinlichkeit |
| `rain` | 0.0 | 1.0 | Wird erst ueber einem Bewoelkungsschwellenwert ausgeloest. Max auf `0.0` setzen fuer keinen Regen |
| `fog` | 0.0 | 0.3 | Werte ueber `0.5` erzeugen nahezu Nullsicht |
| `wind_magnitude` | 0.0 | 18.0 | Beeinflusst Ballistik und Spielerbewegung |

---

## Nachrichtensystem

Die Datei **db/messages.xml** in Ihrem Missionsordner steuert geplante Servernachrichten und Herunterfahren-Warnungen:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- Minuten, bevor die Nachricht ausgeloest wird (fuer Herunterfahren-Nachrichten, Minuten bevor der Server stoppt)
- `shutdown` -- `1` fuer Herunterfahren-Sequenz-Nachrichten, `0` fuer regulaere Rundrufe

Das Nachrichtensystem startet den Server nicht neu. Es zeigt nur Warnungen an, wenn ein Neustart-Zeitplan extern konfiguriert ist.

---

[Home](../README.md) | [<< Zurueck: Fehlerbehebung](11-troubleshooting.md) | [Teil 9 Startseite](01-server-setup.md)
