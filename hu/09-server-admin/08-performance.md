# Chapter 9.8: Teljesítmény hangolás

[Kezdőlap](../README.md) | [<< Előző: Perzisztencia](07-persistence.md) | [Következő: Hozzáférés vezérlés >>](09-access-control.md)

---

> **Összefoglaló:** A szerver teljesítmény a DayZ-ben három dologra vezethető vissza: tárgyak száma, dinamikus események és mod/játékos terhelés. Ez a fejezet tárgyalja a fontos beállításokat, a problémák diagnosztizálásának módját és azt, hogy milyen hardver segít valójában -- mindezt 400+ Discord jelentésből származó valós közösségi adatok alapján FPS csökkenésekről, lagokról és desync-ről.

---

## Tartalomjegyzék

- [Mi befolyásolja a szerver teljesítményt](#mi-befolyásolja-a-szerver-teljesítményt)
- [globals.xml hangolás](#globalsxml-hangolás)
- [Gazdaság hangolás teljesítményért](#gazdaság-hangolás-teljesítményért)
- [cfgeconomycore.xml naplózás](#cfgeconomycorexml-naplózás)
- [serverDZ.cfg teljesítmény beállítások](#serverdzcfg-teljesítmény-beállítások)
- [Mod teljesítmény hatás](#mod-teljesítmény-hatás)
- [Hardver ajánlások](#hardver-ajánlások)
- [Szerver egészség figyelése](#szerver-egészség-figyelése)
- [Gyakori teljesítmény hibák](#gyakori-teljesítmény-hibák)

---

## Mi befolyásolja a szerver teljesítményt

Közösségi adatok alapján (400+ Discord említés FPS/teljesítmény/lag/desync témában) a három legnagyobb teljesítmény tényező:

1. **Tárgyak száma** -- magas `nominal` értékek a `types.xml`-ben azt jelentik, hogy a Központi Gazdaság több objektumot követ és dolgoz fel minden ciklusban. Ez következetesen az első számú oka a szerver oldali lagnak.
2. **Esemény spawnolás** -- túl sok aktív dinamikus esemény (járművek, állatok, helikopter roncsok) az `events.xml`-ben spawn/takarítási ciklusokat és entitás helyeket fogyaszt.
3. **Játékos szám + mod szám** -- minden csatlakoztatott játékos entitás frissítéseket generál, és minden mod szkript osztályokat ad hozzá, amelyeket a motornak minden tickben le kell fordítania és végrehajtania.

A szerver játékciklus fix 30 FPS tick sebességgel fut. Amikor a szerver nem képes tartani a 30 FPS-t, a játékosok desync-et tapasztalnak -- gumiszalag effektus, késleltetett tárgy felvétel és találat regisztrációs hibák. 15 szerver FPS alatt a játék játszhatatlanná válik.

---

## globals.xml hangolás

Ezek a vanilla alapértékek a teljesítményt közvetlenül befolyásoló paraméterekhez:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### Mit szabályoz minden érték

| Paraméter | Alapértelmezett | Teljesítmény hatás |
|-----------|-----------------|-------------------|
| `ZombieMaxCount` | 1000 | A szerveren egyszerre élő fertőzöttek korlátja. Minden zombi AI útvonalkeresést futtat. 500-700-ra csökkentés észrevehetően javítja a szerver FPS-t népes szervereken. |
| `AnimalMaxCount` | 200 | Állatok korlátja. Az állatoknak egyszerűbb AI-juk van, mint a zombiknak, de még mindig fogyasztanak tick időt. Csökkentsd 100-ra, ha FPS problémákat látsz. |
| `ZoneSpawnDist` | 300 | Távolság méterben, amelynél a zombi zónák aktiválódnak a játékosok körül. 200-ra csökkentés kevesebb egyidejű aktív zónát jelent. |
| `SpawnInitial` | 1200 | Tárgyak száma, amelyet a CE az első indításkor spawnol. Magasabb értékek hosszabb kezdeti betöltést jelentenek. Nem befolyásolja az állandó állapotú teljesítményt. |
| `CleanupLifetimeDefault` | 45 | Alapértelmezett takarítási idő másodpercben specifikus élettartam nélküli tárgyakhoz. Alacsonyabb értékek gyorsabb takarítási ciklusokat, de gyakoribb CE feldolgozást jelentenek. |

**Ajánlott teljesítmény profil** (40 játékos feletti nehézségekkel küzdő szerverekhez):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Gazdaság hangolás teljesítményért

A Központi Gazdaság folyamatos ciklust futtat, minden tárgy típust ellenőrizve a `nominal`/`min` célokkal szemben. Több tárgy típus magasabb nominalokkal több munkát jelent ciklusonként.

### Nominal értékek csökkentése

Minden tárgy a `types.xml`-ben `nominal > 0` értékkel nyomon van követve a CE által. Ha 2000 tárgy típusod van átlagosan 20-as nominallal, a CE 40 000 objektumot kezel. Csökkentsd a nominalokat általánosan ennek a számnak a csökkentéséhez:

- Gyakori civil tárgyak: csökkentsd 15-40-ről 10-25-re
- Fegyverek: tartsd alacsonyan (a vanilla már 2-10)
- Ruházat változatok: fontold meg a nem szükséges szín változatok letiltását (`nominal=0`)

### Dinamikus események csökkentése

Az `events.xml`-ben minden aktív esemény entitás csoportokat spawnol és figyel. Csökkentsd a `nominal` értéket a jármű és állat eseményeknél, vagy állítsd `<active>0</active>`-ra a nem szükséges eseményeket.

### Tétlen mód használata

Ha nincs csatlakoztatott játékos, a CE teljesen szünetelhet:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

Az `IdleModeCountdown=60` azt jelenti, hogy a szerver 60 másodperccel az utolsó játékos lecsatlakozása után tétlen módba lép. Az `IdleModeStartup=1` azt jelenti, hogy a szerver tétlen módban indul és csak az első játékos csatlakozásakor aktiválja a CE-t. Ez megakadályozza, hogy a szerver üresen pörögjön a spawn ciklusokon.

### Újraspawn sebesség hangolása

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Ezek szabályozzák, hány tárgyat és tárgy típust dolgoz fel a CE ciklusonként. Alacsonyabb értékek csökkentik a CE terhelést tickenként, de lassítják a zsákmány újraspawnolást. A fenti vanilla alapértékek már konzervatívak.

---

## cfgeconomycore.xml naplózás

Engedélyezd a CE diagnosztikai naplókat ideiglenesen a ciklus idők méréséhez és a szűk keresztmetszetek azonosításához. A `cfgeconomycore.xml`-ben:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Teljesítmény diagnosztizálásához állítsd a `log_ce_statistics` értéket `"true"`-ra. Ez CE ciklus időzítést ír ki a szerver RPT naplóba. Keresd azokat a sorokat, amelyek megmutatják, mennyi ideig tart minden CE ciklus -- ha a ciklusok meghaladják az 1000 ms-t, a gazdaság túlterhelt.

Állítsd a `log_ce_lootspawn` és `log_ce_lootcleanup` értéket `"true"`-ra, hogy lásd, mely tárgy típusok spawnolnak és tisztulnak meg a leggyakrabban. Ezek a jelöltjeid a nominal csökkentésnek.

**Kapcsold ki a naplózást a diagnózis után.** A napló írások maguk is I/O-t fogyasztanak és ronthatják a teljesítményt, ha tartósan engedélyezve maradnak.

---

## serverDZ.cfg teljesítmény beállítások

A fő szerver konfigurációs fájlnak korlátozott teljesítménnyel kapcsolatos lehetőségei vannak:

| Beállítás | Hatás |
|-----------|-------|
| `maxPlayers` | Csökkentsd, ha a szerver küzd. Minden játékos hálózati forgalmat és entitás frissítéseket generál. 60-ról 40 játékosra csökkentés 5-10 szerver FPS-t nyerhet vissza. |
| `instanceId` | Meghatározza a `storage_1/` elérési útvonalát. Nem teljesítmény beállítás, de ha a tárolód lassú lemezen van, befolyásolja a perzisztencia I/O-t. |

**Amit nem változtathatsz meg:** a szerver tick sebesség fix 30 FPS. Nincs beállítás a növelésére vagy csökkentésére. Ha a szerver nem képes tartani a 30 FPS-t, egyszerűen lassabban fut.

---

## Mod teljesítmény hatás

Minden mod szkript osztályokat ad hozzá, amelyeket a motor indításkor lefordít és minden tickben végrehajt. A hatás drámaian eltér a mod minőségétől függően:

- **Csak tartalmi modok** (fegyverek, ruházat, épületek) tárgy típusokat adnak hozzá, de minimális szkript terhelést. Költségük a CE nyomon követésben van, nem a tick feldolgozásban.
- **Szkript-intenzív modok** `OnUpdate()` vagy `OnTick()` ciklusokkal minden szerver frame-ben futtatnak kódot. Rosszul optimalizált ciklusok ezekben a modokban a mod-okkal kapcsolatos lag leggyakoribb oka.
- **Kereskedő/gazdaság modok**, amelyek nagy inventárokat tartanak fenn, perzisztens objektumokat adnak hozzá, amelyeket a motornak nyomon kell követnie.

### Irányelvek

- Adj hozzá modokat fokozatosan. Teszteld a szerver FPS-t minden hozzáadás után, ne 10 hozzáadása után egyszerre.
- Figyeld a szerver FPS-t admin eszközökkel vagy RPT napló kimenettel új modok hozzáadása után.
- Ha egy mod problémákat okoz, ellenőrizd a forráskódját költséges frame-enkénti műveletek szempontjából.

Közösségi konszenzus: "A tárgyak (types) és esemény spawnolás a legigényesebb -- a modok, amelyek ezernyi types.xml bejegyzést adnak hozzá, jobban ártanak, mint azok, amelyek komplex szkripteket adnak hozzá."

---

## Hardver ajánlások

A DayZ szerver játéklogikája **egymagos**. A többmagos processzorok segítenek az OS overhead-del és hálózati I/O-val, de a fő játékciklus egy magon fut.

| Komponens | Ajánlás | Miért |
|-----------|---------|-------|
| **CPU** | A legmagasabb egymagos teljesítmény, amit elérhetsz. AMD 5600X vagy jobb. | A játékciklus egymagos. Az órajel és az IPC fontosabb, mint a magok száma. |
| **RAM** | Minimum 8 GB, 12-16 GB erősen moddolt szerverekhez | A modok és nagy térképek memóriát fogyasztanak. A kifogyás akadozást okoz. |
| **Tároló** | SSD szükséges | A `storage_1/` perzisztencia I/O állandó. HDD akadozást okoz a mentési ciklusok alatt. |
| **Hálózat** | 100 Mbps+ alacsony késleltetéssel | A sávszélesség kevésbé számít, mint a ping stabilitás a desync megelőzéséhez. |

Közösségi tipp: "Az OVH jó ár-érték arányt kínál -- körülbelül 60 USD egy dedikált 5600X gépért, amely elbírja a 60 slotos moddolt szervereket."

Kerüld a megosztott/VPS hosztingot népes szerverekhez. A megosztott hardveren a zajos szomszéd probléma kiszámíthatatlan FPS csökkenéseket okoz, amelyeket lehetetlen a te oldaladról diagnosztizálni.

---

## Szerver egészség figyelése

### Szerver FPS

Ellenőrizd az RPT naplót a szerver FPS-t tartalmazó sorokért. Egy egészséges szerver következetesen 30 FPS-t tart. Figyelmeztetési küszöbök:

| Szerver FPS | Állapot |
|-------------|---------|
| 25-30 | Normális. Kisebb ingadozások várhatók nehéz harc vagy újraindítás közben. |
| 15-25 | Leromlott. A játékosok desync-et észlelnek tárgy interakcióknál és harcnál. |
| 15 alatt | Kritikus. Gumiszalag effektus, sikertelen műveletek, találat regisztráció megtört. |

### CE ciklus figyelmeztetések

A `log_ce_statistics` engedélyezésekor figyeld a CE ciklus időket. A normális 500 ms alatt van. Ha a ciklusok rendszeresen meghaladják az 1000 ms-t, a gazdaságod túl nehéz.

### Tároló növekedés

Figyeld a `storage_1/` méretét. Ellenőrizetlen növekedés perzisztencia duzzadást jelez -- túl sok elhelyezett objektum, sátor vagy rejtekhely halmozódik fel. Rendszeres szerver törlések vagy a `FlagRefreshMaxDuration` csökkentése a `globals.xml`-ben segít ezt kontrollálni.

### Játékos jelentések

A játékosok desync jelentései a legmegbízhatóbb valós idejű mutatód. Ha több játékos egyszerre jelent gumiszalag effektust, a szerver FPS 15 alá esett.

---

## Gyakori teljesítmény hibák

### Túl magas nominal értékek

Minden tárgy `nominal=50`-re állítása, mert "a több zsákmány szórakoztató", tízezernyi nyomon követett objektumot hoz létre. A CE a teljes ciklusát tárgyak kezelésével tölti a játék futtatása helyett. Kezdj vanilla nominalokkal és szelektíven növeld.

### Túl sok jármű esemény

A járművek költséges entitások fizikai szimulációval, felszerelés nyomon követéssel és perzisztenciával. A vanilla összesen körülbelül 50 járművet spawnol. A 150+ járművel rendelkező szerverek jelentős FPS veszteséget tapasztalnak.

### 30+ mod futtatása tesztelés nélkül

Minden mod önmagában rendben van. A 30+ mod összetett hatása -- ezernyi extra típus, tucatnyi frame-enkénti szkript és megnövekedett memória nyomás -- 50%-kal vagy többel csökkentheti a szerver FPS-t. Adj hozzá modokat 3-5-ös csoportokban és tesztelj minden csoport után.

### A szerver soha nem kap újraindítást

Egyes modoknak memóriaszivárgásaik vannak, amelyek idővel felhalmozódnak. Ütemezz automatikus újraindításokat 4-6 óránként. A legtöbb szerver hosting panel támogatja ezt. Még a jól megírt modok is profitálnak az időszakos újraindításokból, mert a motor saját memória fragmentációja növekszik a hosszú munkamenetek során.

### Tároló duzzadás figyelmen kívül hagyása

Egy több gigabájtra növekvő `storage_1/` mappa lelassít minden perzisztencia ciklust. Töröld vagy nyesd időszakosan, különösen ha bázis építést engedélyezel romlási korlátok nélkül.

### Naplózás bekapcsolva hagyva

A CE diagnosztikai naplózás, szkript debug naplózás és admin eszköz naplózás mind minden tickben lemezre ír. Engedélyezd diagnosztizáláshoz, majd kapcsold ki. Tartós bőbeszédű naplózás egy forgalmas szerveren önmagában 1-2 FPS-be kerülhet.

---

[Kezdőlap](../README.md) | [<< Előző: Perzisztencia](07-persistence.md) | [Következő: Hozzáférés vezérlés >>](09-access-control.md)
