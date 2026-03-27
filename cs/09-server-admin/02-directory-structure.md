# Chapter 9.2: Adresarova struktura a slozka mise

[Domu](../README.md) | [<< Predchozi: Nastaveni serveru](01-server-setup.md) | **Adresarova struktura** | [Dalsi: Reference serverDZ.cfg >>](03-server-cfg.md)

---

> **Shrnuti:** Kompletni pruvodce kazdym souborem a slozkou v adresari serveru DayZ a ve slozce mise. Vedet, co ktery soubor dela -- a ktere je bezpecne upravovat -- je nezbytne pred zasahem do lootove ekonomiky nebo pridavanim modu.

---

## Obsah

- [Adresarova struktura nejvyssi urovne serveru](#adresarova-struktura-nejvyssi-urovne-serveru)
- [Slozka addons/](#slozka-addons)
- [Slozka keys/](#slozka-keys)
- [Slozka profiles/](#slozka-profiles)
- [Slozka mpmissions/](#slozka-mpmissions)
- [Struktura slozky mise](#struktura-slozky-mise)
- [Slozka db/ -- jadro ekonomiky](#slozka-db----jadro-ekonomiky)
- [Slozka env/ -- uzemi zvirat](#slozka-env----uzemi-zvirat)
- [Slozka storage_1/ -- persistence](#slozka-storage_1----persistence)
- [Soubory mise nejvyssi urovne](#soubory-mise-nejvyssi-urovne)
- [Ktere soubory upravovat a ktere ne](#ktere-soubory-upravovat-a-ktere-ne)

---

## Adresarova struktura nejvyssi urovne serveru

```
DayZServer/
  DayZServer_x64.exe          # Spustitelny soubor serveru
  serverDZ.cfg                 # Hlavni konfigurace serveru (nazev, heslo, mody, cas)
  dayzsetting.xml              # Nastaveni vykresleni (nerelevantni pro dedickovane servery)
  ban.txt                      # Zablokovana Steam64 ID, jedno na radek
  whitelist.txt                # Steam64 ID na whitelistu, jedno na radek
  steam_appid.txt              # Obsahuje "221100" -- neupravujte
  dayz.gproj                   # Soubor projektu Workbench -- neupravujte
  addons/                      # Vanilkove herní PBO soubory
  battleye/                    # Soubory anti-cheatu
  config/                      # Konfigurace Steamu (config.vdf)
  dta/                         # Zakladni PBO enginu (skripty, GUI, grafika)
  keys/                        # Klice pro overeni podpisu (soubory .bikey)
  logs/                        # Logy na urovni enginu
  mpmissions/                  # Vsechny slozky misi
  profiles/                    # Vystup za behu (logy skriptu, databaze hracu, dumpy padu)
  server_manager/              # Nastroje pro spravu serveru
```

---

## Slozka addons/

Obsahuje veskerý vanilkovy herní obsah zabaleny jako PBO soubory. Kazdy PBO ma odpovidajici podpisovy soubor `.bisign`:

```
addons/
  ai.pbo                       # Skripty chovani AI
  ai.pbo.dayz.bisign           # Podpis pro ai.pbo
  animals.pbo                  # Definice zvirat
  characters_backpacks.pbo     # Modely/konfigurace batohu
  characters_belts.pbo         # Modely predmetu na opasku
  weapons_firearms.pbo         # Modely/konfigurace zbrani
  ... (100+ PBO souboru)
```

**Nikdy tyto soubory neupravujte.** Jsou prepsany pri kazde aktualizaci serveru pres SteamCMD. Mody prepisuji vanilkove chovani pomoci systemu `modded` trid, ne zmenou PBO souboru.

---

## Slozka keys/

Obsahuje verejne klicove soubory `.bikey` pouzivane k overeni podpisu modu:

```
keys/
  dayz.bikey                   # Vanilkovy podpisovy klic (vzdy pritomen)
```

Kdyz pridavate mod, zkopirujte jeho soubor `.bikey` do teto slozky. Server pouziva `verifySignatures = 2` v `serverDZ.cfg` k odmitani jakehokoli PBO, ktere nema odpovidajici `.bikey` v teto slozce.

Pokud hrac nahraje mod, jehoz klic neni ve vasi slozce `keys/`, dostane vyhazov s chybou **"Signature check failed"**.

---

## Slozka profiles/

Vytvori se pri prvním spusteni serveru. Obsahuje vystup za behu:

```
profiles/
  BattlEye/                              # Logy a bany BE
  DataCache/                             # Kachovana data
  Users/                                 # Soubory preferenci jednotlivych hracu
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Adminsky log
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Zprava enginu (informace o padech, varovani)
  script_2026-03-08_11-34-35.log           # Log skriptu (vas primarni nastroj pro ladeni)
```

**Log skriptu** je zde nejdulezitejsi soubor. Kazde volani `Print()`, kazda chyba skriptu a kazda zprava o nacitani modu se zapise sem. Kdyz neco nefunguje, tady se divate jako prvni.

Soubory logu se casem hromadi. Stare logy nejsou automaticky mazany.

---

## Slozka mpmissions/

Obsahuje jednu podslozku pro kazdou mapu:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (zdarma)
  dayzOffline.enoch/            # Livonie (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

Format nazvu slozky je `<nazevMise>.<nazevTerenu>`. Hodnota `template` v `serverDZ.cfg` musi presne odpovidat jednomu z techto nazvu slozek.

---

## Struktura slozky mise

Slozka mise pro Chernarus (`mpmissions/dayzOffline.chernarusplus/`) obsahuje:

```
dayzOffline.chernarusplus/
  init.c                         # Vstupni skript mise
  db/                            # Zakladni soubory ekonomiky
  env/                           # Definice uzemi zvirat
  storage_1/                     # Data persistence (hraci, stav sveta)
  cfgeconomycore.xml             # Korenove tridy ekonomiky a nastaveni logovani
  cfgenvironment.xml             # Odkazy na soubory uzemi zvirat
  cfgeventgroups.xml             # Definice skupin udalosti
  cfgeventspawns.xml             # Presne pozice spawnu udalosti (vozidla atd.)
  cfgeffectarea.json             # Definice kontaminovanych zon
  cfggameplay.json               # Ladeni gameplayu (stamina, poskozeni, stavba)
  cfgignorelist.xml              # Predmety zcela vyloucene z ekonomiky
  cfglimitsdefinition.xml        # Definice platnych tagu kategorie/pouziti/hodnoty
  cfglimitsdefinitionuser.xml    # Uzivatelsky definovane vlastni definice tagu
  cfgplayerspawnpoints.xml       # Lokace spawnu novych hracu
  cfgrandompresets.xml           # Znovupouzitelne definice lootovych poolu
  cfgspawnabletypes.xml          # Predpripojene predmety a naklad na spawnovanych entitach
  cfgundergroundtriggers.json    # Triggery podzemnich oblasti
  cfgweather.xml                 # Konfigurace pocasi
  areaflags.map                  # Data ploskych flagu (binarni)
  mapclusterproto.xml            # Definice prototypu mapovych klustru
  mapgroupcluster.xml            # Definice klustru skupin budov
  mapgroupcluster01.xml          # Data klustru (cast 1)
  mapgroupcluster02.xml          # Data klustru (cast 2)
  mapgroupcluster03.xml          # Data klustru (cast 3)
  mapgroupcluster04.xml          # Data klustru (cast 4)
  mapgroupdirt.xml               # Pozice lootu na zemi
  mapgrouppos.xml                # Pozice mapovych skupin
  mapgroupproto.xml              # Definice prototypu pro mapove skupiny
```

---

## Slozka db/ -- jadro ekonomiky

Toto je srdce Centralni ekonomiky. Pet souboru ridi, co se spawnuje, kde a kolik:

```
db/
  types.xml        # KLICOVY soubor: definuje pravidla spawnu kazdeho predmetu
  globals.xml      # Globalni parametry ekonomiky (casovace, limity, pocty)
  events.xml       # Dynamicke udalosti (zvírata, vozidla, helikoptery)
  economy.xml      # Prepinace subsystemu ekonomiky (loot, zvírata, vozidla)
  messages.xml     # Planovane zpravy serveru hracum
```

### types.xml

Definuje pravidla spawnu pro **kazdy predmet** ve hre. S priblizne 23 000 radky jde zdaleka o nejvetsi soubor ekonomiky. Kazdy zaznam urcuje, kolik kopii predmetu by melo na mape existovat, kde se muze spawnit a jak dlouho pretrva. Podrobnosti najdete v [Kapitole 9.4](04-loot-economy.md).

### globals.xml

Globalni parametry ovlivnujici celou ekonomiku: pocty zombie, pocty zvirat, casovace cisteni, rozsahy poskozeni lootu, casovani respawnu. Celkem 33 parametru. Kompletni referenci najdete v [Kapitole 9.4](04-loot-economy.md).

### events.xml

Definuje dynamicke spawnove udalosti pro zvírata a vozidla. Kazda udalost specifikuje nominalni pocet, omezeni spawnu a detske varianty. Napriklad udalost `VehicleCivilianSedan` spawnuje 8 sedanu po mape ve 3 barevnych variantach.

### economy.xml

Hlavni prepinace subsystemu ekonomiky:

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

| Priznak | Vyznam |
|------|---------|
| `init` | Spawnovat predmety pri prvnim spusteni serveru |
| `load` | Nacist ulozeny stav z persistence |
| `respawn` | Povolit respawn predmetu po cisteni |
| `save` | Ulozit stav do souboru persistence |

### messages.xml

Planovane zpravy vysilane vsem hracum. Podporuje odpocitavaci casovace, intervaly opakovani, zpravy pri pripojeni a varovani pred vypnutim:

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

Pouzijte `#name` pro nazev serveru a `#tmin` pro zbyvajici cas v minutach.

---

## Slozka env/ -- uzemi zvirat

Obsahuje XML soubory definujici, kde se kazdy druh zvírete muze spawnit:

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

Tyto soubory obsahuji stovky souradnicovych bodu definujicich uzemi po cele mape. Odkazuje na ne `cfgenvironment.xml`. Tyto soubory zridka potrebujete upravovat, pokud nechcete zmenit, kde se zvírata nebo zombie geograficky spawnuji.

---

## Slozka storage_1/ -- persistence

Uchovava perzistentni stav serveru mezi restarty:

```
storage_1/
  players.db         # SQLite databaze vsech postav hracu
  spawnpoints.bin    # Binarni data spawnovacich bodu
  backup/            # Automaticke zalohy dat persistence
  data/              # Stav sveta (umistene predmety, stavba bazi, vozidla)
```

**Nikdy neupravujte `players.db` behem behu serveru.** Jde o SQLite databazi zamcenou procesem serveru. Pokud potrebujete vymazat postavy, nejprve zastavte server a soubor smazte nebo prejmennujte.

Pro **uplny wipe** zastavte server a smazte celou slozku `storage_1/`. Server ji vytvori znovu pri dalsim spusteni s cistym svetem.

Pro **castecny wipe** (zachovat postavy, resetovat loot):
1. Zastavte server
2. Smazte soubory v `storage_1/data/`, ale ponechte `players.db`
3. Restartujte

---

## Soubory mise nejvyssi urovne

### cfgeconomycore.xml

Registruje korenove tridy ekonomiky a konfiguruje logovani CE:

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

Nastavte `log_ce_lootspawn` na `"true"` pri ladeni problemu se spawnem predmetu. Produkuje detailni vystup v RPT logu zobrazujici, ktere predmety se CE pokousi spawnit a proc uspely nebo selhaly.

### cfglimitsdefinition.xml

Definuje platne hodnoty pro elementy `<category>`, `<usage>`, `<value>` a `<tag>` pouzivane v `types.xml`:

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

Pokud pouzijete tag `<usage>` nebo `<value>` v `types.xml`, ktery zde neni definovany, predmet se tiše nespawni.

### cfgignorelist.xml

Predmety uvedene zde jsou zcela vylouceny z ekonomiky, i kdyz maji zaznamy v `types.xml`:

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

Pouziva se pro predmety, ktere existuji v kodu hry, ale nemaji se prirozene spawnovat (nedokoncene predmety, zastaraly obsah, sezonni predmety mimo sezonu).

### cfggameplay.json

JSON soubor, ktery prepisuje parametry gameplayu. Ovlada staminu, pohyb, poskozeni bazi, pocasi, teplotu, obstrukci zbrani, topeni a dalsi. Tento soubor je volitelny -- pokud chybi, server pouziva vychozi hodnoty.

### cfgplayerspawnpoints.xml

Definuje, kde se nove spawnnuti hraci objevi na mape, s omezenimi vzdalenosti od nakazenych, ostatnich hracu a budov.

### cfgeventspawns.xml

Obsahuje presne svetove souradnice, kde se mohou spawnit udalosti (vozidla, helikopterove zriceniny atd.). Kazdy nazev udalosti z `events.xml` ma seznam platnych pozic:

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

Atribut `a` je uhel rotace ve stupních.

---

## Ktere soubory upravovat a ktere ne

| Soubor / slozka | Bezpecne upravovat? | Poznamky |
|---------------|:---:|-------|
| `serverDZ.cfg` | Ano | Hlavni konfigurace serveru |
| `db/types.xml` | Ano | Pravidla spawnu predmetu -- vas nejcastejsi zasah |
| `db/globals.xml` | Ano | Parametry ladeni ekonomiky |
| `db/events.xml` | Ano | Udalosti spawnu vozidel/zvirat |
| `db/economy.xml` | Ano | Prepinace subsystemu ekonomiky |
| `db/messages.xml` | Ano | Zpravy vysilane serverem |
| `cfggameplay.json` | Ano | Ladeni gameplayu |
| `cfgspawnabletypes.xml` | Ano | Prednastaveni prislusenstvi/nakladu |
| `cfgrandompresets.xml` | Ano | Definice lootovych poolu |
| `cfglimitsdefinition.xml` | Ano | Pridani vlastnich tagu pouziti/hodnoty |
| `cfgplayerspawnpoints.xml` | Ano | Lokace spawnu hracu |
| `cfgeventspawns.xml` | Ano | Souradnice spawnu udalosti |
| `cfgignorelist.xml` | Ano | Vylouceni predmetu z ekonomiky |
| `cfgweather.xml` | Ano | Vzory pocasi |
| `cfgeffectarea.json` | Ano | Kontaminovane zony |
| `init.c` | Ano | Vstupni skript mise |
| `addons/` | **Ne** | Prepsano pri aktualizaci |
| `dta/` | **Ne** | Zakladni data enginu |
| `keys/` | Pouze pridavat | Kopirovani souboru `.bikey` modu sem |
| `storage_1/` | Pouze mazat | Persistence -- nerucne neupravujte |
| `battleye/` | **Ne** | Anti-cheat -- nesahejte |
| `mapgroup*.xml` | Opatrne | Pozice lootu v budovach -- pouze pokrocila uprava |

---

**Predchozi:** [Nastaveni serveru](01-server-setup.md) | [Domu](../README.md) | **Dalsi:** [Reference serverDZ.cfg >>](03-server-cfg.md)
