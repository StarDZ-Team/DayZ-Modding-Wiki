# Chapter 9.10: Gestione delle Mod

[Home](../README.md) | [<< Precedente: Controllo Accessi](09-access-control.md) | [Successivo: Risoluzione Problemi >>](11-troubleshooting.md)

---

> **Riepilogo:** Installa, configura e mantieni le mod di terze parti su un server dedicato DayZ. Copre i parametri di avvio, i download dal Workshop, le chiavi di firma, l'ordine di caricamento, le mod solo server vs quelle richieste dal client, gli aggiornamenti e gli errori piu comuni che causano crash o espulsioni dei giocatori.

---

## Indice

- [Come si caricano le mod](#come-si-caricano-le-mod)
- [Formato dei parametri di avvio](#formato-dei-parametri-di-avvio)
- [Installazione delle mod dal Workshop](#installazione-delle-mod-dal-workshop)
- [Chiavi delle mod (.bikey)](#chiavi-delle-mod-bikey)
- [Ordine di caricamento e dipendenze](#ordine-di-caricamento-e-dipendenze)
- [Mod solo server vs richieste dal client](#mod-solo-server-vs-richieste-dal-client)
- [Aggiornamento delle mod](#aggiornamento-delle-mod)
- [Risoluzione dei conflitti tra mod](#risoluzione-dei-conflitti-tra-mod)
- [Errori comuni](#errori-comuni)

---

## Come si caricano le mod

DayZ carica le mod tramite il parametro di avvio `-mod=`. Ogni voce e un percorso a una cartella contenente file PBO e un `config.cpp`. Il motore legge ogni PBO in ogni cartella mod, registra le sue classi e script, poi passa alla mod successiva nella lista.

Server e client devono avere le stesse mod in `-mod=`. Se il server elenca `@CF;@MyMod` e il client ha solo `@CF`, la connessione fallisce con un mismatch di firma. Le mod solo server inserite in `-servermod=` sono l'eccezione -- i client non ne hanno mai bisogno.

---

## Formato dei parametri di avvio

Un tipico comando di avvio per un server moddato:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Parametro | Scopo |
|-----------|-------|
| `-mod=` | Mod richieste sia dal server che da tutti i client che si connettono |
| `-servermod=` | Mod solo server (i client non ne hanno bisogno) |

Regole:
- I percorsi sono **separati da punto e virgola** senza spazi intorno ai punti e virgola
- Ogni percorso e relativo alla directory root del server (ad esempio `@CF` significa `<root_server>/@CF/`)
- Puoi usare percorsi assoluti: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **L'ordine conta** -- le dipendenze devono apparire prima delle mod che le richiedono

---

## Installazione delle mod dal Workshop

### Passo 1: Scarica la mod

Usa SteamCMD con l'App ID del **client** DayZ (221100) e l'ID Workshop della mod:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

I file scaricati finiscono in:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Passo 2: Crea un link simbolico o copia

Le cartelle del Workshop usano ID numerici, che sono inutilizzabili in `-mod=`. Crea un link simbolico nominato (raccomandato) o copia la cartella:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Usare una giunzione significa che gli aggiornamenti tramite SteamCMD si applicano automaticamente -- non e necessario ricopiare.

### Passo 3: Copia il .bikey

Vedi la sezione successiva.

---

## Chiavi delle mod (.bikey)

Ogni mod firmata include una cartella `keys/` contenente uno o piu file `.bikey`. Questi file dicono a BattlEye quali firme PBO accettare.

1. Apri la cartella della mod (ad esempio `@CF/keys/`)
2. Copia ogni file `.bikey` nella directory root `keys/` del server

```
DayZServer/
  keys/
    dayz.bikey              # Vanilla -- sempre presente
    cf.bikey                # Copiato da @CF/keys/
    vpp_admintools.bikey    # Copiato da @VPPAdminTools/keys/
```

Senza la chiave corretta, qualsiasi giocatore che usa quella mod riceve: **"Player kicked: Modified data"**.

---

## Ordine di caricamento e dipendenze

Le mod si caricano da sinistra a destra nel parametro `-mod=`. Il `config.cpp` di una mod dichiara le sue dipendenze:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Se `MyMod` richiede `CF`, allora `@CF` deve apparire **prima** di `@MyMod` nel parametro di avvio:

```
-mod=@CF;@MyMod          ✓ corretto
-mod=@MyMod;@CF          ✗ crash o classi mancanti
```

**Schema generale dell'ordine di caricamento:**

1. **Mod framework** -- CF, Community-Online-Tools
2. **Mod libreria** -- BuilderItems, qualsiasi pacchetto di risorse condivise
3. **Mod di funzionalita** -- aggiunte di mappe, armi, veicoli
4. **Mod dipendenti** -- qualsiasi cosa che elenca le precedenti come `requiredAddons`

In caso di dubbio, controlla la pagina Workshop della mod o la sua documentazione. La maggior parte degli autori di mod pubblica l'ordine di caricamento richiesto.

---

## Mod solo server vs richieste dal client

| Parametro | Chi ne ha bisogno | Esempi tipici |
|-----------|-------------------|---------------|
| `-mod=` | Server + tutti i client | Armi, veicoli, mappe, mod UI, abbigliamento |
| `-servermod=` | Solo il server | Gestori dell'economia, strumenti di logging, backend admin, script di programmazione |

La regola e diretta: se una mod contiene **qualsiasi** script lato client, layout, texture o modelli, deve andare in `-mod=`. Se esegue solo logica lato server senza risorse che il client tocca mai, usa `-servermod=`.

Mettere una mod solo server in `-mod=` costringe ogni giocatore a scaricarla. Mettere una mod richiesta dal client in `-servermod=` causa texture mancanti, UI rotte o errori di script sul client.

---

## Aggiornamento delle mod

### Procedura

1. **Ferma il server** -- aggiornare i file mentre il server e in esecuzione puo corrompere i PBO
2. **Riscarica** tramite SteamCMD:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Copia i file .bikey aggiornati** -- gli autori delle mod ruotano occasionalmente le loro chiavi di firma. Copia sempre il `.bikey` aggiornato dalla cartella `keys/` della mod alla directory `keys/` del server
4. **Riavvia il server**

Se hai usato link simbolici (giunzioni), il passo 2 aggiorna i file della mod direttamente. Se hai copiato i file manualmente, devi copiarli di nuovo.

### Aggiornamenti lato client

I giocatori iscritti alla mod sul Workshop di Steam ricevono automaticamente gli aggiornamenti. Se aggiorni una mod sul server e un giocatore ha la versione vecchia, ricevono un mismatch di firma e non possono connettersi finche il loro client non si aggiorna.

---

## Risoluzione dei conflitti tra mod

### Controlla il log RPT

Apri il file `.RPT` piu recente in `profiles/`. Cerca:

- **"Cannot register"** -- una collisione di nomi di classe tra due mod
- **"Missing addons"** -- una dipendenza non e caricata (ordine di caricamento sbagliato o mod mancante)
- **"Signature verification failed"** -- mismatch del `.bikey` o chiave mancante

### Controlla il log degli script

Apri il file `script_*.log` piu recente in `profiles/`. Cerca:

- **"SCRIPT (E)"** -- errori di script, spesso causati dall'ordine di caricamento o da mismatch di versione
- **"Definition of variable ... already exists"** -- due mod definiscono la stessa classe

### Isola il problema

Quando hai molte mod e qualcosa si rompe, testa incrementalmente:

1. Parti con solo le mod framework (`@CF`)
2. Aggiungi una mod alla volta
3. Avvia e controlla i log dopo ogni aggiunta
4. La mod che causa errori e la colpevole

### Due mod che modificano la stessa classe

Se due mod usano entrambe `modded class PlayerBase`, quella caricata **per ultima** (la piu a destra in `-mod=`) vince. La sua chiamata `super` si concatena alla versione dell'altra mod. Questo di solito funziona, ma se una mod sovrascrive un metodo senza chiamare `super`, le modifiche dell'altra mod vanno perse.

---

## Errori comuni

**Ordine di caricamento sbagliato.** Il server va in crash o registra "Missing addons" perche una dipendenza non era ancora caricata. Soluzione: sposta la mod dipendenza prima nella lista `-mod=`.

**Dimenticare `-servermod=` per le mod solo server.** I giocatori sono costretti a scaricare una mod di cui non hanno bisogno. Soluzione: sposta le mod solo server da `-mod=` a `-servermod=`.

**Non aggiornare i file `.bikey` dopo un aggiornamento della mod.** I giocatori vengono espulsi con "Modified data" perche la chiave del server non corrisponde alle nuove firme PBO della mod. Soluzione: ricopia sempre i file `.bikey` quando aggiorni le mod.

**Reimpacchettare i PBO delle mod.** Reimpacchettare i file PBO di una mod rompe la sua firma digitale, causa espulsioni BattlEye per ogni giocatore e viola i termini della maggior parte degli autori di mod. Non reimpacchettare mai una mod che non hai creato tu.

**Mescolare percorsi del Workshop con percorsi locali.** Usare il percorso numerico grezzo del Workshop per alcune mod e cartelle con nome per altre causa confusione durante l'aggiornamento. Scegli un approccio -- i link simbolici sono la soluzione piu pulita.

**Spazi nei percorsi delle mod.** Un percorso come `-mod=@My Mod` rompe il parsing. Rinomina le cartelle delle mod per evitare spazi, o racchiudi l'intero parametro tra virgolette: `-mod="@My Mod;@CF"`.

**Mod obsoleta sul server, aggiornata sul client (o viceversa).** Il mismatch di versione impedisce la connessione. Mantieni sincronizzate le versioni del server e del Workshop. Aggiorna tutte le mod e il server contemporaneamente.

---

[Home](../README.md) | [<< Precedente: Controllo Accessi](09-access-control.md) | [Successivo: Risoluzione Problemi >>](11-troubleshooting.md)
