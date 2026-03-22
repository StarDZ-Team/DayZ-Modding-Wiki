# Kapitel 8.1: Ihre erste Mod (Hello World)

[Startseite](../../README.md) | **Ihre erste Mod** | [Weiter: Ein eigenes Item erstellen >>](02-custom-item.md)

---

## Inhaltsverzeichnis

- [Voraussetzungen](#voraussetzungen)
- [Schritt 1: DayZ Tools installieren](#schritt-1-dayz-tools-installieren)
- [Schritt 2: Das P:-Laufwerk einrichten (Workdrive)](#schritt-2-das-p-laufwerk-einrichten-workdrive)
- [Schritt 3: Die Mod-Verzeichnisstruktur erstellen](#schritt-3-die-mod-verzeichnisstruktur-erstellen)
- [Schritt 4: mod.cpp schreiben](#schritt-4-modcpp-schreiben)
- [Schritt 5: config.cpp schreiben](#schritt-5-configcpp-schreiben)
- [Schritt 6: Ihr erstes Skript schreiben](#schritt-6-ihr-erstes-skript-schreiben)
- [Schritt 7: Das PBO mit Addon Builder packen](#schritt-7-das-pbo-mit-addon-builder-packen)
- [Schritt 8: Die Mod in DayZ laden](#schritt-8-die-mod-in-dayz-laden)
- [Schritt 9: Im Script-Log ueberpruefen](#schritt-9-im-script-log-ueberpruefen)
- [Schritt 10: Haeufige Probleme beheben](#schritt-10-haeufige-probleme-beheben)
- [Vollstaendige Dateireferenz](#vollstaendige-dateireferenz)
- [Naechste Schritte](#naechste-schritte)

---

## Voraussetzungen

Bevor Sie beginnen, stellen Sie sicher, dass Sie haben:

- **Steam** installiert und eingeloggt
- **DayZ** installiert (Retail-Version von Steam)
- Einen **Texteditor** (VS Code, Notepad++ oder sogar Notepad)
- Etwa **15 GB freien Speicherplatz** fuer DayZ Tools

Das ist alles. Fuer dieses Tutorial ist keine Programmiererfahrung erforderlich -- jede Codezeile wird erklaert.

---

## Schritt 1: DayZ Tools installieren

DayZ Tools ist eine kostenlose Anwendung auf Steam, die alles enthaelt, was Sie zum Erstellen von Mods benoetigen: den Workbench-Skripteditor, Addon Builder zum PBO-Packen, Terrain Builder und Object Builder.

### Installation

1. Oeffnen Sie **Steam**
2. Gehen Sie zur **Bibliothek**
3. Aendern Sie im Dropdown-Filter oben **Spiele** zu **Tools**
4. Suchen Sie nach **DayZ Tools**
5. Klicken Sie auf **Installieren**
6. Warten Sie, bis der Download abgeschlossen ist (ca. 12-15 GB)

Nach der Installation finden Sie DayZ Tools in Ihrer Steam-Bibliothek unter Tools. Der Standard-Installationspfad ist:

```
C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\
```

### Was installiert wird

| Tool | Zweck |
|------|---------|
| **Addon Builder** | Packt Ihre Mod-Dateien in `.pbo`-Archive |
| **Workbench** | Skripteditor mit Syntaxhervorhebung |
| **Object Builder** | 3D-Modellbetrachter und -editor fuer `.p3d`-Dateien |
| **Terrain Builder** | Karten-/Gelaendeeditor |
| **TexView2** | Texturbetrachter/-konverter (`.paa`, `.edds`) |

Fuer dieses Tutorial benoetigen Sie nur **Addon Builder**. Die anderen sind spaeter nuetzlich.

---

## Schritt 2: Das P:-Laufwerk einrichten (Workdrive)

DayZ-Modding verwendet einen virtuellen Laufwerksbuchstaben **P:** als gemeinsamen Arbeitsbereich. Alle Mods und Spieldaten referenzieren Pfade ausgehend von P:, was Pfade auf verschiedenen Rechnern konsistent haelt.

### Das P:-Laufwerk erstellen

1. Oeffnen Sie **DayZ Tools** aus Steam
2. Klicken Sie im DayZ-Tools-Hauptfenster auf **P: Drive Management** (oder suchen Sie nach einem Button mit "Mount P drive" / "Setup P drive")
3. Klicken Sie auf **Create/Mount P: Drive**
4. Waehlen Sie einen Speicherort fuer die P:-Laufwerksdaten (Standard ist in Ordnung, oder waehlen Sie ein Laufwerk mit genuegend Platz)
5. Warten Sie, bis der Vorgang abgeschlossen ist

### Ueberpruefen, ob es funktioniert

Oeffnen Sie den **Datei-Explorer** und navigieren Sie zu `P:\`. Sie sollten ein Verzeichnis sehen, das DayZ-Spieldaten enthaelt. Wenn das P:-Laufwerk existiert und Sie es durchsuchen koennen, sind Sie bereit fortzufahren.

### Alternative: Manuelles P:-Laufwerk

Wenn die DayZ-Tools-GUI nicht funktioniert, koennen Sie ein P:-Laufwerk manuell mit einer Windows-Eingabeaufforderung (als Administrator ausfuehren) erstellen:

```batch
subst P: "C:\DayZWorkdrive"
```

Ersetzen Sie `C:\DayZWorkdrive` durch einen beliebigen Ordner. Dies erstellt eine temporaere Laufwerkszuordnung, die bis zum Neustart bestehen bleibt. Fuer eine dauerhafte Zuordnung verwenden Sie `net use` oder die DayZ-Tools-GUI.

### Was, wenn ich kein P:-Laufwerk verwenden moechte?

Sie koennen ohne das P:-Laufwerk entwickeln, indem Sie Ihren Mod-Ordner direkt im DayZ-Spielverzeichnis platzieren und den `-filePatching`-Modus verwenden. Das P:-Laufwerk ist jedoch der Standard-Workflow und alle offizielle Dokumentation setzt es voraus. Wir empfehlen dringend, es einzurichten.

---

## Schritt 3: Die Mod-Verzeichnisstruktur erstellen

Jede DayZ-Mod folgt einer bestimmten Ordnerstruktur. Erstellen Sie die folgenden Verzeichnisse und Dateien auf Ihrem P:-Laufwerk (oder im DayZ-Spielverzeichnis, wenn Sie P: nicht verwenden):

```
P:\MyFirstMod\
    mod.cpp
    Scripts\
        config.cpp
        5_Mission\
            MyFirstMod\
                MissionHello.c
```

### Die Ordner erstellen

1. Oeffnen Sie den **Datei-Explorer**
2. Navigieren Sie zu `P:\`
3. Erstellen Sie einen neuen Ordner namens `MyFirstMod`
4. Erstellen Sie innerhalb von `MyFirstMod` einen Ordner namens `Scripts`
5. Erstellen Sie innerhalb von `Scripts` einen Ordner namens `5_Mission`
6. Erstellen Sie innerhalb von `5_Mission` einen Ordner namens `MyFirstMod`

### Die Struktur verstehen

| Pfad | Zweck |
|------|---------|
| `MyFirstMod/` | Stammverzeichnis Ihrer Mod |
| `mod.cpp` | Metadaten (Name, Autor) die im DayZ-Launcher angezeigt werden |
| `Scripts/config.cpp` | Teilt der Engine mit, wovon Ihre Mod abhaengt und wo die Skripte liegen |
| `Scripts/5_Mission/` | Die Missions-Skriptschicht (UI, Start-Hooks) |
| `Scripts/5_Mission/MyFirstMod/` | Unterordner fuer die Missions-Skripte Ihrer Mod |
| `Scripts/5_Mission/MyFirstMod/MissionHello.c` | Ihre eigentliche Skriptdatei |

Sie benoetigen genau **3 Dateien**. Erstellen wir sie eine nach der anderen.

---

## Schritt 4: mod.cpp schreiben

Erstellen Sie die Datei `P:\MyFirstMod\mod.cpp` in Ihrem Texteditor und fuegen Sie diesen Inhalt ein:

```cpp
name = "My First Mod";
author = "IhrName";
version = "1.0";
overview = "My very first DayZ mod. Prints Hello World to the script log.";
```

### Was jede Zeile macht

- **`name`** -- Der Anzeigename, der in der DayZ-Launcher-Modliste angezeigt wird. Spieler sehen dies bei der Modauswahl.
- **`author`** -- Ihr Name oder Teamname.
- **`version`** -- Ein beliebiger Versionsstring. Die Engine parst ihn nicht.
- **`overview`** -- Eine Beschreibung, die beim Erweitern der Moddetails angezeigt wird.

Speichern Sie die Datei. Das ist der Ausweis Ihrer Mod.

---

## Schritt 5: config.cpp schreiben

Erstellen Sie die Datei `P:\MyFirstMod\Scripts\config.cpp` und fuegen Sie diesen Inhalt ein:

```cpp
class CfgPatches
{
    class MyFirstMod_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data"
        };
    };
};

class CfgMods
{
    class MyFirstMod
    {
        dir = "MyFirstMod";
        name = "My First Mod";
        author = "IhrName";
        type = "mod";

        dependencies[] = { "Mission" };

        class defs
        {
            class missionScriptModule
            {
                value = "";
                files[] = { "MyFirstMod/Scripts/5_Mission" };
            };
        };
    };
};
```

### Was jeder Abschnitt macht

**CfgPatches** deklariert Ihre Mod bei der DayZ-Engine:

- `class MyFirstMod_Scripts` -- Ein eindeutiger Identifikator fuer das Skriptpaket Ihrer Mod. Darf nicht mit einer anderen Mod kollidieren.
- `units[] = {}; weapons[] = {};` -- Listen von Entitaeten und Waffen, die Ihre Mod hinzufuegt. Vorerst leer.
- `requiredVersion = 0.1;` -- Minimale Spielversion. Immer `0.1`.
- `requiredAddons[] = { "DZ_Data" };` -- Abhaengigkeiten. `DZ_Data` sind die Basis-Spieldaten. Dies stellt sicher, dass Ihre Mod **nach** dem Basisspiel geladen wird.

**CfgMods** teilt der Engine mit, wo Ihre Skripte liegen:

- `dir = "MyFirstMod";` -- Stammverzeichnis der Mod.
- `type = "mod";` -- Dies ist eine Client+Server-Mod (im Gegensatz zu `"servermod"` fuer reine Server-Mods).
- `dependencies[] = { "Mission" };` -- Ihr Code klinkt sich in das Mission-Skriptmodul ein.
- `class missionScriptModule` -- Teilt der Engine mit, alle `.c`-Dateien zu kompilieren, die sich in `MyFirstMod/Scripts/5_Mission/` befinden.

**Warum nur `5_Mission`?** Weil unser Hello-World-Skript sich in das Missions-Start-Event einklinkt, das in der Missions-Schicht lebt. Die meisten einfachen Mods beginnen hier.

---

## Schritt 6: Ihr erstes Skript schreiben

Erstellen Sie die Datei `P:\MyFirstMod\Scripts\5_Mission\MyFirstMod\MissionHello.c` und fuegen Sie diesen Inhalt ein:

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The SERVER mission has started.");
    }
};

modded class MissionGameplay
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The CLIENT mission has started.");
    }
};
```

### Zeile-fuer-Zeile-Erklaerung

```c
modded class MissionServer
```
Das `modded`-Schluesselwort ist das Herz des DayZ-Moddings. Es sagt: "Nimm die bestehende `MissionServer`-Klasse aus dem Vanilla-Spiel und fuege meine Aenderungen obendrauf." Sie erstellen keine neue Klasse -- Sie erweitern die bestehende.

```c
    override void OnInit()
```
`OnInit()` wird von der Engine aufgerufen, wenn eine Mission startet. `override` sagt dem Compiler, dass diese Methode bereits in der Elternklasse existiert und wir sie durch unsere Version ersetzen.

```c
        super.OnInit();
```
**Diese Zeile ist kritisch.** `super.OnInit()` ruft die originale Vanilla-Implementierung auf. Wenn Sie dies ueberspringen, laeuft der Vanilla-Missions-Initialisierungscode nie und das Spiel bricht. Rufen Sie `super` immer zuerst auf.

```c
        Print("[MyFirstMod] Hello World! The SERVER mission has started.");
```
`Print()` schreibt eine Nachricht in die DayZ-Script-Logdatei. Das `[MyFirstMod]`-Praefix macht es einfach, Ihre Nachrichten im Log zu finden.

```c
modded class MissionGameplay
```
`MissionGameplay` ist das clientseitige Gegenstueck zu `MissionServer`. Wenn ein Spieler einem Server beitritt, feuert `MissionGameplay.OnInit()` auf dessen Rechner. Durch Modden beider Klassen erscheint Ihre Nachricht sowohl im Server- als auch im Client-Log.

### Ueber `.c`-Dateien

DayZ-Skripte verwenden die `.c`-Dateierweiterung. Trotz des C-aehnlichen Aussehens ist dies **Enforce Script**, DayZ's eigene Skriptsprache. Sie hat Klassen, Vererbung, Arrays und Maps, aber es ist weder C, C++ noch C#. Ihre IDE kann Syntaxfehler anzeigen -- das ist normal und erwartet.

---

## Schritt 7: Das PBO mit Addon Builder packen

DayZ laedt Mods aus `.pbo`-Archivdateien (aehnlich wie .zip, aber in einem Format, das die Engine versteht). Sie muessen Ihren `Scripts`-Ordner in ein PBO packen.

### Addon Builder verwenden (GUI)

1. Oeffnen Sie **DayZ Tools** aus Steam
2. Klicken Sie auf **Addon Builder**, um ihn zu starten
3. Setzen Sie **Source directory** auf: `P:\MyFirstMod\Scripts\`
4. Setzen Sie **Output/Destination directory** auf einen neuen Ordner: `P:\@MyFirstMod\Addons\`

   Erstellen Sie den `@MyFirstMod\Addons\`-Ordner zuerst, falls er nicht existiert.

5. In den **Addon Builder Options**:
   - Setzen Sie **Prefix** auf: `MyFirstMod\Scripts`
   - Lassen Sie andere Optionen auf Standardwerten
6. Klicken Sie auf **Pack**

Bei Erfolg sehen Sie eine Datei unter:

```
P:\@MyFirstMod\Addons\Scripts.pbo
```

### Die endgueltige Mod-Struktur einrichten

Kopieren Sie nun Ihre `mod.cpp` neben den `Addons`-Ordner:

```
P:\@MyFirstMod\
    mod.cpp                         <-- Kopie von P:\MyFirstMod\mod.cpp
    Addons\
        Scripts.pbo                 <-- Vom Addon Builder erstellt
```

Das `@`-Praefix am Ordnernamen ist eine Konvention fuer verteilbare Mods. Es signalisiert Serveradministratoren und dem Launcher, dass dies ein Mod-Paket ist.

### Alternative: Ohne Packen testen (File Patching)

Waehrend der Entwicklung koennen Sie das PBO-Packen komplett ueberspringen, indem Sie den File-Patching-Modus verwenden. Dieser laedt Skripte direkt aus Ihren Quellordnern:

```
DayZDiag_x64.exe -mod=P:\MyFirstMod -filePatching
```

File Patching ist schneller fuer Iterationen, weil Sie eine `.c`-Datei bearbeiten, das Spiel neustarten und die Aenderungen sofort sehen. Kein Packschritt noetig. File Patching funktioniert jedoch nur mit der Diagnose-Executable (`DayZDiag_x64.exe`) und eignet sich nicht zur Verteilung.

---

## Schritt 8: Die Mod in DayZ laden

Es gibt zwei Wege, Ihre Mod zu laden: ueber den Launcher oder per Kommandozeilenparameter.

### Option A: DayZ-Launcher

1. Oeffnen Sie den **DayZ-Launcher** aus Steam
2. Gehen Sie zum **Mods**-Tab
3. Klicken Sie auf **Add local mod** (oder "Mod aus lokalem Speicher hinzufuegen")
4. Navigieren Sie zu `P:\@MyFirstMod\`
5. Aktivieren Sie die Mod durch Ankreuzen ihres Kontrollkaestchens
6. Klicken Sie auf **Play** (stellen Sie sicher, dass Sie sich mit einem lokalen/Offline-Server verbinden oder Einzelspieler starten)

### Option B: Kommandozeile (empfohlen fuer die Entwicklung)

Fuer schnellere Iterationen starten Sie DayZ direkt mit Kommandozeilenparametern. Erstellen Sie eine Verknuepfung oder Batch-Datei:

**Mit der Diagnose-Executable (mit File Patching, kein PBO noetig):**

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -mod=P:\MyFirstMod -filePatching -server -config=serverDZ.cfg -port=2302
```

**Mit dem gepackten PBO:**

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -mod=P:\@MyFirstMod -server -config=serverDZ.cfg -port=2302
```

Das `-server`-Flag startet einen lokalen Listen-Server. Das `-filePatching`-Flag erlaubt das Laden von Skripten aus ungepackten Ordnern.

### Schnelltest: Offline-Modus

Der schnellste Weg zum Testen ist, DayZ im Offline-Modus zu starten:

```batch
DayZDiag_x64.exe -mod=P:\MyFirstMod -filePatching
```

Klicken Sie dann im Hauptmenue auf **Play** und waehlen Sie **Offline-Modus** (oder **Community Offline**). Dies startet eine lokale Einzelspieler-Sitzung ohne einen Server zu benoetigen.

---

## Schritt 9: Im Script-Log ueberpruefen

Nach dem Starten von DayZ mit Ihrer Mod schreibt die Engine alle `Print()`-Ausgaben in Logdateien.

### Die Logdateien finden

DayZ speichert Logs in Ihrem lokalen AppData-Verzeichnis:

```
C:\Users\<IhrWindowsBenutzername>\AppData\Local\DayZ\
```

Um schnell dorthin zu gelangen:
1. Druecken Sie **Win + R** um den Ausfuehren-Dialog zu oeffnen
2. Geben Sie `%localappdata%\DayZ` ein und druecken Sie Enter

Suchen Sie nach der neuesten Datei mit dem Namen:

```
script_<datum>_<zeit>.log
```

Zum Beispiel: `script_2025-01-15_14-30-22.log`

### Wonach suchen

Oeffnen Sie die Logdatei in Ihrem Texteditor und suchen Sie nach `[MyFirstMod]`. Sie sollten eine dieser Nachrichten sehen:

```
[MyFirstMod] Hello World! The SERVER mission has started.
```

oder (wenn Sie als Client geladen haben):

```
[MyFirstMod] Hello World! The CLIENT mission has started.
```

**Wenn Sie Ihre Nachricht sehen: Glueckwunsch.** Ihre erste DayZ-Mod funktioniert. Sie haben erfolgreich:

1. Eine Mod-Verzeichnisstruktur erstellt
2. Eine Config geschrieben, die die Engine liest
3. Sich mit `modded class` in Vanilla-Spielcode eingeklinkt
4. Ausgaben ins Script-Log geschrieben

### Was, wenn Sie Fehler sehen?

Wenn das Log Zeilen enthaelt, die mit `SCRIPT (E):` beginnen, ist etwas schiefgelaufen. Lesen Sie den naechsten Abschnitt.

---

## Schritt 10: Haeufige Probleme beheben

### Problem: Keine Log-Ausgabe (Mod scheint nicht zu laden)

**Pruefen Sie Ihre Startparameter.** Der `-mod=`-Pfad muss auf den korrekten Ordner zeigen. Bei Verwendung von File Patching stellen Sie sicher, dass der Pfad auf den Ordner zeigt, der `Scripts/config.cpp` direkt enthaelt (nicht den `@`-Ordner).

**Pruefen Sie, ob config.cpp auf der richtigen Ebene existiert.** Sie muss sich unter `Scripts/config.cpp` innerhalb Ihres Mod-Stammverzeichnisses befinden. Wenn sie im falschen Ordner ist, ignoriert die Engine Ihre Mod stillschweigend.

**Pruefen Sie den CfgPatches-Klassennamen.** Wenn es keinen `CfgPatches`-Block gibt oder dessen Syntax falsch ist, wird das gesamte PBO uebersprungen.

**Schauen Sie ins Haupt-DayZ-Log** (nicht nur das Script-Log). Pruefen Sie:
```
C:\Users\<IhrName>\AppData\Local\DayZ\DayZ_<datum>_<zeit>.RPT
```
Suchen Sie nach Ihrem Mod-Namen. Sie koennten Nachrichten sehen wie "Addon MyFirstMod_Scripts requires addon DZ_Data which is not loaded."

### Problem: `SCRIPT (E): Undefined variable` oder `Undefined type`

Dies bedeutet, dass Ihr Code etwas referenziert, das die Engine nicht erkennt. Haeufige Ursachen:

- **Tippfehler in einem Klassennamen.** `MisionServer` statt `MissionServer` (beachten Sie das doppelte 's').
- **Falsche Skriptschicht.** Wenn Sie `PlayerBase` aus `5_Mission` referenzieren, sollte es funktionieren. Aber wenn Sie Ihre Datei versehentlich in `3_Game` platziert haben und Missions-Typen referenzieren, erhalten Sie diesen Fehler.
- **Fehlender `super.OnInit()`-Aufruf.** Das Weglassen kann kaskadierende Fehler verursachen.

### Problem: `SCRIPT (E): Member not found`

Die Methode, die Sie aufrufen, existiert nicht auf der Klasse. Ueberpruefen Sie den Methodennamen und stellen Sie sicher, dass Sie eine echte Vanilla-Methode ueberschreiben. `OnInit` existiert auf `MissionServer` und `MissionGameplay` -- aber nicht auf jeder Klasse.

### Problem: Mod laedt, aber Skript wird nie ausgefuehrt

- **Dateierweiterung:** Stellen Sie sicher, dass Ihre Skriptdatei mit `.c` endet (nicht `.c.txt` oder `.cs`). Windows kann Erweiterungen standardmaessig verbergen.
- **Skriptpfad-Nichtuebereneinstimmung:** Der `files[]`-Pfad in `config.cpp` muss mit Ihrem tatsaechlichen Verzeichnis uebereinstimmen. `"MyFirstMod/Scripts/5_Mission"` bedeutet, dass die Engine nach einem Ordner an genau diesem Pfad relativ zum Mod-Stammverzeichnis sucht.
- **Klassenname:** `modded class MissionServer` ist gross-/kleinschreibungssensitiv. Es muss exakt mit dem Vanilla-Klassennamen uebereinstimmen.

### Problem: PBO-Packfehler

- Stellen Sie sicher, dass `config.cpp` auf der Stammebene dessen ist, was Sie packen (der `Scripts/`-Ordner).
- Pruefen Sie, ob das Praefix im Addon Builder mit Ihrem Mod-Pfad uebereinstimmt.
- Stellen Sie sicher, dass keine Nicht-Text-Dateien in den Scripts-Ordner gemischt sind (keine `.exe`, `.dll` oder Binaerdateien).

### Problem: Spiel stuerzt beim Start ab

- Pruefen Sie auf Syntaxfehler in `config.cpp`. Ein fehlendes Semikolon, eine fehlende Klammer oder ein fehlendes Anfuehrungszeichen kann den Config-Parser zum Absturz bringen.
- Ueberpruefen Sie, ob `requiredAddons` gueltige Addon-Namen auflistet. Ein falsch geschriebener Addon-Name verursacht einen harten Fehler.
- Entfernen Sie Ihre Mod aus den Startparametern und bestaetigen Sie, dass das Spiel ohne sie startet. Fuegen Sie sie dann wieder hinzu, um das Problem zu isolieren.

---

## Vollstaendige Dateireferenz

Hier sind alle drei Dateien in ihrer vollstaendigen Form zum einfachen Kopieren:

### Datei 1: `MyFirstMod/mod.cpp`

```cpp
name = "My First Mod";
author = "IhrName";
version = "1.0";
overview = "My very first DayZ mod. Prints Hello World to the script log.";
```

### Datei 2: `MyFirstMod/Scripts/config.cpp`

```cpp
class CfgPatches
{
    class MyFirstMod_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data"
        };
    };
};

class CfgMods
{
    class MyFirstMod
    {
        dir = "MyFirstMod";
        name = "My First Mod";
        author = "IhrName";
        type = "mod";

        dependencies[] = { "Mission" };

        class defs
        {
            class missionScriptModule
            {
                value = "";
                files[] = { "MyFirstMod/Scripts/5_Mission" };
            };
        };
    };
};
```

### Datei 3: `MyFirstMod/Scripts/5_Mission/MyFirstMod/MissionHello.c`

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The SERVER mission has started.");
    }
};

modded class MissionGameplay
{
    override void OnInit()
    {
        super.OnInit();
        Print("[MyFirstMod] Hello World! The CLIENT mission has started.");
    }
};
```

---

## Naechste Schritte

Jetzt, da Sie eine funktionierende Mod haben, hier die natuerlichen Weiterentwicklungen:

1. **[Kapitel 8.2: Ein eigenes Item erstellen](02-custom-item.md)** -- Definieren Sie ein neues Ingame-Item mit Texturen und Spawning.
2. **Weitere Skriptschichten hinzufuegen** -- Erstellen Sie `3_Game`- und `4_World`-Ordner, um Konfiguration, Datenklassen und Entitaetslogik zu organisieren. Siehe [Kapitel 2.1: Die 5-Schichten-Skript-Hierarchie](../02-mod-structure/01-five-layers.md).
3. **Tastenbelegungen hinzufuegen** -- Erstellen Sie eine `Inputs.xml`-Datei und registrieren Sie eigene Tastenaktionen.
4. **UI erstellen** -- Bauen Sie Ingame-Panels mit Layout-Dateien und `ScriptedWidgetEventHandler`. Siehe [Kapitel 3: GUI-System](../03-gui-system/01-widget-types.md).
5. **Ein Framework verwenden** -- Integrieren Sie Community Framework (CF) oder MyFramework fuer erweiterte Features wie RPC, Config-Management und Admin-Panels.

---

**Weiter:** [Kapitel 8.2: Ein eigenes Item erstellen](02-custom-item.md)
