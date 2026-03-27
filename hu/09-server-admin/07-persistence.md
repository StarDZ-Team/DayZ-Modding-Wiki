# Chapter 9.7: Világ állapot és perzisztencia

[Kezdőlap](../README.md) | [<< Előző: Játékos spawnolás](06-player-spawning.md) | [Következő: Teljesítmény hangolás >>](08-performance.md)

A DayZ perzisztencia életben tartja a világot az újraindítások között. A működés megértése lehetővé teszi a bázisok kezelését, a törlések tervezését és az adatsérülések elkerülését.

## Tartalomjegyzék

- [Hogyan működik a perzisztencia](#hogyan-működik-a-perzisztencia)
- [A storage_1/ könyvtár](#a-storage_1-könyvtár)
- [globals.xml perzisztencia paraméterek](#globalsxml-perzisztencia-paraméterek)
- [Területi zászló rendszer](#területi-zászló-rendszer)
- [Hoarder tárgyak](#hoarder-tárgyak)
- [cfggameplay.json perzisztencia beállítások](#cfggameplayjson-perzisztencia-beállítások)
- [Szerver törlési eljárások](#szerver-törlési-eljárások)
- [Biztonsági mentési stratégia](#biztonsági-mentési-stratégia)
- [Gyakori hibák](#gyakori-hibák)

---

## Hogyan működik a perzisztencia

A DayZ a világ állapotot a szerver profil mappáján belüli `storage_1/` könyvtárban tárolja. A ciklus egyszerű:

1. A szerver rendszeresen menti a világ állapotot (alapértelmezés szerint ~30 percenként) és szabályos leállításkor.
2. Újraindításkor a szerver beolvassa a `storage_1/` tartalmát és visszaállítja az összes megőrzött objektumot -- járművek, bázisok, sátrak, hordók, játékos inventárok.
3. A perzisztencia nélküli tárgyak (a legtöbb talajzsákmány) a Központi Gazdaság által generálódnak újra minden újraindításkor.

Ha a `storage_1/` nem létezik indításkor, a szerver friss világot hoz létre játékos adatok és épített szerkezetek nélkül.

---

## A storage_1/ könyvtár

A szerver profil tartalmazza a `storage_1/` mappát ezekkel az alkönyvtárakkal és fájlokkal:

| Útvonal | Tartalom |
|---------|----------|
| `data/` | Bináris fájlok a világ objektumokkal -- bázis elemek, elhelyezett tárgyak, jármű pozíciók |
| `players/` | Játékosokénti **.save** fájlok SteamID64 alapján indexelve. Minden fájl pozíciót, inventárt, életerőt, állapot hatásokat tárol |
| `snapshot/` | Világ állapot pillanatképek mentési műveletek során |
| `events.bin` / `events.xy` | Dinamikus esemény állapot -- nyomon követi a helikopter roncs helyeket, konvoj pozíciókat és más spawnolt eseményeket |

A `data/` mappa adja a perzisztencia tömegét. Serializált objektum adatokat tartalmaz, amelyeket a szerver indításkor olvas be a világ újraépítéséhez.

---

## globals.xml perzisztencia paraméterek

A **globals.xml** fájl (a küldetés mappádban) szabályozza a takarítási időzítőket és a zászló viselkedést. Ezek a perzisztencia szempontjából releváns értékek:

```xml
<!-- Területi zászló frissítés -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 nap (másodpercben) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 nap (másodpercben) -->

<!-- Takarítási időzítők -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Alapértelmezett takarítás (másodperc) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Halott játékos test: 1 óra -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Halott állat: 20 perc -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Halott zombi: 5,5 perc -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Tönkrement tárgy: 5,5 perc -->

<!-- Takarítási viselkedés -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Ciklusonként megtisztított tárgyak maximuma -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Takarítás kihagyása 100 m-en belül egy játékostól -->
```

A `CleanupAvoidance` érték megakadályozza, hogy a szerver aktív játékosok közelében szüntessen meg objektumokat. Ha egy holttest 100 méteren belül van bármely játékosnak, ott marad, amíg a játékos el nem megy vagy az időzítő nem nullázódik.

---

## Területi zászló rendszer

A területi zászlók a DayZ bázis perzisztenciájának magját képezik. Így működik a két kulcsérték együttesen:

- **FlagRefreshFrequency** (`432000` másodperc = 5 nap) -- Milyen gyakran kell interakcióba lépned a zászlóddal az aktív állapot megőrzéséhez. Menj a zászlóhoz és használd a "Frissítés" műveletet.
- **FlagRefreshMaxDuration** (`3456000` másodperc = 40 nap) -- A maximális felhalmozott védelmi idő. Minden frissítés legfeljebb FlagRefreshFrequency értékű időt ad hozzá, de az összeg nem haladhatja meg ezt a korlátot.

Amikor egy zászló időzítője lejár:

1. Maga a zászló megtisztításra jogosulttá válik.
2. A zászlóhoz kapcsolt összes bázis építési elem elveszíti a perzisztencia védelmét.
3. A következő takarítási ciklusban a védelem nélküli elemek elkezdenek eltűnni.

Ha csökkented a FlagRefreshFrequency értéket, a játékosoknak gyakrabban kell meglátogatniuk a bázisaikat. Ha növeled a FlagRefreshMaxDuration értéket, a bázisok hosszabb ideig maradnak fenn a látogatások között. Mindkét értéket együtt állítsd a szervered játékstílusához.

---

## Hoarder tárgyak

A **cfgspawnabletypes.xml**-ben bizonyos tárolók a `<hoarder/>` taggel vannak megjelölve. Ez raktározásra alkalmas tárgyként jelöli meg őket, amelyek beleszámítanak a Központi Gazdaság játékosokénti tárolási korlátaiba.

A vanilla hoarder tárgyak:

| Tárgy | Típus |
|-------|-------|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Tároló hordók |
| CarTent, LargeTent, MediumTent, PartyTent | Sátrak |
| SeaChest | Víz alatti tároló |
| SmallProtectorCase | Kis zárható tok |
| UndergroundStash | Elásott rejtély |
| WoodenCrate | Kézműves tároló |

Példa a **cfgspawnabletypes.xml**-ből:

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

A szerver nyomon követi, hány hoarder tárgyat helyezett el minden játékos. Amikor a korlát elérve, az új elhelyezések meghiúsulnak vagy a legrégebbi tárgy tűnik el (a szerver konfigurációtól függően).

---

## cfggameplay.json perzisztencia beállítások

A **cfggameplay.json** fájl a küldetés mappádban tartalmaz beállításokat, amelyek a bázis és tároló tartósságát befolyásolják:

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Beállítás | Alapértelmezett | Hatás |
|-----------|-----------------|-------|
| `disableBaseDamage` | `false` | Ha `true`, a bázis építési elemek (falak, kapuk, őrtornyok) nem sérülhetnek. Ez gyakorlatilag letiltja a raidolást. |
| `disableContainerDamage` | `false` | Ha `true`, a tároló konténerek (sátrak, hordók, ládák) nem kaphatnak sérülést. A bennük lévő tárgyak biztonságban maradnak. |

Mindkettő `true`-ra állítása PvE-barát szervert hoz létre, ahol a bázisok és tárolók elpusztíthatatlanok. A legtöbb PvP szerver mindkettőt `false`-on hagyja.

---

## Szerver törlési eljárások

Négyféle törlés létezik, mindegyik a `storage_1/` más részét célozza. **Mindig állítsd le a szervert bármilyen törlés előtt.**

### Teljes törlés

Töröld a teljes `storage_1/` mappát. A szerver friss világot hoz létre a következő indításkor. Minden bázis, jármű, sátor, játékos adat és esemény állapot eltűnik.

### Gazdaság törlés (Játékosok megtartása)

Töröld a `storage_1/data/` mappát, de hagyd meg a `storage_1/players/` mappát. A játékosok megtartják karaktereiket és inventárjukat, de minden elhelyezett objektum (bázisok, sátrak, hordók, járművek) eltűnik.

### Játékos törlés (Világ megtartása)

Töröld a `storage_1/players/` mappát. Minden játékos karakter visszaáll friss spawnra. A bázisok és elhelyezett objektumok megmaradnak a világban.

### Időjárás / Esemény visszaállítás

Töröld az `events.bin` vagy `events.xy` fájlt a `storage_1/` mappából. Ez visszaállítja a dinamikus esemény pozíciókat (helikopter roncsok, konvojok). A szerver új esemény helyeket generál a következő indításkor.

---

## Biztonsági mentési stratégia

A perzisztencia adatok pótolhatatlanok az elvesztés után. Kövesd ezeket a gyakorlatokat:

- **Mentés leállított szerver mellett.** Másold a teljes `storage_1/` mappát, amíg a szerver nem fut. Futás közötti másolás kockáztatja a részleges vagy sérült állapot rögzítését.
- **Ütemezz mentéseket újraindítások előtt.** Ha automatikus újraindításokat futtatsz (4-6 óránként), adj hozzá egy mentési lépést az újraindítási szkriptedhez, amely lemásolja a `storage_1/` mappát, mielőtt a szerver folyamat elindul.
- **Tarts fenn több generációt.** Rotáld a mentéseket, hogy legalább 3 friss másolatod legyen. Ha a legújabb mentésed sérült, visszaállíthatsz egy korábbira.
- **Tárolj gépeken kívül.** Másold a mentéseket külön meghajtóra vagy felhőtárolóba. A szerver gép lemezhiba esetén a mentéseid is elvesznek, ha ugyanazon a meghajtón vannak.

Egy minimális mentési szkript (szerver indítás előtt fut):

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Gyakori hibák

Ezek rendszeresen felmerülnek a szerver admin közösségekben:

| Hiba | Mi történik | Megelőzés |
|------|-------------|-----------|
| `storage_1/` törlése futó szerver mellett | Adatsérülés. A szerver már nem létező fájlokba ír, ami összeomlásokat vagy részleges állapotot okoz a következő indításkor. | Mindig állítsd le először a szervert. |
| Nem készítesz biztonsági mentést törlés előtt | Ha véletlenül rossz mappát törölsz vagy a törlés rosszul sikerül, nincs visszaállítási lehetőség. | Mentsd le a `storage_1/` mappát minden törlés előtt. |
| Időjárás visszaállítás és teljes törlés összekeverése | Az `events.xy` törlése csak a dinamikus esemény pozíciókat állítja vissza. Nem állítja vissza a zsákmányt, bázisokat vagy játékosokat. | Tudd, melyik fájl mit szabályoz (lásd a fenti könyvtártáblázatot). |
| Zászló nem frissített időben | 40 nap (FlagRefreshMaxDuration) után a zászló lejár és az összes csatolt bázis elem megtisztításra jogosulttá válik. A játékosok elveszítik a teljes bázisukat. | Emlékeztesd a játékosokat a frissítési intervallumra. Csökkentsd a FlagRefreshMaxDuration értéket alacsony népességű szervereken. |
| globals.xml szerkesztése futó szerver mellett | A változások nem lépnek életbe újraindításig. Rosszabb esetben a szerver leállításkor felülírja a szerkesztéseidet. | Konfigurációs fájlokat csak leállított szerver mellett szerkessz. |

---

[Kezdőlap](../README.md) | [<< Előző: Játékos spawnolás](06-player-spawning.md) | [Következő: Teljesítmény hangolás >>](08-performance.md)
