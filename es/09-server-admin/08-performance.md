# Capitulo 9.8: Ajuste de Rendimiento

[Inicio](../README.md) | [<< Anterior: Persistencia](07-persistence.md) | [Siguiente: Control de Acceso >>](09-access-control.md)

---

> **Resumen:** El rendimiento del servidor en DayZ se reduce a tres cosas: cantidad de items, eventos dinamicos y carga de mods/jugadores. Este capitulo cubre las configuraciones especificas que importan, como diagnosticar problemas y que hardware realmente ayuda -- todo basado en datos reales de la comunidad de mas de 400 reportes de Discord sobre caidas de FPS, lag y desync.

---

## Tabla de Contenidos

- [Que afecta el rendimiento del servidor](#que-afecta-el-rendimiento-del-servidor)
- [Ajuste de globals.xml](#ajuste-de-globalsxml)
- [Ajuste de economia para rendimiento](#ajuste-de-economia-para-rendimiento)
- [Registro en cfgeconomycore.xml](#registro-en-cfgeconomycorexml)
- [Configuracion de rendimiento en serverDZ.cfg](#configuracion-de-rendimiento-en-serverdzycfg)
- [Impacto de mods en el rendimiento](#impacto-de-mods-en-el-rendimiento)
- [Recomendaciones de hardware](#recomendaciones-de-hardware)
- [Monitoreo de la salud del servidor](#monitoreo-de-la-salud-del-servidor)
- [Errores comunes de rendimiento](#errores-comunes-de-rendimiento)

---

## Que afecta el rendimiento del servidor

De los datos de la comunidad (mas de 400 menciones de FPS/rendimiento/lag/desync en Discord), los tres factores de rendimiento mas grandes son:

1. **Cantidad de items** -- valores altos de `nominal` en `types.xml` significan que la Economia Central rastrea y procesa mas objetos en cada ciclo. Esta es consistentemente la causa numero uno de lag del lado del servidor.
2. **Spawn de eventos** -- demasiados eventos dinamicos activos (vehiculos, animales, choques de helicoptero) en `events.xml` consumen ciclos de spawn/limpieza y slots de entidades.
3. **Cantidad de jugadores + cantidad de mods** -- cada jugador conectado genera actualizaciones de entidades, y cada mod agrega clases de script que el motor debe compilar y ejecutar en cada tick.

El bucle de juego del servidor se ejecuta a una tasa fija de 30 FPS. Cuando el servidor no puede mantener 30 FPS, los jugadores experimentan desync -- rubber-banding, recoleccion de items retrasada y fallos en el registro de impactos. Por debajo de 15 FPS del servidor, el juego se vuelve injugable.

---

## Ajuste de globals.xml

Estos son los valores predeterminados vanilla para los parametros que afectan directamente el rendimiento:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### Que controla cada valor

| Parametro | Predeterminado | Efecto en el rendimiento |
|-----------|---------|-------------------|
| `ZombieMaxCount` | 1000 | Tope de infectados totales en el servidor. Cada zombi ejecuta pathfinding de IA. Bajarlo a 500-700 mejora notablemente los FPS del servidor en servidores poblados. |
| `AnimalMaxCount` | 200 | Tope de animales. Los animales tienen IA mas simple que los zombis pero aun consumen tiempo de tick. Baja a 100 si ves problemas de FPS. |
| `ZoneSpawnDist` | 300 | Distancia en metros a la cual las zonas de zombis se activan alrededor de jugadores. Bajarlo a 200 significa menos zonas activas simultaneas. |
| `SpawnInitial` | 1200 | Numero de items que la CE spawnea en el primer inicio. Valores mas altos significan una carga inicial mas larga. No afecta el rendimiento en estado estable. |
| `CleanupLifetimeDefault` | 45 | Tiempo de limpieza predeterminado en segundos para items sin lifetime especifico. Valores mas bajos significan ciclos de limpieza mas rapidos pero procesamiento de CE mas frecuente. |

**Perfil de rendimiento recomendado** (para servidores con dificultades con mas de 40 jugadores):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Ajuste de economia para rendimiento

La Economia Central ejecuta un ciclo continuo verificando cada tipo de item contra sus objetivos de `nominal`/`min`. Mas tipos de items con nominales mas altos significa mas trabajo por ciclo.

### Reducir valores nominales

Cada item en `types.xml` con `nominal > 0` es rastreado por la CE. Si tienes 2000 tipos de items con un nominal promedio de 20, la CE esta gestionando 40,000 objetos. Reduce los nominales en general para disminuir este numero:

- Items civiles comunes: bajar de 15-40 a 10-25
- Armas: mantener bajo (vanilla ya es 2-10)
- Variantes de ropa: considera desactivar variantes de color que no necesitas (`nominal=0`)

### Reducir eventos dinamicos

En `events.xml`, cada evento activo spawnea y monitorea grupos de entidades. Baja el `nominal` en eventos de vehiculos y animales, o pon `<active>0</active>` en eventos que no necesitas.

### Usar modo inactivo

Cuando no hay jugadores conectados, la CE puede pausarse completamente:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` significa que el servidor entra en modo inactivo 60 segundos despues de que el ultimo jugador se desconecta. `IdleModeStartup=1` significa que el servidor inicia en modo inactivo y solo activa la CE cuando el primer jugador se conecta. Esto previene que el servidor procese ciclos de spawn mientras esta vacio.

### Ajustar tasa de respawn

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Estos controlan cuantos items y tipos de items la CE procesa por ciclo. Valores mas bajos reducen la carga de la CE por tick pero ralentizan el respawn de loot. Los valores predeterminados vanilla anteriores ya son conservadores.

---

## Registro en cfgeconomycore.xml

Activa los logs de diagnostico de la CE temporalmente para medir tiempos de ciclo e identificar cuellos de botella. En tu `cfgeconomycore.xml`:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Para diagnosticar rendimiento, pon `log_ce_statistics` a `"true"`. Esto muestra el tiempo de ciclo de la CE en el log RPT del servidor. Busca lineas mostrando cuanto tiempo toma cada ciclo de la CE -- si los ciclos exceden 1000ms, la economia esta sobrecargada.

Pon `log_ce_lootspawn` y `log_ce_lootcleanup` a `"true"` para ver que tipos de items estan spawneando y limpiandose con mas frecuencia. Estos son tus candidatos para reduccion de nominal.

**Desactiva el registro despues del diagnostico.** Las escrituras de log consumen I/O y pueden empeorar el rendimiento si se dejan activadas permanentemente.

---

## Configuracion de rendimiento en serverDZ.cfg

El archivo de configuracion principal del servidor tiene opciones limitadas relacionadas con el rendimiento:

| Configuracion | Efecto |
|---------|--------|
| `maxPlayers` | Baja esto si el servidor tiene dificultades. Cada jugador genera trafico de red y actualizaciones de entidades. Ir de 60 a 40 jugadores puede recuperar 5-10 FPS del servidor. |
| `instanceId` | Determina la ruta de `storage_1/`. No es una configuracion de rendimiento, pero si tu almacenamiento esta en un disco lento, afecta el I/O de persistencia. |

**Lo que no puedes cambiar:** la tasa de ticks del servidor esta fija en 30 FPS. No hay configuracion para aumentarla o disminuirla. Si el servidor no puede mantener 30 FPS, simplemente corre mas lento.

---

## Impacto de mods en el rendimiento

Cada mod agrega clases de script que el motor compila al iniciar y ejecuta en cada tick. El impacto varia dramaticamente segun la calidad del mod:

- **Mods solo de contenido** (armas, ropa, edificios) agregan tipos de items pero minimo overhead de script. Su costo esta en el rastreo de la CE, no en el procesamiento de ticks.
- **Mods pesados en scripts** con bucles `OnUpdate()` o `OnTick()` ejecutan codigo en cada frame del servidor. Bucles mal optimizados en estos mods son la causa mas comun de lag relacionado con mods.
- **Mods de comerciante/economia** que mantienen inventarios grandes agregan objetos persistentes que el motor debe rastrear.

### Directrices

- Agrega mods incrementalmente. Prueba los FPS del servidor despues de cada adicion, no despues de agregar 10 a la vez.
- Monitorea los FPS del servidor con herramientas de admin o salida del log RPT despues de agregar nuevos mods.
- Si un mod causa problemas, revisa su codigo fuente en busca de operaciones costosas por frame.

Consenso de la comunidad: "Los items (types) y el spawn de eventos son los mas demandantes -- los mods que agregan miles de entradas a types.xml afectan mas que los mods que agregan scripts complejos."

---

## Recomendaciones de hardware

La logica de juego del servidor DayZ es **de un solo hilo**. Las CPUs multi-nucleo ayudan con el overhead del SO y el I/O de red, pero el bucle principal del juego corre en un solo nucleo.

| Componente | Recomendacion | Por que |
|-----------|---------------|-----|
| **CPU** | El mayor rendimiento de un solo hilo que puedas obtener. AMD 5600X o mejor. | El bucle del juego es de un solo hilo. La velocidad del reloj y el IPC importan mas que la cantidad de nucleos. |
| **RAM** | 8 GB minimo, 12-16 GB para servidores con muchos mods | Los mods y mapas grandes consumen memoria. Quedarse sin memoria causa tartamudeos. |
| **Almacenamiento** | SSD requerido | El I/O de persistencia de `storage_1/` es constante. Un HDD causa bloqueos durante los ciclos de guardado. |
| **Red** | 100 Mbps+ con baja latencia | El ancho de banda importa menos que la estabilidad del ping para la prevencion de desync. |

Consejo de la comunidad: "OVH ofrece buena relacion calidad-precio -- alrededor de $60 USD por una maquina dedicada 5600X que maneja servidores moddeados de 60 slots."

Evita el hosting compartido/VPS para servidores poblados. El problema de vecino ruidoso en hardware compartido causa caidas de FPS impredecibles que son imposibles de diagnosticar desde tu lado.

---

## Monitoreo de la salud del servidor

### FPS del servidor

Revisa el log RPT en busca de lineas que contengan FPS del servidor. Un servidor saludable mantiene 30 FPS de manera consistente. Umbrales de advertencia:

| FPS del servidor | Estado |
|------------|--------|
| 25-30 | Normal. Las fluctuaciones menores son esperadas durante combate intenso o reinicios. |
| 15-25 | Degradado. Los jugadores notan desync en interacciones de items y combate. |
| Por debajo de 15 | Critico. Rubber-banding, acciones fallidas, registro de impactos roto. |

### Advertencias de ciclo de la CE

Con `log_ce_statistics` activado, observa los tiempos de ciclo de la CE. Lo normal es por debajo de 500ms. Si los ciclos regularmente exceden 1000ms, tu economia es demasiado pesada.

### Crecimiento del almacenamiento

Monitorea el tamano de `storage_1/`. Un crecimiento descontrolado indica inflamacion de persistencia -- demasiados objetos colocados, tiendas o escondites acumulandose. Borrados regulares del servidor o reducir `FlagRefreshMaxDuration` en `globals.xml` ayudan a controlar esto.

### Reportes de jugadores

Los reportes de desync de los jugadores son tu indicador en tiempo real mas confiable. Si multiples jugadores reportan rubber-banding simultaneamente, los FPS del servidor han caido por debajo de 15.

---

## Errores comunes de rendimiento

### Valores nominales demasiado altos

Poner cada item a `nominal=50` porque "mas loot es divertido" crea decenas de miles de objetos rastreados. La CE gasta todo su ciclo gestionando items en lugar de ejecutar el juego. Empieza con los nominales vanilla y aumenta selectivamente.

### Demasiados eventos de vehiculos

Los vehiculos son entidades costosas con simulacion de fisica, rastreo de accesorios y persistencia. Vanilla spawnea alrededor de 50 vehiculos en total. Los servidores que ejecutan 150+ vehiculos ven una perdida significativa de FPS.

### Ejecutar 30+ mods sin probar

Cada mod esta bien de forma aislada. El efecto compuesto de 30+ mods -- miles de tipos extra, docenas de scripts por frame y mayor presion de memoria -- puede reducir los FPS del servidor en un 50% o mas. Agrega mods en lotes de 3-5 y prueba despues de cada lote.

### Nunca reiniciar el servidor

Algunos mods tienen fugas de memoria que se acumulan con el tiempo. Programa reinicios automaticos cada 4-6 horas. La mayoria de paneles de hosting de servidores soportan esto. Incluso los mods bien escritos se benefician de reinicios periodicos porque la propia fragmentacion de memoria del motor aumenta en sesiones largas.

### Ignorar la inflamacion del almacenamiento

Una carpeta `storage_1/` que crece a varios gigabytes ralentiza cada ciclo de persistencia. Borrala o recortala periodicamente, especialmente si permites construccion de bases sin limites de degradacion.

### Registro dejado activado

El registro de diagnostico de la CE, el registro de depuracion de scripts y el registro de herramientas de admin escriben al disco en cada tick. Activalos para diagnostico, luego desactivalos. El registro verboso persistente en un servidor ocupado puede costar 1-2 FPS por si solo.

---

[Inicio](../README.md) | [<< Anterior: Persistencia](07-persistence.md) | [Siguiente: Control de Acceso >>](09-access-control.md)
