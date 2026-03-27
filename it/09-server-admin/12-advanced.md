# Chapter 9.12: Argomenti Avanzati del Server

[Home](../README.md) | [<< Precedente: Risoluzione Problemi](11-troubleshooting.md) | [Home Parte 9](01-server-setup.md)

---

> **Riepilogo:** File di configurazione avanzati, configurazioni multi-mappa, suddivisione dell'economia, territori degli animali, eventi dinamici, controllo del meteo, riavvii automatizzati e sistema dei messaggi.

---

## Indice

- [cfggameplay.json in profondita](#cfggameplayjson-in-profondita)
- [Server multi-mappa](#server-multi-mappa)
- [Regolazione personalizzata dell'economia](#regolazione-personalizzata-delleconomia)
- [cfgenvironment.xml e territori degli animali](#cfgenvironmentxml-e-territori-degli-animali)
- [Eventi dinamici personalizzati](#eventi-dinamici-personalizzati)
- [Automazione dei riavvii del server](#automazione-dei-riavvii-del-server)
- [cfgweather.xml](#cfgweatherxml)
- [Sistema dei messaggi](#sistema-dei-messaggi)

---

## cfggameplay.json in profondita

Il file **cfggameplay.json** si trova nella cartella della tua missione e sovrascrive i valori predefiniti hardcoded del gameplay. Abilitalo prima in **serverDZ.cfg**:

```cpp
enableCfgGameplayFile = 1;
```

Struttura vanilla:

```json
{
  "version": 123,
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false,
    "disableRespawnDialog": false,
    "disableRespawnInUnconsciousness": false
  },
  "PlayerData": {
    "disablePersonalLight": false,
    "StaminaData": {
      "sprintStaminaModifierErc": 1.0, "sprintStaminaModifierCro": 1.0,
      "staminaWeightLimitThreshold": 6000.0, "staminaMax": 100.0,
      "staminaKg": 0.3, "staminaMin": 0.0,
      "staminaDepletionSpeed": 1.0, "staminaRecoverySpeed": 1.0
    },
    "ShockHandlingData": {
      "shockRefillSpeedConscious": 5.0, "shockRefillSpeedUnconscious": 1.0,
      "allowRefillSpeedModifier": true
    },
    "MovementData": {
      "timeToSprint": 0.45, "timeToJog": 0.0,
      "rotationSpeedJog": 0.3, "rotationSpeedSprint": 0.15
    },
    "DrowningData": {
      "staminaDepletionSpeed": 10.0, "healthDepletionSpeed": 3.0,
      "shockDepletionSpeed": 10.0
    },
    "WeaponObstructionData": { "staticMode": 1, "dynamicMode": 1 }
  },
  "WorldsData": {
    "lightingConfig": 0, "objectSpawnersArr": [],
    "environmentMinTemps": [-3, -2, 0, 4, 9, 14, 18, 17, 13, 11, 9, 0],
    "environmentMaxTemps": [3, 5, 7, 14, 19, 24, 26, 25, 18, 14, 10, 5]
  },
  "BaseBuildingData": { "canBuildAnywhere": false, "canCraftAnywhere": false },
  "UIData": {
    "use3DMap": false,
    "HitIndicationData": {
      "hitDirectionOverrideEnabled": false, "hitDirectionBehaviour": 1,
      "hitDirectionStyle": 0, "hitDirectionIndicatorColorStr": "0xffbb0a1e",
      "hitDirectionMaxDuration": 2.0, "hitDirectionBreakPointRelative": 0.2,
      "hitDirectionScatter": 10.0, "hitIndicationPostProcessEnabled": true
    }
  }
}
```

- `version` -- deve corrispondere a quello che il binario del tuo server si aspetta. Non modificarlo.
- `lightingConfig` -- `0` (predefinito) o `1` (notti piu luminose).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 valori, uno per mese (Gen-Dic).
- `disablePersonalLight` -- rimuove la debole luce ambientale vicino ai nuovi giocatori di notte.
- `staminaMax` e i modificatori dello sprint controllano quanto lontano i giocatori possono correre prima dell'esaurimento.
- `use3DMap` -- passa la mappa nel gioco alla variante 3D renderizzata dal terreno.

---

## Server multi-mappa

DayZ supporta mappe multiple attraverso diverse cartelle missione dentro `mpmissions/`:

| Mappa | Cartella missione |
|-------|-------------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Ogni mappa ha i propri file CE (`types.xml`, `events.xml`, ecc.). Cambia mappa tramite `template` in **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Oppure con un parametro di avvio: `-mission=mpmissions/dayzOffline.enoch`

Per eseguire piu mappe contemporaneamente, usa istanze del server separate con la propria configurazione, directory del profilo e intervallo di porte.

---

## Regolazione personalizzata dell'economia

### Suddivisione di types.xml

Suddividi gli oggetti in piu file e registrali in **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

Il server carica e unisce tutti i file con `type="types"`.

### Categorie e tag personalizzati

**cfglimitsdefinition.xml** definisce le categorie/tag per `types.xml` ma viene sovrascritto durante gli aggiornamenti. Usa **cfglimitsdefinitionuser.xml** invece:

```xml
<lists>
    <categories>
        <category name="custom_rare" />
    </categories>
    <tags>
        <tag name="custom_event" />
    </tags>
</lists>
```

---

## cfgenvironment.xml e territori degli animali

Il file **cfgenvironment.xml** nella cartella della tua missione collega ai file dei territori nella sottodirectory `env/`:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

La cartella `env/` contiene questi file dei territori degli animali:

| File | Animali |
|------|---------|
| **bear_territories.xml** | Orsi bruni |
| **wolf_territories.xml** | Branchi di lupi |
| **fox_territories.xml** | Volpi |
| **hare_territories.xml** | Conigli/lepri |
| **hen_territories.xml** | Galline |
| **pig_territories.xml** | Maiali |
| **red_deer_territories.xml** | Cervi rossi |
| **roe_deer_territories.xml** | Caprioli |
| **sheep_goat_territories.xml** | Pecore/capre |
| **wild_boar_territories.xml** | Cinghiali |
| **cattle_territories.xml** | Mucche |

Una voce di territorio definisce zone circolari con posizione e conteggio degli animali:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- coordinate del centro; `r` -- raggio in metri
- `dmin`, `dmax` -- conteggio min/max di animali nella zona
- `smin`, `smax` -- riservati (impostati a `-1`)

---

## Eventi dinamici personalizzati

Gli eventi dinamici (relitti di elicotteri, convogli) sono definiti in **events.xml**. Per creare un evento personalizzato:

**1. Definisci l'evento** in **events.xml**:

```xml
<event name="StaticMyCustomCrash">
    <nominal>3</nominal> <min>1</min> <max>5</max>
    <lifetime>1800</lifetime> <restock>600</restock>
    <saferadius>500</saferadius> <distanceradius>200</distanceradius> <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1" />
    <position>fixed</position> <limit>child</limit> <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_Mi8_Crashed" />
    </children>
</event>
```

**2. Aggiungi posizioni di spawn** in **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Aggiungi guardie infette** (opzionale) -- aggiungi elementi `<secondary type="ZmbM_PatrolNormal_Autumn" />` nella definizione del tuo evento.

**4. Spawn raggruppati** (opzionale) -- definisci i cluster in **cfgeventgroups.xml** e referenzia il nome del gruppo nel tuo evento.

---

## Automazione dei riavvii del server

DayZ non ha un programmatore di riavvii integrato. Usa l'automazione a livello di sistema operativo.

### Windows

Crea **restart_server.bat** ed eseguilo tramite Operazioni Pianificate di Windows ogni 4-6 ore:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Crea uno script shell e aggiungilo al cron (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Fai sempre il backup di `storage_1/` prima di ogni riavvio. La persistenza corrotta durante lo spegnimento puo cancellare le basi e i veicoli dei giocatori.

---

## cfgweather.xml

Il file **cfgweather.xml** nella cartella della tua missione controlla i pattern meteorologici. Ogni mappa viene distribuita con i propri valori predefiniti:

Ogni fenomeno ha `min`, `max`, `duration_min` e `duration_max` (secondi):

| Fenomeno | Min predefinito | Max predefinito | Note |
|----------|-----------------|-----------------|------|
| `overcast` | 0.0 | 1.0 | Guida la densita delle nuvole e la probabilita di pioggia |
| `rain` | 0.0 | 1.0 | Si attiva solo sopra una soglia di copertura nuvolosa. Imposta max a `0.0` per nessuna pioggia |
| `fog` | 0.0 | 0.3 | Valori sopra `0.5` producono visibilita quasi nulla |
| `wind_magnitude` | 0.0 | 18.0 | Influisce sulla balistica e sul movimento del giocatore |

---

## Sistema dei messaggi

Il file **db/messages.xml** nella cartella della tua missione controlla i messaggi programmati del server e gli avvisi di spegnimento:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- minuti prima che il messaggio si attivi (per i messaggi di spegnimento, minuti prima che il server si fermi)
- `shutdown` -- `1` per messaggi della sequenza di spegnimento, `0` per broadcast regolari

Il sistema dei messaggi non riavvia il server. Visualizza solo avvisi quando un programma di riavvio e configurato esternamente.

---

[Home](../README.md) | [<< Precedente: Risoluzione Problemi](11-troubleshooting.md) | [Home Parte 9](01-server-setup.md)
