# Chapter 9.8: Optymalizacja wydajnosci

[Strona glowna](../README.md) | [<< Poprzedni: Trwalosc danych](07-persistence.md) | [Dalej: Kontrola dostepu >>](09-access-control.md)

---

> **Podsumowanie:** Wydajnosc serwera w DayZ sprowadza sie do trzech rzeczy: liczby przedmiotow, zdarzen dynamicznych i obciazenia modami/graczami. Ten rozdzial omawia konkretne ustawienia, ktore maja znaczenie, jak diagnozowac problemy i jaki sprzet naprawde pomaga -- wszystko oparte na prawdziwych danych spolecznosci z 400+ raportow Discord dotyczacych spadkow FPS, lagow i desyncu.

---

## Spis tresci

- [Co wplywa na wydajnosc serwera](#co-wplywa-na-wydajnosc-serwera)
- [Dostrajanie globals.xml](#dostrajanie-globalsxml)
- [Dostrajanie ekonomii pod katem wydajnosci](#dostrajanie-ekonomii-pod-katem-wydajnosci)
- [Logowanie cfgeconomycore.xml](#logowanie-cfgeconomycorexml)
- [Ustawienia wydajnosci serverDZ.cfg](#ustawienia-wydajnosci-serverdzcfg)
- [Wplyw modow na wydajnosc](#wplyw-modow-na-wydajnosc)
- [Zalecenia sprzetowe](#zalecenia-sprzetowe)
- [Monitorowanie stanu serwera](#monitorowanie-stanu-serwera)
- [Typowe bledy wydajnosci](#typowe-bledy-wydajnosci)

---

## Co wplywa na wydajnosc serwera

Z danych spolecznosci (400+ wspomnien o FPS/wydajnosci/lagach/desyncu na Discord), trzy najwieksze czynniki wydajnosci to:

1. **Liczba przedmiotow** -- wysokie wartosci `nominal` w `types.xml` oznaczaja, ze Centralna Ekonomia sledzi i przetwarza wiecej obiektow w kazdym cyklu. To jest konsekwentnie przyczyna numer jeden lagow po stronie serwera.
2. **Spawn zdarzen** -- zbyt wiele aktywnych zdarzen dynamicznych (pojazdy, zwierzeta, rozbicia helikopterow) w `events.xml` zuzywa cykle spawnu/czyszczenia i sloty obiektow.
3. **Liczba graczy + liczba modow** -- kazdy polaczony gracz generuje aktualizacje obiektow, a kazdy mod dodaje klasy skryptow, ktore silnik musi kompilowac i wykonywac co tick.

Petla gry serwera dziala ze stalym tickrate 30 FPS. Gdy serwer nie moze utrzymac 30 FPS, gracze doswiadczaja desyncu -- gumowania, opoznionych podnoszonych przedmiotow i bledow rejestracji trafien. Ponizej 15 FPS serwera gra staje sie niegrywalna.

---

## Dostrajanie globals.xml

Oto vanillowe domyslne wartosci parametrow bezposrednio wplywajacych na wydajnosc:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### Co kontroluje kazda wartosc

| Parametr | Domyslnie | Wplyw na wydajnosc |
|----------|-----------|---------------------|
| `ZombieMaxCount` | 1000 | Limit calkowitej liczby zarazonych na serwerze. Kazdy zombie uzywa pathfindingu AI. Obnizenie do 500-700 zauwaznie poprawia FPS serwera na zaludnionych serwerach. |
| `AnimalMaxCount` | 200 | Limit zwierzat. Zwierzeta maja prostsza AI niz zombie, ale nadal zuzywaja czas ticku. Obniz do 100, jesli widzisz problemy z FPS. |
| `ZoneSpawnDist` | 300 | Odleglosc w metrach, przy ktorej strefy zombie aktywuja sie wokol graczy. Obnizenie do 200 oznacza mniej jednoczesnie aktywnych stref. |
| `SpawnInitial` | 1200 | Liczba przedmiotow, ktore CE tworzy przy pierwszym starcie. Wyzsze wartosci oznaczaja dluzsze poczatkowe ladowanie. Nie wplywa na wydajnosc w stanie ustalonym. |
| `CleanupLifetimeDefault` | 45 | Domyslny czas czyszczenia w sekundach dla przedmiotow bez okreslonego lifetime. Nizsze wartosci oznaczaja szybsze cykle czyszczenia, ale czestsze przetwarzanie CE. |

**Zalecany profil wydajnosci** (dla serwerow majacych problemy powyzej 40 graczy):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Dostrajanie ekonomii pod katem wydajnosci

Centralna Ekonomia dziala w ciaglej petli sprawdzajac kazdy typ przedmiotu wzgledem celow `nominal`/`min`. Wiecej typow przedmiotow z wyzszymi nominalami oznacza wiecej pracy na cykl.

### Redukuj wartosci nominal

Kazdy przedmiot w `types.xml` z `nominal > 0` jest sledzony przez CE. Jesli masz 2000 typow przedmiotow ze srednim nominal rownym 20, CE zarzadza 40 000 obiektami. Redukuj nominaly ogolnie, aby zmniejszyc te liczbe:

- Popularne przedmioty cywilne: obniz z 15-40 do 10-25
- Bronie: zachowaj niskie (vanilia to juz 2-10)
- Warianty kolorystyczne ubran: rozważ wylaczenie wariantow, ktorych nie potrzebujesz (`nominal=0`)

### Redukuj zdarzenia dynamiczne

W `events.xml` kazde aktywne zdarzenie tworzy i monitoruje grupy obiektow. Obniz `nominal` na zdarzeniach pojazdow i zwierzat lub ustaw `<active>0</active>` na zdarzeniach, ktorych nie potrzebujesz.

### Uzyj trybu bezczynnosci

Gdy zaden gracz nie jest polaczony, CE moze sie calkowicie wstrzymac:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` oznacza, ze serwer wchodzi w tryb bezczynnosci 60 sekund po rozlaczeniu ostatniego gracza. `IdleModeStartup=1` oznacza, ze serwer startuje w trybie bezczynnosci i aktywuje CE dopiero gdy pierwszy gracz sie polaczy. Zapobiega to obracaniu serwera przez cykle spawnu podczas pustego stanu.

### Dostosuj czestotliwosc odnowien

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Te wartosci kontroluja ile przedmiotow i typow przedmiotow CE przetwarza na cykl. Nizsze wartosci zmniejszaja obciazenie CE na tick, ale spowalniaja odnowienie lootu. Vanillowe domyslne wartosci powyzej sa juz zachowawcze.

---

## Logowanie cfgeconomycore.xml

Wlacz tymczasowo logi diagnostyczne CE, aby zmierzyc czasy cykli i zidentyfikowac waskie gardla. W twoim `cfgeconomycore.xml`:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Aby zdiagnozowac wydajnosc, ustaw `log_ce_statistics` na `"true"`. Generuje to czasy cykli CE w logu RPT serwera. Szukaj linii pokazujacych jak dlugo trwa kazdy cykl CE -- jesli cykle przekraczaja 1000ms, ekonomia jest przeciazona.

Ustaw `log_ce_lootspawn` i `log_ce_lootcleanup` na `"true"`, aby zobaczyc, ktore typy przedmiotow pojawiaja sie i sa czyszczone najczesciej. To sa twoi kandydaci do redukcji nominal.

**Wylacz logowanie po diagnozie.** Same zapisy logow zuzywaja I/O i moga pogorszyc wydajnosc, jesli pozostana wlaczone na stale.

---

## Ustawienia wydajnosci serverDZ.cfg

Glowny plik konfiguracyjny serwera ma ograniczone opcje zwiazane z wydajnoscia:

| Ustawienie | Efekt |
|------------|-------|
| `maxPlayers` | Obniz to, jesli serwer ma problemy. Kazdy gracz generuje ruch sieciowy i aktualizacje obiektow. Zmiana z 60 na 40 graczy moze odzyskac 5-10 FPS serwera. |
| `instanceId` | Okresla sciezke `storage_1/`. Nie jest ustawieniem wydajnosci, ale jesli twoj magazyn jest na wolnym dysku, wplywa na I/O trwalosci. |

**Czego nie mozesz zmienic:** tickrate serwera jest ustalony na 30 FPS. Nie ma ustawienia, aby go zwiekszyc lub zmniejszyc. Jesli serwer nie moze utrzymac 30 FPS, po prostu dziala wolniej.

---

## Wplyw modow na wydajnosc

Kazdy mod dodaje klasy skryptow, ktore silnik kompiluje przy starcie i wykonuje co tick. Wplyw rozni sie dramatycznie w zaleznosci od jakosci moda:

- **Mody tylko z zawartoscia** (bronie, ubrania, budynki) dodaja typy przedmiotow, ale minimalne obciazenie skryptami. Ich koszt lezy w sledzeniu CE, nie przetwarzaniu tickow.
- **Mody ciezkie skryptowo** z petlami `OnUpdate()` lub `OnTick()` wykonuja kod co klatke serwera. Zle zoptymalizowane petle w tych modach sa najczestsza przyczyna lagow zwiazanych z modami.
- **Mody traderskie/ekonomiczne** utrzymujace duze ekwipunki dodaja trwale obiekty, ktore silnik musi sledzic.

### Wytyczne

- Dodawaj mody stopniowo. Testuj FPS serwera po kazdym dodaniu, nie po dodaniu 10 na raz.
- Monitoruj FPS serwera narzedziami administratorskimi lub wyjsciem logu RPT po dodaniu nowych modow.
- Jesli mod powoduje problemy, sprawdz jego zrodlo pod katem kosztownych operacji per-klatka.

Konsensus spolecznosci: "Przedmioty (typy) i spawn zdarzen sa najbardziej wymagajace -- mody dodajace tysiace wpisow types.xml daja wiecej w kosc niz mody dodajace zlozne skrypty."

---

## Zalecenia sprzetowe

Logika gry serwera DayZ jest **jednowatkowa**. Procesory wielordzeniowe pomagaja z obsluga systemu operacyjnego i I/O sieci, ale glowna petla gry dziala na jednym rdzeniu.

| Komponent | Zalecenie | Dlaczego |
|-----------|-----------|----------|
| **CPU** | Najwyzsza mozliwa wydajnosc jednowatkowa. AMD 5600X lub lepszy. | Petla gry jest jednowatkowa. Taktowanie zegara i IPC maja wieksze znaczenie niz liczba rdzeni. |
| **RAM** | 8 GB minimum, 12-16 GB dla ciezko modowanych serwerow | Mody i duze mapy zuzywaja pamiec. Brak pamieci powoduje drgania. |
| **Dysk** | SSD wymagany | I/O trwalosci `storage_1/` jest ciagly. HDD powoduje przycinanie podczas cykli zapisu. |
| **Siec** | 100 Mbps+ z niskim opoznieniem | Przepustowosc ma mniejsze znaczenie niz stabilnosc pingu dla zapobiegania desyncowi. |

Wskazowka spolecznosci: "OVH oferuje dobry stosunek jakosci do ceny -- okolo 60 USD za dedykowana maszyne 5600X, ktora obsluguje 60-slotowe modowane serwery."

Unikaj hostingu wspoldzielonego/VPS dla zaludnionych serwerow. Problem halaslliwego sasiada na wspoldzielonym sprzecie powoduje nieprzewidywalne spadki FPS, ktore sa niemozliwe do zdiagnozowania z twojej strony.

---

## Monitorowanie stanu serwera

### FPS serwera

Sprawdz log RPT pod katem linii zawierajacych FPS serwera. Zdrowy serwer utrzymuje 30 FPS konsekwentnie. Progi ostrzegawcze:

| FPS serwera | Status |
|-------------|--------|
| 25-30 | Normalny. Drobne wahania sa spodziewane podczas intensywnych walk lub restartow. |
| 15-25 | Pogorszony. Gracze zauwazaja desync przy interakcjach z przedmiotami i walce. |
| Ponizej 15 | Krytyczny. Gumowanie, nieudane akcje, uszkodzona rejestracja trafien. |

### Ostrzezenia cyklu CE

Z wlaczonym `log_ce_statistics` obserwuj czasy cykli CE. Normalny jest ponizej 500ms. Jesli cykle regularnie przekraczaja 1000ms, twoja ekonomia jest zbyt ciezka.

### Wzrost magazynu

Monitoruj rozmiar `storage_1/`. Niekontrolowany wzrost wskazuje na rozrost trwalosci -- zbyt wiele umieszczonych obiektow, namiotow lub skrytek narastajacych. Regularne wipe'y serwera lub redukcja `FlagRefreshMaxDuration` w `globals.xml` pomagaja to kontrolowac.

### Raporty graczy

Raporty desyncu od graczy sa twoim najbardziej niezawodnym wskaznikiem w czasie rzeczywistym. Jesli wielu graczy jednoczesnie zglasza gumowanie, FPS serwera spadl ponizej 15.

---

## Typowe bledy wydajnosci

### Zbyt wysokie wartosci nominal

Ustawienie kazdego przedmiotu na `nominal=50` bo "wiecej lootu to frajda" tworzy dziesiatki tysiecy sledzonych obiektow. CE spedza caly swoj cykl na zarzadzaniu przedmiotami zamiast na prowadzeniu gry. Zacznij od vanillowych nominalow i zwiekszaj selektywnie.

### Zbyt wiele zdarzen pojazdow

Pojazdy sa kosztownymi obiektami z symulacja fizyki, sledzeniem zalacznikow i trwaloscia. Vanilia tworzy okolo 50 pojazdow lacznie. Serwery uruchamiajace 150+ pojazdow obserwuja znaczny spadek FPS.

### Uruchamianie 30+ modow bez testowania

Kazdy mod jest w porzadku w izolacji. Skumulowany efekt 30+ modow -- tysiace dodatkowych typow, dziesiatki skryptow per-klatka i zwiekszona presja na pamiec -- moze obnizyc FPS serwera o 50% lub wiecej. Dodawaj mody partiami po 3-5 i testuj po kazdej partii.

### Nigdy nie restartowanie serwera

Niektore mody maja wycieki pamieci, ktore narastaja z czasem. Zaplanuj automatyczne restarty co 4-6 godzin. Wiekszosc paneli hostingowych to obsluguje. Nawet dobrze napisane mody korzystaja z okresowych restartow, poniewaz fragmentacja pamieci silnika zwieksza sie przy dlugich sesjach.

### Ignorowanie rozrostu magazynu

Folder `storage_1/` rosnacy do kilku gigabajtow spowalnia kazdy cykl trwalosci. Czyscij lub przycinaj go okresowo, zwlaszcza jesli zezwalasz na budowanie baz bez limitow rozpadu.

### Logowanie pozostawione wlaczone

Diagnostyczne logowanie CE, debugowe logowanie skryptow i logowanie narzedzi administratorskich zapisuja na dysku co tick. Wlaczaj je do diagnozy, a potem wylaczaj. Trwale rozbudowane logowanie na zajetym serwerze moze kosztowac 1-2 FPS samo w sobie.

---

[Strona glowna](../README.md) | [<< Poprzedni: Trwalosc danych](07-persistence.md) | [Dalej: Kontrola dostepu >>](09-access-control.md)
