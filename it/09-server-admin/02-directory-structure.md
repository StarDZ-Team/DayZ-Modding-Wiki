# Chapter 9.2: Struttura delle Directory e Cartella Missione

[Home](../README.md) | [<< Precedente: Configurazione del Server](01-server-setup.md) | **Struttura delle Directory** | [Successivo: Riferimento serverDZ.cfg >>](03-server-cfg.md)

---

> **Riepilogo:** Una guida completa di ogni file e cartella nella directory del server DayZ e nella cartella missione. Sapere cosa fa ciascun file -- e quali sono sicuri da modificare -- e essenziale prima di toccare l'economia del loot o aggiungere mod.

---

## Indice

- [Directory principale del server](#directory-principale-del-server)
- [La cartella addons/](#la-cartella-addons)
- [La cartella keys/](#la-cartella-keys)
- [La cartella profiles/](#la-cartella-profiles)
- [La cartella mpmissions/](#la-cartella-mpmissions)
- [Struttura della cartella missione](#struttura-della-cartella-missione)
- [La cartella db/ -- Cuore dell'economia](#la-cartella-db----cuore-delleconomia)
- [La cartella env/ -- Territori degli animali](#la-cartella-env----territori-degli-animali)
- [La cartella storage_1/ -- Persistenza](#la-cartella-storage_1----persistenza)
- [File principali della missione](#file-principali-della-missione)
- [Quali file modificare e quali non toccare](#quali-file-modificare-e-quali-non-toccare)

---

## Directory principale del server

```
DayZServer/
  DayZServer_x64.exe          # Eseguibile del server
  serverDZ.cfg                 # Configurazione principale del server (nome, password, mod, orario)
  dayzsetting.xml              # Impostazioni di rendering (irrilevante per server dedicati)
  ban.txt                      # Steam64 ID bannati, uno per riga
  whitelist.txt                # Steam64 ID nella whitelist, uno per riga
  steam_appid.txt              # Contiene "221100" -- non modificare
  dayz.gproj                   # File progetto Workbench -- non modificare
  addons/                      # PBO del gioco vanilla
  battleye/                    # File anti-cheat
  config/                      # Configurazione Steam (config.vdf)
  dta/                         # PBO core del motore (script, GUI, grafica)
  keys/                        # Chiavi di verifica delle firme (file .bikey)
  logs/                        # Log a livello di motore
  mpmissions/                  # Tutte le cartelle delle missioni
  profiles/                    # Output a runtime (log degli script, DB giocatori, dump dei crash)
  server_manager/              # Utilita di gestione del server
```

---

## La cartella addons/

Contiene tutti i contenuti vanilla del gioco impacchettati come file PBO. Ogni PBO ha un file di firma `.bisign` corrispondente:

```
addons/
  ai.pbo                       # Script di comportamento IA
  ai.pbo.dayz.bisign           # Firma per ai.pbo
  animals.pbo                  # Definizioni degli animali
  characters_backpacks.pbo     # Modelli/config degli zaini
  characters_belts.pbo         # Modelli degli oggetti da cintura
  weapons_firearms.pbo         # Modelli/config delle armi
  ... (100+ file PBO)
```

**Non modificare mai questi file.** Vengono sovrascritti ogni volta che aggiorni il server tramite SteamCMD. Le mod sovrascrivono il comportamento vanilla attraverso il sistema `modded` class, non modificando i PBO.

---

## La cartella keys/

Contiene file di chiave pubblica `.bikey` usati per verificare le firme delle mod:

```
keys/
  dayz.bikey                   # Chiave di firma vanilla (sempre presente)
```

Quando aggiungi una mod, copia il suo file `.bikey` in questa cartella. Il server usa `verifySignatures = 2` in `serverDZ.cfg` per rifiutare qualsiasi PBO che non ha un `.bikey` corrispondente in questa cartella.

Se un giocatore carica una mod la cui chiave non e nella tua cartella `keys/`, riceve un kick con **"Signature check failed"**.

---

## La cartella profiles/

Viene creata al primo avvio del server. Contiene l'output a runtime:

```
profiles/
  BattlEye/                              # Log e ban di BE
  DataCache/                             # Dati memorizzati in cache
  Users/                                 # File delle preferenze per giocatore
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Log di amministrazione
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Report del motore (info sui crash, avvisi)
  script_2026-03-08_11-34-35.log           # Log degli script (il tuo strumento di debug principale)
```

Il **log degli script** e il file piu importante qui. Ogni chiamata `Print()`, ogni errore di script e ogni messaggio di caricamento delle mod finisce qui. Quando qualcosa si rompe, e qui che guardi per primo.

I file di log si accumulano nel tempo. I log vecchi non vengono cancellati automaticamente.

---

## La cartella mpmissions/

Contiene una sottocartella per ogni mappa:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (gratuita)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

Il formato del nome della cartella e `<nomeMissione>.<nomeTerreno>`. Il valore `template` in `serverDZ.cfg` deve corrispondere esattamente a uno di questi nomi di cartella.

---

## Struttura della cartella missione

La cartella missione di Chernarus (`mpmissions/dayzOffline.chernarusplus/`) contiene:

```
dayzOffline.chernarusplus/
  init.c                         # Script del punto di ingresso della missione
  db/                            # File core dell'economia
  env/                           # Definizioni dei territori degli animali
  storage_1/                     # Dati di persistenza (giocatori, stato del mondo)
  cfgeconomycore.xml             # Classi root dell'economia e impostazioni di log
  cfgenvironment.xml             # Collegamento ai file dei territori degli animali
  cfgeventgroups.xml             # Definizioni dei gruppi di eventi
  cfgeventspawns.xml             # Posizioni esatte di spawn per gli eventi (veicoli, ecc.)
  cfgeffectarea.json             # Definizioni delle zone contaminate
  cfggameplay.json               # Regolazione del gameplay (stamina, danno, costruzione)
  cfgignorelist.xml              # Oggetti esclusi completamente dall'economia
  cfglimitsdefinition.xml        # Definizioni valide di tag categoria/usage/value
  cfglimitsdefinitionuser.xml    # Definizioni personalizzate di tag definite dall'utente
  cfgplayerspawnpoints.xml       # Posizioni di spawn dei nuovi giocatori
  cfgrandompresets.xml           # Definizioni riutilizzabili dei pool di loot
  cfgspawnabletypes.xml          # Oggetti e cargo pre-attaccati alle entita generate
  cfgundergroundtriggers.json    # Trigger per aree sotterranee
  cfgweather.xml                 # Configurazione del meteo
  areaflags.map                  # Dati dei flag delle aree (binario)
  mapclusterproto.xml            # Definizioni dei prototipi dei cluster della mappa
  mapgroupcluster.xml            # Definizioni dei cluster dei gruppi di edifici
  mapgroupcluster01.xml          # Dati dei cluster (parte 1)
  mapgroupcluster02.xml          # Dati dei cluster (parte 2)
  mapgroupcluster03.xml          # Dati dei cluster (parte 3)
  mapgroupcluster04.xml          # Dati dei cluster (parte 4)
  mapgroupdirt.xml               # Posizioni del loot a terra/sporco
  mapgrouppos.xml                # Posizioni dei gruppi della mappa
  mapgroupproto.xml              # Definizioni dei prototipi per i gruppi della mappa
```

---

## La cartella db/ -- Cuore dell'economia

Questo e il cuore della Central Economy. Cinque file controllano cosa appare, dove e in che quantita:

```
db/
  types.xml        # IL file chiave: definisce le regole di spawn di ogni oggetto
  globals.xml      # Parametri globali dell'economia (timer, limiti, conteggi)
  events.xml       # Eventi dinamici (animali, veicoli, elicotteri)
  economy.xml      # Toggle per i sottosistemi dell'economia (loot, animali, veicoli)
  messages.xml     # Messaggi del server programmati per i giocatori
```

### types.xml

Definisce le regole di spawn per **ogni oggetto** nel gioco. Con circa 23.000 righe, e di gran lunga il file dell'economia piu grande. Ogni voce specifica quante copie di un oggetto dovrebbero esistere sulla mappa, dove puo apparire e per quanto tempo persiste. Vedi [Capitolo 9.4](04-loot-economy.md) per un'analisi approfondita.

### globals.xml

Parametri globali che influenzano l'intera economia: conteggio degli zombie, conteggio degli animali, timer di pulizia, intervalli di danno del loot, tempistiche di respawn. Ci sono 33 parametri in totale. Vedi [Capitolo 9.4](04-loot-economy.md) per il riferimento completo.

### events.xml

Definisce gli eventi di spawn dinamici per animali e veicoli. Ogni evento specifica un conteggio nominale, vincoli di spawn e varianti figlie. Ad esempio, l'evento `VehicleCivilianSedan` genera 8 berline sulla mappa in 3 varianti di colore.

### economy.xml

Toggle principali per i sottosistemi dell'economia:

```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```

| Flag | Significato |
|------|-------------|
| `init` | Genera oggetti al primo avvio del server |
| `load` | Carica lo stato salvato dalla persistenza |
| `respawn` | Consente il respawn degli oggetti dopo la pulizia |
| `save` | Salva lo stato nei file di persistenza |

### messages.xml

Messaggi programmati trasmessi a tutti i giocatori. Supporta timer di conto alla rovescia, intervalli di ripetizione, messaggi alla connessione e avvisi di spegnimento:

```xml
<messages>
    <message>
        <deadline>600</deadline>
        <shutdown>1</shutdown>
        <text>#name will shutdown in #tmin minutes.</text>
    </message>
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>Welcome to #name</text>
    </message>
</messages>
```

Usa `#name` per il nome del server e `#tmin` per il tempo rimanente in minuti.

---

## La cartella env/ -- Territori degli animali

Contiene file XML che definiscono dove ogni specie animale puo apparire:

```
env/
  bear_territories.xml
  cattle_territories.xml
  domestic_animals_territories.xml
  fox_territories.xml
  hare_territories.xml
  hen_territories.xml
  pig_territories.xml
  red_deer_territories.xml
  roe_deer_territories.xml
  sheep_goat_territories.xml
  wild_boar_territories.xml
  wolf_territories.xml
  zombie_territories.xml
```

Questi file contengono centinaia di punti di coordinate che definiscono le zone di territorio sulla mappa. Sono referenziati da `cfgenvironment.xml`. Raramente hai bisogno di modificarli a meno che tu non voglia cambiare dove gli animali o gli zombie appaiono geograficamente.

---

## La cartella storage_1/ -- Persistenza

Contiene lo stato persistente del server tra i riavvii:

```
storage_1/
  players.db         # Database SQLite di tutti i personaggi dei giocatori
  spawnpoints.bin    # Dati binari dei punti di spawn
  backup/            # Backup automatici dei dati di persistenza
  data/              # Stato del mondo (oggetti piazzati, costruzione basi, veicoli)
```

**Non modificare mai `players.db` mentre il server e in esecuzione.** E un database SQLite bloccato dal processo del server. Se hai bisogno di cancellare i personaggi, ferma prima il server e cancella o rinomina il file.

Per fare un **wipe completo della persistenza**, ferma il server e cancella l'intera cartella `storage_1/`. Il server la ricreera al prossimo avvio con un mondo nuovo.

Per fare un **wipe parziale** (mantieni i personaggi, resetta il loot):
1. Ferma il server
2. Cancella i file in `storage_1/data/` ma mantieni `players.db`
3. Riavvia

---

## File principali della missione

### cfgeconomycore.xml

Registra le classi root per l'economia e configura il logging della CE:

```xml
<economycore>
    <classes>
        <rootclass name="DefaultWeapon" />
        <rootclass name="DefaultMagazine" />
        <rootclass name="Inventory_Base" />
        <rootclass name="HouseNoDestruct" reportMemoryLOD="no" />
        <rootclass name="SurvivorBase" act="character" reportMemoryLOD="no" />
        <rootclass name="DZ_LightAI" act="character" reportMemoryLOD="no" />
        <rootclass name="CarScript" act="car" reportMemoryLOD="no" />
        <rootclass name="BoatScript" act="car" reportMemoryLOD="no" />
    </classes>
    <defaults>
        <default name="log_ce_loop" value="false"/>
        <default name="log_ce_dynamicevent" value="false"/>
        <default name="log_ce_vehicle" value="false"/>
        <default name="log_ce_lootspawn" value="false"/>
        <default name="log_ce_lootcleanup" value="false"/>
        <default name="log_ce_lootrespawn" value="false"/>
        <default name="log_ce_statistics" value="false"/>
        <default name="log_ce_zombie" value="false"/>
        <default name="log_storageinfo" value="false"/>
        <default name="log_hivewarning" value="true"/>
        <default name="log_missionfilewarning" value="true"/>
        <default name="save_events_startup" value="true"/>
        <default name="save_types_startup" value="true"/>
    </defaults>
</economycore>
```

Imposta `log_ce_lootspawn` su `"true"` quando effettui il debug di problemi di spawn degli oggetti. Produce un output dettagliato nel log RPT che mostra quali oggetti la CE sta tentando di generare e perche riescono o falliscono.

### cfglimitsdefinition.xml

Definisce i valori validi per gli elementi `<category>`, `<usage>`, `<value>` e `<tag>` usati in `types.xml`:

```xml
<lists>
    <categories>
        <category name="tools"/>
        <category name="containers"/>
        <category name="clothes"/>
        <category name="food"/>
        <category name="weapons"/>
        <category name="books"/>
        <category name="explosives"/>
        <category name="lootdispatch"/>
    </categories>
    <tags>
        <tag name="floor"/>
        <tag name="shelves"/>
        <tag name="ground"/>
    </tags>
    <usageflags>
        <usage name="Military"/>
        <usage name="Police"/>
        <usage name="Medic"/>
        <usage name="Firefighter"/>
        <usage name="Industrial"/>
        <usage name="Farm"/>
        <usage name="Coast"/>
        <usage name="Town"/>
        <usage name="Village"/>
        <usage name="Hunting"/>
        <usage name="Office"/>
        <usage name="School"/>
        <usage name="Prison"/>
        <usage name="Lunapark"/>
        <usage name="SeasonalEvent"/>
        <usage name="ContaminatedArea"/>
        <usage name="Historical"/>
    </usageflags>
    <valueflags>
        <value name="Tier1"/>
        <value name="Tier2"/>
        <value name="Tier3"/>
        <value name="Tier4"/>
        <value name="Unique"/>
    </valueflags>
</lists>
```

Se usi un tag `<usage>` o `<value>` in `types.xml` che non e definito qui, l'oggetto non apparira silenziosamente.

### cfgignorelist.xml

Gli oggetti elencati qui sono completamente esclusi dall'economia, anche se hanno voci in `types.xml`:

```xml
<ignore>
    <type name="Bandage"></type>
    <type name="CattleProd"></type>
    <type name="Defibrillator"></type>
    <type name="HescoBox"></type>
    <type name="StunBaton"></type>
    <type name="TransitBus"></type>
    <type name="Spear"></type>
    <type name="Mag_STANAGCoupled_30Rnd"></type>
    <type name="Wreck_Mi8"></type>
</ignore>
```

Questo viene usato per oggetti che esistono nel codice del gioco ma non sono destinati a comparire naturalmente (oggetti non finiti, contenuti deprecati, oggetti stagionali fuori stagione).

### cfggameplay.json

Un file JSON che sovrascrive i parametri di gameplay. Controlla stamina, movimento, danno alle basi, meteo, temperatura, ostruzione delle armi, annegamento e altro. Questo file e opzionale -- se assente, il server usa i valori predefiniti.

### cfgplayerspawnpoints.xml

Definisce dove i giocatori appena spawnati appaiono sulla mappa, con vincoli di distanza da infetti, altri giocatori ed edifici.

### cfgeventspawns.xml

Contiene le coordinate esatte nel mondo dove gli eventi (veicoli, relitti di elicotteri, ecc.) possono apparire. Ogni nome di evento da `events.xml` ha una lista di posizioni valide:

```xml
<eventposdef>
    <event name="VehicleCivilianSedan">
        <pos x="12071.933594" z="9129.989258" a="317.953339" />
        <pos x="12302.375001" z="9051.289062" a="60.399284" />
        <pos x="10182.458985" z="1987.5271" a="29.172445" />
        ...
    </event>
</eventposdef>
```

L'attributo `a` e l'angolo di rotazione in gradi.

---

## Quali file modificare e quali non toccare

| File / Cartella | Modificabile? | Note |
|-----------------|:---:|-------|
| `serverDZ.cfg` | Si | Configurazione principale del server |
| `db/types.xml` | Si | Regole di spawn degli oggetti -- la tua modifica piu comune |
| `db/globals.xml` | Si | Parametri di regolazione dell'economia |
| `db/events.xml` | Si | Eventi di spawn veicoli/animali |
| `db/economy.xml` | Si | Toggle dei sottosistemi dell'economia |
| `db/messages.xml` | Si | Messaggi broadcast del server |
| `cfggameplay.json` | Si | Regolazione del gameplay |
| `cfgspawnabletypes.xml` | Si | Preset di attacchi/cargo |
| `cfgrandompresets.xml` | Si | Definizioni dei pool di loot |
| `cfglimitsdefinition.xml` | Si | Aggiungi tag usage/value personalizzati |
| `cfgplayerspawnpoints.xml` | Si | Posizioni di spawn dei giocatori |
| `cfgeventspawns.xml` | Si | Coordinate di spawn degli eventi |
| `cfgignorelist.xml` | Si | Escludi oggetti dall'economia |
| `cfgweather.xml` | Si | Pattern meteo |
| `cfgeffectarea.json` | Si | Zone contaminate |
| `init.c` | Si | Script di ingresso della missione |
| `addons/` | **No** | Sovrascritto durante l'aggiornamento |
| `dta/` | **No** | Dati core del motore |
| `keys/` | Solo aggiunta | Copia qui i file `.bikey` delle mod |
| `storage_1/` | Solo cancellazione | Persistenza -- non modificare a mano |
| `battleye/` | **No** | Anti-cheat -- non toccare |
| `mapgroup*.xml` | Attenzione | Posizioni del loot negli edifici -- modifica avanzata |

---

**Precedente:** [Configurazione del Server](01-server-setup.md) | [Home](../README.md) | **Successivo:** [Riferimento serverDZ.cfg >>](03-server-cfg.md)
