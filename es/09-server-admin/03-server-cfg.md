# Capitulo 9.3: Referencia Completa de serverDZ.cfg

[Inicio](../README.md) | [<< Anterior: Estructura de Directorios](02-directory-structure.md) | **Referencia de serverDZ.cfg** | [Siguiente: Economia de Loot en Profundidad >>](04-loot-economy.md)

---

> **Resumen:** Cada parametro en `serverDZ.cfg` documentado con su proposito, valores validos y comportamiento predeterminado. Este archivo controla la identidad del servidor, configuracion de red, reglas de juego, aceleracion del tiempo y seleccion de mision.

---

## Tabla de Contenidos

- [Formato del archivo](#formato-del-archivo)
- [Identidad del servidor](#identidad-del-servidor)
- [Red y seguridad](#red-y-seguridad)
- [Reglas de juego](#reglas-de-juego)
- [Tiempo y clima](#tiempo-y-clima)
- [Rendimiento y cola de login](#rendimiento-y-cola-de-login)
- [Persistencia e instancia](#persistencia-e-instancia)
- [Seleccion de mision](#seleccion-de-mision)
- [Archivo de ejemplo completo](#archivo-de-ejemplo-completo)
- [Parametros de lanzamiento que sobreescriben la configuracion](#parametros-de-lanzamiento-que-sobreescriben-la-configuracion)

---

## Formato del archivo

`serverDZ.cfg` usa el formato de configuracion de Bohemia (similar a C). Reglas:

- Cada asignacion de parametro termina con **punto y coma** `;`
- Las cadenas se encierran entre **comillas dobles** `""`
- Los comentarios usan `//` para una sola linea
- El bloque `class Missions` usa llaves `{}` y termina con `};`
- El archivo debe estar codificado en UTF-8 o ANSI -- sin BOM

Un punto y coma faltante hara que el servidor falle silenciosamente o ignore los parametros subsiguientes.

---

## Identidad del servidor

```cpp
hostname = "My DayZ Server";         // Nombre del servidor mostrado en el navegador
password = "";                       // Contrasena para conectarse (vacio = publico)
passwordAdmin = "";                  // Contrasena para login de admin via consola del juego
description = "";                    // Descripcion mostrada en los detalles del navegador de servidores
```

| Parametro | Tipo | Predeterminado | Notas |
|-----------|------|---------|-------|
| `hostname` | string | `""` | Se muestra en el navegador de servidores. Maximo ~100 caracteres. |
| `password` | string | `""` | Deja vacio para un servidor publico. Los jugadores deben ingresar esto para unirse. |
| `passwordAdmin` | string | `""` | Se usa con el comando `#login` en el juego. **Configura esto en cada servidor.** |
| `description` | string | `""` | Las descripciones multilinea no son soportadas. Mantenla corta. |

---

## Red y seguridad

```cpp
maxPlayers = 60;                     // Slots maximos de jugadores
verifySignatures = 2;                // Verificacion de firmas PBO (solo 2 es soportado)
forceSameBuild = 1;                  // Requerir version exe cliente/servidor coincidente
enableWhitelist = 0;                 // Activar/desactivar lista blanca
disableVoN = 0;                      // Desactivar voz por red
vonCodecQuality = 20;               // Calidad de audio VoN (0-30)
guaranteedUpdates = 1;               // Protocolo de red (siempre usar 1)
```

| Parametro | Tipo | Valores validos | Predeterminado | Notas |
|-----------|------|-------------|---------|-------|
| `maxPlayers` | int | 1-60 | 60 | Afecta el uso de RAM. Cada jugador agrega ~50-100 MB. |
| `verifySignatures` | int | 2 | 2 | Solo el valor 2 es soportado. Verifica archivos PBO contra llaves `.bisign`. |
| `forceSameBuild` | int | 0, 1 | 1 | Cuando es 1, los clientes deben coincidir con la version exacta del ejecutable del servidor. Siempre mantenlo en 1. |
| `enableWhitelist` | int | 0, 1 | 0 | Cuando es 1, solo los Steam64 IDs listados en `whitelist.txt` pueden conectarse. |
| `disableVoN` | int | 0, 1 | 0 | Pon 1 para desactivar completamente el chat de voz del juego. |
| `vonCodecQuality` | int | 0-30 | 20 | Valores mas altos significan mejor calidad de voz pero mas ancho de banda. 20 es un buen balance. |
| `guaranteedUpdates` | int | 1 | 1 | Configuracion del protocolo de red. Siempre usa 1. |

### Shard ID

```cpp
shardId = "123abc";                  // Seis caracteres alfanumericos para shards privados
```

| Parametro | Tipo | Predeterminado | Notas |
|-----------|------|---------|-------|
| `shardId` | string | `""` | Usado para servidores de hive privado. Los jugadores en servidores con el mismo `shardId` comparten datos de personaje. Deja vacio para un hive publico. |

---

## Reglas de juego

```cpp
disable3rdPerson = 0;               // Desactivar camara en tercera persona
disableCrosshair = 0;               // Desactivar la mira
disablePersonalLight = 1;           // Desactivar la luz ambiental del jugador
lightingConfig = 0;                 // Brillo nocturno (0 = mas brillante, 1 = mas oscuro)
```

| Parametro | Tipo | Valores validos | Predeterminado | Notas |
|-----------|------|-------------|---------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | Pon 1 para servidores solo en primera persona. Esta es la configuracion "hardcore" mas comun. |
| `disableCrosshair` | int | 0, 1 | 0 | Pon 1 para quitar la mira. A menudo se combina con `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | La "luz personal" es un brillo sutil alrededor del jugador de noche. La mayoria de servidores la desactivan (valor 1) para realismo. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = noches mas brillantes (luz de luna visible). 1 = noches completamente oscuras (requiere linterna/NVG). |

---

## Tiempo y clima

```cpp
serverTime = "SystemTime";                 // Hora inicial
serverTimeAcceleration = 12;               // Multiplicador de velocidad del tiempo (0-24)
serverNightTimeAcceleration = 1;           // Multiplicador de velocidad nocturna (0.1-64)
serverTimePersistent = 0;                  // Guardar hora entre reinicios
```

| Parametro | Tipo | Valores validos | Predeterminado | Notas |
|-----------|------|-------------|---------|-------|
| `serverTime` | string | `"SystemTime"` o `"AAAA/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` usa el reloj local de la maquina. Establece una hora fija como `"2024/9/15/12/0"` para un servidor permanentemente de dia. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Multiplicador para el tiempo del juego. A 12, un ciclo completo de 24 horas toma 2 horas reales. A 1, el tiempo es en tiempo real. A 24, un dia completo pasa en 1 hora. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Se multiplica por `serverTimeAcceleration`. Con valor 4 y aceleracion 12, la noche pasa a velocidad 48x (noches muy cortas). |
| `serverTimePersistent` | int | 0, 1 | 0 | Cuando es 1, el servidor guarda su reloj del juego en disco y lo retoma despues del reinicio. Cuando es 0, la hora se reinicia a `serverTime` en cada reinicio. |

### Configuraciones de tiempo comunes

**Siempre de dia:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Ciclo rapido de dia/noche (dias de 2 horas, noches cortas):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Dia/noche en tiempo real:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Rendimiento y cola de login

```cpp
loginQueueConcurrentPlayers = 5;     // Jugadores procesados a la vez durante el login
loginQueueMaxPlayers = 500;          // Tamano maximo de la cola de login
```

| Parametro | Tipo | Predeterminado | Notas |
|-----------|------|---------|-------|
| `loginQueueConcurrentPlayers` | int | 5 | Cuantos jugadores pueden cargar simultaneamente. Valores mas bajos reducen los picos de carga del servidor despues de un reinicio. Aumenta a 10-15 si tu hardware es potente y los jugadores se quejan de tiempos de espera. |
| `loginQueueMaxPlayers` | int | 500 | Si esta cantidad de jugadores ya estan en cola, las nuevas conexiones son rechazadas. 500 esta bien para la mayoria de servidores. |

---

## Persistencia e instancia

```cpp
instanceId = 1;                      // Identificador de instancia del servidor
storageAutoFix = 1;                  // Auto-reparar archivos de persistencia corruptos
```

| Parametro | Tipo | Predeterminado | Notas |
|-----------|------|---------|-------|
| `instanceId` | int | 1 | Identifica la instancia del servidor. Los datos de persistencia se almacenan en `storage_<instanceId>/`. Si ejecutas multiples servidores en la misma maquina, dale a cada uno un `instanceId` diferente. |
| `storageAutoFix` | int | 1 | Cuando es 1, el servidor verifica los archivos de persistencia al iniciar y reemplaza los corruptos con archivos vacios. Siempre deja esto en 1. |

---

## Seleccion de mision

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

El valor de `template` debe coincidir exactamente con un nombre de carpeta dentro de `mpmissions/`. Misiones vanilla disponibles:

| Template | Mapa | DLC requerido |
|----------|-----|:---:|
| `dayzOffline.chernarusplus` | Chernarus | No |
| `dayzOffline.enoch` | Livonia | Si |
| `dayzOffline.sakhal` | Sakhal | Si |

Las misiones personalizadas (por ejemplo, de mods o mapas de la comunidad) usan su propio nombre de template. La carpeta debe existir en `mpmissions/`.

---

## Archivo de ejemplo completo

Este es el `serverDZ.cfg` predeterminado completo con todos los parametros:

```cpp
hostname = "EXAMPLE NAME";              // Nombre del servidor
password = "";                          // Contrasena para conectarse al servidor
passwordAdmin = "";                     // Contrasena para convertirse en admin

description = "";                       // Descripcion del navegador de servidores

enableWhitelist = 0;                    // Activar/desactivar lista blanca (valor 0-1)

maxPlayers = 60;                        // Cantidad maxima de jugadores

verifySignatures = 2;                   // Verifica .pbos contra archivos .bisign (solo 2 es soportado)
forceSameBuild = 1;                     // Requerir version cliente/servidor coincidente (valor 0-1)

disableVoN = 0;                         // Activar/desactivar voz por red (valor 0-1)
vonCodecQuality = 20;                   // Calidad del codec de voz por red (valores 0-30)

shardId = "123abc";                     // Seis caracteres alfanumericos para shard privado

disable3rdPerson = 0;                   // Alterna la vista en 3ra persona (valor 0-1)
disableCrosshair = 0;                   // Alterna la mira (valor 0-1)

disablePersonalLight = 1;              // Desactiva la luz personal para todos los clientes
lightingConfig = 0;                     // 0 para mas brillante, 1 para noche mas oscura

serverTime = "SystemTime";             // Hora inicial del juego ("SystemTime" o "AAAA/MM/DD/HH/MM")
serverTimeAcceleration = 12;           // Multiplicador de velocidad del tiempo (0-24)
serverNightTimeAcceleration = 1;       // Multiplicador de velocidad nocturna (0.1-64), tambien multiplicado por serverTimeAcceleration
serverTimePersistent = 0;              // Guardar hora entre reinicios (valor 0-1)

guaranteedUpdates = 1;                 // Protocolo de red (siempre usar 1)

loginQueueConcurrentPlayers = 5;       // Jugadores procesados simultaneamente durante el login
loginQueueMaxPlayers = 500;            // Tamano maximo de la cola de login

instanceId = 1;                        // ID de instancia del servidor (afecta el nombre de carpeta de almacenamiento)

storageAutoFix = 1;                    // Auto-reparar persistencia corrupta (valor 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Parametros de lanzamiento que sobreescriben la configuracion

Algunas configuraciones pueden sobreescribirse via parametros de linea de comandos al lanzar `DayZServer_x64.exe`:

| Parametro | Sobreescribe | Ejemplo |
|-----------|-----------|---------|
| `-config=` | Ruta del archivo de configuracion | `-config=serverDZ.cfg` |
| `-port=` | Puerto del juego | `-port=2302` |
| `-profiles=` | Directorio de salida de profiles | `-profiles=profiles` |
| `-mod=` | Mods del lado del cliente (separados por punto y coma) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Mods solo del servidor | `-servermod=@MyServerMod` |
| `-BEpath=` | Ruta de BattlEye | `-BEpath=battleye` |
| `-dologs` | Activar registro | -- |
| `-adminlog` | Activar registro de admin | -- |
| `-netlog` | Activar registro de red | -- |
| `-freezecheck` | Auto-reiniciar al congelarse | -- |
| `-cpuCount=` | Nucleos de CPU a usar | `-cpuCount=4` |
| `-noFilePatching` | Desactivar file patching | -- |

### Ejemplo de lanzamiento completo

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Los mods se cargan en el orden especificado en `-mod=`. El orden de dependencias importa: si el Mod B requiere el Mod A, lista el Mod A primero.

---

**Anterior:** [Estructura de Directorios](02-directory-structure.md) | [Inicio](../README.md) | **Siguiente:** [Economia de Loot en Profundidad >>](04-loot-economy.md)
