# Capitulo 9.5: Spawn de Vehiculos y Eventos Dinamicos

[Inicio](../README.md) | [<< Anterior: Economia de Loot](04-loot-economy.md) | [Siguiente: Spawn de Jugadores >>](06-player-spawning.md)

---

> **Resumen:** Los vehiculos y eventos dinamicos (choques de helicopteros, convoyes, autos de policia) NO usan `types.xml`. Usan un sistema separado de tres archivos: `events.xml` define que spawnea y cuantos, `cfgeventspawns.xml` define donde, y `cfgeventgroups.xml` define formaciones agrupadas. Este capitulo cubre los tres archivos con valores reales vanilla.

---

## Tabla de Contenidos

- [Como funciona el spawn de vehiculos](#como-funciona-el-spawn-de-vehiculos)
- [Entradas de vehiculos en events.xml](#entradas-de-vehiculos-en-eventsxml)
- [Referencia de campos de eventos de vehiculos](#referencia-de-campos-de-eventos-de-vehiculos)
- [cfgeventspawns.xml -- Posiciones de spawn](#cfgeventspawnsxml----posiciones-de-spawn)
- [Eventos de choque de helicoptero](#eventos-de-choque-de-helicoptero)
- [Convoy militar](#convoy-militar)
- [Auto de policia](#auto-de-policia)
- [cfgeventgroups.xml -- Spawns agrupados](#cfgeventgroupsxml----spawns-agrupados)
- [Clase raiz de vehiculo en cfgeconomycore.xml](#clase-raiz-de-vehiculo-en-cfgeconomycorexml)
- [Errores comunes](#errores-comunes)

---

## Como funciona el spawn de vehiculos

Los vehiculos **no** se definen en `types.xml`. Si agregas una clase de vehiculo a `types.xml`, no spawneara. Los vehiculos usan un pipeline dedicado de tres archivos:

1. **`events.xml`** -- Define cada evento de vehiculo: cuantos deben existir en el mapa (nominal), que variantes pueden spawnear (hijos), y flags de comportamiento como lifetime y radio seguro.

2. **`cfgeventspawns.xml`** -- Define las posiciones fisicas del mundo donde los eventos de vehiculos pueden colocar entidades. Cada nombre de evento se mapea a una lista de entradas `<pos>` con coordenadas x, z y angulo.

3. **`cfgeventgroups.xml`** -- Define spawns agrupados donde multiples objetos spawnean juntos con offsets de posicion relativos (por ejemplo, trenes abandonados).

La CE lee `events.xml`, elige un evento que necesita spawn, busca posiciones coincidentes en `cfgeventspawns.xml`, selecciona una al azar que satisfaga las restricciones de `saferadius` y `distanceradius`, luego spawnea una entidad hija seleccionada aleatoriamente en esa posicion.

Los tres archivos viven en `mpmissions/<tu_mision>/db/`.

---

## Entradas de vehiculos en events.xml

Cada tipo de vehiculo vanilla tiene su propia entrada de evento. Aqui estan todos con valores reales:

### Sedan civil

```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

### Todos los eventos de vehiculos vanilla

Todos los eventos de vehiculos usan la misma estructura que el Sedan anterior. Solo los valores difieren:

| Nombre del evento | Nominal | Min | Max | Lifetime | Hijos (variantes) |
|------------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Variantes de Hatchback02 |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Variantes de Sedan02 |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | Variantes de camion V3S |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- spawnean menos |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Botes -- mayor conteo, lifetime mas largo |

`VehicleOffroad02` tiene un nominal mas bajo (3) que otros vehiculos terrestres (8). `VehicleBoat` tiene tanto el nominal mas alto (22) como un lifetime mas largo (600 vs 300).

---

## Referencia de campos de eventos de vehiculos

### Campos a nivel de evento

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `name` | string | Identificador del evento. Debe coincidir con una entrada en `cfgeventspawns.xml` cuando `position="fixed"`. |
| `nominal` | int | Numero objetivo de instancias activas de este evento en el mapa. |
| `min` | int | La CE intentara spawnear mas cuando el conteo caiga por debajo de esto. |
| `max` | int | Tope maximo absoluto. La CE nunca excedera este conteo. |
| `lifetime` | int | Segundos entre verificaciones de respawn. Para vehiculos, esto NO es el lifetime de persistencia del vehiculo -- es el intervalo en el cual la CE re-evalua si spawnear o limpiar. |
| `restock` | int | Segundos minimos entre intentos de respawn. 0 = proximo ciclo. |
| `saferadius` | int | Distancia minima (metros) desde cualquier jugador para que el evento spawnee. Previene que vehiculos aparezcan frente a los jugadores. |
| `distanceradius` | int | Distancia minima (metros) entre dos instancias del mismo evento. Previene que dos sedanes spawneen uno al lado del otro. |
| `cleanupradius` | int | Si un jugador esta dentro de esta distancia (metros), la entidad del evento esta protegida de la limpieza. |

### Flags

| Flag | Valores | Descripcion |
|------|--------|-------------|
| `deletable` | 0, 1 | Si la CE puede eliminar esta entidad de evento. Los vehiculos usan 0 (no eliminable por la CE). |
| `init_random` | 0, 1 | Aleatorizar posiciones iniciales en el primer spawn. 0 = usar posiciones fijas de `cfgeventspawns.xml`. |
| `remove_damaged` | 0, 1 | Remover la entidad cuando se arruina. **Critico para vehiculos** -- ver [Errores comunes](#errores-comunes). |

### Otros campos

| Campo | Valores | Descripcion |
|-------|--------|-------------|
| `position` | `fixed`, `player` | `fixed` = spawnear en posiciones de `cfgeventspawns.xml`. `player` = spawnear relativo a posiciones de jugadores. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max aplicado por tipo hijo. `mixed` = min/max compartido entre todos los hijos. `custom` = comportamiento especifico del motor. |
| `active` | 0, 1 | Activar o desactivar este evento. 0 = el evento se omite completamente. |

### Campos de hijos

| Atributo | Descripcion |
|-----------|-------------|
| `type` | Nombre de clase de la entidad a spawnear. |
| `min` | Instancias minimas de esta variante. |
| `max` | Instancias maximas de esta variante. |
| `lootmin` | Numero minimo de items de loot spawneados dentro/alrededor de la entidad. 0 para vehiculos (las partes vienen de `cfgspawnabletypes.xml`). |
| `lootmax` | Maximo de items de loot. Usado por choques de helicoptero y eventos dinamicos, no vehiculos. |

---

## cfgeventspawns.xml -- Posiciones de spawn

Este archivo mapea nombres de eventos a coordenadas del mundo. Cada bloque `<event>` contiene una lista de posiciones de spawn validas para ese tipo de evento. Cuando la CE necesita spawnear un vehiculo, elige una posicion aleatoria de esta lista que satisfaga las restricciones de `saferadius` y `distanceradius`.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... mas posiciones ... -->
</event>
```

Cada `<pos>` tiene tres atributos:

| Atributo | Descripcion |
|-----------|-------------|
| `x` | Coordenada X del mundo (posicion este-oeste en el mapa). |
| `z` | Coordenada Z del mundo (posicion norte-sur en el mapa). |
| `a` | Angulo en grados (0-360). La direccion que enfrenta el vehiculo al spawnear. |

**Reglas clave:**

- Si un evento no tiene un bloque `<event>` correspondiente en `cfgeventspawns.xml`, **no spawneara** independientemente de la configuracion en `events.xml`.
- Necesitas al menos tantas entradas `<pos>` como tu valor de `nominal`. Si pones `nominal=8` pero solo tienes 3 posiciones, solo 3 pueden spawnear.
- Las posiciones deben estar en caminos o terreno plano. Una posicion dentro de un edificio o en terreno empinado hara que el vehiculo spawnee enterrado o volteado.
- El valor `a` (angulo) determina la direccion que enfrenta el vehiculo. Alinealo con la direccion del camino para spawns de apariencia natural.

---

## Eventos de choque de helicoptero

Los choques de helicoptero son eventos dinamicos que spawnean un destrozo con loot militar e infectados circundantes. Usan la etiqueta `<secondary>` para definir spawns de zombis ambientales alrededor del sitio del choque.

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>1</min>
    <max>3</max>
    <lifetime>2100</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="15" lootmin="10" max="3" min="1" type="Wreck_UH1Y"/>
    </children>
</event>
```

### Diferencias clave respecto a eventos de vehiculos

- **`<secondary>InfectedArmy</secondary>`** -- spawnea zombis militares alrededor del sitio del choque. Esta etiqueta referencia un grupo de spawn de infectados que la CE coloca en la proximidad.
- **`lootmin="10"` / `lootmax="15"`** -- el destrozo spawnea con 10-15 items de loot de evento dinamico. Estos son items marcados con `deloot="1"` en `types.xml` (equipo militar, armas raras).
- **`lifetime=2100`** -- el choque persiste por 35 minutos antes de que la CE lo limpie y spawnee uno nuevo en otro lugar.
- **`saferadius=1000`** -- los choques nunca aparecen dentro de 1 km de un jugador.
- **`remove_damaged=0`** -- el destrozo ya esta "danado" por definicion, asi que esto debe ser 0 o seria limpiado inmediatamente.

---

## Convoy militar

Los convoyes militares son grupos de vehiculos destruidos estaticos que spawnean con loot militar y guardias infectados.

```xml
<event name="StaticMilitaryConvoy">
    <nominal>5</nominal>
    <min>3</min>
    <max>5</max>
    <lifetime>1800</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="5" min="3" type="Wreck_V3S"/>
    </children>
</event>
```

Los convoyes funcionan identicamente a los choques de helicoptero: la etiqueta `<secondary>` spawnea `InfectedArmy` alrededor del sitio, y los items de loot con `deloot="1"` aparecen en los destrozos. Con `nominal=5`, hasta 5 sitios de convoy existen en el mapa simultaneamente. Cada uno dura 1800 segundos (30 minutos) antes de ciclar a una nueva ubicacion.

---

## Auto de policia

Los eventos de autos de policia spawnean vehiculos de policia destruidos con infectados tipo policia cerca. Estan **desactivados por defecto**.

```xml
<event name="StaticPoliceCar">
    <nominal>10</nominal>
    <min>5</min>
    <max>10</max>
    <lifetime>2500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>200</distanceradius>
    <cleanupradius>100</cleanupradius>
    <secondary>InfectedPoliceHard</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>0</active>
    <children>
        <child lootmax="5" lootmin="3" max="10" min="5" type="Wreck_PoliceCar"/>
    </children>
</event>
```

**`active=0`** significa que este evento esta desactivado por defecto -- cambialo a `1` para habilitarlo. La etiqueta `<secondary>InfectedPoliceHard</secondary>` spawnea variantes duras de zombis policia (mas resistentes que infectados estandar). Con `nominal=10` y `saferadius=500`, los autos de policia son mas numerosos pero menos valiosos que los choques de helicoptero.

---

## cfgeventgroups.xml -- Spawns agrupados

Este archivo define eventos donde multiples objetos spawnean juntos con offsets de posicion relativos. El uso mas comun es trenes abandonados.

```xml
<event name="Train_Abandoned_Cherno">
    <children>
        <child type="Land_Train_Wagon_Tanker_Blue" x="0" z="0" a="0"/>
        <child type="Land_Train_Wagon_Box_Brown" x="0" z="15" a="0"/>
        <child type="Land_Train_Wagon_Flatbed_Green" x="0" z="30" a="0"/>
        <child type="Land_Train_Engine_Blue" x="0" z="45" a="0"/>
    </children>
</event>
```

El primer hijo se coloca en la posicion de `cfgeventspawns.xml`. Los hijos subsiguientes se desplazan por sus valores `x`, `z`, `a` relativos a ese origen. En este ejemplo, los vagones del tren estan espaciados 15 metros a lo largo del eje z.

Cada `<child>` en un grupo tiene:

| Atributo | Descripcion |
|-----------|-------------|
| `type` | Nombre de clase del objeto a spawnear. |
| `x` | Offset en X en metros desde el origen del grupo. |
| `z` | Offset en Z en metros desde el origen del grupo. |
| `a` | Offset de angulo en grados desde el origen del grupo. |

El evento del grupo en si todavia necesita una entrada correspondiente en `events.xml` para controlar conteos nominales, lifetime y estado activo.

---

## Clase raiz de vehiculo en cfgeconomycore.xml

Para que la CE reconozca vehiculos como entidades rastreables, deben tener una declaracion de clase raiz en `cfgeconomycore.xml`:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** es la clase base para todos los vehiculos terrestres en DayZ.
- **`BoatScript`** es la clase base para todos los botes.
- El atributo `act="car"` le dice a la CE que trate estas entidades con comportamiento especifico de vehiculos (persistencia, spawn basado en eventos).

Sin estas entradas de clase raiz, la CE no rastrearia ni gestionaria instancias de vehiculos. Si agregas un vehiculo moddeado que hereda de una clase base diferente, puede que necesites agregar su clase raiz aqui.

---

## Errores comunes

Estos son los problemas de spawn de vehiculos mas frecuentes que encuentran los administradores de servidores.

### Poner vehiculos en types.xml

**Problema:** Agregas `CivilianSedan` a `types.xml` con un nominal de 10. No spawnean sedanes.

**Solucion:** Remueve el vehiculo de `types.xml`. Agrega o edita el evento del vehiculo en `events.xml` con los hijos apropiados, y asegurate de que existan posiciones de spawn correspondientes en `cfgeventspawns.xml`. Los vehiculos usan el sistema de eventos, no el sistema de spawn de items.

### Sin posiciones de spawn correspondientes en cfgeventspawns.xml

**Problema:** Creas un nuevo evento de vehiculo en `events.xml` pero el vehiculo nunca aparece.

**Solucion:** Agrega un bloque `<event name="TuNombreDeEvento">` correspondiente en `cfgeventspawns.xml` con suficientes entradas `<pos>`. El `name` del evento en ambos archivos debe coincidir exactamente. Necesitas al menos tantas posiciones como tu valor de `nominal`.

### Poner remove_damaged=0 para vehiculos conducibles

**Problema:** Pones `remove_damaged="0"` en un evento de vehiculo. Con el tiempo, el servidor se llena de vehiculos destruidos que nunca desaparecen, bloqueando posiciones de spawn y degradando el rendimiento.

**Solucion:** Manten `remove_damaged="1"` para todos los vehiculos conducibles (sedanes, camiones, hatchbacks, botes). Esto asegura que cuando un vehiculo es destruido, la CE lo remueve y spawnea uno nuevo. Solo pon `remove_damaged="0"` para objetos de destrozo (choques de helicopteros, convoyes) que ya estan danados por diseno.

### Olvidar poner active=1

**Problema:** Configuras un evento de vehiculo pero nunca spawnea.

**Solucion:** Verifica la etiqueta `<active>`. Si esta puesta en `0`, el evento esta desactivado. Algunos eventos vanilla como `StaticPoliceCar` vienen con `active=0`. Ponlo en `1` para habilitar el spawn.

### No hay suficientes posiciones de spawn para el conteo nominal

**Problema:** Pones `nominal=15` para un evento de vehiculo pero solo existen 6 posiciones en `cfgeventspawns.xml`. Solo spawnean 6 vehiculos.

**Solucion:** Agrega mas entradas `<pos>`. Como regla, incluye al menos 2-3x tu valor nominal en posiciones para darle a la CE suficientes opciones para satisfacer las restricciones de `saferadius` y `distanceradius`.

### Vehiculo spawnea dentro de edificios o bajo tierra

**Problema:** Un vehiculo spawnea empotrado en un edificio o enterrado en el terreno.

**Solucion:** Revisa las coordenadas `<pos>` en `cfgeventspawns.xml`. Prueba las posiciones en el juego usando teletransporte de admin antes de agregarlas al archivo. Las posiciones deben estar en caminos planos o terreno abierto, y el angulo (`a`) debe alinearse con la direccion del camino.

---

[Inicio](../README.md) | [<< Anterior: Economia de Loot](04-loot-economy.md) | [Siguiente: Spawn de Jugadores >>](06-player-spawning.md)
