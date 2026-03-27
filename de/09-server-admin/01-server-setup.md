# Kapitel 9.1: Server-Einrichtung & Erster Start

[Home](../README.md) | **Server-Einrichtung** | [Weiter: Verzeichnisstruktur >>](02-directory-structure.md)

---

> **Zusammenfassung:** Installieren Sie einen DayZ Standalone Dedicated Server von Grund auf mit SteamCMD, starten Sie ihn mit einer minimalen Konfiguration, pruefen Sie, ob er im Server-Browser erscheint, und verbinden Sie sich als Spieler. Dieses Kapitel deckt alles ab, von Hardwareanforderungen bis zur Behebung der haeufigsten Startprobleme.

---

## Inhaltsverzeichnis

- [Voraussetzungen](#voraussetzungen)
- [SteamCMD installieren](#steamcmd-installieren)
- [DayZ Server installieren](#dayz-server-installieren)
- [Verzeichnis nach der Installation](#verzeichnis-nach-der-installation)
- [Erster Start mit minimaler Konfiguration](#erster-start-mit-minimaler-konfiguration)
- [Ueberpruefen, ob der Server laeuft](#ueberpruefen-ob-der-server-laeuft)
- [Als Spieler verbinden](#als-spieler-verbinden)
- [Haeufige Startprobleme](#haeufige-startprobleme)

---

## Voraussetzungen

### Hardware

| Komponente | Minimum | Empfohlen |
|------------|---------|-----------|
| CPU | 4 Kerne, 2,4 GHz | 6+ Kerne, 3,5 GHz |
| RAM | 8 GB | 16 GB |
| Festplatte | 20 GB SSD | 40 GB NVMe SSD |
| Netzwerk | 10 Mbit/s Upload | 50+ Mbit/s Upload |
| Betriebssystem | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

DayZ Server ist fuer die Spiellogik single-threaded. Taktfrequenz ist wichtiger als Kernanzahl.

### Software

- **SteamCMD** -- der Steam-Kommandozeilen-Client zum Installieren von Dedicated Servern
- **Visual C++ Redistributable 2019** (Windows) -- erforderlich fuer `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- normalerweise bereits vorhanden
- Ports **2302-2305 UDP** muessen in Ihrem Router/Ihrer Firewall weitergeleitet werden

---

## SteamCMD installieren

### Windows

1. Laden Sie SteamCMD von https://developer.valvesoftware.com/wiki/SteamCMD herunter
2. Entpacken Sie `steamcmd.exe` in einen festen Ordner, z.B. `C:\SteamCMD\`
3. Fuehren Sie `steamcmd.exe` einmal aus -- es aktualisiert sich automatisch

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## DayZ Server installieren

Die Steam App ID des DayZ Servers ist **223350**. Sie koennen ihn installieren, ohne sich mit einem Steam-Konto anzumelden, das DayZ besitzt.

### Einzeilige Installation (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Einzeilige Installation (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Update-Skript

Erstellen Sie ein Skript, das Sie bei jedem Patch erneut ausfuehren koennen:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Update abgeschlossen.
pause
```

Das `validate`-Flag prueft jede Datei auf Beschaedigungen. Bei einer Neuinstallation ist ein Download von 2-3 GB zu erwarten.

---

## Verzeichnis nach der Installation

Nach der Installation sieht das Server-Stammverzeichnis so aus:

```
DayZServer/
  DayZServer_x64.exe        # Die Server-Ausfuehrungsdatei
  serverDZ.cfg               # Haupt-Server-Konfiguration
  dayzsetting.xml            # Rendering-/Videoeinstellungen (fuer Dedicated Server irrelevant)
  addons/                    # Vanilla-PBO-Dateien (ai.pbo, animals.pbo, usw.)
  battleye/                  # BattlEye Anti-Cheat (BEServer_x64.dll)
  dta/                       # Kern-Engine-Daten (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Signaturschluessel (dayz.bikey fuer Vanilla)
  logs/                      # Engine-Logs (Verbindung, Inhalt, Audio)
  mpmissions/                # Missionsordner
    dayzOffline.chernarusplus/   # Chernarus-Mission
    dayzOffline.enoch/           # Livonia-Mission (DLC)
    dayzOffline.sakhal/          # Sakhal-Mission (DLC)
  profiles/                  # Laufzeitausgabe: RPT-Logs, Script-Logs, Spieler-DB
  ban.txt                    # Gesperrte Spielerliste (Steam64-IDs)
  whitelist.txt              # Freigegebene Spieler (Steam64-IDs)
  steam_appid.txt            # Enthaelt "221100"
```

Wichtige Punkte:
- **Sie bearbeiten** `serverDZ.cfg` und Dateien in `mpmissions/`.
- **Sie bearbeiten niemals** Dateien in `addons/` oder `dta/` -- diese werden bei jedem Update ueberschrieben.
- **Mod-PBOs** kommen in das Server-Stammverzeichnis oder einen Unterordner (wird in einem spaeteren Kapitel behandelt).
- **`profiles/`** wird beim ersten Start erstellt und enthaelt Ihre Script-Logs und Crash-Dumps.

---

## Erster Start mit minimaler Konfiguration

### Schritt 1: serverDZ.cfg bearbeiten

Oeffnen Sie `serverDZ.cfg` in einem Texteditor. Fuer einen ersten Test verwenden Sie die einfachstmoegliche Konfiguration:

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### Schritt 2: Den Server starten

Oeffnen Sie eine Eingabeaufforderung im Server-Verzeichnis und fuehren Sie aus:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Flag | Zweck |
|------|-------|
| `-config=serverDZ.cfg` | Pfad zur Konfigurationsdatei |
| `-port=2302` | Haupt-Spielport (verwendet auch 2303-2305) |
| `-profiles=profiles` | Ausgabeordner fuer Logs und Spielerdaten |
| `-dologs` | Server-Logging aktivieren |
| `-adminlog` | Admin-Aktionen protokollieren |
| `-netlog` | Netzwerkereignisse protokollieren |
| `-freezecheck` | Automatischer Neustart bei Freeze-Erkennung |

### Schritt 3: Auf Initialisierung warten

Der Server benoetigt 30-90 Sekunden fuer den vollstaendigen Start. Beobachten Sie die Konsolenausgabe. Wenn Sie eine Zeile wie diese sehen:

```
BattlEye Server: Initialized (v1.xxx)
```

...ist der Server bereit fuer Verbindungen.

---

## Ueberpruefen, ob der Server laeuft

### Methode 1: Script-Log

Pruefen Sie `profiles/` auf eine Datei mit dem Namen `script_YYYY-MM-DD_HH-MM-SS.log`. Oeffnen Sie sie und suchen Sie nach:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Diese Zeilen bestaetigen, dass die Wirtschaft initialisiert und die Mission geladen wurde.

### Methode 2: RPT-Datei

Die `.RPT`-Datei in `profiles/` zeigt die Engine-Level-Ausgabe. Suchen Sie nach:

```
Dedicated host created.
BattlEye Server: Initialized
```

### Methode 3: Steam-Server-Browser

Oeffnen Sie Steam, gehen Sie zu **Ansicht > Spielserver > Favoriten**, klicken Sie auf **Server hinzufuegen**, geben Sie `127.0.0.1:2302` (oder Ihre oeffentliche IP) ein und klicken Sie auf **Spiele an dieser Adresse suchen**. Wenn der Server erscheint, laeuft er und ist erreichbar.

### Methode 4: Query-Port

Verwenden Sie ein externes Tool wie https://www.battlemetrics.com/ oder das npm-Paket `gamedig`, um Port 27016 abzufragen (Steam Query Port = Spielport + 24714).

---

## Als Spieler verbinden

### Vom selben Rechner

1. Starten Sie DayZ (nicht DayZ Server -- den normalen Spiel-Client)
2. Oeffnen Sie den **Server-Browser**
3. Gehen Sie zum Reiter **LAN** oder **Favoriten**
4. Fuegen Sie `127.0.0.1:2302` zu den Favoriten hinzu
5. Klicken Sie auf **Verbinden**

Wenn Sie Client und Server auf demselben Rechner ausfuehren, verwenden Sie `DayZDiag_x64.exe` (den Diagnose-Client) anstelle des regulaeren Clients. Starten Sie mit:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### Von einem anderen Rechner

Verwenden Sie die **oeffentliche IP** oder **LAN-IP** Ihres Servers, je nachdem, ob sich der Client im selben Netzwerk befindet. Die Ports 2302-2305 UDP muessen weitergeleitet werden.

---

## Haeufige Startprobleme

### Server startet, schliesst sich aber sofort

**Ursache:** Fehlende Visual C++ Redistributable oder ein Syntaxfehler in `serverDZ.cfg`.

**Loesung:** Installieren Sie VC++ Redist 2019 (x64). Pruefen Sie `serverDZ.cfg` auf fehlende Semikolons -- jede Parameterzeile muss mit `;` enden.

### "BattlEye initialization failed"

**Ursache:** Der `battleye/`-Ordner fehlt oder das Antivirenprogramm blockiert `BEServer_x64.dll`.

**Loesung:** Validieren Sie die Server-Dateien erneut ueber SteamCMD. Fuegen Sie eine Antivirenausnahme fuer den gesamten Serverordner hinzu.

### Server laeuft, erscheint aber nicht im Browser

**Ursache:** Ports nicht weitergeleitet, oder die Windows-Firewall blockiert die Ausfuehrungsdatei.

**Loesung:**
1. Fuegen Sie eine Windows-Firewall-Eingangsregel fuer `DayZServer_x64.exe` hinzu (alle UDP erlauben)
2. Leiten Sie die Ports **2302-2305 UDP** an Ihrem Router weiter
3. Pruefen Sie mit einem externen Port-Checker, ob 2302 UDP auf Ihrer oeffentlichen IP offen ist

### "Version Mismatch" beim Verbinden

**Ursache:** Server und Client haben unterschiedliche Versionen.

**Loesung:** Aktualisieren Sie beide. Fuehren Sie den SteamCMD-Update-Befehl fuer den Server aus. Der Client aktualisiert sich automatisch ueber Steam.

### Kein Loot spawnt

**Ursache:** Die Datei `init.c` fehlt oder die Hive-Initialisierung ist fehlgeschlagen.

**Loesung:** Stellen Sie sicher, dass `mpmissions/dayzOffline.chernarusplus/init.c` existiert und `CreateHive()` enthaelt. Pruefen Sie das Script-Log auf Fehler.

### Server nutzt 100% eines CPU-Kerns

Das ist normal. DayZ Server ist single-threaded. Fuehren Sie nicht mehrere Server-Instanzen auf demselben Kern aus -- verwenden Sie Prozessoraffinitaet oder separate Maschinen.

### Spieler spawnen als Kraehen / Haengen im Ladebildschirm

**Ursache:** Das Mission-Template in `serverDZ.cfg` stimmt nicht mit einem vorhandenen Ordner in `mpmissions/` ueberein.

**Loesung:** Pruefen Sie den Template-Wert. Er muss exakt mit einem Ordnernamen uebereinstimmen:

```cpp
template = "dayzOffline.chernarusplus";  // Muss mit dem mpmissions/-Ordnernamen uebereinstimmen
```

---

**[Home](../README.md)** | **Weiter:** [Verzeichnisstruktur >>](02-directory-structure.md)
