# Chapter 9.8: Ottimizzazione delle Prestazioni

[Home](../README.md) | [<< Precedente: Persistenza](07-persistence.md) | [Successivo: Controllo Accessi >>](09-access-control.md)

---

> **Riepilogo:** Le prestazioni del server in DayZ dipendono da tre fattori: conteggio degli oggetti, eventi dinamici e carico di mod/giocatori. Questo capitolo copre le impostazioni specifiche che contano, come diagnosticare i problemi e quale hardware aiuta davvero -- tutto basato su dati reali della community da oltre 400 segnalazioni su Discord di cali di FPS, lag e desync.

---

## Indice

- [Cosa influisce sulle prestazioni del server](#cosa-influisce-sulle-prestazioni-del-server)
- [Regolazione di globals.xml](#regolazione-di-globalsxml)
- [Regolazione dell'economia per le prestazioni](#regolazione-delleconomia-per-le-prestazioni)
- [Logging di cfgeconomycore.xml](#logging-di-cfgeconomycorexml)
- [Impostazioni prestazionali di serverDZ.cfg](#impostazioni-prestazionali-di-serverdzcfg)
- [Impatto delle mod sulle prestazioni](#impatto-delle-mod-sulle-prestazioni)
- [Raccomandazioni hardware](#raccomandazioni-hardware)
- [Monitoraggio della salute del server](#monitoraggio-della-salute-del-server)
- [Errori comuni sulle prestazioni](#errori-comuni-sulle-prestazioni)

---

## Cosa influisce sulle prestazioni del server

Dai dati della community (400+ menzioni su Discord di FPS/prestazioni/lag/desync), i tre maggiori fattori prestazionali sono:

1. **Conteggio degli oggetti** -- valori `nominal` alti in `types.xml` significano che la Central Economy traccia ed elabora piu oggetti ad ogni ciclo. Questa e costantemente la causa numero uno del lag lato server.
2. **Spawn di eventi** -- troppi eventi dinamici attivi (veicoli, animali, relitti di elicotteri) in `events.xml` consumano cicli di spawn/pulizia e slot di entita.
3. **Conteggio giocatori + conteggio mod** -- ogni giocatore connesso genera aggiornamenti delle entita, e ogni mod aggiunge classi di script che il motore deve compilare ed eseguire ad ogni tick.

Il game loop del server funziona a un tick rate fisso di 30 FPS. Quando il server non riesce a mantenere 30 FPS, i giocatori sperimentano desync -- rubber-banding, ritardi nel raccogliere oggetti e fallimenti nella registrazione dei colpi. Sotto i 15 FPS del server, il gioco diventa ingiocabile.

---

## Regolazione di globals.xml

Questi sono i valori predefiniti vanilla per i parametri che influiscono direttamente sulle prestazioni:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### Cosa controlla ogni valore

| Parametro | Predefinito | Effetto sulle prestazioni |
|-----------|-------------|---------------------------|
| `ZombieMaxCount` | 1000 | Limite per il totale degli infetti sul server. Ogni zombie esegue il pathfinding dell'IA. Ridurre a 500-700 migliora notevolmente gli FPS del server su server popolati. |
| `AnimalMaxCount` | 200 | Limite per gli animali. Gli animali hanno un'IA piu semplice degli zombie ma consumano comunque tempo di tick. Riduci a 100 se noti problemi di FPS. |
| `ZoneSpawnDist` | 300 | Distanza in metri alla quale le zone zombie si attivano intorno ai giocatori. Ridurre a 200 significa meno zone attive simultaneamente. |
| `SpawnInitial` | 1200 | Numero di oggetti che la CE genera al primo avvio. Valori piu alti significano un caricamento iniziale piu lungo. Non influisce sulle prestazioni a regime. |
| `CleanupLifetimeDefault` | 45 | Tempo di pulizia predefinito in secondi per gli oggetti senza un lifetime specifico. Valori piu bassi significano cicli di pulizia piu veloci ma elaborazione CE piu frequente. |

**Profilo prestazionale raccomandato** (per server che faticano sopra i 40 giocatori):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Regolazione dell'economia per le prestazioni

La Central Economy esegue un ciclo continuo controllando ogni tipo di oggetto rispetto ai suoi target `nominal`/`min`. Piu tipi di oggetto con nominal piu alti significano piu lavoro per ciclo.

### Riduci i valori nominal

Ogni oggetto in `types.xml` con `nominal > 0` e tracciato dalla CE. Se hai 2000 tipi di oggetto con un nominal medio di 20, la CE sta gestendo 40.000 oggetti. Riduci i nominal in modo generalizzato per tagliare questo numero:

- Oggetti civili comuni: riduci da 15-40 a 10-25
- Armi: mantienili bassi (il vanilla e gia 2-10)
- Varianti di colore dell'abbigliamento: considera di disabilitare le varianti di colore che non ti servono (`nominal=0`)

### Riduci gli eventi dinamici

In `events.xml`, ogni evento attivo genera e monitora gruppi di entita. Abbassa il `nominal` sugli eventi veicoli e animali, o imposta `<active>0</active>` sugli eventi di cui non hai bisogno.

### Usa la modalita inattiva

Quando nessun giocatore e connesso, la CE puo fermarsi completamente:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` significa che il server entra in modalita inattiva 60 secondi dopo che l'ultimo giocatore si disconnette. `IdleModeStartup=1` significa che il server si avvia in modalita inattiva e attiva la CE solo quando il primo giocatore si connette. Questo impedisce al server di elaborare cicli di spawn mentre e vuoto.

### Regola la frequenza di respawn

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Questi controllano quanti oggetti e tipi di oggetto la CE elabora per ciclo. Valori piu bassi riducono il carico CE per tick ma rallentano il respawn del loot. I valori predefiniti vanilla sopra sono gia conservativi.

---

## Logging di cfgeconomycore.xml

Abilita i log diagnostici della CE temporaneamente per misurare i tempi dei cicli e identificare i colli di bottiglia. Nel tuo `cfgeconomycore.xml`:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Per diagnosticare le prestazioni, imposta `log_ce_statistics` su `"true"`. Questo produce i tempi dei cicli CE nel log RPT del server. Cerca le righe che mostrano quanto dura ogni ciclo CE -- se i cicli superano i 1000ms, l'economia e sovraccaricata.

Imposta `log_ce_lootspawn` e `log_ce_lootcleanup` su `"true"` per vedere quali tipi di oggetto appaiono e vengono ripuliti piu frequentemente. Questi sono i tuoi candidati per la riduzione del nominal.

**Disattiva il logging dopo la diagnosi.** Le scritture dei log stesse consumano I/O e possono peggiorare le prestazioni se lasciate abilitate permanentemente.

---

## Impostazioni prestazionali di serverDZ.cfg

Il file di configurazione principale del server ha opzioni limitate relative alle prestazioni:

| Impostazione | Effetto |
|--------------|--------|
| `maxPlayers` | Abbassa questo valore se il server fatica. Ogni giocatore genera traffico di rete e aggiornamenti delle entita. Passare da 60 a 40 giocatori puo recuperare 5-10 FPS del server. |
| `instanceId` | Determina il percorso di `storage_1/`. Non e un'impostazione prestazionale, ma se il tuo storage e su un disco lento, influisce sull'I/O della persistenza. |

**Cosa non puoi cambiare:** il tick rate del server e fisso a 30 FPS. Non c'e un'impostazione per aumentarlo o diminuirlo. Se il server non riesce a mantenere 30 FPS, semplicemente gira piu lentamente.

---

## Impatto delle mod sulle prestazioni

Ogni mod aggiunge classi di script che il motore compila all'avvio ed esegue ad ogni tick. L'impatto varia drasticamente in base alla qualita della mod:

- **Mod solo contenuto** (armi, abbigliamento, edifici) aggiungono tipi di oggetto ma overhead di script minimo. Il loro costo e nel tracciamento CE, non nell'elaborazione dei tick.
- **Mod pesanti di script** con loop `OnUpdate()` o `OnTick()` eseguono codice ad ogni frame del server. Loop mal ottimizzati in queste mod sono la causa piu comune di lag legato alle mod.
- **Mod trader/economia** che mantengono grandi inventari aggiungono oggetti persistenti che il motore deve tracciare.

### Linee guida

- Aggiungi le mod incrementalmente. Testa gli FPS del server dopo ogni aggiunta, non dopo averne aggiunte 10 contemporaneamente.
- Monitora gli FPS del server con strumenti admin o output del log RPT dopo aver aggiunto nuove mod.
- Se una mod causa problemi, controlla il suo codice sorgente per operazioni costose per-frame.

Consenso della community: "Gli oggetti (types) e lo spawn degli eventi sono i piu impegnativi -- le mod che aggiungono migliaia di voci in types.xml fanno piu danno delle mod che aggiungono script complessi."

---

## Raccomandazioni hardware

La logica di gioco del server DayZ e **single-threaded**. CPU multi-core aiutano con l'overhead del sistema operativo e l'I/O di rete, ma il game loop principale gira su un core.

| Componente | Raccomandazione | Perche |
|------------|-----------------|--------|
| **CPU** | Le prestazioni single-thread piu alte che puoi ottenere. AMD 5600X o superiore. | Il game loop e single-threaded. La frequenza di clock e l'IPC contano piu del numero di core. |
| **RAM** | 8 GB minimo, 12-16 GB per server pesantemente moddati | Le mod e le mappe grandi consumano memoria. Esaurirla causa stuttering. |
| **Storage** | SSD obbligatorio | L'I/O di persistenza di `storage_1/` e costante. Un HDD causa hitching durante i cicli di salvataggio. |
| **Rete** | 100 Mbps+ con bassa latenza | La banda conta meno della stabilita del ping per la prevenzione del desync. |

Consiglio della community: "OVH offre un buon rapporto qualita-prezzo -- circa 60 USD per una macchina dedicata 5600X che gestisce server moddati da 60 slot."

Evita l'hosting condiviso/VPS per server popolati. Il problema del vicino rumoroso sull'hardware condiviso causa cali di FPS imprevedibili che sono impossibili da diagnosticare dalla tua parte.

---

## Monitoraggio della salute del server

### FPS del server

Controlla il log RPT per le righe contenenti gli FPS del server. Un server sano mantiene costantemente 30 FPS. Soglie di allarme:

| FPS del server | Stato |
|----------------|-------|
| 25-30 | Normale. Fluttuazioni minori sono previste durante combattimenti intensi o riavvii. |
| 15-25 | Degradato. I giocatori notano desync nelle interazioni con gli oggetti e nel combattimento. |
| Sotto 15 | Critico. Rubber-banding, azioni fallite, registrazione dei colpi compromessa. |

### Avvisi sui cicli CE

Con `log_ce_statistics` abilitato, osserva i tempi dei cicli CE. Il normale e sotto i 500ms. Se i cicli superano regolarmente i 1000ms, la tua economia e troppo pesante.

### Crescita dello storage

Monitora la dimensione di `storage_1/`. Una crescita incontrollata indica un'inflazione della persistenza -- troppi oggetti piazzati, tende o scorte che si accumulano. Wipe regolari del server o la riduzione di `FlagRefreshMaxDuration` in `globals.xml` aiutano a controllare questo.

### Segnalazioni dei giocatori

Le segnalazioni di desync dai giocatori sono il tuo indicatore in tempo reale piu affidabile. Se piu giocatori segnalano rubber-banding simultaneamente, gli FPS del server sono scesi sotto 15.

---

## Errori comuni sulle prestazioni

### Valori nominal troppo alti

Impostare ogni oggetto a `nominal=50` perche "piu loot e divertente" crea decine di migliaia di oggetti tracciati. La CE spende il suo intero ciclo a gestire gli oggetti invece di far girare il gioco. Parti con i nominal vanilla e aumenta selettivamente.

### Troppi eventi veicolo

I veicoli sono entita costose con simulazione fisica, tracciamento degli accessori e persistenza. Il vanilla genera circa 50 veicoli in totale. I server che eseguono 150+ veicoli vedono una perdita significativa di FPS.

### Eseguire 30+ mod senza testare

Ogni mod va bene in isolamento. L'effetto composto di 30+ mod -- migliaia di tipi extra, dozzine di script per-frame e aumento della pressione sulla memoria -- puo far calare gli FPS del server del 50% o piu. Aggiungi le mod a gruppi di 3-5 e testa dopo ogni gruppo.

### Non riavviare mai il server

Alcune mod hanno memory leak che si accumulano nel tempo. Programma riavvii automatici ogni 4-6 ore. La maggior parte dei pannelli di hosting dei server lo supporta. Anche le mod ben scritte beneficiano di riavvii periodici perche la frammentazione della memoria del motore stesso aumenta durante le sessioni lunghe.

### Ignorare l'inflazione dello storage

Una cartella `storage_1/` che cresce fino a diversi gigabyte rallenta ogni ciclo di persistenza. Fai il wipe o riducila periodicamente, specialmente se consenti la costruzione di basi senza limiti di degrado.

### Logging lasciato abilitato

Il logging diagnostico della CE, il logging di debug degli script e il logging degli strumenti admin scrivono tutti su disco ad ogni tick. Abilitali per la diagnosi, poi disattivali. Il logging verbose persistente su un server attivo puo costare 1-2 FPS da solo.

---

[Home](../README.md) | [<< Precedente: Persistenza](07-persistence.md) | [Successivo: Controllo Accessi >>](09-access-control.md)
