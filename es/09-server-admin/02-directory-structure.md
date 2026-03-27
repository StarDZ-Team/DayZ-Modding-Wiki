# Capitulo 9.2: Estructura de Directorios y Carpeta de Mision

[Inicio](../README.md) | [<< Anterior: Configuracion del Servidor](01-server-setup.md) | **Estructura de Directorios** | [Siguiente: Referencia de serverDZ.cfg >>](03-server-cfg.md)

---

> **Resumen:** Un recorrido completo de cada archivo y carpeta en el directorio del servidor DayZ y la carpeta de mision. Saber que hace cada archivo -- y cuales son seguros de editar -- es esencial antes de tocar la economia de loot o agregar mods.

---

## Tabla de Contenidos

- [Directorio raiz del servidor](#directorio-raiz-del-servidor)
- [La carpeta addons/](#la-carpeta-addons)
- [La carpeta keys/](#la-carpeta-keys)
- [La carpeta profiles/](#la-carpeta-profiles)
- [La carpeta mpmissions/](#la-carpeta-mpmissions)
- [Estructura de la carpeta de mision](#estructura-de-la-carpeta-de-mision)
- [La carpeta db/ -- Nucleo de la economia](#la-carpeta-db----nucleo-de-la-economia)
- [La carpeta env/ -- Territorios de animales](#la-carpeta-env----territorios-de-animales)
- [La carpeta storage_1/ -- Persistencia](#la-carpeta-storage_1----persistencia)
- [Archivos de mision de nivel superior](#archivos-de-mision-de-nivel-superior)
- [Que archivos editar y cuales dejar intactos](#que-archivos-editar-y-cuales-dejar-intactos)

---

## Directorio raiz del servidor

```
DayZServer/
  DayZServer_x64.exe          # Ejecutable del servidor
  serverDZ.cfg                 # Configuracion principal (nombre, contrasena, mods, hora)
  dayzsetting.xml              # Configuracion de renderizado (irrelevante para servidores dedicados)
  ban.txt                      # Steam64 IDs baneados, uno por linea
  whitelist.txt                # Steam64 IDs en lista blanca, uno por linea
  steam_appid.txt              # Contiene "221100" -- no editar
  dayz.gproj                   # Archivo de proyecto de Workbench -- no editar
  addons/                      # PBOs vanilla del juego
  battleye/                    # Archivos anti-cheat
  config/                      # Configuracion de Steam (config.vdf)
  dta/                         # PBOs centrales del motor (scripts, GUI, graficos)
  keys/                        # Llaves de verificacion de firma (archivos .bikey)
  logs/                        # Logs a nivel del motor
  mpmissions/                  # Todas las carpetas de misiones
  profiles/                    # Salida en tiempo de ejecucion (logs de scripts, BD de jugadores, volcados de errores)
  server_manager/              # Utilidades de administracion del servidor
```

---

## La carpeta addons/

Contiene todo el contenido vanilla del juego empaquetado como archivos PBO. Cada PBO tiene un archivo de firma `.bisign` correspondiente:

```
addons/
  ai.pbo                       # Scripts de comportamiento de IA
  ai.pbo.dayz.bisign           # Firma para ai.pbo
  animals.pbo                  # Definiciones de animales
  characters_backpacks.pbo     # Modelos/configuraciones de mochilas
  characters_belts.pbo         # Modelos de items de cinturon
  weapons_firearms.pbo         # Modelos/configuraciones de armas
  ... (100+ archivos PBO)
```

**Nunca edites estos archivos.** Se sobrescriben cada vez que actualizas el servidor via SteamCMD. Los mods sobreescriben el comportamiento vanilla a traves del sistema de clases `modded`, no modificando PBOs.

---

## La carpeta keys/

Contiene archivos de llave publica `.bikey` usados para verificar firmas de mods:

```
keys/
  dayz.bikey                   # Llave de firma vanilla (siempre presente)
```

Cuando agregas un mod, copia su archivo `.bikey` en esta carpeta. El servidor usa `verifySignatures = 2` en `serverDZ.cfg` para rechazar cualquier PBO que no tenga un `.bikey` correspondiente en esta carpeta.

Si un jugador carga un mod cuya llave no esta en tu carpeta `keys/`, recibe un kick por **"Signature check failed"**.

---

## La carpeta profiles/

Se crea en el primer inicio del servidor. Contiene la salida en tiempo de ejecucion:

```
profiles/
  BattlEye/                              # Logs y bans de BE
  DataCache/                             # Datos en cache
  Users/                                 # Archivos de preferencias por jugador
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Log de administrador
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Reporte del motor (info de errores, advertencias)
  script_2026-03-08_11-34-35.log           # Log de scripts (tu herramienta principal de depuracion)
```

El **log de scripts** es el archivo mas importante aqui. Cada llamada a `Print()`, cada error de script y cada mensaje de carga de mods va aqui. Cuando algo falla, este es el primer lugar donde debes mirar.

Los archivos de log se acumulan con el tiempo. Los logs antiguos no se eliminan automaticamente.

---

## La carpeta mpmissions/

Contiene una subcarpeta por mapa:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (gratis)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

El formato del nombre de carpeta es `<nombreMision>.<nombreTerreno>`. El valor de `template` en `serverDZ.cfg` debe coincidir exactamente con uno de estos nombres de carpeta.

---

## Estructura de la carpeta de mision

La carpeta de mision de Chernarus (`mpmissions/dayzOffline.chernarusplus/`) contiene:

```
dayzOffline.chernarusplus/
  init.c                         # Script de punto de entrada de la mision
  db/                            # Archivos centrales de la economia
  env/                           # Definiciones de territorios de animales
  storage_1/                     # Datos de persistencia (jugadores, estado del mundo)
  cfgeconomycore.xml             # Clases raiz de la economia y configuracion de logs
  cfgenvironment.xml             # Enlaces a archivos de territorios de animales
  cfgeventgroups.xml             # Definiciones de grupos de eventos
  cfgeventspawns.xml             # Posiciones exactas de spawn para eventos (vehiculos, etc.)
  cfgeffectarea.json             # Definiciones de zonas contaminadas
  cfggameplay.json               # Ajustes de jugabilidad (resistencia, dano, construccion)
  cfgignorelist.xml              # Items excluidos de la economia por completo
  cfglimitsdefinition.xml        # Definiciones validas de etiquetas de categoria/uso/valor
  cfglimitsdefinitionuser.xml    # Definiciones de etiquetas personalizadas del usuario
  cfgplayerspawnpoints.xml       # Ubicaciones de spawn para jugadores nuevos
  cfgrandompresets.xml           # Definiciones de pools de loot reutilizables
  cfgspawnabletypes.xml          # Items pre-adjuntos y carga en entidades spawneadas
  cfgundergroundtriggers.json    # Triggers de areas subterraneas
  cfgweather.xml                 # Configuracion del clima
  areaflags.map                  # Datos de flags de area (binario)
  mapclusterproto.xml            # Definiciones de prototipos de clusters de mapa
  mapgroupcluster.xml            # Definiciones de clusters de grupos de edificios
  mapgroupcluster01.xml          # Datos de cluster (parte 1)
  mapgroupcluster02.xml          # Datos de cluster (parte 2)
  mapgroupcluster03.xml          # Datos de cluster (parte 3)
  mapgroupcluster04.xml          # Datos de cluster (parte 4)
  mapgroupdirt.xml               # Posiciones de loot en suelo/tierra
  mapgrouppos.xml                # Posiciones de grupos de mapa
  mapgroupproto.xml              # Definiciones de prototipos para grupos de mapa
```

---

## La carpeta db/ -- Nucleo de la economia

Este es el corazon de la Economia Central. Cinco archivos controlan que aparece, donde y cuanto:

```
db/
  types.xml        # EL archivo clave: define las reglas de spawn de cada item
  globals.xml      # Parametros globales de la economia (temporizadores, limites, conteos)
  events.xml       # Eventos dinamicos (animales, vehiculos, helicopteros)
  economy.xml      # Interruptores para subsistemas de la economia (loot, animales, vehiculos)
  messages.xml     # Mensajes programados del servidor para los jugadores
```

### types.xml

Define las reglas de spawn para **cada item** en el juego. Con aproximadamente 23,000 lineas, este es por mucho el archivo de economia mas grande. Cada entrada especifica cuantas copias de un item deben existir en el mapa, donde puede spawnear y cuanto tiempo persiste. Consulta el [Capitulo 9.4](04-loot-economy.md) para un analisis detallado.

### globals.xml

Parametros globales que afectan toda la economia: conteo de zombis, conteo de animales, temporizadores de limpieza, rangos de dano del loot, tiempo de respawn. Hay 33 parametros en total. Consulta el [Capitulo 9.4](04-loot-economy.md) para la referencia completa.

### events.xml

Define eventos de spawn dinamico para animales y vehiculos. Cada evento especifica un conteo nominal, restricciones de spawn y variantes hijas. Por ejemplo, el evento `VehicleCivilianSedan` spawnea 8 sedanes por el mapa en 3 variantes de color.

### economy.xml

Interruptores maestros para subsistemas de la economia:

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

| Flag | Significado |
|------|---------|
| `init` | Spawnear items en el primer inicio del servidor |
| `load` | Cargar estado guardado desde la persistencia |
| `respawn` | Permitir el respawn de items despues de la limpieza |
| `save` | Guardar estado en archivos de persistencia |

### messages.xml

Mensajes programados transmitidos a todos los jugadores. Soporta temporizadores de cuenta regresiva, intervalos de repeticion, mensajes al conectarse y avisos de apagado:

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

Usa `#name` para el nombre del servidor y `#tmin` para el tiempo restante en minutos.

---

## La carpeta env/ -- Territorios de animales

Contiene archivos XML que definen donde puede spawnear cada especie animal:

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

Estos archivos contienen cientos de puntos de coordenadas que definen zonas de territorio a lo largo del mapa. Son referenciados por `cfgenvironment.xml`. Rara vez necesitas editarlos a menos que quieras cambiar donde spawnean animales o zombis geograficamente.

---

## La carpeta storage_1/ -- Persistencia

Almacena el estado persistente del servidor entre reinicios:

```
storage_1/
  players.db         # Base de datos SQLite de todos los personajes de jugadores
  spawnpoints.bin    # Datos binarios de puntos de spawn
  backup/            # Copias de seguridad automaticas de datos de persistencia
  data/              # Estado del mundo (items colocados, construccion de bases, vehiculos)
```

**Nunca edites `players.db` mientras el servidor esta funcionando.** Es una base de datos SQLite bloqueada por el proceso del servidor. Si necesitas borrar personajes, detiene el servidor primero y elimina o renombra el archivo.

Para hacer un **borrado completo de persistencia**, detiene el servidor y elimina toda la carpeta `storage_1/`. El servidor la recreara en el proximo inicio con un mundo nuevo.

Para hacer un **borrado parcial** (mantener personajes, reiniciar loot):
1. Detiene el servidor
2. Elimina los archivos en `storage_1/data/` pero conserva `players.db`
3. Reinicia

---

## Archivos de mision de nivel superior

### cfgeconomycore.xml

Registra las clases raiz para la economia y configura el registro de la CE:

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

Establece `log_ce_lootspawn` a `"true"` al depurar problemas de spawn de items. Produce una salida detallada en el log RPT mostrando que items la CE intenta spawnear y por que tienen exito o fallan.

### cfglimitsdefinition.xml

Define los valores validos para los elementos `<category>`, `<usage>`, `<value>` y `<tag>` usados en `types.xml`:

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

Si usas una etiqueta `<usage>` o `<value>` en `types.xml` que no esta definida aqui, el item fallara silenciosamente al spawnear.

### cfgignorelist.xml

Los items listados aqui son completamente excluidos de la economia, incluso si tienen entradas en `types.xml`:

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

Esto se usa para items que existen en el codigo del juego pero no estan destinados a spawnear naturalmente (items sin terminar, contenido obsoleto, items de temporada fuera de temporada).

### cfggameplay.json

Un archivo JSON que sobreescribe parametros de jugabilidad. Controla la resistencia, el movimiento, el dano a bases, el clima, la temperatura, la obstruccion de armas, el ahogamiento y mas. Este archivo es opcional -- si no esta presente, el servidor usa valores predeterminados.

### cfgplayerspawnpoints.xml

Define donde aparecen los jugadores recien spawneados en el mapa, con restricciones de distancia respecto a infectados, otros jugadores y edificios.

### cfgeventspawns.xml

Contiene coordenadas exactas del mundo donde los eventos (vehiculos, choques de helicopteros, etc.) pueden spawnear. Cada nombre de evento de `events.xml` tiene una lista de posiciones validas:

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

El atributo `a` es el angulo de rotacion en grados.

---

## Que archivos editar y cuales dejar intactos

| Archivo / Carpeta | Seguro de editar? | Notas |
|---------------|:---:|-------|
| `serverDZ.cfg` | Si | Configuracion principal del servidor |
| `db/types.xml` | Si | Reglas de spawn de items -- tu edicion mas comun |
| `db/globals.xml` | Si | Parametros de ajuste de la economia |
| `db/events.xml` | Si | Eventos de spawn de vehiculos/animales |
| `db/economy.xml` | Si | Interruptores de subsistemas de la economia |
| `db/messages.xml` | Si | Mensajes de transmision del servidor |
| `cfggameplay.json` | Si | Ajustes de jugabilidad |
| `cfgspawnabletypes.xml` | Si | Presets de accesorios/carga |
| `cfgrandompresets.xml` | Si | Definiciones de pools de loot |
| `cfglimitsdefinition.xml` | Si | Agregar etiquetas personalizadas de uso/valor |
| `cfgplayerspawnpoints.xml` | Si | Ubicaciones de spawn de jugadores |
| `cfgeventspawns.xml` | Si | Coordenadas de spawn de eventos |
| `cfgignorelist.xml` | Si | Excluir items de la economia |
| `cfgweather.xml` | Si | Patrones de clima |
| `cfgeffectarea.json` | Si | Zonas contaminadas |
| `init.c` | Si | Script de entrada de la mision |
| `addons/` | **No** | Se sobrescribe en cada actualizacion |
| `dta/` | **No** | Datos centrales del motor |
| `keys/` | Solo agregar | Copia archivos `.bikey` de mods aqui |
| `storage_1/` | Solo eliminar | Persistencia -- no editar manualmente |
| `battleye/` | **No** | Anti-cheat -- no tocar |
| `mapgroup*.xml` | Con cuidado | Posiciones de loot en edificios -- solo edicion avanzada |

---

**Anterior:** [Configuracion del Servidor](01-server-setup.md) | [Inicio](../README.md) | **Siguiente:** [Referencia de serverDZ.cfg >>](03-server-cfg.md)
