# Kapitel 8.6: Debugging & Testen Ihrer Mod

[Startseite](../../README.md) | [<< Zurueck: Die DayZ-Mod-Vorlage verwenden](05-mod-template.md) | **Debugging & Testen** | [Weiter: Im Steam Workshop veroeffentlichen >>](07-publishing-workshop.md)

---

## Inhaltsverzeichnis

- [Einfuehrung](#einfuehrung)
- [Das Script-Log -- Ihr bester Freund](#das-script-log----ihr-bester-freund)
- [Print-Debugging (die zuverlaessige Methode)](#print-debugging-die-zuverlaessige-methode)
- [DayZDiag -- Die Debug-Executable](#dayzdiag----die-debug-executable)
- [File Patching -- Bearbeiten ohne Neuerstellen](#file-patching----bearbeiten-ohne-neuerstellen)
- [Workbench -- Skripteditor und Debugger](#workbench----skripteditor-und-debugger)
- [Haeufige Fehlermuster und Loesungen](#haeufige-fehlermuster-und-loesungen)
- [Test-Workflow](#test-workflow)
- [Ingame-Debug-Tools](#ingame-debug-tools)
- [Pre-Release-Checkliste](#pre-release-checkliste)
- [Haeufige Fehler](#haeufige-fehler)
- [Naechste Schritte](#naechste-schritte)

---

## Einfuehrung

Anders als Unity oder Unreal unterstuetzt die Retail-DayZ-Executable kein Anfuegen eines Debuggers an Enforce Script. Stattdessen verlassen Sie sich auf fuenf Werkzeuge:

1. **Script-Logs** -- Textdateien, die jeden Fehler, jede Warnung und Print-Ausgabe erfassen
2. **Print-Anweisungen** -- Ausfuehrungsfluss verfolgen und Variablenwerte inspizieren
3. **DayZDiag** -- Diagnose-Build mit erweiterter Fehlerberichterstattung und Debug-Tools
4. **File Patching** -- Skripte bearbeiten, ohne jedes Mal Ihr PBO neu zu erstellen
5. **Workbench** -- Offizieller Skripteditor mit Syntaxpruefung und einer Skriptkonsole

Zusammen bilden sie ein leistungsstarkes Toolkit. Dieses Kapitel lehrt Sie, wie Sie jedes einzelne verwenden.

---

## Das Script-Log -- Ihr bester Freund

Jedes Mal, wenn DayZ laeuft, schreibt es eine Script-Logdatei. Diese Datei erfasst jeden Skriptfehler, jede Warnung und Print()-Ausgabe. Wenn etwas schiefgeht, ist das Script-Log der erste Ort zum Nachschauen.

### Wo Sie Script-Logs finden

**Client-Logs:** `%LocalAppData%\DayZ\` (druecken Sie `Win+R`, einfuegen, Enter)

**Server-Logs:** Im Profilordner Ihres Servers (gesetzt via `-profiles=serverprofile`)

Dateien heissen `script_YYYY-MM-DD_HH-MM-SS.log` -- der neueste Zeitstempel ist Ihre letzte Sitzung.

### Wonach Sie suchen

Script-Logs enthalten Tausende von Zeilen. Sie muessen wissen, wonach Sie suchen.

**Fehler** sind mit `SCRIPT (E)` markiert:

```
SCRIPT (E): MyMod/Scripts/4_World/MyManager.c :: OnInit -- Null pointer access
```

Dies ist ein harter Fehler. Ihr Code hat versucht, etwas Ungueltiges zu tun, und DayZ hat die Ausfuehrung dieses Codepfads gestoppt. Diese muessen behoben werden.

**Warnungen** sind mit `SCRIPT (W)` markiert:

```
SCRIPT (W): MyMod/Scripts/4_World/MyManager.c :: Load -- Cannot open file "$profile:MyMod/config.json"
```

Warnungen bringen Ihren Code nicht zum Absturz, aber sie deuten oft auf ein Problem hin, das spaeter Probleme verursachen wird. Ignorieren Sie sie nicht.

**Print-Ausgaben** erscheinen als Klartext ohne Praefix:

```
[MyMod] Manager initialized with 5 items
```

Dies ist die Ausgabe Ihrer eigenen `Print()`-Aufrufe. Es ist die primaere Methode, mit der Sie verfolgen, was Ihr Code tut.

### Effizient suchen

Script-Logs koennen Zehntausende Zeilen umfassen. Lesen Sie nie Zeile fuer Zeile -- suchen Sie nach Ihrem Mod-Praefix oder Fehlermarkierungen:

```powershell
# PowerShell -- alle Fehler im neuesten Log finden
Select-String -Path "$env:LOCALAPPDATA\DayZ\script*.log" -Pattern "SCRIPT \(E\)" | Select-Object -Last 20

# PowerShell -- alle Zeilen von Ihrer Mod finden
Select-String -Path "$env:LOCALAPPDATA\DayZ\script*.log" -Pattern "MyMod" | Select-Object -Last 30
```

```cmd
:: Eingabeaufforderung-Alternative
findstr "SCRIPT (E)" "%LocalAppData%\DayZ\script_2026-03-21_14-30-05.log"
```

### Haeufige Log-Eintraege verstehen

| Log-Eintrag | Bedeutung |
|-----------|---------|
| `SCRIPT (E): Cannot convert string to int` | Typkonflikt -- falschen Typ uebergeben oder zugewiesen |
| `SCRIPT (E): Null pointer access in ... :: Update` | Methode auf einem NULL-Objekt aufgerufen (haeufigster Fehler) |
| `SCRIPT (E): Undefined variable 'manger'` | Tippfehler in einem Variablennamen oder falscher Scope |
| `SCRIPT (E): Method 'GetHelth' not found in class 'EntityAI'` | Methode existiert nicht -- Schreibweise und Elternklasse pruefen |

### Echtzeit-Log-Ueberwachung

Beobachten Sie das Log live in einem separaten PowerShell-Fenster, waehrend DayZ laeuft:

```powershell
# Das neueste Script-Log in Echtzeit verfolgen
Get-ChildItem "$env:LOCALAPPDATA\DayZ\script*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object {
    Get-Content $_.FullName -Wait -Tail 50
}
```

Filtern, um nur Fehler und Ihre Mod-Ausgabe anzuzeigen:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\DayZ\script*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object {
    Get-Content $_.FullName -Wait -Tail 50 | Where-Object { $_ -match "SCRIPT \(E\)|SCRIPT \(W\)|\[MyMod\]" }
}
```

---

## Print-Debugging (die zuverlaessige Methode)

Wenn Sie wissen muessen, was Ihr Code zur Laufzeit tut, ist `Print()` Ihr primaeres Werkzeug. Es schreibt eine Zeile ins Script-Log, die Sie danach lesen oder in Echtzeit beobachten koennen.

### Grundlegende Print-Verwendung

```c
class MyManager
{
    void Init()
    {
        Print("[MyMod] MyManager.Init() aufgerufen");

        int count = LoadItems();
        Print("[MyMod] " + count.ToString() + " Items geladen");
    }
}
```

Dies erzeugt Zeilen im Script-Log wie:

```
[MyMod] MyManager.Init() aufgerufen
[MyMod] 5 Items geladen
```

### Formatierte Ausgabe

Verwenden Sie String-Verkettung, um informative Nachrichten mit genug Kontext aufzubauen, um fuer sich allein nuetzlich zu sein:

```c
void ProcessPlayer(PlayerBase player)
{
    if (!player)
    {
        Print("[MyMod] ProcessPlayer: player ist NULL, Abbruch");
        return;
    }

    string name = player.GetIdentity().GetName();
    vector pos = player.GetPosition();
    Print("[MyMod] Verarbeite: " + name + " bei " + pos.ToString());
}
```

### Einen Debug-Logger erstellen

Statt rohe `Print()`-Aufrufe zu verstreuen, erstellen Sie einen umschaltbaren Logger:

```c
class MyModDebug
{
    static bool s_Enabled = true;

    static void Log(string msg)
    {
        if (s_Enabled)
            Print("[MyMod:DEBUG] " + msg);
    }

    static void Error(string msg)
    {
        // Fehler werden immer ausgegeben, unabhaengig vom Debug-Flag
        Print("[MyMod:ERROR] " + msg);
    }
}
```

Verwenden Sie ihn in Ihrem gesamten Code: `MyModDebug.Log("Spieler verbunden: " + name);`

### Praeprozessor-Defines fuer Debug-Only-Code verwenden

Enforce Script unterstuetzt `#ifdef`, um Code nur in Entwicklungs-Builds einzuschliessen:

```c
void Update()
{
    #ifdef DEVELOPER
    Print("[MyMod] Update-Tick, aktive Items: " + m_Items.Count().ToString());
    #endif

    // Normaler Code hier...
}
```

`DEVELOPER` ist in DayZDiag und Workbench gesetzt, aber nicht im Retail-DayZ. `DIAG_DEVELOPER` ist ein weiteres nuetzliches Define, das nur in Diagnose-Builds verfuegbar ist. Code innerhalb dieser Guards hat null Kosten in Release-Builds.

### Debug-Prints vor Release entfernen

Wenn Sie keine `#ifdef`-Guards verwenden, entfernen Sie alle `Print()`-Aufrufe vor der Veroeffentlichung. Uebermassige Ausgabe blaest Logs auf, schadet der Server-Leistung und kann interne Informationen preisgeben. Ein konsistentes Praefix wie `[MyMod:DEBUG]` macht sie leicht zu finden und zu entfernen.

---

## DayZDiag -- Die Debug-Executable

DayZDiag ist ein spezieller Diagnose-Build von DayZ mit Features, die die Retail-Version nicht hat.

### Was DayZDiag anders macht

| Feature | Retail DayZ | DayZDiag |
|---------|-------------|----------|
| File-Patching-Unterstuetzung | Nein | Ja |
| `DEVELOPER`-Define aktiv | Nein | Ja |
| `DIAG_DEVELOPER`-Define aktiv | Nein | Ja |
| Zusaetzliche Fehlerdetails in Logs | Grundlegend | Ausfuehrlich |
| Admin-Konsole-Zugang | Nein | Ja |
| Skriptkonsole | Nein | Ja |
| Freie Kamera | Nein | Ja |

### DayZDiag erhalten

DayZDiag ist in DayZ Tools enthalten (kein separater Download). Nach der Installation von DayZ Tools aus Steam finden Sie `DayZDiag_x64.exe` unter:

```
C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\
```

### Startparameter

Erstellen Sie eine Batch-Datei oder Verknuepfung mit diesen Parametern:

**Client (Einzelspieler mit Server):**

```batch
DayZDiag_x64.exe -filePatching -mod=P:\MyMod -profiles=clientprofile -server -port=2302
```

**Client (mit separatem Server verbinden):**

```batch
DayZDiag_x64.exe -filePatching -mod=P:\MyMod -connect=127.0.0.1 -port=2302
```

**Dedizierter Server:**

```batch
DayZDiag_x64.exe -filePatching -server -mod=P:\MyMod -config=serverDZ.cfg -port=2302 -profiles=serverprofile
```

Wichtige Parameter:

| Parameter | Zweck |
|-----------|---------|
| `-filePatching` | Laden loser Dateien vom P:-Laufwerk aktivieren (siehe naechster Abschnitt) |
| `-mod=P:\MyMod` | Ihre Mod vom P:-Laufwerk laden |
| `-profiles=ordner` | Profilordner fuer Logs und Configs setzen |
| `-server` | Als lokalen Listen-Server laufen lassen (Einzelspieler-Tests) |
| `-connect=IP` | Mit einem Server an der angegebenen IP verbinden |
| `-port=PORT` | Netzwerkport setzen (Standard 2302) |

### Wann DayZDiag vs. Retail verwenden

- **Waehrend der Entwicklung:** Verwenden Sie immer DayZDiag. Es gibt Ihnen File Patching, bessere Fehler und Debug-Tools.
- **Vor der Veroeffentlichung:** Testen Sie mit der Retail-DayZ-Executable, um sicherzustellen, dass alles fuer Spieler funktioniert. Einige Verhaltensweisen unterscheiden sich zwischen DayZDiag und Retail (zum Beispiel laeuft `#ifdef DEVELOPER`-Code nicht im Retail).

---

## File Patching -- Bearbeiten ohne Neuerstellen

File Patching ist die groesste Zeitersparnis im DayZ-Modding. Ohne es erfordert jede Skriptaenderung: Datei bearbeiten, PBO neu erstellen, PBO kopieren, DayZ neustarten. Mit File Patching koennen Sie: Datei bearbeiten, Mission neustarten. Das ist alles.

### Wie es funktioniert

Wenn DayZ mit dem `-filePatching`-Parameter gestartet wird, prueft es das P:-Laufwerk auf lose Dateien, bevor es Dateien aus PBOs laedt. Wenn es eine Datei auf P: findet, die einer Datei in einem PBO entspricht, hat die lose Datei Vorrang.

Das bedeutet:

1. Ihre Mod ist auf dem P:-Laufwerk eingerichtet (via `SetupWorkdrive.bat` oder manueller Junction)
2. Sie starten DayZDiag mit `-filePatching -mod=P:\MyMod`
3. DayZ laedt Ihre Skripte direkt vom P:-Laufwerk -- nicht aus dem PBO
4. Sie bearbeiten eine `.c`-Datei auf dem P:-Laufwerk und speichern sie
5. Sie verbinden sich neu oder starten die Mission im Spiel neu
6. DayZ nimmt Ihre geaenderte Datei sofort auf

Kein PBO-Neubau noetig. Der Bearbeitungs-Test-Zyklus sinkt von Minuten auf Sekunden.

### File Patching einrichten

1. Stellen Sie sicher, dass Ihr Mod-Quellcode auf dem P:-Laufwerk liegt (aus [Kapitel 8.1](01-first-mod.md))
2. Starten Sie: `DayZDiag_x64.exe -filePatching -mod=P:\MyMod -server -port=2302`
3. Bearbeiten Sie eine `.c`-Datei, speichern Sie, verbinden Sie sich im Spiel neu -- Ihre Aenderungen sind live

### Was mit File Patching funktioniert

| Dateityp | File Patching funktioniert? |
|-----------|---------------------|
| Skriptdateien (`.c`) | Ja |
| Layout-Dateien (`.layout`) | Ja |
| Texturen (`.edds`, `.paa`) | Ja |
| Sounddateien | Ja |
| `config.cpp` | **Nein** -- PBO-Neubau erforderlich |
| `mod.cpp` | **Nein** -- PBO-Neubau erforderlich |
| Neue Dateien (nicht im PBO) | **Nein** -- PBO-Neubau erforderlich, um sie zu registrieren |

Die wichtigste Einschraenkung: `config.cpp`-Aenderungen erfordern immer einen PBO-Neubau. Dazu gehoert das Hinzufuegen neuer Klassen, Aendern von `requiredAddons` oder Modifizieren von `CfgMods`. Wenn Sie eine brandneue `.c`-Datei hinzufuegen, benoetigen Sie ebenfalls einen PBO-Neubau, damit das Skript-Laden der `config.cpp` die neue Datei kennt.

### Der File-Patching-Workflow

Hier ist der ideale Entwicklungszyklus:

```
1. Ihr PBO einmal erstellen (um die Dateiliste in config.cpp festzulegen)
2. DayZDiag mit -filePatching -mod=P:\MyMod starten
3. Eine .c-Datei auf dem P:-Laufwerk bearbeiten
4. Die Datei speichern
5. Im Spiel: trennen und neu verbinden (oder Mission neustarten)
6. Das Script-Log auf Ihre Aenderungen pruefen
7. Ab Schritt 3 wiederholen
```

Diese Schleife kann unter 30 Sekunden pro Iteration dauern, verglichen mit mehreren Minuten beim PBO-Neubau jedes Mal.

---

## Workbench -- Skripteditor und Debugger

Workbench ist die offizielle DayZ-Entwicklungsumgebung, die in DayZ Tools enthalten ist.

### Starten und einrichten

1. Oeffnen Sie **DayZ Tools** aus Steam, klicken Sie auf **Workbench**
2. Gehen Sie zu **File > Open Project** und zeigen Sie auf das Skriptverzeichnis Ihrer Mod auf dem P:-Laufwerk
3. Workbench indiziert Ihre `.c`-Dateien und bietet Syntaxerkennung

### Wichtige Features

- **Syntaxhervorhebung** -- Schluesselwoerter, Typen, Strings und Kommentare sind farblich markiert
- **Code-Vervollstaendigung** -- Tippen Sie einen Klassennamen gefolgt von einem Punkt, um verfuegbare Methoden zu sehen
- **Fehlerhervorhebung** -- Syntaxfehler werden rot unterstrichen, bevor Sie etwas ausfuehren
- **Skriptkonsole** -- Enforce-Script-Befehle live ausfuehren:

```c
// Die Position des Spielers ausgeben
Print(GetGame().GetPlayer().GetPosition().ToString());

// Ein Item an Ihrer Position spawnen
GetGame().GetPlayer().SpawnEntityOnGroundPos("AKM", GetGame().GetPlayer().GetPosition());
```

### Einschraenkungen

- **Keine vollstaendige Spielumgebung:** Einige APIs funktionieren nur im eigentlichen Spiel, nicht in Workbenchs Simulation
- **Getrennt von der Spiel-Laufzeit:** Sie muessen Dateien immer noch speichern und die Mission neustarten, um Aenderungen im Spiel zu sehen
- **Unvollstaendiger Mod-Kontext:** Cross-Mod-Referenzen koennen als Fehler angezeigt werden, auch wenn sie im Spiel funktionieren

---

## Haeufige Fehlermuster und Loesungen

Referenztabellen der haeufigsten Fehler und wie sie zu beheben sind. Setzen Sie ein Lesezeichen fuer diesen Abschnitt.

### Skriptfehler

| Fehlermeldung | Ursache | Loesung |
|---------------|-------|-----|
| `Null pointer access` | Methode auf einer NULL-Variable aufgerufen | Null-Pruefung vor Verwendung hinzufuegen: `if (obj) { obj.DoThing(); }` |
| `Cannot convert X to Y` | Typkonflikt bei Zuweisung oder Funktionsaufruf | Erwarteten Typ pruefen. `Class.CastTo()` fuer sicheres Casting verwenden. |
| `Undefined variable 'xyz'` | Tippfehler im Variablennamen oder falscher Scope | Schreibweise pruefen. Sicherstellen, dass die Variable im aktuellen Scope deklariert ist. |
| `Method 'xyz' not found in class 'Abc'` | Methode existiert nicht auf dieser Klasse | Klassenhierarchie pruefen. Den korrekten Methodennamen in der API nachschlagen. |
| `Division by zero` | Division durch eine Variable die gleich 0 ist | Guard hinzufuegen: `if (divisor != 0) { result = value / divisor; }` |
| `Stack overflow` | Endlose Rekursion in Ihrem Code | Methoden pruefen, die sich selbst ohne korrekte Abbruchbedingung aufrufen. |
| `Type 'MyClass' not found` | Die Datei, die MyClass definiert, wird nicht geladen oder befindet sich in einer hoeheren Skriptschicht | config.cpp Skript-Ladereihenfolge pruefen. Untere Schichten koennen obere nicht sehen. |

### Config-Fehler

| Fehlermeldung | Ursache | Loesung |
|---------------|-------|-----|
| `Config parse error` | Fehlendes Semikolon, fehlende Klammer oder fehlendes Anfuehrungszeichen in config.cpp | config.cpp-Syntax sorgfaeltig pruefen. Jede Eigenschaft braucht ein Semikolon. Jede Klasse braucht oeffnende und schliessende Klammern. |
| `Addon 'X' requires addon 'Y'` | Fehlende Abhaengigkeit in requiredAddons | Das benoetigte Addon zum `requiredAddons[]`-Array hinzufuegen. |
| `Cannot find mod` | Mod-Ordnername oder -pfad ist falsch | Ueberpruefen, dass der `-mod=`-Parameter exakt mit Ihrem Mod-Ordnernamen uebereinstimmt. |

### Mod-Ladefehler

| Symptom | Ursache | Loesung |
|---------|-------|-----|
| Mod erscheint nicht im Launcher | Fehlende oder ungueltige `mod.cpp` | Pruefen, dass `mod.cpp` im Mod-Stamm existiert und gueltige `name`- und `dir`-Felder hat. |
| Skripte werden nicht ausgefuehrt | config.cpp registriert Skripte nicht | Ueberpruefen, dass die `CfgMods`-Klasse in config.cpp den korrekten Skriptpfad hat. |
| Mod laedt, aber Features fehlen | Skriptschicht-Problem | Ueberpruefen, dass Dateien in den korrekten Schichtordnern sind (3_Game, 4_World, 5_Mission). |

### Laufzeitprobleme

| Symptom | Ursache | Loesung |
|---------|-------|-----|
| RPC wird auf dem Server nicht empfangen | Falsche RPC-Registrierung oder Identitaets-Nichtueberereinstimmung | Pruefen, dass RPC sowohl auf Client als auch Server registriert ist. RPC-ID-Uebereinstimmung ueberpruefen. |
| RPC wird auf dem Client nicht empfangen | Server sendet nicht, oder Client nicht registriert | Print() auf Serverseite hinzufuegen, um Senden zu bestaetigen. Client-Registrierungscode pruefen. |
| UI wird nicht angezeigt | Layout-Pfad falsch oder Eltern-Widget ist null | Ueberpruefen, dass der `.layout`-Dateipfad relativ zur Mod korrekt ist. Pruefen, dass das Eltern-Widget existiert. |
| JSON-Config laedt nicht | Dateipfad falsch oder JSON-Syntaxfehler | Dateipfad pruefen. JSON-Syntax validieren (keine nachgestellten Kommas, korrekte Anfuehrungszeichen). |
| Spielerdaten werden nicht gespeichert | Profilordner-Berechtigungen oder Pfadproblem | Pruefen, dass der `$profile:`-Pfad zugaenglich ist und der Ordner existiert. |

### Null-Pointer und sicheres Casting -- detaillierte Beispiele

Diese beiden Fehler sind so haeufig, dass sie ausfuehrliche Beispiele verdienen.

**Unsicherer Code (stuerzt ab wenn GetPlayer() oder GetIdentity() NULL zurueckgibt):**

```c
void DoSomething()
{
    PlayerBase player = PlayerBase.Cast(GetGame().GetPlayer());
    string name = player.GetIdentity().GetName();  // Absturz wenn player oder identity NULL ist
}
```

**Sicherer Code (jeden potenziellen Null absichern):**

```c
void DoSomething()
{
    Man man = GetGame().GetPlayer();
    if (!man)
        return;

    PlayerBase player;
    if (!Class.CastTo(player, man))
        return;

    PlayerIdentity identity = player.GetIdentity();
    if (!identity)
        return;

    Print("[MyMod] Spieler: " + identity.GetName());
}
```

**Sicheres Casting-Muster mit `Class.CastTo()`:**

```c
void ProcessEntity(Object obj)
{
    ItemBase item;
    if (Class.CastTo(item, obj))
    {
        item.SetQuantity(1);
    }
    else
    {
        Print("[MyMod] Objekt ist kein ItemBase: " + obj.GetType());
    }
}
```

`Class.CastTo()` gibt `true` bei Erfolg zurueck, `false` bei Misserfolg. Pruefen Sie immer den Rueckgabewert.

---

## Test-Workflow

DayZ-Modding hat kein automatisiertes Testframework. Testen ist manuell: erstellen, starten, spielen, beobachten, Logs pruefen. Ein effizienter Workflow ist entscheidend.

### Der grundlegende Testzyklus

```
Code bearbeiten --> PBO erstellen --> DayZ starten --> Im Spiel testen --> Log pruefen --> Beheben --> Wiederholen
```

Mit File Patching ueberspringen Sie den PBO-Bau: `.c` auf dem P:-Laufwerk bearbeiten, neu verbinden, Log pruefen. Dies reduziert die Iteration von Minuten auf Sekunden.

### Server-Mods testen

Wenn Ihre Mod serverseitige Logik hat, benoetigen Sie einen lokalen dedizierten Server.

**Option 1: Listen-Server (am einfachsten)**

Starten Sie DayZDiag mit `-server`, um Client und Server in einem einzelnen Prozess auszufuehren:

```batch
DayZDiag_x64.exe -filePatching -mod=P:\MyMod -server -port=2302
```

Dies ist der schnellste Weg zum Testen, repliziert aber keine dedizierte Serverumgebung perfekt.

**Option 2: Lokaler dedizierter Server (am genauesten)**

Fuehren Sie einen separaten DayZDiag-Serverprozess aus und verbinden Sie sich dann mit einem DayZDiag-Client:

Server:
```batch
DayZDiag_x64.exe -filePatching -server -mod=P:\MyMod -config=serverDZ.cfg -port=2302 -profiles=serverprofile
```

Client:
```batch
DayZDiag_x64.exe -filePatching -mod=P:\MyMod -connect=127.0.0.1 -port=2302
```

Dies gibt Ihnen separate Client- und Server-Logs, was fuer das Debugging von RPC-Kommunikation und Client-Server-Split-Logik wesentlich ist.

### Client-Only- und Multiplayer-Tests

Fuer reine Client-Mods (UI, HUD) reicht ein Listen-Server aus: fuegen Sie `-server` zu Ihren Startparametern hinzu.

Fuer Multiplayer-Tests haben Sie drei Optionen:
- **Zwei Instanzen auf einem Rechner:** DayZDiag-Server + zwei Clients mit verschiedenen `-profiles`-Ordnern ausfuehren
- **Mit einem Freund testen:** DayZDiag-Server hosten, Firewall-Port 2302 oeffnen
- **Cloud-Server:** Einen entfernten dedizierten Server einrichten

### Build-Skripte verwenden

Wenn Ihr Projekt ein Build-Skript hat (wie `dev.py`), verwenden Sie es, um den Zyklus zu automatisieren:

```bash
python dev.py build     # Alle PBOs erstellen
python dev.py server    # Erstellen + Server starten + Logs ueberwachen
python dev.py client    # Client starten (verbindet sich mit localhost:2302)
python dev.py full      # Erstellen + Server + Ueberwachen + Client automatisch starten
python dev.py check     # Neuestes Script-Log auf Fehler pruefen (offline)
python dev.py watch     # Echtzeit-Log-Verfolgung, gefiltert fuer Fehler und Mod-Ausgabe
python dev.py kill      # DayZ-Prozesse fuer Neustart beenden
```

Der `watch`-Befehl ist besonders wertvoll -- er filtert das Live-Log, um nur relevante Ausgaben anzuzeigen.

---

## Ingame-Debug-Tools

DayZDiag bietet mehrere Ingame-Tools zum Testen. Diese sind in Retail-Builds nicht verfuegbar.

### Skriptkonsole

Oeffnen Sie mit der Akzent-Taste (`` ` ``) oder pruefen Sie Ihre Tastenbelegungen fuer "Script Console". Fuehren Sie Enforce-Script-Befehle live aus:

```c
// Ein Item an Ihrer Position spawnen
GetGame().GetPlayer().SpawnEntityOnGroundPos("AKM", GetGame().GetPlayer().GetPosition());

// Zu Koordinaten teleportieren
GetGame().GetPlayer().SetPosition("8000 0 10000");

// Ihre aktuelle Position ausgeben
Print(GetGame().GetPlayer().GetPosition().ToString());
```

### Freie Kamera

Umschaltbar ueber das Admin-Tools-Menue. Fliegen Sie losgeloest von Ihrem Charakter herum, um gespawnte Objekte zu inspizieren, Platzierung zu pruefen oder KI-Verhalten zu beobachten.

### Objekt-Spawning

```c
// Einen Zombie spawnen
GetGame().CreateObjectEx("ZmbM_HermitSkinny_Base", "8000 0 10000", ECE_PLACE_ON_SURFACE);

// Ein Fahrzeug spawnen
GetGame().CreateObjectEx("OffroadHatchback", "8000 0 10000", ECE_PLACE_ON_SURFACE);
```

### Zeit- und Wetter-Manipulation

```c
// Auf Mittag / Mitternacht setzen
GetGame().GetWorld().SetDate(2026, 6, 15, 12, 0);
GetGame().GetWorld().SetDate(2026, 6, 15, 0, 0);

// Wetter ueberschreiben
Weather weather = GetGame().GetWeather();
weather.GetOvercast().Set(0.8, 0, 0);
weather.GetRain().Set(1.0, 0, 0);
weather.GetFog().Set(0.5, 0, 0);
```

---

## Pre-Release-Checkliste

Bevor Sie im Steam Workshop veroeffentlichen, gehen Sie jeden Punkt durch.

### 1. Alle Debug-Ausgaben entfernen oder absichern

Suchen Sie nach `Print(` und stellen Sie sicher, dass jeder Debug-Print entfernt oder in `#ifdef DEVELOPER` eingewickelt ist.

### 2. Mit einem sauberen Profil testen

Benennen Sie `%LocalAppData%\DayZ\` in `DayZ_backup` um und testen Sie von Grund auf. Dies fangen Annahmen ueber zwischengespeicherte Daten oder bestehende Config-Dateien ab.

### 3. Mod-Ladereihenfolge testen

Testen Sie Ihre Mod geladen vor und nach anderen populaeren Mods. Pruefen Sie auf Klassennamen-Kollisionen, RPC-ID-Konflikte und config.cpp-Ueberschreibungen.

### 4. Auf Speicherlecks pruefen

Beobachten Sie den Serverspeicher ueber die Zeit. Haeufige Leak-Ursachen: Objekte, die in Schleifen ohne Bereinigung erstellt werden, zirkulaere `ref`-Referenzen (eine Seite muss roh sein), Arrays, die ohne Grenzen wachsen.

### 5. Stringtable-Eintraege ueberpruefen

Jeder `#key_name`, der im Code referenziert wird, braucht eine passende Zeile in der `stringtable.csv`. Fehlende Eintraege werden als rohe Schluessel-Strings im Spiel angezeigt.

### 6. Auf einem dedizierten Server testen

Listen-Server-Tests verbergen RPC-Timing-Probleme, Autoritaetsunterschiede und Multi-Client-Sync-Bugs. Fuehren Sie immer einen finalen Test auf einem echten dedizierten Server durch.

### 7. Eine frische Workshop-Installation testen

Abonnement kuendigen, lokalen Mod-Ordner loeschen, neu abonnieren und testen. Dies verifiziert, dass der Workshop-Upload vollstaendig ist.

---

## Haeufige Fehler

Fehler, die jeder DayZ-Modder mindestens einmal macht. Lernen Sie daraus.

### 1. Debug-Prints in Release-Builds lassen

Spieler brauchen kein `[MyMod:DEBUG] Tick count: 14523` in ihren Logs. Wickeln Sie es in `#ifdef DEVELOPER` ein oder entfernen Sie es vollstaendig.

### 2. Nur im Einzelspieler testen

Listen-Server fuehren Client und Server in einem Prozess aus und verbergen RPCs, die nie das Netzwerk kreuzen, Race Conditions, Autoritaetspruefungsunterschiede und Null-Identitaets-Referenzen. Testen Sie mit einem separaten dedizierten Server.

### 3. Nicht mit anderen Mods testen

Ihre Mod kann mit CF, Expansion oder anderen populaeren Mods ueber doppelte RPC-IDs, fehlende `super`-Aufrufe in Overrides oder Config-Klassen-Kollisionen konfligieren. Testen Sie Kombinationen vor der Veroeffentlichung.

### 4. Warnungen ignorieren

`SCRIPT (W)`-Warnungen sagen oft zukuenftige Abstuerze voraus. Eine fehlende-Datei-Warnung heute wird morgen ein Null-Pointer.

### 5. File Patching nicht verwenden

PBOs fuer jede einzelne Zeilenaenderung neu erstellen vergeudet enorm viel Zeit. Richten Sie File Patching einmal ein (siehe [oben](#file-patching----bearbeiten-ohne-neuerstellen)).

### 6. Nicht beide Client- und Server-Logs pruefen

Bei RPC-/Client-Server-Problemen ist der Fehler oft auf einer Seite und das Symptom auf der anderen. Pruefen Sie sowohl `%LocalAppData%\DayZ\` (Client) als auch den Profilordner Ihres Servers.

### 7. config.cpp aendern ohne Neuerstellen

File Patching gilt nicht fuer `config.cpp`. Neue Klassen, `requiredAddons`-Aenderungen und `CfgMods`-Bearbeitungen erfordern immer einen PBO-Neubau.

### 8. Falsche Skriptschicht

Untere Schichten koennen obere nicht sehen. Wenn `3_Game/`-Code `PlayerBase` referenziert (definiert in `4_World/`), schlaegt es fehl:

```
3_Game/   -- Kann nicht auf 4_World- oder 5_Mission-Typen referenzieren
4_World/  -- Kann auf 3_Game referenzieren, nicht auf 5_Mission
5_Mission/-- Kann auf 3_Game und 4_World referenzieren
```

---

## Naechste Schritte

1. **File Patching einrichten**, falls Sie es noch nicht getan haben. Es ist die wirkungsvollste Einzelverbesserung fuer Ihren Entwicklungs-Workflow.
2. **Eine Debug-Logger-Klasse** fuer Ihre Mod mit konsistentem Praefix erstellen, damit Sie Log-Ausgaben leicht filtern koennen.
3. **Das Script-Log lesen ueben.** Oeffnen Sie es nach jeder Testsitzung und suchen Sie nach Fehlern und Warnungen, auch wenn alles zu funktionieren schien. Stille Fehler koennen subtile Bugs verursachen, die spaeter auftauchen.
4. **Workbench erkunden.** Oeffnen Sie die Skripte Ihrer Mod in Workbench und probieren Sie die Skriptkonsole. Es braucht Zeit, sich einzugewoehnen, aber es zahlt sich aus.
5. **Ein Testszenario erstellen.** Erstellen Sie eine gespeicherte Mission oder ein Skript, das eine bestimmte Testumgebung einrichtet (Items spawnt, Tageszeit setzt, zu einem Ort teleportiert), damit Sie Bugs schnell reproduzieren koennen.
6. **[Kapitel 8.1](01-first-mod.md) lesen**, falls Sie Ihre erste Mod noch nicht erstellt haben. Debugging ist viel einfacher, wenn Sie die vollstaendige Mod-Struktur verstehen.

---

## Bewaehrte Methoden

- **Zuerst das Script-Log pruefen, bevor Sie Code aendern.** Die meisten Bugs haben eine klare Fehlermeldung im Log. Code zu aendern, ohne das Log zu lesen, fuehrt zu blindem Raten und neuen Bugs.
- **`#ifdef DEVELOPER`-Guards fuer alle Debug-Prints verwenden.** Dies stellt null Leistungskosten in Retail-Builds sicher und verhindert Log-Spam fuer Spieler. Reservieren Sie ungesicherte `Print()`-Aufrufe nur fuer kritische Fehler.
- **Immer sowohl Client- als auch Server-Logs bei RPC-Problemen pruefen.** Der Fehler ist oft auf einer Seite und das Symptom auf der anderen. Ein serverseitiger Null-Pointer verwirft die Antwort stillschweigend, und der Client sieht nur "keine Daten empfangen."
- **File Patching am ersten Tag einrichten.** Der Bearbeiten-Neustart-Pruefen-Zyklus sinkt von 3-5 Minuten (PBO-Neubau) auf unter 30 Sekunden (speichern und neu verbinden). Dies ist die groesste Einzelproduktivitaetsverbesserung.
- **Ein konsistentes Log-Praefix wie `[MyMod]` in jedem Print-Aufruf verwenden.** Script-Logs enthalten Ausgaben von Vanilla-Code, der Engine und jeder geladenen Mod. Ohne Praefix ist Ihre Ausgabe im Rauschen unsichtbar.

---

## Theorie vs. Praxis

| Konzept | Theorie | Realitaet |
|---------|--------|---------|
| `SCRIPT (W)`-Warnungen | Warnungen sind nicht-fatal und koennen sicher ignoriert werden | Warnungen sagen oft zukuenftige Abstuerze voraus. Eine "Cannot open file"-Warnung heute wird morgen ein Null-Pointer-Absturz, wenn Code annimmt, dass die Datei geladen wurde. |
| Listen-Server-Tests | Gut genug um zu verifizieren, dass Skripte funktionieren | Listen-Server verbergen ganze Kategorien von Bugs: RPCs die nie das Netzwerk kreuzen, fehlende Autoritaetspruefungen, Null-`PlayerIdentity` auf dem Server und Race Conditions zwischen Client- und Server-Init. |
| File Patching | Jede Datei bearbeiten und Aenderungen sofort sehen | `config.cpp` wird nie per File Patching geladen. Neue `.c`-Dateien werden ebenfalls nicht aufgenommen. Beides erfordert einen PBO-Neubau. Nur Modifikationen an bestehenden Skript- und Layout-Dateien werden live nachgeladen. |
| Workbench-Debugger | Vollstaendige IDE-Debugging-Erfahrung | Workbench kann Syntax pruefen und isolierte Skripte ausfuehren, aber es repliziert nicht die vollstaendige Spielumgebung. Viele APIs geben null zurueck oder verhalten sich ausserhalb des Spiels anders. |

---

## Was Sie gelernt haben

In diesem Tutorial haben Sie gelernt:
- Wie Sie DayZ-Script-Logs finden und lesen, und was `SCRIPT (E)`- und `SCRIPT (W)`-Markierungen bedeuten
- Wie Sie `Print()`-Debugging mit Praefixen, Formatierern und umschaltbaren Debug-Loggern verwenden
- Wie Sie DayZDiag mit File Patching fuer schnelle Iteration einrichten
- Wie Sie die haeufigsten Fehlermuster diagnostizieren: Null-Pointer, Typkonflikte, undefinierte Variablen und Skriptschicht-Verletzungen
- Wie Sie einen zuverlaessigen Test-Workflow von der Bearbeitung bis zur Verifizierung etablieren

**Naechstes:** [Kapitel 8.8: Ein HUD-Overlay bauen](08-hud-overlay.md)

---
