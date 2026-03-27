# Chapter 9.5: Spawnovani vozidel a dynamicke udalosti

[Domu](../README.md) | [<< Predchozi: Lootova ekonomika](04-loot-economy.md) | [Dalsi: Spawnovani hracu >>](06-player-spawning.md)

---

> **Shrnuti:** Vozidla a dynamicke udalosti (helikopterove zriceniny, konvoje, policejni auta) NEPOUZIVAJI `types.xml`. Pouzivaji oddeleny system trí souboru: `events.xml` definuje, co se spawnuje a kolik, `cfgeventspawns.xml` definuje kde a `cfgeventgroups.xml` definuje skupinove formace. Tato kapitola pokryva vsechny tri soubory s realnymi vanilkovymi hodnotami.

---

## Obsah

- [Jak funguje spawnovani vozidel](#jak-funguje-spawnovani-vozidel)
- [Zaznamy vozidel v events.xml](#zaznamy-vozidel-v-eventsxml)
- [Reference poli udalosti vozidel](#reference-poli-udalosti-vozidel)
- [cfgeventspawns.xml -- pozice spawnu](#cfgeventspawnsxml----pozice-spawnu)
- [Udalosti helikopterovych zricenin](#udalosti-helikopterovych-zricenin)
- [Vojensky konvoj](#vojensky-konvoj)
- [Policejni auto](#policejni-auto)
- [cfgeventgroups.xml -- skupinove spawny](#cfgeventgroupsxml----skupinove-spawny)
- [Korenova trida vozidel v cfgeconomycore.xml](#korenova-trida-vozidel-v-cfgeconomycorexml)
- [Caste chyby](#caste-chyby)

---

## Jak funguje spawnovani vozidel

Vozidla **nejsou** definovana v `types.xml`. Pokud pridáte tridu vozidla do `types.xml`, nespawnuje se. Vozidla pouzivaji vyhrazeny system tri souboru:

1. **`events.xml`** -- Definuje kazdou udalost vozidla: kolik jich ma na mape existovat (nominal), ktere varianty se mohou spawnit (children) a flagy chovani jako zivotnost a bezpecny polomer.

2. **`cfgeventspawns.xml`** -- Definuje fyzicke svetove pozice, kde mohou udalosti vozidel umistovat entity. Kazdy nazev udalosti se mapuje na seznam zaznamu `<pos>` s x, z souradnicemi a uhlem.

3. **`cfgeventgroups.xml`** -- Definuje skupinove spawny, kde se vice objektu spawnuje spolecne s relativnimi pozicnimi ofsety (napr. vlakove vraky).

CE precte `events.xml`, vybere udalost, ktera potrebuje spawn, vyhledá odpovidajici pozice v `cfgeventspawns.xml`, vybere nahodne jednu, ktera splnuje omezeni `saferadius` a `distanceradius`, a pote spawnuje nahodne vybranou detskou entitu na teto pozici.

Vsechny tri soubory se nachazi v `mpmissions/<vase_mise>/db/`.

---

## Zaznamy vozidel v events.xml

Kazdy vanilkovy typ vozidla ma svuj vlastni zaznam udalosti. Zde jsou vsechny s realnymi hodnotami:

### Civilni sedan

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

### Vsechny vanilkove udalosti vozidel

Vsechny udalosti vozidel pouzivaji stejnou strukturu jako sedan vyse. Lisi se pouze hodnoty:

| Nazev udalosti | Nominal | Min | Max | Lifetime | Deti (varianty) |
|------------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Varianty Hatchback02 |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Varianty Sedan02 |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | Varianty nakladaku V3S |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- mene spawnu |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Lodě -- nejvyssi pocet, delsi zivotnost |

`VehicleOffroad02` ma nizsi nominal (3) nez ostatni pozemni vozidla (8). `VehicleBoat` ma jak nejvyssi nominal (22), tak delsi zivotnost (600 vs 300).

---

## Reference poli udalosti vozidel

### Pole na urovni udalosti

| Pole | Typ | Popis |
|-------|------|-------------|
| `name` | string | Identifikator udalosti. Musi odpovidat zaznamu v `cfgeventspawns.xml` kdyz `position="fixed"`. |
| `nominal` | int | Cilovy pocet aktivnich instanci teto udalosti na mape. |
| `min` | int | CE se pokusi spawnit vice, kdyz pocet klesne pod tuto hodnotu. |
| `max` | int | Tvrdy horni limit. CE tento pocet nikdy neprekroci. |
| `lifetime` | int | Sekundy mezi kontrolami respawnu. U vozidel toto NENI zivotnost persistence vozidla -- je to interval, ve kterem CE prehodnocuje, zda spawnit nebo vycistit. |
| `restock` | int | Minimalni sekundy mezi pokusy o respawn. 0 = dalsi cyklus. |
| `saferadius` | int | Minimalni vzdalenost (metry) od jakehokoliv hrace pro spawn udalosti. Zabranuje objeveni vozidel pred hraci. |
| `distanceradius` | int | Minimalni vzdalenost (metry) mezi dvema instancemi stejne udalosti. Zabranuje spawnu dvou sedanu vedle sebe. |
| `cleanupradius` | int | Pokud je hrac v teto vzdalenosti (metry), entita udalosti je chranena pred cistenim. |

### Flagy

| Flag | Hodnoty | Popis |
|------|--------|-------------|
| `deletable` | 0, 1 | Zda CE muze smazat entitu teto udalosti. Vozidla pouzivaji 0 (nesmazatelna CE). |
| `init_random` | 0, 1 | Nahodne generovat pocatecni pozice pri prvnim spawnu. 0 = pouzit pevne pozice z `cfgeventspawns.xml`. |
| `remove_damaged` | 0, 1 | Odstranit entitu, kdyz se stane znicenou. **Kriticke pro vozidla** -- viz [Caste chyby](#caste-chyby). |

### Dalsi pole

| Pole | Hodnoty | Popis |
|-------|--------|-------------|
| `position` | `fixed`, `player` | `fixed` = spawnovat na pozicich z `cfgeventspawns.xml`. `player` = spawnovat relativne k pozicim hracu. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max vynuceno pro kazdy detsky typ. `mixed` = min/max sdileno mezi vsemi detmi. `custom` = chovani specificke pro engine. |
| `active` | 0, 1 | Povolit nebo zakazat tuto udalost. 0 = udalost je zcela preskocena. |

### Pole deti

| Atribut | Popis |
|-----------|-------------|
| `type` | Nazev tridy entity ke spawnu. |
| `min` | Minimalni pocet instanci teto varianty. |
| `max` | Maximalni pocet instanci teto varianty. |
| `lootmin` | Minimalni pocet lootovych predmetu spawnovaných uvnitr/kolem entity. 0 pro vozidla (dily pochazi z `cfgspawnabletypes.xml`). |
| `lootmax` | Maximalni pocet lootovych predmetu. Pouziva se helikopterovymi zriceninami a dynamickymi udalostmi, ne vozidly. |

---

## cfgeventspawns.xml -- pozice spawnu

Tento soubor mapuje nazvy udalosti na svetove souradnice. Kazdy blok `<event>` obsahuje seznam platnych pozic spawnu pro tento typ udalosti. Kdyz CE potrebuje spawnit vozidlo, vybere nahodnou pozici ze seznamu, ktera splnuje omezeni `saferadius` a `distanceradius`.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... dalsi pozice ... -->
</event>
```

Kazdy `<pos>` ma tri atributy:

| Atribut | Popis |
|-----------|-------------|
| `x` | Svetova souradnice X (pozice vychod-zapad na mape). |
| `z` | Svetova souradnice Z (pozice sever-jih na mape). |
| `a` | Uhel ve stupnich (0-360). Smer, kterym vozidlo smeri pri spawnu. |

**Klicova pravidla:**

- Pokud udalost nema odpovidajici blok `<event>` v `cfgeventspawns.xml`, **nespawnuje se** bez ohledu na konfiguraci `events.xml`.
- Potrebujete alespon tolik zaznamu `<pos>` jako je vase hodnota `nominal`. Pokud nastavite `nominal=8`, ale mate pouze 3 pozice, spawnuji se pouze 3.
- Pozice by mely byt na silnicich nebo rovnem terenu. Pozice uvnitr budovy nebo na strmen terenu zpusobi, ze se vozidlo spawnuje zahrabane nebo prevracene.
- Hodnota `a` (uhel) urcuje smer, kterym vozidlo smeri. Zarovnejte ji se smerem silnice pro prirozene vypadajici spawny.

---

## Udalosti helikopterovych zricenin

Helikopterove zriceniny jsou dynamicke udalosti, ktere spawnuji vrak s vojenskym lootem a okolnimi nakazenymi. Pouzivaji tag `<secondary>` pro definovani ambientnich spawnu zombie kolem mista zriceniny.

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

### Klicove rozdily od udalosti vozidel

- **`<secondary>InfectedArmy</secondary>`** -- spawnuje vojenske zombie kolem mista zriceniny. Tento tag odkazuje na skupinu infikovaných spawnu, kterou CE umisti do blizkosti.
- **`lootmin="10"` / `lootmax="15"`** -- vrak se spawnuje s 10-15 lootovymi predmety dynamicke udalosti. To jsou predmety oznacene `deloot="1"` v `types.xml` (vojenská vybava, vzacne zbrane).
- **`lifetime=2100`** -- zricenina pretrva 35 minut pred vycistenim CE a spawnem nove jinde.
- **`saferadius=1000`** -- zriceniny se nikdy neobjevi do 1 km od hrace.
- **`remove_damaged=0`** -- vrak je jiz "poskozeny" ze sve podstaty, takze toto musi byt 0, jinak by byl okamzite vycisten.

---

## Vojensky konvoj

Vojenske konvoje jsou staticke skupiny zničených vozidel, ktere se spawnuji s vojenskym lootem a nakazenymi strazci.

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

Konvoje funguji identicky jako helikopterove zriceniny: tag `<secondary>` spawnuje `InfectedArmy` kolem mista a lootove predmety s `deloot="1"` se objevi na vracich. S `nominal=5` muze na mape soucasne existovat az 5 mist konvoju. Kazdy trva 1800 sekund (30 minut) pred presunenim na novou lokaci.

---

## Policejni auto

Udalosti policejnich aut spawnuji znicena policejni vozidla s nakazenymi policejniho typu v blizkosti. Ve vychozim stavu jsou **zakazany**.

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

**`active=0`** znamena, ze tato udalost je ve vychozim stavu zakazana -- zmente na `1` pro jeji povoleni. Tag `<secondary>InfectedPoliceHard</secondary>` spawnuje hard-variantu policejnich zombie (odolnejsich nez standardni nakazeni). S `nominal=10` a `saferadius=500` jsou policejni auta pocetnejsi, ale mene hodnotna nez helikopterove zriceniny.

---

## cfgeventgroups.xml -- skupinove spawny

Tento soubor definuje udalosti, kde se vice objektu spawnuje spolecne s relativnimi pozicnimi ofsety. Nejcastejsi pouziti jsou opustene vlaky.

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

Prvni dite je umisteno na pozici z `cfgeventspawns.xml`. Nasledujici deti jsou odsazeny svymi hodnotami `x`, `z`, `a` relativne k tomu puvodu. V tomto prikladu jsou vlakove vozy rozmisteny 15 metru od sebe podél osy z.

Kazdy `<child>` ve skupine ma:

| Atribut | Popis |
|-----------|-------------|
| `type` | Nazev tridy objektu ke spawnu. |
| `x` | Odsazeni X v metrech od puvodu skupiny. |
| `z` | Odsazeni Z v metrech od puvodu skupiny. |
| `a` | Odsazeni uhlu ve stupnich od puvodu skupiny. |

Skupinova udalost sama stale potrebuje odpovidajici zaznam v `events.xml` pro rizeni nominalnich poctu, zivotnosti a aktivniho stavu.

---

## Korenova trida vozidel v cfgeconomycore.xml

Aby CE rozpoznala vozidla jako sledovatelne entity, musi mit deklaraci korenove tridy v `cfgeconomycore.xml`:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** je zakladni trida pro vsechna pozemni vozidla v DayZ.
- **`BoatScript`** je zakladni trida pro vsechny lodě.
- Atribut `act="car"` rika CE, aby s temito entitami zachazela s chovanim specifickym pro vozidla (persistence, spawnovani zalozene na udalostech).

Bez techto zaznamu korenovych trid by CE nesledovala ani nespravovala instance vozidel. Pokud pridáte modovane vozidlo, ktere dedi z jine zakladni tridy, mozná budete muset pridat jeho korenovou tridu sem.

---

## Caste chyby

Toto jsou nejcastejsi problemy se spawnovanim vozidel, se kterymi se serverovi admini setkavaji.

### Umisteni vozidel do types.xml

**Problem:** Pridáte `CivilianSedan` do `types.xml` s nominalem 10. Zadne sedany se nespawnuji.

**Reseni:** Odstrante vozidlo z `types.xml`. Pridejte nebo upravte udalost vozidla v `events.xml` s odpovidajicimi detmi a zajistete, ze odpovidajici pozice spawnu existuji v `cfgeventspawns.xml`. Vozidla pouzivaji system udalosti, ne system spawnu predmetu.

### Zadne odpovidajici pozice spawnu v cfgeventspawns.xml

**Problem:** Vytvorite novou udalost vozidla v `events.xml`, ale vozidlo se nikdy neobjevi.

**Reseni:** Pridejte odpovidajici blok `<event name="NazevVasiUdalosti">` v `cfgeventspawns.xml` s dostatecnym poctem zaznamu `<pos>`. Nazev `name` udalosti v obou souborech musi presne odpovidat. Potrebujete alespon tolik pozic jako je vase hodnota `nominal`.

### Nastaveni remove_damaged=0 pro jizdni vozidla

**Problem:** Nastavite `remove_damaged="0"` na udalosti vozidla. Postupem casu se server zaplni zniceným vozidly, ktera nikdy nezmizi, coz blokuje pozice spawnu a snizuje vykon.

**Reseni:** Ponechte `remove_damaged="1"` pro vsechna jizdni vozidla (sedany, nakladaky, hatchbacky, lodě). Tím se zajistí, ze kdyz je vozidlo zniceno, CE ho odstrani a spawnuje nove. Nastavte `remove_damaged="0"` pouze pro objekty vraku (helikopterove zriceniny, konvoje), ktere jsou poskozene uz ze sve podstaty.

### Zapomenuti nastavit active=1

**Problem:** Nakonfigurujete udalost vozidla, ale nikdy se nespawnuje.

**Reseni:** Zkontrolujte tag `<active>`. Pokud je nastaven na `0`, udalost je zakazana. Nekteré vanilkove udalosti jako `StaticPoliceCar` jsou dodavany s `active=0`. Nastavte na `1` pro povoleni spawnovani.

### Nedostatek pozic spawnu pro nominal

**Problem:** Nastavite `nominal=15` pro udalost vozidla, ale v `cfgeventspawns.xml` existuje pouze 6 pozic. Spawnuje se pouze 6 vozidel.

**Reseni:** Pridejte vice zaznamu `<pos>`. Jako pravidlo zahrnte alespon 2-3x vasi hodnotu nominal v pozicich, abyste dali CE dostatek moznosti ke splneni omezeni `saferadius` a `distanceradius`.

### Vozidlo se spawnuje uvnitr budov nebo pod zemi

**Problem:** Vozidlo se spawnuje zaborene do budovy nebo zahrabane v terenu.

**Reseni:** Zkontrolujte souradnice `<pos>` v `cfgeventspawns.xml`. Otestujte pozice ve hre pomoci adminskehho teleportu pred jejich pridanim do souboru. Pozice by mely byt na rovných silnicich nebo otevrenem terenu a uhel (`a`) by mel byt zarovnan se smerem silnice.

---

[Domu](../README.md) | [<< Predchozi: Lootova ekonomika](04-loot-economy.md) | [Dalsi: Spawnovani hracu >>](06-player-spawning.md)
