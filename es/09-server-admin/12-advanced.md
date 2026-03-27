# Capitulo 9.12: Temas Avanzados del Servidor

[Inicio](../README.md) | [<< Anterior: Solucion de Problemas](11-troubleshooting.md) | [Inicio de la Parte 9](01-server-setup.md)

---

> **Resumen:** Archivos de configuracion profunda, configuraciones multi-mapa, division de economia, territorios de animales, eventos dinamicos, control del clima, reinicios automatizados y el sistema de mensajes.

---

## Tabla de Contenidos

- [cfggameplay.json en profundidad](#cfggameplayjson-en-profundidad)
- [Servidores multi-mapa](#servidores-multi-mapa)
- [Ajuste personalizado de la economia](#ajuste-personalizado-de-la-economia)
- [cfgenvironment.xml y territorios de animales](#cfgenvironmentxml-y-territorios-de-animales)
- [Eventos dinamicos personalizados](#eventos-dinamicos-personalizados)
- [Automatizacion de reinicios del servidor](#automatizacion-de-reinicios-del-servidor)
- [cfgweather.xml](#cfgweatherxml)
- [Sistema de mensajes](#sistema-de-mensajes)

---

## cfggameplay.json en profundidad

El archivo **cfggameplay.json** vive en tu carpeta de mision y sobreescribe los valores predeterminados de jugabilidad codificados. Habilitalo en **serverDZ.cfg** primero:

```cpp
enableCfgGameplayFile = 1;
```

Estructura vanilla:

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

- `version` -- debe coincidir con lo que tu binario del servidor espera. No lo cambies.
- `lightingConfig` -- `0` (predeterminado) o `1` (noches mas brillantes).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 valores, uno por mes (Ene-Dic).
- `disablePersonalLight` -- remueve la luz ambiental tenue cerca de jugadores nuevos de noche.
- `staminaMax` y los modificadores de sprint controlan que tan lejos pueden correr los jugadores antes de agotarse.
- `use3DMap` -- cambia el mapa del juego a la variante 3D renderizada del terreno.

---

## Servidores multi-mapa

DayZ soporta multiples mapas a traves de diferentes carpetas de mision dentro de `mpmissions/`:

| Mapa | Carpeta de mision |
|-----|---------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Cada mapa tiene sus propios archivos de CE (`types.xml`, `events.xml`, etc.). Cambia de mapa via `template` en **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

O con un parametro de lanzamiento: `-mission=mpmissions/dayzOffline.enoch`

Para ejecutar multiples mapas simultaneamente, usa instancias de servidor separadas con su propia configuracion, directorio de perfil y rango de puertos.

---

## Ajuste personalizado de la economia

### Dividir types.xml

Divide los items en multiples archivos y registralos en **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

El servidor carga y fusiona todos los archivos con `type="types"`.

### Categorias y etiquetas personalizadas

**cfglimitsdefinition.xml** define categorias/etiquetas para `types.xml` pero se sobrescribe en las actualizaciones. Usa **cfglimitsdefinitionuser.xml** en su lugar:

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

## cfgenvironment.xml y territorios de animales

El archivo **cfgenvironment.xml** en tu carpeta de mision enlaza a archivos de territorio en el subdirectorio `env/`:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

La carpeta `env/` contiene estos archivos de territorio animal:

| Archivo | Animales |
|------|---------|
| **bear_territories.xml** | Osos pardos |
| **wolf_territories.xml** | Manadas de lobos |
| **fox_territories.xml** | Zorros |
| **hare_territories.xml** | Conejos/liebres |
| **hen_territories.xml** | Gallinas |
| **pig_territories.xml** | Cerdos |
| **red_deer_territories.xml** | Ciervos rojos |
| **roe_deer_territories.xml** | Corzos |
| **sheep_goat_territories.xml** | Ovejas/cabras |
| **wild_boar_territories.xml** | Jabalies |
| **cattle_territories.xml** | Vacas |

Una entrada de territorio define zonas circulares con posicion y cantidad de animales:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- coordenadas del centro; `r` -- radio en metros
- `dmin`, `dmax` -- cantidad min/max de animales en la zona
- `smin`, `smax` -- reservado (puesto en `-1`)

---

## Eventos dinamicos personalizados

Los eventos dinamicos (choques de helicoptero, convoyes) se definen en **events.xml**. Para crear un evento personalizado:

**1. Define el evento** en **events.xml**:

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

**2. Agrega posiciones de spawn** en **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Agrega guardias infectados** (opcional) -- agrega elementos `<secondary type="ZmbM_PatrolNormal_Autumn" />` en tu definicion de evento.

**4. Spawns agrupados** (opcional) -- define clusters en **cfgeventgroups.xml** y referencia el nombre del grupo en tu evento.

---

## Automatizacion de reinicios del servidor

DayZ no tiene un programador de reinicios integrado. Usa automatizacion a nivel del SO.

### Windows

Crea **restart_server.bat** y ejecutalo via Tarea Programada de Windows cada 4-6 horas:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Crea un shell script y agregalo a cron (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Siempre haz copia de seguridad de `storage_1/` antes de cada reinicio. La persistencia corrupta durante el apagado puede borrar bases y vehiculos de jugadores.

---

## cfgweather.xml

El archivo **cfgweather.xml** en tu carpeta de mision controla los patrones climaticos. Cada mapa viene con sus propios valores predeterminados:

Cada fenomeno tiene `min`, `max`, `duration_min` y `duration_max` (segundos):

| Fenomeno | Min predeterminado | Max predeterminado | Notas |
|------------|-------------|-------------|-------|
| `overcast` | 0.0 | 1.0 | Controla la densidad de nubes y la probabilidad de lluvia |
| `rain` | 0.0 | 1.0 | Solo se activa por encima de un umbral de overcast. Pon max en `0.0` para que no llueva |
| `fog` | 0.0 | 0.3 | Valores por encima de `0.5` producen visibilidad casi nula |
| `wind_magnitude` | 0.0 | 18.0 | Afecta la balistica y el movimiento del jugador |

---

## Sistema de mensajes

El archivo **db/messages.xml** en tu carpeta de mision controla los mensajes programados del servidor y los avisos de apagado:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- minutos antes de que el mensaje se active (para mensajes de apagado, minutos antes de que el servidor se detenga)
- `shutdown` -- `1` para mensajes de secuencia de apagado, `0` para transmisiones regulares

El sistema de mensajes no reinicia el servidor. Solo muestra avisos cuando un horario de reinicio esta configurado externamente.

---

[Inicio](../README.md) | [<< Anterior: Solucion de Problemas](11-troubleshooting.md) | [Inicio de la Parte 9](01-server-setup.md)
