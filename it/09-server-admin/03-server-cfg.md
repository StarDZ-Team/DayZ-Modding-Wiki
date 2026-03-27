# Chapter 9.3: Riferimento Completo di serverDZ.cfg

[Home](../README.md) | [<< Precedente: Struttura delle Directory](02-directory-structure.md) | **Riferimento serverDZ.cfg** | [Successivo: Economia del Loot in Dettaglio >>](04-loot-economy.md)

---

> **Riepilogo:** Ogni parametro di `serverDZ.cfg` documentato con il suo scopo, valori validi e comportamento predefinito. Questo file controlla l'identita del server, le impostazioni di rete, le regole di gameplay, l'accelerazione del tempo e la selezione della missione.

---

## Indice

- [Formato del file](#formato-del-file)
- [Identita del server](#identita-del-server)
- [Rete e sicurezza](#rete-e-sicurezza)
- [Regole di gameplay](#regole-di-gameplay)
- [Tempo e meteo](#tempo-e-meteo)
- [Prestazioni e coda di login](#prestazioni-e-coda-di-login)
- [Persistenza e istanza](#persistenza-e-istanza)
- [Selezione della missione](#selezione-della-missione)
- [File di esempio completo](#file-di-esempio-completo)
- [Parametri di avvio che sovrascrivono la configurazione](#parametri-di-avvio-che-sovrascrivono-la-configurazione)

---

## Formato del file

`serverDZ.cfg` usa il formato di configurazione di Bohemia (simile al C). Regole:

- Ogni assegnazione di parametro termina con un **punto e virgola** `;`
- Le stringhe sono racchiuse tra **virgolette doppie** `""`
- I commenti usano `//` per singola riga
- Il blocco `class Missions` usa parentesi graffe `{}` e termina con `};`
- Il file deve essere codificato in UTF-8 o ANSI -- senza BOM

Un punto e virgola mancante fara fallire silenziosamente il server o ignorare i parametri successivi.

---

## Identita del server

```cpp
hostname = "My DayZ Server";         // Nome del server mostrato nel browser
password = "";                       // Password per connettersi (vuota = pubblico)
passwordAdmin = "";                  // Password per il login admin tramite console di gioco
description = "";                    // Descrizione mostrata nei dettagli del browser dei server
```

| Parametro | Tipo | Predefinito | Note |
|-----------|------|-------------|------|
| `hostname` | stringa | `""` | Visualizzato nel browser dei server. Massimo ~100 caratteri. |
| `password` | stringa | `""` | Lascia vuoto per un server pubblico. I giocatori devono inserirla per unirsi. |
| `passwordAdmin` | stringa | `""` | Usata con il comando `#login` nel gioco. **Impostala su ogni server.** |
| `description` | stringa | `""` | Le descrizioni multi-riga non sono supportate. Mantienila breve. |

---

## Rete e sicurezza

```cpp
maxPlayers = 60;                     // Slot massimi per i giocatori
verifySignatures = 2;                // Verifica delle firme PBO (solo 2 e supportato)
forceSameBuild = 1;                  // Richiedi versione client/server corrispondente
enableWhitelist = 0;                 // Abilita/disabilita whitelist
disableVoN = 0;                      // Disabilita la voce sulla rete
vonCodecQuality = 20;               // Qualita audio VoN (0-30)
guaranteedUpdates = 1;               // Protocollo di rete (usa sempre 1)
```

| Parametro | Tipo | Valori validi | Predefinito | Note |
|-----------|------|---------------|-------------|------|
| `maxPlayers` | int | 1-60 | 60 | Influisce sull'uso della RAM. Ogni giocatore aggiunge ~50-100 MB. |
| `verifySignatures` | int | 2 | 2 | Solo il valore 2 e supportato. Verifica i file PBO rispetto alle chiavi `.bisign`. |
| `forceSameBuild` | int | 0, 1 | 1 | Quando e 1, i client devono corrispondere alla versione esatta dell'eseguibile del server. Mantieni sempre a 1. |
| `enableWhitelist` | int | 0, 1 | 0 | Quando e 1, solo gli Steam64 ID elencati in `whitelist.txt` possono connettersi. |
| `disableVoN` | int | 0, 1 | 0 | Imposta a 1 per disabilitare completamente la chat vocale nel gioco. |
| `vonCodecQuality` | int | 0-30 | 20 | Valori piu alti significano migliore qualita vocale ma piu banda. 20 e un buon equilibrio. |
| `guaranteedUpdates` | int | 1 | 1 | Impostazione del protocollo di rete. Usa sempre 1. |

### Shard ID

```cpp
shardId = "123abc";                  // Sei caratteri alfanumerici per shard privati
```

| Parametro | Tipo | Predefinito | Note |
|-----------|------|-------------|------|
| `shardId` | stringa | `""` | Usato per server con hive privato. I giocatori su server con lo stesso `shardId` condividono i dati del personaggio. Lascia vuoto per un hive pubblico. |

---

## Regole di gameplay

```cpp
disable3rdPerson = 0;               // Disabilita la telecamera in terza persona
disableCrosshair = 0;               // Disabilita il mirino
disablePersonalLight = 1;           // Disabilita la luce ambientale del giocatore
lightingConfig = 0;                 // Luminosita notturna (0 = piu chiaro, 1 = piu scuro)
```

| Parametro | Tipo | Valori validi | Predefinito | Note |
|-----------|------|---------------|-------------|------|
| `disable3rdPerson` | int | 0, 1 | 0 | Imposta a 1 per server solo in prima persona. Questa e l'impostazione "hardcore" piu comune. |
| `disableCrosshair` | int | 0, 1 | 0 | Imposta a 1 per rimuovere il mirino. Spesso abbinato a `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | La "luce personale" e un bagliore sottile intorno al giocatore di notte. La maggior parte dei server la disabilita (valore 1) per realismo. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = notti piu luminose (chiaro di luna visibile). 1 = notti completamente buie (necessaria torcia/NVG). |

---

## Tempo e meteo

```cpp
serverTime = "SystemTime";                 // Orario iniziale
serverTimeAcceleration = 12;               // Moltiplicatore velocita del tempo (0-24)
serverNightTimeAcceleration = 1;           // Moltiplicatore velocita del tempo notturno (0.1-64)
serverTimePersistent = 0;                  // Salva l'orario tra i riavvii
```

| Parametro | Tipo | Valori validi | Predefinito | Note |
|-----------|------|---------------|-------------|------|
| `serverTime` | stringa | `"SystemTime"` o `"AAAA/MM/GG/HH/MM"` | `"SystemTime"` | `"SystemTime"` usa l'orologio locale della macchina. Imposta un orario fisso come `"2024/9/15/12/0"` per un server perennemente diurno. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Moltiplicatore per il tempo di gioco. A 12, un ciclo completo di 24 ore dura 2 ore reali. A 1, il tempo e in tempo reale. A 24, un giorno intero passa in 1 ora. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Moltiplicato per `serverTimeAcceleration`. Con valore 4 e accelerazione 12, la notte passa a velocita 48x (notti molto brevi). |
| `serverTimePersistent` | int | 0, 1 | 0 | Quando e 1, il server salva il suo orologio di gioco su disco e lo riprende dopo il riavvio. Quando e 0, l'orario si resetta a `serverTime` ad ogni riavvio. |

### Configurazioni comuni del tempo

**Sempre giorno:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Ciclo giorno/notte veloce (giorni di 2 ore, notti brevi):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Giorno/notte in tempo reale:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Prestazioni e coda di login

```cpp
loginQueueConcurrentPlayers = 5;     // Giocatori processati contemporaneamente durante il login
loginQueueMaxPlayers = 500;          // Dimensione massima della coda di login
```

| Parametro | Tipo | Predefinito | Note |
|-----------|------|-------------|------|
| `loginQueueConcurrentPlayers` | int | 5 | Quanti giocatori possono caricare simultaneamente. Valori piu bassi riducono i picchi di carico del server dopo un riavvio. Aumenta a 10-15 se il tuo hardware e potente e i giocatori si lamentano dei tempi di coda. |
| `loginQueueMaxPlayers` | int | 500 | Se questo numero di giocatori sta gia facendo la coda, le nuove connessioni vengono rifiutate. 500 va bene per la maggior parte dei server. |

---

## Persistenza e istanza

```cpp
instanceId = 1;                      // Identificatore dell'istanza del server
storageAutoFix = 1;                  // Ripara automaticamente i file di persistenza corrotti
```

| Parametro | Tipo | Predefinito | Note |
|-----------|------|-------------|------|
| `instanceId` | int | 1 | Identifica l'istanza del server. I dati di persistenza sono memorizzati in `storage_<instanceId>/`. Se esegui piu server sulla stessa macchina, dai a ciascuno un `instanceId` diverso. |
| `storageAutoFix` | int | 1 | Quando e 1, il server controlla i file di persistenza all'avvio e sostituisce quelli corrotti con file vuoti. Lascia sempre a 1. |

---

## Selezione della missione

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

Il valore `template` deve corrispondere esattamente al nome di una cartella dentro `mpmissions/`. Missioni vanilla disponibili:

| Template | Mappa | DLC richiesto |
|----------|-------|:---:|
| `dayzOffline.chernarusplus` | Chernarus | No |
| `dayzOffline.enoch` | Livonia | Si |
| `dayzOffline.sakhal` | Sakhal | Si |

Le missioni personalizzate (ad esempio da mod o mappe della community) usano il proprio nome di template. La cartella deve esistere in `mpmissions/`.

---

## File di esempio completo

Questo e il file `serverDZ.cfg` predefinito completo con tutti i parametri:

```cpp
hostname = "EXAMPLE NAME";              // Nome del server
password = "";                          // Password per connettersi al server
passwordAdmin = "";                     // Password per diventare admin del server

description = "";                       // Descrizione nel browser dei server

enableWhitelist = 0;                    // Abilita/disabilita whitelist (valore 0-1)

maxPlayers = 60;                        // Numero massimo di giocatori

verifySignatures = 2;                   // Verifica i .pbo rispetto ai file .bisign (solo 2 e supportato)
forceSameBuild = 1;                     // Richiedi versione client/server corrispondente (valore 0-1)

disableVoN = 0;                         // Abilita/disabilita la voce sulla rete (valore 0-1)
vonCodecQuality = 20;                   // Qualita del codec della voce sulla rete (valori 0-30)

shardId = "123abc";                     // Sei caratteri alfanumerici per shard privato

disable3rdPerson = 0;                   // Attiva/disattiva la visuale in terza persona (valore 0-1)
disableCrosshair = 0;                   // Attiva/disattiva il mirino (valore 0-1)

disablePersonalLight = 1;              // Disabilita la luce personale per tutti i client
lightingConfig = 0;                     // 0 per notti piu luminose, 1 per notti piu scure

serverTime = "SystemTime";             // Orario iniziale nel gioco ("SystemTime" o "AAAA/MM/GG/HH/MM")
serverTimeAcceleration = 12;           // Moltiplicatore velocita del tempo (0-24)
serverNightTimeAcceleration = 1;       // Moltiplicatore velocita del tempo notturno (0.1-64), anche moltiplicato per serverTimeAcceleration
serverTimePersistent = 0;              // Salva l'orario tra i riavvii (valore 0-1)

guaranteedUpdates = 1;                 // Protocollo di rete (usa sempre 1)

loginQueueConcurrentPlayers = 5;       // Giocatori processati simultaneamente durante il login
loginQueueMaxPlayers = 500;            // Dimensione massima della coda di login

instanceId = 1;                        // ID dell'istanza del server (influisce sul nome della cartella di storage)

storageAutoFix = 1;                    // Riparazione automatica della persistenza corrotta (valore 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Parametri di avvio che sovrascrivono la configurazione

Alcune impostazioni possono essere sovrascritte tramite parametri da riga di comando quando si avvia `DayZServer_x64.exe`:

| Parametro | Sovrascrive | Esempio |
|-----------|-------------|---------|
| `-config=` | Percorso del file di configurazione | `-config=serverDZ.cfg` |
| `-port=` | Porta di gioco | `-port=2302` |
| `-profiles=` | Directory di output dei profili | `-profiles=profiles` |
| `-mod=` | Mod lato client (separate da punto e virgola) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Mod solo server | `-servermod=@MyServerMod` |
| `-BEpath=` | Percorso di BattlEye | `-BEpath=battleye` |
| `-dologs` | Abilita il logging | -- |
| `-adminlog` | Abilita il log di amministrazione | -- |
| `-netlog` | Abilita il log di rete | -- |
| `-freezecheck` | Riavvio automatico in caso di freeze | -- |
| `-cpuCount=` | Core CPU da usare | `-cpuCount=4` |
| `-noFilePatching` | Disabilita il file patching | -- |

### Esempio completo di avvio

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Le mod vengono caricate nell'ordine specificato in `-mod=`. L'ordine delle dipendenze conta: se la Mod B richiede la Mod A, elenca la Mod A per prima.

---

**Precedente:** [Struttura delle Directory](02-directory-structure.md) | [Home](../README.md) | **Successivo:** [Economia del Loot in Dettaglio >>](04-loot-economy.md)
