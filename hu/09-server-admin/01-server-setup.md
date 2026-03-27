# Chapter 9.1: Szerver telepítés és első indítás

[Kezdőlap](../README.md) | **Szerver telepítés** | [Következő: Könyvtárszerkezet >>](02-directory-structure.md)

---

> **Összefoglaló:** Telepíts egy DayZ Standalone dedikált szervert a nulláról SteamCMD segítségével, indítsd el minimális konfigurációval, ellenőrizd, hogy megjelenik-e a szerver böngészőben, és csatlakozz játékosként. Ez a fejezet a hardverkövetelményektől a leggyakoribb első indítási hibák javításáig mindent lefed.

---

## Tartalomjegyzék

- [Előfeltételek](#előfeltételek)
- [A SteamCMD telepítése](#a-steamcmd-telepítése)
- [A DayZ szerver telepítése](#a-dayz-szerver-telepítése)
- [Könyvtár a telepítés után](#könyvtár-a-telepítés-után)
- [Első indítás minimális konfigurációval](#első-indítás-minimális-konfigurációval)
- [A szerver futásának ellenőrzése](#a-szerver-futásának-ellenőrzése)
- [Csatlakozás játékosként](#csatlakozás-játékosként)
- [Gyakori első indítási problémák](#gyakori-első-indítási-problémák)

---

## Előfeltételek

### Hardver

| Komponens | Minimum | Ajánlott |
|-----------|---------|----------|
| CPU | 4 mag, 2.4 GHz | 6+ mag, 3.5 GHz |
| RAM | 8 GB | 16 GB |
| Lemez | 20 GB SSD | 40 GB NVMe SSD |
| Hálózat | 10 Mbps feltöltés | 50+ Mbps feltöltés |
| OS | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

A DayZ szerver egymagos a játéklogika szempontjából. Az órajel fontosabb, mint a magok száma.

### Szoftver

- **SteamCMD** -- a Steam parancssoros kliens dedikált szerverek telepítéséhez
- **Visual C++ Redistributable 2019** (Windows) -- a `DayZServer_x64.exe` futtatásához szükséges
- **DirectX Runtime** (Windows) -- általában már telepítve van
- **2302-2305 UDP** portok továbbítva a routeren/tűzfalon

---

## A SteamCMD telepítése

### Windows

1. Töltsd le a SteamCMD-t innen: https://developer.valvesoftware.com/wiki/SteamCMD
2. Csomagold ki a `steamcmd.exe` fájlt egy állandó mappába, pl. `C:\SteamCMD\`
3. Futtasd egyszer a `steamcmd.exe` fájlt -- automatikusan frissíti magát

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## A DayZ szerver telepítése

A DayZ szerver Steam App ID-ja **223350**. A DayZ-t birtokló Steam fiók nélkül is telepítheted.

### Egysoros telepítés (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Egysoros telepítés (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Frissítési szkript

Készíts egy szkriptet, amit minden frissítéskor újrafuttathatsz:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Frissítés kész.
pause
```

A `validate` jelző minden fájlt ellenőriz a sérülések szempontjából. Friss telepítésnél 2-3 GB letöltésre számíts.

---

## Könyvtár a telepítés után

A telepítés után a szerver gyökérkönyvtára így néz ki:

```
DayZServer/
  DayZServer_x64.exe        # A szerver futtatható fájl
  serverDZ.cfg               # Fő szerver konfiguráció
  dayzsetting.xml            # Megjelenítési/videó beállítások (dedikált szervernél nem releváns)
  addons/                    # Vanilla PBO fájlok (ai.pbo, animals.pbo, stb.)
  battleye/                  # BattlEye csalás elleni védelem (BEServer_x64.dll)
  dta/                       # Motor alap adatok (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Aláírás kulcsok (dayz.bikey a vanillához)
  logs/                      # Motor naplófájlok (kapcsolat, tartalom, hang)
  mpmissions/                # Küldetés mappák
    dayzOffline.chernarusplus/   # Chernarus küldetés
    dayzOffline.enoch/           # Livonia küldetés (DLC)
    dayzOffline.sakhal/          # Sakhal küldetés (DLC)
  profiles/                  # Futásidejű kimenet: RPT naplók, szkript naplók, játékos DB
  ban.txt                    # Kitiltott játékosok listája (Steam64 ID-k)
  whitelist.txt              # Engedélyezett játékosok (Steam64 ID-k)
  steam_appid.txt            # Tartalmazza: "221100"
```

Fontos tudnivalók:
- **Szerkesztendő:** `serverDZ.cfg` és a `mpmissions/` mappán belüli fájlok.
- **Soha ne szerkeszd** az `addons/` vagy `dta/` mappák fájljait -- minden frissítésnél felülíródnak.
- **Mod PBO-k** a szerver gyökérbe vagy egy almappába kerülnek (egy későbbi fejezetben tárgyaljuk).
- **A `profiles/`** az első indításkor jön létre, és tartalmazza a szkript naplókat és összeomlási mentéseket.

---

## Első indítás minimális konfigurációval

### 1. lépés: A serverDZ.cfg szerkesztése

Nyisd meg a `serverDZ.cfg` fájlt egy szövegszerkesztőben. Első teszthez használd a lehető legegyszerűbb konfigurációt:

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### 2. lépés: A szerver indítása

Nyiss egy Parancssort a szerver könyvtárban, és futtasd:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Jelző | Cél |
|-------|-----|
| `-config=serverDZ.cfg` | Konfigurációs fájl elérési útja |
| `-port=2302` | Fő játékport (a 2303-2305 portokat is használja) |
| `-profiles=profiles` | Kimeneti mappa naplókhoz és játékos adatokhoz |
| `-dologs` | Szerver naplózás engedélyezése |
| `-adminlog` | Admin műveletek naplózása |
| `-netlog` | Hálózati események naplózása |
| `-freezecheck` | Automatikus újraindítás lefagyás észlelésekor |

### 3. lépés: Várakozás az inicializálásra

A szerver teljes indítása 30-90 másodpercig tart. Figyeld a konzol kimenetét. Amikor ilyen sort látsz:

```
BattlEye Server: Initialized (v1.xxx)
```

...a szerver készen áll a csatlakozásra.

---

## A szerver futásának ellenőrzése

### 1. módszer: Szkript napló

Ellenőrizd a `profiles/` mappát, keress egy `script_YYYY-MM-DD_HH-MM-SS.log` nevű fájlt. Nyisd meg és keresd:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Ezek a sorok megerősítik, hogy a gazdaság inicializálódott és a küldetés betöltődött.

### 2. módszer: RPT fájl

A `.RPT` fájl a `profiles/` mappában a motor szintű kimenetet mutatja. Keresd:

```
Dedicated host created.
BattlEye Server: Initialized
```

### 3. módszer: Steam szerver böngésző

Nyisd meg a Steamet, menj a **Nézet > Játékszerverek > Kedvencek** menüpontra, kattints a **Szerver hozzáadása** gombra, írd be a `127.0.0.1:2302` címet (vagy a nyilvános IP-det), és kattints a **Játékok keresése ezen a címen** gombra. Ha a szerver megjelenik, fut és elérhető.

### 4. módszer: Lekérdezési port

Használj külső eszközt, mint a https://www.battlemetrics.com/ vagy a `gamedig` npm csomagot a 27016-os port lekérdezéséhez (Steam lekérdezési port = játékport + 24714).

---

## Csatlakozás játékosként

### Ugyanarról a gépről

1. Indítsd el a DayZ-t (ne a DayZ Servert -- a normál játék klienst)
2. Nyisd meg a **Szerver böngészőt**
3. Menj a **LAN** vagy **Kedvencek** fülre
4. Add hozzá a `127.0.0.1:2302` címet a kedvencekhez
5. Kattints a **Csatlakozás** gombra

Ha a klienst és a szervert ugyanazon a gépen futtatod, használd a `DayZDiag_x64.exe` fájlt (a diagnosztikai kliens) a kereskedelmi kliens helyett. Indítsd így:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### Másik gépről

Használd a szervered **nyilvános IP** vagy **LAN IP** címét attól függően, hogy a kliens ugyanazon a hálózaton van-e. A 2302-2305 UDP portoknak továbbítva kell lenniük.

---

## Gyakori első indítási problémák

### A szerver elindul, de azonnal bezárul

**Ok:** Hiányzó Visual C++ Redistributable vagy szintaktikai hiba a `serverDZ.cfg` fájlban.

**Javítás:** Telepítsd a VC++ Redist 2019-et (x64). Ellenőrizd a `serverDZ.cfg` fájlt hiányzó pontosvesszők szempontjából -- minden paramétersornak `;`-vel kell végződnie.

### "BattlEye initialization failed"

**Ok:** A `battleye/` mappa hiányzik, vagy a vírusirtó blokkolja a `BEServer_x64.dll` fájlt.

**Javítás:** Validáld újra a szerverfájlokat SteamCMD-vel. Adj hozzá egy vírusirtó kivételt a teljes szerver mappára.

### A szerver fut, de nem jelenik meg a böngészőben

**Ok:** A portok nincsenek továbbítva, vagy a Windows tűzfal blokkolja a futtatható fájlt.

**Javítás:**
1. Adj hozzá egy Windows tűzfal bejövő szabályt a `DayZServer_x64.exe` fájlhoz (engedélyezz minden UDP-t)
2. Továbbítsd a **2302-2305 UDP** portokat a routeren
3. Ellenőrizd egy külső portellenőrzővel, hogy a 2302 UDP port nyitva van a nyilvános IP-den

### "Version Mismatch" csatlakozáskor

**Ok:** A szerver és a kliens eltérő verziójú.

**Javítás:** Frissítsd mindkettőt. Futtasd a SteamCMD frissítési parancsot a szerverhez. A kliens automatikusan frissül a Steamen keresztül.

### Nem jelenik meg zsákmány

**Ok:** Az `init.c` fájl hiányzik, vagy a Hive nem tudott inicializálódni.

**Javítás:** Ellenőrizd, hogy létezik a `mpmissions/dayzOffline.chernarusplus/init.c` és tartalmazza a `CreateHive()` hívást. Ellenőrizd a szkript naplót hibák szempontjából.

### A szerver 100%-on használ egy CPU magot

Ez normális. A DayZ szerver egymagos. Ne futtass több szerverpéldányt ugyanazon a magon -- használj processzor affinitást vagy különálló gépeket.

### A játékosok varjúként jelennek meg / Betöltésnél elakadnak

**Ok:** A `serverDZ.cfg` fájlban lévő küldetés sablon nem egyezik a `mpmissions/` mappában lévő mappával.

**Javítás:** Ellenőrizd a template értéket. Pontosan meg kell egyeznie a mappa nevével:

```cpp
template = "dayzOffline.chernarusplus";  // Meg kell egyeznie a mpmissions/ mappa nevével
```

---

**[Kezdőlap](../README.md)** | **Következő:** [Könyvtárszerkezet >>](02-directory-structure.md)
