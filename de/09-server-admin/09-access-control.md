# Kapitel 9.9: Zugriffskontrolle

[Home](../README.md) | [<< Zurueck: Performance-Optimierung](08-performance.md) | [Weiter: Mod-Verwaltung >>](10-mod-management.md)

---

> **Zusammenfassung:** Konfigurieren Sie, wer sich mit Ihrem DayZ-Server verbinden kann, wie Sperren funktionieren, wie Sie die Fernverwaltung aktivieren und wie die Mod-Signaturverifizierung unbefugte Inhalte fernhaelt. Dieses Kapitel behandelt jeden Zugriffskontrollmechanismus, der einem Serverbetreiber zur Verfuegung steht.

---

## Inhaltsverzeichnis

- [Admin-Zugang ueber serverDZ.cfg](#admin-zugang-ueber-serverdzcfg)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [BattlEye Anti-Cheat](#battleye-anti-cheat)
- [RCON (Remote Console)](#rcon-remote-console)
- [Signaturverifizierung](#signaturverifizierung)
- [Das keys/-Verzeichnis](#das-keys-verzeichnis)
- [In-Game Admin-Tools](#in-game-admin-tools)
- [Haeufige Fehler](#haeufige-fehler)

---

## Admin-Zugang ueber serverDZ.cfg

Der `passwordAdmin`-Parameter in **serverDZ.cfg** setzt das Admin-Passwort fuer Ihren Server:

```cpp
passwordAdmin = "YourSecretPassword";
```

Sie verwenden dieses Passwort auf zwei Arten:

1. **Im Spiel** -- oeffnen Sie den Chat und geben Sie `#login YourSecretPassword` ein, um Admin-Privilegien fuer diese Sitzung zu erhalten.
2. **RCON** -- verbinden Sie sich mit einem BattlEye-RCON-Client unter Verwendung dieses Passworts (siehe den RCON-Abschnitt unten).

Halten Sie das Admin-Passwort lang und einzigartig. Jeder, der es hat, hat volle Kontrolle ueber den laufenden Server.

---

## ban.txt

Die Datei **ban.txt** befindet sich in Ihrem Server-Profilverzeichnis (der Pfad, den Sie mit `-profiles=` festgelegt haben). Sie enthaelt eine SteamID64 pro Zeile:

```
76561198012345678
76561198087654321
```

- Jede Zeile ist eine nackte 17-stellige SteamID64 -- keine Namen, keine Kommentare, keine Passwoerter.
- Spieler, deren SteamID in dieser Datei erscheint, wird die Verbindung beim Beitritt verweigert.
- Sie koennen die Datei bearbeiten, waehrend der Server laeuft; Aenderungen werden beim naechsten Verbindungsversuch wirksam.

---

## whitelist.txt

Die Datei **whitelist.txt** befindet sich im selben Profilverzeichnis. Wenn Sie die Whitelist aktivieren, koennen sich nur SteamIDs verbinden, die in dieser Datei aufgefuehrt sind:

```
76561198012345678
76561198087654321
```

Das Format ist identisch mit **ban.txt** -- eine SteamID64 pro Zeile, sonst nichts.

Die Whitelist ist nuetzlich fuer private Communities, Testserver oder Events, bei denen Sie eine kontrollierte Spielerliste benoetigen.

---

## BattlEye Anti-Cheat

BattlEye ist das in DayZ integrierte Anti-Cheat-System. Seine Dateien befinden sich im `BattlEye/`-Ordner innerhalb Ihres Serververzeichnisses:

| Datei | Zweck |
|-------|-------|
| **BEServer_x64.dll** | Die BattlEye Anti-Cheat-Engine-Binaerdatei |
| **beserver_x64.cfg** | Konfigurationsdatei (RCON-Port, RCON-Passwort) |
| **bans.txt** | BattlEye-spezifische Sperren (GUID-basiert, nicht SteamID) |

BattlEye ist standardmaessig aktiviert. Sie starten den Server mit `DayZServer_x64.exe` und BattlEye laedt automatisch. Um es explizit zu deaktivieren (fuer Produktionsserver nicht empfohlen), verwenden Sie den Startparameter `-noBE`.

Die **bans.txt**-Datei im `BattlEye/`-Ordner verwendet BattlEye-GUIDs, die sich von SteamID64s unterscheiden. Sperren, die ueber RCON oder BattlEye-Befehle ausgesprochen werden, werden automatisch in diese Datei geschrieben.

---

## RCON (Remote Console)

BattlEye RCON ermoeglicht Ihnen, den Server ohne In-Game-Praesenz aus der Ferne zu verwalten. Konfigurieren Sie es in `BattlEye/beserver_x64.cfg`:

```
RConPassword yourpassword
RConPort 2306
```

Der Standard-RCON-Port ist Ihr Spielport plus 4. Wenn Ihr Server auf Port `2302` laeuft, ist der RCON-Standard `2306`.

### Verfuegbare RCON-Befehle

| Befehl | Auswirkung |
|--------|------------|
| `kick <Spieler> [Grund]` | Einen Spieler vom Server kicken |
| `ban <Spieler> [Minuten] [Grund]` | Einen Spieler sperren (schreibt in BattlEye bans.txt) |
| `say -1 <Nachricht>` | Nachricht an alle Spieler senden |
| `#shutdown` | Ordnungsgemaesses Herunterfahren des Servers |
| `#lock` | Server sperren (keine neuen Verbindungen) |
| `#unlock` | Server entsperren |
| `players` | Verbundene Spieler auflisten |

Sie verbinden sich mit RCON ueber einen BattlEye-RCON-Client (mehrere kostenlose Tools existieren). Die Verbindung erfordert die IP, den RCON-Port und das Passwort aus **beserver_x64.cfg**.

---

## Signaturverifizierung

Der `verifySignatures`-Parameter in **serverDZ.cfg** steuert, ob der Server Mod-Signaturen prueft:

```cpp
verifySignatures = 2;
```

| Wert | Verhalten |
|------|-----------|
| `0` | Deaktiviert -- jeder kann mit beliebigen Mods beitreten, keine Signaturpruefung |
| `2` | Vollstaendige Verifizierung -- Clients muessen gueltige Signaturen fuer alle geladenen Mods haben (Standard) |

Verwenden Sie auf Produktionsservern immer `verifySignatures = 2`. Die Einstellung auf `0` erlaubt Spielern, mit modifizierten oder unsignierten Mods beizutreten, was ein ernstes Sicherheitsrisiko darstellt.

---

## Das keys/-Verzeichnis

Das `keys/`-Verzeichnis in Ihrem Server-Stammverzeichnis enthaelt **.bikey**-Dateien. Jede `.bikey` entspricht einem Mod und teilt dem Server mit: "Die Signaturen dieses Mods sind vertrauenswuerdig."

Wenn `verifySignatures = 2`:

1. Der Server prueft jeden Mod, den der verbindende Client geladen hat.
2. Fuer jeden Mod sucht der Server nach einer passenden `.bikey` in `keys/`.
3. Wenn ein passender Schluessel fehlt, wird der Spieler gekickt.

Jeder Mod, den Sie auf dem Server installieren, wird mit einer `.bikey`-Datei geliefert (normalerweise im `Keys/`- oder `Key/`-Unterordner des Mods). Sie kopieren diese Datei in das `keys/`-Verzeichnis Ihres Servers.

```
DayZServer/
  keys/
    dayz.bikey              <- Vanilla (immer vorhanden)
    MyMod.bikey             <- kopiert aus @MyMod/Keys/
    AnotherMod.bikey        <- kopiert aus @AnotherMod/Keys/
```

Wenn Sie einen neuen Mod hinzufuegen und vergessen, seine `.bikey` zu kopieren, wird jeder Spieler, der diesen Mod nutzt, beim Verbinden gekickt.

---

## In-Game Admin-Tools

Sobald Sie sich mit `#login <Passwort>` im Chat eingeloggt haben, erhalten Sie Zugang zu den Admin-Tools:

- **Spielerliste** -- alle verbundenen Spieler mit ihren SteamIDs anzeigen.
- **Kick/Sperre** -- Spieler direkt aus der Spielerliste entfernen oder sperren.
- **Teleport** -- die Admin-Karte verwenden, um sich an beliebige Positionen zu teleportieren.
- **Admin-Log** -- serverseitiges Protokoll von Spieleraktionen (Kills, Verbindungen, Trennungen), geschrieben in `*.ADM`-Dateien im Profilverzeichnis.
- **Freie Kamera** -- vom Charakter loesen und ueber die Karte fliegen.

Diese Tools sind im Vanilla-Spiel integriert. Drittanbieter-Mods (wie Community Online Tools) erweitern die Admin-Moeglichkeiten erheblich.

---

## Haeufige Fehler

Dies sind die Probleme, auf die Serverbetreiber am haeufigsten stossen:

| Fehler | Symptom | Loesung |
|--------|---------|---------|
| Fehlende `.bikey` in `keys/` | Spieler werden beim Beitritt mit einem Signaturfehler gekickt | Kopieren Sie die `.bikey`-Datei des Mods in das `keys/`-Verzeichnis Ihres Servers |
| Namen oder Passwoerter in **ban.txt** eintragen | Sperren funktionieren nicht; zufaellige Fehler | Verwenden Sie nur nackte SteamID64-Werte, einen pro Zeile |
| RCON-Portkonflikt | RCON-Client kann sich nicht verbinden | Stellen Sie sicher, dass der RCON-Port nicht von einem anderen Dienst belegt ist; pruefen Sie die Firewallregeln |
| `verifySignatures = 0` in der Produktion | Jeder kann mit manipulierten Mods beitreten | Setzen Sie es auf `2` auf jedem oeffentlichen Server |
| Vergessen, den RCON-Port in der Firewall zu oeffnen | RCON-Client laeuft in Timeout | Oeffnen Sie den RCON UDP-Port (Standard 2306) in Ihrer Firewall |
| **bans.txt** im `BattlEye/`-Ordner mit SteamIDs bearbeiten | Sperren funktionieren nicht | BattlEye **bans.txt** verwendet GUIDs, nicht SteamIDs; verwenden Sie **ban.txt** im Profilverzeichnis fuer SteamID-Sperren |

---

[Home](../README.md) | [<< Zurueck: Performance-Optimierung](08-performance.md) | [Weiter: Mod-Verwaltung >>](10-mod-management.md)
