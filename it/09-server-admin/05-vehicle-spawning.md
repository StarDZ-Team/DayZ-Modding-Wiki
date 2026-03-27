# Chapter 9.5: Spawn di Veicoli ed Eventi Dinamici

[Home](../README.md) | [<< Precedente: Economia del Loot](04-loot-economy.md) | [Successivo: Spawn dei Giocatori >>](06-player-spawning.md)

---

> **Riepilogo:** I veicoli e gli eventi dinamici (relitti di elicotteri, convogli, auto della polizia) NON usano `types.xml`. Utilizzano un sistema separato a tre file: `events.xml` definisce cosa appare e in che quantita, `cfgeventspawns.xml` definisce dove, e `cfgeventgroups.xml` definisce le formazioni raggruppate. Questo capitolo copre tutti e tre i file con valori vanilla reali.

---

## Indice

- [Come funziona lo spawn dei veicoli](#come-funziona-lo-spawn-dei-veicoli)
- [Voci dei veicoli in events.xml](#voci-dei-veicoli-in-eventsxml)
- [Riferimento dei campi degli eventi veicolo](#riferimento-dei-campi-degli-eventi-veicolo)
- [cfgeventspawns.xml -- Posizioni di spawn](#cfgeventspawnsxml----posizioni-di-spawn)
- [Eventi relitti di elicotteri](#eventi-relitti-di-elicotteri)
- [Convoglio militare](#convoglio-militare)
- [Auto della polizia](#auto-della-polizia)
- [cfgeventgroups.xml -- Spawn raggruppati](#cfgeventgroupsxml----spawn-raggruppati)
- [Classe root veicolo in cfgeconomycore.xml](#classe-root-veicolo-in-cfgeconomycorexml)
- [Errori comuni](#errori-comuni)

---

## Come funziona lo spawn dei veicoli

I veicoli **non** sono definiti in `types.xml`. Se aggiungi una classe veicolo a `types.xml`, non apparira. I veicoli usano una pipeline dedicata a tre file:

1. **`events.xml`** -- Definisce ogni evento veicolo: quanti dovrebbero esistere sulla mappa (nominal), quali varianti possono apparire (figli) e flag di comportamento come lifetime e raggio di sicurezza.

2. **`cfgeventspawns.xml`** -- Definisce le posizioni fisiche nel mondo dove gli eventi veicolo possono piazzare le entita. Ogni nome di evento corrisponde a una lista di voci `<pos>` con coordinate x, z e angolo.

3. **`cfgeventgroups.xml`** -- Definisce gli spawn raggruppati dove piu oggetti appaiono insieme con offset posizionali relativi (ad esempio, relitti di treni).

La CE legge `events.xml`, seleziona un evento che necessita di spawn, cerca le posizioni corrispondenti in `cfgeventspawns.xml`, ne seleziona una a caso che soddisfa i vincoli di `saferadius` e `distanceradius`, poi genera un'entita figlio selezionata casualmente in quella posizione.

Tutti e tre i file si trovano in `mpmissions/<tua_missione>/db/`.

---

## Voci dei veicoli in events.xml

Ogni tipo di veicolo vanilla ha la propria voce evento. Ecco tutti con i valori reali:

### Berlina civile

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

### Tutti gli eventi veicolo vanilla

Tutti gli eventi veicolo usano la stessa struttura della Berlina sopra. Solo i valori differiscono:

| Nome evento | Nominal | Min | Max | Lifetime | Figli (varianti) |
|-------------|---------|-----|-----|----------|-------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Varianti Hatchback02 |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Varianti Sedan02 |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | Varianti camion V3S |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- ne appaiono meno |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Barche -- conteggio piu alto, lifetime piu lungo |

`VehicleOffroad02` ha un nominal piu basso (3) rispetto agli altri veicoli terrestri (8). `VehicleBoat` ha sia il nominal piu alto (22) che un lifetime piu lungo (600 vs 300).

---

## Riferimento dei campi degli eventi veicolo

### Campi a livello di evento

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `name` | stringa | Identificatore dell'evento. Deve corrispondere a una voce in `cfgeventspawns.xml` quando `position="fixed"`. |
| `nominal` | int | Numero target di istanze attive di questo evento sulla mappa. |
| `min` | int | La CE tentera di generarne altri quando il conteggio scende sotto questo valore. |
| `max` | int | Limite massimo rigido. La CE non superera mai questo conteggio. |
| `lifetime` | int | Secondi tra i controlli di respawn. Per i veicoli, questo NON e il lifetime di persistenza del veicolo -- e l'intervallo al quale la CE rivaluta se generare o ripulire. |
| `restock` | int | Secondi minimi tra i tentativi di respawn. 0 = prossimo ciclo. |
| `saferadius` | int | Distanza minima (metri) da qualsiasi giocatore perche l'evento possa apparire. Impedisce ai veicoli di materializzarsi davanti ai giocatori. |
| `distanceradius` | int | Distanza minima (metri) tra due istanze dello stesso evento. Impedisce a due berline di apparire una accanto all'altra. |
| `cleanupradius` | int | Se un giocatore e entro questa distanza (metri), l'entita dell'evento e protetta dalla pulizia. |

### Flags

| Flag | Valori | Descrizione |
|------|--------|-------------|
| `deletable` | 0, 1 | Se la CE puo eliminare questa entita evento. I veicoli usano 0 (non eliminabile dalla CE). |
| `init_random` | 0, 1 | Randomizza le posizioni iniziali al primo spawn. 0 = usa posizioni fisse da `cfgeventspawns.xml`. |
| `remove_damaged` | 0, 1 | Rimuovi l'entita quando diventa rovinata. **Critico per i veicoli** -- vedi [Errori comuni](#errori-comuni). |

### Altri campi

| Campo | Valori | Descrizione |
|-------|--------|-------------|
| `position` | `fixed`, `player` | `fixed` = appare nelle posizioni da `cfgeventspawns.xml`. `player` = appare in relazione alle posizioni dei giocatori. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max applicati per tipo di figlio. `mixed` = min/max condivisi tra tutti i figli. `custom` = comportamento specifico del motore. |
| `active` | 0, 1 | Abilita o disabilita questo evento. 0 = l'evento viene saltato completamente. |

### Campi dei figli

| Attributo | Descrizione |
|-----------|-------------|
| `type` | Nome della classe dell'entita da generare. |
| `min` | Numero minimo di istanze di questa variante. |
| `max` | Numero massimo di istanze di questa variante. |
| `lootmin` | Numero minimo di oggetti loot generati dentro/intorno all'entita. 0 per i veicoli (i pezzi vengono da `cfgspawnabletypes.xml`). |
| `lootmax` | Numero massimo di oggetti loot. Usato dai relitti di elicotteri e dagli eventi dinamici, non dai veicoli. |

---

## cfgeventspawns.xml -- Posizioni di spawn

Questo file mappa i nomi degli eventi alle coordinate nel mondo. Ogni blocco `<event>` contiene una lista di posizioni di spawn valide per quel tipo di evento. Quando la CE deve generare un veicolo, sceglie una posizione casuale da questa lista che soddisfa i vincoli di `saferadius` e `distanceradius`.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... altre posizioni ... -->
</event>
```

Ogni `<pos>` ha tre attributi:

| Attributo | Descrizione |
|-----------|-------------|
| `x` | Coordinata X nel mondo (posizione est-ovest sulla mappa). |
| `z` | Coordinata Z nel mondo (posizione nord-sud sulla mappa). |
| `a` | Angolo in gradi (0-360). La direzione che il veicolo ha quando appare. |

**Regole chiave:**

- Se un evento non ha un blocco `<event>` corrispondente in `cfgeventspawns.xml`, **non apparira** indipendentemente dalla configurazione in `events.xml`.
- Hai bisogno di almeno tante voci `<pos>` quanto il tuo valore `nominal`. Se imposti `nominal=8` ma hai solo 3 posizioni, solo 3 potranno apparire.
- Le posizioni dovrebbero essere su strade o terreno piatto. Una posizione dentro un edificio o su terreno ripido causera la generazione del veicolo sotterrato o capovolto.
- Il valore `a` (angolo) determina la direzione del veicolo. Allinealo con la direzione della strada per spawn dall'aspetto naturale.

---

## Eventi relitti di elicotteri

I relitti di elicotteri sono eventi dinamici che generano un relitto con loot militare e infetti circostanti. Usano il tag `<secondary>` per definire gli spawn di zombie ambientali intorno al sito del crash.

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

### Differenze chiave dagli eventi veicolo

- **`<secondary>InfectedArmy</secondary>`** -- genera zombie militari intorno al sito del crash. Questo tag fa riferimento a un gruppo di spawn di infetti che la CE piazza nelle vicinanze.
- **`lootmin="10"` / `lootmax="15"`** -- il relitto appare con 10-15 oggetti loot di eventi dinamici. Questi sono oggetti con il flag `deloot="1"` in `types.xml` (equipaggiamento militare, armi rare).
- **`lifetime=2100`** -- il crash persiste per 35 minuti prima che la CE lo ripulisca e ne generi uno nuovo altrove.
- **`saferadius=1000`** -- i crash non appaiono mai entro 1 km da un giocatore.
- **`remove_damaged=0`** -- il relitto e gia "danneggiato" per definizione, quindi questo deve essere 0 altrimenti verrebbe immediatamente ripulito.

---

## Convoglio militare

I convogli militari sono gruppi statici di veicoli distrutti che appaiono con loot militare e guardie infette.

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

I convogli funzionano in modo identico ai relitti di elicotteri: il tag `<secondary>` genera `InfectedArmy` intorno al sito, e gli oggetti loot con `deloot="1"` appaiono sui relitti. Con `nominal=5`, fino a 5 siti di convoglio esistono sulla mappa contemporaneamente. Ciascuno dura 1800 secondi (30 minuti) prima di ruotare verso una nuova posizione.

---

## Auto della polizia

Gli eventi auto della polizia generano veicoli della polizia distrutti con infetti di tipo poliziotto nelle vicinanze. Sono **disabilitati per impostazione predefinita**.

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

**`active=0`** significa che questo evento e disabilitato per impostazione predefinita -- cambia a `1` per abilitarlo. Il tag `<secondary>InfectedPoliceHard</secondary>` genera varianti hard di zombie poliziotto (piu resistenti degli infetti standard). Con `nominal=10` e `saferadius=500`, le auto della polizia sono piu numerose ma meno preziose dei relitti di elicotteri.

---

## cfgeventgroups.xml -- Spawn raggruppati

Questo file definisce eventi dove piu oggetti appaiono insieme con offset posizionali relativi. L'uso piu comune sono i treni abbandonati.

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

Il primo figlio viene piazzato nella posizione da `cfgeventspawns.xml`. I figli successivi sono spostati in base ai loro valori `x`, `z`, `a` relativi a quel punto di origine. In questo esempio, i vagoni del treno sono distanziati di 15 metri lungo l'asse z.

Ogni `<child>` in un gruppo ha:

| Attributo | Descrizione |
|-----------|-------------|
| `type` | Nome della classe dell'oggetto da generare. |
| `x` | Offset X in metri dal punto di origine del gruppo. |
| `z` | Offset Z in metri dal punto di origine del gruppo. |
| `a` | Offset dell'angolo in gradi dal punto di origine del gruppo. |

L'evento del gruppo stesso ha comunque bisogno di una voce corrispondente in `events.xml` per controllare i conteggi nominal, il lifetime e lo stato di attivazione.

---

## Classe root veicolo in cfgeconomycore.xml

Affinche la CE riconosca i veicoli come entita tracciabili, devono avere una dichiarazione di classe root in `cfgeconomycore.xml`:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** e la classe base per tutti i veicoli terrestri in DayZ.
- **`BoatScript`** e la classe base per tutte le barche.
- L'attributo `act="car"` dice alla CE di trattare queste entita con un comportamento specifico per i veicoli (persistenza, spawn basato su eventi).

Senza queste voci di classe root, la CE non traccerebbe ne gestirebbe le istanze dei veicoli. Se aggiungi un veicolo moddato che eredita da una classe base diversa, potresti dover aggiungere la sua classe root qui.

---

## Errori comuni

Questi sono i problemi di spawn dei veicoli piu frequenti riscontrati dagli amministratori di server.

### Inserire veicoli in types.xml

**Problema:** Aggiungi `CivilianSedan` a `types.xml` con un nominal di 10. Nessuna berlina appare.

**Soluzione:** Rimuovi il veicolo da `types.xml`. Aggiungi o modifica l'evento veicolo in `events.xml` con i figli appropriati, e assicurati che esistano posizioni di spawn corrispondenti in `cfgeventspawns.xml`. I veicoli usano il sistema degli eventi, non il sistema di spawn degli oggetti.

### Nessuna posizione di spawn corrispondente in cfgeventspawns.xml

**Problema:** Crei un nuovo evento veicolo in `events.xml` ma il veicolo non appare mai.

**Soluzione:** Aggiungi un blocco `<event name="NomeTuoEvento">` corrispondente in `cfgeventspawns.xml` con sufficienti voci `<pos>`. Il `name` dell'evento in entrambi i file deve corrispondere esattamente. Hai bisogno di almeno tante posizioni quanto il tuo valore `nominal`.

### Impostare remove_damaged=0 per veicoli guidabili

**Problema:** Imposti `remove_damaged="0"` su un evento veicolo. Col tempo, il server si riempie di veicoli distrutti che non scompaiono mai, bloccando le posizioni di spawn e degradando le prestazioni.

**Soluzione:** Mantieni `remove_damaged="1"` per tutti i veicoli guidabili (berline, camion, hatchback, barche). Questo assicura che quando un veicolo viene distrutto, la CE lo rimuove e ne genera uno nuovo. Imposta `remove_damaged="0"` solo per gli oggetti relitto (crash di elicotteri, convogli) che sono gia danneggiati per design.

### Dimenticare di impostare active=1

**Problema:** Configuri un evento veicolo ma non appare mai.

**Soluzione:** Controlla il tag `<active>`. Se e impostato a `0`, l'evento e disabilitato. Alcuni eventi vanilla come `StaticPoliceCar` vengono distribuiti con `active=0`. Impostalo a `1` per abilitare lo spawn.

### Non abbastanza posizioni di spawn per il conteggio nominal

**Problema:** Imposti `nominal=15` per un evento veicolo ma esistono solo 6 posizioni in `cfgeventspawns.xml`. Solo 6 veicoli appaiono.

**Soluzione:** Aggiungi piu voci `<pos>`. Come regola, includi almeno 2-3 volte il tuo valore nominal in posizioni per dare alla CE abbastanza opzioni per soddisfare i vincoli di `saferadius` e `distanceradius`.

### Il veicolo appare dentro edifici o sottoterra

**Problema:** Un veicolo appare incastrato in un edificio o sepolto nel terreno.

**Soluzione:** Rivedi le coordinate `<pos>` in `cfgeventspawns.xml`. Testa le posizioni nel gioco usando il teletrasporto admin prima di aggiungerle al file. Le posizioni dovrebbero essere su strade piatte o terreno aperto, e l'angolo (`a`) dovrebbe allinearsi con la direzione della strada.

---

[Home](../README.md) | [<< Precedente: Economia del Loot](04-loot-economy.md) | [Successivo: Spawn dei Giocatori >>](06-player-spawning.md)
