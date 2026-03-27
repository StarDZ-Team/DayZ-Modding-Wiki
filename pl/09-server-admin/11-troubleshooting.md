# Chapter 9.11: Rozwiazywanie problemow z serwerem

[Strona glowna](../README.md) | [<< Poprzedni: Zarzadzanie modami](10-mod-management.md) | [Dalej: Tematy zaawansowane >>](12-advanced.md)

---

> **Podsumowanie:** Diagnozowanie i naprawianie najczestszych problemow serwera DayZ -- awarie startu, problemy z laczeniem, crasha, spawn lootu i pojazdow, trwalosc i wydajnosc. Kazde rozwiazanie tutaj pochodzi z prawdziwych wzorow awarii z tysiecy raportow spolecznosci.

---

## Spis tresci

- [Serwer nie uruchamia sie](#serwer-nie-uruchamia-sie)
- [Gracze nie moga sie polaczyc](#gracze-nie-moga-sie-polaczyc)
- [Awarie i wskazniki null](#awarie-i-wskazniki-null)
- [Loot sie nie pojawia](#loot-sie-nie-pojawia)
- [Pojazdy sie nie pojawiaja](#pojazdy-sie-nie-pojawiaja)
- [Problemy z trwaloscia](#problemy-z-trwaloscia)
- [Problemy z wydajnoscia](#problemy-z-wydajnoscia)
- [Czytanie plikow logow](#czytanie-plikow-logow)
- [Szybka lista kontrolna diagnostyki](#szybka-lista-kontrolna-diagnostyki)

---

## Serwer nie uruchamia sie

### Brakujace pliki DLL

Jesli `DayZServer_x64.exe` natychmiast ulega awarii z bledem brakujacego DLL, zainstaluj najnowszy **Visual C++ Redistributable for Visual Studio 2019** (x64) z oficjalnej strony Microsoft i zrestartuj.

### Port juz w uzyciu

Inna instancja DayZ lub aplikacja zajmuje port 2302. Sprawdz za pomoca `netstat -ano | findstr 2302` (Windows) lub `ss -tulnp | grep 2302` (Linux). Zakoncz proces powodujacy konflikt lub zmien port za pomoca `-port=2402`.

### Brakujacy folder misji

Serwer oczekuje `mpmissions/<template>/`, gdzie nazwa folderu dokladnie odpowiada wartosci `template` w **serverDZ.cfg**. Dla Chernarusa to `mpmissions/dayzOffline.chernarusplus/` i musi zawierac co najmniej **init.c**.

### Nieprawidlowy serverDZ.cfg

Pojedynczy brakujacy srednik lub zly typ cudzyslowu po cichu uniemozliwia start. Uwazaj na:

- Brakujace `;` na koncu linii wartosci
- Inteligentne cudzyslowy zamiast prostych
- Brakujace `{};` wokol wpisow klas

### Brakujace pliki modow

Kazda sciezka w `-mod=@CF;@VPPAdminTools;@MyMod` musi istniec wzgledem glownego katalogu serwera i zawierac folder **addons/** z plikami `.pbo`. Jedna zla sciezka uniemozliwia start.

---

## Gracze nie moga sie polaczyc

### Przekierowanie portow

DayZ wymaga przekierowania i otwarcia w firewallu nastepujacych portow:

| Port | Protokol | Przeznaczenie |
|------|----------|---------------|
| 2302 | UDP | Ruch gry |
| 2303 | UDP | Siec Steam |
| 2304 | UDP | Zapytanie Steam (wewnetrzne) |
| 27016 | UDP | Zapytanie przegladarki serwerow Steam |

Jesli zmieniles port bazowy za pomoca `-port=`, wszystkie inne porty przesuwa sie o taki sam offset.

### Blokowanie firewalla

Dodaj **DayZServer_x64.exe** do wyjatkow firewalla systemu. W systemie Windows: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. W systemie Linux otworz porty za pomoca `ufw` lub `iptables`.

### Niezgodnosc modow

Klienci musza miec dokladnie te same wersje modow co serwer. Jesli gracz widzi "Mod mismatch", jedna ze stron ma przestarzala wersje. Aktualizuj oba, gdy jakikolwiek mod otrzyma aktualizacje Workshop.

### Brakujace pliki .bikey

Plik `.bikey` kazdego moda musi znajdowac sie w katalogu `keys/` serwera. Bez niego BattlEye odrzuca podpisane PBO klienta. Zajrzyj do folderu `keys/` lub `key/` kazdego moda.

### Serwer pelny

Sprawdz `maxPlayers` w **serverDZ.cfg** (domyslnie 60).

---

## Awarie i wskazniki null

### Dostep do wskaznika null

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- najczestszy blad skryptu. Mod wywoluje metode na usunietym lub niezainicjalizowanym obiekcie. To jest blad moda, nie bledna konfiguracja serwera. Zglos go autorowi moda z pelnym logiem RPT.

### Znajdowanie bledow skryptow

Przeszukaj log RPT pod katem `SCRIPT (E)`. Nazwa klasy i metody w bledzie mowi ci, ktory mod jest odpowiedzialny. Lokalizacje RPT:

- **Serwer:** katalog `$profiles/` (lub glowny katalog serwera jesli nie ustawiono `-profiles=`)
- **Klient:** `%localappdata%\DayZ\`

### Awaria przy restarcie

Jesli serwer ulega awarii przy kazdym restarcie, **storage_1/** moze byc uszkodzony. Zatrzymaj serwer, zrob kopie zapasowa `storage_1/`, usun `storage_1/data/events.bin` i zrestartuj. Jesli to nie pomoze, usun caly katalog `storage_1/` (czysci cala trwalosc).

### Awaria po aktualizacji moda

Wroc do poprzedniej wersji moda. Sprawdz changelog Workshop pod katem zmian powodujacych awarie -- zmienione nazwy klas, usuniete konfiguracje i zmienione formaty RPC to typowe przyczyny.

---

## Loot sie nie pojawia

### types.xml nie zarejestrowany

Przedmioty zdefiniowane w **types.xml** nie pojawia sie, dopoki plik nie jest zarejestrowany w **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Jesli uzywasz niestandardowego pliku typow (np. **types_custom.xml**), dodaj oddzielny wpis `<file>` dla niego.

### Bledne tagi category, usage lub value

Kazdy tag `<category>`, `<usage>` i `<value>` w types.xml musi odpowiadac nazwie zdefiniowanej w **cfglimitsdefinition.xml**. Literowka jak `usage name="Military"` (wielkie M) gdy definicja mowi `military` (male m) po cichu uniemozliwia spawn przedmiotu.

### Nominal ustawiony na zero

Jesli `nominal` wynosi `0`, CE nigdy nie stworzy tego przedmiotu. To jest zamierzone dla przedmiotow, ktore powinny istniec tylko przez crafting, zdarzenia lub umieszczenie przez administratora. Jesli chcesz, aby przedmiot pojawial sie naturalnie, ustaw `nominal` na co najmniej `1`.

### Brakujace pozycje grup mapy

Przedmioty potrzebuja prawidlowych pozycji spawnu wewnatrz budynkow. Jesli niestandardowy przedmiot nie ma pasujacych pozycji grup mapy (zdefiniowanych w **mapgroupproto.xml**), CE nie ma gdzie go umiescic. Przypisz przedmiot do kategorii i uzyc, ktore juz maja prawidlowe pozycje na mapie.

---

## Pojazdy sie nie pojawiaja

Pojazdy uzywaja systemu zdarzen, **nie** types.xml.

### Konfiguracja events.xml

Spawny pojazdow sa zdefiniowane w **events.xml**:

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

### Brakujace pozycje spawnu

Zdarzenia pojazdow z `<position>fixed</position>` wymagaja wpisow w **cfgeventspawns.xml**. Bez zdefiniowanych wspolrzednych zdarzenie nie ma gdzie umiescic pojazdu.

### Zdarzenie wylaczone

Jesli `<active>0</active>`, zdarzenie jest calkowicie wylaczone. Ustaw na `1`.

### Uszkodzone pojazdy blokuja sloty

Jesli `remove_damaged="0"`, zniszczone pojazdy pozostaja na swiecie na zawsze i zajmuja sloty spawnu. Ustaw `remove_damaged="1"`, aby CE czyscila wraki i tworzyla zamienniki.

---

## Problemy z trwaloscia

### Bazy znikaja

Maszty flagowe musza byc odswiezane zanim ich zegar wygasnie. Domyslna wartosc `FlagRefreshFrequency` to `432000` sekund (5 dni). Jesli zaden gracz nie wejdzie w interakcje z flaga w tym oknie, flaga i wszystkie obiekty w jej promieniu sa usuwane.

Sprawdz wartosc w **globals.xml**:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Zwieksz te wartosc na serwerach z mala populacja, gdzie gracze loguja sie rzadziej.

### Przedmioty znikaja po restarcie

Kazdy przedmiot ma `lifetime` w **types.xml** (sekundy). Gdy wygasnie bez interakcji gracza, CE go usuwa. Referencja: `3888000` = 45 dni, `604800` = 7 dni, `14400` = 4 godziny. Przedmioty wewnatrz pojemnikow dziedzicza lifetime pojemnika.

### storage_1/ rosnie za bardzo

Jesli twoj katalog `storage_1/` przekracza kilkaset MB, twoja ekonomia produkuje zbyt wiele przedmiotow. Redukuj wartosci `nominal` w types.xml, szczegolnie dla przedmiotow o wysokiej liczbie jak jedzenie, ubrania i amunicja. Rozdety plik trwalosci powoduje dluzsze czasy restartu.

### Dane graczy utracone

Ekwipunki i pozycje graczy sa przechowywane w `storage_1/players/`. Jesli ten katalog zostanie usuniety lub uszkodzony, wszyscy gracze pojawiaja sie od nowa. Regularnie rob kopie zapasowe `storage_1/`.

---

## Problemy z wydajnoscia

### Spadek FPS serwera

Serwery DayZ celuja w 30+ FPS dla plynnej rozgrywki. Typowe przyczyny niskiego FPS serwera:

- **Zbyt wiele zombie** -- redukuj `ZombieMaxCount` w **globals.xml** (domyslnie 800, probuj 400-600)
- **Zbyt wiele zwierzat** -- redukuj `AnimalMaxCount` (domyslnie 200, probuj 100)
- **Nadmiar lootu** -- obniz wartosci `nominal` w types.xml
- **Zbyt wiele obiektow baz** -- duze bazy z setkami przedmiotow obciazaja trwalosc
- **Ciezkie mody skryptowe** -- niektore mody uruchamiaja kosztowna logike per-klatka

### Desync

Gracze doswiadczajacy gumowania, opoznionych akcji lub niewidzialnych zombie to objawy desyncu. To prawie zawsze oznacza, ze FPS serwera spadl ponizej 15. Napraw podstawowy problem z wydajnoscia zamiast szukac ustawienia specyficznego dla desyncu.

### Dlugie czasy restartu

Czas restartu jest wprost proporcjonalny do rozmiaru `storage_1/`. Jesli restarty trwaja dluzej niz 2-3 minuty, masz zbyt wiele trwalych obiektow. Redukuj wartosci nominal lootu i ustawiaj odpowiednie lifetimes.

---

## Czytanie plikow logow

### Lokalizacja RPT serwera

Plik RPT znajduje sie w `$profiles/` (jesli uruchomiono z `-profiles=`) lub w glownym katalogu serwera. Wzorzec nazwy pliku: `DayZServer_x64_<data>_<czas>.RPT`.

### Czego szukac

| Szukany tekst | Znaczenie |
|---------------|-----------|
| `SCRIPT (E)` | Blad skryptu -- mod ma buga |
| `[ERROR]` | Blad na poziomie silnika |
| `ErrorMessage` | Fatalny blad mogacy spowodowac zamkniecie |
| `Cannot open` | Brakujacy plik (PBO, config, misja) |
| `Crash` | Awaria na poziomie aplikacji |

### Logi BattlEye

Logi BattlEye znajduja sie w katalogu `BattlEye/` wewnatrz glownego katalogu serwera. Pokazuja zdarzenia wyrzucenia i banu. Jesli gracze zglaszaja nieoczekiwane wyrzucanie, sprawdz najpierw tutaj.

---

## Szybka lista kontrolna diagnostyki

Gdy cos pojdzie nie tak, przejdz przez te liste po kolei:

```
1. Sprawdz RPT serwera pod katem linii SCRIPT (E) i [ERROR]
2. Sprawdz czy kazda sciezka -mod= istnieje i zawiera addons/*.pbo
3. Sprawdz czy wszystkie pliki .bikey sa skopiowane do keys/
4. Sprawdz serverDZ.cfg pod katem bledow skladni (brakujace sredniki)
5. Sprawdz przekierowanie portow: 2302 UDP + 27016 UDP
6. Sprawdz czy folder misji odpowiada wartosci template w serverDZ.cfg
7. Sprawdz storage_1/ pod katem uszkodzen (usun events.bin jesli trzeba)
8. Przetestuj bez modow, potem dodawaj mody jeden po drugim
```

Krok 8 to najpotezniejsza technika. Jesli serwer dziala w vanilli, ale psuje sie z modami, mozesz wyizolowac problematyczny mod przez wyszukiwanie binarne -- dodaj polowe swoich modow, przetestuj, a nastepnie zawez zakres.

---

[Strona glowna](../README.md) | [<< Poprzedni: Zarzadzanie modami](10-mod-management.md) | [Dalej: Tematy zaawansowane >>](12-advanced.md)
