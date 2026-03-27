# Chapter 9.10: Zarzadzanie modami

[Strona glowna](../README.md) | [<< Poprzedni: Kontrola dostepu](09-access-control.md) | [Dalej: Rozwiazywanie problemow >>](11-troubleshooting.md)

---

> **Podsumowanie:** Instalacja, konfiguracja i utrzymanie modow firm trzecich na dedykowanym serwerze DayZ. Obejmuje parametry uruchomienia, pobieranie z Workshop, klucze sygnatur, kolejnosc ladowania, mody tylko serwerowe vs wymagane przez klienta, aktualizacje i najczestsze bledy powodujace awarie lub wyrzucanie graczy.

---

## Spis tresci

- [Jak laduja sie mody](#jak-laduja-sie-mody)
- [Format parametrow uruchomienia](#format-parametrow-uruchomienia)
- [Instalacja modow z Workshop](#instalacja-modow-z-workshop)
- [Klucze modow (.bikey)](#klucze-modow-bikey)
- [Kolejnosc ladowania i zaleznosci](#kolejnosc-ladowania-i-zaleznosci)
- [Mody tylko serwerowe vs wymagane przez klienta](#mody-tylko-serwerowe-vs-wymagane-przez-klienta)
- [Aktualizacja modow](#aktualizacja-modow)
- [Rozwiazywanie konfliktow modow](#rozwiazywanie-konfliktow-modow)
- [Typowe bledy](#typowe-bledy)

---

## Jak laduja sie mody

DayZ laduje mody przez parametr uruchomienia `-mod=`. Kazdy wpis to sciezka do folderu zawierajacego pliki PBO i `config.cpp`. Silnik odczytuje kazdy PBO w kazdym folderze moda, rejestruje jego klasy i skrypty, a nastepnie przechodzi do nastepnego moda na liscie.

Serwer i klient musza miec te same mody w `-mod=`. Jesli serwer wymienia `@CF;@MyMod`, a klient ma tylko `@CF`, polaczenie nie powiedzie sie z bledem niezgodnosci sygnatur. Mody tylko serwerowe umieszczone w `-servermod=` sa wyjatkiem -- klienci nigdy ich nie potrzebuja.

---

## Format parametrow uruchomienia

Typowa komenda uruchomienia modowanego serwera:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Parametr | Przeznaczenie |
|----------|---------------|
| `-mod=` | Mody wymagane zarowno przez serwer jak i wszystkich laczacych sie klientow |
| `-servermod=` | Mody tylko serwerowe (klienci ich nie potrzebuja) |

Zasady:
- Sciezki sa **rozdzielone srednikami** bez spacji wokol srednikow
- Kazda sciezka jest wzgledna do glownego katalogu serwera (np. `@CF` oznacza `<root_serwera>/@CF/`)
- Mozesz uzywac sciezek bezwzglednych: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **Kolejnosc ma znaczenie** -- zaleznosci musza pojawic sie przed modami, ktore ich wymagaja

---

## Instalacja modow z Workshop

### Krok 1: Pobranie moda

Uzyj SteamCMD z App ID **klienta** DayZ (221100) i ID Workshop moda:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

Pobrane pliki trafiaja do:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Krok 2: Utworzenie dowiazania symbolicznego lub kopii

Foldery Workshop uzywaja numerycznych ID, ktore sa nieuzyteczne w `-mod=`. Utworz nazwane dowiazanie symboliczne (zalecane) lub skopiuj folder:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Uzycie dowiazania oznacza, ze aktualizacje przez SteamCMD sa automatycznie stosowane -- nie trzeba ponownie kopiowac.

### Krok 3: Skopiowanie .bikey

Zobacz nastepna sekcje.

---

## Klucze modow (.bikey)

Kazdy podpisany mod jest dostarczany z folderem `keys/` zawierajacym jeden lub wiecej plikow `.bikey`. Te pliki mowia BattlEye, ktore sygnatury PBO akceptowac.

1. Otworz folder moda (np. `@CF/keys/`)
2. Skopiuj kazdy plik `.bikey` do glownego katalogu `keys/` serwera

```
DayZServer/
  keys/
    dayz.bikey              # Vanilia -- zawsze obecny
    cf.bikey                # Skopiowany z @CF/keys/
    vpp_admintools.bikey    # Skopiowany z @VPPAdminTools/keys/
```

Bez prawidlowego klucza kazdy gracz uruchamiajacy ten mod otrzyma: **"Player kicked: Modified data"**.

---

## Kolejnosc ladowania i zaleznosci

Mody laduja sie od lewej do prawej w parametrze `-mod=`. `config.cpp` moda deklaruje jego zaleznosci:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Jesli `MyMod` wymaga `CF`, to `@CF` musi pojawic sie **przed** `@MyMod` w parametrze uruchomienia:

```
-mod=@CF;@MyMod          ✓ poprawnie
-mod=@MyMod;@CF          ✗ awaria lub brakujace klasy
```

**Ogolny wzorzec kolejnosci ladowania:**

1. **Mody frameworkowe** -- CF, Community-Online-Tools
2. **Mody biblioteczne** -- BuilderItems, dowolny wspoldzielony pakiet zasobow
3. **Mody funkcjonalne** -- dodatki map, bronie, pojazdy
4. **Mody zalezne** -- cokolwiek co wymienia powyzsze jako `requiredAddons`

W razie watpliwosci sprawdz strone Workshop moda lub jego dokumentacje. Wiekszosc autorow modow publikuje wymagana kolejnosc ladowania.

---

## Mody tylko serwerowe vs wymagane przez klienta

| Parametr | Kto potrzebuje | Typowe przyklady |
|----------|---------------|------------------|
| `-mod=` | Serwer + wszyscy klienci | Bronie, pojazdy, mapy, mody UI, ubrania |
| `-servermod=` | Tylko serwer | Menedzery ekonomii, narzedzia logowania, backendy administracyjne, skrypty planisty |

Zasada jest prosta: jesli mod zawiera **jakiekolwiek** skrypty po stronie klienta, layouty, tekstury lub modele, musi isc do `-mod=`. Jesli uruchamia tylko logike serwerowa bez zasobow, ktore klient kiedykolwiek dotyka, uzyj `-servermod=`.

Umieszczenie moda tylko serwerowego w `-mod=` zmusza kazdego gracza do jego pobrania. Umieszczenie moda wymaganego przez klienta w `-servermod=` powoduje brakujace tekstury, uszkodzony UI lub bledy skryptow po stronie klienta.

---

## Aktualizacja modow

### Procedura

1. **Zatrzymaj serwer** -- aktualizacja plikow podczas pracy serwera moze uszkodzic pliki PBO
2. **Pobierz ponownie** przez SteamCMD:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Skopiuj zaktualizowane pliki .bikey** -- autorzy modow czasami rotuja swoje klucze podpisywania. Zawsze kopiuj swiezy `.bikey` z folderu `keys/` moda do katalogu `keys/` serwera
4. **Zrestartuj serwer**

Jesli uzyles dowiazañ symbolicznych (junctions), krok 2 aktualizuje pliki moda na miejscu. Jesli kopiowales pliki recznie, musisz je skopiowac ponownie.

### Aktualizacje po stronie klienta

Gracze zasubskrybowani do moda na Steam Workshop otrzymuja aktualizacje automatycznie. Jesli zaktualizujesz mod na serwerze, a gracz ma stara wersje, otrzyma niezgodnosc sygnatur i nie bedzie mogl sie polaczyc, dopoki jego klient nie zostanie zaktualizowany.

---

## Rozwiazywanie konfliktow modow

### Sprawdz log RPT

Otworz najnowszy plik `.RPT` w `profiles/`. Szukaj:

- **"Cannot register"** -- kolizja nazw klas miedzy dwoma modami
- **"Missing addons"** -- zaleznos nie jest zaladowana (zla kolejnosc ladowania lub brakujacy mod)
- **"Signature verification failed"** -- niezgodnosc `.bikey` lub brakujacy klucz

### Sprawdz log skryptow

Otworz najnowszy `script_*.log` w `profiles/`. Szukaj:

- **Linie "SCRIPT (E)"** -- bledy skryptow, czesto spowodowane kolejnoscia ladowania lub niezgodnoscia wersji
- **"Definition of variable ... already exists"** -- dwa mody definiuja ta sama klase

### Izoluj problem

Gdy masz wiele modow i cos sie psuje, testuj stopniowo:

1. Zacznij od samych modow frameworkowych (`@CF`)
2. Dodaj jeden mod naraz
3. Uruchom i sprawdz logi po kazdym dodaniu
4. Mod powodujacy bledy jest winowajca

### Dwa mody edytujace ta sama klase

Jesli dwa mody oba uzywaja `modded class PlayerBase`, ten zaladowany **ostatni** (najdalej na prawo w `-mod=`) wygrywa. Jego wywolanie `super` prowadzi do wersji drugiego moda. To zwykle dziala, ale jesli jeden mod nadpisuje metode bez wywolywania `super`, zmiany drugiego moda sa tracone.

---

## Typowe bledy

**Zla kolejnosc ladowania.** Serwer ulega awarii lub loguje "Missing addons", poniewaz zaleznosc nie byla jeszcze zaladowana. Rozwiazanie: przenies mod zaleznosci wczesniej na liscie `-mod=`.

**Zapomnienie o `-servermod=` dla modow tylko serwerowych.** Gracze sa zmuszeni do pobrania moda, ktorego nie potrzebuja. Rozwiazanie: przenies mody tylko serwerowe z `-mod=` do `-servermod=`.

**Brak aktualizacji plikow `.bikey` po aktualizacji moda.** Gracze sa wyrzucani z bledem "Modified data", poniewaz klucz serwera nie odpowiada nowym sygnaturom PBO moda. Rozwiazanie: zawsze ponownie kopiuj pliki `.bikey` przy aktualizacji modow.

**Przepakowywanie PBO modow.** Przepakowanie plikow PBO moda lamie jego cyfrowa sygnature, powoduje wyrzucanie BattlEye dla kazdego gracza i narusza warunki wiekszosci autorow modow. Nigdy nie przepakowuj moda, ktorego nie stworzylesz.

**Mieszanie sciezek Workshop ze scieżkami lokalnymi.** Uzywanie surowej numerycznej sciezki Workshop dla niektorych modow i nazwanych folderow dla innych powoduje zamieszanie przy aktualizacjach. Wybierz jedno podejscie -- dowiazania symboliczne sa najczystsze.

**Spacje w sciezkach modow.** Sciezka jak `-mod=@My Mod` psuje parsowanie. Zmien nazwy folderow modow, aby unikac spacji, lub otocz caly parametr cudzyslowami: `-mod="@My Mod;@CF"`.

**Przestarzaly mod na serwerze, zaktualizowany na kliencie (lub odwrotnie).** Niezgodnosc wersji uniemozliwia polaczenie. Synchronizuj wersje serwera i Workshop. Aktualizuj wszystkie mody i serwer w tym samym czasie.

---

[Strona glowna](../README.md) | [<< Poprzedni: Kontrola dostepu](09-access-control.md) | [Dalej: Rozwiazywanie problemow >>](11-troubleshooting.md)
