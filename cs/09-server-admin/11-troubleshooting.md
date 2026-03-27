# Chapter 9.11: Reseni problemu serveru

[Domu](../README.md) | [<< Predchozi: Sprava modu](10-mod-management.md) | [Dalsi: Pokrocila temata >>](12-advanced.md)

---

> **Shrnuti:** Diagnostikujte a opravte nejcastejsi problemy serveru DayZ -- selhani pri startu, problemy s pripojenim, pady, spawn lootu a vozidel, persistence a vykon. Kazde reseni zde pochazi z realnych vzoru selhani z tisicu komunitnich hlaseni.

---

## Obsah

- [Server se nespusti](#server-se-nespusti)
- [Hraci se nemohou pripojit](#hraci-se-nemohou-pripojit)
- [Pady a null pointery](#pady-a-null-pointery)
- [Loot se nespawnuje](#loot-se-nespawnuje)
- [Vozidla se nespawnuji](#vozidla-se-nespawnuji)
- [Problemy s persistenci](#problemy-s-persistenci)
- [Vykonove problemy](#vykonove-problemy)
- [Cteni souboru logu](#cteni-souboru-logu)
- [Rychly diagnosticky checklist](#rychly-diagnosticky-checklist)

---

## Server se nespusti

### Chybejici DLL soubory

Pokud `DayZServer_x64.exe` okamzite spadne s chybou chybejiciho DLL, nainstalujte nejnovejsi **Visual C++ Redistributable for Visual Studio 2019** (x64) z oficialnich stranek Microsoftu a restartujte.

### Port jiz pouzivan

Jina instance DayZ nebo aplikace zabira port 2302. Zkontrolujte pomoci `netstat -ano | findstr 2302` (Windows) nebo `ss -tulnp | grep 2302` (Linux). Ukoncete konfliktni proces nebo zmente vas port s `-port=2402`.

### Chybejici slozka mise

Server ocekava `mpmissions/<template>/`, kde nazev slozky presne odpovida hodnote `template` v **serverDZ.cfg**. Pro Chernarus je to `mpmissions/dayzOffline.chernarusplus/` a musi obsahovat alespon **init.c**.

### Neplatny serverDZ.cfg

Jediny chybejici strednik nebo spatny typ uvozovek zabrani startu tiše. Sledujte:

- Chybejici `;` na konci radku hodnot
- Chytre uvozovky misto rovnych uvozovek
- Chybejici `{};` blok kolem class zaznamu

### Chybejici soubory modu

Kazda cesta v `-mod=@CF;@VPPAdminTools;@MyMod` musi existovat relativne ke koreni serveru a obsahovat slozku **addons/** se soubory `.pbo`. Jedina spatna cesta zabrani startu.

---

## Hraci se nemohou pripojit

### Presmerovani portu

DayZ vyzaduje presmerovani a otevreni techto portu ve vasem firewallu:

| Port | Protokol | Ucel |
|------|----------|---------|
| 2302 | UDP | Herní provoz |
| 2303 | UDP | Sit Steamu |
| 2304 | UDP | Dotaz Steamu (interni) |
| 27016 | UDP | Dotaz prohlizece serveru Steamu |

Pokud jste zmenili zakladni port s `-port=`, vsechny ostatni porty se posunuji o stejny ofset.

### Blokovani firewallem

Pridejte **DayZServer_x64.exe** do vyjimek firewallu vaseho OS. Na Windows: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. Na Linuxu otevrte porty s `ufw` nebo `iptables`.

### Nesoulad modu

Klienti musi mit presne stejne verze modu jako server. Pokud hrac vidi "Mod mismatch," jedna ze stran ma zastaralou verzi. Aktualizujte obe strany, kdyz jakýkoliv mod dostane aktualizaci na Workshopu.

### Chybejici soubory .bikey

Soubor `.bikey` kazdeho modu musi byt v adresari `keys/` serveru. Bez nej BattlEye odmitne podepsana PBO klienta. Podivejte se do slozky `keys/` nebo `key/` kazdeho modu.

### Server je plny

Zkontrolujte `maxPlayers` v **serverDZ.cfg** (vychozi 60).

---

## Pady a null pointery

### Pristup k null pointeru

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- nejcastejsi chyba skriptu. Mod vola metodu na smazanem nebo neinicializovanem objektu. Toto je chyba modu, ne spatna konfigurace serveru. Nahlaste ji autorovi modu s uplnym RPT logem.

### Hledani chyb skriptu

Prohledejte RPT log na `SCRIPT (E)`. Nazev tridy a metody v chybe vam rekne, ktery mod je zodpovedny. Umisteni RPT:

- **Server:** adresar `$profiles/` (nebo koren serveru, pokud neni nastaven `-profiles=`)
- **Klient:** `%localappdata%\DayZ\`

### Pad pri restartu

Pokud server padá pri kazdem restartu, **storage_1/** muze byt poskozeno. Zastavte server, zalohujte `storage_1/`, smazte `storage_1/data/events.bin` a restartujte. Pokud to selze, smazte cely adresar `storage_1/` (wipe veskere persistence).

### Pad po aktualizaci modu

Vratte se k predchozi verzi modu. Zkontrolujte changelog Workshopu na prelomove zmeny -- prejmenované tridy, odebrane konfigurace a zmenene formaty RPC jsou caste priciny.

---

## Loot se nespawnuje

### types.xml neni registrovany

Predmety definovane v **types.xml** se nespawnuji, pokud soubor neni registrovan v **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Pokud pouzivate vlastni soubor typu (napr. **types_custom.xml**), pridejte pro nej oddelený zaznam `<file>`.

### Spatne tagy kategorie, pouziti nebo hodnoty

Kazdy tag `<category>`, `<usage>` a `<value>` ve vasem types.xml musi odpovidat nazvu definovanemu v **cfglimitsdefinition.xml**. Preklep jako `usage name="Military"` (velke M) kdyz definice rika `military` (male) tiše zabrani spawnu predmetu.

### Nominal nastaven na nulu

Pokud je `nominal` `0`, CE tento predmet nikdy nespawnuje. To je umyslne pro predmety, ktere by meli existovat pouze pres crafting, udalosti nebo adminske umisteni. Pokud chcete, aby se predmet spawnoval prirozene, nastavte `nominal` na alespon `1`.

### Chybejici pozice mapovych skupin

Predmety potrebuji platne pozice spawnu uvnitr budov. Pokud vlastni predmet nema odpovidajici pozice mapovych skupin (definovane v **mapgroupproto.xml**), CE nema kam jej umistit. Priradte predmet ke kategoriim a pouzitim, ktere jiz maji platne pozice na mape.

---

## Vozidla se nespawnuji

Vozidla pouzivaji system udalosti, **ne** types.xml.

### Konfigurace events.xml

Spawny vozidel jsou definovany v **events.xml**:

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

### Chybejici pozice spawnu

Udalosti vozidel s `<position>fixed</position>` vyzaduji zaznamy v **cfgeventspawns.xml**. Bez definovanych souradnic nema udalost kam vozidlo umistit.

### Udalost zakazana

Pokud je `<active>0</active>`, udalost je zcela zakazana. Nastavte na `1`.

### Poskozena vozidla blokuji sloty

Pokud je `remove_damaged="0"`, znicena vozidla zustanou ve svete navzdy a zabírajíslozy spawnu. Nastavte `remove_damaged="1"`, aby CE cistilo vraky a spawnilo nahrady.

---

## Problemy s persistenci

### Baze mizi

Uzemní vlajky musi byt obnoveny pred vyprsenim jejich casovace. Vychozi `FlagRefreshFrequency` je `432000` sekund (5 dní). Pokud zadny hrac neinteraguje s vlajkou behem tohoto okna, vlajka a vsechny objekty v jejim polomeru jsou smazany.

Zkontrolujte hodnotu v **globals.xml**:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Zvyste tuto hodnotu na malo populovanych serverech, kde se hraci prihlasují mene casto.

### Predmety mizi po restartu

Kazdy predmet ma `lifetime` v **types.xml** (sekundy). Kdyz vyprsi bez interakce hrace, CE ho odstrani. Reference: `3888000` = 45 dní, `604800` = 7 dní, `14400` = 4 hodiny. Predmety uvnitr kontejneru dedi zivotnost kontejneru.

### storage_1/ roste prilis

Pokud vas adresar `storage_1/` naroste pres nekolik set MB, vase ekonomika produkuje prilis mnoho predmetu. Snizte hodnoty `nominal` napric vasim types.xml, zejmena u predmetu s vysokym poctem jako jidlo, obleceni a munice. Nafouknury soubor persistence zpusobi delsi casy restartu.

### Data hracu ztracena

Inventare a pozice hracu jsou ulozeny v `storage_1/players/`. Pokud je tento adresar smazan nebo poskozen, vsichni hraci se spawnuji jako novi. Pravidelne zalohujte `storage_1/`.

---

## Vykonove problemy

### Pokles FPS serveru

Servery DayZ ciluji na 30+ FPS pro plynulý gameplay. Bezne priciny nizkeho server FPS:

- **Prilis mnoho zombie** -- snizte `ZombieMaxCount` v **globals.xml** (vychozi 800, zkuste 400-600)
- **Prilis mnoho zvirat** -- snizte `AnimalMaxCount` (vychozi 200, zkuste 100)
- **Nadmerny loot** -- snizte hodnoty `nominal` napric vasim types.xml
- **Prilis mnoho objektu bazi** -- velke baze se stovkami predmetu zatezuji persistenci
- **Tezke skriptove mody** -- nekteré mody spousteji drahou logiku kazdy snimek

### Desync

Hraci zazivajici rubber-banding, zpozdene akce nebo neviditelne zombie jsou priznaky desyncu. Toto temer vzdy znamena, ze server FPS kleslo pod 15. Opravte zakladni vykonovy problem misto hledani nastaveni specifickeho pro desync.

### Dlouhe casy restartu

Cas restartu je primo umerny velikosti `storage_1/`. Pokud restarty trvaji dele nez 2-3 minuty, mate prilis mnoho perzistentnich objektu. Snizte hodnoty nominal lootu a nastavte prislusne zivotnosti.

---

## Cteni souboru logu

### Umisteni RPT serveru

RPT soubor je v `$profiles/` (pokud je spusten s `-profiles=`) nebo v koreni serveru. Vzor nazvu souboru: `DayZServer_x64_<datum>_<cas>.RPT`.

### Co hledat

| Hledany vyraz | Vyznam |
|-------------|---------|
| `SCRIPT (E)` | Chyba skriptu -- mod ma bug |
| `[ERROR]` | Chyba na urovni enginu |
| `ErrorMessage` | Fatalni chyba, ktera muze zpusobit vypnuti |
| `Cannot open` | Chybejici soubor (PBO, konfigurace, mise) |
| `Crash` | Pad na urovni aplikace |

### Logy BattlEye

Logy BattlEye jsou v adresari `BattlEye/` uvnitr korene vaseho serveru. Tyto zobrazuji udalosti vykopnuti a banu. Pokud hraci hlasi neocekovane vykopnuti, zkontrolujte nejprve zde.

---

## Rychly diagnosticky checklist

Kdyz se neco pokazi, projdete si tento seznam v poradi:

```
1. Zkontrolujte RPT serveru na radky SCRIPT (E) a [ERROR]
2. Overte, ze kazda cesta -mod= existuje a obsahuje addons/*.pbo
3. Overte, ze vsechny soubory .bikey jsou zkopirovany do keys/
4. Zkontrolujte serverDZ.cfg na syntakticke chyby (chybejici stredniky)
5. Zkontrolujte presmerovani portu: 2302 UDP + 27016 UDP
6. Overte, ze slozka mise odpovida hodnote template v serverDZ.cfg
7. Zkontrolujte storage_1/ na poskozeni (smazte events.bin pokud je potreba)
8. Testujte nejprve bez modu, pak pridavejte mody jeden po druhem
```

Krok 8 je nejucinnejsi technika. Pokud server funguje vanilkove, ale rozbije se s mody, muzete izolovat problemovy mod pomoci binárniho vyhledávani -- pridejte polovinu modu, testujte, pak zuzte.

---

[Domu](../README.md) | [<< Predchozi: Sprava modu](10-mod-management.md) | [Dalsi: Pokrocila temata >>](12-advanced.md)
