# Chapter 9.2: Könyvtárszerkezet és küldetés mappa

[Kezdőlap](../README.md) | [<< Előző: Szerver telepítés](01-server-setup.md) | **Könyvtárszerkezet** | [Következő: serverDZ.cfg referencia >>](03-server-cfg.md)

---

> **Összefoglaló:** A DayZ szerver könyvtárban és a küldetés mappában található összes fájl és mappa teljes áttekintése. Az egyes fájlok szerepének ismerete -- és annak tudása, hogy melyiket biztonságos szerkeszteni -- elengedhetetlen a zsákmánygazdaság módosítása vagy modok hozzáadása előtt.

---

## Tartalomjegyzék

- [Felső szintű szerver könyvtár](#felső-szintű-szerver-könyvtár)
- [Az addons/ mappa](#az-addons-mappa)
- [A keys/ mappa](#a-keys-mappa)
- [A profiles/ mappa](#a-profiles-mappa)
- [Az mpmissions/ mappa](#az-mpmissions-mappa)
- [Küldetés mappa szerkezete](#küldetés-mappa-szerkezete)
- [A db/ mappa -- A gazdaság magja](#a-db-mappa----a-gazdaság-magja)
- [Az env/ mappa -- Állat területek](#az-env-mappa----állat-területek)
- [A storage_1/ mappa -- Perzisztencia](#a-storage_1-mappa----perzisztencia)
- [Felső szintű küldetésfájlok](#felső-szintű-küldetésfájlok)
- [Mely fájlokat szerkeszd és melyeket ne](#mely-fájlokat-szerkeszd-és-melyeket-ne)

---

## Felső szintű szerver könyvtár

```
DayZServer/
  DayZServer_x64.exe          # Szerver futtatható fájl
  serverDZ.cfg                 # Fő szerver konfiguráció (név, jelszó, modok, idő)
  dayzsetting.xml              # Megjelenítési beállítások (dedikált szervereknél nem releváns)
  ban.txt                      # Kitiltott Steam64 ID-k, soronként egy
  whitelist.txt                # Engedélyezett Steam64 ID-k, soronként egy
  steam_appid.txt              # Tartalmazza: "221100" -- ne szerkeszd
  dayz.gproj                   # Workbench projektfájl -- ne szerkeszd
  addons/                      # Vanilla játék PBO-k
  battleye/                    # Csalásellenes fájlok
  config/                      # Steam konfiguráció (config.vdf)
  dta/                         # Motor alap PBO-k (szkriptek, GUI, grafika)
  keys/                        # Aláírás ellenőrző kulcsok (.bikey fájlok)
  logs/                        # Motor szintű naplók
  mpmissions/                  # Összes küldetés mappa
  profiles/                    # Futásidejű kimenet (szkript naplók, játékos DB, összeomlási mentések)
  server_manager/              # Szerver kezelő segédprogramok
```

---

## Az addons/ mappa

Tartalmazza az összes vanilla játéktartalmat PBO fájlokba csomagolva. Minden PBO-hoz tartozik egy megfelelő `.bisign` aláírás fájl:

```
addons/
  ai.pbo                       # AI viselkedési szkriptek
  ai.pbo.dayz.bisign           # Az ai.pbo aláírása
  animals.pbo                  # Állat definíciók
  characters_backpacks.pbo     # Hátizsák modellek/konfigok
  characters_belts.pbo         # Öv tárgy modellek
  weapons_firearms.pbo         # Fegyver modellek/konfigok
  ... (100+ PBO fájl)
```

**Soha ne szerkeszd ezeket a fájlokat.** Minden SteamCMD frissítéskor felülíródnak. A modok a `modded` class rendszeren keresztül írják felül a vanilla viselkedést, nem a PBO-k módosításával.

---

## A keys/ mappa

`.bikey` nyilvános kulcsfájlokat tartalmaz, amelyek a mod aláírások ellenőrzésére szolgálnak:

```
keys/
  dayz.bikey                   # Vanilla aláírás kulcs (mindig jelen van)
```

Amikor modot adsz hozzá, másold be a `.bikey` fájlját ebbe a mappába. A szerver a `verifySignatures = 2` beállítást használja a `serverDZ.cfg` fájlban, hogy visszautasítson minden PBO-t, amelyhez nincs megfelelő `.bikey` ebben a mappában.

Ha egy játékos olyan modot tölt be, amelynek a kulcsa nincs a `keys/` mappádban, **"Signature check failed"** kicket kap.

---

## A profiles/ mappa

Az első szerverindításkor jön létre. Futásidejű kimenetet tartalmaz:

```
profiles/
  BattlEye/                              # BE naplók és kitiltások
  DataCache/                             # Gyorsítótárazott adatok
  Users/                                 # Játékosokénti beállítás fájlok
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Admin napló
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Motor jelentés (összeomlási info, figyelmeztetések)
  script_2026-03-08_11-34-35.log           # Szkript napló (az elsődleges hibakereső eszközöd)
```

A **szkript napló** a legfontosabb fájl itt. Minden `Print()` hívás, minden szkript hiba és minden mod betöltési üzenet ide kerül. Amikor valami elromlik, itt kell először keresned.

A naplófájlok idővel felhalmozódnak. A régi naplók nem törlődnek automatikusan.

---

## Az mpmissions/ mappa

Térképenként egy almappát tartalmaz:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (ingyenes)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

A mappa névformátuma: `<küldetésNév>.<terrainNév>`. A `serverDZ.cfg` fájlban lévő `template` értéknek pontosan meg kell egyeznie ezen mappanevek egyikével.

---

## Küldetés mappa szerkezete

A Chernarus küldetés mappa (`mpmissions/dayzOffline.chernarusplus/`) tartalma:

```
dayzOffline.chernarusplus/
  init.c                         # Küldetés belépési pont szkript
  db/                            # Gazdaság alapfájlok
  env/                           # Állat terület definíciók
  storage_1/                     # Perzisztencia adatok (játékosok, világ állapot)
  cfgeconomycore.xml             # Gazdaság gyökér osztályok és naplózási beállítások
  cfgenvironment.xml             # Hivatkozások az állat terület fájlokra
  cfgeventgroups.xml             # Esemény csoport definíciók
  cfgeventspawns.xml             # Pontos spawn pozíciók eseményekhez (járművek, stb.)
  cfgeffectarea.json             # Fertőzött zóna definíciók
  cfggameplay.json               # Játékmenet finomhangolás (állóképesség, sebzés, építés)
  cfgignorelist.xml              # Teljesen kizárt tárgyak a gazdaságból
  cfglimitsdefinition.xml        # Érvényes kategória/használat/érték tag definíciók
  cfglimitsdefinitionuser.xml    # Felhasználó által definiált egyedi tag definíciók
  cfgplayerspawnpoints.xml       # Friss spawn helyek
  cfgrandompresets.xml           # Újrafelhasználható zsákmánykészlet definíciók
  cfgspawnabletypes.xml          # Előre csatolt tárgyak és rakomány a spawnolt entitásokon
  cfgundergroundtriggers.json    # Föld alatti terület triggerek
  cfgweather.xml                 # Időjárás konfiguráció
  areaflags.map                  # Terület jelző adatok (bináris)
  mapclusterproto.xml            # Térkép klaszter prototípus definíciók
  mapgroupcluster.xml            # Épület csoport klaszter definíciók
  mapgroupcluster01.xml          # Klaszter adatok (1. rész)
  mapgroupcluster02.xml          # Klaszter adatok (2. rész)
  mapgroupcluster03.xml          # Klaszter adatok (3. rész)
  mapgroupcluster04.xml          # Klaszter adatok (4. rész)
  mapgroupdirt.xml               # Talaj zsákmány pozíciók
  mapgrouppos.xml                # Térképcsoport pozíciók
  mapgroupproto.xml              # Térképcsoportok prototípus definíciói
```

---

## A db/ mappa -- A gazdaság magja

Ez a Központi Gazdaság szíve. Öt fájl szabályozza, hogy mi jelenik meg, hol és mennyi:

```
db/
  types.xml        # A kulcsfájl: minden tárgy spawn szabályait definiálja
  globals.xml      # Globális gazdasági paraméterek (időzítők, korlátok, mennyiségek)
  events.xml       # Dinamikus események (állatok, járművek, helikopterek)
  economy.xml      # Gazdasági alrendszerek kapcsolói (zsákmány, állatok, járművek)
  messages.xml     # Ütemezett szerver üzenetek a játékosoknak
```

### types.xml

Meghatározza a spawn szabályokat **minden tárgyra** a játékban. Körülbelül 23 000 sorával messze a legnagyobb gazdaságfájl. Minden bejegyzés megadja, hány példány létezhet az adott tárgyból a térképen, hol jelenhet meg és meddig marad meg. Részletes áttekintés a [9.4. fejezetben](04-loot-economy.md).

### globals.xml

Globális paraméterek, amelyek az egész gazdaságot érintik: zombi számok, állat számok, takarítási időzítők, zsákmány sérülés tartományok, újraspawnolás időzítése. Összesen 33 paraméter van. A teljes referencia a [9.4. fejezetben](04-loot-economy.md).

### events.xml

Dinamikus spawn eseményeket definiál állatokhoz és járművekhez. Minden esemény megad egy névleges számot, spawn feltételeket és gyerek variánsokat. Például a `VehicleCivilianSedan` esemény 8 szedánt spawnol a térképen 3 színváltozatban.

### economy.xml

Fő kapcsolók a gazdasági alrendszerekhez:

```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```

| Jelző | Jelentés |
|-------|----------|
| `init` | Tárgyak spawnolása az első szerver indításkor |
| `load` | Mentett állapot betöltése a perzisztenciából |
| `respawn` | Tárgyak újraspawnolásának engedélyezése takarítás után |
| `save` | Állapot mentése perzisztencia fájlokba |

### messages.xml

Ütemezett üzenetek, amelyek minden játékosnak megjelennek. Támogatja a visszaszámlálókat, ismétlési intervallumokat, csatlakozáskori üzeneteket és leállítási figyelmeztetéseket:

```xml
<messages>
    <message>
        <deadline>600</deadline>
        <shutdown>1</shutdown>
        <text>#name will shutdown in #tmin minutes.</text>
    </message>
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>Welcome to #name</text>
    </message>
</messages>
```

Használd a `#name` változót a szerver nevéhez és a `#tmin` változót a hátralévő időhöz percben.

---

## Az env/ mappa -- Állat területek

XML fájlokat tartalmaz, amelyek meghatározzák, hogy az egyes állatfajok hol jelenhetnek meg:

```
env/
  bear_territories.xml
  cattle_territories.xml
  domestic_animals_territories.xml
  fox_territories.xml
  hare_territories.xml
  hen_territories.xml
  pig_territories.xml
  red_deer_territories.xml
  roe_deer_territories.xml
  sheep_goat_territories.xml
  wild_boar_territories.xml
  wolf_territories.xml
  zombie_territories.xml
```

Ezek a fájlok több száz koordinátapontot tartalmaznak, amelyek terület zónákat definiálnak a térképen. A `cfgenvironment.xml` hivatkozik rájuk. Ritkán kell szerkesztened ezeket, hacsak nem akarod megváltoztatni, hogy földrajzilag hol jelenjenek meg az állatok vagy zombik.

---

## A storage_1/ mappa -- Perzisztencia

A szerver perzisztens állapotát tárolja az újraindítások között:

```
storage_1/
  players.db         # SQLite adatbázis az összes játékos karakterről
  spawnpoints.bin    # Bináris spawn pont adatok
  backup/            # Automatikus biztonsági mentések a perzisztencia adatokról
  data/              # Világ állapot (elhelyezett tárgyak, bázis építés, járművek)
```

**Soha ne szerkeszd a `players.db` fájlt, amíg a szerver fut.** Ez egy SQLite adatbázis, amelyet a szerver folyamat zárol. Ha karaktereket kell törölnöd, először állítsd le a szervert, majd töröld vagy nevezd át a fájlt.

**Teljes perzisztencia törléshez** állítsd le a szervert és töröld a teljes `storage_1/` mappát. A szerver a következő indításkor újra létrehozza friss világgal.

**Részleges törléshez** (karakterek megtartása, zsákmány visszaállítása):
1. Állítsd le a szervert
2. Töröld a `storage_1/data/` fájljait, de tartsd meg a `players.db` fájlt
3. Indítsd újra

---

## Felső szintű küldetésfájlok

### cfgeconomycore.xml

Regisztrálja a gazdaság gyökér osztályait és konfigurálja a CE naplózást:

```xml
<economycore>
    <classes>
        <rootclass name="DefaultWeapon" />
        <rootclass name="DefaultMagazine" />
        <rootclass name="Inventory_Base" />
        <rootclass name="HouseNoDestruct" reportMemoryLOD="no" />
        <rootclass name="SurvivorBase" act="character" reportMemoryLOD="no" />
        <rootclass name="DZ_LightAI" act="character" reportMemoryLOD="no" />
        <rootclass name="CarScript" act="car" reportMemoryLOD="no" />
        <rootclass name="BoatScript" act="car" reportMemoryLOD="no" />
    </classes>
    <defaults>
        <default name="log_ce_loop" value="false"/>
        <default name="log_ce_dynamicevent" value="false"/>
        <default name="log_ce_vehicle" value="false"/>
        <default name="log_ce_lootspawn" value="false"/>
        <default name="log_ce_lootcleanup" value="false"/>
        <default name="log_ce_lootrespawn" value="false"/>
        <default name="log_ce_statistics" value="false"/>
        <default name="log_ce_zombie" value="false"/>
        <default name="log_storageinfo" value="false"/>
        <default name="log_hivewarning" value="true"/>
        <default name="log_missionfilewarning" value="true"/>
        <default name="save_events_startup" value="true"/>
        <default name="save_types_startup" value="true"/>
    </defaults>
</economycore>
```

Állítsd a `log_ce_lootspawn` értékét `"true"`-ra, amikor tárgy spawn problémákat hibakeresed. Részletes kimenetet ad az RPT naplóban, megmutatva, hogy mely tárgyakat próbálja a CE spawnolni és miért sikerül vagy nem.

### cfglimitsdefinition.xml

Meghatározza a `types.xml`-ben használt `<category>`, `<usage>`, `<value>` és `<tag>` elemek érvényes értékeit:

```xml
<lists>
    <categories>
        <category name="tools"/>
        <category name="containers"/>
        <category name="clothes"/>
        <category name="food"/>
        <category name="weapons"/>
        <category name="books"/>
        <category name="explosives"/>
        <category name="lootdispatch"/>
    </categories>
    <tags>
        <tag name="floor"/>
        <tag name="shelves"/>
        <tag name="ground"/>
    </tags>
    <usageflags>
        <usage name="Military"/>
        <usage name="Police"/>
        <usage name="Medic"/>
        <usage name="Firefighter"/>
        <usage name="Industrial"/>
        <usage name="Farm"/>
        <usage name="Coast"/>
        <usage name="Town"/>
        <usage name="Village"/>
        <usage name="Hunting"/>
        <usage name="Office"/>
        <usage name="School"/>
        <usage name="Prison"/>
        <usage name="Lunapark"/>
        <usage name="SeasonalEvent"/>
        <usage name="ContaminatedArea"/>
        <usage name="Historical"/>
    </usageflags>
    <valueflags>
        <value name="Tier1"/>
        <value name="Tier2"/>
        <value name="Tier3"/>
        <value name="Tier4"/>
        <value name="Unique"/>
    </valueflags>
</lists>
```

Ha olyan `<usage>` vagy `<value>` taget használsz a `types.xml`-ben, amely nincs itt definiálva, a tárgy csendben nem fog megjelenni.

### cfgignorelist.xml

Az itt felsorolt tárgyak teljesen ki vannak zárva a gazdaságból, még akkor is, ha van bejegyzésük a `types.xml`-ben:

```xml
<ignore>
    <type name="Bandage"></type>
    <type name="CattleProd"></type>
    <type name="Defibrillator"></type>
    <type name="HescoBox"></type>
    <type name="StunBaton"></type>
    <type name="TransitBus"></type>
    <type name="Spear"></type>
    <type name="Mag_STANAGCoupled_30Rnd"></type>
    <type name="Wreck_Mi8"></type>
</ignore>
```

Ez olyan tárgyakhoz használatos, amelyek léteznek a játék kódjában, de nem szándékoznak természetesen megjelenni (befejezetlen tárgyak, elavult tartalom, szezonon kívüli szezonális tárgyak).

### cfggameplay.json

Egy JSON fájl, amely felülírja a játékmenet paramétereit. Szabályozza az állóképességet, mozgást, bázis sebzést, időjárást, hőmérsékletet, fegyver akadályozást, fulladást és egyebeket. Ez a fájl opcionális -- ha hiányzik, a szerver az alapértékeket használja.

### cfgplayerspawnpoints.xml

Meghatározza, hogy a frissen spawnolt játékosok hol jelennek meg a térképen, távolsági feltételekkel a fertőzöttektől, más játékosoktól és épületektől.

### cfgeventspawns.xml

Pontos világ koordinátákat tartalmaz, ahol események (járművek, helikopter roncsok, stb.) jelenhetnek meg. Az `events.xml` fájlból minden eseménynévhez tartozik egy érvényes pozíciólista:

```xml
<eventposdef>
    <event name="VehicleCivilianSedan">
        <pos x="12071.933594" z="9129.989258" a="317.953339" />
        <pos x="12302.375001" z="9051.289062" a="60.399284" />
        <pos x="10182.458985" z="1987.5271" a="29.172445" />
        ...
    </event>
</eventposdef>
```

Az `a` attribútum az elforgatási szög fokban.

---

## Mely fájlokat szerkeszd és melyeket ne

| Fájl / Mappa | Szerkeszthető? | Megjegyzések |
|---------------|:--------------:|--------------|
| `serverDZ.cfg` | Igen | Fő szerver konfiguráció |
| `db/types.xml` | Igen | Tárgy spawn szabályok -- a leggyakoribb szerkesztés |
| `db/globals.xml` | Igen | Gazdaság finomhangolási paraméterek |
| `db/events.xml` | Igen | Jármű/állat spawn események |
| `db/economy.xml` | Igen | Gazdasági alrendszer kapcsolók |
| `db/messages.xml` | Igen | Szerver üzenetszórás |
| `cfggameplay.json` | Igen | Játékmenet finomhangolás |
| `cfgspawnabletypes.xml` | Igen | Felszerelés/rakomány előbeállítások |
| `cfgrandompresets.xml` | Igen | Zsákmánykészlet definíciók |
| `cfglimitsdefinition.xml` | Igen | Egyedi usage/value tagek hozzáadása |
| `cfgplayerspawnpoints.xml` | Igen | Játékos spawn helyek |
| `cfgeventspawns.xml` | Igen | Esemény spawn koordináták |
| `cfgignorelist.xml` | Igen | Tárgyak kizárása a gazdaságból |
| `cfgweather.xml` | Igen | Időjárás minták |
| `cfgeffectarea.json` | Igen | Fertőzött zónák |
| `init.c` | Igen | Küldetés belépési szkript |
| `addons/` | **Nem** | Frissítéskor felülíródik |
| `dta/` | **Nem** | Motor alap adatok |
| `keys/` | Csak hozzáadás | Mod `.bikey` fájlok másolása ide |
| `storage_1/` | Csak törlés | Perzisztencia -- ne szerkeszd kézzel |
| `battleye/` | **Nem** | Csalásellenes -- ne nyúlj hozzá |
| `mapgroup*.xml` | Óvatosan | Épület zsákmány pozíciók -- csak haladó szerkesztés |

---

**Előző:** [Szerver telepítés](01-server-setup.md) | [Kezdőlap](../README.md) | **Következő:** [serverDZ.cfg referencia >>](03-server-cfg.md)
