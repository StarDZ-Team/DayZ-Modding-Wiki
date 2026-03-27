# Kapitel 9.8: Performance-Optimierung

[Home](../README.md) | [<< Zurueck: Persistenz](07-persistence.md) | [Weiter: Zugriffskontrolle >>](09-access-control.md)

---

> **Zusammenfassung:** Server-Performance in DayZ laesst sich auf drei Dinge zurueckfuehren: Item-Anzahl, dynamische Events und Mod-/Spielerlast. Dieses Kapitel behandelt die spezifischen Einstellungen, die wichtig sind, wie Sie Probleme diagnostizieren und welche Hardware tatsaechlich hilft -- alles basierend auf realen Community-Daten aus ueber 400 Discord-Berichten ueber FPS-Einbrueche, Lag und Desync.

---

## Inhaltsverzeichnis

- [Was die Server-Performance beeinflusst](#was-die-server-performance-beeinflusst)
- [globals.xml-Optimierung](#globalsxml-optimierung)
- [Wirtschafts-Optimierung fuer Performance](#wirtschafts-optimierung-fuer-performance)
- [cfgeconomycore.xml Logging](#cfgeconomycorexml-logging)
- [serverDZ.cfg Performance-Einstellungen](#serverdzycfg-performance-einstellungen)
- [Mod-Performance-Auswirkungen](#mod-performance-auswirkungen)
- [Hardware-Empfehlungen](#hardware-empfehlungen)
- [Server-Gesundheit ueberwachen](#server-gesundheit-ueberwachen)
- [Haeufige Performance-Fehler](#haeufige-performance-fehler)

---

## Was die Server-Performance beeinflusst

Aus Community-Daten (ueber 400 Discord-Erwaehnungen von FPS/Performance/Lag/Desync) sind die drei groessten Performance-Faktoren:

1. **Item-Anzahl** -- hohe `nominal`-Werte in `types.xml` bedeuten, dass die Zentralwirtschaft mehr Objekte pro Zyklus verfolgt und verarbeitet. Dies ist durchweg die Hauptursache fuer serverseitigen Lag.
2. **Event-Spawning** -- zu viele aktive dynamische Events (Fahrzeuge, Tiere, Heliabstuerze) in `events.xml` verbrauchen Spawn-/Aufraeumzyklen und Entitaets-Slots.
3. **Spieleranzahl + Mod-Anzahl** -- jeder verbundene Spieler generiert Entitaets-Updates, und jeder Mod fuegt Script-Klassen hinzu, die die Engine jeden Tick kompilieren und ausfuehren muss.

Die Server-Spielschleife laeuft mit einer festen Tickrate von 30 FPS. Wenn der Server keine 30 FPS halten kann, erleben Spieler Desync -- Rubberbanding, verzoegertes Item-Aufheben und Treffer-Registrierungsfehler. Unter 15 Server-FPS wird das Spiel unspielbar.

---

## globals.xml-Optimierung

Dies sind die Vanilla-Standardwerte fuer die Parameter, die die Performance direkt beeinflussen:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### Was jeder Wert steuert

| Parameter | Standard | Performance-Auswirkung |
|-----------|----------|------------------------|
| `ZombieMaxCount` | 1000 | Obergrenze fuer gesamte Infizierte auf dem Server. Jeder Zombie fuehrt KI-Pfadfindung aus. Eine Senkung auf 500-700 verbessert die Server-FPS auf bevoelkerten Servern spuerbar. |
| `AnimalMaxCount` | 200 | Obergrenze fuer Tiere. Tiere haben einfachere KI als Zombies, verbrauchen aber trotzdem Tick-Zeit. Senken Sie auf 100, wenn FPS-Probleme auftreten. |
| `ZoneSpawnDist` | 300 | Entfernung in Metern, ab der Zombie-Zonen um Spieler aktiviert werden. Eine Senkung auf 200 bedeutet weniger gleichzeitig aktive Zonen. |
| `SpawnInitial` | 1200 | Anzahl der Items, die die CE beim ersten Start spawnt. Hoehere Werte bedeuten eine laengere initiale Ladezeit. Beeinflusst nicht die Steady-State-Performance. |
| `CleanupLifetimeDefault` | 45 | Standard-Aufraeumzeit in Sekunden fuer Items ohne spezifische Lebensdauer. Niedrigere Werte bedeuten schnellere Aufraeumzyklen, aber haeufigere CE-Verarbeitung. |

**Empfohlenes Performance-Profil** (fuer Server, die ueber 40 Spielern kaempfen):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Wirtschafts-Optimierung fuer Performance

Die Zentralwirtschaft fuehrt eine kontinuierliche Schleife aus, die jeden Item-Typ gegen seine `nominal`/`min`-Ziele prueft. Mehr Item-Typen mit hoeheren Nominalwerten bedeuten mehr Arbeit pro Zyklus.

### Nominalwerte reduzieren

Jedes Item in `types.xml` mit `nominal > 0` wird von der CE verfolgt. Wenn Sie 2000 Item-Typen mit einem durchschnittlichen Nominal von 20 haben, verwaltet die CE 40.000 Objekte. Reduzieren Sie die Nominalwerte durchgaengig, um diese Zahl zu senken:

- Gaengige Zivilistengegenstande: von 15-40 auf 10-25 senken
- Waffen: niedrig halten (Vanilla liegt bereits bei 2-10)
- Kleidungsvarianten: erwaegen Sie, Farbvarianten zu deaktivieren, die Sie nicht benoetigen (`nominal=0`)

### Dynamische Events reduzieren

In `events.xml` spawnt und ueberwacht jedes aktive Event Entitaetsgruppen. Senken Sie den `nominal`-Wert bei Fahrzeug- und Tier-Events, oder setzen Sie `<active>0</active>` bei Events, die Sie nicht benoetigen.

### Leerlaufmodus verwenden

Wenn keine Spieler verbunden sind, kann die CE komplett pausieren:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` bedeutet, der Server geht 60 Sekunden nach der Trennung des letzten Spielers in den Leerlaufmodus. `IdleModeStartup=1` bedeutet, der Server startet im Leerlaufmodus und aktiviert die CE erst, wenn der erste Spieler sich verbindet. Dies verhindert, dass der Server Spawn-Zyklen durchlaeuft, waehrend er leer ist.

### Respawn-Rate anpassen

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Diese steuern, wie viele Items und Item-Typen die CE pro Zyklus verarbeitet. Niedrigere Werte reduzieren die CE-Last pro Tick, verlangsamen aber das Loot-Respawning. Die Vanilla-Standardwerte oben sind bereits konservativ.

---

## cfgeconomycore.xml Logging

Aktivieren Sie CE-Diagnose-Logs voruebergehend, um Zykluszeiten zu messen und Engpaesse zu identifizieren. In Ihrer `cfgeconomycore.xml`:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Fuer die Diagnose setzen Sie `log_ce_statistics` auf `"true"`. Dies gibt CE-Zykluszeiten in das Server-RPT-Log aus. Suchen Sie nach Zeilen, die zeigen, wie lange jeder CE-Zyklus dauert -- wenn Zyklen 1000ms ueberschreiten, ist die Wirtschaft ueberlastet.

Setzen Sie `log_ce_lootspawn` und `log_ce_lootcleanup` auf `"true"`, um zu sehen, welche Item-Typen am haeufigsten spawnen und aufgeraeumt werden. Dies sind Ihre Kandidaten fuer eine Nominal-Reduzierung.

**Deaktivieren Sie das Logging nach der Diagnose.** Log-Schreibvorgaenge selbst verbrauchen I/O und koennen die Performance verschlechtern, wenn sie dauerhaft aktiviert bleiben.

---

## serverDZ.cfg Performance-Einstellungen

Die Haupt-Server-Konfigurationsdatei hat begrenzte performancebezogene Optionen:

| Einstellung | Auswirkung |
|-------------|------------|
| `maxPlayers` | Senken Sie dies, wenn der Server kaempft. Jeder Spieler erzeugt Netzwerkverkehr und Entitaets-Updates. Von 60 auf 40 Spieler zu gehen kann 5-10 Server-FPS zurueckgewinnen. |
| `instanceId` | Bestimmt den `storage_1/`-Pfad. Keine Performance-Einstellung, aber wenn Ihr Speicher auf einer langsamen Festplatte liegt, beeinflusst es die Persistenz-I/O. |

**Was Sie nicht aendern koennen:** Die Server-Tickrate ist fest auf 30 FPS. Es gibt keine Einstellung, um sie zu erhoehen oder zu senken. Wenn der Server keine 30 FPS halten kann, laeuft er einfach langsamer.

---

## Mod-Performance-Auswirkungen

Jeder Mod fuegt Script-Klassen hinzu, die die Engine beim Start kompiliert und jeden Tick ausfuehrt. Die Auswirkung variiert dramatisch je nach Mod-Qualitaet:

- **Inhalts-Only-Mods** (Waffen, Kleidung, Gebaeude) fuegen Item-Typen hinzu, aber minimalen Script-Overhead. Ihre Kosten liegen im CE-Tracking, nicht in der Tick-Verarbeitung.
- **Script-intensive Mods** mit `OnUpdate()`- oder `OnTick()`-Schleifen fuehren Code jeden Server-Frame aus. Schlecht optimierte Schleifen in diesen Mods sind die haeufigste Ursache fuer modbedingten Lag.
- **Haendler-/Wirtschaftsmods**, die grosse Inventare verwalten, fuegen persistente Objekte hinzu, die die Engine verfolgen muss.

### Richtlinien

- Fuegen Sie Mods schrittweise hinzu. Testen Sie die Server-FPS nach jeder Hinzufuegung, nicht nachdem Sie 10 auf einmal hinzugefuegt haben.
- Ueberwachen Sie die Server-FPS mit Admin-Tools oder RPT-Log-Ausgabe nach dem Hinzufuegen neuer Mods.
- Wenn ein Mod Probleme verursacht, pruefen Sie seinen Quellcode auf teure Pro-Frame-Operationen.

Community-Konsens: "Items (types) und Event-Spawning sind am anspruchsvollsten -- Mods, die Tausende von types.xml-Eintraegen hinzufuegen, schaden mehr als Mods, die komplexe Scripts hinzufuegen."

---

## Hardware-Empfehlungen

DayZ-Server-Spiellogik ist **single-threaded**. Multi-Core-CPUs helfen beim OS-Overhead und Netzwerk-I/O, aber die Haupt-Spielschleife laeuft auf einem Kern.

| Komponente | Empfehlung | Warum |
|------------|------------|-------|
| **CPU** | Hoechste Single-Thread-Performance, die Sie bekommen koennen. AMD 5600X oder besser. | Spielschleife ist single-threaded. Taktfrequenz und IPC sind wichtiger als Kernanzahl. |
| **RAM** | 8 GB Minimum, 12-16 GB fuer stark gemodde Server | Mods und grosse Karten verbrauchen Speicher. Speichermangel verursacht Stottern. |
| **Speicher** | SSD erforderlich | `storage_1/`-Persistenz-I/O ist konstant. HDD verursacht Haker waehrend der Speicherzyklen. |
| **Netzwerk** | 100 Mbit/s+ mit niedriger Latenz | Bandbreite ist weniger wichtig als Ping-Stabilitaet fuer Desync-Vermeidung. |

Community-Tipp: "OVH bietet ein gutes Preis-Leistungs-Verhaeltnis -- etwa 60 USD fuer eine dedizierte 5600X-Maschine, die 60-Slot-Modded-Server bewaeltigt."

Vermeiden Sie Shared/VPS-Hosting fuer bevoelkerte Server. Das Noisy-Neighbor-Problem auf geteilter Hardware verursacht unvorhersehbare FPS-Einbrueche, die von Ihrer Seite aus nicht diagnostiziert werden koennen.

---

## Server-Gesundheit ueberwachen

### Server-FPS

Pruefen Sie das RPT-Log auf Zeilen, die Server-FPS enthalten. Ein gesunder Server haelt konstant 30 FPS. Warnschwellen:

| Server-FPS | Status |
|------------|--------|
| 25-30 | Normal. Geringfuegige Schwankungen sind bei schwerem Kampf oder Neustarts zu erwarten. |
| 15-25 | Beeintraechtigt. Spieler bemerken Desync bei Item-Interaktionen und Kampf. |
| Unter 15 | Kritisch. Rubberbanding, fehlgeschlagene Aktionen, Trefferregistrierung defekt. |

### CE-Zyklus-Warnungen

Mit aktiviertem `log_ce_statistics` achten Sie auf CE-Zykluszeiten. Normal ist unter 500ms. Wenn Zyklen regelmaessig 1000ms ueberschreiten, ist Ihre Wirtschaft zu schwer.

### Speicherwachstum

Ueberwachen Sie die Groesse von `storage_1/`. Unkontrolliertes Wachstum deutet auf Persistenz-Aufblaehung hin -- zu viele platzierte Objekte, Zelte oder Verstecke, die sich ansammeln. Regelmaessige Server-Wipes oder das Reduzieren von `FlagRefreshMaxDuration` in `globals.xml` helfen, dies zu kontrollieren.

### Spielerberichte

Desync-Berichte von Spielern sind Ihr zuverlaessigster Echtzeit-Indikator. Wenn mehrere Spieler gleichzeitig Rubberbanding melden, ist die Server-FPS unter 15 gefallen.

---

## Haeufige Performance-Fehler

### Nominalwerte zu hoch

Jedes Item auf `nominal=50` zu setzen, weil "mehr Loot Spass macht", erzeugt Zehntausende verfolgter Objekte. Die CE verbringt ihren gesamten Zyklus mit Item-Verwaltung statt mit dem Spielbetrieb. Beginnen Sie mit Vanilla-Nominalwerten und erhoehen Sie selektiv.

### Zu viele Fahrzeug-Events

Fahrzeuge sind teure Entitaeten mit Physiksimulation, Anbauteil-Verfolgung und Persistenz. Vanilla spawnt insgesamt etwa 50 Fahrzeuge. Server mit ueber 150 Fahrzeugen erleben erhebliche FPS-Verluste.

### 30+ Mods ohne Testen betreiben

Jeder Mod ist fuer sich allein in Ordnung. Der kumulative Effekt von 30+ Mods -- Tausende zusaetzlicher Types, Dutzende Pro-Frame-Scripts und erhoehter Speicherdruck -- kann die Server-FPS um 50% oder mehr senken. Fuegen Sie Mods in Gruppen von 3-5 hinzu und testen Sie nach jeder Gruppe.

### Server nie neustarten

Einige Mods haben Speicherlecks, die sich ueber die Zeit ansammeln. Planen Sie automatische Neustarts alle 4-6 Stunden. Die meisten Server-Hosting-Panels unterstuetzen dies. Auch gut geschriebene Mods profitieren von periodischen Neustarts, da die Speicherfragmentierung der Engine ueber lange Sitzungen zunimmt.

### Speicher-Aufblaehung ignorieren

Ein `storage_1/`-Ordner, der auf mehrere Gigabyte anwaechst, verlangsamt jeden Persistenzzyklus. Wipen oder beschneiden Sie ihn regelmaessig, besonders wenn Sie Basisbau ohne Verfallslimits erlauben.

### Logging dauerhaft aktiviert lassen

CE-Diagnose-Logging, Script-Debug-Logging und Admin-Tool-Logging schreiben alle jeden Tick auf die Festplatte. Aktivieren Sie sie zur Diagnose, dann deaktivieren Sie sie. Dauerhaftes ausfuehrliches Logging auf einem ausgelasteten Server kann allein 1-2 FPS kosten.

---

[Home](../README.md) | [<< Zurueck: Persistenz](07-persistence.md) | [Weiter: Zugriffskontrolle >>](09-access-control.md)
