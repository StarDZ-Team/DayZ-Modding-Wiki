# Chapter 9.11: Szerver hibaelhárítás

[Kezdőlap](../README.md) | [<< Előző: Mod kezelés](10-mod-management.md) | [Következő: Haladó témák >>](12-advanced.md)

---

> **Összefoglaló:** A leggyakoribb DayZ szerver problémák diagnosztizálása és javítása -- indítási hibák, csatlakozási problémák, összeomlások, zsákmány és jármű spawnolás, perzisztencia és teljesítmény. Minden megoldás itt valós hibamintákon alapul ezernyi közösségi jelentésből.

---

## Tartalomjegyzék

- [A szerver nem indul el](#a-szerver-nem-indul-el)
- [Játékosok nem tudnak csatlakozni](#játékosok-nem-tudnak-csatlakozni)
- [Összeomlások és null pointerek](#összeomlások-és-null-pointerek)
- [Zsákmány nem jelenik meg](#zsákmány-nem-jelenik-meg)
- [Járművek nem jelennek meg](#járművek-nem-jelennek-meg)
- [Perzisztencia problémák](#perzisztencia-problémák)
- [Teljesítmény problémák](#teljesítmény-problémák)
- [Naplófájlok olvasása](#naplófájlok-olvasása)
- [Gyors diagnosztikai ellenőrzőlista](#gyors-diagnosztikai-ellenőrzőlista)

---

## A szerver nem indul el

### Hiányzó DLL fájlok

Ha a `DayZServer_x64.exe` azonnal összeomlik hiányzó DLL hibával, telepítsd a legújabb **Visual C++ Redistributable for Visual Studio 2019** (x64) csomagot a Microsoft hivatalos oldaláról és indítsd újra.

### A port már használatban van

Egy másik DayZ példány vagy alkalmazás foglalja a 2302-es portot. Ellenőrizd a `netstat -ano | findstr 2302` (Windows) vagy `ss -tulnp | grep 2302` (Linux) paranccsal. Állítsd le az ütköző folyamatot vagy változtasd meg a portot a `-port=2402` paraméterrel.

### Hiányzó küldetés mappa

A szerver az `mpmissions/<template>/` mappát keresi, ahol a mappa neve pontosan megegyezik a **serverDZ.cfg** `template` értékével. Chernarus esetén ez az `mpmissions/dayzOffline.chernarusplus/`, és tartalmaznia kell legalább az **init.c** fájlt.

### Érvénytelen serverDZ.cfg

Egyetlen hiányzó pontosvessző vagy rossz idézőjel típus csendben megakadályozza az indítást. Figyelj:

- Hiányzó `;` az értéksorok végén
- Tipográfiai idézőjelek az egyenes idézőjelek helyett
- Hiányzó `{};` blokk a class bejegyzések körül

### Hiányzó mod fájlok

Minden elérési útnak a `-mod=@CF;@VPPAdminTools;@MyMod` paraméterben léteznie kell a szerver gyökérhez képest, és tartalmaznia kell egy **addons/** mappát `.pbo` fájlokkal. Egyetlen hibás elérési út megakadályozza az indítást.

---

## Játékosok nem tudnak csatlakozni

### Port továbbítás

A DayZ-nek ezeket a portokat kell továbbítani és megnyitni a tűzfalban:

| Port | Protokoll | Cél |
|------|-----------|-----|
| 2302 | UDP | Játék forgalom |
| 2303 | UDP | Steam hálózatkezelés |
| 2304 | UDP | Steam lekérdezés (belső) |
| 27016 | UDP | Steam szerver böngésző lekérdezés |

Ha megváltoztattad az alapportot a `-port=` paraméterrel, minden más port ugyanannyival eltolódik.

### Tűzfal blokkolás

Add hozzá a **DayZServer_x64.exe** fájlt az OS tűzfal kivételekhez. Windowson: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. Linuxon nyisd meg a portokat `ufw`-vel vagy `iptables`-szel.

### Mod eltérés

A klienseknek pontosan ugyanazokkal a mod verziókkal kell rendelkezniük, mint a szerver. Ha egy játékos "Mod mismatch" üzenetet lát, valamelyik oldal elavult verzióval rendelkezik. Frissíts mindkét oldalon, amikor bármely mod Workshop frissítést kap.

### Hiányzó .bikey fájlok

Minden mod `.bikey` fájljának a szerver `keys/` könyvtárában kell lennie. Enélkül a BattlEye elutasítja a kliens aláírt PBO-it. Keresd meg minden mod `keys/` vagy `key/` mappáját.

### Szerver tele

Ellenőrizd a `maxPlayers` értéket a **serverDZ.cfg**-ben (alapértelmezett 60).

---

## Összeomlások és null pointerek

### Null Pointer hozzáférés

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- a leggyakoribb szkript hiba. Egy mod törölt vagy inicializálatlan objektumon hív metódust. Ez mod hiba, nem szerver konfigurációs hiba. Jelentsd a mod készítőnek a teljes RPT naplóval.

### Szkript hibák keresése

Keresd az RPT naplóban a `SCRIPT (E)` szöveget. A hibában szereplő osztály és metódusnév elárulja, melyik mod a felelős. RPT helyek:

- **Szerver:** `$profiles/` könyvtár (vagy a szerver gyökér, ha nincs `-profiles=` beállítva)
- **Kliens:** `%localappdata%\DayZ\`

### Összeomlás újraindításkor

Ha a szerver minden újraindításnál összeomlik, a **storage_1/** sérült lehet. Állítsd le a szervert, mentsd le a `storage_1/` mappát, töröld a `storage_1/data/events.bin` fájlt, és indítsd újra. Ha ez sem segít, töröld a teljes `storage_1/` könyvtárat (törli az összes perzisztenciát).

### Összeomlás mod frissítés után

Állítsd vissza az előző mod verziót. Ellenőrizd a Workshop változásnaplót a törő változások szempontjából -- átnevezett osztályok, eltávolított konfigok és megváltozott RPC formátumok gyakori okok.

---

## Zsákmány nem jelenik meg

### types.xml nincs regisztrálva

A **types.xml**-ben definiált tárgyak nem jelennek meg, hacsak a fájl nincs regisztrálva a **cfgeconomycore.xml**-ben:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Ha egyedi types fájlt használsz (pl. **types_custom.xml**), adj hozzá egy külön `<file>` bejegyzést neki.

### Rossz kategória, használat vagy érték tagek

Minden `<category>`, `<usage>` és `<value>` tagnak a types.xml-ben meg kell egyeznie a **cfglimitsdefinition.xml**-ben definiált névvel. Egy elírás, mint `usage name="Military"` (nagy M), amikor a definíció `military` (kis m) mondja, csendben megakadályozza a tárgy megjelenését.

### Nominal nullára állítva

Ha `nominal` értéke `0`, a CE soha nem fogja spawnolni azt a tárgyat. Ez szándékos olyan tárgyaknál, amelyek csak megmunkálással, eseményekkel vagy admin elhelyezéssel létezhetnek. Ha azt szeretnéd, hogy a tárgy természetesen megjelenjen, állítsd a `nominal` értéket legalább `1`-re.

### Hiányzó térképcsoport pozíciók

A tárgyaknak érvényes spawn pozíciókra van szükségük az épületeken belül. Ha egy egyedi tárgynak nincs megfelelő térképcsoport pozíciója (a **mapgroupproto.xml**-ben definiálva), a CE-nek nincs hova helyeznie. Rendeld hozzá a tárgyat olyan kategóriákhoz és használatokhoz, amelyeknek már vannak érvényes pozícióik a térképen.

---

## Járművek nem jelennek meg

A járművek az esemény rendszert használják, **nem** a types.xml-t.

### events.xml konfiguráció

A jármű spawnok az **events.xml**-ben vannak definiálva:

```xml
<event name="VehicleOffroadHatchback">
    <nominal>8</nominal>
    <min>5</min>
    <max>8</max>
    <lifetime>3888000</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="1" min="1" type="OffroadHatchback"/>
    </children>
</event>
```

### Hiányzó spawn pozíciók

A `<position>fixed</position>` jármű eseményeknek bejegyzésekre van szükségük a **cfgeventspawns.xml**-ben. Definiált koordináták nélkül az eseménynek nincs hova helyeznie a járművet.

### Esemény letiltva

Ha `<active>0</active>`, az esemény teljesen le van tiltva. Állítsd `1`-re.

### Sérült járművek blokkolják a helyeket

Ha `remove_damaged="0"`, az elpusztult járművek örökre a világban maradnak és elfoglalják a spawn helyeket. Állítsd `remove_damaged="1"`-re, hogy a CE megtisztítsa a roncsokat és pótlásokat spawnoljon.

---

## Perzisztencia problémák

### Bázisok eltűnnek

A területi zászlókat frissíteni kell, mielőtt az időzítőjük lejár. Az alapértelmezett `FlagRefreshFrequency` `432000` másodperc (5 nap). Ha egyetlen játékos sem lép interakcióba a zászlóval ezen időn belül, a zászló és a sugáron belüli összes objektum törlődik.

Ellenőrizd az értéket a **globals.xml**-ben:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Növeld ezt az értéket alacsony népességű szervereken, ahol a játékosok ritkábban lépnek be.

### Tárgyak eltűnnek újraindítás után

Minden tárgynak van `lifetime` értéke a **types.xml**-ben (másodpercben). Amikor ez lejár játékos interakció nélkül, a CE eltávolítja. Referencia: `3888000` = 45 nap, `604800` = 7 nap, `14400` = 4 óra. A tárolókban lévő tárgyak a tároló élettartamát öröklik.

### storage_1/ túl nagyra nő

Ha a `storage_1/` könyvtárad több száz MB fölé nő, a gazdaságod túl sok tárgyat termel. Csökkentsd a `nominal` értékeket a types.xml-ben, különösen a magas számú tárgyaknál, mint étel, ruházat és lőszer. A felduzzadt perzisztencia fájl hosszabb újraindítási időket okoz.

### Játékos adatok elvesztek

A játékos inventárok és pozíciók a `storage_1/players/` mappában tárolódnak. Ha ez a könyvtár törlődik vagy megsérül, minden játékos frissen spawnol. Rendszeresen mentsd a `storage_1/` mappát.

---

## Teljesítmény problémák

### Szerver FPS csökken

A DayZ szerverek 30+ FPS-t céloznak a gördülékeny játékmenethez. Az alacsony szerver FPS gyakori okai:

- **Túl sok zombi** -- csökkentsd a `ZombieMaxCount` értéket a **globals.xml**-ben (alapértelmezett 800, próbálj 400-600-at)
- **Túl sok állat** -- csökkentsd az `AnimalMaxCount` értéket (alapértelmezett 200, próbálj 100-at)
- **Túlzott zsákmány** -- csökkentsd a `nominal` értékeket a types.xml-ben
- **Túl sok bázis objektum** -- a nagy bázisok száznyi tárggyal terhelik a perzisztenciát
- **Nehéz szkript modok** -- egyes modok költséges frame-enkénti logikát futtatnak

### Desync

A gumiszalag effektust, késleltetett műveleteket vagy láthatatlan zombikat tapasztaló játékosok a desync tünetei. Ez szinte mindig azt jelenti, hogy a szerver FPS 15 alá esett. Javítsd az alapvető teljesítmény problémát ahelyett, hogy desync-specifikus beállítást keresnél.

### Hosszú újraindítási idők

Az újraindítási idő egyenesen arányos a `storage_1/` méretével. Ha az újraindítás több mint 2-3 percig tart, túl sok perzisztens objektumod van. Csökkentsd a zsákmány nominal értékeket és állíts be megfelelő élettartamokat.

---

## Naplófájlok olvasása

### Szerver RPT helye

Az RPT fájl a `$profiles/` könyvtárban van (ha a `-profiles=` paraméterrel indítottál) vagy a szerver gyökérben. Fájlnév mintája: `DayZServer_x64_<dátum>_<idő>.RPT`.

### Mire keress

| Keresési kifejezés | Jelentés |
|--------------------|----------|
| `SCRIPT (E)` | Szkript hiba -- egy modnak hibája van |
| `[ERROR]` | Motor szintű hiba |
| `ErrorMessage` | Végzetes hiba, amely leállítást okozhat |
| `Cannot open` | Hiányzó fájl (PBO, konfig, küldetés) |
| `Crash` | Alkalmazás szintű összeomlás |

### BattlEye naplók

A BattlEye naplók a szerver gyökerén belüli `BattlEye/` könyvtárban vannak. Ezek kirúgási és kitiltási eseményeket mutatnak. Ha játékosok váratlan kirúgásról számolnak be, itt ellenőrizz először.

---

## Gyors diagnosztikai ellenőrzőlista

Ha valami elromlik, dolgozd végig ezt a listát sorrendben:

```
1. Ellenőrizd a szerver RPT-t SCRIPT (E) és [ERROR] sorokért
2. Ellenőrizd, hogy minden -mod= elérési út létezik és tartalmaz addons/*.pbo fájlokat
3. Ellenőrizd, hogy minden .bikey fájl be van másolva a keys/ mappába
4. Ellenőrizd a serverDZ.cfg fájlt szintaktikai hibákért (hiányzó pontosvesszők)
5. Ellenőrizd a port továbbítást: 2302 UDP + 27016 UDP
6. Ellenőrizd, hogy a küldetés mappa megegyezik a serverDZ.cfg template értékével
7. Ellenőrizd a storage_1/ mappát sérülés szempontjából (töröld az events.bin fájlt, ha szükséges)
8. Tesztelj először nulla moddal, majd adj hozzá modokat egyenként
```

A 8. lépés a legerősebb technika. Ha a szerver vanilla módban működik, de modokkal elromlik, izolálhatod a problémás modot bináris kereséssel -- add hozzá a modjaid felét, tesztelj, majd szűkítsd le.

---

[Kezdőlap](../README.md) | [<< Előző: Mod kezelés](10-mod-management.md) | [Következő: Haladó témák >>](12-advanced.md)
