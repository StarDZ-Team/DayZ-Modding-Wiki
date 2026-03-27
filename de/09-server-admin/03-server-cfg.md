# Kapitel 9.3: Vollstaendige serverDZ.cfg-Referenz

[Home](../README.md) | [<< Zurueck: Verzeichnisstruktur](02-directory-structure.md) | **serverDZ.cfg-Referenz** | [Weiter: Loot-Wirtschaft im Detail >>](04-loot-economy.md)

---

> **Zusammenfassung:** Jeder Parameter in `serverDZ.cfg` dokumentiert mit Zweck, gueltigen Werten und Standardverhalten. Diese Datei steuert Server-Identitaet, Netzwerkeinstellungen, Gameplay-Regeln, Zeitbeschleunigung und Missionsauswahl.

---

## Inhaltsverzeichnis

- [Dateiformat](#dateiformat)
- [Server-Identitaet](#server-identitaet)
- [Netzwerk & Sicherheit](#netzwerk--sicherheit)
- [Gameplay-Regeln](#gameplay-regeln)
- [Zeit & Wetter](#zeit--wetter)
- [Performance & Login-Warteschlange](#performance--login-warteschlange)
- [Persistenz & Instanz](#persistenz--instanz)
- [Missionsauswahl](#missionsauswahl)
- [Vollstaendige Beispieldatei](#vollstaendige-beispieldatei)
- [Startparameter, die die Konfiguration ueberschreiben](#startparameter-die-die-konfiguration-ueberschreiben)

---

## Dateiformat

`serverDZ.cfg` verwendet Bohemias Konfigurationsformat (aehnlich wie C). Regeln:

- Jede Parameterzuweisung endet mit einem **Semikolon** `;`
- Strings werden in **doppelte Anfuehrungszeichen** `""` eingeschlossen
- Kommentare verwenden `//` fuer Einzeiler
- Der `class Missions`-Block verwendet geschweifte Klammern `{}` und endet mit `};`
- Die Datei muss UTF-8 oder ANSI codiert sein -- kein BOM

Ein fehlendes Semikolon fuehrt dazu, dass der Server stillschweigend fehlschlaegt oder nachfolgende Parameter ignoriert.

---

## Server-Identitaet

```cpp
hostname = "My DayZ Server";         // Servername im Browser
password = "";                       // Passwort zum Verbinden (leer = oeffentlich)
passwordAdmin = "";                  // Passwort fuer Admin-Login ueber die In-Game-Konsole
description = "";                    // Beschreibung in den Server-Browser-Details
```

| Parameter | Typ | Standard | Hinweise |
|-----------|-----|----------|----------|
| `hostname` | string | `""` | Wird im Server-Browser angezeigt. Maximal ~100 Zeichen. |
| `password` | string | `""` | Leer lassen fuer einen oeffentlichen Server. Spieler muessen dies eingeben, um beizutreten. |
| `passwordAdmin` | string | `""` | Wird mit dem Befehl `#login` im Spiel verwendet. **Setzen Sie dies auf jedem Server.** |
| `description` | string | `""` | Mehrzeilige Beschreibungen werden nicht unterstuetzt. Halten Sie es kurz. |

---

## Netzwerk & Sicherheit

```cpp
maxPlayers = 60;                     // Maximale Spielerplaetze
verifySignatures = 2;                // PBO-Signaturverifizierung (nur 2 wird unterstuetzt)
forceSameBuild = 1;                  // Uebereinstimmende Client-/Server-Exe-Version erforderlich
enableWhitelist = 0;                 // Whitelist aktivieren/deaktivieren
disableVoN = 0;                      // Voice-over-Network deaktivieren
vonCodecQuality = 20;               // VoN-Audioqualitaet (0-30)
guaranteedUpdates = 1;               // Netzwerkprotokoll (immer 1 verwenden)
```

| Parameter | Typ | Gueltige Werte | Standard | Hinweise |
|-----------|-----|----------------|----------|----------|
| `maxPlayers` | int | 1-60 | 60 | Beeinflusst den RAM-Verbrauch. Jeder Spieler fuegt ~50-100 MB hinzu. |
| `verifySignatures` | int | 2 | 2 | Nur der Wert 2 wird unterstuetzt. Verifiziert PBO-Dateien gegen `.bisign`-Schluessel. |
| `forceSameBuild` | int | 0, 1 | 1 | Bei 1 muessen Clients die exakte Server-Exe-Version haben. Immer auf 1 belassen. |
| `enableWhitelist` | int | 0, 1 | 0 | Bei 1 koennen nur Steam64-IDs aus `whitelist.txt` verbinden. |
| `disableVoN` | int | 0, 1 | 0 | Auf 1 setzen, um den In-Game-Voice-Chat komplett zu deaktivieren. |
| `vonCodecQuality` | int | 0-30 | 20 | Hoehere Werte bedeuten bessere Sprachqualitaet, aber mehr Bandbreite. 20 ist ein guter Kompromiss. |
| `guaranteedUpdates` | int | 1 | 1 | Netzwerkprotokoll-Einstellung. Immer 1 verwenden. |

### Shard-ID

```cpp
shardId = "123abc";                  // Sechs alphanumerische Zeichen fuer private Shards
```

| Parameter | Typ | Standard | Hinweise |
|-----------|-----|----------|----------|
| `shardId` | string | `""` | Wird fuer Private-Hive-Server verwendet. Spieler auf Servern mit derselben `shardId` teilen Charakterdaten. Leer lassen fuer einen Public Hive. |

---

## Gameplay-Regeln

```cpp
disable3rdPerson = 0;               // Dritte-Person-Kamera deaktivieren
disableCrosshair = 0;               // Fadenkreuz deaktivieren
disablePersonalLight = 1;           // Umgebungs-Spielerlicht deaktivieren
lightingConfig = 0;                 // Nachthelligkeit (0 = heller, 1 = dunkler)
```

| Parameter | Typ | Gueltige Werte | Standard | Hinweise |
|-----------|-----|----------------|----------|----------|
| `disable3rdPerson` | int | 0, 1 | 0 | Auf 1 setzen fuer Erste-Person-Only-Server. Dies ist die haeufigste "Hardcore"-Einstellung. |
| `disableCrosshair` | int | 0, 1 | 0 | Auf 1 setzen, um das Fadenkreuz zu entfernen. Wird oft mit `disable3rdPerson=1` kombiniert. |
| `disablePersonalLight` | int | 0, 1 | 1 | Das "Personal Light" ist ein dezentes Leuchten um den Spieler bei Nacht. Die meisten Server deaktivieren es (Wert 1) fuer Realismus. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = hellere Naechte (Mondlicht sichtbar). 1 = stockdunkle Naechte (Taschenlampe/NVG erforderlich). |

---

## Zeit & Wetter

```cpp
serverTime = "SystemTime";                 // Anfangszeit
serverTimeAcceleration = 12;               // Zeitgeschwindigkeits-Multiplikator (0-24)
serverNightTimeAcceleration = 1;           // Nachtzeit-Geschwindigkeits-Multiplikator (0.1-64)
serverTimePersistent = 0;                  // Zeit zwischen Neustarts speichern
```

| Parameter | Typ | Gueltige Werte | Standard | Hinweise |
|-----------|-----|----------------|----------|----------|
| `serverTime` | string | `"SystemTime"` oder `"YYYY/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` verwendet die lokale Uhr des Rechners. Setzen Sie eine feste Zeit wie `"2024/9/15/12/0"` fuer einen permanenten Tagesserver. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Multiplikator fuer die In-Game-Zeit. Bei 12 dauert ein voller 24-Stunden-Zyklus 2 reale Stunden. Bei 1 laeuft die Zeit in Echtzeit. Bei 24 vergeht ein voller Tag in 1 Stunde. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Wird mit `serverTimeAcceleration` multipliziert. Bei Wert 4 mit Beschleunigung 12 vergeht die Nacht mit 48-facher Geschwindigkeit (sehr kurze Naechte). |
| `serverTimePersistent` | int | 0, 1 | 0 | Bei 1 speichert der Server seine In-Game-Uhr auf der Festplatte und setzt sie nach einem Neustart fort. Bei 0 wird die Zeit bei jedem Neustart auf `serverTime` zurueckgesetzt. |

### Gaengige Zeitkonfigurationen

**Immer Tag:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Schneller Tag-/Nachtzyklus (2-Stunden-Tage, kurze Naechte):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Echtzeit Tag/Nacht:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Performance & Login-Warteschlange

```cpp
loginQueueConcurrentPlayers = 5;     // Gleichzeitig verarbeitete Spieler beim Login
loginQueueMaxPlayers = 500;          // Maximale Login-Warteschlangengroesse
```

| Parameter | Typ | Standard | Hinweise |
|-----------|-----|----------|----------|
| `loginQueueConcurrentPlayers` | int | 5 | Wie viele Spieler gleichzeitig geladen werden. Niedrigere Werte reduzieren Server-Lastspitzen nach einem Neustart. Erhoehen Sie auf 10-15, wenn Ihre Hardware leistungsstark ist und Spieler sich ueber Wartezeiten beschweren. |
| `loginQueueMaxPlayers` | int | 500 | Wenn bereits so viele Spieler in der Warteschlange sind, werden neue Verbindungen abgelehnt. 500 reicht fuer die meisten Server. |

---

## Persistenz & Instanz

```cpp
instanceId = 1;                      // Server-Instanz-Bezeichner
storageAutoFix = 1;                  // Automatische Reparatur beschaedigter Persistenzdateien
```

| Parameter | Typ | Standard | Hinweise |
|-----------|-----|----------|----------|
| `instanceId` | int | 1 | Identifiziert die Server-Instanz. Persistenzdaten werden in `storage_<instanceId>/` gespeichert. Wenn Sie mehrere Server auf demselben Rechner betreiben, geben Sie jedem eine andere `instanceId`. |
| `storageAutoFix` | int | 1 | Bei 1 prueft der Server Persistenzdateien beim Start und ersetzt beschaedigte durch leere Dateien. Immer auf 1 belassen. |

---

## Missionsauswahl

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

Der `template`-Wert muss exakt mit einem Ordnernamen in `mpmissions/` uebereinstimmen. Verfuegbare Vanilla-Missionen:

| Template | Karte | DLC erforderlich |
|----------|-------|:---:|
| `dayzOffline.chernarusplus` | Chernarus | Nein |
| `dayzOffline.enoch` | Livonia | Ja |
| `dayzOffline.sakhal` | Sakhal | Ja |

Benutzerdefinierte Missionen (z.B. von Mods oder Community-Karten) verwenden ihren eigenen Template-Namen. Der Ordner muss in `mpmissions/` vorhanden sein.

---

## Vollstaendige Beispieldatei

Dies ist die vollstaendige Standard-`serverDZ.cfg` mit allen Parametern:

```cpp
hostname = "EXAMPLE NAME";              // Servername
password = "";                          // Passwort zum Verbinden mit dem Server
passwordAdmin = "";                     // Passwort, um Server-Admin zu werden

description = "";                       // Server-Browser-Beschreibung

enableWhitelist = 0;                    // Whitelist aktivieren/deaktivieren (Wert 0-1)

maxPlayers = 60;                        // Maximale Spieleranzahl

verifySignatures = 2;                   // Verifiziert .pbos gegen .bisign-Dateien (nur 2 wird unterstuetzt)
forceSameBuild = 1;                     // Uebereinstimmende Client-/Server-Version erforderlich (Wert 0-1)

disableVoN = 0;                         // Voice-over-Network aktivieren/deaktivieren (Wert 0-1)
vonCodecQuality = 20;                   // Voice-over-Network-Codec-Qualitaet (Werte 0-30)

shardId = "123abc";                     // Sechs alphanumerische Zeichen fuer privaten Shard

disable3rdPerson = 0;                   // Dritte-Person-Ansicht umschalten (Wert 0-1)
disableCrosshair = 0;                   // Fadenkreuz umschalten (Wert 0-1)

disablePersonalLight = 1;              // Persoenliches Licht fuer alle Clients deaktivieren
lightingConfig = 0;                     // 0 fuer hellere, 1 fuer dunklere Nacht

serverTime = "SystemTime";             // Anfangs-In-Game-Zeit ("SystemTime" oder "YYYY/MM/DD/HH/MM")
serverTimeAcceleration = 12;           // Zeitgeschwindigkeits-Multiplikator (0-24)
serverNightTimeAcceleration = 1;       // Nachtzeit-Geschwindigkeits-Multiplikator (0.1-64), wird auch mit serverTimeAcceleration multipliziert
serverTimePersistent = 0;              // Zeit zwischen Neustarts speichern (Wert 0-1)

guaranteedUpdates = 1;                 // Netzwerkprotokoll (immer 1 verwenden)

loginQueueConcurrentPlayers = 5;       // Gleichzeitig verarbeitete Spieler beim Login
loginQueueMaxPlayers = 500;            // Maximale Login-Warteschlangengroesse

instanceId = 1;                        // Server-Instanz-ID (beeinflusst storage-Ordnerbenennung)

storageAutoFix = 1;                    // Automatische Reparatur beschaedigter Persistenz (Wert 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Startparameter, die die Konfiguration ueberschreiben

Einige Einstellungen koennen ueber Kommandozeilenparameter beim Start von `DayZServer_x64.exe` ueberschrieben werden:

| Parameter | Ueberschreibt | Beispiel |
|-----------|---------------|----------|
| `-config=` | Konfigurationsdateipfad | `-config=serverDZ.cfg` |
| `-port=` | Spielport | `-port=2302` |
| `-profiles=` | Ausgabeverzeichnis fuer Profile | `-profiles=profiles` |
| `-mod=` | Client-seitige Mods (durch Semikolons getrennt) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Server-Only-Mods | `-servermod=@MyServerMod` |
| `-BEpath=` | BattlEye-Pfad | `-BEpath=battleye` |
| `-dologs` | Logging aktivieren | -- |
| `-adminlog` | Admin-Logging aktivieren | -- |
| `-netlog` | Netzwerk-Logging aktivieren | -- |
| `-freezecheck` | Automatischer Neustart bei Freeze | -- |
| `-cpuCount=` | Zu verwendende CPU-Kerne | `-cpuCount=4` |
| `-noFilePatching` | File Patching deaktivieren | -- |

### Vollstaendiges Startbeispiel

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Mods werden in der in `-mod=` angegebenen Reihenfolge geladen. Die Abhaengigkeitsreihenfolge ist wichtig: Wenn Mod B Mod A benoetigt, listen Sie Mod A zuerst auf.

---

**Zurueck:** [Verzeichnisstruktur](02-directory-structure.md) | [Home](../README.md) | **Weiter:** [Loot-Wirtschaft im Detail >>](04-loot-economy.md)
