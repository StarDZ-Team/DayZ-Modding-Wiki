# Chapter 9.11: Risoluzione Problemi del Server

[Home](../README.md) | [<< Precedente: Gestione delle Mod](10-mod-management.md) | [Successivo: Argomenti Avanzati >>](12-advanced.md)

---

> **Riepilogo:** Diagnostica e risolvi i problemi piu comuni del server DayZ -- errori di avvio, problemi di connessione, crash, loot e spawn dei veicoli, persistenza e prestazioni. Ogni soluzione qui proviene da pattern di errore reali attraverso migliaia di segnalazioni della community.

---

## Indice

- [Il server non si avvia](#il-server-non-si-avvia)
- [I giocatori non riescono a connettersi](#i-giocatori-non-riescono-a-connettersi)
- [Crash e puntatori nulli](#crash-e-puntatori-nulli)
- [Il loot non appare](#il-loot-non-appare)
- [I veicoli non appaiono](#i-veicoli-non-appaiono)
- [Problemi di persistenza](#problemi-di-persistenza)
- [Problemi di prestazioni](#problemi-di-prestazioni)
- [Lettura dei file di log](#lettura-dei-file-di-log)
- [Checklist diagnostica rapida](#checklist-diagnostica-rapida)

---

## Il server non si avvia

### File DLL mancanti

Se `DayZServer_x64.exe` va in crash immediatamente con un errore di DLL mancante, installa l'ultima versione di **Visual C++ Redistributable per Visual Studio 2019** (x64) dal sito ufficiale di Microsoft e riavvia.

### Porta gia in uso

Un'altra istanza di DayZ o un'altra applicazione sta occupando la porta 2302. Controlla con `netstat -ano | findstr 2302` (Windows) o `ss -tulnp | grep 2302` (Linux). Termina il processo in conflitto o cambia la tua porta con `-port=2402`.

### Cartella missione mancante

Il server si aspetta `mpmissions/<template>/` dove il nome della cartella corrisponde esattamente al valore `template` in **serverDZ.cfg**. Per Chernarus, e `mpmissions/dayzOffline.chernarusplus/` e deve contenere almeno **init.c**.

### serverDZ.cfg non valido

Un singolo punto e virgola mancante o un tipo di virgolette sbagliato impedisce l'avvio silenziosamente. Fai attenzione a:

- `;` mancante alla fine delle righe dei valori
- Virgolette smart invece di virgolette dritte
- Blocco `{};` mancante intorno alle voci delle classi

### File mod mancanti

Ogni percorso in `-mod=@CF;@VPPAdminTools;@MyMod` deve esistere relativo alla root del server e contenere una cartella **addons/** con file `.pbo`. Un singolo percorso errato impedisce l'avvio.

---

## I giocatori non riescono a connettersi

### Inoltro porte

DayZ richiede queste porte inoltrate e aperte nel tuo firewall:

| Porta | Protocollo | Scopo |
|-------|------------|-------|
| 2302 | UDP | Traffico di gioco |
| 2303 | UDP | Networking Steam |
| 2304 | UDP | Query Steam (interna) |
| 27016 | UDP | Query del browser server Steam |

Se hai cambiato la porta base con `-port=`, tutte le altre porte si spostano dello stesso offset.

### Firewall che blocca

Aggiungi **DayZServer_x64.exe** alle eccezioni del firewall del tuo OS. Su Windows: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. Su Linux, apri le porte con `ufw` o `iptables`.

### Mismatch delle mod

I client devono avere esattamente le stesse versioni delle mod del server. Se un giocatore vede "Mod mismatch", una delle due parti ha una versione obsoleta. Aggiorna entrambi quando una mod riceve un aggiornamento dal Workshop.

### File .bikey mancanti

Ogni file `.bikey` delle mod deve essere nella directory `keys/` del server. Senza di esso, BattlEye rifiuta i PBO firmati del client. Cerca dentro la cartella `keys/` o `key/` di ogni mod.

### Server pieno

Controlla `maxPlayers` in **serverDZ.cfg** (predefinito 60).

---

## Crash e puntatori nulli

### Accesso a puntatore nullo

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- l'errore di script piu comune. Una mod sta chiamando un metodo su un oggetto eliminato o non inizializzato. Questo e un bug della mod, non una configurazione errata del server. Segnalalo all'autore della mod con il log RPT completo.

### Trovare gli errori di script

Cerca nel log RPT `SCRIPT (E)`. Il nome della classe e del metodo nell'errore ti dice quale mod e responsabile. Posizioni RPT:

- **Server:** directory `$profiles/` (o root del server se non e impostato `-profiles=`)
- **Client:** `%localappdata%\DayZ\`

### Crash al riavvio

Se il server va in crash ad ogni riavvio, **storage_1/** potrebbe essere corrotto. Ferma il server, fai il backup di `storage_1/`, cancella `storage_1/data/events.bin` e riavvia. Se non funziona, cancella l'intera directory `storage_1/` (cancella tutta la persistenza).

### Crash dopo l'aggiornamento di una mod

Ritorna alla versione precedente della mod. Controlla il changelog del Workshop per modifiche incompatibili -- classi rinominate, configurazioni rimosse e formati RPC cambiati sono cause comuni.

---

## Il loot non appare

### types.xml non registrato

Gli oggetti definiti in **types.xml** non appariranno a meno che il file non sia registrato in **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Se usi un file types personalizzato (ad esempio **types_custom.xml**), aggiungi una voce `<file>` separata per esso.

### Tag category, usage o value errati

Ogni tag `<category>`, `<usage>` e `<value>` nel tuo types.xml deve corrispondere a un nome definito in **cfglimitsdefinition.xml**. Un errore di battitura come `usage name="Military"` (M maiuscola) quando la definizione dice `military` (minuscola) impedisce silenziosamente all'oggetto di apparire.

### Nominal impostato a zero

Se `nominal` e `0`, la CE non generera mai quell'oggetto. Questo e intenzionale per oggetti che dovrebbero esistere solo tramite crafting, eventi o piazzamento admin. Se vuoi che l'oggetto appaia naturalmente, imposta `nominal` ad almeno `1`.

### Posizioni dei gruppi mappa mancanti

Gli oggetti hanno bisogno di posizioni di spawn valide dentro gli edifici. Se un oggetto personalizzato non ha posizioni di gruppi mappa corrispondenti (definite in **mapgroupproto.xml**), la CE non ha dove piazzarlo. Assegna l'oggetto a categorie e usage che hanno gia posizioni valide sulla mappa.

---

## I veicoli non appaiono

I veicoli usano il sistema degli eventi, **non** types.xml.

### Configurazione in events.xml

Gli spawn dei veicoli sono definiti in **events.xml**:

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

### Posizioni di spawn mancanti

Gli eventi veicolo con `<position>fixed</position>` richiedono voci in **cfgeventspawns.xml**. Senza coordinate definite, l'evento non ha dove piazzare il veicolo.

### Evento disabilitato

Se `<active>0</active>`, l'evento e completamente disabilitato. Impostalo a `1`.

### Veicoli danneggiati che bloccano gli slot

Se `remove_damaged="0"`, i veicoli distrutti rimangono nel mondo per sempre e occupano gli slot di spawn. Imposta `remove_damaged="1"` in modo che la CE ripulisca i relitti e generi sostituti.

---

## Problemi di persistenza

### Le basi scompaiono

I pali con bandiera devono essere aggiornati prima che il loro timer scada. Il `FlagRefreshFrequency` predefinito e `432000` secondi (5 giorni). Se nessun giocatore interagisce con la bandiera entro quella finestra, la bandiera e tutti gli oggetti nel suo raggio vengono eliminati.

Controlla il valore in **globals.xml**:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Aumenta questo valore sui server con poca popolazione dove i giocatori accedono meno frequentemente.

### Gli oggetti svaniscono dopo il riavvio

Ogni oggetto ha un `lifetime` in **types.xml** (secondi). Quando scade senza interazione del giocatore, la CE lo rimuove. Riferimento: `3888000` = 45 giorni, `604800` = 7 giorni, `14400` = 4 ore. Gli oggetti dentro i contenitori ereditano il lifetime del contenitore.

### storage_1/ che cresce troppo

Se la tua directory `storage_1/` cresce oltre qualche centinaio di MB, la tua economia sta producendo troppi oggetti. Riduci i valori `nominal` nel tuo types.xml, specialmente per gli oggetti ad alto conteggio come cibo, abbigliamento e munizioni. Un file di persistenza gonfio causa tempi di riavvio piu lunghi.

### Dati dei giocatori persi

Gli inventari e le posizioni dei giocatori sono memorizzati in `storage_1/players/`. Se questa directory viene cancellata o corrotta, tutti i giocatori spawnano come nuovi. Fai il backup di `storage_1/` regolarmente.

---

## Problemi di prestazioni

### FPS del server che calano

I server DayZ puntano a 30+ FPS per un gameplay fluido. Cause comuni di FPS bassi del server:

- **Troppi zombie** -- riduci `ZombieMaxCount` in **globals.xml** (predefinito 800, prova 400-600)
- **Troppi animali** -- riduci `AnimalMaxCount` (predefinito 200, prova 100)
- **Loot eccessivo** -- abbassa i valori `nominal` nel tuo types.xml
- **Troppi oggetti nelle basi** -- basi grandi con centinaia di oggetti affaticano la persistenza
- **Mod con script pesanti** -- alcune mod eseguono logica costosa per-frame

### Desync

I giocatori che sperimentano rubber-banding, azioni ritardate o zombie invisibili sono sintomi di desync. Questo quasi sempre significa che gli FPS del server sono scesi sotto 15. Risolvi il problema prestazionale sottostante piuttosto che cercare un'impostazione specifica per il desync.

### Tempi di riavvio lunghi

Il tempo di riavvio e direttamente proporzionale alla dimensione di `storage_1/`. Se i riavvii richiedono piu di 2-3 minuti, hai troppi oggetti persistenti. Riduci i valori nominal del loot e imposta lifetime appropriati.

---

## Lettura dei file di log

### Posizione RPT del server

Il file RPT si trova in `$profiles/` (se avviato con `-profiles=`) o nella root del server. Pattern del nome file: `DayZServer_x64_<data>_<ora>.RPT`.

### Cosa cercare

| Termine di ricerca | Significato |
|--------------------|-------------|
| `SCRIPT (E)` | Errore di script -- una mod ha un bug |
| `[ERROR]` | Errore a livello di motore |
| `ErrorMessage` | Errore fatale che potrebbe causare lo spegnimento |
| `Cannot open` | File mancante (PBO, config, missione) |
| `Crash` | Crash a livello di applicazione |

### Log di BattlEye

I log di BattlEye sono nella directory `BattlEye/` all'interno della root del tuo server. Mostrano eventi di espulsione e ban. Se i giocatori segnalano di essere stati espulsi inaspettatamente, controlla qui per primo.

---

## Checklist diagnostica rapida

Quando qualcosa va storto, segui questa lista in ordine:

```
1. Controlla il RPT del server per righe SCRIPT (E) e [ERROR]
2. Verifica che ogni percorso -mod= esista e contenga addons/*.pbo
3. Verifica che tutti i file .bikey siano copiati in keys/
4. Controlla serverDZ.cfg per errori di sintassi (punti e virgola mancanti)
5. Controlla l'inoltro porte: 2302 UDP + 27016 UDP
6. Verifica che la cartella missione corrisponda al valore template in serverDZ.cfg
7. Controlla storage_1/ per corruzione (cancella events.bin se necessario)
8. Testa con zero mod prima, poi aggiungi le mod una alla volta
```

Il passo 8 e la tecnica piu potente. Se il server funziona vanilla ma si rompe con le mod, puoi isolare la mod problematica tramite ricerca binaria -- aggiungi meta delle tue mod, testa, poi restringi.

---

[Home](../README.md) | [<< Precedente: Gestione delle Mod](10-mod-management.md) | [Successivo: Argomenti Avanzati >>](12-advanced.md)
