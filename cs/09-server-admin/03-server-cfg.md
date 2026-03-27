# Chapter 9.3: Kompletni reference serverDZ.cfg

[Domu](../README.md) | [<< Predchozi: Adresarova struktura](02-directory-structure.md) | **Reference serverDZ.cfg** | [Dalsi: Lootova ekonomika podrobne >>](04-loot-economy.md)

---

> **Shrnuti:** Kazdy parametr v `serverDZ.cfg` zdokumentovany s jeho ucelem, platnymi hodnotami a vychozim chovanim. Tento soubor ridi identitu serveru, sitova nastaveni, pravidla gameplayu, zrychleni casu a vyber mise.

---

## Obsah

- [Format souboru](#format-souboru)
- [Identita serveru](#identita-serveru)
- [Sit a zabezpeceni](#sit-a-zabezpeceni)
- [Pravidla gameplayu](#pravidla-gameplayu)
- [Cas a pocasi](#cas-a-pocasi)
- [Vykon a prihlasovaci fronta](#vykon-a-prihlasovaci-fronta)
- [Persistence a instance](#persistence-a-instance)
- [Vyber mise](#vyber-mise)
- [Kompletni priklad souboru](#kompletni-priklad-souboru)
- [Spousteci parametry prepisujici konfiguraci](#spousteci-parametry-prepisujici-konfiguraci)

---

## Format souboru

`serverDZ.cfg` pouziva konfiguracni format Bohemia (podobny C). Pravidla:

- Kazde prirazeni parametru konci **strednikem** `;`
- Retezce jsou uzavreny v **uvozovkach** `""`
- Komentare pouzivaji `//` pro jednoradkove
- Blok `class Missions` pouziva slozene zavorky `{}` a konci `};`
- Soubor musi byt kodovan v UTF-8 nebo ANSI -- bez BOM

Chybejici strednik zpusobi, ze server tiše selze nebo ignoruje nasledujici parametry.

---

## Identita serveru

```cpp
hostname = "My DayZ Server";         // Nazev serveru zobrazeny v prohlizeci
password = "";                       // Heslo pro pripojeni (prazdne = verejny)
passwordAdmin = "";                  // Heslo pro adminovo prihlaseni pres hernі konzoli
description = "";                    // Popis zobrazeny v detailech prohlizece serveru
```

| Parametr | Typ | Vychozi | Poznamky |
|-----------|------|---------|-------|
| `hostname` | string | `""` | Zobrazeno v prohlizeci serveru. Maximalne ~100 znaku. |
| `password` | string | `""` | Ponechte prazdne pro verejny server. Hraci musi toto zadat pro pripojeni. |
| `passwordAdmin` | string | `""` | Pouziva se s prikazem `#login` ve hre. **Nastavte na kazdem serveru.** |
| `description` | string | `""` | Viceradkove popisy nejsou podporovany. Udrzujte kratke. |

---

## Sit a zabezpeceni

```cpp
maxPlayers = 60;                     // Maximalni pocet hracskych slotu
verifySignatures = 2;                // Overeni podpisu PBO (podporovano pouze 2)
forceSameBuild = 1;                  // Vyzadovat shodnou verzi klient/server
enableWhitelist = 0;                 // Povolit/zakazat whitelist
disableVoN = 0;                      // Zakazat hlasovy chat
vonCodecQuality = 20;               // Kvalita zvuku VoN (0-30)
guaranteedUpdates = 1;               // Sitovy protokol (vzdy pouzijte 1)
```

| Parametr | Typ | Platne hodnoty | Vychozi | Poznamky |
|-----------|------|-------------|---------|-------|
| `maxPlayers` | int | 1-60 | 60 | Ovlivnuje spotreby RAM. Kazdy hrac prida ~50-100 MB. |
| `verifySignatures` | int | 2 | 2 | Podporovana je pouze hodnota 2. Overuje PBO soubory oproti klicum `.bisign`. |
| `forceSameBuild` | int | 0, 1 | 1 | Kdyz je 1, klienti musi mit presne stejnou verzi spustitelneho souboru jako server. Vzdy ponechte na 1. |
| `enableWhitelist` | int | 0, 1 | 0 | Kdyz je 1, pripojit se mohou pouze Steam64 ID uvedena v `whitelist.txt`. |
| `disableVoN` | int | 0, 1 | 0 | Nastavte na 1 pro uplne zakazani hlasoveho chatu ve hre. |
| `vonCodecQuality` | int | 0-30 | 20 | Vyssi hodnoty znamenaji lepsi kvalitu hlasu, ale vetsi spotrbu sirky pasma. 20 je dobry kompromis. |
| `guaranteedUpdates` | int | 1 | 1 | Nastaveni sitoveho protokolu. Vzdy pouzijte 1. |

### Shard ID

```cpp
shardId = "123abc";                  // Sest alfanumerickych znaku pro privatni shardy
```

| Parametr | Typ | Vychozi | Poznamky |
|-----------|------|---------|-------|
| `shardId` | string | `""` | Pouziva se pro servery s privatnim hive. Hraci na serverech se stejnym `shardId` sdileji data postav. Ponechte prazdne pro verejny hive. |

---

## Pravidla gameplayu

```cpp
disable3rdPerson = 0;               // Zakazat kameru treti osoby
disableCrosshair = 0;               // Zakazat zamerovac
disablePersonalLight = 1;           // Zakazat ambientni svetlo hrace
lightingConfig = 0;                 // Jas v noci (0 = svetlejsi, 1 = tmavsi)
```

| Parametr | Typ | Platne hodnoty | Vychozi | Poznamky |
|-----------|------|-------------|---------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | Nastavte na 1 pro servery pouze s prvni osobou. Toto je nejcastejsi "hardcore" nastaveni. |
| `disableCrosshair` | int | 0, 1 | 0 | Nastavte na 1 pro odstraneni zamerovace. Casto kombinovano s `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | "Osobni svetlo" je jemna zare kolem hrace v noci. Vetsina serveru ho zakazuje (hodnota 1) pro realismus. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = svetlejsi noci (viditelne mesicni svetlo). 1 = uhelnate tmavy noci (vyzaduje baterku/NVG). |

---

## Cas a pocasi

```cpp
serverTime = "SystemTime";                 // Pocatecni cas
serverTimeAcceleration = 12;               // Nasobitel rychlosti casu (0-24)
serverNightTimeAcceleration = 1;           // Nasobitel rychlosti nocniho casu (0.1-64)
serverTimePersistent = 0;                  // Ulozit cas mezi restarty
```

| Parametr | Typ | Platne hodnoty | Vychozi | Poznamky |
|-----------|------|-------------|---------|-------|
| `serverTime` | string | `"SystemTime"` nebo `"RRRR/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` pouziva mistni hodiny pocitace. Nastavte fixni cas jako `"2024/9/15/12/0"` pro trvale denni server. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Nasobitel herniho casu. Při 12 trva cely 24hodinovy cyklus 2 realne hodiny. Pri 1 je cas realtimovy. Pri 24 uplyne cely den za 1 hodinu. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Nasobeno `serverTimeAcceleration`. Pri hodnote 4 se zrychlenim 12 probiha noc rychlosti 48x (velmi kratke noci). |
| `serverTimePersistent` | int | 0, 1 | 0 | Kdyz je 1, server ukla svuj herní cas na disk a po restartu v nem pokracuje. Kdyz je 0, cas se pri kazdem restartu resetuje na `serverTime`. |

### Bezne konfigurace casu

**Vzdy den:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Rychly cyklus dne/noci (2hodinove dny, kratke noci):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Realtimovy den/noc:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Vykon a prihlasovaci fronta

```cpp
loginQueueConcurrentPlayers = 5;     // Pocet hracu zpracovavanych soucasne behem prihlaseni
loginQueueMaxPlayers = 500;          // Maximalni velikost prihlasovaci fronty
```

| Parametr | Typ | Vychozi | Poznamky |
|-----------|------|---------|-------|
| `loginQueueConcurrentPlayers` | int | 5 | Kolik hracu se muze nacitat soucasne. Nizsi hodnoty snizuji zatezove spicky serveru po restartu. Zvyste na 10-15, pokud mate silny hardware a hraci si stezuji na casy ve fronte. |
| `loginQueueMaxPlayers` | int | 500 | Pokud jiz tolik hracu ceka ve fronte, nova pripojeni jsou odmitnuta. 500 staci pro vetsinu serveru. |

---

## Persistence a instance

```cpp
instanceId = 1;                      // Identifikator instance serveru
storageAutoFix = 1;                  // Automaticka oprava poskozenych souboru persistence
```

| Parametr | Typ | Vychozi | Poznamky |
|-----------|------|---------|-------|
| `instanceId` | int | 1 | Identifikuje instanci serveru. Data persistence se ukladaji do `storage_<instanceId>/`. Pokud provozujete vice serveru na stejnem pocitaci, dejte kazdemu jiny `instanceId`. |
| `storageAutoFix` | int | 1 | Kdyz je 1, server kontroluje soubory persistence pri spusteni a poskozene nahradi prazdnymi soubory. Vzdy ponechte na 1. |

---

## Vyber mise

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

Hodnota `template` musi presne odpovidat nazvu slozky uvnitr `mpmissions/`. Dostupne vanilkove mise:

| Sablona | Mapa | Vyzaduje DLC |
|----------|-----|:---:|
| `dayzOffline.chernarusplus` | Chernarus | Ne |
| `dayzOffline.enoch` | Livonie | Ano |
| `dayzOffline.sakhal` | Sakhal | Ano |

Vlastni mise (napr. od modu nebo komunitnich map) pouzivaji svuj vlastni nazev sablony. Slozka musi existovat v `mpmissions/`.

---

## Kompletni priklad souboru

Toto je kompletni vychozi `serverDZ.cfg` se vsemi parametry:

```cpp
hostname = "EXAMPLE NAME";              // Nazev serveru
password = "";                          // Heslo pro pripojeni k serveru
passwordAdmin = "";                     // Heslo pro ziskani admina serveru

description = "";                       // Popis v prohlizeci serveru

enableWhitelist = 0;                    // Povolit/zakazat whitelist (hodnota 0-1)

maxPlayers = 60;                        // Maximalni pocet hracu

verifySignatures = 2;                   // Overuje .pbo oproti souberum .bisign (podporovano pouze 2)
forceSameBuild = 1;                     // Vyzadovat shodnou verzi klient/server (hodnota 0-1)

disableVoN = 0;                         // Povolit/zakazat hlasovy chat (hodnota 0-1)
vonCodecQuality = 20;                   // Kvalita kodeku hlasoveho chatu (hodnoty 0-30)

shardId = "123abc";                     // Sest alfanumerickych znaku pro privatni shard

disable3rdPerson = 0;                   // Prepina pohled treti osoby (hodnota 0-1)
disableCrosshair = 0;                   // Prepina zamerovac (hodnota 0-1)

disablePersonalLight = 1;              // Zakazuje osobni svetlo pro vsechny klienty
lightingConfig = 0;                     // 0 pro svetlejsi, 1 pro tmavsi noc

serverTime = "SystemTime";             // Pocatecni herní cas ("SystemTime" nebo "RRRR/MM/DD/HH/MM")
serverTimeAcceleration = 12;           // Nasobitel rychlosti casu (0-24)
serverNightTimeAcceleration = 1;       // Nasobitel rychlosti nocniho casu (0.1-64), take nasobeno serverTimeAcceleration
serverTimePersistent = 0;              // Ulozit cas mezi restarty (hodnota 0-1)

guaranteedUpdates = 1;                 // Sitovy protokol (vzdy pouzijte 1)

loginQueueConcurrentPlayers = 5;       // Pocet hracu zpracovavanych soucasne behem prihlaseni
loginQueueMaxPlayers = 500;            // Maximalni velikost prihlasovaci fronty

instanceId = 1;                        // ID instance serveru (ovlivnuje pojmenovani slozky storage)

storageAutoFix = 1;                    // Automaticka oprava poskozene persistence (hodnota 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Spousteci parametry prepisujici konfiguraci

Nektera nastaveni mohou byt prepsana parametry prikazoveho radku pri spousteni `DayZServer_x64.exe`:

| Parametr | Prepisuje | Priklad |
|-----------|-----------|---------|
| `-config=` | Cesta ke konfiguracnimu souboru | `-config=serverDZ.cfg` |
| `-port=` | Herní port | `-port=2302` |
| `-profiles=` | Vystupni adresar profilu | `-profiles=profiles` |
| `-mod=` | Klientske mody (oddelene strednikem) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Mody pouze pro server | `-servermod=@MyServerMod` |
| `-BEpath=` | Cesta k BattlEye | `-BEpath=battleye` |
| `-dologs` | Povoleni logovani | -- |
| `-adminlog` | Povoleni adminskeho logovani | -- |
| `-netlog` | Povoleni sitoveho logovani | -- |
| `-freezecheck` | Automaticky restart pri zamrznuti | -- |
| `-cpuCount=` | Pocet pouzitych CPU jader | `-cpuCount=4` |
| `-noFilePatching` | Zakazani file patchingu | -- |

### Kompletni priklad spusteni

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Mody se nacitaji v poradi uvedenem v `-mod=`. Poradi zavislosti je dulezite: pokud Mod B vyzaduje Mod A, uveďte Mod A prvni.

---

**Predchozi:** [Adresarova struktura](02-directory-structure.md) | [Domu](../README.md) | **Dalsi:** [Lootova ekonomika podrobne >>](04-loot-economy.md)
