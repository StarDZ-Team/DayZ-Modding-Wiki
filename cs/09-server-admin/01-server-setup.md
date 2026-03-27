# Chapter 9.1: Nastaveni serveru a prvni spusteni

[Domu](../README.md) | **Nastaveni serveru** | [Dalsi: Adresarova struktura >>](02-directory-structure.md)

---

> **Shruti:** Nainstalujte dedickovany server DayZ Standalone od nuly pomoci SteamCMD, spustte jej s minimalni konfiguraci, overte, ze se objevi v prohlizeci serveru, a pripojte se jako hrac. Tato kapitola pokryva vse od hardwarovych pozadavku az po opravu nejcastejsich problemu pri prvnim spusteni.

---

## Obsah

- [Predpoklady](#predpoklady)
- [Instalace SteamCMD](#instalace-steamcmd)
- [Instalace serveru DayZ](#instalace-serveru-dayz)
- [Adresar po instalaci](#adresar-po-instalaci)
- [Prvni spusteni s minimalni konfiguraci](#prvni-spusteni-s-minimalni-konfiguraci)
- [Overeni, ze server bezi](#overeni-ze-server-bezi)
- [Pripojeni jako hrac](#pripojeni-jako-hrac)
- [Caste problemy pri prvnim spusteni](#caste-problemy-pri-prvnim-spusteni)

---

## Predpoklady

### Hardware

| Komponenta | Minimum | Doporuceno |
|-----------|---------|-------------|
| CPU | 4 jadra, 2,4 GHz | 6+ jader, 3,5 GHz |
| RAM | 8 GB | 16 GB |
| Disk | 20 GB SSD | 40 GB NVMe SSD |
| Sit | 10 Mbps upload | 50+ Mbps upload |
| OS | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

DayZ Server je jednovlaknovy pro herní logiku. Taktovaci frekvence je dulezitejsi nez pocet jader.

### Software

- **SteamCMD** -- prikazovy radkovy klient Steamu pro instalaci dedickovanych serveru
- **Visual C++ Redistributable 2019** (Windows) -- vyzadovano souborem `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- obvykle jiz nainstalovano
- Porty **2302-2305 UDP** presmerovane na vasem routeru/firewallu

---

## Instalace SteamCMD

### Windows

1. Stahnete SteamCMD z https://developer.valvesoftware.com/wiki/SteamCMD
2. Rozbalte `steamcmd.exe` do trvale slozky, napr. `C:\SteamCMD\`
3. Spustte `steamcmd.exe` jednou -- automaticky se aktualizuje

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## Instalace serveru DayZ

Steam App ID serveru DayZ je **223350**. Muzete jej nainstalovat bez prihlaseni k uctu Steamu, ktery vlastni DayZ.

### Jednoradkova instalace (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Jednoradkova instalace (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Aktualizacni skript

Vytvorte skript, ktery muzete znovu spustit pri kazdem vydani patche:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Aktualizace dokoncena.
pause
```

Priznak `validate` kontroluje kazdy soubor na poskozeni. Pri ciste instalaci ocekavejte stahovani 2-3 GB.

---

## Adresar po instalaci

Po instalaci vypada korenovy adresar serveru takto:

```
DayZServer/
  DayZServer_x64.exe        # Spustitelny soubor serveru
  serverDZ.cfg               # Hlavni konfigurace serveru
  dayzsetting.xml            # Nastaveni vykresleni/videa (nerelevantni pro dedickovany server)
  addons/                    # Vanilkove PBO soubory (ai.pbo, animals.pbo atd.)
  battleye/                  # BattlEye anti-cheat (BEServer_x64.dll)
  dta/                       # Zakladni data enginu (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Podpisove klice (dayz.bikey pro vanilku)
  logs/                      # Logy enginu (pripojeni, obsah, zvuk)
  mpmissions/                # Slozky misi
    dayzOffline.chernarusplus/   # Mise pro Chernarus
    dayzOffline.enoch/           # Mise pro Livonii (DLC)
    dayzOffline.sakhal/          # Mise pro Sakhal (DLC)
  profiles/                  # Vystup za behu: RPT logy, logy skriptu, databaze hracu
  ban.txt                    # Seznam zablokovanych hracu (Steam64 ID)
  whitelist.txt              # Hráci na whitelistu (Steam64 ID)
  steam_appid.txt            # Obsahuje "221100"
```

Klicove body:
- **Upravujete** `serverDZ.cfg` a soubory uvnitr `mpmissions/`.
- **Nikdy neupravujte** soubory v `addons/` nebo `dta/` -- jsou prepsany pri kazde aktualizaci.
- **PBO modu** se umistuji do korenoveho adresare serveru nebo do podslozky (probrano v pozdejsi kapitole).
- **`profiles/`** se vytvori pri prvnim spusteni a obsahuje vase logy skriptu a dumpy padu.

---

## Prvni spusteni s minimalni konfiguraci

### Krok 1: Upravte serverDZ.cfg

Otevrte `serverDZ.cfg` v textovem editoru. Pro prvni test pouzijte co nejjednodussi konfiguraci:

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

### Krok 2: Spustte server

Otevrte prikazovy radek v adresari serveru a spustte:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Priznak | Ucel |
|------|---------|
| `-config=serverDZ.cfg` | Cesta ke konfiguracnimu souboru |
| `-port=2302` | Hlavni herní port (pouziva take 2303-2305) |
| `-profiles=profiles` | Vystupni slozka pro logy a data hracu |
| `-dologs` | Povoleni logovani serveru |
| `-adminlog` | Logovani adminskych akci |
| `-netlog` | Logovani sitovych udalosti |
| `-freezecheck` | Automaticky restart pri detekci zamrznuti |

### Krok 3: Pockejte na inicializaci

Server potrebuje 30-90 sekund na plne spusteni. Sledujte vystup konzole. Kdyz uvidite radek jako:

```
BattlEye Server: Initialized (v1.xxx)
```

...server je pripraven na pripojeni.

---

## Overeni, ze server bezi

### Metoda 1: Log skriptu

Zkontrolujte v `profiles/` soubor s nazvem jako `script_YYYY-MM-DD_HH-MM-SS.log`. Otevrte jej a hledejte:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Tyto radky potvrzuji, ze se ekonomika inicializovala a mise se nahral.

### Metoda 2: RPT soubor

Soubor `.RPT` v `profiles/` ukazuje vystup na urovni enginu. Hledejte:

```
Dedicated host created.
BattlEye Server: Initialized
```

### Metoda 3: Prohlizec serveru ve Steamu

Otevrte Steam, prejdete na **Zobrazit > Herní servery > Oblibene**, kliknete na **Pridat server**, zadejte `127.0.0.1:2302` (nebo vasi verejnou IP) a kliknete na **Najit hry na teto adrese**. Pokud se server objevi, bezi a je dostupny.

### Metoda 4: Dotazovaci port

Pouzijte externi nastroj jako https://www.battlemetrics.com/ nebo balicek `gamedig` npm pro dotaz na port 27016 (dotazovaci port Steamu = herní port + 24714).

---

## Pripojeni jako hrac

### Ze stejneho pocitace

1. Spustte DayZ (ne DayZ Server -- bezny herní klient)
2. Otevrte **Prohlizec serveru**
3. Prejdete na kartu **LAN** nebo **Oblibene**
4. Pridejte `127.0.0.1:2302` do oblibenych
5. Kliknete na **Pripojit**

Pokud spoustite klienta a server na stejnem pocitaci, pouzijte `DayZDiag_x64.exe` (diagnosticky klient) misto retailoveho klienta. Spustte s:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### Z jineho pocitace

Pouzijte **verejnou IP** nebo **LAN IP** vaseho serveru podle toho, zda je klient na stejne siti. Porty 2302-2305 UDP musi byt presmerovany.

---

## Caste problemy pri prvnim spusteni

### Server se spusti, ale okamzite se zavre

**Pricina:** Chybejici Visual C++ Redistributable nebo syntakticka chyba v `serverDZ.cfg`.

**Reseni:** Nainstalujte VC++ Redist 2019 (x64). Zkontrolujte `serverDZ.cfg` na chybejici stredniky -- kazdy radek parametru musi koncit `;`.

### "BattlEye initialization failed"

**Pricina:** Slozka `battleye/` chybi nebo antivirus blokuje `BEServer_x64.dll`.

**Reseni:** Znovu oveřte soubory serveru pres SteamCMD. Pridejte vyjimku antiviroveho programu pro celou slozku serveru.

### Server bezi, ale neobjevuje se v prohlizeci

**Pricina:** Porty nejsou presmerovany, nebo Windows Firewall blokuje spustitelny soubor.

**Reseni:**
1. Pridejte pravidlo prichozich spojeni ve Windows Firewall pro `DayZServer_x64.exe` (povolit vsechny UDP)
2. Presmerujte porty **2302-2305 UDP** na vasem routeru
3. Zkontrolujte pomoci externiho nastroje pro kontrolu portu, ze 2302 UDP je otevreny na vasi verejne IP

### "Version Mismatch" pri pripojovani

**Pricina:** Server a klient jsou na ruznych verzich.

**Reseni:** Aktualizujte oba. Spustte prikaz SteamCMD pro aktualizaci serveru. Klient se aktualizuje automaticky pres Steam.

### Nespawnuje se loot

**Pricina:** Soubor `init.c` chybi nebo se Hive neinicializoval.

**Reseni:** Overte, ze `mpmissions/dayzOffline.chernarusplus/init.c` existuje a obsahuje `CreateHive()`. Zkontrolujte log skriptu na chyby.

### Server pouziva 100 % jednoho jadra CPU

To je normalni. DayZ Server je jednovlaknovy. Nespoustejte vice instanci serveru na stejnem jadre -- pouzijte afinitu procesoru nebo oddelene pocitace.

### Hraci se spawnuji jako vrany / zaseknou se v nacitani

**Pricina:** Sablona mise v `serverDZ.cfg` neodpovida existujici slozce v `mpmissions/`.

**Reseni:** Zkontrolujte hodnotu template. Musi presne odpovidat nazvu slozky:

```cpp
template = "dayzOffline.chernarusplus";  // Musi odpovidat nazvu slozky v mpmissions/
```

---

**[Domu](../README.md)** | **Dalsi:** [Adresarova struktura >>](02-directory-structure.md)
