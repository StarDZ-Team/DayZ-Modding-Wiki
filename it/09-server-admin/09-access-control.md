# Chapter 9.9: Controllo Accessi

[Home](../README.md) | [<< Precedente: Ottimizzazione delle Prestazioni](08-performance.md) | [Successivo: Gestione delle Mod >>](10-mod-management.md)

---

> **Riepilogo:** Configura chi puo connettersi al tuo server DayZ, come funzionano i ban, come abilitare l'amministrazione remota e come la verifica delle firme delle mod tiene fuori i contenuti non autorizzati. Questo capitolo copre ogni meccanismo di controllo degli accessi disponibile per un operatore di server.

---

## Indice

- [Accesso admin tramite serverDZ.cfg](#accesso-admin-tramite-serverdzcfg)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [Anti-cheat BattlEye](#anti-cheat-battleye)
- [RCON (Console Remota)](#rcon-console-remota)
- [Verifica delle firme](#verifica-delle-firme)
- [La directory keys/](#la-directory-keys)
- [Strumenti admin nel gioco](#strumenti-admin-nel-gioco)
- [Errori comuni](#errori-comuni)

---

## Accesso admin tramite serverDZ.cfg

Il parametro `passwordAdmin` in **serverDZ.cfg** imposta la password admin per il tuo server:

```cpp
passwordAdmin = "YourSecretPassword";
```

Usi questa password in due modi:

1. **Nel gioco** -- apri la chat e digita `#login YourSecretPassword` per ottenere i privilegi di admin per quella sessione.
2. **RCON** -- connettiti con un client BattlEye RCON usando questa password (vedi la sezione RCON qui sotto).

Mantieni la password admin lunga e unica. Chiunque la possieda ha il pieno controllo sul server in esecuzione.

---

## ban.txt

Il file **ban.txt** si trova nella directory del profilo del tuo server (il percorso che imposti con `-profiles=`). Contiene un SteamID64 per riga:

```
76561198012345678
76561198087654321
```

- Ogni riga e un SteamID64 a 17 cifre senza altro -- niente nomi, niente commenti, niente password.
- Ai giocatori il cui SteamID appare in questo file viene rifiutata la connessione al momento dell'accesso.
- Puoi modificare il file mentre il server e in esecuzione; le modifiche hanno effetto al prossimo tentativo di connessione.

---

## whitelist.txt

Il file **whitelist.txt** si trova nella stessa directory del profilo. Quando abiliti la whitelist, solo gli SteamID elencati in questo file possono connettersi:

```
76561198012345678
76561198087654321
```

Il formato e identico a **ban.txt** -- un SteamID64 per riga, nient'altro.

La whitelist e utile per community private, server di test o eventi dove hai bisogno di una lista controllata di giocatori.

---

## Anti-cheat BattlEye

BattlEye e il sistema anti-cheat integrato in DayZ. I suoi file si trovano nella cartella `BattlEye/` dentro la directory del tuo server:

| File | Scopo |
|------|-------|
| **BEServer_x64.dll** | Il binario del motore anti-cheat BattlEye |
| **beserver_x64.cfg** | File di configurazione (porta RCON, password RCON) |
| **bans.txt** | Ban specifici di BattlEye (basati su GUID, non su SteamID) |

BattlEye e abilitato per impostazione predefinita. Avvii il server con `DayZServer_x64.exe` e BattlEye si carica automaticamente. Per disabilitarlo esplicitamente (non raccomandato per la produzione), usa il parametro di avvio `-noBE`.

Il file **bans.txt** nella cartella `BattlEye/` usa i GUID di BattlEye, che sono diversi dagli SteamID64. I ban emessi tramite RCON o comandi BattlEye scrivono automaticamente in questo file.

---

## RCON (Console Remota)

BattlEye RCON ti permette di amministrare il server da remoto senza essere nel gioco. Configuralo in `BattlEye/beserver_x64.cfg`:

```
RConPassword yourpassword
RConPort 2306
```

La porta RCON predefinita e la tua porta di gioco piu 4. Se il tuo server gira sulla porta `2302`, RCON usa per impostazione predefinita la `2306`.

### Comandi RCON disponibili

| Comando | Effetto |
|---------|--------|
| `kick <giocatore> [motivo]` | Espelli un giocatore dal server |
| `ban <giocatore> [minuti] [motivo]` | Banna un giocatore (scrive nel bans.txt di BattlEye) |
| `say -1 <messaggio>` | Trasmetti un messaggio a tutti i giocatori |
| `#shutdown` | Spegnimento controllato del server |
| `#lock` | Blocca il server (nessuna nuova connessione) |
| `#unlock` | Sblocca il server |
| `players` | Elenca i giocatori connessi |

Ti connetti a RCON usando un client BattlEye RCON (esistono diversi strumenti gratuiti). La connessione richiede l'IP, la porta RCON e la password da **beserver_x64.cfg**.

---

## Verifica delle firme

Il parametro `verifySignatures` in **serverDZ.cfg** controlla se il server verifica le firme delle mod:

```cpp
verifySignatures = 2;
```

| Valore | Comportamento |
|--------|---------------|
| `0` | Disabilitata -- chiunque puo unirsi con qualsiasi mod, nessun controllo delle firme |
| `2` | Verifica completa -- i client devono avere firme valide per tutte le mod caricate (predefinito) |

Usa sempre `verifySignatures = 2` sui server di produzione. Impostarlo a `0` permette ai giocatori di unirsi con mod modificate o non firmate, il che rappresenta un serio rischio di sicurezza.

---

## La directory keys/

La directory `keys/` nella root del tuo server contiene file **.bikey**. Ogni `.bikey` corrisponde a una mod e dice al server "le firme di questa mod sono affidabili."

Quando `verifySignatures = 2`:

1. Il server controlla ogni mod che il client connesso ha caricato.
2. Per ogni mod, il server cerca un `.bikey` corrispondente in `keys/`.
3. Se una chiave corrispondente manca, il giocatore viene espulso.

Ogni mod che installi sul server include un file `.bikey` (di solito nella sottocartella `Keys/` o `Key/` della mod). Copi quel file nella directory `keys/` del tuo server.

```
DayZServer/
├── keys/
│   ├── dayz.bikey              ← vanilla (sempre presente)
│   ├── MyMod.bikey             ← copiato da @MyMod/Keys/
│   └── AnotherMod.bikey        ← copiato da @AnotherMod/Keys/
```

Se aggiungi una nuova mod e dimentichi di copiare il suo `.bikey`, ogni giocatore che usa quella mod viene espulso alla connessione.

---

## Strumenti admin nel gioco

Una volta effettuato l'accesso con `#login <password>` nella chat, ottieni l'accesso agli strumenti admin:

- **Lista giocatori** -- visualizza tutti i giocatori connessi con i loro SteamID.
- **Espelli/Banna** -- rimuovi o banna i giocatori direttamente dalla lista.
- **Teletrasporto** -- usa la mappa admin per teletrasportarti in qualsiasi posizione.
- **Log admin** -- log lato server delle azioni dei giocatori (uccisioni, connessioni, disconnessioni) scritto nei file `*.ADM` nella directory del profilo.
- **Telecamera libera** -- staccati dal tuo personaggio e vola per la mappa.

Questi strumenti sono integrati nel gioco vanilla. Le mod di terze parti (come Community Online Tools) estendono significativamente le capacita di amministrazione.

---

## Errori comuni

Questi sono i problemi che gli operatori di server incontrano piu spesso:

| Errore | Sintomo | Soluzione |
|--------|---------|-----------|
| `.bikey` mancante in `keys/` | I giocatori vengono espulsi all'accesso con un errore di firma | Copia il file `.bikey` della mod nella directory `keys/` del tuo server |
| Inserire nomi o password in **ban.txt** | I ban non funzionano; errori casuali | Usa solo valori SteamID64, uno per riga |
| Conflitto sulla porta RCON | Il client RCON non riesce a connettersi | Assicurati che la porta RCON non sia usata da un altro servizio; controlla le regole del firewall |
| `verifySignatures = 0` in produzione | Chiunque puo unirsi con mod manomesse | Impostalo a `2` su qualsiasi server pubblico |
| Dimenticare di aprire la porta RCON nel firewall | Il client RCON va in timeout | Apri la porta UDP RCON (predefinita 2306) nel tuo firewall |
| Modificare **bans.txt** in `BattlEye/` con SteamID | I ban non funzionano | **bans.txt** di BattlEye usa i GUID, non gli SteamID; usa **ban.txt** nella directory del profilo per i ban tramite SteamID |

---

[Home](../README.md) | [<< Precedente: Ottimizzazione delle Prestazioni](08-performance.md) | [Successivo: Gestione delle Mod >>](10-mod-management.md)
