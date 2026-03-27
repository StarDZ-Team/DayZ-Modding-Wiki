# Chapter 9.5: Jármű és dinamikus esemény spawnolás

[Kezdőlap](../README.md) | [<< Előző: Zsákmánygazdaság](04-loot-economy.md) | [Következő: Játékos spawnolás >>](06-player-spawning.md)

---

> **Összefoglaló:** A járművek és dinamikus események (helikopter roncsok, konvojok, rendőrautók) NEM használják a `types.xml` fájlt. Egy külön háromfájlos rendszert használnak: az `events.xml` definiálja, mi jelenik meg és hány, a `cfgeventspawns.xml` definiálja, hol, és a `cfgeventgroups.xml` definiálja a csoportos formációkat. Ez a fejezet mindhárom fájlt tárgyalja valós vanilla értékekkel.

---

## Tartalomjegyzék

- [Hogyan működik a jármű spawnolás](#hogyan-működik-a-jármű-spawnolás)
- [events.xml jármű bejegyzések](#eventsxml-jármű-bejegyzések)
- [Jármű esemény mező referencia](#jármű-esemény-mező-referencia)
- [cfgeventspawns.xml -- Spawn pozíciók](#cfgeventspawnsxml----spawn-pozíciók)
- [Helikopter roncs események](#helikopter-roncs-események)
- [Katonai konvoj](#katonai-konvoj)
- [Rendőrautó](#rendőrautó)
- [cfgeventgroups.xml -- Csoportos spawnok](#cfgeventgroupsxml----csoportos-spawnok)
- [cfgeconomycore.xml jármű gyökér osztály](#cfgeconomycorexml-jármű-gyökér-osztály)
- [Gyakori hibák](#gyakori-hibák)

---

## Hogyan működik a jármű spawnolás

A járművek **nincsenek** a `types.xml`-ben definiálva. Ha jármű osztályt adsz a `types.xml`-hez, az nem fog megjelenni. A járművek egy dedikált háromfájlos csővezetéket használnak:

1. **`events.xml`** -- Definiálja az egyes jármű eseményeket: hány legyen a térképen (nominal), mely változatok jelenhetnek meg (gyerekek), és viselkedési jelzők mint élettartam és biztonsági sugár.

2. **`cfgeventspawns.xml`** -- Definiálja a fizikai világ pozíciókat, ahova a jármű események elhelyezhetik az entitásokat. Minden eseménynév `<pos>` bejegyzések listájára mutat x, z koordinátákkal és szöggel.

3. **`cfgeventgroups.xml`** -- Definiálja a csoportos spawnokat, ahol több objektum jelenik meg együtt relatív pozíció eltolással (pl. vonat roncsok).

A CE olvassa az `events.xml`-t, kiválaszt egy spawnolásra szoruló eseményt, megkeresi a megfelelő pozíciókat a `cfgeventspawns.xml`-ben, véletlenszerűen kiválaszt egyet, amely kielégíti a `saferadius` és `distanceradius` feltételeket, majd spawnol egy véletlenszerűen kiválasztott gyerek entitást azon a pozíción.

Mindhárom fájl a `mpmissions/<a_te_küldetésed>/db/` mappában található.

---

## events.xml jármű bejegyzések

Minden vanilla jármű típusnak saját esemény bejegyzése van. Íme az összesítés valós értékekkel:

### Civilian Sedan

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

### Összes vanilla jármű esemény

Minden jármű esemény ugyanazt a struktúrát használja, mint a fenti Sedan. Csak az értékek különböznek:

| Esemény név | Nominal | Min | Max | Lifetime | Gyerekek (változatok) |
|-------------|---------|-----|-----|----------|----------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Hatchback02 változatok |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Sedan02 változatok |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | V3S teherautó változatok |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- kevesebb jelenik meg |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Csónakok -- legmagasabb szám, hosszabb élettartam |

A `VehicleOffroad02` alacsonyabb nominal értékkel (3) rendelkezik, mint más szárazföldi járművek (8). A `VehicleBoat`-nak van a legmagasabb nominal értéke (22) és hosszabb élettartama (600 vs 300).

---

## Jármű esemény mező referencia

### Esemény szintű mezők

| Mező | Típus | Leírás |
|------|-------|--------|
| `name` | string | Esemény azonosító. Meg kell egyeznie egy bejegyzéssel a `cfgeventspawns.xml`-ben, ha `position="fixed"`. |
| `nominal` | int | Aktív példányok célszáma ezen eseményből a térképen. |
| `min` | int | A CE megpróbál többet spawnolni, ha a szám ez alá esik. |
| `max` | int | Kemény felső korlát. A CE soha nem lépi túl ezt a számot. |
| `lifetime` | int | Újraspawn ellenőrzések közötti másodpercek. Járműveknél ez NEM a jármű perzisztencia élettartama -- ez az intervallum, amelynél a CE újraértékeli, hogy spawnoljon-e vagy takarítson. |
| `restock` | int | Minimális másodpercek újraspawn kísérletek között. 0 = következő ciklus. |
| `saferadius` | int | Minimális távolság (méterben) bármely játékostól az esemény spawnolásához. Megakadályozza, hogy járművek a játékosok előtt jelenjenek meg. |
| `distanceradius` | int | Minimális távolság (méterben) ugyanazon esemény két példánya között. Megakadályozza, hogy két szedán egymás mellett jelenjen meg. |
| `cleanupradius` | int | Ha egy játékos ezen a távolságon (méterben) belül van, az esemény entitás védett a takarítástól. |

### Jelzők

| Jelző | Értékek | Leírás |
|-------|---------|--------|
| `deletable` | 0, 1 | A CE törölheti-e ezt az esemény entitást. Járművek 0-t használnak (a CE nem törölheti). |
| `init_random` | 0, 1 | Kezdeti pozíciók randomizálása az első spawnoláskor. 0 = rögzített pozíciók használata a `cfgeventspawns.xml`-ből. |
| `remove_damaged` | 0, 1 | Az entitás eltávolítása, ha tönkremegy. **Kritikus járműveknél** -- lásd [Gyakori hibák](#gyakori-hibák). |

### Egyéb mezők

| Mező | Értékek | Leírás |
|------|---------|--------|
| `position` | `fixed`, `player` | `fixed` = pozíciók a `cfgeventspawns.xml`-ből. `player` = spawnolás játékos pozíciókhoz képest. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max gyerek típusonként. `mixed` = min/max az összes gyerek között megosztva. `custom` = motor-specifikus viselkedés. |
| `active` | 0, 1 | Az esemény engedélyezése vagy letiltása. 0 = az esemény teljesen kihagyásra kerül. |

### Gyerek mezők

| Attribútum | Leírás |
|------------|--------|
| `type` | A spawnolni kívánt entitás osztályneve. |
| `min` | Minimális példányok ebből a változatból. |
| `max` | Maximális példányok ebből a változatból. |
| `lootmin` | Az entitáson belül/körül spawnolt zsákmány tárgyak minimális száma. 0 járműveknél (az alkatrészek a `cfgspawnabletypes.xml`-ből jönnek). |
| `lootmax` | Maximális zsákmány tárgyak. Helikopter roncsok és dinamikus események használják, járművek nem. |

---

## cfgeventspawns.xml -- Spawn pozíciók

Ez a fájl eseményneveket világ koordinátákhoz rendel. Minden `<event>` blokk érvényes spawn pozíciók listáját tartalmazza az adott eseménytípushoz. Amikor a CE-nek spawnolnia kell egy járművet, véletlenszerűen választ egy pozíciót ebből a listából, amely kielégíti a `saferadius` és `distanceradius` feltételeket.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... további pozíciók ... -->
</event>
```

Minden `<pos>` három attribútummal rendelkezik:

| Attribútum | Leírás |
|------------|--------|
| `x` | Világ X koordináta (kelet-nyugat pozíció a térképen). |
| `z` | Világ Z koordináta (észak-dél pozíció a térképen). |
| `a` | Szög fokban (0-360). Az irány, amerre a jármű néz spawnoláskor. |

**Kulcs szabályok:**

- Ha egy eseménynek nincs megfelelő `<event>` blokkja a `cfgeventspawns.xml`-ben, **nem fog megjelenni** az `events.xml` konfigurációtól függetlenül.
- Legalább annyi `<pos>` bejegyzésre van szükséged, mint a `nominal` értéked. Ha `nominal=8`-at állítasz, de csak 3 pozíciód van, csak 3 jelenhet meg.
- A pozícióknak utakon vagy sík talajon kell lenniük. Egy épületen belüli vagy meredek terepen lévő pozíció miatt a jármű eltemetve vagy felborulva jelenik meg.
- Az `a` (szög) érték határozza meg a jármű nézési irányát. Igazítsd az útirányhoz a természetes megjelenésért.

---

## Helikopter roncs események

A helikopter roncsok dinamikus események, amelyek egy roncsot spawnolnak katonai zsákmánnyal és környező fertőzöttekkel. A `<secondary>` taget használják a roncs körüli zombi spawnok definiálásához.

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

### Kulcs különbségek a jármű eseményekhez képest

- **`<secondary>InfectedArmy</secondary>`** -- katonai zombikat spawnol a roncs körül. Ez a tag egy fertőzött spawn csoportra hivatkozik, amelyet a CE a közelben elhelyez.
- **`lootmin="10"` / `lootmax="15"`** -- a roncs 10-15 dinamikus esemény zsákmány tárggyal jelenik meg. Ezek a `types.xml`-ben `deloot="1"` jelzővel ellátott tárgyak (katonai felszerelés, ritka fegyverek).
- **`lifetime=2100`** -- a roncs 35 percig marad meg, mielőtt a CE megtisztítja és máshol spawnol egy újat.
- **`saferadius=1000`** -- a roncsok soha nem jelennek meg 1 km-en belül egy játékostól.
- **`remove_damaged=0`** -- a roncs definíció szerint már "sérült", tehát ennek 0-nak kell lennie, különben azonnal megtisztulna.

---

## Katonai konvoj

A katonai konvojok statikus roncsolt jármű csoportok, amelyek katonai zsákmánnyal és fertőzött őrökkel jelennek meg.

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

A konvojok azonosan működnek a helikopter roncsokkal: a `<secondary>` tag `InfectedArmy`-t spawnol a helyszín körül, és a `deloot="1"` jelzővel ellátott zsákmány tárgyak a roncsokra kerülnek. `nominal=5` mellett egyszerre legfeljebb 5 konvoj helyszín létezik a térképen. Mindegyik 1800 másodpercig (30 perc) tart, mielőtt új helyre ciklizál.

---

## Rendőrautó

A rendőrautó események roncsolt rendőr járműveket spawnolnak rendőr típusú fertőzöttekkel a közelben. Alapértelmezés szerint **le vannak tiltva**.

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

**`active=0`** azt jelenti, hogy ez az esemény alapértelmezés szerint le van tiltva -- módosítsd `1`-re az engedélyezéséhez. Az `<secondary>InfectedPoliceHard</secondary>` tag nehéz változatú rendőr zombikat spawnol (erősebbek a szokásos fertőzötteknél). `nominal=10` és `saferadius=500` mellett a rendőrautók számosabbak, de kevésbé értékesek, mint a helikopter roncsok.

---

## cfgeventgroups.xml -- Csoportos spawnok

Ez a fájl olyan eseményeket definiál, ahol több objektum jelenik meg együtt relatív pozíció eltolással. A leggyakoribb felhasználás az elhagyott vonatok.

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

Az első gyerek a `cfgeventspawns.xml` pozíciójára kerül. A további gyerekek az `x`, `z`, `a` értékeikkel eltolva az eredeti ponthoz képest. Ebben a példában a vagonok 15 méteres távolságra vannak egymástól a z-tengely mentén.

Minden csoportbeli `<child>` elemnek van:

| Attribútum | Leírás |
|------------|--------|
| `type` | A spawnolni kívánt objektum osztályneve. |
| `x` | X eltolás méterben a csoport origójától. |
| `z` | Z eltolás méterben a csoport origójától. |
| `a` | Szög eltolás fokban a csoport origójától. |

A csoport eseménynek magának továbbra is szüksége van egy megfelelő bejegyzésre az `events.xml`-ben a nominal számok, élettartam és aktív állapot szabályozásához.

---

## cfgeconomycore.xml jármű gyökér osztály

Ahhoz, hogy a CE felismerje a járműveket nyomon követhető entitásokként, rendelkezniük kell gyökér osztály deklarációval a `cfgeconomycore.xml`-ben:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- A **`CarScript`** a DayZ összes szárazföldi járművének alaposztálya.
- A **`BoatScript`** az összes csónak alaposztálya.
- Az `act="car"` attribútum utasítja a CE-t, hogy jármű-specifikus viselkedéssel kezelje ezeket az entitásokat (perzisztencia, esemény-alapú spawnolás).

Ezen gyökér osztály bejegyzések nélkül a CE nem követné vagy kezelné a jármű példányokat. Ha olyan moddolt járművet adsz hozzá, amely más alaposztályból öröklődik, lehet, hogy hozzá kell adnod a gyökér osztályát ide.

---

## Gyakori hibák

Ezek a leggyakoribb jármű spawnolási problémák, amelyekkel szerver adminok találkoznak.

### Járművek hozzáadása a types.xml-hez

**Probléma:** Hozzáadod a `CivilianSedan`-t a `types.xml`-hez 10-es nominal értékkel. Egyetlen szedán sem jelenik meg.

**Javítás:** Távolítsd el a járművet a `types.xml`-ből. Add hozzá vagy szerkeszd a jármű eseményt az `events.xml`-ben a megfelelő gyerekekkel, és győződj meg róla, hogy megfelelő spawn pozíciók léteznek a `cfgeventspawns.xml`-ben. A járművek az esemény rendszert használják, nem a tárgy spawn rendszert.

### Nincs megfelelő spawn pozíció a cfgeventspawns.xml-ben

**Probléma:** Létrehozol egy új jármű eseményt az `events.xml`-ben, de a jármű soha nem jelenik meg.

**Javítás:** Adj hozzá egy megfelelő `<event name="AzEseményNeved">` blokkot a `cfgeventspawns.xml`-ben elegendő `<pos>` bejegyzéssel. Az esemény `name` attribútumnak mindkét fájlban pontosan egyeznie kell. Legalább annyi pozícióra van szükséged, mint a `nominal` értéked.

### remove_damaged=0 beállítás vezethető járművekhez

**Probléma:** `remove_damaged="0"`-t állítasz egy jármű eseményhez. Idővel a szerver megtelik roncsolt járművekkel, amelyek soha nem tűnnek el, blokkolják a spawn pozíciókat és rontják a teljesítményt.

**Javítás:** Tartsd a `remove_damaged="1"` beállítást minden vezethető járműhöz (szedánok, teherautók, ferdehátúak, csónakok). Ez biztosítja, hogy amikor egy jármű megsemmisül, a CE eltávolítja és friss példányt spawnol. Csak roncs objektumokhoz (helikopter roncsok, konvojok) állítsd `remove_damaged="0"`-ra, amelyek eleve sérültek.

### Elfelejtett active=1 beállítás

**Probléma:** Konfigurálsz egy jármű eseményt, de az soha nem jelenik meg.

**Javítás:** Ellenőrizd az `<active>` taget. Ha `0`-ra van állítva, az esemény le van tiltva. Néhány vanilla esemény, mint a `StaticPoliceCar`, `active=0`-val szállít. Állítsd `1`-re a spawnolás engedélyezéséhez.

### Nem elég spawn pozíció a nominal számhoz

**Probléma:** `nominal=15`-öt állítasz egy jármű eseményhez, de csak 6 pozíció létezik a `cfgeventspawns.xml`-ben. Csak 6 jármű jelenik meg.

**Javítás:** Adj hozzá több `<pos>` bejegyzést. Szabály szerint adj meg legalább 2-3x annyi pozíciót, mint a nominal értéked, hogy a CE-nek elég lehetősége legyen a `saferadius` és `distanceradius` feltételek kielégítéséhez.

### Jármű épületen belül vagy föld alatt jelenik meg

**Probléma:** Egy jármű épületbe beékelve vagy a terepbe temetve jelenik meg.

**Javítás:** Ellenőrizd a `<pos>` koordinátákat a `cfgeventspawns.xml`-ben. Teszteld a pozíciókat játékon belül admin teleporttal, mielőtt hozzáadod a fájlhoz. A pozícióknak sík utakon vagy nyílt terepen kell lenniük, és a szögnek (`a`) igazodnia kell az út irányához.

---

[Kezdőlap](../README.md) | [<< Előző: Zsákmánygazdaság](04-loot-economy.md) | [Következő: Játékos spawnolás >>](06-player-spawning.md)
