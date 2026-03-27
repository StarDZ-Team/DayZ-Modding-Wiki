# Chapter 9.1: Konfiguracja serwera i pierwszy start

[Strona glowna](../README.md) | **Konfiguracja serwera** | [Dalej: Struktura katalogow >>](02-directory-structure.md)

---

> **Podsumowanie:** Zainstaluj dedykowany serwer DayZ Standalone od zera za pomoca SteamCMD, uruchom go z minimalna konfiguracja, sprawdz czy pojawia sie w przegladarce serwerow i polacz sie jako gracz. Ten rozdzial obejmuje wszystko -- od wymagan sprzetowych po naprawianie najczestszych problemow z pierwszym uruchomieniem.

---

## Spis tresci

- [Wymagania wstepne](#wymagania-wstepne)
- [Instalacja SteamCMD](#instalacja-steamcmd)
- [Instalacja serwera DayZ](#instalacja-serwera-dayz)
- [Katalog po instalacji](#katalog-po-instalacji)
- [Pierwszy start z minimalna konfiguracja](#pierwszy-start-z-minimalna-konfiguracja)
- [Weryfikacja dzialania serwera](#weryfikacja-dzialania-serwera)
- [Laczenie sie jako gracz](#laczenie-sie-jako-gracz)
- [Typowe problemy z pierwszym uruchomieniem](#typowe-problemy-z-pierwszym-uruchomieniem)

---

## Wymagania wstepne

### Sprzet

| Komponent | Minimum | Zalecane |
|-----------|---------|----------|
| CPU | 4 rdzenie, 2.4 GHz | 6+ rdzeni, 3.5 GHz |
| RAM | 8 GB | 16 GB |
| Dysk | 20 GB SSD | 40 GB NVMe SSD |
| Siec | 10 Mbps upload | 50+ Mbps upload |
| System | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

Serwer DayZ jest jednowatkowy dla logiki rozgrywki. Taktowanie zegara jest wazniejsze niz liczba rdzeni.

### Oprogramowanie

- **SteamCMD** -- klient Steam uruchamiany z wiersza polecen do instalacji serwerow dedykowanych
- **Visual C++ Redistributable 2019** (Windows) -- wymagany przez `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- zwykle juz zainstalowany
- Porty **2302-2305 UDP** przekierowane na routerze/firewallu

---

## Instalacja SteamCMD

### Windows

1. Pobierz SteamCMD ze strony https://developer.valvesoftware.com/wiki/SteamCMD
2. Wypakuj `steamcmd.exe` do stalego folderu, np. `C:\SteamCMD\`
3. Uruchom `steamcmd.exe` raz -- zaktualizuje sie automatycznie

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## Instalacja serwera DayZ

Steam App ID serwera DayZ to **223350**. Mozesz go zainstalowac bez logowania na konto Steam posiadajace DayZ.

### Instalacja jednym poleceniem (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Instalacja jednym poleceniem (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Skrypt aktualizacji

Utworz skrypt, ktory mozesz ponownie uruchomic za kazdym razem, gdy wyjdzie aktualizacja:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Aktualizacja zakonczona.
pause
```

Flaga `validate` sprawdza kazdy plik pod katem uszkodzen. Przy swiezej instalacji spodziewaj sie pobrania 2-3 GB.

---

## Katalog po instalacji

Po instalacji glowny katalog serwera wyglada tak:

```
DayZServer/
  DayZServer_x64.exe        # Plik wykonywalny serwera
  serverDZ.cfg               # Glowna konfiguracja serwera
  dayzsetting.xml            # Ustawienia renderowania/wideo (nieistotne dla serwera dedykowanego)
  addons/                    # Pliki PBO vanilli (ai.pbo, animals.pbo, itp.)
  battleye/                  # Anty-cheat BattlEye (BEServer_x64.dll)
  dta/                       # Dane silnika (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Klucze weryfikacji sygnatur (dayz.bikey dla vanilli)
  logs/                      # Logi silnika (polaczenia, tresc, audio)
  mpmissions/                # Foldery misji
    dayzOffline.chernarusplus/   # Misja Chernarus
    dayzOffline.enoch/           # Misja Livonia (DLC)
    dayzOffline.sakhal/          # Misja Sakhal (DLC)
  profiles/                  # Dane wyjsciowe: logi RPT, logi skryptow, baza graczy
  ban.txt                    # Lista zbanowanych graczy (Steam64 ID)
  whitelist.txt              # Lista dozwolonych graczy (Steam64 ID)
  steam_appid.txt            # Zawiera "221100"
```

Wazne informacje:
- **Edytujesz** `serverDZ.cfg` i pliki wewnatrz `mpmissions/`.
- **Nigdy nie edytuj** plikow w `addons/` ani `dta/` -- sa nadpisywane przy kazdej aktualizacji.
- **Pliki PBO modow** trafiaja do glownego katalogu serwera lub podkatalogu (omowione w pozniejszym rozdziale).
- **`profiles/`** jest tworzony przy pierwszym uruchomieniu i zawiera logi skryptow oraz zrzuty awarii.

---

## Pierwszy start z minimalna konfiguracja

### Krok 1: Edycja serverDZ.cfg

Otworz `serverDZ.cfg` w edytorze tekstu. Do pierwszego testu uzyj najprostszej mozliwej konfiguracji:

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### Krok 2: Uruchomienie serwera

Otworz Wiersz polecen w katalogu serwera i uruchom:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Flaga | Przeznaczenie |
|-------|---------------|
| `-config=serverDZ.cfg` | Sciezka do pliku konfiguracyjnego |
| `-port=2302` | Glowny port gry (uzywa tez 2303-2305) |
| `-profiles=profiles` | Folder wyjsciowy dla logow i danych graczy |
| `-dologs` | Wlaczenie logowania serwera |
| `-adminlog` | Logowanie akcji administratora |
| `-netlog` | Logowanie zdarzen sieciowych |
| `-freezecheck` | Auto-restart po wykryciu zawieszenia |

### Krok 3: Oczekiwanie na inicjalizacje

Serwer potrzebuje 30-90 sekund na pelne uruchomienie. Obserwuj wyjscie konsoli. Gdy zobaczysz linie taka jak:

```
BattlEye Server: Initialized (v1.xxx)
```

...serwer jest gotowy na polaczenia.

---

## Weryfikacja dzialania serwera

### Metoda 1: Log skryptow

Sprawdz `profiles/` w poszukiwaniu pliku o nazwie `script_YYYY-MM-DD_HH-MM-SS.log`. Otworz go i szukaj:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Te linie potwierdzaja, ze ekonomia zostala zainicjalizowana, a misja zaladowana.

### Metoda 2: Plik RPT

Plik `.RPT` w `profiles/` pokazuje dane wyjsciowe na poziomie silnika. Szukaj:

```
Dedicated host created.
BattlEye Server: Initialized
```

### Metoda 3: Przegladarka serwerow Steam

Otworz Steam, przejdz do **Widok > Serwery gier > Ulubione**, kliknij **Dodaj serwer**, wpisz `127.0.0.1:2302` (lub twoj publiczny IP) i kliknij **Znajdz gry pod tym adresem**. Jesli serwer sie pojawi, dziala i jest osiagalny.

### Metoda 4: Port zapytan

Uzyj zewnetrznego narzedzia, takiego jak https://www.battlemetrics.com/ lub pakietu npm `gamedig`, aby odpytac port 27016 (port zapytan Steam = port gry + 24714).

---

## Laczenie sie jako gracz

### Z tego samego komputera

1. Uruchom DayZ (nie DayZ Server -- zwykly klient gry)
2. Otworz **Przegladarke serwerow**
3. Przejdz do zakladki **LAN** lub **Ulubione**
4. Dodaj `127.0.0.1:2302` do ulubionych
5. Kliknij **Polacz**

Jesli uruchamiasz klienta i serwer na tym samym komputerze, uzyj `DayZDiag_x64.exe` (klient diagnostyczny) zamiast klienta detalicznego. Uruchom za pomoca:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### Z innego komputera

Uzyj **publicznego IP** lub **IP w sieci LAN** swojego serwera, w zaleznosci od tego, czy klient jest w tej samej sieci. Porty 2302-2305 UDP musza byc przekierowane.

---

## Typowe problemy z pierwszym uruchomieniem

### Serwer uruchamia sie, ale natychmiast sie zamyka

**Przyczyna:** Brakujacy Visual C++ Redistributable lub blad skladni w `serverDZ.cfg`.

**Rozwiazanie:** Zainstaluj VC++ Redist 2019 (x64). Sprawdz `serverDZ.cfg` pod katem brakujacych srednikow -- kazda linia parametru musi konczyc sie znakiem `;`.

### "BattlEye initialization failed"

**Przyczyna:** Folder `battleye/` nie istnieje lub antywirus blokuje `BEServer_x64.dll`.

**Rozwiazanie:** Ponownie zweryfikuj pliki serwera za pomoca SteamCMD. Dodaj wyjatek antywirusa dla calego folderu serwera.

### Serwer dziala, ale nie pojawia sie w przegladarce

**Przyczyna:** Porty nie sa przekierowane lub Zapora systemu Windows blokuje plik wykonywalny.

**Rozwiazanie:**
1. Dodaj regule zapory systemu Windows dla `DayZServer_x64.exe` (zezwol na caly ruch UDP)
2. Przekieruj porty **2302-2305 UDP** na routerze
3. Sprawdz zewnetrznym narzedziem, czy port 2302 UDP jest otwarty na twoim publicznym IP

### "Version Mismatch" przy laczeniu

**Przyczyna:** Serwer i klient maja rozne wersje.

**Rozwiazanie:** Zaktualizuj oba. Uruchom polecenie aktualizacji SteamCMD dla serwera. Klient aktualizuje sie automatycznie przez Steam.

### Brak spawnu lootu

**Przyczyna:** Plik `init.c` nie istnieje lub Hive nie zostal zainicjalizowany.

**Rozwiazanie:** Sprawdz, czy `mpmissions/dayzOffline.chernarusplus/init.c` istnieje i zawiera `CreateHive()`. Sprawdz log skryptow pod katem bledow.

### Serwer uzywa 100% jednego rdzenia CPU

To jest normalne. Serwer DayZ jest jednowatkowy. Nie uruchamiaj wielu instancji serwera na tym samym rdzeniu -- uzyj koligacji procesora lub oddzielnych maszyn.

### Gracze pojawiaja sie jako wrony / utkneli na ekranie ladowania

**Przyczyna:** Szablon misji w `serverDZ.cfg` nie odpowiada istniejacemu folderowi w `mpmissions/`.

**Rozwiazanie:** Sprawdz wartosc template. Musi dokladnie odpowiadac nazwie folderu:

```cpp
template = "dayzOffline.chernarusplus";  // Musi odpowiadac nazwie folderu w mpmissions/
```

---

**[Strona glowna](../README.md)** | **Dalej:** [Struktura katalogow >>](02-directory-structure.md)
