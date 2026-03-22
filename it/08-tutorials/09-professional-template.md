# Capitolo 8.9: Template Professionale per Mod

[Home](../README.md) | [<< Precedente: Costruire un Overlay HUD](08-hud-overlay.md) | **Template Professionale per Mod** | [Successivo: Creare un Veicolo Personalizzato >>](10-vehicle-mod.md)

---

> **Riepilogo:** Questo capitolo fornisce un template completo, pronto per la produzione, con ogni file necessario per un mod DayZ professionale. A differenza del [Capitolo 8.5](05-mod-template.md) che introduce lo scheletro iniziale di InclementDab, questo è un template completo con sistema di configurazione, manager singleton, RPC client-server, pannello UI, keybind, localizzazione e automazione della build. Ogni file è pronto da copiare e incollare, con commenti dettagliati che spiegano **perché** ogni riga esiste.

---

## Indice dei Contenuti

- [Panoramica](#panoramica)
- [Struttura Completa delle Directory](#struttura-completa-delle-directory)
- [mod.cpp](#modcpp)
- [config.cpp](#configcpp)
- [File delle Costanti (3_Game)](#file-delle-costanti-3_game)
- [Classe Dati di Configurazione (3_Game)](#classe-dati-di-configurazione-3_game)
- [Definizioni RPC (3_Game)](#definizioni-rpc-3_game)
- [Manager Singleton (4_World)](#manager-singleton-4_world)
- [Gestore Eventi Giocatore (4_World)](#gestore-eventi-giocatore-4_world)
- [Hook Missione: Server (5_Mission)](#hook-missione-server-5_mission)
- [Hook Missione: Client (5_Mission)](#hook-missione-client-5_mission)
- [Script Pannello UI (5_Mission)](#script-pannello-ui-5_mission)
- [File Layout](#file-layout)
- [stringtable.csv](#stringtablecsv)
- [Inputs.xml](#inputsxml)
- [Script di Build](#script-di-build)
- [Guida alla Personalizzazione](#guida-alla-personalizzazione)
- [Guida all'Espansione delle Funzionalità](#guida-allespansione-delle-funzionalità)
- [Prossimi Passi](#prossimi-passi)

---

## Panoramica

Un mod "Hello World" dimostra che la toolchain funziona. Un mod professionale richiede molto di più:

| Aspetto | Hello World | Template Professionale |
|---------|-------------|----------------------|
| Configurazione | Valori hardcoded | Configurazione JSON con caricamento/salvataggio/valori predefiniti |
| Comunicazione | Istruzioni Print | RPC con routing a stringhe (client verso server e ritorno) |
| Architettura | Un file, una funzione | Manager singleton, script a livelli, ciclo di vita pulito |
| Interfaccia utente | Nessuna | Pannello UI guidato da layout con apertura/chiusura |
| Binding input | Nessuno | Keybind personalizzato in Opzioni > Controlli |
| Localizzazione | Nessuna | stringtable.csv con 13 lingue |
| Pipeline di build | Addon Builder manuale | Script batch con un clic |
| Pulizia | Nessuna | Shutdown corretto alla fine della missione, nessuna perdita di memoria |

Questo template ti dà tutto questo pronto all'uso. Rinomini gli identificatori, elimini i sistemi di cui non hai bisogno e inizi a costruire la tua funzionalità effettiva su una base solida.

---

## Struttura Completa delle Directory

Questo è il layout completo del sorgente. Ogni file elencato di seguito è fornito come template completo in questo capitolo.

```
MyProfessionalMod/                          <-- Radice sorgente (vive sul drive P:)
    mod.cpp                                 <-- Metadati per il launcher
    Scripts/
        config.cpp                          <-- Registrazione motore (CfgPatches + CfgMods)
        Inputs.xml                          <-- Definizioni keybind
        stringtable.csv                     <-- Stringhe localizzate (13 lingue)
        3_Game/
            MyMod/
                MyModConstants.c            <-- Enum, stringa versione, costanti condivise
                MyModConfig.c               <-- Configurazione serializzabile in JSON con valori predefiniti
                MyModRPC.c                  <-- Nomi di rotta RPC e registrazione
        4_World/
            MyMod/
                MyModManager.c              <-- Manager singleton (ciclo di vita, configurazione, stato)
                MyModPlayerHandler.c        <-- Hook connessione/disconnessione giocatore
        5_Mission/
            MyMod/
                MyModMissionServer.c        <-- modded MissionServer (init/shutdown server)
                MyModMissionClient.c        <-- modded MissionGameplay (init/shutdown client)
                MyModUI.c                   <-- Script pannello UI (apertura/chiusura/popolamento)
        GUI/
            layouts/
                MyModPanel.layout           <-- Definizione layout UI
    build.bat                               <-- Automazione impacchettamento PBO

Dopo la build, la cartella mod distribuibile appare così:

@MyProfessionalMod/                         <-- Quello che va sul server / Workshop
    mod.cpp
    addons/
        MyProfessionalMod_Scripts.pbo       <-- Impacchettato da Scripts/
    keys/
        MyMod.bikey                         <-- Chiave per server firmati
    meta.cpp                                <-- Metadati Workshop (auto-generato)
```

---

## mod.cpp

Questo file controlla ciò che i giocatori vedono nel launcher di DayZ. È posizionato alla radice del mod, **non** dentro `Scripts/`.

```cpp
// ==========================================================================
// mod.cpp - Identità del mod per il launcher di DayZ
// Questo file è letto dal launcher per mostrare le info del mod nella lista.
// NON è compilato dal motore di script -- è puro metadata.
// ==========================================================================

// Nome visualizzato nella lista mod del launcher e nella schermata mod in gioco.
name         = "My Professional Mod";

// Il tuo nome o nome del team. Mostrato nella colonna "Author".
author       = "YourName";

// Stringa di versione semantica. Aggiornala con ogni rilascio.
// Il launcher mostra questo così i giocatori sanno quale versione hanno.
version      = "1.0.0";

// Breve descrizione mostrata passando il mouse sul mod nel launcher.
// Mantienila sotto i 200 caratteri per leggibilità.
overview     = "A professional mod template with config, RPC, UI, and keybinds.";

// Tooltip mostrato al passaggio del mouse. Di solito corrisponde al nome del mod.
tooltipOwned = "My Professional Mod";

// Opzionale: percorso a un'immagine di anteprima (relativo alla radice del mod).
// Dimensione raccomandata: 256x256 o 512x512, formato PAA o EDDS.
// Lascia vuoto se non hai ancora un'immagine.
picture      = "";

// Opzionale: logo mostrato nel pannello dettagli del mod.
logo         = "";
logoSmall    = "";
logoOver     = "";

// Opzionale: URL aperto quando il giocatore clicca "Website" nel launcher.
action       = "";
actionURL    = "";
```

---

## config.cpp

Questo è il file più critico. Registra il tuo mod con il motore, dichiara le dipendenze, collega i layer di script e opzionalmente imposta definizioni del preprocessore e set di immagini.

Posizionalo in `Scripts/config.cpp`.

```cpp
// ==========================================================================
// config.cpp - Registrazione motore
// Il motore di DayZ legge questo per sapere cosa fornisce il tuo mod.
// Due sezioni sono importanti: CfgPatches (grafo delle dipendenze) e CfgMods (caricamento script).
// ==========================================================================

// --------------------------------------------------------------------------
// CfgPatches - Dichiarazione delle Dipendenze
// Il motore usa questo per determinare l'ordine di caricamento. Se il tuo mod
// dipende da un altro mod, elenca la classe CfgPatches di quel mod in requiredAddons[].
// --------------------------------------------------------------------------
class CfgPatches
{
    // Il nome della classe DEVE essere globalmente unico tra tutti i mod.
    // Convenzione: ModName_Scripts (corrisponde al nome del PBO).
    class MyMod_Scripts
    {
        // units[] e weapons[] dichiarano le classi config definite da questo addon.
        // Per mod solo-script, lascia questi vuoti. Sono usati dai mod
        // che definiscono nuovi oggetti, armi o veicoli in config.cpp.
        units[] = {};
        weapons[] = {};

        // Versione minima del motore. 0.1 funziona per tutte le versioni attuali di DayZ.
        requiredVersion = 0.1;

        // Dipendenze: elenca i nomi delle classi CfgPatches di altri mod.
        // "DZ_Data" è il gioco base -- ogni mod dovrebbe dipendere da esso.
        // Aggiungi "CF_Scripts" se usi Community Framework.
        // Aggiungi altri patch di mod se li estendi.
        requiredAddons[] =
        {
            "DZ_Data"
        };
    };
};

// --------------------------------------------------------------------------
// CfgMods - Registrazione del Modulo di Script
// Dice al motore dove si trova ogni layer di script e quali define impostare.
// --------------------------------------------------------------------------
class CfgMods
{
    // Il nome della classe qui è l'identificatore interno del tuo mod.
    // NON ha bisogno di corrispondere a CfgPatches -- ma mantenerli correlati
    // rende il codebase più facile da navigare.
    class MyMod
    {
        // dir: il nome della cartella sul drive P: (o nel PBO).
        // Deve corrispondere esattamente al nome della tua cartella radice effettiva.
        dir = "MyProfessionalMod";

        // Nome visualizzato (mostrato in Workbench e in alcuni log del motore).
        name = "My Professional Mod";

        // Autore e descrizione per i metadati del motore.
        author = "YourName";
        overview = "Professional mod template";

        // Tipo di mod. Sempre "mod" per i mod di script.
        type = "mod";

        // credits: percorso opzionale a un file Credits.json.
        // creditsJson = "MyProfessionalMod/Scripts/Credits.json";

        // inputs: percorso al tuo Inputs.xml per keybind personalizzati.
        // Questo DEVE essere impostato qui perché il motore carichi i tuoi keybind.
        inputs = "MyProfessionalMod/Scripts/Inputs.xml";

        // defines: simboli del preprocessore impostati quando il tuo mod è caricato.
        // Altri mod possono usare #ifdef MYMOD per rilevare la presenza del tuo mod
        // e compilare condizionalmente codice di integrazione.
        defines[] = { "MYMOD" };

        // dependencies: quali moduli di script vanilla il tuo mod aggancia.
        // "Game" = 3_Game, "World" = 4_World, "Mission" = 5_Mission.
        // La maggior parte dei mod necessita di tutti e tre. Aggiungi "Core" solo se usi 1_Core.
        dependencies[] =
        {
            "Game", "World", "Mission"
        };

        // defs: mappa ogni modulo di script alla sua cartella su disco.
        // Il motore compila tutti i file .c trovati ricorsivamente in questi percorsi.
        // Non esiste #include in Enforce Script -- è così che vengono caricati i file.
        class defs
        {
            // imageSets: registra file .imageset per l'uso nei layout.
            // Necessario solo se hai icone/texture personalizzate per la UI.
            // Decommenta e aggiorna i percorsi se aggiungi un imageset.
            //
            // class imageSets
            // {
            //     files[] =
            //     {
            //         "MyProfessionalMod/GUI/imagesets/mymod_icons.imageset"
            //     };
            // };

            // Layer Game (3_Game): si carica per primo.
            // Posiziona qui enum, costanti, classi config, definizioni RPC.
            // NON PUÒ referenziare tipi da 4_World o 5_Mission.
            class gameScriptModule
            {
                value = "";
                files[] = { "MyProfessionalMod/Scripts/3_Game" };
            };

            // Layer World (4_World): si carica per secondo.
            // Posiziona qui manager, modifiche alle entità, interazioni col mondo.
            // PUÒ referenziare tipi di 3_Game. NON PUÒ referenziare tipi di 5_Mission.
            class worldScriptModule
            {
                value = "";
                files[] = { "MyProfessionalMod/Scripts/4_World" };
            };

            // Layer Mission (5_Mission): si carica per ultimo.
            // Posiziona qui hook di missione, pannelli UI, logica di avvio/chiusura.
            // PUÒ referenziare tipi da tutti i layer inferiori.
            class missionScriptModule
            {
                value = "";
                files[] = { "MyProfessionalMod/Scripts/5_Mission" };
            };
        };
    };
};
```

---

## File delle Costanti (3_Game)

Posizionalo in `Scripts/3_Game/MyMod/MyModConstants.c`.

Questo file definisce tutte le costanti condivise, gli enum e la stringa di versione. Risiede in `3_Game` così ogni layer superiore può accedere a questi valori.

```c
// ==========================================================================
// MyModConstants.c - Costanti condivise e enum
// Layer 3_Game: disponibile a tutti i layer superiori (4_World, 5_Mission).
//
// PERCHÉ questo file esiste:
//   Centralizzare le costanti previene numeri magici sparsi tra i file.
//   Gli enum danno sicurezza a tempo di compilazione invece di confronti con int grezzi.
//   La stringa di versione è definita una volta e usata nei log e nella UI.
// ==========================================================================

// ---------------------------------------------------------------------------
// Versione - aggiorna questo con ogni rilascio
// ---------------------------------------------------------------------------
const string MYMOD_VERSION = "1.0.0";

// ---------------------------------------------------------------------------
// Tag di log - prefisso per tutti i messaggi Print/log da questo mod
// Usare un tag consistente rende facile filtrare il log degli script.
// ---------------------------------------------------------------------------
const string MYMOD_TAG = "[MyMod]";

// ---------------------------------------------------------------------------
// Percorsi file - centralizzati così gli errori di battitura vengono individuati in un solo punto
// $profile: si risolve nella directory profilo del server a runtime.
// ---------------------------------------------------------------------------
const string MYMOD_CONFIG_DIR  = "$profile:MyMod";
const string MYMOD_CONFIG_PATH = "$profile:MyMod/config.json";

// ---------------------------------------------------------------------------
// Enum: Modalità funzionalità
// Usa gli enum invece di int grezzi per leggibilità e controlli a tempo di compilazione.
// ---------------------------------------------------------------------------
enum MyModMode
{
    DISABLED = 0,    // Funzionalità disattivata
    PASSIVE  = 1,    // Funzionalità in esecuzione ma non interferisce
    ACTIVE   = 2     // Funzionalità completamente abilitata
};

// ---------------------------------------------------------------------------
// Enum: Tipi di notifica (usati dalla UI per scegliere icona/colore)
// ---------------------------------------------------------------------------
enum MyModNotifyType
{
    INFO    = 0,
    SUCCESS = 1,
    WARNING = 2,
    ERROR   = 3
};
```

---

## Classe Dati di Configurazione (3_Game)

Posizionala in `Scripts/3_Game/MyMod/MyModConfig.c`.

Questa è una classe di impostazioni serializzabile in JSON. Il server la carica all'avvio. Se non esiste nessun file, vengono usati i valori predefiniti e una configurazione nuova viene salvata su disco.

```c
// ==========================================================================
// MyModConfig.c - Configurazione JSON con valori predefiniti
// Layer 3_Game così sia i manager di 4_World che gli hook di 5_Mission possono leggerla.
//
// COME FUNZIONA:
//   JsonFileLoader<MyModConfig> usa il serializzatore JSON integrato di Enforce Script.
//   Ogni campo con un valore predefinito viene scritto/letto dal file JSON.
//   Aggiungere un nuovo campo è sicuro -- i vecchi file config ottengono
//   semplicemente il valore predefinito per i campi mancanti.
//
// TRABOCCHETTO ENFORCE SCRIPT:
//   JsonFileLoader<T>.JsonLoadFile(path, obj) restituisce VOID.
//   NON PUOI fare: if (JsonFileLoader<T>.JsonLoadFile(...)) -- non compilerà.
//   Passa sempre un oggetto pre-creato per riferimento.
// ==========================================================================

class MyModConfig
{
    // --- Impostazioni Generali ---

    // Interruttore principale: se false, l'intero mod è disabilitato.
    bool Enabled = true;

    // Quanto spesso (in secondi) il manager esegue il suo tick di aggiornamento.
    // Valori più bassi = più reattivo ma costo CPU più alto.
    float UpdateInterval = 5.0;

    // Numero massimo di oggetti/entità che questo mod gestisce simultaneamente.
    int MaxItems = 100;

    // Modalità: 0 = DISABLED, 1 = PASSIVE, 2 = ACTIVE (vedi enum MyModMode).
    int Mode = 2;

    // --- Messaggi ---

    // Messaggio di benvenuto mostrato ai giocatori quando si connettono.
    // Stringa vuota = nessun messaggio.
    string WelcomeMessage = "Welcome to the server!";

    // Se mostrare il messaggio di benvenuto come notifica o messaggio in chat.
    bool WelcomeAsNotification = true;

    // --- Logging ---

    // Abilita il logging verboso di debug. Disattiva per i server in produzione.
    bool DebugLogging = false;

    // -----------------------------------------------------------------------
    // Load - legge la config da disco, restituisce istanza con valori predefiniti se mancante
    // -----------------------------------------------------------------------
    static MyModConfig Load()
    {
        // Crea sempre prima un'istanza nuova. Questo assicura che tutti i valori predefiniti
        // siano impostati anche se il file JSON manca di campi (ad esempio, dopo
        // un aggiornamento che ha aggiunto nuove impostazioni).
        MyModConfig cfg = new MyModConfig();

        // Controlla se il file config esiste prima di provare a caricarlo.
        // Al primo avvio, non esisterà -- usiamo i valori predefiniti e salviamo.
        if (FileExist(MYMOD_CONFIG_PATH))
        {
            // JsonLoadFile popola l'oggetto esistente. NON restituisce
            // un nuovo oggetto. I campi presenti nel JSON sovrascrivono i valori predefiniti;
            // i campi mancanti dal JSON mantengono i loro valori predefiniti.
            JsonFileLoader<MyModConfig>.JsonLoadFile(MYMOD_CONFIG_PATH, cfg);
        }
        else
        {
            // Primo avvio: salva i valori predefiniti così l'admin ha un file da modificare.
            cfg.Save();
            Print(MYMOD_TAG + " No config found, created default at: " + MYMOD_CONFIG_PATH);
        }

        return cfg;
    }

    // -----------------------------------------------------------------------
    // Save - scrive i valori correnti su disco come JSON formattato
    // -----------------------------------------------------------------------
    void Save()
    {
        // Assicura che la directory esista. MakeDirectory è sicuro da chiamare
        // anche se la directory esiste già.
        if (!FileExist(MYMOD_CONFIG_DIR))
        {
            MakeDirectory(MYMOD_CONFIG_DIR);
        }

        // JsonSaveFile scrive tutti i campi come oggetto JSON.
        // Il file viene sovrascritto interamente -- non c'è unione.
        JsonFileLoader<MyModConfig>.JsonSaveFile(MYMOD_CONFIG_PATH, this);
    }
};
```

Il `config.json` risultante su disco appare così:

```json
{
    "Enabled": true,
    "UpdateInterval": 5.0,
    "MaxItems": 100,
    "Mode": 2,
    "WelcomeMessage": "Welcome to the server!",
    "WelcomeAsNotification": true,
    "DebugLogging": false
}
```

Gli admin modificano questo file, riavviano il server, e i nuovi valori hanno effetto.

---

## Definizioni RPC (3_Game)

Posizionale in `Scripts/3_Game/MyMod/MyModRPC.c`.

RPC (Remote Procedure Call) è il modo in cui client e server comunicano in DayZ. Questo file definisce i nomi delle rotte e fornisce metodi helper per la registrazione.

```c
// ==========================================================================
// MyModRPC.c - Definizioni rotte RPC e helper
// Layer 3_Game: le costanti dei nomi delle rotte devono essere disponibili ovunque.
//
// COME FUNZIONA L'RPC IN DAYZ:
//   Il motore fornisce ScriptRPC e OnRPC per inviare/ricevere dati.
//   Chiami GetGame().RPCSingleParam() o crei un ScriptRPC, scrivi
//   i dati al suo interno e lo invii. Il ricevitore legge i dati nello stesso ordine.
//
//   DayZ usa ID RPC interi. Per evitare collisioni tra mod, ogni
//   mod dovrebbe scegliere un range di ID unico o usare un sistema di routing a stringhe.
//   Questo template usa un singolo ID intero unico con un prefisso stringa
//   per identificare quale gestore dovrebbe processare ogni messaggio.
//
// PATTERN:
//   1. Il client vuole dati -> invia RPC di richiesta al server
//   2. Il server elabora  -> invia RPC di risposta al client
//   3. Il client riceve   -> aggiorna UI o stato
// ==========================================================================

// ---------------------------------------------------------------------------
// ID RPC - scegli un numero unico improbabile da collidere con altri mod.
// Controlla la wiki della community DayZ per i range comunemente usati.
// Gli RPC built-in del motore usano numeri bassi (0-1000).
// Convenzione: usa un numero a 5 cifre basato sull'hash del nome del tuo mod.
// ---------------------------------------------------------------------------
const int MYMOD_RPC_ID = 74291;

// ---------------------------------------------------------------------------
// Nomi Rotte RPC - identificatori stringa per ogni endpoint RPC.
// Usare costanti previene errori di battitura e abilita la ricerca nell'IDE.
// ---------------------------------------------------------------------------
const string MYMOD_RPC_CONFIG_SYNC     = "MyMod:ConfigSync";
const string MYMOD_RPC_WELCOME         = "MyMod:Welcome";
const string MYMOD_RPC_PLAYER_DATA     = "MyMod:PlayerData";
const string MYMOD_RPC_UI_REQUEST      = "MyMod:UIRequest";
const string MYMOD_RPC_UI_RESPONSE     = "MyMod:UIResponse";

// ---------------------------------------------------------------------------
// MyModRPCHelper - classe di utilità statica per inviare RPC
// Avvolge il boilerplate di creare un ScriptRPC, scrivere la rotta
// stringa, scrivere il payload, e chiamare Send().
// ---------------------------------------------------------------------------
class MyModRPCHelper
{
    // Invia un messaggio stringa dal server a un client specifico.
    // identity: il giocatore target. null = broadcast a tutti.
    // routeName: quale gestore dovrebbe processare questo (ad esempio, MYMOD_RPC_WELCOME).
    // message: il payload stringa.
    static void SendStringToClient(PlayerIdentity identity, string routeName, string message)
    {
        // Crea l'oggetto RPC. Questa è la busta.
        ScriptRPC rpc = new ScriptRPC();

        // Scrivi prima il nome della rotta. Il ricevitore legge questo per decidere
        // quale gestore chiamare. Scrivi/leggi sempre nello stesso ordine.
        rpc.Write(routeName);

        // Scrivi i dati del payload.
        rpc.Write(message);

        // Invia al client. Parametri:
        //   null    = nessun oggetto target (l'entità giocatore non è necessaria per RPC personalizzati)
        //   MYMOD_RPC_ID = il nostro canale RPC unico
        //   true    = consegna garantita (simile a TCP). Usa false per aggiornamenti frequenti.
        //   identity = client target. null farebbe broadcast a TUTTI i client.
        rpc.Send(null, MYMOD_RPC_ID, true, identity);
    }

    // Invia una richiesta dal client al server (nessun payload, solo la rotta).
    static void SendRequestToServer(string routeName)
    {
        ScriptRPC rpc = new ScriptRPC();
        rpc.Write(routeName);
        // Quando si invia AL server, identity è null (il server non ha PlayerIdentity).
        // guaranteed = true assicura che il messaggio arrivi.
        rpc.Send(null, MYMOD_RPC_ID, true, null);
    }
};
```

---

## Manager Singleton (4_World)

Posizionalo in `Scripts/4_World/MyMod/MyModManager.c`.

Questo è il cervello centrale del tuo mod lato server. Possiede la configurazione, processa gli RPC, e esegue aggiornamenti periodici.

```c
// ==========================================================================
// MyModManager.c - Manager singleton lato server
// Layer 4_World: può referenziare tipi di 3_Game (config, costanti, RPC).
//
// PERCHÉ un singleton:
//   Il manager necessita di esattamente un'istanza che persiste per l'intera
//   missione. Istanze multiple causerebbero elaborazione duplicata e
//   stato conflittuale. Il pattern singleton garantisce un'istanza
//   e fornisce accesso globale tramite GetInstance().
//
// CICLO DI VITA:
//   1. MissionServer.OnInit() chiama MyModManager.GetInstance().Init()
//   2. Il manager carica la config, registra gli RPC, avvia i timer
//   3. Il manager processa gli eventi durante il gameplay
//   4. MissionServer.OnMissionFinish() chiama MyModManager.Cleanup()
//   5. Il singleton viene distrutto, tutti i riferimenti vengono rilasciati
// ==========================================================================

class MyModManager
{
    // La singola istanza. 'ref' significa che questa classe POSSIEDE l'oggetto.
    // Quando s_Instance è impostato a null, l'oggetto viene distrutto.
    private static ref MyModManager s_Instance;

    // Configurazione caricata da disco.
    // 'ref' perché il manager possiede il ciclo di vita dell'oggetto config.
    protected ref MyModConfig m_Config;

    // Tempo accumulato dall'ultimo tick di aggiornamento (secondi).
    protected float m_TimeSinceUpdate;

    // Tiene traccia se Init() è stato chiamato con successo.
    protected bool m_Initialized;

    // -----------------------------------------------------------------------
    // Accesso singleton
    // -----------------------------------------------------------------------

    static MyModManager GetInstance()
    {
        if (!s_Instance)
        {
            s_Instance = new MyModManager();
        }
        return s_Instance;
    }

    // Chiama questo alla fine della missione per distruggere il singleton e liberare memoria.
    // Impostare s_Instance a null attiva il distruttore.
    static void Cleanup()
    {
        s_Instance = null;
    }

    // -----------------------------------------------------------------------
    // Ciclo di vita
    // -----------------------------------------------------------------------

    // Chiamato una volta da MissionServer.OnInit().
    void Init()
    {
        if (m_Initialized) return;

        // Carica la config da disco (o crea i valori predefiniti al primo avvio).
        m_Config = MyModConfig.Load();

        if (!m_Config.Enabled)
        {
            Print(MYMOD_TAG + " Mod is DISABLED in config. Skipping initialization.");
            return;
        }

        // Resetta il timer di aggiornamento.
        m_TimeSinceUpdate = 0;

        m_Initialized = true;

        Print(MYMOD_TAG + " Manager initialized (v" + MYMOD_VERSION + ")");

        if (m_Config.DebugLogging)
        {
            Print(MYMOD_TAG + " Debug logging enabled");
            Print(MYMOD_TAG + " Update interval: " + m_Config.UpdateInterval.ToString() + "s");
            Print(MYMOD_TAG + " Max items: " + m_Config.MaxItems.ToString());
        }
    }

    // Chiamato ogni frame da MissionServer.OnUpdate().
    // timeslice è i secondi trascorsi dall'ultimo frame.
    void OnUpdate(float timeslice)
    {
        if (!m_Initialized || !m_Config.Enabled) return;

        // Accumula il tempo ed elabora solo all'intervallo configurato.
        // Questo previene l'esecuzione di logica costosa ad ogni singolo frame.
        m_TimeSinceUpdate += timeslice;
        if (m_TimeSinceUpdate < m_Config.UpdateInterval) return;
        m_TimeSinceUpdate = 0;

        // --- La logica di aggiornamento periodico va qui ---
        // Esempio: iterare sulle entità tracciate, controllare condizioni, ecc.
        if (m_Config.DebugLogging)
        {
            Print(MYMOD_TAG + " Periodic update tick");
        }
    }

    // Chiamato quando la missione finisce (arresto o riavvio del server).
    void Shutdown()
    {
        if (!m_Initialized) return;

        Print(MYMOD_TAG + " Manager shutting down");

        // Salva qualsiasi stato runtime se necessario.
        // m_Config.Save();

        m_Initialized = false;
    }

    // -----------------------------------------------------------------------
    // Gestori RPC
    // -----------------------------------------------------------------------

    // Chiamato quando un client richiede dati UI.
    // sender: il giocatore che ha inviato la richiesta.
    // ctx: lo stream di dati (già dopo il nome della rotta).
    void OnUIRequest(PlayerIdentity sender, ParamsReadContext ctx)
    {
        if (!sender) return;

        if (m_Config.DebugLogging)
        {
            Print(MYMOD_TAG + " UI data requested by: " + sender.GetName());
        }

        // Costruisci i dati di risposta e rinviali.
        // In un mod reale, raccoglieresti dati effettivi qui.
        string responseData = "Items: " + m_Config.MaxItems.ToString();
        MyModRPCHelper.SendStringToClient(sender, MYMOD_RPC_UI_RESPONSE, responseData);
    }

    // Chiamato quando un giocatore si connette. Invia il messaggio di benvenuto se configurato.
    void OnPlayerConnected(PlayerIdentity identity)
    {
        if (!m_Initialized || !m_Config.Enabled) return;
        if (!identity) return;

        // Invia il messaggio di benvenuto se configurato.
        if (m_Config.WelcomeMessage != "")
        {
            MyModRPCHelper.SendStringToClient(identity, MYMOD_RPC_WELCOME, m_Config.WelcomeMessage);

            if (m_Config.DebugLogging)
            {
                Print(MYMOD_TAG + " Sent welcome to: " + identity.GetName());
            }
        }
    }

    // -----------------------------------------------------------------------
    // Accessori
    // -----------------------------------------------------------------------

    MyModConfig GetConfig()
    {
        return m_Config;
    }

    bool IsInitialized()
    {
        return m_Initialized;
    }
};
```

---

## Gestore Eventi Giocatore (4_World)

Posizionalo in `Scripts/4_World/MyMod/MyModPlayerHandler.c`.

Questo usa il pattern `modded class` per agganciarsi all'entità vanilla `PlayerBase` e rilevare eventi di connessione/disconnessione.

```c
// ==========================================================================
// MyModPlayerHandler.c - Hook del ciclo di vita del giocatore
// Layer 4_World: modded PlayerBase per intercettare connessione/disconnessione.
//
// PERCHÉ modded class:
//   DayZ non ha un callback evento "giocatore connesso". Il pattern standard
//   è sovrascrivere metodi su MissionServer (per nuove connessioni)
//   o agganciarsi a PlayerBase (per eventi a livello di entità come la morte).
//   Usiamo qui modded PlayerBase per dimostrare hook a livello di entità.
//
// IMPORTANTE:
//   Chiama sempre super.NomeMetodo() per primo nelle override. Non farlo
//   rompe la catena di comportamento vanilla e altri mod che sovrascrivono
//   anch'essi lo stesso metodo.
// ==========================================================================

modded class PlayerBase
{
    // Tiene traccia se abbiamo inviato l'evento init per questo giocatore.
    // Questo previene elaborazione duplicata se Init() viene chiamato più volte.
    protected bool m_MyModPlayerReady;

    // -----------------------------------------------------------------------
    // Chiamato dopo che l'entità giocatore è completamente creata e replicata.
    // Sul server, è qui che il giocatore è "pronto" a ricevere RPC.
    // -----------------------------------------------------------------------
    override void Init()
    {
        super.Init();

        // Esegui solo sul server. GetGame().IsServer() restituisce true su
        // server dedicati e sull'host di un listen server.
        if (!GetGame().IsServer()) return;

        // Guardia contro doppia inizializzazione.
        if (m_MyModPlayerReady) return;
        m_MyModPlayerReady = true;

        // Ottieni l'identità di rete del giocatore.
        // Sul server, GetIdentity() restituisce l'oggetto PlayerIdentity
        // contenente il nome del giocatore, Steam ID (PlainId) e UID.
        PlayerIdentity identity = GetIdentity();
        if (!identity) return;

        // Notifica il manager che un giocatore si è connesso.
        MyModManager mgr = MyModManager.GetInstance();
        if (mgr)
        {
            mgr.OnPlayerConnected(identity);
        }
    }
};
```

---

## Hook Missione: Server (5_Mission)

Posizionalo in `Scripts/5_Mission/MyMod/MyModMissionServer.c`.

Questo si aggancia a `MissionServer` per inizializzare e chiudere il mod lato server.

```c
// ==========================================================================
// MyModMissionServer.c - Hook di missione lato server
// Layer 5_Mission: ultimo a caricarsi, può referenziare tutti i layer inferiori.
//
// PERCHÉ modded MissionServer:
//   MissionServer è il punto di ingresso per la logica lato server. Il suo OnInit()
//   viene eseguito una volta quando la missione inizia (avvio del server). OnMissionFinish()
//   viene eseguito quando il server si arresta o si riavvia. Questi sono i posti corretti
//   per configurare e dismettere i sistemi del tuo mod.
//
// ORDINE DEL CICLO DI VITA:
//   1. Il motore carica tutti i layer di script (3_Game -> 4_World -> 5_Mission)
//   2. Il motore crea l'istanza di MissionServer
//   3. OnInit() viene chiamato -> inizializza i tuoi sistemi qui
//   4. OnMissionStart() viene chiamato -> il mondo è pronto, i giocatori possono entrare
//   5. OnUpdate() viene chiamato ogni frame
//   6. OnMissionFinish() viene chiamato -> il server si sta arrestando
// ==========================================================================

modded class MissionServer
{
    // -----------------------------------------------------------------------
    // Inizializzazione
    // -----------------------------------------------------------------------
    override void OnInit()
    {
        // Chiama SEMPRE super per primo. Altri mod nella catena dipendono da questo.
        super.OnInit();

        // Inizializza il singleton del manager. Questo carica la config da disco,
        // registra i gestori RPC e prepara il mod per l'operazione.
        MyModManager.GetInstance().Init();

        Print(MYMOD_TAG + " Server mission initialized");
    }

    // -----------------------------------------------------------------------
    // Aggiornamento per-frame
    // -----------------------------------------------------------------------
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);

        // Delega al manager. Il manager gestisce il proprio rate
        // limiting (UpdateInterval dalla config) quindi questo è leggero.
        MyModManager mgr = MyModManager.GetInstance();
        if (mgr)
        {
            mgr.OnUpdate(timeslice);
        }
    }

    // -----------------------------------------------------------------------
    // Connessione giocatore - dispatch RPC del server
    // Chiamato dal motore quando un client invia un RPC al server.
    // -----------------------------------------------------------------------
    override void OnRPC(PlayerIdentity sender, Object target, int rpc_type, ParamsReadContext ctx)
    {
        super.OnRPC(sender, target, rpc_type, ctx);

        // Gestisci solo il nostro ID RPC. Tutti gli altri RPC passano attraverso.
        if (rpc_type != MYMOD_RPC_ID) return;

        // Leggi il nome della rotta (prima stringa scritta dal mittente).
        string routeName;
        if (!ctx.Read(routeName)) return;

        // Despaccia al gestore corretto in base al nome della rotta.
        MyModManager mgr = MyModManager.GetInstance();
        if (!mgr) return;

        if (routeName == MYMOD_RPC_UI_REQUEST)
        {
            mgr.OnUIRequest(sender, ctx);
        }
        // Aggiungi più rotte qui man mano che il tuo mod cresce:
        // else if (routeName == MYMOD_RPC_SOME_OTHER)
        // {
        //     mgr.OnSomeOther(sender, ctx);
        // }
    }

    // -----------------------------------------------------------------------
    // Shutdown
    // -----------------------------------------------------------------------
    override void OnMissionFinish()
    {
        // Chiudi il manager prima di chiamare super.
        // Questo assicura che la nostra pulizia venga eseguita prima che il motore
        // smantelli l'infrastruttura della missione.
        MyModManager mgr = MyModManager.GetInstance();
        if (mgr)
        {
            mgr.Shutdown();
        }

        // Distruggi il singleton per liberare memoria e prevenire stato stantio
        // se la missione si riavvia (ad esempio, riavvio del server senza uscita dal processo).
        MyModManager.Cleanup();

        Print(MYMOD_TAG + " Server mission finished");

        super.OnMissionFinish();
    }
};
```

---

## Hook Missione: Client (5_Mission)

Posizionalo in `Scripts/5_Mission/MyMod/MyModMissionClient.c`.

Questo si aggancia a `MissionGameplay` per l'inizializzazione lato client, la gestione degli input e la ricezione degli RPC.

```c
// ==========================================================================
// MyModMissionClient.c - Hook di missione lato client
// Layer 5_Mission.
//
// PERCHÉ MissionGameplay:
//   Sul client, MissionGameplay è la classe missione attiva durante
//   il gameplay. Riceve OnUpdate() ogni frame (per il polling dell'input)
//   e OnRPC() per i messaggi in arrivo dal server.
//
// NOTA SUI LISTEN SERVER:
//   Su un listen server (host + gioca), SIA MissionServer che
//   MissionGameplay sono attivi. Il tuo codice client verrà eseguito insieme
//   al codice server. Proteggi con GetGame().IsClient() o GetGame().IsServer()
//   se hai bisogno di logica specifica per lato.
// ==========================================================================

modded class MissionGameplay
{
    // Riferimento al pannello UI. null quando chiuso.
    protected ref MyModUI m_MyModPanel;

    // Tiene traccia dello stato di inizializzazione.
    protected bool m_MyModInitialized;

    // -----------------------------------------------------------------------
    // Inizializzazione
    // -----------------------------------------------------------------------
    override void OnInit()
    {
        super.OnInit();

        m_MyModInitialized = true;

        Print(MYMOD_TAG + " Client mission initialized");
    }

    // -----------------------------------------------------------------------
    // Aggiornamento per-frame: polling input e gestione UI
    // -----------------------------------------------------------------------
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);

        if (!m_MyModInitialized) return;

        // Fai polling per il keybind definito in Inputs.xml.
        // GetUApi() restituisce l'API UserActions.
        // GetInputByName() cerca l'azione per il nome in Inputs.xml.
        // LocalPress() restituisce true nel frame in cui il tasto viene premuto.
        UAInput panelInput = GetUApi().GetInputByName("UAMyModPanel");
        if (panelInput && panelInput.LocalPress())
        {
            TogglePanel();
        }
    }

    // -----------------------------------------------------------------------
    // Ricevitore RPC: gestisce i messaggi dal server
    // -----------------------------------------------------------------------
    override void OnRPC(PlayerIdentity sender, Object target, int rpc_type, ParamsReadContext ctx)
    {
        super.OnRPC(sender, target, rpc_type, ctx);

        // Gestisci solo il nostro ID RPC.
        if (rpc_type != MYMOD_RPC_ID) return;

        // Leggi il nome della rotta.
        string routeName;
        if (!ctx.Read(routeName)) return;

        // Despaccia in base alla rotta.
        if (routeName == MYMOD_RPC_WELCOME)
        {
            string welcomeMsg;
            if (ctx.Read(welcomeMsg))
            {
                // Mostra il messaggio di benvenuto al giocatore.
                // GetGame().GetMission().OnEvent() può mostrare notifiche,
                // oppure puoi usare una UI personalizzata. Per semplicità, usiamo la chat.
                GetGame().Chat(welcomeMsg, "");
                Print(MYMOD_TAG + " Welcome message: " + welcomeMsg);
            }
        }
        else if (routeName == MYMOD_RPC_UI_RESPONSE)
        {
            string responseData;
            if (ctx.Read(responseData))
            {
                // Aggiorna il pannello UI con i dati ricevuti.
                if (m_MyModPanel)
                {
                    m_MyModPanel.SetData(responseData);
                }
            }
        }
    }

    // -----------------------------------------------------------------------
    // Toggle del pannello UI
    // -----------------------------------------------------------------------
    protected void TogglePanel()
    {
        if (m_MyModPanel && m_MyModPanel.IsOpen())
        {
            m_MyModPanel.Close();
            m_MyModPanel = null;
        }
        else
        {
            // Apri solo se il giocatore è vivo e nessun altro menù è mostrato.
            PlayerBase player = PlayerBase.Cast(GetGame().GetPlayer());
            if (!player || !player.IsAlive()) return;

            UIManager uiMgr = GetGame().GetUIManager();
            if (uiMgr && uiMgr.GetMenu()) return;

            m_MyModPanel = new MyModUI();
            m_MyModPanel.Open();

            // Richiedi dati freschi dal server.
            MyModRPCHelper.SendRequestToServer(MYMOD_RPC_UI_REQUEST);
        }
    }

    // -----------------------------------------------------------------------
    // Shutdown
    // -----------------------------------------------------------------------
    override void OnMissionFinish()
    {
        // Chiudi e distruggi il pannello UI se aperto.
        if (m_MyModPanel)
        {
            m_MyModPanel.Close();
            m_MyModPanel = null;
        }

        m_MyModInitialized = false;

        Print(MYMOD_TAG + " Client mission finished");

        super.OnMissionFinish();
    }
};
```

---

## Script Pannello UI (5_Mission)

Posizionalo in `Scripts/5_Mission/MyMod/MyModUI.c`.

Questo script pilota il pannello UI definito nel file `.layout`. Trova i riferimenti ai widget, li popola con dati e gestisce apertura/chiusura.

```c
// ==========================================================================
// MyModUI.c - Controller del pannello UI
// Layer 5_Mission: può referenziare tutti i layer inferiori.
//
// COME FUNZIONA LA UI DI DAYZ:
//   1. Un file .layout definisce la gerarchia dei widget (come HTML).
//   2. Una classe script carica il layout, trova i widget per nome, e
//      li manipola (imposta testo, mostra/nascondi, risponde ai click).
//   3. Lo script mostra/nasconde il widget radice e gestisce il focus dell'input.
//
// CICLO DI VITA DEL WIDGET:
//   GetGame().GetWorkspace().CreateWidgets() carica il file layout e
//   restituisce il widget radice. Poi usi FindAnyWidget() per ottenere
//   riferimenti ai widget figli nominati. Quando hai finito, chiama widget.Unlink()
//   per distruggere l'intero albero dei widget.
// ==========================================================================

class MyModUI
{
    // Widget radice del pannello (caricato dal .layout).
    protected ref Widget m_Root;

    // Widget figli nominati.
    protected TextWidget m_TitleText;
    protected TextWidget m_DataText;
    protected TextWidget m_VersionText;
    protected ButtonWidget m_CloseButton;

    // Tracciamento dello stato.
    protected bool m_IsOpen;

    // -----------------------------------------------------------------------
    // Costruttore: carica il layout e trova i riferimenti ai widget
    // -----------------------------------------------------------------------
    void MyModUI()
    {
        // CreateWidgets carica il file .layout e istanzia tutti i widget.
        // Il percorso è relativo alla radice del mod (come i percorsi in config.cpp).
        m_Root = GetGame().GetWorkspace().CreateWidgets(
            "MyProfessionalMod/Scripts/GUI/layouts/MyModPanel.layout"
        );

        // Inizialmente nascosto fino a quando Open() viene chiamato.
        if (m_Root)
        {
            m_Root.Show(false);

            // Trova i widget nominati. Questi nomi DEVONO corrispondere ai nomi dei widget
            // nel file .layout esattamente (sensibile alle maiuscole).
            m_TitleText   = TextWidget.Cast(m_Root.FindAnyWidget("TitleText"));
            m_DataText    = TextWidget.Cast(m_Root.FindAnyWidget("DataText"));
            m_VersionText = TextWidget.Cast(m_Root.FindAnyWidget("VersionText"));
            m_CloseButton = ButtonWidget.Cast(m_Root.FindAnyWidget("CloseButton"));

            // Imposta il contenuto statico.
            if (m_TitleText)
                m_TitleText.SetText("My Professional Mod");

            if (m_VersionText)
                m_VersionText.SetText("v" + MYMOD_VERSION);
        }
    }

    // -----------------------------------------------------------------------
    // Open: mostra il pannello e cattura l'input
    // -----------------------------------------------------------------------
    void Open()
    {
        if (!m_Root) return;

        m_Root.Show(true);
        m_IsOpen = true;

        // Blocca i controlli del giocatore così WASD non muove il personaggio
        // mentre il pannello è aperto. Questo mostra un cursore.
        GetGame().GetMission().PlayerControlDisable(INPUT_EXCLUDE_ALL);
        GetGame().GetUIManager().ShowUICursor(true);

        Print(MYMOD_TAG + " UI panel opened");
    }

    // -----------------------------------------------------------------------
    // Close: nascondi il pannello e rilascia l'input
    // -----------------------------------------------------------------------
    void Close()
    {
        if (!m_Root) return;

        m_Root.Show(false);
        m_IsOpen = false;

        // Riabilita i controlli del giocatore.
        GetGame().GetMission().PlayerControlEnable(true);
        GetGame().GetUIManager().ShowUICursor(false);

        Print(MYMOD_TAG + " UI panel closed");
    }

    // -----------------------------------------------------------------------
    // Aggiornamento dati: chiamato quando il server invia dati UI
    // -----------------------------------------------------------------------
    void SetData(string data)
    {
        if (m_DataText)
        {
            m_DataText.SetText(data);
        }
    }

    // -----------------------------------------------------------------------
    // Interrogazione stato
    // -----------------------------------------------------------------------
    bool IsOpen()
    {
        return m_IsOpen;
    }

    // -----------------------------------------------------------------------
    // Distruttore: pulisci l'albero dei widget
    // -----------------------------------------------------------------------
    void ~MyModUI()
    {
        // Unlink distrugge il widget radice e tutti i suoi figli.
        // Questo libera la memoria usata dall'albero dei widget.
        if (m_Root)
        {
            m_Root.Unlink();
        }
    }
};
```

---

## File Layout

Posizionalo in `Scripts/GUI/layouts/MyModPanel.layout`.

Questo definisce la struttura visuale del pannello UI. I layout di DayZ usano un formato di testo personalizzato (non XML).

```
// ==========================================================================
// MyModPanel.layout - Struttura del pannello UI
//
// REGOLE DI DIMENSIONAMENTO:
//   hexactsize 1 + vexactsize 1 = la dimensione è in pixel (ad esempio, size 400 300)
//   hexactsize 0 + vexactsize 0 = la dimensione è proporzionale (da 0.0 a 1.0)
//   halign/valign controllano il punto di ancoraggio:
//     left_ref/top_ref     = ancorato al bordo sinistro/superiore del genitore
//     center_ref           = centrato nel genitore
//     right_ref/bottom_ref = ancorato al bordo destro/inferiore del genitore
//
// IMPORTANTE:
//   - Non usare mai dimensioni negative. Usa allineamento e posizione invece.
//   - I nomi dei widget devono corrispondere alle chiamate FindAnyWidget() nello script esattamente.
//   - 'ignorepointer 1' significa che il widget non riceve click del mouse.
//   - 'scriptclass' collega un widget a una classe script per la gestione degli eventi.
// ==========================================================================

// Pannello radice: centrato sullo schermo, 400x300 pixel, sfondo semi-trasparente.
PanelWidgetClass MyModPanelRoot {
 position 0 0
 size 400 300
 halign center_ref
 valign center_ref
 hexactpos 1
 vexactpos 1
 hexactsize 1
 vexactsize 1
 color 0.1 0.1 0.12 0.92
 priority 100
 {
  // Barra del titolo: larghezza piena, 36px di altezza, in cima.
  PanelWidgetClass TitleBar {
   position 0 0
   size 1 36
   hexactpos 1
   vexactpos 1
   hexactsize 0
   vexactsize 1
   color 0.15 0.15 0.18 1
   {
    // Testo del titolo: allineato a sinistra con padding.
    TextWidgetClass TitleText {
     position 12 0
     size 300 36
     hexactpos 1
     vexactpos 1
     hexactsize 1
     vexactsize 1
     valign center_ref
     ignorepointer 1
     text "My Mod"
     font "gui/fonts/metron2"
     "exact size" 16
     color 1 1 1 0.9
    }
    // Testo della versione: lato destro della barra del titolo.
    TextWidgetClass VersionText {
     position 0 0
     size 80 36
     halign right_ref
     hexactpos 1
     vexactpos 1
     hexactsize 1
     vexactsize 1
     valign center_ref
     ignorepointer 1
     text "v1.0.0"
     font "gui/fonts/metron2"
     "exact size" 12
     color 0.6 0.6 0.6 0.8
    }
   }
  }
  // Area contenuto: sotto la barra del titolo, riempie lo spazio rimanente.
  PanelWidgetClass ContentArea {
   position 0 40
   size 380 200
   halign center_ref
   hexactpos 1
   vexactpos 1
   hexactsize 1
   vexactsize 1
   color 0 0 0 0
   {
    // Testo dati: dove vengono visualizzati i dati del server.
    TextWidgetClass DataText {
     position 12 12
     size 356 160
     hexactpos 1
     vexactpos 1
     hexactsize 1
     vexactsize 1
     ignorepointer 1
     text "Waiting for data..."
     font "gui/fonts/metron2"
     "exact size" 14
     color 0.85 0.85 0.85 1
    }
   }
  }
  // Pulsante chiudi: angolo in basso a destra.
  ButtonWidgetClass CloseButton {
   position 0 0
   size 100 32
   halign right_ref
   valign bottom_ref
   hexactpos 1
   vexactpos 1
   hexactsize 1
   vexactsize 1
   text "Close"
   font "gui/fonts/metron2"
   "exact size" 14
  }
 }
}
```

---

## stringtable.csv

Posizionalo in `Scripts/stringtable.csv`.

Questo fornisce la localizzazione per tutto il testo visibile al giocatore. Il motore legge la colonna corrispondente alla lingua di gioco del giocatore. La colonna `original` è il fallback.

DayZ supporta 13 colonne di lingua. Ogni riga deve avere tutte le 13 colonne (usa il testo inglese come segnaposto per le lingue che non traduci).

```csv
"Language","original","english","czech","german","russian","polish","hungarian","italian","spanish","french","chinese","japanese","portuguese","chinesesimp",
"STR_MYMOD_INPUT_GROUP","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod","My Mod",
"STR_MYMOD_INPUT_PANEL","Open Panel","Open Panel","Otevrit Panel","Panel offnen","Otkryt Panel","Otworz Panel","Panel megnyitasa","Apri Pannello","Abrir Panel","Ouvrir Panneau","Open Panel","Open Panel","Abrir Painel","Open Panel",
"STR_MYMOD_TITLE","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod","My Professional Mod",
"STR_MYMOD_CLOSE","Close","Close","Zavrit","Schliessen","Zakryt","Zamknij","Bezaras","Chiudi","Cerrar","Fermer","Close","Close","Fechar","Close",
"STR_MYMOD_WELCOME","Welcome!","Welcome!","Vitejte!","Willkommen!","Dobro pozhalovat!","Witaj!","Udvozoljuk!","Benvenuto!","Bienvenido!","Bienvenue!","Welcome!","Welcome!","Bem-vindo!","Welcome!",
```

**Importante:** Ogni riga deve terminare con una virgola finale dopo l'ultima colonna di lingua. Questo è un requisito del parser CSV di DayZ.

---

## Inputs.xml

Posizionalo in `Scripts/Inputs.xml`.

Questo definisce i keybind personalizzati che appaiono nel menù Opzioni > Controlli del gioco. Il campo `inputs` in `config.cpp` CfgMods deve puntare a questo file.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<!--
    Inputs.xml - Definizioni keybind personalizzati

    STRUTTURA:
    - <actions>:  dichiara i nomi delle azioni di input e le loro stringhe di visualizzazione
    - <sorting>:  raggruppa le azioni sotto una categoria nel menù Controlli
    - <preset>:   imposta il binding tasto predefinito

    CONVENZIONE DI NAMING:
    - I nomi delle azioni iniziano con "UA" (User Action) seguito dal prefisso del tuo mod.
    - L'attributo "loc" referenzia una chiave stringa da stringtable.csv.

    NOMI DEI TASTI:
    - Tastiera: kA fino a kZ, k0-k9, kInsert, kHome, kEnd, kDelete,
      kNumpad0-kNumpad9, kF1-kF12, kLControl, kRControl, kLShift, kRShift,
      kLAlt, kRAlt, kSpace, kReturn, kBack, kTab, kEscape
    - Mouse: mouse1 (sinistro), mouse2 (destro), mouse3 (centrale)
    - Combinazioni di tasti: usa l'elemento <combo> con più figli <btn>
-->
<modded_inputs>
    <inputs>
        <!-- Dichiara l'azione di input. -->
        <actions>
            <input name="UAMyModPanel" loc="STR_MYMOD_INPUT_PANEL" />
        </actions>

        <!-- Raggruppa sotto una categoria in Opzioni > Controlli. -->
        <!-- Il "name" è un ID interno; "loc" è il nome visualizzato da stringtable. -->
        <sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
            <input name="UAMyModPanel"/>
        </sorting>
    </inputs>

    <!-- Preset tasto predefinito. I giocatori possono riconfigurare in Opzioni > Controlli. -->
    <preset>
        <!-- Associa al tasto Home per impostazione predefinita. -->
        <input name="UAMyModPanel">
            <btn name="kHome"/>
        </input>

        <!--
        ESEMPIO COMBINAZIONE TASTI (decommenta per usare):
        Questo assocerebbe a Ctrl+H invece di un singolo tasto.
        <input name="UAMyModPanel">
            <combo>
                <btn name="kLControl"/>
                <btn name="kH"/>
            </combo>
        </input>
        -->
    </preset>
</modded_inputs>
```

---

## Script di Build

Posizionalo come `build.bat` nella radice del mod.

Questo file batch automatizza l'impacchettamento PBO usando Addon Builder da DayZ Tools.

```batch
@echo off
REM ==========================================================================
REM build.bat - Impacchettamento PBO automatizzato per MyProfessionalMod
REM
REM COSA FA QUESTO:
REM   1. Impacchetta la cartella Scripts/ in un file PBO
REM   2. Posiziona il PBO nella cartella mod distribuibile @mod
REM   3. Copia mod.cpp nella cartella distribuibile
REM
REM PREREQUISITI:
REM   - DayZ Tools installato tramite Steam
REM   - Sorgente del mod in P:\MyProfessionalMod\
REM
REM UTILIZZO:
REM   Fai doppio click su questo file o esegui da riga di comando: build.bat
REM ==========================================================================

REM --- Configurazione: aggiorna questi percorsi per corrispondere alla tua installazione ---

REM Percorso a DayZ Tools (controlla il percorso della tua libreria Steam).
set DAYZ_TOOLS=C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools

REM Cartella sorgente: la directory Scripts che viene impacchettata nel PBO.
set SOURCE=P:\MyProfessionalMod\Scripts

REM Cartella di output: dove va il PBO impacchettato.
set OUTPUT=P:\@MyProfessionalMod\addons

REM Prefisso: il percorso virtuale dentro il PBO. Deve corrispondere ai percorsi
REM in config.cpp (ad esempio, "MyProfessionalMod/Scripts/3_Game" deve risolversi).
set PREFIX=MyProfessionalMod\Scripts

REM --- Passi di Build ---

echo ============================================
echo  Building MyProfessionalMod
echo ============================================

REM Crea la directory di output se non esiste.
if not exist "%OUTPUT%" mkdir "%OUTPUT%"

REM Esegui Addon Builder.
REM   -clear  = rimuovi il vecchio PBO prima di impacchettare
REM   -prefix = imposta il prefisso PBO (necessario perché i percorsi degli script si risolvano)
echo Packing PBO...
"%DAYZ_TOOLS%\Bin\AddonBuilder\AddonBuilder.exe" "%SOURCE%" "%OUTPUT%" -prefix=%PREFIX% -clear

REM Controlla se Addon Builder ha avuto successo.
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRORE: Impacchettamento PBO fallito! Controlla l'output sopra per i dettagli.
    echo Cause comuni:
    echo   - Il percorso a DayZ Tools è sbagliato
    echo   - La cartella sorgente non esiste
    echo   - Un file .c ha un errore di sintassi che impedisce l'impacchettamento
    pause
    exit /b 1
)

REM Copia mod.cpp nella cartella distribuibile.
echo Copying mod.cpp...
copy /Y "P:\MyProfessionalMod\mod.cpp" "P:\@MyProfessionalMod\mod.cpp" >nul

echo.
echo ============================================
echo  Build completata!
echo  Output: P:\@MyProfessionalMod\
echo ============================================
echo.
echo Per testare con file patching (nessun PBO necessario):
echo   DayZDiag_x64.exe -mod=P:\MyProfessionalMod -filePatching
echo.
echo Per testare con il PBO costruito:
echo   DayZDiag_x64.exe -mod=P:\@MyProfessionalMod
echo.
pause
```

---

## Guida alla Personalizzazione

Quando usi questo template per il tuo mod, devi rinominare ogni occorrenza dei nomi segnaposto. Ecco una checklist completa.

### Step 1: Scegli i Tuoi Nomi

Decidi questi identificatori prima di fare qualsiasi modifica:

| Identificatore | Esempio | Regole |
|----------------|---------|--------|
| **Nome cartella mod** | `MyBountySystem` | Nessuno spazio, PascalCase o underscore |
| **Nome visualizzato** | `"My Bounty System"` | Leggibile, per mod.cpp e config.cpp |
| **Classe CfgPatches** | `MyBountySystem_Scripts` | Deve essere globalmente unico tra tutti i mod |
| **Classe CfgMods** | `MyBountySystem` | Identificatore interno del motore |
| **Prefisso script** | `MyBounty` | Prefisso breve per le classi: `MyBountyManager`, `MyBountyConfig` |
| **Costante tag** | `MYBOUNTY_TAG` | Per i messaggi di log: `"[MyBounty]"` |
| **Define preprocessore** | `MYBOUNTYSYSTEM` | Per la rilevazione cross-mod `#ifdef` |
| **ID RPC** | `58432` | Numero unico a 5 cifre, non usato da altri mod |
| **Nome azione input** | `UAMyBountyPanel` | Inizia con `UA`, unico |

### Step 2: Rinomina File e Cartelle

Rinomina ogni file e cartella che contiene "MyMod" o "MyProfessionalMod":

```
MyProfessionalMod/           -> MyBountySystem/
  Scripts/3_Game/MyMod/      -> Scripts/3_Game/MyBounty/
    MyModConstants.c          -> MyBountyConstants.c
    MyModConfig.c             -> MyBountyConfig.c
    MyModRPC.c                -> MyBountyRPC.c
  Scripts/4_World/MyMod/     -> Scripts/4_World/MyBounty/
    MyModManager.c            -> MyBountyManager.c
    MyModPlayerHandler.c      -> MyBountyPlayerHandler.c
  Scripts/5_Mission/MyMod/   -> Scripts/5_Mission/MyBounty/
    MyModMissionServer.c      -> MyBountyMissionServer.c
    MyModMissionClient.c      -> MyBountyMissionClient.c
    MyModUI.c                 -> MyBountyUI.c
  Scripts/GUI/layouts/
    MyModPanel.layout          -> MyBountyPanel.layout
```

### Step 3: Trova-e-Sostituisci in Ogni File

Esegui queste sostituzioni **in ordine** (stringhe più lunghe per prime per evitare corrispondenze parziali):

| Trova | Sostituisci | File Interessati |
|-------|-------------|------------------|
| `MyProfessionalMod` | `MyBountySystem` | config.cpp, mod.cpp, build.bat, script UI |
| `MyModManager` | `MyBountyManager` | Manager, hook missione, gestore giocatore |
| `MyModConfig` | `MyBountyConfig` | Classe config, manager |
| `MyModConstants` | `MyBountyConstants` | (solo nome file) |
| `MyModRPCHelper` | `MyBountyRPCHelper` | Helper RPC, hook missione |
| `MyModUI` | `MyBountyUI` | Script UI, hook missione client |
| `MyModPanel` | `MyBountyPanel` | File layout, script UI |
| `MyMod_Scripts` | `MyBountySystem_Scripts` | config.cpp CfgPatches |
| `MYMOD_RPC_ID` | `MYBOUNTY_RPC_ID` | Costanti, RPC, hook missione |
| `MYMOD_RPC_` | `MYBOUNTY_RPC_` | Tutte le costanti rotte RPC |
| `MYMOD_TAG` | `MYBOUNTY_TAG` | Costanti, tutti i file che usano il tag di log |
| `MYMOD_CONFIG` | `MYBOUNTY_CONFIG` | Costanti, classe config |
| `MYMOD_VERSION` | `MYBOUNTY_VERSION` | Costanti, script UI |
| `MYMOD` | `MYBOUNTYSYSTEM` | config.cpp defines[] |
| `MyMod` | `MyBounty` | config.cpp classe CfgMods, stringhe rotte RPC |
| `My Mod` | `My Bounty System` | Stringhe nei layout, stringtable |
| `mymod` | `mybounty` | Inputs.xml nome sorting |
| `STR_MYMOD_` | `STR_MYBOUNTY_` | stringtable.csv, Inputs.xml |
| `UAMyMod` | `UAMyBounty` | Inputs.xml, hook missione client |
| `m_MyMod` | `m_MyBounty` | Variabili membro hook missione client |
| `74291` | `58432` | ID RPC (il tuo numero unico scelto) |

### Step 4: Verifica

Dopo la rinomina, fai una ricerca a livello di progetto per "MyMod" e "MyProfessionalMod" per catturare qualsiasi cosa tu abbia dimenticato. Poi compila e testa:

```batch
DayZDiag_x64.exe -mod=P:\MyBountySystem -filePatching
```

Controlla il log degli script per il tuo tag (ad esempio, `[MyBounty]`) per confermare che tutto si è caricato.

---

## Guida all'Espansione delle Funzionalità

Una volta che il tuo mod è in esecuzione, ecco come aggiungere funzionalità comuni.

### Aggiungere un Nuovo Endpoint RPC

**1. Definisci la costante della rotta** in `MyModRPC.c` (3_Game):

```c
const string MYMOD_RPC_BOUNTY_SET = "MyMod:BountySet";
```

**2. Aggiungi il gestore server** in `MyModManager.c` (4_World):

```c
void OnBountySet(PlayerIdentity sender, ParamsReadContext ctx)
{
    // Leggi i parametri scritti dal client.
    string targetName;
    int bountyAmount;
    if (!ctx.Read(targetName)) return;
    if (!ctx.Read(bountyAmount)) return;

    Print(MYMOD_TAG + " Bounty set on " + targetName + ": " + bountyAmount.ToString());
    // ... la tua logica qui ...
}
```

**3. Aggiungi il caso di dispatch** in `MyModMissionServer.c` (5_Mission), dentro `OnRPC()`:

```c
else if (routeName == MYMOD_RPC_BOUNTY_SET)
{
    mgr.OnBountySet(sender, ctx);
}
```

**4. Invia dal client** (ovunque l'azione venga attivata):

```c
ScriptRPC rpc = new ScriptRPC();
rpc.Write(MYMOD_RPC_BOUNTY_SET);
rpc.Write("PlayerName");
rpc.Write(5000);
rpc.Send(null, MYMOD_RPC_ID, true, null);
```

### Aggiungere un Nuovo Campo Config

**1. Aggiungi il campo** in `MyModConfig.c` con un valore predefinito:

```c
// Importo minimo taglia che i giocatori possono impostare.
int MinBountyAmount = 100;
```

Questo è tutto. Il serializzatore JSON raccoglie i campi pubblici automaticamente. I file config esistenti su disco useranno il valore predefinito per il nuovo campo fino a quando l'admin non modifica e salva.

**2. Referenzialo** dal manager:

```c
if (bountyAmount < m_Config.MinBountyAmount)
{
    // Rifiuta: troppo basso.
    return;
}
```

### Aggiungere un Nuovo Pannello UI

**1. Crea il layout** in `Scripts/GUI/layouts/MyModBountyList.layout`:

```
PanelWidgetClass BountyListRoot {
 position 0 0
 size 500 400
 halign center_ref
 valign center_ref
 hexactpos 1
 vexactpos 1
 hexactsize 1
 vexactsize 1
 color 0.1 0.1 0.12 0.92
 {
  TextWidgetClass BountyListTitle {
   position 12 8
   size 476 30
   hexactpos 1
   vexactpos 1
   hexactsize 1
   vexactsize 1
   text "Active Bounties"
   font "gui/fonts/metron2"
   "exact size" 18
   color 1 1 1 0.9
  }
 }
}
```

**2. Crea lo script** in `Scripts/5_Mission/MyMod/MyModBountyListUI.c`:

```c
class MyModBountyListUI
{
    protected ref Widget m_Root;
    protected bool m_IsOpen;

    void MyModBountyListUI()
    {
        m_Root = GetGame().GetWorkspace().CreateWidgets(
            "MyProfessionalMod/Scripts/GUI/layouts/MyModBountyList.layout"
        );
        if (m_Root)
            m_Root.Show(false);
    }

    void Open()  { if (m_Root) { m_Root.Show(true); m_IsOpen = true; } }
    void Close() { if (m_Root) { m_Root.Show(false); m_IsOpen = false; } }
    bool IsOpen() { return m_IsOpen; }

    void ~MyModBountyListUI()
    {
        if (m_Root) m_Root.Unlink();
    }
};
```

### Aggiungere un Nuovo Keybind

**1. Aggiungi l'azione** in `Inputs.xml`:

```xml
<actions>
    <input name="UAMyModPanel" loc="STR_MYMOD_INPUT_PANEL" />
    <input name="UAMyModBountyList" loc="STR_MYMOD_INPUT_BOUNTYLIST" />
</actions>

<sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
    <input name="UAMyModPanel"/>
    <input name="UAMyModBountyList"/>
</sorting>
```

**2. Aggiungi il binding predefinito** nella sezione `<preset>`:

```xml
<input name="UAMyModBountyList">
    <btn name="kEnd"/>
</input>
```

**3. Aggiungi la localizzazione** in `stringtable.csv`:

```csv
"STR_MYMOD_INPUT_BOUNTYLIST","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List","Bounty List",
```

**4. Fai polling per l'input** in `MyModMissionClient.c`:

```c
UAInput bountyInput = GetUApi().GetInputByName("UAMyModBountyList");
if (bountyInput && bountyInput.LocalPress())
{
    ToggleBountyList();
}
```

### Aggiungere una Nuova Voce stringtable

**1. Aggiungi la riga** in `stringtable.csv`. Ogni riga necessita di tutte le 13 colonne di lingua più una virgola finale:

```csv
"STR_MYMOD_BOUNTY_PLACED","Bounty placed!","Bounty placed!","Odměna vypsána!","Kopfgeld gesetzt!","Награда назначена!","Nagroda wyznaczona!","Fejpénz kiírva!","Taglia piazzata!","Recompensa puesta!","Prime placée!","Bounty placed!","Bounty placed!","Recompensa colocada!","Bounty placed!",
```

**2. Usala** nel codice script:

```c
// Widget.SetText() NON risolve automaticamente le chiavi stringtable.
// Devi usare Widget.SetText() con la stringa risolta:
string localizedText = Widget.TranslateString("#STR_MYMOD_BOUNTY_PLACED");
myTextWidget.SetText(localizedText);
```

Oppure in un file `.layout`, il motore risolve automaticamente le chiavi `#STR_`:

```
text "#STR_MYMOD_BOUNTY_PLACED"
```

---

## Prossimi Passi

Con questo template professionale in esecuzione, puoi:

1. **Studiare mod in produzione** -- Leggi [DayZ Expansion](https://github.com/salutesh/DayZ-Expansion-Scripts) e il sorgente di `StarDZ_Core` per pattern reali su scala.
2. **Aggiungere oggetti personalizzati** -- Segui il [Capitolo 8.2: Creare un Oggetto Personalizzato](02-custom-item.md) e integrali con il tuo manager.
3. **Costruire un pannello admin** -- Segui il [Capitolo 8.3: Costruire un Pannello Admin](03-admin-panel.md) usando il tuo sistema di configurazione.
4. **Aggiungere un overlay HUD** -- Segui il [Capitolo 8.8: Costruire un Overlay HUD](08-hud-overlay.md) per elementi UI sempre visibili.
5. **Pubblicare sul Workshop** -- Segui il [Capitolo 8.7: Pubblicazione sul Workshop](07-publishing-workshop.md) quando il tuo mod è pronto.
6. **Imparare il debugging** -- Leggi il [Capitolo 8.6: Debugging e Testing](06-debugging-testing.md) per l'analisi dei log e la risoluzione dei problemi.

---

**Precedente:** [Capitolo 8.8: Costruire un Overlay HUD](08-hud-overlay.md) | [Home](../README.md)
