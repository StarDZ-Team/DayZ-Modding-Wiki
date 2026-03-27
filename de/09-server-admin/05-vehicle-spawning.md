# Kapitel 9.5: Fahrzeug- & Dynamic-Event-Spawning

[Home](../README.md) | [<< Zurueck: Loot-Wirtschaft](04-loot-economy.md) | [Weiter: Spieler-Spawning >>](06-player-spawning.md)

---

> **Zusammenfassung:** Fahrzeuge und dynamische Events (Heliabstuerze, Konvois, Polizeiwagen) verwenden NICHT `types.xml`. Sie nutzen ein separates Drei-Dateien-System: `events.xml` definiert, was und wie viel spawnt, `cfgeventspawns.xml` definiert wo, und `cfgeventgroups.xml` definiert gruppierte Formationen. Dieses Kapitel behandelt alle drei Dateien mit realen Vanilla-Werten.

---

## Inhaltsverzeichnis

- [Wie Fahrzeug-Spawning funktioniert](#wie-fahrzeug-spawning-funktioniert)
- [events.xml Fahrzeug-Eintraege](#eventsxml-fahrzeug-eintraege)
- [Fahrzeug-Event-Feldreferenz](#fahrzeug-event-feldreferenz)
- [cfgeventspawns.xml -- Spawn-Positionen](#cfgeventspawnsxml----spawn-positionen)
- [Heliabsturz-Events](#heliabsturz-events)
- [Militaerkonvoi](#militaerkonvoi)
- [Polizeiwagen](#polizeiwagen)
- [cfgeventgroups.xml -- Gruppierte Spawns](#cfgeventgroupsxml----gruppierte-spawns)
- [cfgeconomycore.xml Fahrzeug-Root-Klasse](#cfgeconomycorexml-fahrzeug-root-klasse)
- [Haeufige Fehler](#haeufige-fehler)

---

## Wie Fahrzeug-Spawning funktioniert

Fahrzeuge werden **nicht** in `types.xml` definiert. Wenn Sie eine Fahrzeugklasse zu `types.xml` hinzufuegen, wird sie nicht spawnen. Fahrzeuge verwenden eine dedizierte Drei-Dateien-Pipeline:

1. **`events.xml`** -- Definiert jedes Fahrzeug-Event: wie viele auf der Karte existieren sollen (nominal), welche Varianten spawnen koennen (children), und Verhaltens-Flags wie Lebensdauer und Sicherheitsradius.

2. **`cfgeventspawns.xml`** -- Definiert die physischen Weltpositionen, an denen Fahrzeug-Events Entitaeten platzieren koennen. Jeder Eventname wird einer Liste von `<pos>`-Eintraegen mit x-, z-Koordinaten und Winkel zugeordnet.

3. **`cfgeventgroups.xml`** -- Definiert gruppierte Spawns, bei denen mehrere Objekte zusammen mit relativen Positionsoffsets spawnen (z.B. Zugwracks).

Die CE liest `events.xml`, waehlt ein Event aus, das gespawnt werden muss, sucht passende Positionen in `cfgeventspawns.xml`, waehlt zufaellig eine aus, die die `saferadius`- und `distanceradius`-Einschraenkungen erfuellt, und spawnt dann eine zufaellig ausgewaehlte Kind-Entitaet an dieser Position.

Alle drei Dateien befinden sich in `mpmissions/<Ihre_Mission>/db/`.

---

## events.xml Fahrzeug-Eintraege

Jeder Vanilla-Fahrzeugtyp hat seinen eigenen Event-Eintrag. Hier sind alle mit realen Werten:

### Zivil-Limousine

```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

### Alle Vanilla-Fahrzeug-Events

Alle Fahrzeug-Events verwenden dieselbe Struktur wie die Limousine oben. Nur die Werte unterscheiden sich:

| Eventname | Nominal | Min | Max | Lifetime | Kinder (Varianten) |
|-----------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Hatchback02-Varianten |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Sedan02-Varianten |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | V3S-LKW-Varianten |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- weniger spawnen |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Boote -- hoechste Anzahl, laengere Lebensdauer |

`VehicleOffroad02` hat einen niedrigeren Nominal (3) als andere Landfahrzeuge (8). `VehicleBoat` hat sowohl den hoechsten Nominal (22) als auch eine laengere Lebensdauer (600 vs 300).

---

## Fahrzeug-Event-Feldreferenz

### Event-Level-Felder

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `name` | string | Event-Bezeichner. Muss mit einem Eintrag in `cfgeventspawns.xml` uebereinstimmen, wenn `position="fixed"`. |
| `nominal` | int | Zielanzahl aktiver Instanzen dieses Events auf der Karte. |
| `min` | int | Die CE versucht nachzuspawnen, wenn die Anzahl darunter faellt. |
| `max` | int | Feste Obergrenze. Die CE wird diese Anzahl niemals ueberschreiten. |
| `lifetime` | int | Sekunden zwischen Respawn-Pruefungen. Fuer Fahrzeuge ist dies NICHT die Persistenz-Lebensdauer des Fahrzeugs -- es ist das Intervall, in dem die CE neu bewertet, ob gespawnt oder aufgeraeumt werden soll. |
| `restock` | int | Minimale Sekunden zwischen Respawn-Versuchen. 0 = naechster Zyklus. |
| `saferadius` | int | Mindestentfernung (Meter) von jedem Spieler, damit das Event spawnt. Verhindert, dass Fahrzeuge vor Spielern erscheinen. |
| `distanceradius` | int | Mindestentfernung (Meter) zwischen zwei Instanzen desselben Events. Verhindert, dass zwei Limousinen nebeneinander spawnen. |
| `cleanupradius` | int | Wenn ein Spieler innerhalb dieser Entfernung (Meter) ist, wird die Event-Entitaet vor Aufraeumung geschuetzt. |

### Flags

| Flag | Werte | Beschreibung |
|------|-------|--------------|
| `deletable` | 0, 1 | Ob die CE diese Event-Entitaet loeschen kann. Fahrzeuge verwenden 0 (nicht von der CE loeschbar). |
| `init_random` | 0, 1 | Anfangspositionen beim ersten Spawn zufaellig verteilen. 0 = feste Positionen aus `cfgeventspawns.xml` verwenden. |
| `remove_damaged` | 0, 1 | Entitaet entfernen, wenn sie zerstoert wird. **Kritisch fuer Fahrzeuge** -- siehe [Haeufige Fehler](#haeufige-fehler). |

### Weitere Felder

| Feld | Werte | Beschreibung |
|------|-------|--------------|
| `position` | `fixed`, `player` | `fixed` = Positionen aus `cfgeventspawns.xml` spawnen. `player` = relativ zu Spielerpositionen spawnen. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max pro Kindtyp erzwungen. `mixed` = min/max ueber alle Kinder geteilt. `custom` = Engine-spezifisches Verhalten. |
| `active` | 0, 1 | Dieses Event aktivieren oder deaktivieren. 0 = das Event wird komplett uebersprungen. |

### Kind-Felder

| Attribut | Beschreibung |
|----------|--------------|
| `type` | Klassenname der zu spawnenden Entitaet. |
| `min` | Mindestinstanzen dieser Variante. |
| `max` | Maximalinstanzen dieser Variante. |
| `lootmin` | Mindestanzahl von Loot-Items, die in/um die Entitaet gespawnt werden. 0 fuer Fahrzeuge (Teile kommen aus `cfgspawnabletypes.xml`). |
| `lootmax` | Maximale Loot-Items. Wird von Heliabstuerzen und dynamischen Events verwendet, nicht von Fahrzeugen. |

---

## cfgeventspawns.xml -- Spawn-Positionen

Diese Datei ordnet Eventnamen Weltkoordinaten zu. Jeder `<event>`-Block enthaelt eine Liste gueltiger Spawn-Positionen fuer diesen Eventtyp. Wenn die CE ein Fahrzeug spawnen muss, waehlt sie eine zufaellige Position aus dieser Liste, die die `saferadius`- und `distanceradius`-Einschraenkungen erfuellt.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... weitere Positionen ... -->
</event>
```

Jede `<pos>` hat drei Attribute:

| Attribut | Beschreibung |
|----------|--------------|
| `x` | Welt-X-Koordinate (Ost-West-Position auf der Karte). |
| `z` | Welt-Z-Koordinate (Nord-Sued-Position auf der Karte). |
| `a` | Winkel in Grad (0-360). Die Richtung, in die das Fahrzeug beim Spawn blickt. |

**Wichtige Regeln:**

- Wenn ein Event keinen passenden `<event>`-Block in `cfgeventspawns.xml` hat, wird es **nicht spawnen**, unabhaengig von der `events.xml`-Konfiguration.
- Sie benoetigen mindestens so viele `<pos>`-Eintraege wie Ihren `nominal`-Wert. Wenn Sie `nominal=8` setzen, aber nur 3 Positionen haben, koennen nur 3 spawnen.
- Positionen sollten auf Strassen oder ebenem Boden liegen. Eine Position in einem Gebaeude oder auf steilem Gelaende fuehrt dazu, dass das Fahrzeug vergraben oder umgekippt spawnt.
- Der `a`-Wert (Winkel) bestimmt die Blickrichtung des Fahrzeugs. Richten Sie ihn an der Strassenrichtung aus fuer natuerlich aussehende Spawns.

---

## Heliabsturz-Events

Helikopterabstuerze sind dynamische Events, die ein Wrack mit Militaer-Loot und umgebenden Infizierten spawnen. Sie verwenden das `<secondary>`-Tag, um umgebende Zombie-Spawns um die Absturzstelle zu definieren.

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>1</min>
    <max>3</max>
    <lifetime>2100</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="15" lootmin="10" max="3" min="1" type="Wreck_UH1Y"/>
    </children>
</event>
```

### Hauptunterschiede zu Fahrzeug-Events

- **`<secondary>InfectedArmy</secondary>`** -- spawnt Militaerzombies um die Absturzstelle. Dieses Tag referenziert eine Infiziertengruppe, die die CE in der Naehe platziert.
- **`lootmin="10"` / `lootmax="15"`** -- das Wrack spawnt mit 10-15 Dynamic-Event-Loot-Items. Dies sind Items mit `deloot="1"` in `types.xml` (Militaerausruestung, seltene Waffen).
- **`lifetime=2100`** -- der Absturz bleibt 35 Minuten bestehen, bevor die CE ihn aufraeumt und einen neuen anderswo spawnt.
- **`saferadius=1000`** -- Abstuerze erscheinen nie innerhalb von 1 km von einem Spieler.
- **`remove_damaged=0`** -- das Wrack ist per Definition bereits "beschaedigt", daher muss dies 0 sein, da es sonst sofort aufgeraeumt wuerde.

---

## Militaerkonvoi

Militaerkonvois sind statische zerstoerte Fahrzeuggruppen, die mit Militaer-Loot und infizierten Wachen spawnen.

```xml
<event name="StaticMilitaryConvoy">
    <nominal>5</nominal>
    <min>3</min>
    <max>5</max>
    <lifetime>1800</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="5" min="3" type="Wreck_V3S"/>
    </children>
</event>
```

Konvois funktionieren identisch zu Heliabstuerzen: Das `<secondary>`-Tag spawnt `InfectedArmy` um die Stelle, und Loot-Items mit `deloot="1"` erscheinen an den Wracks. Mit `nominal=5` existieren bis zu 5 Konvoistellen gleichzeitig auf der Karte. Jeder bleibt 1800 Sekunden (30 Minuten), bevor er an einen neuen Ort wechselt.

---

## Polizeiwagen

Polizeiwagen-Events spawnen zerstoerte Polizeifahrzeuge mit polizeiartigen Infizierten in der Naehe. Sie sind **standardmaessig deaktiviert**.

```xml
<event name="StaticPoliceCar">
    <nominal>10</nominal>
    <min>5</min>
    <max>10</max>
    <lifetime>2500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>200</distanceradius>
    <cleanupradius>100</cleanupradius>
    <secondary>InfectedPoliceHard</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>0</active>
    <children>
        <child lootmax="5" lootmin="3" max="10" min="5" type="Wreck_PoliceCar"/>
    </children>
</event>
```

**`active=0`** bedeutet, dass dieses Event standardmaessig deaktiviert ist -- aendern Sie es auf `1`, um es zu aktivieren. Das `<secondary>InfectedPoliceHard</secondary>`-Tag spawnt Polizeizombies der schweren Variante (widerstandsfaehiger als normale Infizierte). Mit `nominal=10` und `saferadius=500` sind Polizeiwagen zahlreicher, aber weniger wertvoll als Heliabstuerze.

---

## cfgeventgroups.xml -- Gruppierte Spawns

Diese Datei definiert Events, bei denen mehrere Objekte zusammen mit relativen Positionsoffsets spawnen. Die haeufigste Verwendung sind verlassene Zuege.

```xml
<event name="Train_Abandoned_Cherno">
    <children>
        <child type="Land_Train_Wagon_Tanker_Blue" x="0" z="0" a="0"/>
        <child type="Land_Train_Wagon_Box_Brown" x="0" z="15" a="0"/>
        <child type="Land_Train_Wagon_Flatbed_Green" x="0" z="30" a="0"/>
        <child type="Land_Train_Engine_Blue" x="0" z="45" a="0"/>
    </children>
</event>
```

Das erste Kind wird an der Position aus `cfgeventspawns.xml` platziert. Nachfolgende Kinder werden um ihre `x`-, `z`-, `a`-Werte relativ zu diesem Ursprung versetzt. In diesem Beispiel sind die Waggons im 15-Meter-Abstand entlang der Z-Achse aufgereiht.

Jedes `<child>` in einer Gruppe hat:

| Attribut | Beschreibung |
|----------|--------------|
| `type` | Klassenname des zu spawnenden Objekts. |
| `x` | X-Offset in Metern vom Gruppenursprung. |
| `z` | Z-Offset in Metern vom Gruppenursprung. |
| `a` | Winkeloffset in Grad vom Gruppenursprung. |

Das Gruppen-Event selbst benoetigt weiterhin einen passenden Eintrag in `events.xml`, um Nominalwerte, Lebensdauer und Aktivstatus zu steuern.

---

## cfgeconomycore.xml Fahrzeug-Root-Klasse

Damit die CE Fahrzeuge als verfolgbare Entitaeten erkennt, muessen sie eine Root-Klassen-Deklaration in `cfgeconomycore.xml` haben:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** ist die Basisklasse fuer alle Landfahrzeuge in DayZ.
- **`BoatScript`** ist die Basisklasse fuer alle Boote.
- Das `act="car"`-Attribut teilt der CE mit, diese Entitaeten mit fahrzeugspezifischem Verhalten zu behandeln (Persistenz, eventbasiertes Spawning).

Ohne diese Root-Klassen-Eintraege wuerde die CE Fahrzeuginstanzen nicht verfolgen oder verwalten. Wenn Sie ein Mod-Fahrzeug hinzufuegen, das von einer anderen Basisklasse erbt, muessen Sie moeglicherweise dessen Root-Klasse hier hinzufuegen.

---

## Haeufige Fehler

Dies sind die haeufigsten Fahrzeug-Spawn-Probleme, auf die Serveradministratoren stossen.

### Fahrzeuge in types.xml eintragen

**Problem:** Sie fuegen `CivilianSedan` zu `types.xml` mit einem Nominal von 10 hinzu. Keine Limousinen spawnen.

**Loesung:** Entfernen Sie das Fahrzeug aus `types.xml`. Fuegen Sie das Fahrzeug-Event in `events.xml` hinzu oder bearbeiten Sie es mit den entsprechenden Kindern, und stellen Sie sicher, dass passende Spawn-Positionen in `cfgeventspawns.xml` existieren. Fahrzeuge verwenden das Eventsystem, nicht das Item-Spawn-System.

### Keine passenden Spawn-Positionen in cfgeventspawns.xml

**Problem:** Sie erstellen ein neues Fahrzeug-Event in `events.xml`, aber das Fahrzeug erscheint nie.

**Loesung:** Fuegen Sie einen passenden `<event name="IhrEventName">`-Block in `cfgeventspawns.xml` mit genuegend `<pos>`-Eintraegen hinzu. Der Event-`name` in beiden Dateien muss exakt uebereinstimmen. Sie benoetigen mindestens so viele Positionen wie Ihren `nominal`-Wert.

### remove_damaged=0 fuer fahrbare Fahrzeuge setzen

**Problem:** Sie setzen `remove_damaged="0"` auf ein Fahrzeug-Event. Mit der Zeit fuellt sich der Server mit zerstoerten Fahrzeugen, die nie despawnen, Spawn-Positionen blockieren und die Performance beeintraechtigen.

**Loesung:** Behalten Sie `remove_damaged="1"` fuer alle fahrbaren Fahrzeuge (Limousinen, LKWs, Schraeghecks, Boote). Dies stellt sicher, dass die CE ein zerstoertes Fahrzeug entfernt und ein frisches spawnt. Setzen Sie `remove_damaged="0"` nur fuer Wrack-Objekte (Heliabstuerze, Konvois), die konstruktionsbedingt bereits beschaedigt sind.

### Vergessen, active=1 zu setzen

**Problem:** Sie konfigurieren ein Fahrzeug-Event, aber es spawnt nie.

**Loesung:** Pruefen Sie das `<active>`-Tag. Wenn es auf `0` gesetzt ist, ist das Event deaktiviert. Einige Vanilla-Events wie `StaticPoliceCar` werden mit `active=0` ausgeliefert. Setzen Sie es auf `1`, um das Spawning zu aktivieren.

### Nicht genug Spawn-Positionen fuer den Nominalwert

**Problem:** Sie setzen `nominal=15` fuer ein Fahrzeug-Event, aber nur 6 Positionen existieren in `cfgeventspawns.xml`. Nur 6 Fahrzeuge spawnen jemals.

**Loesung:** Fuegen Sie mehr `<pos>`-Eintraege hinzu. Als Faustregel sollten Sie mindestens 2-3x Ihren Nominalwert an Positionen haben, um der CE genuegend Optionen zu geben, die `saferadius`- und `distanceradius`-Einschraenkungen zu erfuellen.

### Fahrzeug spawnt in Gebaeuden oder unterirdisch

**Problem:** Ein Fahrzeug spawnt in ein Gebaeude geclippt oder im Gelaende vergraben.

**Loesung:** Ueberpruefen Sie die `<pos>`-Koordinaten in `cfgeventspawns.xml`. Testen Sie Positionen im Spiel mit Admin-Teleport, bevor Sie sie zur Datei hinzufuegen. Positionen sollten auf ebenen Strassen oder offenem Gelaende liegen, und der Winkel (`a`) sollte zur Strassenrichtung ausgerichtet sein.

---

[Home](../README.md) | [<< Zurueck: Loot-Wirtschaft](04-loot-economy.md) | [Weiter: Spieler-Spawning >>](06-player-spawning.md)
