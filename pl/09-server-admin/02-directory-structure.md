# Chapter 9.2: Struktura katalogow i folder misji

[Strona glowna](../README.md) | [<< Poprzedni: Konfiguracja serwera](01-server-setup.md) | **Struktura katalogow** | [Dalej: Kompletna dokumentacja serverDZ.cfg >>](03-server-cfg.md)

---

> **Podsumowanie:** Kompletny przewodnik po kazdym pliku i folderze w katalogu serwera DayZ oraz folderze misji. Znajomosc przeznaczenia kazdego pliku -- i tego, ktore mozna bezpiecznie edytowac -- jest niezbedna zanim zaczniesz modyfikowac ekonomie lootu lub dodawac mody.

---

## Spis tresci

- [Glowny katalog serwera](#glowny-katalog-serwera)
- [Folder addons/](#folder-addons)
- [Folder keys/](#folder-keys)
- [Folder profiles/](#folder-profiles)
- [Folder mpmissions/](#folder-mpmissions)
- [Struktura folderu misji](#struktura-folderu-misji)
- [Folder db/ -- Rdzen ekonomii](#folder-db----rdzen-ekonomii)
- [Folder env/ -- Terytoria zwierzat](#folder-env----terytoria-zwierzat)
- [Folder storage_1/ -- Trwalosc danych](#folder-storage_1----trwalosc-danych)
- [Pliki glowne misji](#pliki-glowne-misji)
- [Ktore pliki edytowac, a ktore zostawic](#ktore-pliki-edytowac-a-ktore-zostawic)

---

## Glowny katalog serwera

```
DayZServer/
  DayZServer_x64.exe          # Plik wykonywalny serwera
  serverDZ.cfg                 # Glowna konfiguracja serwera (nazwa, haslo, mody, czas)
  dayzsetting.xml              # Ustawienia renderowania (nieistotne dla serwerow dedykowanych)
  ban.txt                      # Zbanowane Steam64 ID, jedno na linie
  whitelist.txt                # Dozwolone Steam64 ID, jedno na linie
  steam_appid.txt              # Zawiera "221100" -- nie edytuj
  dayz.gproj                   # Plik projektu Workbench -- nie edytuj
  addons/                      # Pliki PBO vanilli
  battleye/                    # Pliki anty-cheata
  config/                      # Konfiguracja Steam (config.vdf)
  dta/                         # Pliki PBO silnika (skrypty, GUI, grafika)
  keys/                        # Klucze weryfikacji sygnatur (pliki .bikey)
  logs/                        # Logi na poziomie silnika
  mpmissions/                  # Wszystkie foldery misji
  profiles/                    # Dane wyjsciowe (logi skryptow, baza graczy, zrzuty awarii)
  server_manager/              # Narzedzia do zarzadzania serwerem
```

---

## Folder addons/

Zawiera cala zawartosc vanillowej gry spakowana jako pliki PBO. Kazdy PBO ma odpowiadajacy plik sygnatury `.bisign`:

```
addons/
  ai.pbo                       # Skrypty zachowan AI
  ai.pbo.dayz.bisign           # Sygnatura dla ai.pbo
  animals.pbo                  # Definicje zwierzat
  characters_backpacks.pbo     # Modele/konfiguracje plecakow
  characters_belts.pbo         # Modele przedmiotow paska
  weapons_firearms.pbo         # Modele/konfiguracje broni
  ... (100+ plikow PBO)
```

**Nigdy nie edytuj tych plikow.** Sa nadpisywane przy kazdej aktualizacji serwera przez SteamCMD. Mody nadpisuja zachowanie vanilli za pomoca systemu klas `modded`, a nie przez zmiane PBO.

---

## Folder keys/

Zawiera pliki kluczy publicznych `.bikey` uzywane do weryfikacji sygnatur modow:

```
keys/
  dayz.bikey                   # Klucz sygnatury vanilli (zawsze obecny)
```

Gdy dodajesz mod, skopiuj jego plik `.bikey` do tego folderu. Serwer uzywa `verifySignatures = 2` w `serverDZ.cfg`, aby odrzucic kazdy PBO, ktory nie ma odpowiadajacego `.bikey` w tym folderze.

Jesli gracz zaladuje mod, ktorego klucz nie znajduje sie w twoim folderze `keys/`, zostanie wyrzucony z bledem **"Signature check failed"**.

---

## Folder profiles/

Tworzony przy pierwszym uruchomieniu serwera. Zawiera dane wyjsciowe:

```
profiles/
  BattlEye/                              # Logi i bany BE
  DataCache/                             # Dane w pamieci podrecznej
  Users/                                 # Pliki preferencji poszczegolnych graczy
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Log administratora
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Raport silnika (informacje o awariach, ostrzezenia)
  script_2026-03-08_11-34-35.log           # Log skryptow (twoje glowne narzedzie do debugowania)
```

**Log skryptow** to najwazniejszy plik tutaj. Kazde wywolanie `Print()`, kazdy blad skryptu i kazdy komunikat ladowania moda trafia tutaj. Gdy cos sie zepsuje, to jest pierwsze miejsce, w ktorym szukasz.

Pliki logow narastaja z czasem. Stare logi nie sa automatycznie usuwane.

---

## Folder mpmissions/

Zawiera jeden podkatalog na mape:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (darmowa)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

Format nazwy folderu to `<nazwamiisji>.<nazwaterenu>`. Wartosc `template` w `serverDZ.cfg` musi dokladnie odpowiadac jednej z tych nazw folderow.

---

## Struktura folderu misji

Folder misji Chernarus (`mpmissions/dayzOffline.chernarusplus/`) zawiera:

```
dayzOffline.chernarusplus/
  init.c                         # Skrypt punktu wejscia misji
  db/                            # Glowne pliki ekonomii
  env/                           # Definicje terytoriow zwierzat
  storage_1/                     # Dane trwalosci (gracze, stan swiata)
  cfgeconomycore.xml             # Klasy bazowe ekonomii i ustawienia logowania
  cfgenvironment.xml             # Odniesienia do plikow terytoriow zwierzat
  cfgeventgroups.xml             # Definicje grup zdarzen
  cfgeventspawns.xml             # Dokladne pozycje spawnu dla zdarzen (pojazdy itp.)
  cfgeffectarea.json             # Definicje stref skazen
  cfggameplay.json               # Dostrajanie rozgrywki (wytrzymalosc, obrazenia, budowanie)
  cfgignorelist.xml              # Przedmioty calkowicie wykluczone z ekonomii
  cfglimitsdefinition.xml        # Definicje prawidlowych tagow kategorii/uzycia/wartosci
  cfglimitsdefinitionuser.xml    # Niestandardowe definicje tagow uzytkownika
  cfgplayerspawnpoints.xml       # Lokalizacje spawnu swiezych graczy
  cfgrandompresets.xml           # Definicje pul lootu do ponownego uzycia
  cfgspawnabletypes.xml          # Wstepnie zamocowane przedmioty i ladunek na pojawiajacych sie obiektach
  cfgundergroundtriggers.json    # Wyzwalacze obszarow podziemnych
  cfgweather.xml                 # Konfiguracja pogody
  areaflags.map                  # Dane flag obszaru (binarnie)
  mapclusterproto.xml            # Definicje prototypow klastrow mapy
  mapgroupcluster.xml            # Definicje klastrow grup budynkow
  mapgroupcluster01.xml          # Dane klastra (czesc 1)
  mapgroupcluster02.xml          # Dane klastra (czesc 2)
  mapgroupcluster03.xml          # Dane klastra (czesc 3)
  mapgroupcluster04.xml          # Dane klastra (czesc 4)
  mapgroupdirt.xml               # Pozycje lootu na ziemi/brudzie
  mapgrouppos.xml                # Pozycje grup na mapie
  mapgroupproto.xml              # Definicje prototypow grup mapy
```

---

## Folder db/ -- Rdzen ekonomii

To serce Centralnej Ekonomii. Piec plikow kontroluje co sie pojawia, gdzie i w jakiej ilosci:

```
db/
  types.xml        # KLUCZOWY plik: definiuje reguly spawnu kazdego przedmiotu
  globals.xml      # Globalne parametry ekonomii (zegary, limity, ilosci)
  events.xml       # Zdarzenia dynamiczne (zwierzeta, pojazdy, helikoptery)
  economy.xml      # Przelaczniki podsystemow ekonomii (loot, zwierzeta, pojazdy)
  messages.xml     # Zaplanowane wiadomosci serwera dla graczy
```

### types.xml

Definiuje reguly spawnu dla **kazdego przedmiotu** w grze. Przy okolo 23 000 liniach jest to zdecydowanie najwiekszy plik ekonomii. Kazdy wpis okresla, ile kopii przedmiotu powinno istniec na mapie, gdzie moze sie pojawic i jak dlugo przetrwa. Zobacz [Rozdzial 9.4](04-loot-economy.md) po szczegolowe omowienie.

### globals.xml

Globalne parametry wplywajace na cala ekonomie: liczba zombie, liczba zwierzat, zegary czyszczenia, zakresy uszkodzen lootu, czas odnowienia. Lacznie 33 parametry. Zobacz [Rozdzial 9.4](04-loot-economy.md) po kompletna dokumentacje.

### events.xml

Definiuje dynamiczne zdarzenia spawnu dla zwierzat i pojazdow. Kazde zdarzenie okresla nominalna ilosc, ograniczenia spawnu i warianty potomne. Na przyklad zdarzenie `VehicleCivilianSedan` tworzy 8 sedanow na mapie w 3 wariantach kolorystycznych.

### economy.xml

Glowne przelaczniki podsystemow ekonomii:

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

| Flaga | Znaczenie |
|-------|-----------|
| `init` | Tworzenie przedmiotow przy pierwszym starcie serwera |
| `load` | Ladowanie zapisanego stanu z trwalosci |
| `respawn` | Zezwolenie na ponowne pojawianie sie przedmiotow po czyszczeniu |
| `save` | Zapisywanie stanu do plikow trwalosci |

### messages.xml

Zaplanowane wiadomosci nadawane do wszystkich graczy. Obsluguje zegary odliczania, interwaly powtorzen, wiadomosci przy polaczeniu i ostrzezenia o wylaczeniu:

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

Uzyj `#name` dla nazwy serwera i `#tmin` dla czasu pozostalego w minutach.

---

## Folder env/ -- Terytoria zwierzat

Zawiera pliki XML definiujace, gdzie kazdy gatunek zwierzat moze sie pojawic:

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

Te pliki zawieraja setki punktow wspolrzednych definiujacych strefy terytoriow na calej mapie. Sa odwolywane przez `cfgenvironment.xml`. Rzadko musisz je edytowac, chyba ze chcesz zmienic geograficznie miejsce spawnu zwierzat lub zombie.

---

## Folder storage_1/ -- Trwalosc danych

Przechowuje trwaly stan serwera miedzy restartami:

```
storage_1/
  players.db         # Baza danych SQLite wszystkich postaci graczy
  spawnpoints.bin    # Binarne dane punktow spawnu
  backup/            # Automatyczne kopie zapasowe danych trwalosci
  data/              # Stan swiata (umieszczone przedmioty, budowanie baz, pojazdy)
```

**Nigdy nie edytuj `players.db` gdy serwer jest uruchomiony.** To baza danych SQLite zablokowana przez proces serwera. Jesli musisz wyczyscic postacie, najpierw zatrzymaj serwer, a nastepnie usun lub zmien nazwe pliku.

Aby wykonac **pelne czyszczenie trwalosci**, zatrzymaj serwer i usun caly folder `storage_1/`. Serwer odtworzy go przy nastepnym uruchomieniu ze swiezym swiatem.

Aby wykonac **czesciowe czyszczenie** (zachowaj postacie, zresetuj loot):
1. Zatrzymaj serwer
2. Usun pliki w `storage_1/data/`, ale zachowaj `players.db`
3. Uruchom ponownie

---

## Pliki glowne misji

### cfgeconomycore.xml

Rejestruje klasy bazowe ekonomii i konfiguruje logowanie CE:

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

Ustaw `log_ce_lootspawn` na `"true"` podczas debugowania problemow ze spawnem przedmiotow. Generuje to szczegolowe dane w logu RPT, pokazujace ktore przedmioty CE probuje stworzyc i dlaczego sie to udaje lub nie.

### cfglimitsdefinition.xml

Definiuje prawidlowe wartosci dla elementow `<category>`, `<usage>`, `<value>` i `<tag>` uzywanych w `types.xml`:

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

Jesli uzywasz tagu `<usage>` lub `<value>` w `types.xml`, ktory nie jest tutaj zdefiniowany, przedmiot po cichu nie pojawi sie na mapie.

### cfgignorelist.xml

Przedmioty wymienione tutaj sa calkowicie wykluczone z ekonomii, nawet jesli maja wpisy w `types.xml`:

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

Sluzy to do przedmiotow, ktore istnieja w kodzie gry, ale nie sa przeznaczone do naturalnego spawnu (niedokonczone przedmioty, przestarzala zawartosc, sezonowe przedmioty poza sezonem).

### cfggameplay.json

Plik JSON nadpisujacy parametry rozgrywki. Kontroluje wytrzymalosc, ruch, obrazenia bazy, pogode, temperature, obstrukcje broni, toniecle i wiecej. Ten plik jest opcjonalny -- jesli go nie ma, serwer uzywa domyslnych wartosci.

### cfgplayerspawnpoints.xml

Definiuje, gdzie swiezo pojawieni gracze pojawiaja sie na mapie, z ograniczeniami odleglosci od zarazonych, innych graczy i budynkow.

### cfgeventspawns.xml

Zawiera dokladne wspolrzedne swiata, w ktorych moga sie pojawiac zdarzenia (pojazdy, helikoptery itp.). Kazda nazwa zdarzenia z `events.xml` ma liste prawidlowych pozycji:

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

Atrybut `a` to kat obrotu w stopniach.

---

## Ktore pliki edytowac, a ktore zostawic

| Plik / Folder | Mozna edytowac? | Uwagi |
|---------------|:---:|-------|
| `serverDZ.cfg` | Tak | Glowna konfiguracja serwera |
| `db/types.xml` | Tak | Reguly spawnu przedmiotow -- najczesciej edytowany plik |
| `db/globals.xml` | Tak | Parametry dostrajania ekonomii |
| `db/events.xml` | Tak | Zdarzenia spawnu pojazdow/zwierzat |
| `db/economy.xml` | Tak | Przelaczniki podsystemow ekonomii |
| `db/messages.xml` | Tak | Wiadomosci serwera |
| `cfggameplay.json` | Tak | Dostrajanie rozgrywki |
| `cfgspawnabletypes.xml` | Tak | Presety zalacznikow/ladunku |
| `cfgrandompresets.xml` | Tak | Definicje pul lootu |
| `cfglimitsdefinition.xml` | Tak | Dodawanie niestandardowych tagow uzycia/wartosci |
| `cfgplayerspawnpoints.xml` | Tak | Lokalizacje spawnu graczy |
| `cfgeventspawns.xml` | Tak | Wspolrzedne spawnu zdarzen |
| `cfgignorelist.xml` | Tak | Wykluczanie przedmiotow z ekonomii |
| `cfgweather.xml` | Tak | Wzorce pogody |
| `cfgeffectarea.json` | Tak | Strefy skazen |
| `init.c` | Tak | Skrypt wejscia misji |
| `addons/` | **Nie** | Nadpisywane przy aktualizacji |
| `dta/` | **Nie** | Dane silnika |
| `keys/` | Tylko dodawanie | Kopiuj pliki `.bikey` modow tutaj |
| `storage_1/` | Tylko usuwanie | Trwalosc -- nie edytuj recznie |
| `battleye/` | **Nie** | Anty-cheat -- nie ruszaj |
| `mapgroup*.xml` | Ostroznie | Pozycje lootu w budynkach -- tylko zaawansowana edycja |

---

**Poprzedni:** [Konfiguracja serwera](01-server-setup.md) | [Strona glowna](../README.md) | **Dalej:** [Kompletna dokumentacja serverDZ.cfg >>](03-server-cfg.md)
