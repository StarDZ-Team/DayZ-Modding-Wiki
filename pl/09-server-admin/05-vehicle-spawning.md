# Chapter 9.5: Spawn pojazdow i zdarzen dynamicznych

[Strona glowna](../README.md) | [<< Poprzedni: Ekonomia lootu](04-loot-economy.md) | [Dalej: Spawn graczy >>](06-player-spawning.md)

---

> **Podsumowanie:** Pojazdy i zdarzenia dynamiczne (rozbicia helikopterow, konwoje, radiowozy) NIE uzywaja `types.xml`. Korzystaja z oddzielnego systemu trzech plikow: `events.xml` definiuje co sie pojawia i w jakiej ilosci, `cfgeventspawns.xml` definiuje gdzie, a `cfgeventgroups.xml` definiuje formacje grupowe. Ten rozdzial omawia wszystkie trzy pliki z prawdziwymi wartosciami vanillowymi.

---

## Spis tresci

- [Jak dziala spawn pojazdow](#jak-dziala-spawn-pojazdow)
- [Wpisy pojazdow w events.xml](#wpisy-pojazdow-w-eventsxml)
- [Dokumentacja pol zdarzen pojazdow](#dokumentacja-pol-zdarzen-pojazdow)
- [cfgeventspawns.xml -- Pozycje spawnu](#cfgeventspawnsxml----pozycje-spawnu)
- [Zdarzenia rozbitych helikopterow](#zdarzenia-rozbitych-helikopterow)
- [Konwoj wojskowy](#konwoj-wojskowy)
- [Radiowoz policyjny](#radiowoz-policyjny)
- [cfgeventgroups.xml -- Spawny grupowe](#cfgeventgroupsxml----spawny-grupowe)
- [Klasa bazowa pojazdow w cfgeconomycore.xml](#klasa-bazowa-pojazdow-w-cfgeconomycorexml)
- [Typowe bledy](#typowe-bledy)

---

## Jak dziala spawn pojazdow

Pojazdy **nie** sa definiowane w `types.xml`. Jesli dodasz klase pojazdu do `types.xml`, nie pojawi sie. Pojazdy uzywaja dedykowanego potoku trzech plikow:

1. **`events.xml`** -- Definiuje kazde zdarzenie pojazdu: ile powinno istniec na mapie (nominal), ktore warianty moga sie pojawic (children) oraz flagi zachowania jak lifetime i safe radius.

2. **`cfgeventspawns.xml`** -- Definiuje fizyczne pozycje swiata, w ktorych zdarzenia pojazdow moga umieszczac obiekty. Kazda nazwa zdarzenia mapuje sie na liste wpisow `<pos>` ze wspolrzednymi x, z i katem.

3. **`cfgeventgroups.xml`** -- Definiuje spawny grupowe, gdzie wiele obiektow pojawia sie razem z wzglednym przesunieciami pozycji (np. wraki pociagow).

CE odczytuje `events.xml`, wybiera zdarzenie wymagajace spawnu, wyszukuje pasujace pozycje w `cfgeventspawns.xml`, losowo wybiera taka, ktora spelnia ograniczenia `saferadius` i `distanceradius`, a nastepnie tworzy losowo wybrany obiekt potomny w tej pozycji.

Wszystkie trzy pliki znajduja sie w `mpmissions/<twoja_misja>/db/`.

---

## Wpisy pojazdow w events.xml

Kazdy vanillowy typ pojazdu ma wlasny wpis zdarzenia. Oto wszystkie z prawdziwymi wartosciami:

### Sedan cywilny

```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

### Wszystkie vanillowe zdarzenia pojazdow

Wszystkie zdarzenia pojazdow uzywaja tej samej struktury co Sedan powyzej. Roznia sie tylko wartosciami:

| Nazwa zdarzenia | Nominal | Min | Max | Lifetime | Potomne (warianty) |
|-----------------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Warianty Hatchback02 |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Warianty Sedan02 |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | Warianty ciezarowki V3S |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- mniej pojazdow |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Lodzie -- najwyzsza liczba, dluzszy lifetime |

`VehicleOffroad02` ma nizszy nominal (3) niz inne pojazdy ladowe (8). `VehicleBoat` ma zarowno najwyzszy nominal (22) jak i dluzszy lifetime (600 vs 300).

---

## Dokumentacja pol zdarzen pojazdow

### Pola na poziomie zdarzenia

| Pole | Typ | Opis |
|------|-----|------|
| `name` | string | Identyfikator zdarzenia. Musi odpowiadac wpisowi w `cfgeventspawns.xml` gdy `position="fixed"`. |
| `nominal` | int | Docelowa liczba aktywnych instancji tego zdarzenia na mapie. |
| `min` | int | CE sprobuje stworzyc wiecej, gdy liczba spadnie ponizej tej wartosci. |
| `max` | int | Twardy gorny limit. CE nigdy nie przekroczy tej liczby. |
| `lifetime` | int | Sekundy miedzy sprawdzeniami odnowienia. Dla pojazdow to NIE jest czas trwalosci pojazdu -- to interwal, w jakim CE ponownie ocenia, czy tworzyc lub czyscic. |
| `restock` | int | Minimalne sekundy miedzy probami odnowienia. 0 = nastepny cykl. |
| `saferadius` | int | Minimalna odleglosc (metry) od jakiegokolwiek gracza, aby zdarzenie moglo sie pojawic. Zapobiega pojawianiu sie pojazdow przed graczami. |
| `distanceradius` | int | Minimalna odleglosc (metry) miedzy dwoma instancjami tego samego zdarzenia. Zapobiega pojawianiu sie dwoch sedanow obok siebie. |
| `cleanupradius` | int | Jesli gracz jest w tej odleglosci (metry), obiekt zdarzenia jest chroniony przed czyszczeniem. |

### Flagi

| Flaga | Wartosci | Opis |
|-------|----------|------|
| `deletable` | 0, 1 | Czy CE moze usunac ten obiekt zdarzenia. Pojazdy uzywaja 0 (nie do usuniecia przez CE). |
| `init_random` | 0, 1 | Losowanie poczatkowych pozycji przy pierwszym spawnie. 0 = uzyj stalych pozycji z `cfgeventspawns.xml`. |
| `remove_damaged` | 0, 1 | Usuniecie obiektu gdy stanie sie zniszczony. **Krytyczne dla pojazdow** -- zobacz [Typowe bledy](#typowe-bledy). |

### Inne pola

| Pole | Wartosci | Opis |
|------|----------|------|
| `position` | `fixed`, `player` | `fixed` = spawn w pozycjach z `cfgeventspawns.xml`. `player` = spawn wzgledem pozycji graczy. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max wymuszane na typ potomny. `mixed` = min/max wspolne dla wszystkich potomnych. `custom` = zachowanie specyficzne dla silnika. |
| `active` | 0, 1 | Wlaczenie lub wylaczenie tego zdarzenia. 0 = zdarzenie jest calkowicie pomijane. |

### Pola potomne

| Atrybut | Opis |
|---------|------|
| `type` | Nazwa klasy obiektu do stworzenia. |
| `min` | Minimalna liczba instancji tego wariantu. |
| `max` | Maksymalna liczba instancji tego wariantu. |
| `lootmin` | Minimalna liczba przedmiotow lootu tworzonych wewnatrz/wokol obiektu. 0 dla pojazdow (czesci pochodza z `cfgspawnabletypes.xml`). |
| `lootmax` | Maksymalna liczba przedmiotow lootu. Uzywane przez rozbicia helikopterow i zdarzenia dynamiczne, nie pojazdy. |

---

## cfgeventspawns.xml -- Pozycje spawnu

Ten plik mapuje nazwy zdarzen na wspolrzedne swiata. Kazdy blok `<event>` zawiera liste prawidlowych pozycji spawnu dla danego typu zdarzenia. Gdy CE musi stworzyc pojazd, losowo wybiera pozycje z tej listy, ktora spelnia ograniczenia `saferadius` i `distanceradius`.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... wiecej pozycji ... -->
</event>
```

Kazdy `<pos>` ma trzy atrybuty:

| Atrybut | Opis |
|---------|------|
| `x` | Wspolrzedna X swiata (pozycja wschod-zachod na mapie). |
| `z` | Wspolrzedna Z swiata (pozycja polnoc-poludnie na mapie). |
| `a` | Kat w stopniach (0-360). Kierunek, w ktorym pojazd jest zwrocony przy spawnie. |

**Kluczowe zasady:**

- Jesli zdarzenie nie ma odpowiadajacego bloku `<event>` w `cfgeventspawns.xml`, **nie pojawi sie** niezaleznie od konfiguracji w `events.xml`.
- Potrzebujesz co najmniej tylu wpisow `<pos>` ile wynosi twoja wartosc `nominal`. Jesli ustawisz `nominal=8`, ale masz tylko 3 pozycje, tylko 3 moga sie pojawic.
- Pozycje powinny byc na drogach lub plaskim terenie. Pozycja wewnatrz budynku lub na stromym terenie spowoduje, ze pojazd pojawi sie zakopany lub przewrocony.
- Wartosc `a` (kat) okresla kierunek pojazdu. Wyrownaj go z kierunkiem drogi dla naturalnie wygladajacych spawnow.

---

## Zdarzenia rozbitych helikopterow

Rozbicia helikopterow to zdarzenia dynamiczne, ktore tworza wrak z wojskowym lootem i zarazonymi w okolicy. Uzywaja tagu `<secondary>` do definiowania ambientowych spawnow zombie wokol miejsca rozbicia.

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>1</min>
    <max>3</max>
    <lifetime>2100</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="15" lootmin="10" max="3" min="1" type="Wreck_UH1Y"/>
    </children>
</event>
```

### Kluczowe roznice od zdarzen pojazdow

- **`<secondary>InfectedArmy</secondary>`** -- tworzy wojskowe zombie wokol miejsca rozbicia. Ten tag odwoluje sie do grupy spawnu zarazonych, ktora CE umieszcza w poblizu.
- **`lootmin="10"` / `lootmax="15"`** -- wrak pojawia sie z 10-15 przedmiotami lootu zdarzenia dynamicznego. Sa to przedmioty z flaga `deloot="1"` w `types.xml` (sprzet wojskowy, rzadka bron).
- **`lifetime=2100`** -- rozbicie przetrwa 35 minut zanim CE je wyczyści i stworzy nowe w innym miejscu.
- **`saferadius=1000`** -- rozbicia nigdy nie pojawiaja sie blizej niz 1 km od gracza.
- **`remove_damaged=0`** -- wrak jest z definicji juz "uszkodzony", wiec musi byc 0, bo inaczej bylby natychmiast czyszczony.

---

## Konwoj wojskowy

Konwoje wojskowe to statyczne grupy zniszczonych pojazdow, ktore pojawiaja sie z wojskowym lootem i zarazonymi straznikami.

```xml
<event name="StaticMilitaryConvoy">
    <nominal>5</nominal>
    <min>3</min>
    <max>5</max>
    <lifetime>1800</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="5" min="3" type="Wreck_V3S"/>
    </children>
</event>
```

Konwoje dzialaja identycznie jak rozbicia helikopterow: tag `<secondary>` tworzy `InfectedArmy` wokol miejsca, a przedmioty lootu z `deloot="1"` pojawiaja sie na wrakach. Przy `nominal=5` do 5 miejsc konwojow istnieje na mapie jednoczesnie. Kazdy trwa 1800 sekund (30 minut) przed przeniesieniem na nowa lokalizacje.

---

## Radiowoz policyjny

Zdarzenia radiowozow policyjnych tworza zniszczone pojazdy policyjne z zarazonymi typu policyjnego w poblizu. Sa **domyslnie wylaczone**.

```xml
<event name="StaticPoliceCar">
    <nominal>10</nominal>
    <min>5</min>
    <max>10</max>
    <lifetime>2500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>200</distanceradius>
    <cleanupradius>100</cleanupradius>
    <secondary>InfectedPoliceHard</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>0</active>
    <children>
        <child lootmax="5" lootmin="3" max="10" min="5" type="Wreck_PoliceCar"/>
    </children>
</event>
```

**`active=0`** oznacza, ze to zdarzenie jest domyslnie wylaczone -- zmien na `1`, aby je wlaczyc. Tag `<secondary>InfectedPoliceHard</secondary>` tworzy trudnych wariantow policyjnych zombie (mocniejszych niz standardowe zarazone). Przy `nominal=10` i `saferadius=500` radiowozy policyjne sa liczniejsze, ale mniej wartosciowe niz rozbicia helikopterow.

---

## cfgeventgroups.xml -- Spawny grupowe

Ten plik definiuje zdarzenia, w ktorych wiele obiektow pojawia sie razem z wzglednym przesunieciami pozycji. Najczestszym zastosowaniem sa porzucone pociagi.

```xml
<event name="Train_Abandoned_Cherno">
    <children>
        <child type="Land_Train_Wagon_Tanker_Blue" x="0" z="0" a="0"/>
        <child type="Land_Train_Wagon_Box_Brown" x="0" z="15" a="0"/>
        <child type="Land_Train_Wagon_Flatbed_Green" x="0" z="30" a="0"/>
        <child type="Land_Train_Engine_Blue" x="0" z="45" a="0"/>
    </children>
</event>
```

Pierwszy potomny jest umieszczany w pozycji z `cfgeventspawns.xml`. Nastepne potomne sa przesuniete o ich wartosci `x`, `z`, `a` wzgledem tego punktu poczatkowego. W tym przykladzie wagony sa rozmieszczone co 15 metrow wzdluz osi z.

Kazdy `<child>` w grupie ma:

| Atrybut | Opis |
|---------|------|
| `type` | Nazwa klasy obiektu do stworzenia. |
| `x` | Przesuniecie X w metrach od poczatku grupy. |
| `z` | Przesuniecie Z w metrach od poczatku grupy. |
| `a` | Przesuniecie kata w stopniach od poczatku grupy. |

Samo zdarzenie grupowe nadal potrzebuje odpowiadajacego wpisu w `events.xml` do kontroli wartosci nominal, lifetime i stanu aktywnosci.

---

## Klasa bazowa pojazdow w cfgeconomycore.xml

Aby CE rozpoznala pojazdy jako sledzony typ obiektow, musza miec deklaracje klasy bazowej w `cfgeconomycore.xml`:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** to klasa bazowa dla wszystkich pojazdow ladowych w DayZ.
- **`BoatScript`** to klasa bazowa dla wszystkich lodzi.
- Atrybut `act="car"` mowi CE, aby traktowala te obiekty ze specyficznym zachowaniem pojazdowym (trwalosc, spawn oparty na zdarzeniach).

Bez tych wpisow klas bazowych CE nie sledzi ani nie zarzadza instancjami pojazdow. Jesli dodajesz modowany pojazd dziedziczacy z innej klasy bazowej, moze byc konieczne dodanie jego klasy bazowej tutaj.

---

## Typowe bledy

Oto najczestsze problemy ze spawnem pojazdow spotykane przez administratorow serwerow.

### Umieszczanie pojazdow w types.xml

**Problem:** Dodajesz `CivilianSedan` do `types.xml` z nominal rownym 10. Zadne sedany sie nie pojawiaja.

**Rozwiazanie:** Usun pojazd z `types.xml`. Dodaj lub edytuj zdarzenie pojazdu w `events.xml` z odpowiednimi potomnymi i upewnij sie, ze odpowiadajace pozycje spawnu istnieja w `cfgeventspawns.xml`. Pojazdy uzywaja systemu zdarzen, nie systemu spawnu przedmiotow.

### Brak odpowiadajacych pozycji spawnu w cfgeventspawns.xml

**Problem:** Tworzysz nowe zdarzenie pojazdu w `events.xml`, ale pojazd nigdy sie nie pojawia.

**Rozwiazanie:** Dodaj odpowiadajacy blok `<event name="TwojaNazwaZdarzenia">` w `cfgeventspawns.xml` z wystarczajaca liczba wpisow `<pos>`. Nazwa zdarzenia `name` w obu plikach musi sie dokladnie zgadzac. Potrzebujesz co najmniej tylu pozycji ile wynosi twoja wartosc `nominal`.

### Ustawienie remove_damaged=0 dla pojezdnych pojazdow

**Problem:** Ustawiasz `remove_damaged="0"` na zdarzeniu pojazdu. Z czasem serwer zapelnia sie zniszczonymi pojazdami, ktore nigdy nie znikaja, blokujac pozycje spawnu i obniajac wydajnosc.

**Rozwiazanie:** Zachowaj `remove_damaged="1"` dla wszystkich pojezdnych pojazdow (sedany, ciezarowki, hatchbacki, lodzie). Zapewnia to, ze gdy pojazd zostanie zniszczony, CE go usunie i stworzy swiezy zamiennik. Ustawiaj `remove_damaged="0"` tylko dla obiektow-wrakow (rozbicia helikopterow, konwoje), ktore sa z zalozenia juz uszkodzone.

### Zapomnienie o ustawieniu active=1

**Problem:** Konfigurujesz zdarzenie pojazdu, ale nigdy sie nie pojawia.

**Rozwiazanie:** Sprawdz tag `<active>`. Jesli jest ustawiony na `0`, zdarzenie jest wylaczone. Niektore vanillowe zdarzenia jak `StaticPoliceCar` sa dostarczane z `active=0`. Ustaw na `1`, aby wlaczyc spawn.

### Zbyt malo pozycji spawnu dla wartosci nominal

**Problem:** Ustawiasz `nominal=15` dla zdarzenia pojazdu, ale w `cfgeventspawns.xml` istnieje tylko 6 pozycji. Pojawia sie tylko 6 pojazdow.

**Rozwiazanie:** Dodaj wiecej wpisow `<pos>`. Jako zasade, umieszczaj co najmniej 2-3x twojej wartosci nominal w pozycjach, aby dac CE wystarczajaco duzo opcji do spelnienia ograniczen `saferadius` i `distanceradius`.

### Pojazd pojawia sie wewnatrz budynkow lub pod ziemia

**Problem:** Pojazd pojawia sie wcisniety w budynek lub zakopany w terenie.

**Rozwiazanie:** Przejrzyj wspolrzedne `<pos>` w `cfgeventspawns.xml`. Przetestuj pozycje w grze uzywajac teleportacji administratora przed dodaniem ich do pliku. Pozycje powinny byc na plaskich drogach lub otwartym terenie, a kat (`a`) powinien byc wyrownany z kierunkiem drogi.

---

[Strona glowna](../README.md) | [<< Poprzedni: Ekonomia lootu](04-loot-economy.md) | [Dalej: Spawn graczy >>](06-player-spawning.md)
