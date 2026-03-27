# Kapitel 9.10: Mod-Verwaltung

[Home](../README.md) | [<< Zurueck: Zugriffskontrolle](09-access-control.md) | [Weiter: Fehlerbehebung >>](11-troubleshooting.md)

---

> **Zusammenfassung:** Installieren, konfigurieren und warten Sie Drittanbieter-Mods auf einem DayZ Dedicated Server. Behandelt werden Startparameter, Workshop-Downloads, Signaturschluessel, Ladereihenfolge, Server-Only vs Client-erforderliche Mods, Updates und die haeufigsten Fehler, die zu Abstuerzen oder Spieler-Kicks fuehren.

---

## Inhaltsverzeichnis

- [Wie Mods geladen werden](#wie-mods-geladen-werden)
- [Startparameter-Format](#startparameter-format)
- [Workshop-Mod-Installation](#workshop-mod-installation)
- [Mod-Schluessel (.bikey)](#mod-schluessel-bikey)
- [Ladereihenfolge und Abhaengigkeiten](#ladereihenfolge-und-abhaengigkeiten)
- [Server-Only vs Client-erforderliche Mods](#server-only-vs-client-erforderliche-mods)
- [Mods aktualisieren](#mods-aktualisieren)
- [Mod-Konflikte beheben](#mod-konflikte-beheben)
- [Haeufige Fehler](#haeufige-fehler)

---

## Wie Mods geladen werden

DayZ laedt Mods ueber den `-mod=`-Startparameter. Jeder Eintrag ist ein Pfad zu einem Ordner, der PBO-Dateien und eine `config.cpp` enthaelt. Die Engine liest jede PBO in jedem Mod-Ordner, registriert ihre Klassen und Scripts und faehrt dann mit dem naechsten Mod in der Liste fort.

Server und Client muessen dieselben Mods in `-mod=` haben. Wenn der Server `@CF;@MyMod` auflistet und der Client nur `@CF` hat, schlaegt die Verbindung mit einem Signatur-Mismatch fehl. Server-Only-Mods in `-servermod=` sind die Ausnahme -- Clients benoetigen diese nie.

---

## Startparameter-Format

Ein typischer Modded-Server-Startbefehl:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Parameter | Zweck |
|-----------|-------|
| `-mod=` | Mods, die sowohl von Server als auch von allen verbindenden Clients benoetigt werden |
| `-servermod=` | Server-Only-Mods (Clients benoetigen sie nicht) |

Regeln:
- Pfade sind **durch Semikolons getrennt**, ohne Leerzeichen um die Semikolons
- Jeder Pfad ist relativ zum Server-Stammverzeichnis (z.B. `@CF` bedeutet `<server_root>/@CF/`)
- Sie koennen absolute Pfade verwenden: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **Reihenfolge ist wichtig** -- Abhaengigkeiten muessen vor den Mods erscheinen, die sie benoetigen

---

## Workshop-Mod-Installation

### Schritt 1: Mod herunterladen

Verwenden Sie SteamCMD mit der DayZ-**Client**-App-ID (221100) und der Workshop-ID des Mods:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

Heruntergeladene Dateien landen in:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Schritt 2: Symlink oder Kopie erstellen

Workshop-Ordner verwenden numerische IDs, die in `-mod=` nicht nutzbar sind. Erstellen Sie einen benannten Symlink (empfohlen) oder kopieren Sie den Ordner:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Die Verwendung einer Junction bedeutet, dass Updates ueber SteamCMD automatisch angewendet werden -- kein erneutes Kopieren erforderlich.

### Schritt 3: .bikey kopieren

Siehe den naechsten Abschnitt.

---

## Mod-Schluessel (.bikey)

Jeder signierte Mod wird mit einem `keys/`-Ordner geliefert, der eine oder mehrere `.bikey`-Dateien enthaelt. Diese Dateien teilen BattlEye mit, welche PBO-Signaturen akzeptiert werden sollen.

1. Oeffnen Sie den Mod-Ordner (z.B. `@CF/keys/`)
2. Kopieren Sie jede `.bikey`-Datei in das `keys/`-Stammverzeichnis des Servers

```
DayZServer/
  keys/
    dayz.bikey              # Vanilla -- immer vorhanden
    cf.bikey                # Kopiert aus @CF/keys/
    vpp_admintools.bikey    # Kopiert aus @VPPAdminTools/keys/
```

Ohne den korrekten Schluessel erhaelt jeder Spieler, der diesen Mod nutzt: **"Player kicked: Modified data"**.

---

## Ladereihenfolge und Abhaengigkeiten

Mods werden von links nach rechts im `-mod=`-Parameter geladen. Die `config.cpp` eines Mods deklariert seine Abhaengigkeiten:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Wenn `MyMod` `CF` benoetigt, muss `@CF` **vor** `@MyMod` im Startparameter erscheinen:

```
-mod=@CF;@MyMod          korrekt
-mod=@MyMod;@CF          Absturz oder fehlende Klassen
```

**Allgemeines Ladereihenfolge-Muster:**

1. **Framework-Mods** -- CF, Community-Online-Tools
2. **Bibliotheks-Mods** -- BuilderItems, jedes geteilte Asset-Paket
3. **Feature-Mods** -- Kartenerweiterungen, Waffen, Fahrzeuge
4. **Abhaengige Mods** -- alles, was die oben genannten als `requiredAddons` auflistet

Im Zweifelsfall pruefen Sie die Workshop-Seite oder Dokumentation des Mods. Die meisten Mod-Autoren veroeffentlichen ihre erforderliche Ladereihenfolge.

---

## Server-Only vs Client-erforderliche Mods

| Parameter | Wer benoetigt ihn | Typische Beispiele |
|-----------|-------------------|---------------------|
| `-mod=` | Server + alle Clients | Waffen, Fahrzeuge, Karten, UI-Mods, Kleidung |
| `-servermod=` | Nur der Server | Wirtschaftsmanager, Logging-Tools, Admin-Backends, Scheduler-Scripts |

Die Regel ist einfach: Wenn ein Mod **irgendwelche** clientseitigen Scripts, Layouts, Texturen oder Modelle enthaelt, muss er in `-mod=`. Wenn er nur serverseitige Logik ohne Assets ausfuehrt, die der Client jemals beruehrt, verwenden Sie `-servermod=`.

Einen Server-Only-Mod in `-mod=` zu platzieren zwingt jeden Spieler, ihn herunterzuladen. Einen Client-erforderlichen Mod in `-servermod=` zu platzieren verursacht fehlende Texturen, defekte UI oder Script-Fehler auf dem Client.

---

## Mods aktualisieren

### Vorgehensweise

1. **Server stoppen** -- das Aktualisieren von Dateien waehrend der Server laeuft kann PBOs beschaedigen
2. **Erneut herunterladen** ueber SteamCMD:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Aktualisierte .bikey-Dateien kopieren** -- Mod-Autoren rotieren gelegentlich ihre Signierschluessel. Kopieren Sie immer die frische `.bikey` aus dem `keys/`-Ordner des Mods in das `keys/`-Verzeichnis des Servers
4. **Server neustarten**

Wenn Sie Symlinks (Junctions) verwendet haben, aktualisiert Schritt 2 die Mod-Dateien direkt. Wenn Sie Dateien manuell kopiert haben, muessen Sie sie erneut kopieren.

### Client-seitige Updates

Spieler, die den Mod auf dem Steam Workshop abonniert haben, erhalten Updates automatisch. Wenn Sie einen Mod auf dem Server aktualisieren und ein Spieler die alte Version hat, erhaelt er einen Signatur-Mismatch und kann sich nicht verbinden, bis sein Client aktualisiert ist.

---

## Mod-Konflikte beheben

### RPT-Log pruefen

Oeffnen Sie die neueste `.RPT`-Datei in `profiles/`. Suchen Sie nach:

- **"Cannot register"** -- eine Klassennamen-Kollision zwischen zwei Mods
- **"Missing addons"** -- eine Abhaengigkeit ist nicht geladen (falsche Ladereihenfolge oder fehlender Mod)
- **"Signature verification failed"** -- `.bikey`-Mismatch oder fehlender Schluessel

### Script-Log pruefen

Oeffnen Sie das neueste `script_*.log` in `profiles/`. Suchen Sie nach:

- **"SCRIPT (E)"**-Zeilen -- Script-Fehler, oft verursacht durch Ladereihenfolge oder Versions-Mismatch
- **"Definition of variable ... already exists"** -- zwei Mods definieren dieselbe Klasse

### Problem isolieren

Wenn Sie viele Mods haben und etwas nicht funktioniert, testen Sie schrittweise:

1. Starten Sie nur mit Framework-Mods (`@CF`)
2. Fuegen Sie einen Mod nach dem anderen hinzu
3. Starten Sie und pruefen Sie die Logs nach jeder Hinzufuegung
4. Der Mod, der Fehler verursacht, ist der Uebeltaeter

### Zwei Mods bearbeiten dieselbe Klasse

Wenn zwei Mods beide `modded class PlayerBase` verwenden, gewinnt der zuletzt geladene (am weitesten rechts in `-mod=`). Sein `super`-Aufruf verkettet sich zur Version des anderen Mods. Dies funktioniert normalerweise, aber wenn ein Mod eine Methode ueberschreibt, ohne `super` aufzurufen, gehen die Aenderungen des anderen Mods verloren.

---

## Haeufige Fehler

**Falsche Ladereihenfolge.** Der Server stuerzt ab oder protokolliert "Missing addons", weil eine Abhaengigkeit noch nicht geladen war. Loesung: Verschieben Sie den Abhaengigkeits-Mod frueher in die `-mod=`-Liste.

**Vergessen von `-servermod=` fuer Server-Only-Mods.** Spieler werden gezwungen, einen Mod herunterzuladen, den sie nicht benoetigen. Loesung: Verschieben Sie Server-Only-Mods von `-mod=` nach `-servermod=`.

**`.bikey`-Dateien nach einem Mod-Update nicht aktualisieren.** Spieler werden mit "Modified data" gekickt, weil der Server-Schluessel nicht zu den neuen PBO-Signaturen des Mods passt. Loesung: Kopieren Sie immer `.bikey`-Dateien erneut, wenn Sie Mods aktualisieren.

**Mod-PBOs neu verpacken.** Das Neuverpacken der PBO-Dateien eines Mods bricht seine digitale Signatur, verursacht BattlEye-Kicks fuer jeden Spieler und verstoesst gegen die Nutzungsbedingungen der meisten Mod-Autoren. Verpacken Sie niemals einen Mod neu, den Sie nicht erstellt haben.

**Workshop-Pfade mit lokalen Pfaden mischen.** Den rohen numerischen Workshop-Pfad fuer einige Mods und benannte Ordner fuer andere zu verwenden, verursacht Verwirrung beim Aktualisieren. Entscheiden Sie sich fuer einen Ansatz -- Symlinks sind am saubersten.

**Leerzeichen in Mod-Pfaden.** Ein Pfad wie `-mod=@My Mod` bricht das Parsen. Benennen Sie Mod-Ordner um, um Leerzeichen zu vermeiden, oder umschliessen Sie den gesamten Parameter mit Anfuehrungszeichen: `-mod="@My Mod;@CF"`.

**Veralteter Mod auf dem Server, aktualisiert auf dem Client (oder umgekehrt).** Versions-Mismatch verhindert die Verbindung. Halten Sie Server- und Workshop-Versionen synchron. Aktualisieren Sie alle Mods und den Server gleichzeitig.

---

[Home](../README.md) | [<< Zurueck: Zugriffskontrolle](09-access-control.md) | [Weiter: Fehlerbehebung >>](11-troubleshooting.md)
