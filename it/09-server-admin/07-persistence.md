# Chapter 9.7: Stato del Mondo e Persistenza

[Home](../README.md) | [<< Precedente: Spawn dei Giocatori](06-player-spawning.md) | [Successivo: Ottimizzazione delle Prestazioni >>](08-performance.md)

La persistenza di DayZ mantiene il mondo vivo tra i riavvii. Capire come funziona ti permette di gestire le basi, pianificare i wipe ed evitare la corruzione dei dati.

## Indice

- [Come funziona la persistenza](#come-funziona-la-persistenza)
- [La directory storage_1/](#la-directory-storage_1)
- [Parametri di persistenza in globals.xml](#parametri-di-persistenza-in-globalsxml)
- [Sistema dei pali con bandiera](#sistema-dei-pali-con-bandiera)
- [Oggetti accumulatori](#oggetti-accumulatori)
- [Impostazioni di persistenza in cfggameplay.json](#impostazioni-di-persistenza-in-cfggameplayjson)
- [Procedure di wipe del server](#procedure-di-wipe-del-server)
- [Strategia di backup](#strategia-di-backup)
- [Errori comuni](#errori-comuni)

---

## Come funziona la persistenza

DayZ memorizza lo stato del mondo nella directory `storage_1/` all'interno della cartella profilo del tuo server. Il ciclo e semplice:

1. Il server salva lo stato del mondo periodicamente (ogni ~30 minuti per impostazione predefinita) e allo spegnimento controllato.
2. Al riavvio, il server legge `storage_1/` e ripristina tutti gli oggetti persistiti -- veicoli, basi, tende, barili, inventari dei giocatori.
3. Gli oggetti senza persistenza (la maggior parte del loot a terra) vengono rigenerati dalla Central Economy ad ogni riavvio.

Se `storage_1/` non esiste all'avvio, il server crea un mondo nuovo senza dati dei giocatori e senza strutture costruite.

---

## La directory storage_1/

Il profilo del tuo server contiene `storage_1/` con queste sottodirectory e file:

| Percorso | Contenuti |
|----------|-----------|
| `data/` | File binari contenenti gli oggetti del mondo -- parti delle basi, oggetti piazzati, posizioni dei veicoli |
| `players/` | File **.save** per giocatore indicizzati per SteamID64. Ogni file memorizza posizione, inventario, salute, effetti di stato |
| `snapshot/` | Snapshot dello stato del mondo usati durante le operazioni di salvataggio |
| `events.bin` / `events.xy` | Stato degli eventi dinamici -- traccia le posizioni dei relitti di elicotteri, dei convogli e di altri eventi generati |

La cartella `data/` e la parte principale della persistenza. Contiene dati serializzati degli oggetti che il server legge all'avvio per ricostruire il mondo.

---

## Parametri di persistenza in globals.xml

Il file **globals.xml** (nella cartella della tua missione) controlla i timer di pulizia e il comportamento delle bandiere. Questi sono i valori rilevanti per la persistenza:

```xml
<!-- Refresh del palo con bandiera -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 giorni (secondi) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 giorni (secondi) -->

<!-- Timer di pulizia -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Pulizia predefinita (secondi) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Corpo giocatore morto: 1 ora -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Animale morto: 20 minuti -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Zombie morto: 5,5 minuti -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Oggetto rovinato: 5,5 minuti -->

<!-- Comportamento della pulizia -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Massimo oggetti ripuliti per ciclo -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Salta la pulizia entro 100m da un giocatore -->
```

Il valore `CleanupAvoidance` impedisce al server di rimuovere oggetti vicino ai giocatori attivi. Se un corpo morto e entro 100 metri da qualsiasi giocatore, rimane finche il giocatore non si allontana o il timer si resetta.

---

## Sistema dei pali con bandiera

I pali con bandiera (territory flag) sono il cuore della persistenza delle basi in DayZ. Ecco come interagiscono i due valori chiave:

- **FlagRefreshFrequency** (`432000` secondi = 5 giorni) -- Quanto spesso devi interagire con la tua bandiera per mantenerla attiva. Avvicinati alla bandiera e usa l'azione "Aggiorna".
- **FlagRefreshMaxDuration** (`3456000` secondi = 40 giorni) -- Il tempo massimo di protezione accumulato. Ogni aggiornamento aggiunge fino a FlagRefreshFrequency di tempo, ma il totale non puo superare questo limite.

Quando il timer di una bandiera scade:

1. La bandiera stessa diventa idonea alla pulizia.
2. Tutte le parti di costruzione base collegate a quella bandiera perdono la protezione della persistenza.
3. Al prossimo ciclo di pulizia, le parti non protette iniziano a scomparire.

Se abbassi FlagRefreshFrequency, i giocatori devono visitare le loro basi piu spesso. Se alzi FlagRefreshMaxDuration, le basi sopravvivono piu a lungo tra le visite. Regola entrambi i valori insieme per adattarli allo stile di gioco del tuo server.

---

## Oggetti accumulatori

In **cfgspawnabletypes.xml**, certi contenitori sono contrassegnati con `<hoarder/>`. Questo li segna come oggetti capaci di stoccaggio che contano verso i limiti di stoccaggio per giocatore nella Central Economy.

Gli oggetti accumulatori vanilla sono:

| Oggetto | Tipo |
|---------|------|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Barili di stoccaggio |
| CarTent, LargeTent, MediumTent, PartyTent | Tende |
| SeaChest | Stoccaggio subacqueo |
| SmallProtectorCase | Piccola cassa con lucchetto |
| UndergroundStash | Scorta sepolta |
| WoodenCrate | Cassa artigianale |

Esempio da **cfgspawnabletypes.xml**:

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

Il server traccia quanti oggetti accumulatori ogni giocatore ha piazzato. Quando il limite viene raggiunto, i nuovi piazzamenti falliscono o l'oggetto piu vecchio scompare (a seconda della configurazione del server).

---

## Impostazioni di persistenza in cfggameplay.json

Il file **cfggameplay.json** nella cartella della tua missione contiene impostazioni che influenzano la durabilita delle basi e dei contenitori:

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Impostazione | Predefinito | Effetto |
|--------------|-------------|--------|
| `disableBaseDamage` | `false` | Quando e `true`, le parti di costruzione base (muri, cancelli, torri di guardia) non possono essere danneggiate. Questo disabilita effettivamente il raiding. |
| `disableContainerDamage` | `false` | Quando e `true`, i contenitori di stoccaggio (tende, barili, casse) non possono subire danni. Gli oggetti dentro rimangono al sicuro. |

Impostare entrambi su `true` crea un server PvE-friendly dove le basi e lo stoccaggio sono indistruttibili. La maggior parte dei server PvP lascia entrambi su `false`.

---

## Procedure di wipe del server

Hai quattro tipi di wipe, ciascuno mirato a una parte diversa di `storage_1/`. **Ferma sempre il server prima di eseguire qualsiasi wipe.**

### Wipe completo

Cancella l'intera cartella `storage_1/`. Il server crea un mondo nuovo al prossimo avvio. Tutte le basi, i veicoli, le tende, i dati dei giocatori e lo stato degli eventi sono persi.

### Wipe dell'economia (mantieni i giocatori)

Cancella `storage_1/data/` ma lascia intatto `storage_1/players/`. I giocatori mantengono i loro personaggi e inventari, ma tutti gli oggetti piazzati (basi, tende, barili, veicoli) vengono rimossi.

### Wipe dei giocatori (mantieni il mondo)

Cancella `storage_1/players/`. Tutti i personaggi dei giocatori si resettano a nuovi spawn. Le basi e gli oggetti piazzati rimangono nel mondo.

### Reset meteo / eventi

Cancella `events.bin` o `events.xy` da `storage_1/`. Questo resetta le posizioni degli eventi dinamici (relitti di elicotteri, convogli). Il server genera nuove posizioni degli eventi al prossimo avvio.

---

## Strategia di backup

I dati di persistenza sono insostituibili una volta persi. Segui queste pratiche:

- **Esegui il backup da fermo.** Copia l'intera cartella `storage_1/` mentre il server non e in esecuzione. Copiare durante l'esecuzione rischia di catturare uno stato parziale o corrotto.
- **Programma i backup prima dei riavvii.** Se esegui riavvii automatizzati (ogni 4-6 ore), aggiungi un passo di backup al tuo script di riavvio che copia `storage_1/` prima che il processo del server si avvii.
- **Mantieni piu generazioni.** Ruota i backup in modo da avere almeno 3 copie recenti. Se il tuo ultimo backup e corrotto, puoi tornare a uno precedente.
- **Conserva fuori dalla macchina.** Copia i backup su un disco separato o su cloud storage. Un guasto del disco sulla macchina del server porta via anche i tuoi backup se sono sullo stesso disco.

Uno script di backup minimale (eseguito prima dell'avvio del server):

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Errori comuni

Questi vengono fuori ripetutamente nelle comunita di amministratori di server:

| Errore | Cosa succede | Prevenzione |
|--------|-------------|-------------|
| Cancellare `storage_1/` mentre il server e in esecuzione | Corruzione dei dati. Il server scrive su file che non esistono piu, causando crash o stato parziale al prossimo avvio. | Ferma sempre il server prima. |
| Non fare il backup prima di un wipe | Se cancelli accidentalmente la cartella sbagliata o il wipe va storto, non c'e recupero. | Fai il backup di `storage_1/` prima di ogni wipe. |
| Confondere il reset del meteo con il wipe completo | Cancellare `events.xy` resetta solo le posizioni degli eventi dinamici. Non resetta il loot, le basi o i giocatori. | Sappi quali file controllano cosa (vedi la tabella delle directory sopra). |
| Bandiera non aggiornata in tempo | Dopo 40 giorni (FlagRefreshMaxDuration), la bandiera scade e tutte le parti della base collegate diventano idonee alla pulizia. I giocatori perdono l'intera base. | Ricorda ai giocatori l'intervallo di aggiornamento. Abbassa FlagRefreshMaxDuration sui server con pochi giocatori. |
| Modificare globals.xml mentre il server e in esecuzione | Le modifiche non vengono recepite fino al riavvio. Peggio, il server potrebbe sovrascrivere le tue modifiche allo spegnimento. | Modifica i file di configurazione solo mentre il server e fermo. |

---

[Home](../README.md) | [<< Precedente: Spawn dei Giocatori](06-player-spawning.md) | [Successivo: Ottimizzazione delle Prestazioni >>](08-performance.md)
