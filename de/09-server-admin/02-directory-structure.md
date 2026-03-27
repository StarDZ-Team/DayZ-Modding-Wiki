# Kapitel 9.2: Verzeichnisstruktur & Missionsordner

[Home](../README.md) | [<< Zurueck: Server-Einrichtung](01-server-setup.md) | **Verzeichnisstruktur** | [Weiter: serverDZ.cfg-Referenz >>](03-server-cfg.md)

---

> **Zusammenfassung:** Ein vollstaendiger Rundgang durch jede Datei und jeden Ordner im DayZ-Server-Verzeichnis und im Missionsordner. Zu wissen, was jede Datei tut -- und welche sicher bearbeitet werden koennen -- ist unerlaeasslich, bevor Sie die Loot-Wirtschaft anpassen oder Mods hinzufuegen.

---

## Inhaltsverzeichnis

- [Server-Stammverzeichnis](#server-stammverzeichnis)
- [Der addons/-Ordner](#der-addons-ordner)
- [Der keys/-Ordner](#der-keys-ordner)
- [Der profiles/-Ordner](#der-profiles-ordner)
- [Der mpmissions/-Ordner](#der-mpmissions-ordner)
- [Missionsordner-Struktur](#missionsordner-struktur)
- [Der db/-Ordner -- Wirtschaftskern](#der-db-ordner----wirtschaftskern)
- [Der env/-Ordner -- Tierterritorien](#der-env-ordner----tierterritorien)
- [Der storage_1/-Ordner -- Persistenz](#der-storage_1-ordner----persistenz)
- [Missions-Dateien auf oberster Ebene](#missions-dateien-auf-oberster-ebene)
- [Welche Dateien bearbeiten, welche nicht](#welche-dateien-bearbeiten-welche-nicht)

---

## Server-Stammverzeichnis

```
DayZServer/
  DayZServer_x64.exe          # Server-Ausfuehrungsdatei
  serverDZ.cfg                 # Haupt-Server-Konfiguration (Name, Passwort, Mods, Zeit)
  dayzsetting.xml              # Rendereinstellungen (fuer Dedicated Server irrelevant)
  ban.txt                      # Gesperrte Steam64-IDs, eine pro Zeile
  whitelist.txt                # Freigegebene Steam64-IDs, eine pro Zeile
  steam_appid.txt              # Enthaelt "221100" -- nicht bearbeiten
  dayz.gproj                   # Workbench-Projektdatei -- nicht bearbeiten
  addons/                      # Vanilla-Spiel-PBOs
  battleye/                    # Anti-Cheat-Dateien
  config/                      # Steam-Konfiguration (config.vdf)
  dta/                         # Kern-Engine-PBOs (Scripts, GUI, Grafik)
  keys/                        # Signatur-Verifizierungsschluessel (.bikey-Dateien)
  logs/                        # Engine-Level-Logs
  mpmissions/                  # Alle Missionsordner
  profiles/                    # Laufzeitausgabe (Script-Logs, Spieler-DB, Crash-Dumps)
  server_manager/              # Server-Management-Utilities
```

---

## Der addons/-Ordner

Enthaelt den gesamten Vanilla-Spielinhalt als PBO-Dateien. Jede PBO hat eine passende `.bisign`-Signaturdatei:

```
addons/
  ai.pbo                       # KI-Verhaltens-Scripts
  ai.pbo.dayz.bisign           # Signatur fuer ai.pbo
  animals.pbo                  # Tierdefinitionen
  characters_backpacks.pbo     # Rucksack-Modelle/Konfigurationen
  characters_belts.pbo         # Guertel-Item-Modelle
  weapons_firearms.pbo         # Waffen-Modelle/Konfigurationen
  ... (100+ PBO-Dateien)
```

**Bearbeiten Sie diese Dateien niemals.** Sie werden bei jedem Server-Update ueber SteamCMD ueberschrieben. Mods ueberschreiben Vanilla-Verhalten durch das `modded`-Klassensystem, nicht durch Aendern von PBOs.

---

## Der keys/-Ordner

Enthaelt `.bikey`-Public-Key-Dateien zur Verifizierung von Mod-Signaturen:

```
keys/
  dayz.bikey                   # Vanilla-Signaturschluessel (immer vorhanden)
```

Wenn Sie einen Mod hinzufuegen, kopieren Sie dessen `.bikey`-Datei in diesen Ordner. Der Server verwendet `verifySignatures = 2` in `serverDZ.cfg`, um jede PBO abzulehnen, die keine passende `.bikey` in diesem Ordner hat.

Wenn ein Spieler einen Mod laedt, dessen Schluessel nicht in Ihrem `keys/`-Ordner liegt, erhaelt er einen **"Signature check failed"**-Kick.

---

## Der profiles/-Ordner

Wird beim ersten Server-Start erstellt. Enthaelt Laufzeitausgaben:

```
profiles/
  BattlEye/                              # BE-Logs und Sperren
  DataCache/                             # Zwischengespeicherte Daten
  Users/                                 # Spieler-spezifische Einstellungsdateien
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Admin-Log
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Engine-Bericht (Crash-Infos, Warnungen)
  script_2026-03-08_11-34-35.log           # Script-Log (Ihr wichtigstes Debug-Tool)
```

Das **Script-Log** ist die wichtigste Datei hier. Jeder `Print()`-Aufruf, jeder Script-Fehler und jede Mod-Lademeldung wird hier protokolliert. Wenn etwas nicht funktioniert, schauen Sie hier zuerst nach.

Log-Dateien sammeln sich mit der Zeit an. Alte Logs werden nicht automatisch geloescht.

---

## Der mpmissions/-Ordner

Enthaelt einen Unterordner pro Karte:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (kostenlos)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

Das Ordnernamenformat ist `<missionName>.<terrainName>`. Der `template`-Wert in `serverDZ.cfg` muss exakt mit einem dieser Ordnernamen uebereinstimmen.

---

## Missionsordner-Struktur

Der Chernarus-Missionsordner (`mpmissions/dayzOffline.chernarusplus/`) enthaelt:

```
dayzOffline.chernarusplus/
  init.c                         # Missions-Einstiegspunkt-Script
  db/                            # Kern-Wirtschaftsdateien
  env/                           # Tierterritorium-Definitionen
  storage_1/                     # Persistenzdaten (Spieler, Weltzustand)
  cfgeconomycore.xml             # Wirtschafts-Root-Klassen und Logging-Einstellungen
  cfgenvironment.xml             # Verknuepfungen zu Tierterritorium-Dateien
  cfgeventgroups.xml             # Event-Gruppen-Definitionen
  cfgeventspawns.xml             # Exakte Spawn-Positionen fuer Events (Fahrzeuge usw.)
  cfgeffectarea.json             # Kontaminierte-Zonen-Definitionen
  cfggameplay.json               # Gameplay-Feineinstellungen (Ausdauer, Schaden, Bauen)
  cfgignorelist.xml              # Items, die komplett von der Wirtschaft ausgeschlossen sind
  cfglimitsdefinition.xml        # Gueltige Kategorie-/Usage-/Value-Tag-Definitionen
  cfglimitsdefinitionuser.xml    # Benutzerdefinierte Tag-Definitionen
  cfgplayerspawnpoints.xml       # Spawn-Orte fuer neue Spieler
  cfgrandompresets.xml           # Wiederverwendbare Loot-Pool-Definitionen
  cfgspawnabletypes.xml          # Vorinstallierte Items und Ladung bei gespawnten Entitaeten
  cfgundergroundtriggers.json    # Unterirdische Bereichs-Trigger
  cfgweather.xml                 # Wetterkonfiguration
  areaflags.map                  # Bereichsflag-Daten (binaer)
  mapclusterproto.xml            # Kartencluster-Prototyp-Definitionen
  mapgroupcluster.xml            # Gebaeude-Gruppencluster-Definitionen
  mapgroupcluster01.xml          # Clusterdaten (Teil 1)
  mapgroupcluster02.xml          # Clusterdaten (Teil 2)
  mapgroupcluster03.xml          # Clusterdaten (Teil 3)
  mapgroupcluster04.xml          # Clusterdaten (Teil 4)
  mapgroupdirt.xml               # Boden-Loot-Positionen
  mapgrouppos.xml                # Kartengruppen-Positionen
  mapgroupproto.xml              # Prototyp-Definitionen fuer Kartengruppen
```

---

## Der db/-Ordner -- Wirtschaftskern

Dies ist das Herzstück der Zentralwirtschaft. Fuenf Dateien steuern, was spawnt, wo und wie viel:

```
db/
  types.xml        # DIE Schluesseldatei: definiert die Spawn-Regeln jedes Items
  globals.xml      # Globale Wirtschaftsparameter (Timer, Limits, Zaehler)
  events.xml       # Dynamische Events (Tiere, Fahrzeuge, Helikopter)
  economy.xml      # Schalter fuer Wirtschaftssubsysteme (Loot, Tiere, Fahrzeuge)
  messages.xml     # Geplante Servernachrichten an Spieler
```

### types.xml

Definiert Spawn-Regeln fuer **jedes Item** im Spiel. Mit etwa 23.000 Zeilen ist dies bei weitem die groesste Wirtschaftsdatei. Jeder Eintrag gibt an, wie viele Kopien eines Items auf der Karte existieren sollen, wo es spawnen kann und wie lange es bestehen bleibt. Siehe [Kapitel 9.4](04-loot-economy.md) fuer eine ausfuehrliche Erklaerung.

### globals.xml

Globale Parameter, die die gesamte Wirtschaft betreffen: Zombie-Anzahlen, Tieranzahlen, Aufraeum-Timer, Loot-Schadensbereiche, Respawn-Zeiten. Es gibt insgesamt 33 Parameter. Siehe [Kapitel 9.4](04-loot-economy.md) fuer die vollstaendige Referenz.

### events.xml

Definiert dynamische Spawn-Events fuer Tiere und Fahrzeuge. Jedes Event gibt eine Sollanzahl, Spawn-Einschraenkungen und Kindvarianten an. Zum Beispiel spawnt das Event `VehicleCivilianSedan` 8 Limousinen in 3 Farbvarianten ueber die Karte verteilt.

### economy.xml

Hauptschalter fuer Wirtschaftssubsysteme:

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

| Flag | Bedeutung |
|------|-----------|
| `init` | Items beim ersten Serverstart spawnen |
| `load` | Gespeicherten Zustand aus der Persistenz laden |
| `respawn` | Respawn von Items nach Aufraeumung erlauben |
| `save` | Zustand in Persistenzdateien speichern |

### messages.xml

Geplante Nachrichten, die an alle Spieler gesendet werden. Unterstuetzt Countdown-Timer, Wiederholungsintervalle, Begruessung bei Verbindung und Herunterfahren-Warnungen:

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

Verwenden Sie `#name` fuer den Servernamen und `#tmin` fuer die verbleibende Zeit in Minuten.

---

## Der env/-Ordner -- Tierterritorien

Enthaelt XML-Dateien, die festlegen, wo jede Tierart spawnen kann:

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

Diese Dateien enthalten Hunderte von Koordinatenpunkten, die Territorienzonen ueber die Karte definieren. Sie werden von `cfgenvironment.xml` referenziert. Sie muessen diese selten bearbeiten, es sei denn, Sie moechten aendern, wo Tiere oder Zombies geografisch spawnen.

---

## Der storage_1/-Ordner -- Persistenz

Speichert den persistenten Zustand des Servers zwischen Neustarts:

```
storage_1/
  players.db         # SQLite-Datenbank aller Spielercharaktere
  spawnpoints.bin    # Binaere Spawnpunkt-Daten
  backup/            # Automatische Backups der Persistenzdaten
  data/              # Weltzustand (platzierte Items, Basisbau, Fahrzeuge)
```

**Bearbeiten Sie niemals `players.db`, waehrend der Server laeuft.** Es handelt sich um eine SQLite-Datenbank, die vom Serverprozess gesperrt wird. Wenn Sie Charaktere zuruecksetzen muessen, stoppen Sie zuerst den Server und loeschen oder benennen Sie die Datei um.

Fuer einen **vollstaendigen Persistenz-Wipe** stoppen Sie den Server und loeschen den gesamten `storage_1/`-Ordner. Der Server erstellt ihn beim naechsten Start mit einer frischen Welt neu.

Fuer einen **teilweisen Wipe** (Charaktere behalten, Loot zuruecksetzen):
1. Server stoppen
2. Dateien in `storage_1/data/` loeschen, aber `players.db` behalten
3. Neustarten

---

## Missions-Dateien auf oberster Ebene

### cfgeconomycore.xml

Registriert Root-Klassen fuer die Wirtschaft und konfiguriert CE-Logging:

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

Setzen Sie `log_ce_lootspawn` auf `"true"`, wenn Sie Item-Spawn-Probleme debuggen. Dies erzeugt detaillierte Ausgaben im RPT-Log, die zeigen, welche Items die CE zu spawnen versucht und warum sie erfolgreich sind oder fehlschlagen.

### cfglimitsdefinition.xml

Definiert die gueltigen Werte fuer `<category>`-, `<usage>`-, `<value>`- und `<tag>`-Elemente, die in `types.xml` verwendet werden:

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

Wenn Sie ein `<usage>`- oder `<value>`-Tag in `types.xml` verwenden, das hier nicht definiert ist, wird das Item stillschweigend nicht spawnen.

### cfgignorelist.xml

Hier aufgefuehrte Items werden vollstaendig von der Wirtschaft ausgeschlossen, selbst wenn sie Eintraege in `types.xml` haben:

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

Dies wird fuer Items verwendet, die im Spielcode existieren, aber nicht natuerlich spawnen sollen (unfertige Items, veraltete Inhalte, saisonale Items ausserhalb der Saison).

### cfggameplay.json

Eine JSON-Datei, die Gameplay-Parameter ueberschreibt. Steuert Ausdauer, Bewegung, Basisschaden, Wetter, Temperatur, Waffenobstruktion, Ertrinken und mehr. Diese Datei ist optional -- fehlt sie, verwendet der Server die Standardwerte.

### cfgplayerspawnpoints.xml

Definiert, wo frisch gespawnte Spieler auf der Karte erscheinen, mit Abstandseinschraenkungen zu Infizierten, anderen Spielern und Gebaeuden.

### cfgeventspawns.xml

Enthaelt exakte Weltkoordinaten, an denen Events (Fahrzeuge, Heliabstuerze usw.) spawnen koennen. Jeder Eventname aus `events.xml` hat eine Liste gueltiger Positionen:

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

Das `a`-Attribut ist der Rotationswinkel in Grad.

---

## Welche Dateien bearbeiten, welche nicht

| Datei / Ordner | Sicher zu bearbeiten? | Hinweise |
|----------------|:---:|---------|
| `serverDZ.cfg` | Ja | Haupt-Server-Konfiguration |
| `db/types.xml` | Ja | Item-Spawn-Regeln -- Ihre haeufigste Bearbeitung |
| `db/globals.xml` | Ja | Wirtschafts-Feineinstellungsparameter |
| `db/events.xml` | Ja | Fahrzeug-/Tier-Spawn-Events |
| `db/economy.xml` | Ja | Wirtschaftssubsystem-Schalter |
| `db/messages.xml` | Ja | Server-Broadcast-Nachrichten |
| `cfggameplay.json` | Ja | Gameplay-Feineinstellungen |
| `cfgspawnabletypes.xml` | Ja | Anbauteile-/Ladungs-Voreinstellungen |
| `cfgrandompresets.xml` | Ja | Loot-Pool-Definitionen |
| `cfglimitsdefinition.xml` | Ja | Benutzerdefinierte Usage-/Value-Tags hinzufuegen |
| `cfgplayerspawnpoints.xml` | Ja | Spieler-Spawn-Orte |
| `cfgeventspawns.xml` | Ja | Event-Spawn-Koordinaten |
| `cfgignorelist.xml` | Ja | Items von der Wirtschaft ausschliessen |
| `cfgweather.xml` | Ja | Wettermuster |
| `cfgeffectarea.json` | Ja | Kontaminierte Zonen |
| `init.c` | Ja | Missions-Einstiegs-Script |
| `addons/` | **Nein** | Wird beim Update ueberschrieben |
| `dta/` | **Nein** | Kern-Engine-Daten |
| `keys/` | Nur hinzufuegen | Mod-`.bikey`-Dateien hierher kopieren |
| `storage_1/` | Nur loeschen | Persistenz -- nicht von Hand bearbeiten |
| `battleye/` | **Nein** | Anti-Cheat -- nicht anfassen |
| `mapgroup*.xml` | Vorsichtig | Gebaeude-Loot-Positionen -- nur fuer fortgeschrittene Bearbeitung |

---

**Zurueck:** [Server-Einrichtung](01-server-setup.md) | [Home](../README.md) | **Weiter:** [serverDZ.cfg-Referenz >>](03-server-cfg.md)
