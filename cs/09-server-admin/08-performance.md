# Chapter 9.8: Ladeni vykonu

[Domu](../README.md) | [<< Predchozi: Persistence](07-persistence.md) | [Dalsi: Rizeni pristupu >>](09-access-control.md)

---

> **Shrnuti:** Vykon serveru v DayZ se odviij od tri veci: poctu predmetu, dynamickych udalosti a zateze modu/hracu. Tato kapitola pokryva konkretni nastaveni, ktera jsou dulezita, jak diagnostikovat problemy a jaky hardware skutecne pomaha -- vsechno na zaklade realnych komunitnich dat ze 400+ Discord hlaseni o poklesech FPS, lagach a desyncu.

---

## Obsah

- [Co ovlivnuje vykon serveru](#co-ovlivnuje-vykon-serveru)
- [Ladeni globals.xml](#ladeni-globalsxml)
- [Ladeni ekonomiky pro vykon](#ladeni-ekonomiky-pro-vykon)
- [Logovani cfgeconomycore.xml](#logovani-cfgeconomycorexml)
- [Nastaveni vykonu v serverDZ.cfg](#nastaveni-vykonu-v-serverdzcfg)
- [Dopad modu na vykon](#dopad-modu-na-vykon)
- [Doporuceni pro hardware](#doporuceni-pro-hardware)
- [Monitorovani zdravi serveru](#monitorovani-zdravi-serveru)
- [Caste chyby vykonu](#caste-chyby-vykonu)

---

## Co ovlivnuje vykon serveru

Z komunitnich dat (400+ zminku na Discordu o FPS/vykonu/lagu/desyncu) jsou tri nejvetsi vykonove faktory:

1. **Pocet predmetu** -- vysoke hodnoty `nominal` v `types.xml` znamenaji, ze Centralni ekonomika sleduje a zpracovava vice objektu v kazdem cyklu. Toto je konzistentne pricina cislo jedna server-side lagu.
2. **Spawnovani udalosti** -- prilis mnoho aktivnich dynamickych udalosti (vozidla, zvírata, helikopterove zriceniny) v `events.xml` spotrebovava cykly spawnu/cisteni a sloty entit.
3. **Pocet hracu + pocet modu** -- kazdy pripojeny hrac generuje aktualizace entit a kazdy mod pridava tridy skriptu, ktere engine musi kompilovat a vykonavat kazdy tick.

Herní smycka serveru bezi na fixni obnovovaci frekvenci 30 FPS. Kdyz server nemuze udrzet 30 FPS, hraci zaznamenaji desync -- rubber-banding, zpozdene sebirani predmetu a selhani registrace zasahu. Pod 15 server FPS je hra nehratelna.

---

## Ladeni globals.xml

Toto jsou vanilkove vychozi hodnoty pro parametry, ktere primo ovlivnuji vykon:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### Co kazda hodnota ridi

| Parametr | Vychozi | Vykonový efekt |
|-----------|---------|-------------------|
| `ZombieMaxCount` | 1000 | Strop pro celkovy pocet nakazenych na serveru. Kazdy zombie spousti pathfinding AI. Snizení na 500-700 znatelne zlepsuje FPS serveru na populovanych serverech. |
| `AnimalMaxCount` | 200 | Strop pro zvírata. Zvírata mají jednodussi AI nez zombie, ale stale spotrebovavaji cas ticku. Snizte na 100, pokud vidite problemy s FPS. |
| `ZoneSpawnDist` | 300 | Vzdalenost v metrech, pri ktere se aktivuji zony zombie kolem hracu. Snizení na 200 znamena mene soucasne aktivnich zon. |
| `SpawnInitial` | 1200 | Pocet predmetu, ktere CE spawnuje pri prvnim startu. Vyssi hodnoty znamenaji delsi pocatecni nacitani. Neovlivnuje vykon v ustalenem stavu. |
| `CleanupLifetimeDefault` | 45 | Vychozi cas cisteni v sekundach pro predmety bez specificke zivotnosti. Nizsi hodnoty znamenaji rychlejsi cykly cisteni, ale castejsi zpracovani CE. |

**Doporuceny vykonovy profil** (pro servery mající problemy nad 40 hracu):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Ladeni ekonomiky pro vykon

Centralni ekonomika bezi v nepretrziitem cyklu kontrolujicim kazdy typ predmetu oproti cilovym hodnotam `nominal`/`min`. Vice typu predmetu s vyssimi nominaly znamena vice prace za cyklus.

### Snizte hodnoty nominal

Kazdy predmet v `types.xml` s `nominal > 0` je sledovan CE. Pokud mate 2000 typu predmetu s prumernym nominalem 20, CE spravuje 40 000 objektu. Snizte nominaly celoplochne pro snizeni tohoto cisla:

- Bezne civilni predmety: snizte z 15-40 na 10-25
- Zbrane: udrzujte nizke (vanilka je jiz 2-10)
- Barevne varianty obleceni: zvazujte deaktivaci barevnych variant, ktere nepotrebujete (`nominal=0`)

### Snizte dynamicke udalosti

V `events.xml` kazda aktivni udalost spawnuje a monitoruje skupiny entit. Snizte `nominal` na udalostech vozidel a zvirat, nebo nastavte `<active>0</active>` na udalostech, ktere nepotrebujete.

### Pouzijte rezim necinnosti

Kdyz nejsou pripojeni zadni hraci, CE muze zcela pozastavit:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` znamena, ze server vstoupi do rezimu necinnosti 60 sekund po odpojení posledniho hrace. `IdleModeStartup=1` znamena, ze server startuje v rezimu necinnosti a CE aktivuje az kdyz se pripoji prvni hrac. Tím se zabrani serveru v projizdeni cyklu spawnu, kdyz je prazdny.

### Naladte rychlost respawnu

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Tyto ridi, kolik predmetu a typu predmetu CE zpracovava za cyklus. Nizsi hodnoty snizuji zatez CE na tick, ale zpomaluji respawn lootu. Vanilkove vychozi hodnoty vyse jsou jiz konzervativni.

---

## Logovani cfgeconomycore.xml

Povolte diagnosticke logy CE docasne pro mereni casu cyklu a identifikaci uzkych mist. Ve vasem `cfgeconomycore.xml`:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Pro diagnostiku vykonu nastavte `log_ce_statistics` na `"true"`. To vypisuje casovani cyklu CE do RPT logu serveru. Hledejte radky ukazujici, jak dlouho kazdy cyklus CE trva -- pokud cykly preksracuji 1000 ms, ekonomika je pretizena.

Nastavte `log_ce_lootspawn` a `log_ce_lootcleanup` na `"true"` pro zobrazeni, ktere typy predmetu se nejcasteji spawnuji a cistek. To jsou vasi kandidati pro snizeni nominalu.

**Po diagnostice logovani vypnete.** Samotne zapisy logu spotrebovavaji I/O a mohou zhorsit vykon, pokud zustanou trvale povoleny.

---

## Nastaveni vykonu v serverDZ.cfg

Hlavni konfiguracni soubor serveru ma omezene moznosti souvisejici s vykonem:

| Nastaveni | Efekt |
|---------|--------|
| `maxPlayers` | Snizte toto, pokud server ma problemy. Kazdy hrac generuje sitovy provoz a aktualizace entit. Prechod z 60 na 40 hracu muze ziskat 5-10 server FPS. |
| `instanceId` | Urcuje cestu `storage_1/`. Neni to nastaveni vykonu, ale pokud je vase uloziste na pomalem disku, ovlivnuje to I/O persistence. |

**Co nemuzete zmenit:** obnovovaci frekvence serveru je fixni na 30 FPS. Neexistuje nastaveni pro jeji zvyseni nebo snizeni. Pokud server nemuze udrzet 30 FPS, jednodusse bezi pomaleji.

---

## Dopad modu na vykon

Kazdy mod pridava tridy skriptu, ktere engine kompiluje pri startu a vykonava kazdy tick. Dopad se dramaticky lisi podle kvality modu:

- **Mody pouze s obsahem** (zbrane, obleceni, budovy) pridavaji typy predmetu, ale minimalni rezii skriptu. Jejich naklady jsou ve sledovani CE, ne ve zpracovani ticku.
- **Mody s tezkymi skripty** s cykly `OnUpdate()` nebo `OnTick()` spousteji kod kazdy snimek serveru. Spatne optimalizovane cykly v techto modech jsou nejcastejsi pricinou lagu souvisejicich s mody.
- **Mody obchodu/ekonomiky**, ktere spravuji velke inventare, pridavaji perzistentni objekty, ktere engine musi sledovat.

### Pokyny

- Pridavejte mody inkrementalne. Testujte server FPS po kazdem pridani, ne po pridani 10 najednou.
- Monitorujte server FPS s admin nastroji nebo vystupem RPT logu po pridani novych modu.
- Pokud mod zpusobuje problemy, zkontrolujte jeho zdroj na drahé operace kazdy snimek.

Komunitni shoda: "Predmety (typy) a spawnovani udalosti jsou nejnarocnejsi -- mody, ktere pridavaji tisice zaznamu types.xml skodi vice nez mody, ktere pridavaji slozite skripty."

---

## Doporuceni pro hardware

Herní logika serveru DayZ je **jednovlaknova**. Vicejadroveprocesory pomahaji s reziemi OS a sitovym I/O, ale hlavni herní smycka bezi na jednom jadre.

| Komponenta | Doporuceni | Proc |
|-----------|---------------|-----|
| **CPU** | Nejvyssi jednovlaknovy vykon, jaky muzete ziskat. AMD 5600X nebo lepsi. | Herní smycka je jednovlaknova. Taktovaci frekvence a IPC jsou dulezitejsi nez pocet jader. |
| **RAM** | 8 GB minimum, 12-16 GB pro silne modovane servery | Mody a velke mapy spotrebovavaji pamet. Vycerpani zpusobi zadrhavani. |
| **Uloziste** | SSD vyzadovano | I/O persistence `storage_1/` je neustale. HDD zpusobi zadrhavani behem cyklu ukladani. |
| **Sit** | 100 Mbps+ s nízkou latenci | Sirka pasma je mene dulezita nez stabilita pingu pro prevenci desyncu. |

Komunitni tip: "OVH poskytuje dobrou hodnotu -- kolem $60 USD za dedickovany stroj s 5600X, ktery zvladne 60-slotove modovane servery."

Vyhybejte se sdílenemu/VPS hostingu pro populovane servery. Problem hlucneho souseda na sdílenem hardwaru zpusobuje nepredvidatelne poklesy FPS, ktere neni mozne diagnostikovat z vasi strany.

---

## Monitorovani zdravi serveru

### Server FPS

Kontrolujte RPT log na radky obsahujici server FPS. Zdravy server udrzuje konzistentne 30 FPS. Varovne prahy:

| Server FPS | Stav |
|------------|--------|
| 25-30 | Normalni. Drobne vykyvy jsou ocekavany behem tezkych boju nebo restartu. |
| 15-25 | Snizeny. Hraci zaznamenavaji desync pri interakcich s predmety a v boji. |
| Pod 15 | Kriticky. Rubber-banding, selhavajici akce, registrace zasahu rozbita. |

### Varovani cyklu CE

S povolenym `log_ce_statistics` sledujte casy cyklu CE. Normalni je pod 500 ms. Pokud cykly pravidelne prekracuji 1000 ms, vase ekonomika je prilis tezka.

### Rust uloziste

Monitorujte velikost `storage_1/`. Nekontrolovany rust indikuje naduti persistence -- prilis mnoho umistenych objektu, stanu nebo skrysi se hromadi. Pravidelne wipy serveru nebo snizení `FlagRefreshMaxDuration` v `globals.xml` pomahaji toto kontrolovat.

### Hlaseni hracu

Hlaseni desyncu od hracu jsou vasim nejspolehlivejsim realtimovym indikatorem. Pokud vice hracu hlasi rubber-banding soucasne, FPS serveru kleslo pod 15.

---

## Caste chyby vykonu

### Prilis vysoke hodnoty nominal

Nastaveni kazdeho predmetu na `nominal=50`, protoze "vice lootu je zabavne", vytvari desitky tisic sledovanych objektu. CE stravi cely svuj cyklus spravou predmetu misto behu hry. Zacnete s vanilkovymi nominaly a zvysujte selektivne.

### Prilis mnoho udalosti vozidel

Vozidla jsou drahe entity s fyzikou simulaci, sledovanim prislusenstvi a persistenci. Vanilka spawnuje celkem kolem 50 vozidel. Servery se 150+ vozidly zaznamenavaji vyraznou ztratu FPS.

### Spousteni 30+ modu bez testovani

Kazdy mod je v izolaci v poradku. Slozeny efekt 30+ modu -- tisice extra typu, desitky skriptu kazdy snimek a zvyseny tlak na pamet -- muze snizit server FPS o 50 % nebo vice. Pridavejte mody v davkach po 3-5 a testujte po kazde davce.

### Nikdy nerestartovat server

Nekteré mody mají uniky pameti, ktere se hromadi v case. Naplánujte automaticke restarty kazdych 4-6 hodin. Vetsina hostingovych panelu serveru to podporuje. I dobre napsane mody maji prospech z periodickych restartu, protoze vlastni fragmentace pameti enginu se zvysuje behem dlouhych session.

### Ignorovani naduti uloziste

Slozka `storage_1/`, ktera naroste na nekolik gigabajtu, zpomaluje kazdy cyklus persistence. Pravidelne ji wipujte nebo orezavejte, zejmena pokud povolujete stavbu bazi bez limitu rozpadu.

### Logovani ponechano povolene

Diagnosticke logovani CE, logovani ladeni skriptu a logovani admin nastroju vse zapisuji na disk kazdy tick. Povolte je pro diagnostiku, pak je vypnete. Trvale podrobne logovani na vytizenem serveru muze stat 1-2 FPS samo o sobe.

---

[Domu](../README.md) | [<< Predchozi: Persistence](07-persistence.md) | [Dalsi: Rizeni pristupu >>](09-access-control.md)
