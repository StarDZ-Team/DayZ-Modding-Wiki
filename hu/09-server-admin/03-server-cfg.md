# Chapter 9.3: serverDZ.cfg teljes referencia

[Kezdőlap](../README.md) | [<< Előző: Könyvtárszerkezet](02-directory-structure.md) | **serverDZ.cfg referencia** | [Következő: Zsákmánygazdaság részletes áttekintés >>](04-loot-economy.md)

---

> **Összefoglaló:** A `serverDZ.cfg` minden paramétere dokumentálva a céljával, érvényes értékeivel és alapértelmezett viselkedésével. Ez a fájl szabályozza a szerver identitását, hálózati beállításait, játékszabályait, időgyorsítást és küldetésválasztást.

---

## Tartalomjegyzék

- [Fájlformátum](#fájlformátum)
- [Szerver identitás](#szerver-identitás)
- [Hálózat és biztonság](#hálózat-és-biztonság)
- [Játékszabályok](#játékszabályok)
- [Idő és időjárás](#idő-és-időjárás)
- [Teljesítmény és bejelentkezési sor](#teljesítmény-és-bejelentkezési-sor)
- [Perzisztencia és példány](#perzisztencia-és-példány)
- [Küldetés kiválasztás](#küldetés-kiválasztás)
- [Teljes példafájl](#teljes-példafájl)
- [Konfigurációt felülíró indítási paraméterek](#konfigurációt-felülíró-indítási-paraméterek)

---

## Fájlformátum

A `serverDZ.cfg` Bohemia konfigurációs formátumát használja (C-hez hasonló). Szabályok:

- Minden paraméter értékadás **pontosvesszővel** `;` végződik
- A szövegeket **dupla idézőjelek** `""` fogják közre
- A megjegyzések `//`-vel kezdődnek (egysoros)
- A `class Missions` blokk kapcsos zárójeleket `{}` használ és `};`-vel végződik
- A fájlnak UTF-8 vagy ANSI kódolásúnak kell lennie -- BOM nélkül

Egy hiányzó pontosvessző miatt a szerver csendben meghiúsulhat vagy figyelmen kívül hagyhatja a következő paramétereket.

---

## Szerver identitás

```cpp
hostname = "My DayZ Server";         // A böngészőben megjelenő szerver név
password = "";                       // Csatlakozási jelszó (üres = nyilvános)
passwordAdmin = "";                  // Admin bejelentkezés jelszava a játékon belüli konzolon
description = "";                    // A szerver böngésző részleteiben megjelenő leírás
```

| Paraméter | Típus | Alapértelmezett | Megjegyzések |
|-----------|-------|-----------------|--------------|
| `hostname` | string | `""` | Megjelenik a szerver böngészőben. Maximum ~100 karakter. |
| `password` | string | `""` | Hagyd üresen nyilvános szerverhez. A játékosoknak meg kell adniuk a csatlakozáshoz. |
| `passwordAdmin` | string | `""` | A `#login` paranccsal használatos a játékban. **Állítsd be minden szerveren.** |
| `description` | string | `""` | Többsoros leírások nem támogatottak. Tartsd rövidnek. |

---

## Hálózat és biztonság

```cpp
maxPlayers = 60;                     // Maximum játékos helyek
verifySignatures = 2;                // PBO aláírás ellenőrzés (csak a 2-es érték támogatott)
forceSameBuild = 1;                  // Egyező kliens/szerver exe verzió megkövetelése
enableWhitelist = 0;                 // Fehérlista engedélyezése/letiltása
disableVoN = 0;                      // Hálózaton keresztüli hang letiltása
vonCodecQuality = 20;               // VoN hangminőség (0-30)
guaranteedUpdates = 1;               // Hálózati protokoll (mindig használj 1-et)
```

| Paraméter | Típus | Érvényes értékek | Alapértelmezett | Megjegyzések |
|-----------|-------|-----------------|-----------------|--------------|
| `maxPlayers` | int | 1-60 | 60 | Hatással van a RAM használatra. Minden játékos ~50-100 MB-ot ad hozzá. |
| `verifySignatures` | int | 2 | 2 | Csak a 2-es érték támogatott. Ellenőrzi a PBO fájlokat a `.bisign` kulcsokkal szemben. |
| `forceSameBuild` | int | 0, 1 | 1 | Ha 1, a klienseknek pontosan meg kell egyezniük a szerver futtatható verziójával. Mindig tartsd 1-en. |
| `enableWhitelist` | int | 0, 1 | 0 | Ha 1, csak a `whitelist.txt`-ben felsorolt Steam64 ID-k csatlakozhatnak. |
| `disableVoN` | int | 0, 1 | 0 | Állítsd 1-re a játékon belüli hangcsevegés teljes letiltásához. |
| `vonCodecQuality` | int | 0-30 | 20 | Magasabb értékek jobb hangminőséget, de több sávszélességet jelentenek. A 20 jó egyensúly. |
| `guaranteedUpdates` | int | 1 | 1 | Hálózati protokoll beállítás. Mindig használj 1-et. |

### Shard ID

```cpp
shardId = "123abc";                  // Hat alfanumerikus karakter privát shardokhoz
```

| Paraméter | Típus | Alapértelmezett | Megjegyzések |
|-----------|-------|-----------------|--------------|
| `shardId` | string | `""` | Privát hive szerverekhez használatos. Az azonos `shardId`-val rendelkező szervereken a játékosok megosztják a karakter adataikat. Hagyd üresen nyilvános hive-hoz. |

---

## Játékszabályok

```cpp
disable3rdPerson = 0;               // Harmadik személyű kamera letiltása
disableCrosshair = 0;               // Célkereszt letiltása
disablePersonalLight = 1;           // Környezeti játékos fény letiltása
lightingConfig = 0;                 // Éjszakai fényerő (0 = világosabb, 1 = sötétebb)
```

| Paraméter | Típus | Érvényes értékek | Alapértelmezett | Megjegyzések |
|-----------|-------|-----------------|-----------------|--------------|
| `disable3rdPerson` | int | 0, 1 | 0 | Állítsd 1-re az első személyű szerverekhez. Ez a leggyakoribb "hardcore" beállítás. |
| `disableCrosshair` | int | 0, 1 | 0 | Állítsd 1-re a célkereszt eltávolításához. Gyakran párosítják a `disable3rdPerson=1` beállítással. |
| `disablePersonalLight` | int | 0, 1 | 1 | A "személyes fény" egy finom ragyogás a játékos körül éjszaka. A legtöbb szerver letiltja (1-es érték) a realizmus kedvéért. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = világosabb éjszakák (holdfény látható). 1 = koromsötét éjszakák (zseblámpa/éjjellátó szükséges). |

---

## Idő és időjárás

```cpp
serverTime = "SystemTime";                 // Kezdeti idő
serverTimeAcceleration = 12;               // Idősebesség szorzó (0-24)
serverNightTimeAcceleration = 1;           // Éjszakai idősebesség szorzó (0.1-64)
serverTimePersistent = 0;                  // Idő mentése újraindítások között
```

| Paraméter | Típus | Érvényes értékek | Alapértelmezett | Megjegyzések |
|-----------|-------|-----------------|-----------------|--------------|
| `serverTime` | string | `"SystemTime"` vagy `"ÉÉÉÉ/HH/NN/ÓÓ/PP"` | `"SystemTime"` | `"SystemTime"` a gép helyi óráját használja. Állíts be fix időt, pl. `"2024/9/15/12/0"` az állandó nappali szerverhez. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Szorzó a játékon belüli időhöz. 12-nél egy teljes 24 órás ciklus 2 valós órát vesz igénybe. 1-nél valós idejű. 24-nél egy teljes nap 1 óra alatt telik el. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Megszorozva a `serverTimeAcceleration` értékével. 4-es értéknél 12-es gyorsítással az éjszaka 48x sebességgel halad (nagyon rövid éjszakák). |
| `serverTimePersistent` | int | 0, 1 | 0 | Ha 1, a szerver lemezre menti a játékon belüli óráját és újraindítás után onnan folytatja. Ha 0, az idő minden újraindításkor visszaáll a `serverTime` értékre. |

### Gyakori idő konfigurációk

**Mindig nappal:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Gyors nappali/éjszakai ciklus (2 órás napok, rövid éjszakák):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Valós idejű nappali/éjszakai ciklus:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Teljesítmény és bejelentkezési sor

```cpp
loginQueueConcurrentPlayers = 5;     // Egyszerre feldolgozott játékosok bejelentkezéskor
loginQueueMaxPlayers = 500;          // Maximum bejelentkezési sor méret
```

| Paraméter | Típus | Alapértelmezett | Megjegyzések |
|-----------|-------|-----------------|--------------|
| `loginQueueConcurrentPlayers` | int | 5 | Hány játékos tölthet be egyszerre. Alacsonyabb értékek csökkentik a szerver terhelési csúcsokat újraindítás után. Emeld 10-15-re, ha erős a hardvered és a játékosok panaszkodnak a várakozási időkre. |
| `loginQueueMaxPlayers` | int | 500 | Ha ennyi játékos már várakozik, az új kapcsolatokat elutasítja. Az 500 megfelelő a legtöbb szerverhez. |

---

## Perzisztencia és példány

```cpp
instanceId = 1;                      // Szerver példány azonosító
storageAutoFix = 1;                  // Sérült perzisztencia fájlok automatikus javítása
```

| Paraméter | Típus | Alapértelmezett | Megjegyzések |
|-----------|-------|-----------------|--------------|
| `instanceId` | int | 1 | Azonosítja a szerver példányt. A perzisztencia adatok a `storage_<instanceId>/` mappában tárolódnak. Ha több szervert futtatsz ugyanazon a gépen, adj mindegyiknek más `instanceId`-t. |
| `storageAutoFix` | int | 1 | Ha 1, a szerver indításkor ellenőrzi a perzisztencia fájlokat és a sérülteket üres fájlokkal helyettesíti. Mindig hagyd 1-en. |

---

## Küldetés kiválasztás

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

A `template` értéknek pontosan meg kell egyeznie az `mpmissions/` mappán belüli mappanevekkel. Elérhető vanilla küldetések:

| Template | Térkép | DLC szükséges |
|----------|--------|:-------------:|
| `dayzOffline.chernarusplus` | Chernarus | Nem |
| `dayzOffline.enoch` | Livonia | Igen |
| `dayzOffline.sakhal` | Sakhal | Igen |

Egyedi küldetések (pl. modoktól vagy közösségi térképektől) saját template nevet használnak. A mappának léteznie kell az `mpmissions/` könyvtárban.

---

## Teljes példafájl

Ez a teljes alapértelmezett `serverDZ.cfg` minden paraméterrel:

```cpp
hostname = "EXAMPLE NAME";              // Szerver név
password = "";                          // Jelszó a szerverhez csatlakozáshoz
passwordAdmin = "";                     // Jelszó az admin jogok megszerzéséhez

description = "";                       // Szerver böngésző leírás

enableWhitelist = 0;                    // Fehérlista engedélyezése/letiltása (0-1 érték)

maxPlayers = 60;                        // Maximum játékosszám

verifySignatures = 2;                   // .pbo fájlok ellenőrzése .bisign fájlokkal (csak a 2-es támogatott)
forceSameBuild = 1;                     // Egyező kliens/szerver verzió megkövetelése (0-1 érték)

disableVoN = 0;                         // Hálózaton keresztüli hang engedélyezése/letiltása (0-1 érték)
vonCodecQuality = 20;                   // Hálózaton keresztüli hang codec minőség (0-30 érték)

shardId = "123abc";                     // Hat alfanumerikus karakter privát shardhoz

disable3rdPerson = 0;                   // 3. személyű nézet kapcsolása (0-1 érték)
disableCrosshair = 0;                   // Célkereszt kapcsolása (0-1 érték)

disablePersonalLight = 1;              // Személyes fény letiltása minden kliensnél
lightingConfig = 0;                     // 0 = világosabb, 1 = sötétebb éjszaka

serverTime = "SystemTime";             // Kezdeti játékon belüli idő ("SystemTime" vagy "ÉÉÉÉ/HH/NN/ÓÓ/PP")
serverTimeAcceleration = 12;           // Idősebesség szorzó (0-24)
serverNightTimeAcceleration = 1;       // Éjszakai idősebesség szorzó (0.1-64), szintén szorzódik a serverTimeAcceleration-nel
serverTimePersistent = 0;              // Idő mentése újraindítások között (0-1 érték)

guaranteedUpdates = 1;                 // Hálózati protokoll (mindig használj 1-et)

loginQueueConcurrentPlayers = 5;       // Egyszerre feldolgozott játékosok bejelentkezéskor
loginQueueMaxPlayers = 500;            // Maximum bejelentkezési sor méret

instanceId = 1;                        // Szerver példány id (hatással van a tároló mappa nevére)

storageAutoFix = 1;                    // Sérült perzisztencia automatikus javítása (0-1 érték)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Konfigurációt felülíró indítási paraméterek

Egyes beállítások felülírhatók parancssori paraméterekkel a `DayZServer_x64.exe` indításakor:

| Paraméter | Felülírja | Példa |
|-----------|-----------|-------|
| `-config=` | Konfigurációs fájl elérési útja | `-config=serverDZ.cfg` |
| `-port=` | Játékport | `-port=2302` |
| `-profiles=` | Profilok kimeneti könyvtára | `-profiles=profiles` |
| `-mod=` | Kliens oldali modok (pontosvesszővel elválasztva) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Csak szerver oldali modok | `-servermod=@MyServerMod` |
| `-BEpath=` | BattlEye elérési útja | `-BEpath=battleye` |
| `-dologs` | Naplózás engedélyezése | -- |
| `-adminlog` | Admin naplózás engedélyezése | -- |
| `-netlog` | Hálózati naplózás engedélyezése | -- |
| `-freezecheck` | Automatikus újraindítás lefagyáskor | -- |
| `-cpuCount=` | Használandó CPU magok | `-cpuCount=4` |
| `-noFilePatching` | Fájl javítás letiltása | -- |

### Teljes indítási példa

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

A modok a `-mod=` paraméterben megadott sorrendben töltődnek be. A függőségi sorrend számít: ha a B mod igényli az A modot, az A modot kell előbb felsorolni.

---

**Előző:** [Könyvtárszerkezet](02-directory-structure.md) | [Kezdőlap](../README.md) | **Következő:** [Zsákmánygazdaság részletes áttekintés >>](04-loot-economy.md)
