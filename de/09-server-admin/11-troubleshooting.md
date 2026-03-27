# Kapitel 9.11: Server-Fehlerbehebung

[Home](../README.md) | [<< Zurueck: Mod-Verwaltung](10-mod-management.md) | [Weiter: Fortgeschrittene Themen >>](12-advanced.md)

---

> **Zusammenfassung:** Diagnostizieren und beheben Sie die haeufigsten DayZ-Server-Probleme -- Startfehler, Verbindungsprobleme, Abstuerze, Loot- und Fahrzeug-Spawning, Persistenz und Performance. Jede Loesung hier stammt aus realen Fehlermustern ueber Tausende von Community-Berichten.

---

## Inhaltsverzeichnis

- [Server startet nicht](#server-startet-nicht)
- [Spieler koennen sich nicht verbinden](#spieler-koennen-sich-nicht-verbinden)
- [Abstuerze und Null-Pointer](#abstuerze-und-null-pointer)
- [Loot spawnt nicht](#loot-spawnt-nicht)
- [Fahrzeuge spawnen nicht](#fahrzeuge-spawnen-nicht)
- [Persistenz-Probleme](#persistenz-probleme)
- [Performance-Probleme](#performance-probleme)
- [Log-Dateien lesen](#log-dateien-lesen)
- [Schnelle Diagnose-Checkliste](#schnelle-diagnose-checkliste)

---

## Server startet nicht

### Fehlende DLL-Dateien

Wenn `DayZServer_x64.exe` sofort mit einem fehlenden-DLL-Fehler abstuerzt, installieren Sie die neueste **Visual C++ Redistributable fuer Visual Studio 2019** (x64) von der offiziellen Microsoft-Website und starten Sie neu.

### Port bereits belegt

Eine andere DayZ-Instanz oder Anwendung belegt Port 2302. Pruefen Sie mit `netstat -ano | findstr 2302` (Windows) oder `ss -tulnp | grep 2302` (Linux). Beenden Sie den konkurrierenden Prozess oder aendern Sie Ihren Port mit `-port=2402`.

### Fehlender Missionsordner

Der Server erwartet `mpmissions/<template>/`, wobei der Ordnername exakt mit dem `template`-Wert in **serverDZ.cfg** uebereinstimmen muss. Fuer Chernarus ist das `mpmissions/dayzOffline.chernarusplus/` und muss mindestens **init.c** enthalten.

### Ungueltige serverDZ.cfg

Ein einziges fehlendes Semikolon oder ein falscher Anfuehrungszeichentyp verhindert den Start stillschweigend. Achten Sie auf:

- Fehlendes `;` am Ende von Wertzeilen
- Typografische Anfuehrungszeichen anstelle gerader Anfuehrungszeichen
- Fehlende `{};`-Bloecke um Klasseneintraege

### Fehlende Mod-Dateien

Jeder Pfad in `-mod=@CF;@VPPAdminTools;@MyMod` muss relativ zum Server-Stammverzeichnis existieren und einen **addons/**-Ordner mit `.pbo`-Dateien enthalten. Ein einziger fehlerhafter Pfad verhindert den Start.

---

## Spieler koennen sich nicht verbinden

### Portweiterleitung

DayZ benoetigt diese Ports weitergeleitet und in Ihrer Firewall geoeffnet:

| Port | Protokoll | Zweck |
|------|-----------|-------|
| 2302 | UDP | Spielverkehr |
| 2303 | UDP | Steam-Networking |
| 2304 | UDP | Steam-Query (intern) |
| 27016 | UDP | Steam-Server-Browser-Query |

Wenn Sie den Basisport mit `-port=` geaendert haben, verschieben sich alle anderen Ports um denselben Offset.

### Firewall-Blockierung

Fuegen Sie **DayZServer_x64.exe** zu den Firewall-Ausnahmen Ihres Betriebssystems hinzu. Unter Windows: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. Unter Linux oeffnen Sie die Ports mit `ufw` oder `iptables`.

### Mod-Mismatch

Clients muessen exakt dieselben Mod-Versionen wie der Server haben. Wenn ein Spieler "Mod mismatch" sieht, hat eine Seite eine veraltete Version. Aktualisieren Sie beide, wenn ein Mod ein Workshop-Update erhaelt.

### Fehlende .bikey-Dateien

Die `.bikey`-Datei jedes Mods muss im `keys/`-Verzeichnis des Servers liegen. Ohne sie lehnt BattlEye die signierten PBOs des Clients ab. Schauen Sie in den `keys/`- oder `key/`-Ordner jedes Mods.

### Server voll

Pruefen Sie `maxPlayers` in **serverDZ.cfg** (Standard 60).

---

## Abstuerze und Null-Pointer

### Null-Pointer-Zugriff

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- der haeufigste Script-Fehler. Ein Mod ruft eine Methode auf einem geloeschten oder nicht initialisierten Objekt auf. Dies ist ein Mod-Bug, keine Fehlkonfiguration des Servers. Melden Sie es dem Mod-Autor mit dem vollstaendigen RPT-Log.

### Script-Fehler finden

Durchsuchen Sie das RPT-Log nach `SCRIPT (E)`. Der Klassen- und Methodenname im Fehler zeigt Ihnen, welcher Mod verantwortlich ist. RPT-Speicherorte:

- **Server:** `$profiles/`-Verzeichnis (oder Server-Stammverzeichnis, wenn kein `-profiles=` gesetzt ist)
- **Client:** `%localappdata%\DayZ\`

### Absturz beim Neustart

Wenn der Server bei jedem Neustart abstuerzt, ist moeglicherweise **storage_1/** beschaedigt. Stoppen Sie den Server, erstellen Sie ein Backup von `storage_1/`, loeschen Sie `storage_1/data/events.bin` und starten Sie neu. Wenn das fehlschlaegt, loeschen Sie das gesamte `storage_1/`-Verzeichnis (loescht alle Persistenz).

### Absturz nach Mod-Update

Kehren Sie zur vorherigen Mod-Version zurueck. Pruefen Sie das Workshop-Aenderungsprotokoll auf brechende Aenderungen -- umbenannte Klassen, entfernte Konfigurationen und geaenderte RPC-Formate sind haeufige Ursachen.

---

## Loot spawnt nicht

### types.xml nicht registriert

Items, die in **types.xml** definiert sind, spawnen nicht, es sei denn, die Datei ist in **cfgeconomycore.xml** registriert:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Wenn Sie eine benutzerdefinierte Types-Datei verwenden (z.B. **types_custom.xml**), fuegen Sie einen separaten `<file>`-Eintrag dafuer hinzu.

### Falsche Kategorie-, Usage- oder Value-Tags

Jedes `<category>`-, `<usage>`- und `<value>`-Tag in Ihrer types.xml muss mit einem in **cfglimitsdefinition.xml** definierten Namen uebereinstimmen. Ein Tippfehler wie `usage name="Military"` (grosses M), wenn die Definition `military` (Kleinbuchstaben) sagt, verhindert stillschweigend das Spawnen des Items.

### Nominal auf Null gesetzt

Wenn `nominal` `0` ist, wird die CE dieses Item nie spawnen. Dies ist beabsichtigt fuer Items, die nur durch Herstellung, Events oder Admin-Platzierung existieren sollen. Wenn Sie moechten, dass das Item natuerlich spawnt, setzen Sie `nominal` auf mindestens `1`.

### Fehlende Kartengruppen-Positionen

Items benoetigen gueltige Spawn-Positionen in Gebaeuden. Wenn ein benutzerdefiniertes Item keine passenden Kartengruppen-Positionen hat (definiert in **mapgroupproto.xml**), hat die CE keinen Platz dafuer. Weisen Sie dem Item Kategorien und Usages zu, die bereits gueltige Positionen auf der Karte haben.

---

## Fahrzeuge spawnen nicht

Fahrzeuge verwenden das Eventsystem, **nicht** types.xml.

### events.xml-Konfiguration

Fahrzeug-Spawns werden in **events.xml** definiert:

```xml
<event name="VehicleOffroadHatchback">
    <nominal>8</nominal>
    <min>5</min>
    <max>8</max>
    <lifetime>3888000</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="1" min="1" type="OffroadHatchback"/>
    </children>
</event>
```

### Fehlende Spawn-Positionen

Fahrzeug-Events mit `<position>fixed</position>` benoetigen Eintraege in **cfgeventspawns.xml**. Ohne definierte Koordinaten hat das Event keinen Platz, um das Fahrzeug zu platzieren.

### Event deaktiviert

Wenn `<active>0</active>`, ist das Event komplett deaktiviert. Setzen Sie es auf `1`.

### Beschaedigte Fahrzeuge blockieren Slots

Wenn `remove_damaged="0"`, bleiben zerstoerte Fahrzeuge fuer immer in der Welt und belegen Spawn-Slots. Setzen Sie `remove_damaged="1"`, damit die CE Wracks aufraeumt und Ersatz spawnt.

---

## Persistenz-Probleme

### Basen verschwinden

Territorium-Fahnen muessen aufgefrischt werden, bevor ihr Timer ablaeuft. Die Standard-`FlagRefreshFrequency` betraegt `432000` Sekunden (5 Tage). Wenn kein Spieler innerhalb dieses Zeitfensters mit der Fahne interagiert, werden die Fahne und alle Objekte in ihrem Radius geloescht.

Pruefen Sie den Wert in **globals.xml**:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Erhoehen Sie diesen Wert auf Servern mit geringer Bevoelkerung, auf denen sich Spieler seltener einloggen.

### Items verschwinden nach Neustart

Jedes Item hat eine `lifetime` in **types.xml** (Sekunden). Wenn sie ohne Spielerinteraktion ablaeuft, entfernt die CE es. Referenz: `3888000` = 45 Tage, `604800` = 7 Tage, `14400` = 4 Stunden. Items in Containern erben die Lebensdauer des Containers.

### storage_1/ wird zu gross

Wenn Ihr `storage_1/`-Verzeichnis ueber mehrere hundert MB hinauswaechst, produziert Ihre Wirtschaft zu viele Items. Reduzieren Sie `nominal`-Werte in Ihrer types.xml, insbesondere fuer Items mit hoher Anzahl wie Nahrung, Kleidung und Munition. Eine aufgeblaehte Persistenzdatei verursacht laengere Neustartzeiten.

### Spielerdaten verloren

Spielerinventare und -positionen werden in `storage_1/players/` gespeichert. Wenn dieses Verzeichnis geloescht oder beschaedigt wird, spawnen alle Spieler frisch. Erstellen Sie regelmaessig Backups von `storage_1/`.

---

## Performance-Probleme

### Server-FPS sinken

DayZ-Server zielen auf 30+ FPS fuer fluessiges Gameplay. Haeufige Ursachen fuer niedrige Server-FPS:

- **Zu viele Zombies** -- reduzieren Sie `ZombieMaxCount` in **globals.xml** (Standard 800, versuchen Sie 400-600)
- **Zu viele Tiere** -- reduzieren Sie `AnimalMaxCount` (Standard 200, versuchen Sie 100)
- **Uebermaessiges Loot** -- senken Sie `nominal`-Werte in Ihrer types.xml
- **Zu viele Basis-Objekte** -- grosse Basen mit Hunderten von Items belasten die Persistenz
- **Script-intensive Mods** -- einige Mods fuehren teure Pro-Frame-Logik aus

### Desync

Spieler, die Rubberbanding, verzoegerte Aktionen oder unsichtbare Zombies erleben, sind Symptome von Desync. Dies bedeutet fast immer, dass die Server-FPS unter 15 gefallen sind. Beheben Sie das zugrunde liegende Performance-Problem, anstatt nach einer desyncspezifischen Einstellung zu suchen.

### Lange Neustartzeiten

Die Neustartzeit ist direkt proportional zur Groesse von `storage_1/`. Wenn Neustarts mehr als 2-3 Minuten dauern, haben Sie zu viele persistente Objekte. Reduzieren Sie Loot-Nominalwerte und setzen Sie angemessene Lebensdauern.

---

## Log-Dateien lesen

### Server-RPT-Speicherort

Die RPT-Datei befindet sich in `$profiles/` (wenn mit `-profiles=` gestartet) oder im Server-Stammverzeichnis. Dateinamenmuster: `DayZServer_x64_<datum>_<zeit>.RPT`.

### Wonach suchen

| Suchbegriff | Bedeutung |
|-------------|-----------|
| `SCRIPT (E)` | Script-Fehler -- ein Mod hat einen Bug |
| `[ERROR]` | Engine-Level-Fehler |
| `ErrorMessage` | Fataler Fehler, der moeglicherweise zum Herunterfahren fuehrt |
| `Cannot open` | Fehlende Datei (PBO, Konfiguration, Mission) |
| `Crash` | Anwendungs-Level-Absturz |

### BattlEye-Logs

BattlEye-Logs befinden sich im `BattlEye/`-Verzeichnis innerhalb Ihres Server-Stammverzeichnisses. Diese zeigen Kick- und Sperrereignisse. Wenn Spieler unerwartete Kicks melden, pruefen Sie hier zuerst.

---

## Schnelle Diagnose-Checkliste

Wenn etwas schiefgeht, arbeiten Sie diese Liste der Reihe nach durch:

```
1. Pruefen Sie das Server-RPT auf SCRIPT (E)- und [ERROR]-Zeilen
2. Stellen Sie sicher, dass jeder -mod=-Pfad existiert und addons/*.pbo enthaelt
3. Stellen Sie sicher, dass alle .bikey-Dateien nach keys/ kopiert wurden
4. Pruefen Sie serverDZ.cfg auf Syntaxfehler (fehlende Semikolons)
5. Pruefen Sie Portweiterleitung: 2302 UDP + 27016 UDP
6. Stellen Sie sicher, dass der Missionsordner mit dem template-Wert in serverDZ.cfg uebereinstimmt
7. Pruefen Sie storage_1/ auf Beschaedigung (events.bin loeschen, falls noetig)
8. Testen Sie zuerst ohne Mods, dann fuegen Sie Mods einzeln hinzu
```

Schritt 8 ist die wirkungsvollste Technik. Wenn der Server vanilla funktioniert, aber mit Mods nicht, koennen Sie den Problem-Mod durch binaere Suche isolieren -- fuegen Sie die Haelfte Ihrer Mods hinzu, testen Sie, dann grenzen Sie ein.

---

[Home](../README.md) | [<< Zurueck: Mod-Verwaltung](10-mod-management.md) | [Weiter: Fortgeschrittene Themen >>](12-advanced.md)
