# Chapter 9.3: Kompletna dokumentacja serverDZ.cfg

[Strona glowna](../README.md) | [<< Poprzedni: Struktura katalogow](02-directory-structure.md) | **Dokumentacja serverDZ.cfg** | [Dalej: Szczegolowy przewodnik po ekonomii lootu >>](04-loot-economy.md)

---

> **Podsumowanie:** Kazdy parametr w `serverDZ.cfg` udokumentowany z jego przeznaczeniem, prawidlowymi wartosciami i domyslnym zachowaniem. Ten plik kontroluje tozsamosc serwera, ustawienia sieciowe, reguly rozgrywki, przyspieszenie czasu i wybor misji.

---

## Spis tresci

- [Format pliku](#format-pliku)
- [Tozsamosc serwera](#tozsamosc-serwera)
- [Siec i bezpieczenstwo](#siec-i-bezpieczenstwo)
- [Reguly rozgrywki](#reguly-rozgrywki)
- [Czas i pogoda](#czas-i-pogoda)
- [Wydajnosc i kolejka logowania](#wydajnosc-i-kolejka-logowania)
- [Trwalosc i instancja](#trwalosc-i-instancja)
- [Wybor misji](#wybor-misji)
- [Kompletny przykladowy plik](#kompletny-przykladowy-plik)
- [Parametry uruchomienia nadpisujace konfiguracje](#parametry-uruchomienia-nadpisujace-konfiguracje)

---

## Format pliku

`serverDZ.cfg` uzywa formatu konfiguracji Bohemia (podobnego do C). Zasady:

- Kazde przypisanie parametru konczy sie **srednikiem** `;`
- Lancuchy znakow sa ujete w **podwojne cudzyslowy** `""`
- Komentarze uzywaja `//` dla jednej linii
- Blok `class Missions` uzywa nawiasow klamrowych `{}` i konczy sie `};`
- Plik musi byc zakodowany w UTF-8 lub ANSI -- bez BOM

Brakujacy srednik spowoduje, ze serwer cicho zawiedzie lub zignoruje nastepne parametry.

---

## Tozsamosc serwera

```cpp
hostname = "My DayZ Server";         // Nazwa serwera widoczna w przegladarce
password = "";                       // Haslo do polaczenia (puste = publiczny)
passwordAdmin = "";                  // Haslo do logowania administratora przez konsole w grze
description = "";                    // Opis widoczny w szczegolach przegladarki serwerow
```

| Parametr | Typ | Domyslnie | Uwagi |
|----------|-----|-----------|-------|
| `hostname` | string | `""` | Wyswietlane w przegladarce serwerow. Maksymalnie ~100 znakow. |
| `password` | string | `""` | Zostaw puste dla serwera publicznego. Gracze musza to wpisac, aby dolaczyc. |
| `passwordAdmin` | string | `""` | Uzywane z komenda `#login` w grze. **Ustaw to na kazdym serwerze.** |
| `description` | string | `""` | Wieloliniowe opisy nie sa obslugiwane. Pisz krotko. |

---

## Siec i bezpieczenstwo

```cpp
maxPlayers = 60;                     // Maksymalna liczba slotow dla graczy
verifySignatures = 2;                // Weryfikacja sygnatur PBO (tylko wartosc 2 jest obslugiwana)
forceSameBuild = 1;                  // Wymaganie pasujace wersji klient/serwer
enableWhitelist = 0;                 // Wlaczenie/wylaczenie bialej listy
disableVoN = 0;                      // Wylaczenie czatu glosowego
vonCodecQuality = 20;               // Jakosc dzwieku VoN (0-30)
guaranteedUpdates = 1;               // Protokol sieciowy (zawsze uzywaj 1)
```

| Parametr | Typ | Prawidlowe wartosci | Domyslnie | Uwagi |
|----------|-----|---------------------|-----------|-------|
| `maxPlayers` | int | 1-60 | 60 | Wplywa na zuzycie RAM. Kazdy gracz dodaje ~50-100 MB. |
| `verifySignatures` | int | 2 | 2 | Tylko wartosc 2 jest obslugiwana. Weryfikuje pliki PBO na podstawie kluczy `.bisign`. |
| `forceSameBuild` | int | 0, 1 | 1 | Gdy 1, klienci musza miec dokladnie taka sama wersje pliku wykonywalnego jak serwer. Zawsze trzymaj na 1. |
| `enableWhitelist` | int | 0, 1 | 0 | Gdy 1, tylko Steam64 ID wymienione w `whitelist.txt` moga sie polaczyc. |
| `disableVoN` | int | 0, 1 | 0 | Ustaw na 1, aby calkowicie wylaczyc czat glosowy w grze. |
| `vonCodecQuality` | int | 0-30 | 20 | Wyzsze wartosci oznaczaja lepsza jakosc glosu, ale wieksze zuzycie pasma. 20 to dobry kompromis. |
| `guaranteedUpdates` | int | 1 | 1 | Ustawienie protokolu sieciowego. Zawsze uzywaj 1. |

### Shard ID

```cpp
shardId = "123abc";                  // Szesc znakow alfanumerycznych dla prywatnych shardow
```

| Parametr | Typ | Domyslnie | Uwagi |
|----------|-----|-----------|-------|
| `shardId` | string | `""` | Uzywany dla serwerow z prywatnym hive. Gracze na serwerach z tym samym `shardId` wspoldziela dane postaci. Zostaw puste dla publicznego hive. |

---

## Reguly rozgrywki

```cpp
disable3rdPerson = 0;               // Wylaczenie kamery trzeciej osoby
disableCrosshair = 0;               // Wylaczenie celownika
disablePersonalLight = 1;           // Wylaczenie swiatla otoczenia gracza
lightingConfig = 0;                 // Jasnosc nocy (0 = jasniejsza, 1 = ciemniejsza)
```

| Parametr | Typ | Prawidlowe wartosci | Domyslnie | Uwagi |
|----------|-----|---------------------|-----------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | Ustaw na 1 dla serwerow tylko z pierwsza osoba. To najczestsze ustawienie "hardcore". |
| `disableCrosshair` | int | 0, 1 | 0 | Ustaw na 1, aby usunac celownik. Czesto laczone z `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | "Personal light" to subtelna poswiate wokol gracza w nocy. Wiekszosc serwerow je wylacza (wartosc 1) dla realizmu. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = jasniejsze noce (widoczne swiatlo ksiezyca). 1 = zupelnie ciemne noce (wymaga latarki/noktowizji). |

---

## Czas i pogoda

```cpp
serverTime = "SystemTime";                 // Czas poczatkowy
serverTimeAcceleration = 12;               // Mnoznik szybkosci czasu (0-24)
serverNightTimeAcceleration = 1;           // Mnoznik szybkosci nocy (0.1-64)
serverTimePersistent = 0;                  // Zapisywanie czasu miedzy restartami
```

| Parametr | Typ | Prawidlowe wartosci | Domyslnie | Uwagi |
|----------|-----|---------------------|-----------|-------|
| `serverTime` | string | `"SystemTime"` lub `"RRRR/MM/DD/GG/MM"` | `"SystemTime"` | `"SystemTime"` uzywa lokalnego zegara maszyny. Ustaw staly czas jak `"2024/9/15/12/0"` dla serwera z wiecznym dniem. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Mnoznik czasu w grze. Przy 12 pelny cykl 24-godzinny trwa 2 godziny realne. Przy 1 czas jest rzeczywisty. Przy 24 pelny dzien mija w 1 godzine. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Mnozone przez `serverTimeAcceleration`. Przy wartosci 4 z przyspieszeniem 12, noc mija z predkoscia 48x (bardzo krotkie noce). |
| `serverTimePersistent` | int | 0, 1 | 0 | Gdy 1, serwer zapisuje swoj zegar w grze na dysk i wznawia go po restarcie. Gdy 0, czas resetuje sie do `serverTime` przy kazdym restarcie. |

### Typowe konfiguracje czasu

**Zawsze dzien:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Szybki cykl dnia/nocy (2-godzinne dni, krotkie noce):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Czas rzeczywisty dnia/nocy:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Wydajnosc i kolejka logowania

```cpp
loginQueueConcurrentPlayers = 5;     // Gracze przetwarzani jednoczesnie podczas logowania
loginQueueMaxPlayers = 500;          // Maksymalny rozmiar kolejki logowania
```

| Parametr | Typ | Domyslnie | Uwagi |
|----------|-----|-----------|-------|
| `loginQueueConcurrentPlayers` | int | 5 | Ilu graczy moze sie ladowac jednoczesnie. Nizsze wartosci zmniejszaja skoki obciazenia serwera po restarcie. Zwieksz do 10-15, jesli twoj sprzet jest mocny, a gracze narzekaja na czas oczekiwania w kolejce. |
| `loginQueueMaxPlayers` | int | 500 | Jesli tylu graczy juz czeka w kolejce, nowe polaczenia sa odrzucane. 500 jest odpowiednie dla wiekszosci serwerow. |

---

## Trwalosc i instancja

```cpp
instanceId = 1;                      // Identyfikator instancji serwera
storageAutoFix = 1;                  // Automatyczna naprawa uszkodzonych plikow trwalosci
```

| Parametr | Typ | Domyslnie | Uwagi |
|----------|-----|-----------|-------|
| `instanceId` | int | 1 | Identyfikuje instancje serwera. Dane trwalosci sa przechowywane w `storage_<instanceId>/`. Jesli uruchamiasz wiele serwerow na jednej maszynie, nadaj kazdemu inny `instanceId`. |
| `storageAutoFix` | int | 1 | Gdy 1, serwer sprawdza pliki trwalosci przy starcie i zastepuje uszkodzone pustymi plikami. Zawsze zostawiaj na 1. |

---

## Wybor misji

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

Wartosc `template` musi dokladnie odpowiadac nazwie folderu wewnatrz `mpmissions/`. Dostepne misje vanillowe:

| Template | Mapa | Wymagane DLC |
|----------|------|:---:|
| `dayzOffline.chernarusplus` | Chernarus | Nie |
| `dayzOffline.enoch` | Livonia | Tak |
| `dayzOffline.sakhal` | Sakhal | Tak |

Niestandardowe misje (np. z modow lub map spolecznosci) uzywaja wlasnej nazwy szablonu. Folder musi istniec w `mpmissions/`.

---

## Kompletny przykladowy plik

To kompletny domyslny `serverDZ.cfg` ze wszystkimi parametrami:

```cpp
hostname = "EXAMPLE NAME";              // Nazwa serwera
password = "";                          // Haslo do polaczenia z serwerem
passwordAdmin = "";                     // Haslo do uzyskania uprawnien administratora

description = "";                       // Opis w przegladarce serwerow

enableWhitelist = 0;                    // Wlaczenie/wylaczenie bialej listy (wartosc 0-1)

maxPlayers = 60;                        // Maksymalna liczba graczy

verifySignatures = 2;                   // Weryfikacja plikow .pbo na podstawie plikow .bisign (tylko wartosc 2 jest obslugiwana)
forceSameBuild = 1;                     // Wymaganie pasujace wersji klient/serwer (wartosc 0-1)

disableVoN = 0;                         // Wlaczenie/wylaczenie czatu glosowego (wartosc 0-1)
vonCodecQuality = 20;                   // Jakosc kodeka czatu glosowego (wartosci 0-30)

shardId = "123abc";                     // Szesc znakow alfanumerycznych dla prywatnego shardu

disable3rdPerson = 0;                   // Przelaczanie widoku trzeciej osoby (wartosc 0-1)
disableCrosshair = 0;                   // Przelaczanie celownika (wartosc 0-1)

disablePersonalLight = 1;              // Wylaczenie swiatla osobistego dla wszystkich klientow
lightingConfig = 0;                     // 0 dla jasniejszej nocy, 1 dla ciemniejszej

serverTime = "SystemTime";             // Poczatkowy czas w grze ("SystemTime" lub "RRRR/MM/DD/GG/MM")
serverTimeAcceleration = 12;           // Mnoznik szybkosci czasu (0-24)
serverNightTimeAcceleration = 1;       // Mnoznik szybkosci nocy (0.1-64), rowniez mnozony przez serverTimeAcceleration
serverTimePersistent = 0;              // Zapisywanie czasu miedzy restartami (wartosc 0-1)

guaranteedUpdates = 1;                 // Protokol sieciowy (zawsze uzywaj 1)

loginQueueConcurrentPlayers = 5;       // Gracze przetwarzani jednoczesnie podczas logowania
loginQueueMaxPlayers = 500;            // Maksymalny rozmiar kolejki logowania

instanceId = 1;                        // ID instancji serwera (wplywa na nazwe folderu przechowywania)

storageAutoFix = 1;                    // Automatyczna naprawa uszkodzonej trwalosci (wartosc 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Parametry uruchomienia nadpisujace konfiguracje

Niektore ustawienia moga byc nadpisane parametrami wiersza polecen podczas uruchamiania `DayZServer_x64.exe`:

| Parametr | Nadpisuje | Przyklad |
|----------|-----------|---------|
| `-config=` | Sciezka do pliku konfiguracyjnego | `-config=serverDZ.cfg` |
| `-port=` | Port gry | `-port=2302` |
| `-profiles=` | Katalog wyjsciowy profili | `-profiles=profiles` |
| `-mod=` | Mody po stronie klienta (rozdzielone srednikami) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Mody tylko serwerowe | `-servermod=@MyServerMod` |
| `-BEpath=` | Sciezka do BattlEye | `-BEpath=battleye` |
| `-dologs` | Wlaczenie logowania | -- |
| `-adminlog` | Wlaczenie logowania administratora | -- |
| `-netlog` | Wlaczenie logowania sieci | -- |
| `-freezecheck` | Auto-restart po zawieszeniu | -- |
| `-cpuCount=` | Liczba rdzeni CPU do uzycia | `-cpuCount=4` |
| `-noFilePatching` | Wylaczenie patchowania plikow | -- |

### Pelny przyklad uruchomienia

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Mody sa ladowane w kolejnosci podanej w `-mod=`. Kolejnosc zaleznosci ma znaczenie: jesli Mod B wymaga Modu A, wymien Mod A jako pierwszy.

---

**Poprzedni:** [Struktura katalogow](02-directory-structure.md) | [Strona glowna](../README.md) | **Dalej:** [Szczegolowy przewodnik po ekonomii lootu >>](04-loot-economy.md)
