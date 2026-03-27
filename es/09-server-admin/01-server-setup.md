# Capitulo 9.1: Configuracion del Servidor y Primer Inicio

[Inicio](../README.md) | **Configuracion del Servidor** | [Siguiente: Estructura de Directorios >>](02-directory-structure.md)

---

> **Resumen:** Instala un servidor dedicado de DayZ Standalone desde cero usando SteamCMD, ejecutalo con una configuracion minima, verifica que aparezca en el navegador de servidores y conectate como jugador. Este capitulo cubre todo, desde los requisitos de hardware hasta la solucion de los fallos mas comunes en el primer inicio.

---

## Tabla de Contenidos

- [Requisitos previos](#requisitos-previos)
- [Instalacion de SteamCMD](#instalacion-de-steamcmd)
- [Instalacion del servidor DayZ](#instalacion-del-servidor-dayz)
- [Directorio despues de la instalacion](#directorio-despues-de-la-instalacion)
- [Primer inicio con configuracion minima](#primer-inicio-con-configuracion-minima)
- [Verificar que el servidor esta corriendo](#verificar-que-el-servidor-esta-corriendo)
- [Conectarse como jugador](#conectarse-como-jugador)
- [Problemas comunes del primer inicio](#problemas-comunes-del-primer-inicio)

---

## Requisitos previos

### Hardware

| Componente | Minimo | Recomendado |
|-----------|---------|-------------|
| CPU | 4 nucleos, 2.4 GHz | 6+ nucleos, 3.5 GHz |
| RAM | 8 GB | 16 GB |
| Disco | 20 GB SSD | 40 GB NVMe SSD |
| Red | 10 Mbps de subida | 50+ Mbps de subida |
| SO | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

DayZ Server usa un solo hilo para la logica del juego. La velocidad del reloj importa mas que la cantidad de nucleos.

### Software

- **SteamCMD** -- el cliente de linea de comandos de Steam para instalar servidores dedicados
- **Visual C++ Redistributable 2019** (Windows) -- requerido por `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- generalmente ya esta presente
- Puertos **2302-2305 UDP** redirigidos en tu router/firewall

---

## Instalacion de SteamCMD

### Windows

1. Descarga SteamCMD desde https://developer.valvesoftware.com/wiki/SteamCMD
2. Extrae `steamcmd.exe` en una carpeta permanente, por ejemplo `C:\SteamCMD\`
3. Ejecuta `steamcmd.exe` una vez -- se actualizara automaticamente

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## Instalacion del servidor DayZ

El App ID de Steam del servidor DayZ es **223350**. Puedes instalarlo sin iniciar sesion en una cuenta de Steam que posea DayZ.

### Instalacion en una linea (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Instalacion en una linea (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Script de actualizacion

Crea un script que puedas volver a ejecutar cada vez que salga un parche:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Actualizacion completada.
pause
```

El flag `validate` verifica cada archivo en busca de corrupcion. En una instalacion nueva, espera una descarga de 2-3 GB.

---

## Directorio despues de la instalacion

Despues de la instalacion, el directorio raiz del servidor se ve asi:

```
DayZServer/
  DayZServer_x64.exe        # El ejecutable del servidor
  serverDZ.cfg               # Configuracion principal del servidor
  dayzsetting.xml            # Configuracion de renderizado/video (no relevante para dedicados)
  addons/                    # Archivos PBO vanilla (ai.pbo, animals.pbo, etc.)
  battleye/                  # Anti-cheat BattlEye (BEServer_x64.dll)
  dta/                       # Datos centrales del motor (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Llaves de firma (dayz.bikey para vanilla)
  logs/                      # Logs del motor (conexion, contenido, audio)
  mpmissions/                # Carpetas de misiones
    dayzOffline.chernarusplus/   # Mision de Chernarus
    dayzOffline.enoch/           # Mision de Livonia (DLC)
    dayzOffline.sakhal/          # Mision de Sakhal (DLC)
  profiles/                  # Salida en tiempo de ejecucion: logs RPT, logs de scripts, BD de jugadores
  ban.txt                    # Lista de jugadores baneados (Steam64 IDs)
  whitelist.txt              # Jugadores en lista blanca (Steam64 IDs)
  steam_appid.txt            # Contiene "221100"
```

Puntos clave:
- **Tu editas** `serverDZ.cfg` y los archivos dentro de `mpmissions/`.
- **Nunca edites** archivos en `addons/` o `dta/` -- se sobrescriben en cada actualizacion.
- Los **PBOs de mods** van en el directorio raiz del servidor o en una subcarpeta (cubierto en un capitulo posterior).
- **`profiles/`** se crea en el primer inicio y contiene tus logs de scripts y volcados de errores.

---

## Primer inicio con configuracion minima

### Paso 1: Editar serverDZ.cfg

Abre `serverDZ.cfg` en un editor de texto. Para una primera prueba, usa la configuracion mas simple posible:

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### Paso 2: Iniciar el servidor

Abre un Simbolo del sistema en el directorio del servidor y ejecuta:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Flag | Proposito |
|------|---------|
| `-config=serverDZ.cfg` | Ruta al archivo de configuracion |
| `-port=2302` | Puerto principal del juego (tambien usa 2303-2305) |
| `-profiles=profiles` | Carpeta de salida para logs y datos de jugadores |
| `-dologs` | Activar el registro del servidor |
| `-adminlog` | Registrar acciones de administrador |
| `-netlog` | Registrar eventos de red |
| `-freezecheck` | Auto-reiniciar al detectar congelamiento |

### Paso 3: Esperar la inicializacion

El servidor tarda entre 30 y 90 segundos en iniciarse completamente. Observa la salida de la consola. Cuando veas una linea como:

```
BattlEye Server: Initialized (v1.xxx)
```

...el servidor esta listo para recibir conexiones.

---

## Verificar que el servidor esta corriendo

### Metodo 1: Log de scripts

Busca en `profiles/` un archivo con nombre similar a `script_YYYY-MM-DD_HH-MM-SS.log`. Abrelo y busca:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Estas lineas confirman que la economia se inicializo y la mision se cargo.

### Metodo 2: Archivo RPT

El archivo `.RPT` en `profiles/` muestra la salida a nivel del motor. Busca:

```
Dedicated host created.
BattlEye Server: Initialized
```

### Metodo 3: Navegador de servidores de Steam

Abre Steam, ve a **Ver > Servidores de juego > Favoritos**, haz clic en **Agregar un servidor**, ingresa `127.0.0.1:2302` (o tu IP publica), y haz clic en **Buscar juegos en esta direccion**. Si el servidor aparece, esta funcionando y es accesible.

### Metodo 4: Puerto de consulta

Usa una herramienta externa como https://www.battlemetrics.com/ o el paquete npm `gamedig` para consultar el puerto 27016 (puerto de consulta de Steam = puerto del juego + 24714).

---

## Conectarse como jugador

### Desde la misma maquina

1. Inicia DayZ (no DayZ Server -- el cliente normal del juego)
2. Abre el **Navegador de servidores**
3. Ve a la pestana **LAN** o **Favoritos**
4. Agrega `127.0.0.1:2302` a favoritos
5. Haz clic en **Conectar**

Si ejecutas cliente y servidor en la misma maquina, usa `DayZDiag_x64.exe` (el cliente de diagnostico) en lugar del cliente retail. Inicialo con:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### Desde otra maquina

Usa la **IP publica** o la **IP de LAN** de tu servidor dependiendo de si el cliente esta en la misma red. Los puertos 2302-2305 UDP deben estar redirigidos.

---

## Problemas comunes del primer inicio

### El servidor inicia pero se cierra inmediatamente

**Causa:** Falta Visual C++ Redistributable o hay un error de sintaxis en `serverDZ.cfg`.

**Solucion:** Instala VC++ Redist 2019 (x64). Revisa `serverDZ.cfg` en busca de punto y coma faltantes -- cada linea de parametro debe terminar con `;`.

### "BattlEye initialization failed"

**Causa:** La carpeta `battleye/` no existe o el antivirus esta bloqueando `BEServer_x64.dll`.

**Solucion:** Vuelve a validar los archivos del servidor via SteamCMD. Agrega una excepcion de antivirus para toda la carpeta del servidor.

### El servidor funciona pero no aparece en el navegador

**Causa:** Puertos no redirigidos, o el Firewall de Windows bloqueando el ejecutable.

**Solucion:**
1. Agrega una regla de entrada en el Firewall de Windows para `DayZServer_x64.exe` (permitir todo UDP)
2. Redirige los puertos **2302-2305 UDP** en tu router
3. Verifica con un comprobador de puertos externo que el puerto 2302 UDP esta abierto en tu IP publica

### "Version Mismatch" al conectarse

**Causa:** El servidor y el cliente estan en versiones diferentes.

**Solucion:** Actualiza ambos. Ejecuta el comando de actualizacion de SteamCMD para el servidor. El cliente se actualiza automaticamente a traves de Steam.

### No aparece loot

**Causa:** El archivo `init.c` no existe o el Hive fallo al inicializar.

**Solucion:** Verifica que `mpmissions/dayzOffline.chernarusplus/init.c` existe y contiene `CreateHive()`. Revisa el log de scripts en busca de errores.

### El servidor usa el 100% de un nucleo de CPU

Esto es normal. DayZ Server usa un solo hilo. No ejecutes multiples instancias del servidor en el mismo nucleo -- usa afinidad de procesador o maquinas separadas.

### Los jugadores aparecen como cuervos / atascados en la carga

**Causa:** La plantilla de mision en `serverDZ.cfg` no coincide con una carpeta existente en `mpmissions/`.

**Solucion:** Verifica el valor de template. Debe coincidir exactamente con el nombre de una carpeta:

```cpp
template = "dayzOffline.chernarusplus";  // Debe coincidir con el nombre de carpeta en mpmissions/
```

---

**[Inicio](../README.md)** | **Siguiente:** [Estructura de Directorios >>](02-directory-structure.md)
