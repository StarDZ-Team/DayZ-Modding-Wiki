# Kapitel 9.7: Weltzustand & Persistenz

[Home](../README.md) | [<< Zurueck: Spieler-Spawning](06-player-spawning.md) | [Weiter: Performance-Optimierung >>](08-performance.md)

DayZ-Persistenz haelt die Welt zwischen Neustarts am Leben. Das Verstaendnis ihrer Funktionsweise ermoeglicht Ihnen, Basen zu verwalten, Wipes zu planen und Datenbeschaedigungen zu vermeiden.

## Inhaltsverzeichnis

- [Wie Persistenz funktioniert](#wie-persistenz-funktioniert)
- [Das storage_1/-Verzeichnis](#das-storage_1-verzeichnis)
- [globals.xml Persistenz-Parameter](#globalsxml-persistenz-parameter)
- [Territorium-Fahnen-System](#territorium-fahnen-system)
- [Hoarder-Items](#hoarder-items)
- [cfggameplay.json Persistenz-Einstellungen](#cfggameplayjson-persistenz-einstellungen)
- [Server-Wipe-Verfahren](#server-wipe-verfahren)
- [Backup-Strategie](#backup-strategie)
- [Haeufige Fehler](#haeufige-fehler)

---

## Wie Persistenz funktioniert

DayZ speichert den Weltzustand im `storage_1/`-Verzeichnis innerhalb Ihres Server-Profilordners. Der Ablauf ist einfach:

1. Der Server speichert den Weltzustand periodisch (standardmaessig etwa alle 30 Minuten) und beim ordnungsgemaessen Herunterfahren.
2. Beim Neustart liest der Server `storage_1/` und stellt alle persistierten Objekte wieder her -- Fahrzeuge, Basen, Zelte, Faesser, Spielerinventare.
3. Items ohne Persistenz (der meiste Bodenloot) werden bei jedem Neustart von der Zentralwirtschaft neu generiert.

Wenn `storage_1/` beim Start nicht existiert, erstellt der Server eine frische Welt ohne Spielerdaten und ohne gebaute Strukturen.

---

## Das storage_1/-Verzeichnis

Ihr Serverprofil enthaelt `storage_1/` mit diesen Unterverzeichnissen und Dateien:

| Pfad | Inhalt |
|------|--------|
| `data/` | Binaerdateien mit Weltobjekten -- Basisteile, platzierte Items, Fahrzeugpositionen |
| `players/` | Pro-Spieler-**.save**-Dateien, indiziert nach SteamID64. Jede Datei speichert Position, Inventar, Gesundheit, Statuseffekte |
| `snapshot/` | Weltzustand-Snapshots, die waehrend Speichervorgaengen verwendet werden |
| `events.bin` / `events.xy` | Dynamischer Event-Zustand -- verfolgt Heliabsturz-Orte, Konvoi-Positionen und andere gespawnte Events |

Der `data/`-Ordner macht den Grossteil der Persistenz aus. Er enthaelt serialisierte Objektdaten, die der Server beim Booten liest, um die Welt zu rekonstruieren.

---

## globals.xml Persistenz-Parameter

Die Datei **globals.xml** (in Ihrem Missionsordner) steuert Aufraeumtimer und Fahnenverhalten. Dies sind die persistenzrelevanten Werte:

```xml
<!-- Territorium-Fahnen-Auffrischung -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 Tage (Sekunden) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 Tage (Sekunden) -->

<!-- Aufraeumtimer -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Standard-Aufraeumung (Sekunden) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Toter Spielerkoerper: 1 Stunde -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Totes Tier: 20 Minuten -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Toter Zombie: 5,5 Minuten -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Zerstoertes Item: 5,5 Minuten -->

<!-- Aufraeumverhalten -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Max Items pro Aufraeumzyklus -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Aufraeumung innerhalb von 100m eines Spielers ueberspringen -->
```

Der `CleanupAvoidance`-Wert verhindert, dass der Server Objekte in der Naehe aktiver Spieler despawnt. Wenn ein toter Koerper innerhalb von 100 Metern eines Spielers liegt, bleibt er, bis der Spieler sich entfernt oder der Timer zurueckgesetzt wird.

---

## Territorium-Fahnen-System

Territorium-Fahnen sind der Kern der Basenpersistenz in DayZ. So wirken die beiden Schluessewerte zusammen:

- **FlagRefreshFrequency** (`432000` Sekunden = 5 Tage) -- Wie oft Sie mit Ihrer Fahne interagieren muessen, um sie aktiv zu halten. Gehen Sie zur Fahne und verwenden Sie die "Auffrischen"-Aktion.
- **FlagRefreshMaxDuration** (`3456000` Sekunden = 40 Tage) -- Die maximale angesammelte Schutzzeit. Jede Auffrischung fuegt bis zu FlagRefreshFrequency an Zeit hinzu, aber die Gesamtzeit kann dieses Maximum nicht ueberschreiten.

Wenn der Timer einer Fahne ablaeuft:

1. Die Fahne selbst wird aufraeumungsberechtigt.
2. Alle an dieser Fahne befestigten Basisteile verlieren ihren Persistenzschutz.
3. Beim naechsten Aufraeumzyklus beginnen ungeschuetzte Teile zu despawnen.

Wenn Sie FlagRefreshFrequency senken, muessen Spieler ihre Basen haeufiger besuchen. Wenn Sie FlagRefreshMaxDuration erhoehen, ueberleben Basen laenger zwischen Besuchen. Passen Sie beide Werte gemeinsam an den Spielstil Ihres Servers an.

---

## Hoarder-Items

In **cfgspawnabletypes.xml** sind bestimmte Container mit `<hoarder/>` markiert. Dies kennzeichnet sie als versteckfaehige Items, die auf spielerspezifische Speicherlimits in der Zentralwirtschaft angerechnet werden.

Die Vanilla-Hoarder-Items sind:

| Item | Typ |
|------|-----|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Lagerfaesser |
| CarTent, LargeTent, MediumTent, PartyTent | Zelte |
| SeaChest | Unterwasserlager |
| SmallProtectorCase | Kleine abschliessbare Kiste |
| UndergroundStash | Vergrabenes Versteck |
| WoodenCrate | Herstellbare Lagerkiste |

Beispiel aus **cfgspawnabletypes.xml**:

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

Der Server verfolgt, wie viele Hoarder-Items jeder Spieler platziert hat. Wenn das Limit erreicht ist, schlagen neue Platzierungen entweder fehl oder das aelteste Item despawnt (abhaengig von der Serverkonfiguration).

---

## cfggameplay.json Persistenz-Einstellungen

Die Datei **cfggameplay.json** in Ihrem Missionsordner enthaelt Einstellungen, die die Haltbarkeit von Basen und Containern beeinflussen:

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Einstellung | Standard | Auswirkung |
|-------------|----------|------------|
| `disableBaseDamage` | `false` | Bei `true` koennen Basisteile (Waende, Tore, Wachttuerme) nicht beschaedigt werden. Dies deaktiviert effektiv das Raiden. |
| `disableContainerDamage` | `false` | Bei `true` koennen Lagercontainer (Zelte, Faesser, Kisten) keinen Schaden nehmen. Items darin bleiben sicher. |

Beide auf `true` zu setzen erstellt einen PvE-freundlichen Server, auf dem Basen und Lager unzerstoerbar sind. Die meisten PvP-Server belassen beide auf `false`.

---

## Server-Wipe-Verfahren

Sie haben vier Arten von Wipes, die jeweils einen anderen Teil von `storage_1/` betreffen. **Stoppen Sie immer den Server, bevor Sie einen Wipe durchfuehren.**

### Vollstaendiger Wipe

Loeschen Sie den gesamten `storage_1/`-Ordner. Der Server erstellt eine frische Welt beim naechsten Start. Alle Basen, Fahrzeuge, Zelte, Spielerdaten und Event-Zustaende sind weg.

### Wirtschafts-Wipe (Spieler behalten)

Loeschen Sie `storage_1/data/`, aber lassen Sie `storage_1/players/` intakt. Spieler behalten ihre Charaktere und Inventare, aber alle platzierten Objekte (Basen, Zelte, Faesser, Fahrzeuge) werden entfernt.

### Spieler-Wipe (Welt behalten)

Loeschen Sie `storage_1/players/`. Alle Spielercharaktere werden auf frische Spawns zurueckgesetzt. Basen und platzierte Objekte bleiben in der Welt.

### Wetter-/Event-Reset

Loeschen Sie `events.bin` oder `events.xy` aus `storage_1/`. Dies setzt die Positionen dynamischer Events zurueck (Heliabstuerze, Konvois). Der Server generiert beim naechsten Start neue Event-Orte.

---

## Backup-Strategie

Persistenzdaten sind nach Verlust unwiederbringlich. Befolgen Sie diese Praktiken:

- **Backup bei gestopptem Server.** Kopieren Sie den gesamten `storage_1/`-Ordner, waehrend der Server nicht laeuft. Kopieren waehrend der Laufzeit riskiert einen teilweisen oder beschaedigten Zustand.
- **Planen Sie Backups vor Neustarts.** Wenn Sie automatische Neustarts durchfuehren (alle 4-6 Stunden), fuegen Sie Ihrem Neustart-Skript einen Backup-Schritt hinzu, der `storage_1/` kopiert, bevor der Serverprozess startet.
- **Behalten Sie mehrere Generationen.** Rotieren Sie Backups, damit Sie mindestens 3 aktuelle Kopien haben. Wenn Ihr letztes Backup beschaedigt ist, koennen Sie auf ein frueheres zurueckgreifen.
- **Extern speichern.** Kopieren Sie Backups auf ein separates Laufwerk oder in Cloud-Speicher. Ein Festplattenausfall auf dem Serverrechner nimmt Ihre Backups mit, wenn sie auf demselben Laufwerk sind.

Ein minimales Backup-Skript (wird vor dem Serverstart ausgefuehrt):

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Haeufige Fehler

Diese kommen in Server-Admin-Communities immer wieder vor:

| Fehler | Auswirkung | Vermeidung |
|--------|-----------|------------|
| `storage_1/` loeschen, waehrend der Server laeuft | Datenbeschaedigung. Der Server schreibt in Dateien, die nicht mehr existieren, was Abstuerze oder teilweisen Zustand beim naechsten Start verursacht. | Stoppen Sie immer zuerst den Server. |
| Kein Backup vor einem Wipe | Wenn Sie versehentlich den falschen Ordner loeschen oder der Wipe schiefgeht, gibt es keine Wiederherstellung. | Erstellen Sie vor jedem Wipe ein Backup von `storage_1/`. |
| Wetter-Reset mit vollstaendigem Wipe verwechseln | Das Loeschen von `events.xy` setzt nur dynamische Event-Positionen zurueck. Es setzt weder Loot, noch Basen, noch Spieler zurueck. | Wissen Sie, welche Dateien was steuern (siehe die Verzeichnistabelle oben). |
| Fahne nicht rechtzeitig aufgefrischt | Nach 40 Tagen (FlagRefreshMaxDuration) laeuft die Fahne ab und alle angebundenen Basisteile werden aufraeumungsberechtigt. Spieler verlieren ihre gesamte Basis. | Erinnern Sie Spieler an das Auffrischungsintervall. Senken Sie FlagRefreshMaxDuration auf Low-Pop-Servern. |
| globals.xml bearbeiten, waehrend der Server laeuft | Aenderungen werden erst beim Neustart uebernommen. Schlimmer noch, der Server ueberschreibt moeglicherweise Ihre Bearbeitungen beim Herunterfahren. | Bearbeiten Sie Konfigurationsdateien nur bei gestopptem Server. |

---

[Home](../README.md) | [<< Zurueck: Spieler-Spawning](06-player-spawning.md) | [Weiter: Performance-Optimierung >>](08-performance.md)
