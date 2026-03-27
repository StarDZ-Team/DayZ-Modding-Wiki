# Chapter 9.7: Stan swiata i trwalosc danych

[Strona glowna](../README.md) | [<< Poprzedni: Spawn graczy](06-player-spawning.md) | [Dalej: Optymalizacja wydajnosci >>](08-performance.md)

Trwalosc danych DayZ utrzymuje swiat przy zyciu miedzy restartami. Zrozumienie jej dzialania pozwala zarzadzac bazami, planowac wipe'y i unikac uszkodzenia danych.

## Spis tresci

- [Jak dziala trwalosc danych](#jak-dziala-trwalosc-danych)
- [Katalog storage_1/](#katalog-storage_1)
- [Parametry trwalosci w globals.xml](#parametry-trwalosci-w-globalsxml)
- [System masztow flagowych](#system-masztow-flagowych)
- [Przedmioty hoarderow](#przedmioty-hoarderow)
- [Ustawienia trwalosci w cfggameplay.json](#ustawienia-trwalosci-w-cfggameplayjson)
- [Procedury czyszczenia serwera](#procedury-czyszczenia-serwera)
- [Strategia kopii zapasowych](#strategia-kopii-zapasowych)
- [Typowe bledy](#typowe-bledy)

---

## Jak dziala trwalosc danych

DayZ przechowuje stan swiata w katalogu `storage_1/` wewnatrz folderu profilu serwera. Cykl jest prosty:

1. Serwer zapisuje stan swiata okresowo (domyslnie co ~30 minut) i przy prawidlowym zamknieciu.
2. Przy restarcie serwer odczytuje `storage_1/` i przywraca wszystkie utrwalone obiekty -- pojazdy, bazy, namioty, beczki, ekwipunki graczy.
3. Przedmioty bez trwalosci (wiekszosc lootu na ziemi) sa generowane od nowa przez Centralna Ekonomie przy kazdym restarcie.

Jesli `storage_1/` nie istnieje przy starcie, serwer tworzy swiezy swiat bez danych graczy i bez zbudowanych struktur.

---

## Katalog storage_1/

Twoj profil serwera zawiera `storage_1/` z nastepujacymi podkatalogami i plikami:

| Sciezka | Zawartosc |
|---------|-----------|
| `data/` | Pliki binarne przechowujace obiekty swiata -- elementy baz, umieszczone przedmioty, pozycje pojazdow |
| `players/` | Pliki **.save** per-gracz indeksowane przez SteamID64. Kazdy plik przechowuje pozycje, ekwipunek, zdrowie, efekty statusowe |
| `snapshot/` | Migawki stanu swiata uzywane podczas operacji zapisu |
| `events.bin` / `events.xy` | Stan zdarzen dynamicznych -- sledzi lokalizacje rozbic helikopterow, pozycje konwojow i inne stworzonych zdarzen |

Folder `data/` stanowi wiekszosc trwalosci. Zawiera zserializowane dane obiektow, ktore serwer odczytuje przy starcie, aby zrekonstruowac swiat.

---

## Parametry trwalosci w globals.xml

Plik **globals.xml** (w folderze misji) kontroluje zegary czyszczenia i zachowanie flag. Oto wartosci zwiazane z trwaloscia:

```xml
<!-- Odswiezanie masztu flagowego -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 dni (sekundy) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 dni (sekundy) -->

<!-- Zegary czyszczenia -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Domyslne czyszczenie (sekundy) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Cialo martwego gracza: 1 godzina -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Martwe zwierze: 20 minut -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Martwy zombie: 5.5 minuty -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Zniszczony przedmiot: 5.5 minuty -->

<!-- Zachowanie czyszczenia -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Maks. przedmiotow czyszczonych na cykl -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Pomijaj czyszczenie w promieniu 100m od gracza -->
```

Wartosc `CleanupAvoidance` zapobiega despawnowi obiektow w poblizu aktywnych graczy. Jesli martwe cialo znajduje sie w promieniu 100 metrow od jakiegokolwiek gracza, pozostaje do momentu odejscia gracza lub zresetowania zegara.

---

## System masztow flagowych

Maszty flagowe sa rdzeniem trwalosci baz w DayZ. Oto jak dwie kluczowe wartosci wspoldzialaja:

- **FlagRefreshFrequency** (`432000` sekund = 5 dni) -- Jak czesto musisz wchodzic w interakcje z flaga, aby utrzymac ja aktywna. Podejdz do flagi i uzyj akcji "Odswiez".
- **FlagRefreshMaxDuration** (`3456000` sekund = 40 dni) -- Maksymalny skumulowany czas ochrony. Kazde odswiezenie dodaje do FlagRefreshFrequency wartosci czasu, ale suma nie moze przekroczyc tego limitu.

Gdy zegar flagi wygasa:

1. Sama flaga staje sie kwalifikowana do czyszczenia.
2. Wszystkie elementy budowania baz powiazane z ta flaga traca ochrone trwalosci.
3. W nastepnym cyklu czyszczenia niechronione elementy zaczynaja znikac.

Jesli obnizysz FlagRefreshFrequency, gracze musza czesciej odwiedzac swoje bazy. Jesli podniesiesz FlagRefreshMaxDuration, bazy przetrwaja dluzej miedzy wizytami. Dostosuj obie wartosci razem, aby pasowaly do stylu gry na twoim serwerze.

---

## Przedmioty hoarderow

W **cfgspawnabletypes.xml** pewne pojemniki sa oznaczone tagiem `<hoarder/>`. Oznacza to je jako przedmioty zdolne do przechowywania, ktore licza sie do limitow magazynowania per-gracz w Centralnej Ekonomii.

Vanillowe przedmioty hoarderow:

| Przedmiot | Typ |
|-----------|-----|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Beczki magazynowe |
| CarTent, LargeTent, MediumTent, PartyTent | Namioty |
| SeaChest | Magazyn podwodny |
| SmallProtectorCase | Mala zamykana walizka |
| UndergroundStash | Zakopana skrytka |
| WoodenCrate | Craftowalny pojemnik |

Przyklad z **cfgspawnabletypes.xml**:

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

Serwer sledzi ile przedmiotow hoarderowych kazdy gracz umiescil. Gdy limit zostanie osiagniety, nowe umieszczenia albo sie nie powioda, albo najstarszy przedmiot zniknie (w zaleznosci od konfiguracji serwera).

---

## Ustawienia trwalosci w cfggameplay.json

Plik **cfggameplay.json** w folderze misji zawiera ustawienia wplywajace na wytrzymalosc baz i pojemnikow:

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Ustawienie | Domyslnie | Efekt |
|------------|-----------|-------|
| `disableBaseDamage` | `false` | Gdy `true`, elementy budowania baz (sciany, bramy, wiezy wartownicze) nie moga byc uszkodzone. To efektywnie wylacza rajdy. |
| `disableContainerDamage` | `false` | Gdy `true`, pojemniki magazynowe (namioty, beczki, skrzynie) nie moga otrzymywac obrazen. Przedmioty wewnatrz pozostaja bezpieczne. |

Ustawienie obu na `true` tworzy serwer przyjazny PvE, gdzie bazy i magazyny sa niezniszczalne. Wiekszosc serwerow PvP zostawia oba na `false`.

---

## Procedury czyszczenia serwera

Masz cztery typy czyszczenia, kazdy celujacy w inna czesc `storage_1/`. **Zawsze zatrzymaj serwer przed wykonaniem jakiegokolwiek czyszczenia.**

### Pelne czyszczenie

Usun caly folder `storage_1/`. Serwer tworzy swiezy swiat przy nastepnym starcie. Wszystkie bazy, pojazdy, namioty, dane graczy i stan zdarzen sa skasowane.

### Czyszczenie ekonomii (zachowaj graczy)

Usun `storage_1/data/` ale pozostaw `storage_1/players/` nienaruszony. Gracze zachowuja postacie i ekwipunki, ale wszystkie umieszczone obiekty (bazy, namioty, beczki, pojazdy) sa usuwane.

### Czyszczenie graczy (zachowaj swiat)

Usun `storage_1/players/`. Wszystkie postacie graczy resetuja sie do swiezych spawnow. Bazy i umieszczone obiekty pozostaja na swiecie.

### Reset pogody / zdarzen

Usun `events.bin` lub `events.xy` z `storage_1/`. To resetuje pozycje zdarzen dynamicznych (rozbicia helikopterow, konwoje). Serwer generuje nowe lokalizacje zdarzen przy nastepnym starcie.

---

## Strategia kopii zapasowych

Dane trwalosci sa nie do zastapienia po utracie. Przestrzegaj tych praktyk:

- **Tworzenie kopii przy zatrzymanym serwerze.** Skopiuj caly folder `storage_1/` gdy serwer nie jest uruchomiony. Kopiowanie podczas pracy ryzukuje przechwycenie czesciowego lub uszkodzonego stanu.
- **Planuj kopie przed restartami.** Jesli uruchamiasz automatyczne restarty (co 4-6 godzin), dodaj krok kopiowania do skryptu restartu, ktory kopiuje `storage_1/` przed startem procesu serwera.
- **Zachowuj wiele generacji.** Rotuj kopie zapasowe, aby miec co najmniej 3 aktualne kopie. Jesli najnowsza kopia jest uszkodzona, mozesz cofnac sie do wczesniejszej.
- **Przechowuj poza maszyna.** Kopiuj kopie zapasowe na oddzielny dysk lub do chmury. Awaria dysku na maszynie serwera zabierze kopie zapasowe ze soba, jesli sa na tym samym dysku.

Minimalny skrypt kopii zapasowej (uruchamiany przed startem serwera):

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Typowe bledy

Powtarzaja sie regularnie w spolecznosciach administratorow serwerow:

| Blad | Co sie dzieje | Zapobieganie |
|------|---------------|--------------|
| Usuwanie `storage_1/` podczas pracy serwera | Uszkodzenie danych. Serwer zapisuje do plikow, ktore juz nie istnieja, powodujac awarie lub czesciowy stan przy nastepnym starcie. | Zawsze najpierw zatrzymaj serwer. |
| Brak kopii zapasowej przed czyszczeniem | Jesli przypadkowo usuniesz zly folder lub czyszczenie pojdzie nie tak, nie ma sposobu na odzyskanie. | Zrob kopie zapasowa `storage_1/` przed kazdym czyszczeniem. |
| Pomylenie resetu pogody z pelnym czyszczeniem | Usuniecie `events.xy` resetuje tylko pozycje zdarzen dynamicznych. Nie resetuje lootu, baz ani graczy. | Wiedz, ktore pliki kontroluja co (zobacz tabele katalogow powyzej). |
| Flaga nie odswiezona na czas | Po 40 dniach (FlagRefreshMaxDuration) flaga wygasa i wszystkie powiazane elementy bazy staja sie kwalifikowane do czyszczenia. Gracze traca cala baze. | Przypominaj graczom o interwale odswiezania. Obniz FlagRefreshMaxDuration na serwerach z mala populacja. |
| Edycja globals.xml podczas pracy serwera | Zmiany nie sa stosowane do restartu. Co gorsza, serwer moze nadpisac twoje edycje przy zamknieciu. | Edytuj pliki konfiguracyjne tylko gdy serwer jest zatrzymany. |

---

[Strona glowna](../README.md) | [<< Poprzedni: Spawn graczy](06-player-spawning.md) | [Dalej: Optymalizacja wydajnosci >>](08-performance.md)
