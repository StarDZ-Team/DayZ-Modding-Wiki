# Chapter 9.10: Mod kezelés

[Kezdőlap](../README.md) | [<< Előző: Hozzáférés vezérlés](09-access-control.md) | [Következő: Hibaelhárítás >>](11-troubleshooting.md)

---

> **Összefoglaló:** Harmadik féltől származó modok telepítése, konfigurálása és karbantartása egy DayZ dedikált szerveren. Lefedi az indítási paramétereket, Workshop letöltéseket, aláírás kulcsokat, betöltési sorrendet, csak szerver vs kliens oldali modokat, frissítéseket és a leggyakoribb hibákat, amelyek összeomlásokat vagy játékos kirúgásokat okoznak.

---

## Tartalomjegyzék

- [Hogyan töltődnek be a modok](#hogyan-töltődnek-be-a-modok)
- [Indítási paraméter formátum](#indítási-paraméter-formátum)
- [Workshop mod telepítés](#workshop-mod-telepítés)
- [Mod kulcsok (.bikey)](#mod-kulcsok-bikey)
- [Betöltési sorrend és függőségek](#betöltési-sorrend-és-függőségek)
- [Csak szerver vs kliens oldali modok](#csak-szerver-vs-kliens-oldali-modok)
- [Modok frissítése](#modok-frissítése)
- [Mod konfliktusok hibaelhárítása](#mod-konfliktusok-hibaelhárítása)
- [Gyakori hibák](#gyakori-hibák)

---

## Hogyan töltődnek be a modok

A DayZ a modokat a `-mod=` indítási paraméteren keresztül tölti be. Minden bejegyzés egy PBO fájlokat és egy `config.cpp`-t tartalmazó mappa elérési útja. A motor beolvassa minden mod mappa összes PBO-ját, regisztrálja az osztályokat és szkripteket, majd továbblép a lista következő modjára.

A szervernek és a kliensnek azonos modokkal kell rendelkeznie a `-mod=` paraméterben. Ha a szerver `@CF;@MyMod`-ot listáz és a kliens csak `@CF`-et tartalmaz, a csatlakozás aláírás eltéréssel meghiúsul. A `-servermod=` paraméterbe helyezett, csak szerver oldali modok a kivétel -- a klienseknek soha nincs szükségük ezekre.

---

## Indítási paraméter formátum

Egy tipikus moddolt szerver indítási parancs:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Paraméter | Cél |
|-----------|-----|
| `-mod=` | A szerver és minden csatlakozó kliens által igényelt modok |
| `-servermod=` | Csak szerver oldali modok (a klienseknek nincs szükségük rájuk) |

Szabályok:
- Az elérési utak **pontosvesszővel elválasztottak**, szóközök nélkül a pontosvesszők körül
- Minden elérési út relatív a szerver gyökérkönyvtárhoz (pl. `@CF` azt jelenti, hogy `<szerver_gyökér>/@CF/`)
- Használhatsz abszolút elérési utakat: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **A sorrend számít** -- a függőségeknek a rájuk támaszkodó modok előtt kell szerepelniük

---

## Workshop mod telepítés

### 1. lépés: A mod letöltése

Használd a SteamCMD-t a DayZ **kliens** App ID-val (221100) és a mod Workshop ID-jával:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

A letöltött fájlok ide kerülnek:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### 2. lépés: Szimbolikus link vagy másolás létrehozása

A Workshop mappák numerikus ID-kat használnak, amelyek használhatatlanok a `-mod=` paraméterben. Hozz létre egy elnevezett szimbolikus linket (ajánlott) vagy másold a mappát:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Junction használatával a SteamCMD-n keresztüli frissítések automatikusan érvényesülnek -- nincs szükség újramásolásra.

### 3. lépés: A .bikey másolása

Lásd a következő szekciót.

---

## Mod kulcsok (.bikey)

Minden aláírt mod egy `keys/` mappával szállít, amely egy vagy több `.bikey` fájlt tartalmaz. Ezek a fájlok mondják meg a BattlEye-nak, mely PBO aláírásokat fogadja el.

1. Nyisd meg a mod mappáját (pl. `@CF/keys/`)
2. Másolj minden `.bikey` fájlt a szerver gyökér `keys/` könyvtárába

```
DayZServer/
  keys/
    dayz.bikey              # Vanilla -- mindig jelen van
    cf.bikey                # Másolva a @CF/keys/ mappából
    vpp_admintools.bikey    # Másolva a @VPPAdminTools/keys/ mappából
```

A helyes kulcs nélkül minden játékos, aki azt a modot futtatja, ezt kapja: **"Player kicked: Modified data"**.

---

## Betöltési sorrend és függőségek

A modok balról jobbra töltődnek be a `-mod=` paraméterben. A mod `config.cpp` fájlja deklarálja a függőségeit:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Ha a `MyMod` igényli a `CF`-et, akkor a `@CF`-nek **előbb** kell megjelennie, mint a `@MyMod` az indítási paraméterben:

```
-mod=@CF;@MyMod          ✓ helyes
-mod=@MyMod;@CF          ✗ összeomlás vagy hiányzó osztályok
```

**Általános betöltési sorrend minta:**

1. **Keretrendszer modok** -- CF, Community-Online-Tools
2. **Könyvtár modok** -- BuilderItems, bármely megosztott asset csomag
3. **Funkció modok** -- térkép kiegészítések, fegyverek, járművek
4. **Függő modok** -- bármi, ami a fentieket `requiredAddons`-ként listázza

Ha bizonytalan vagy, ellenőrizd a mod Workshop oldalát vagy dokumentációját. A legtöbb mod készítő közzéteszi a szükséges betöltési sorrendet.

---

## Csak szerver vs kliens oldali modok

| Paraméter | Kinek kell | Tipikus példák |
|-----------|-----------|----------------|
| `-mod=` | Szerver + minden kliens | Fegyverek, járművek, térképek, UI modok, ruházat |
| `-servermod=` | Csak szerver | Gazdaság kezelők, naplózó eszközök, admin háttérrendszerek, ütemező szkriptek |

A szabály egyértelmű: ha egy mod **bármilyen** kliens oldali szkriptet, layoutot, textúrát vagy modellt tartalmaz, a `-mod=` paraméterbe kell kerülnie. Ha csak szerver oldali logikát futtat a kliens által soha nem érintett asset-ek nélkül, használd a `-servermod=` paramétert.

Egy csak szerver oldali mod `-mod=`-ba helyezése minden játékost a letöltésre kényszerít. Egy kliens oldali mod `-servermod=`-ba helyezése hiányzó textúrákat, törött UI-t vagy szkript hibákat okoz a kliensnél.

---

## Modok frissítése

### Eljárás

1. **Állítsd le a szervert** -- fájlok frissítése futó szerver mellett sértheti a PBO-kat
2. **Töltsd le újra** SteamCMD-vel:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Másold a frissített .bikey fájlokat** -- a mod készítők időnként cserélik az aláíró kulcsaikat. Mindig másold a friss `.bikey`-t a mod `keys/` mappájából a szerver `keys/` könyvtárába
4. **Indítsd újra a szervert**

Ha szimbolikus linkeket (junction) használtál, a 2. lépés helyben frissíti a mod fájlokat. Ha manuálisan másoltad a fájlokat, újra másolnod kell.

### Kliens oldali frissítések

A Steam Workshop-on feliratkozott játékosok automatikusan megkapják a frissítéseket. Ha frissítesz egy modot a szerveren és egy játékosnak a régi verzió van, aláírás eltérést kap és nem tud csatlakozni, amíg a kliense nem frissül.

---

## Mod konfliktusok hibaelhárítása

### Az RPT napló ellenőrzése

Nyisd meg a legújabb `.RPT` fájlt a `profiles/` mappából. Keresd:

- **"Cannot register"** -- osztálynév ütközés két mod között
- **"Missing addons"** -- egy függőség nincs betöltve (rossz betöltési sorrend vagy hiányzó mod)
- **"Signature verification failed"** -- `.bikey` eltérés vagy hiányzó kulcs

### A szkript napló ellenőrzése

Nyisd meg a legújabb `script_*.log` fájlt a `profiles/` mappából. Keresd:

- **"SCRIPT (E)"** sorok -- szkript hibák, gyakran betöltési sorrend vagy verzió eltérés okozza
- **"Definition of variable ... already exists"** -- két mod definiálja ugyanazt az osztályt

### A probléma izolálása

Ha sok moddal rendelkezel és valami elromlik, tesztelj fokozatosan:

1. Kezdd csak a keretrendszer modokkal (`@CF`)
2. Adj hozzá egyszerre egy modot
3. Indíts el és ellenőrizd a naplókat minden hozzáadás után
4. A hibát okozó mod a tettes

### Két mod ugyanazt az osztályt szerkeszti

Ha két mod egyaránt `modded class PlayerBase`-t használ, az **utolsóként** betöltött (a `-mod=` jobb szélén) nyer. A `super` hívása a másik mod verziójára láncolódik. Ez általában működik, de ha az egyik mod felülír egy metódust a `super` hívása nélkül, a másik mod változtatásai elvesznek.

---

## Gyakori hibák

**Rossz betöltési sorrend.** A szerver összeomlik vagy "Missing addons"-t naplóz, mert egy függőség még nem volt betöltve. Javítás: mozgasd a függőség modot korábbra a `-mod=` listában.

**Elfelejtett `-servermod=` a csak szerver modokhoz.** A játékosok kénytelenek letölteni egy modot, amelyre nincs szükségük. Javítás: mozgasd a csak szerver modokat a `-mod=`-ból a `-servermod=`-ba.

**A `.bikey` fájlok frissítésének elmulasztása mod frissítés után.** A játékosokat "Modified data" üzenettel kirúgja, mert a szerver kulcsa nem egyezik a mod új PBO aláírásaival. Javítás: mindig másold újra a `.bikey` fájlokat modok frissítésekor.

**Mod PBO-k újracsomagolása.** Egy mod PBO fájljainak újracsomagolása megtöri a digitális aláírást, BattlEye kirúgásokat okoz minden játékosnál, és megsérti a legtöbb mod készítő feltételeit. Soha ne csomagolj újra egy modot, amelyet nem te készítettél.

**Workshop elérési utak és helyi elérési utak keverése.** Egyes modokhoz a nyers Workshop numerikus elérési út, másokhoz elnevezett mappák használata zavart okoz frissítéskor. Válassz egy megközelítést -- a szimbolikus linkek a legtisztább megoldás.

**Szóközök a mod elérési utakban.** Egy `-mod=@My Mod` típusú elérési út megtöri az elemzést. Nevezd át a mod mappákat a szóközök elkerülése érdekében, vagy tedd az egész paramétert idézőjelbe: `-mod="@My Mod;@CF"`.

**Elavult mod a szerveren, frissített a kliensnél (vagy fordítva).** Verzió eltérés megakadályozza a csatlakozást. Tartsd szinkronban a szerver és Workshop verziókat. Frissítsd egyszerre az összes modot és a szervert.

---

[Kezdőlap](../README.md) | [<< Előző: Hozzáférés vezérlés](09-access-control.md) | [Következő: Hibaelhárítás >>](11-troubleshooting.md)
