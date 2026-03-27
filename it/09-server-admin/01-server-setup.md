# Chapter 9.1: Configurazione del Server e Primo Avvio

[Home](../README.md) | **Configurazione del Server** | [Successivo: Struttura delle Directory >>](02-directory-structure.md)

---

> **Riepilogo:** Installa un server dedicato DayZ Standalone da zero usando SteamCMD, avvialo con una configurazione minima, verifica che appaia nel browser dei server e connettiti come giocatore. Questo capitolo copre tutto, dai requisiti hardware alla risoluzione dei problemi piu comuni al primo avvio.

---

## Indice

- [Prerequisiti](#prerequisiti)
- [Installazione di SteamCMD](#installazione-di-steamcmd)
- [Installazione del Server DayZ](#installazione-del-server-dayz)
- [Directory dopo l'installazione](#directory-dopo-linstallazione)
- [Primo avvio con configurazione minima](#primo-avvio-con-configurazione-minima)
- [Verifica che il server sia in esecuzione](#verifica-che-il-server-sia-in-esecuzione)
- [Connettersi come giocatore](#connettersi-come-giocatore)
- [Problemi comuni al primo avvio](#problemi-comuni-al-primo-avvio)

---

## Prerequisiti

### Hardware

| Componente | Minimo | Raccomandato |
|------------|--------|--------------|
| CPU | 4 core, 2.4 GHz | 6+ core, 3.5 GHz |
| RAM | 8 GB | 16 GB |
| Disco | 20 GB SSD | 40 GB NVMe SSD |
| Rete | 10 Mbps upload | 50+ Mbps upload |
| OS | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

DayZ Server usa un singolo thread per la logica di gioco. La frequenza di clock conta piu del numero di core.

### Software

- **SteamCMD** -- il client Steam a riga di comando per installare server dedicati
- **Visual C++ Redistributable 2019** (Windows) -- richiesto da `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- solitamente gia presente
- Porte **2302-2305 UDP** inoltrate sul router/firewall

---

## Installazione di SteamCMD

### Windows

1. Scarica SteamCMD da https://developer.valvesoftware.com/wiki/SteamCMD
2. Estrai `steamcmd.exe` in una cartella permanente, ad esempio `C:\SteamCMD\`
3. Esegui `steamcmd.exe` una volta -- si aggiornera automaticamente

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## Installazione del Server DayZ

L'App ID di Steam per DayZ Server e **223350**. Puoi installarlo senza accedere a un account Steam che possiede DayZ.

### Installazione in una riga (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Installazione in una riga (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Script di aggiornamento

Crea uno script che puoi rieseguire ogni volta che esce una patch:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Aggiornamento completato.
pause
```

Il flag `validate` controlla ogni file per eventuali corruzioni. Per un'installazione nuova, aspettati un download di 2-3 GB.

---

## Directory dopo l'installazione

Dopo l'installazione, la directory principale del server appare cosi:

```
DayZServer/
  DayZServer_x64.exe        # L'eseguibile del server
  serverDZ.cfg               # Configurazione principale del server
  dayzsetting.xml            # Impostazioni di rendering/video (non rilevante per il dedicato)
  addons/                    # File PBO vanilla (ai.pbo, animals.pbo, ecc.)
  battleye/                  # Anti-cheat BattlEye (BEServer_x64.dll)
  dta/                       # Dati core del motore (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Chiavi di firma (dayz.bikey per il vanilla)
  logs/                      # Log del motore (connessione, contenuto, audio)
  mpmissions/                # Cartelle delle missioni
    dayzOffline.chernarusplus/   # Missione Chernarus
    dayzOffline.enoch/           # Missione Livonia (DLC)
    dayzOffline.sakhal/          # Missione Sakhal (DLC)
  profiles/                  # Output a runtime: log RPT, log degli script, DB giocatori
  ban.txt                    # Lista giocatori bannati (Steam64 ID)
  whitelist.txt              # Giocatori nella whitelist (Steam64 ID)
  steam_appid.txt            # Contiene "221100"
```

Punti chiave:
- **Devi modificare** `serverDZ.cfg` e i file dentro `mpmissions/`.
- **Non modificare mai** i file in `addons/` o `dta/` -- vengono sovrascritti ad ogni aggiornamento.
- I **PBO delle mod** vanno nella cartella principale del server o in una sottocartella (trattato in un capitolo successivo).
- **`profiles/`** viene creata al primo avvio e contiene i log degli script e i dump dei crash.

---

## Primo avvio con configurazione minima

### Passo 1: Modifica serverDZ.cfg

Apri `serverDZ.cfg` in un editor di testo. Per un primo test, usa la configurazione piu semplice possibile:

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

### Passo 2: Avvia il Server

Apri un Prompt dei comandi nella directory del server ed esegui:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Flag | Scopo |
|------|-------|
| `-config=serverDZ.cfg` | Percorso al file di configurazione |
| `-port=2302` | Porta principale del gioco (usa anche le porte 2303-2305) |
| `-profiles=profiles` | Cartella di output per log e dati giocatori |
| `-dologs` | Abilita il logging del server |
| `-adminlog` | Registra le azioni di amministrazione |
| `-netlog` | Registra gli eventi di rete |
| `-freezecheck` | Riavvio automatico in caso di freeze rilevato |

### Passo 3: Attendi l'inizializzazione

Il server impiega 30-90 secondi per avviarsi completamente. Osserva l'output della console. Quando vedi una riga come:

```
BattlEye Server: Initialized (v1.xxx)
```

...il server e pronto per le connessioni.

---

## Verifica che il server sia in esecuzione

### Metodo 1: Log degli script

Controlla `profiles/` per un file con nome simile a `script_YYYY-MM-DD_HH-MM-SS.log`. Aprilo e cerca:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Queste righe confermano che l'economia si e inizializzata e la missione si e caricata.

### Metodo 2: File RPT

Il file `.RPT` in `profiles/` mostra l'output a livello di motore. Cerca:

```
Dedicated host created.
BattlEye Server: Initialized
```

### Metodo 3: Browser Server di Steam

Apri Steam, vai su **Visualizza > Server di gioco > Preferiti**, clicca su **Aggiungi un server**, inserisci `127.0.0.1:2302` (o il tuo IP pubblico) e clicca su **Trova giochi a questo indirizzo**. Se il server appare, e in esecuzione e raggiungibile.

### Metodo 4: Porta di query

Usa uno strumento esterno come https://www.battlemetrics.com/ o il pacchetto npm `gamedig` per interrogare la porta 27016 (porta query di Steam = porta gioco + 24714).

---

## Connettersi come giocatore

### Dalla stessa macchina

1. Avvia DayZ (non DayZ Server -- il client di gioco normale)
2. Apri il **Browser dei Server**
3. Vai alla scheda **LAN** o **Preferiti**
4. Aggiungi `127.0.0.1:2302` ai preferiti
5. Clicca su **Connetti**

Se esegui client e server sulla stessa macchina, usa `DayZDiag_x64.exe` (il client diagnostico) invece del client retail. Avvia con:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### Da un'altra macchina

Usa l'**IP pubblico** del tuo server o l'**IP LAN** a seconda che il client sia sulla stessa rete. Le porte 2302-2305 UDP devono essere inoltrate.

---

## Problemi comuni al primo avvio

### Il server si avvia ma si chiude immediatamente

**Causa:** Visual C++ Redistributable mancante o errore di sintassi in `serverDZ.cfg`.

**Soluzione:** Installa VC++ Redist 2019 (x64). Controlla `serverDZ.cfg` per punti e virgola mancanti -- ogni riga di parametro deve terminare con `;`.

### "BattlEye initialization failed"

**Causa:** La cartella `battleye/` e mancante oppure l'antivirus sta bloccando `BEServer_x64.dll`.

**Soluzione:** Riconvalida i file del server tramite SteamCMD. Aggiungi un'eccezione antivirus per l'intera cartella del server.

### Il server funziona ma non appare nel browser

**Causa:** Porte non inoltrate o Windows Firewall che blocca l'eseguibile.

**Soluzione:**
1. Aggiungi una regola in ingresso in Windows Firewall per `DayZServer_x64.exe` (consenti tutto UDP)
2. Inoltra le porte **2302-2305 UDP** sul router
3. Verifica con un port checker esterno che la porta 2302 UDP sia aperta sul tuo IP pubblico

### "Version Mismatch" durante la connessione

**Causa:** Server e client sono su versioni diverse.

**Soluzione:** Aggiorna entrambi. Esegui il comando di aggiornamento SteamCMD per il server. Il client si aggiorna automaticamente tramite Steam.

### Nessun loot appare

**Causa:** Il file `init.c` e mancante oppure l'Hive non si e inizializzato.

**Soluzione:** Verifica che `mpmissions/dayzOffline.chernarusplus/init.c` esista e contenga `CreateHive()`. Controlla il log degli script per errori.

### Il server usa il 100% di un core della CPU

Questo e normale. DayZ Server usa un singolo thread. Non eseguire piu istanze del server sullo stesso core -- usa l'affinita del processore o macchine separate.

### I giocatori spawnano come corvi / Bloccati nel caricamento

**Causa:** Il template della missione in `serverDZ.cfg` non corrisponde a una cartella esistente in `mpmissions/`.

**Soluzione:** Controlla il valore del template. Deve corrispondere esattamente al nome di una cartella:

```cpp
template = "dayzOffline.chernarusplus";  // Deve corrispondere al nome della cartella in mpmissions/
```

---

**[Home](../README.md)** | **Successivo:** [Struttura delle Directory >>](02-directory-structure.md)
