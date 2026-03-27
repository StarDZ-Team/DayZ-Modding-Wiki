# Capitulo 9.7: Estado del Mundo y Persistencia

[Inicio](../README.md) | [<< Anterior: Spawn de Jugadores](06-player-spawning.md) | [Siguiente: Ajuste de Rendimiento >>](08-performance.md)

La persistencia de DayZ mantiene el mundo vivo entre reinicios. Entender como funciona te permite gestionar bases, planificar borrados y evitar corrupcion de datos.

## Tabla de Contenidos

- [Como funciona la persistencia](#como-funciona-la-persistencia)
- [El directorio storage_1/](#el-directorio-storage_1)
- [Parametros de persistencia en globals.xml](#parametros-de-persistencia-en-globalsxml)
- [Sistema de banderas de territorio](#sistema-de-banderas-de-territorio)
- [Items de hoarder](#items-de-hoarder)
- [Configuracion de persistencia en cfggameplay.json](#configuracion-de-persistencia-en-cfggameplayjson)
- [Procedimientos de borrado del servidor](#procedimientos-de-borrado-del-servidor)
- [Estrategia de copias de seguridad](#estrategia-de-copias-de-seguridad)
- [Errores comunes](#errores-comunes)

---

## Como funciona la persistencia

DayZ almacena el estado del mundo en el directorio `storage_1/` dentro de la carpeta de perfil de tu servidor. El ciclo es directo:

1. El servidor guarda el estado del mundo periodicamente (por defecto cada ~30 minutos) y al apagarse correctamente.
2. Al reiniciar, el servidor lee `storage_1/` y restaura todos los objetos persistidos -- vehiculos, bases, tiendas, barriles, inventarios de jugadores.
3. Los items sin persistencia (la mayoria del loot en el suelo) son regenerados por la Economia Central en cada reinicio.

Si `storage_1/` no existe al iniciar, el servidor crea un mundo nuevo sin datos de jugadores y sin estructuras construidas.

---

## El directorio storage_1/

Tu perfil del servidor contiene `storage_1/` con estos subdirectorios y archivos:

| Ruta | Contenido |
|------|----------|
| `data/` | Archivos binarios con objetos del mundo -- partes de bases, items colocados, posiciones de vehiculos |
| `players/` | Archivos **.save** por jugador indexados por SteamID64. Cada archivo almacena posicion, inventario, salud, efectos de estado |
| `snapshot/` | Snapshots del estado del mundo usados durante operaciones de guardado |
| `events.bin` / `events.xy` | Estado de eventos dinamicos -- rastrea ubicaciones de choques de helicoptero, posiciones de convoyes y otros eventos spawneados |

La carpeta `data/` es la mayor parte de la persistencia. Contiene datos serializados de objetos que el servidor lee al iniciar para reconstruir el mundo.

---

## Parametros de persistencia en globals.xml

El archivo **globals.xml** (en tu carpeta de mision) controla los temporizadores de limpieza y el comportamiento de banderas. Estos son los valores relevantes para la persistencia:

```xml
<!-- Refresco de bandera de territorio -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 dias (segundos) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 dias (segundos) -->

<!-- Temporizadores de limpieza -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Limpieza predeterminada (segundos) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Cuerpo de jugador muerto: 1 hora -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Animal muerto: 20 minutos -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Zombi muerto: 5.5 minutos -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Item arruinado: 5.5 minutos -->

<!-- Comportamiento de limpieza -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Max items limpiados por ciclo -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Omitir limpieza dentro de 100m de un jugador -->
```

El valor de `CleanupAvoidance` previene que el servidor despawnee objetos cerca de jugadores activos. Si un cuerpo muerto esta dentro de 100 metros de cualquier jugador, permanece hasta que el jugador se aleje o el temporizador se reinicie.

---

## Sistema de banderas de territorio

Las banderas de territorio son el nucleo de la persistencia de bases en DayZ. Asi es como interactuan los dos valores clave:

- **FlagRefreshFrequency** (`432000` segundos = 5 dias) -- Con que frecuencia debes interactuar con tu bandera para mantenerla activa. Acercate a la bandera y usa la accion "Refrescar".
- **FlagRefreshMaxDuration** (`3456000` segundos = 40 dias) -- El tiempo de proteccion acumulado maximo. Cada refresco agrega hasta FlagRefreshFrequency de tiempo, pero el total no puede exceder este tope.

Cuando el temporizador de una bandera se agota:

1. La bandera misma se vuelve elegible para limpieza.
2. Todas las partes de construccion de base adjuntas a esa bandera pierden su proteccion de persistencia.
3. En el siguiente ciclo de limpieza, las partes no protegidas comienzan a despawnear.

Si bajas FlagRefreshFrequency, los jugadores deben visitar sus bases con mas frecuencia. Si subes FlagRefreshMaxDuration, las bases sobreviven mas tiempo entre visitas. Ajusta ambos valores juntos para que coincidan con el estilo de juego de tu servidor.

---

## Items de hoarder

En **cfgspawnabletypes.xml**, ciertos contenedores estan etiquetados con `<hoarder/>`. Esto los marca como items capaces de ser escondites que cuentan hacia los limites de almacenamiento por jugador en la Economia Central.

Los items de hoarder vanilla son:

| Item | Tipo |
|------|------|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Barriles de almacenamiento |
| CarTent, LargeTent, MediumTent, PartyTent | Tiendas |
| SeaChest | Almacenamiento subacuatico |
| SmallProtectorCase | Estuche pequeno con candado |
| UndergroundStash | Escondite enterrado |
| WoodenCrate | Almacenamiento crafteable |

Ejemplo de **cfgspawnabletypes.xml**:

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

El servidor rastrea cuantos items de hoarder ha colocado cada jugador. Cuando se alcanza el limite, las nuevas colocaciones fallan o el item mas antiguo despawnea (dependiendo de la configuracion del servidor).

---

## Configuracion de persistencia en cfggameplay.json

El archivo **cfggameplay.json** en tu carpeta de mision contiene configuraciones que afectan la durabilidad de bases y contenedores:

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Configuracion | Predeterminado | Efecto |
|---------|---------|--------|
| `disableBaseDamage` | `false` | Cuando es `true`, las partes de construccion de base (muros, puertas, atalayas) no pueden ser danadas. Esto efectivamente desactiva el raideo. |
| `disableContainerDamage` | `false` | Cuando es `true`, los contenedores de almacenamiento (tiendas, barriles, cajas) no pueden recibir dano. Los items dentro permanecen seguros. |

Poner ambos en `true` crea un servidor amigable para PvE donde las bases y el almacenamiento son indestructibles. La mayoria de servidores PvP dejan ambos en `false`.

---

## Procedimientos de borrado del servidor

Tienes cuatro tipos de borrado, cada uno apuntando a una parte diferente de `storage_1/`. **Siempre detiene el servidor antes de realizar cualquier borrado.**

### Borrado completo

Elimina toda la carpeta `storage_1/`. El servidor crea un mundo nuevo en el proximo inicio. Todas las bases, vehiculos, tiendas, datos de jugadores y estado de eventos desaparecen.

### Borrado de economia (mantener jugadores)

Elimina `storage_1/data/` pero deja `storage_1/players/` intacto. Los jugadores mantienen sus personajes e inventarios, pero todos los objetos colocados (bases, tiendas, barriles, vehiculos) son removidos.

### Borrado de jugadores (mantener mundo)

Elimina `storage_1/players/`. Todos los personajes de jugadores se reinician a spawns nuevos. Las bases y objetos colocados permanecen en el mundo.

### Reinicio de clima / eventos

Elimina `events.bin` o `events.xy` de `storage_1/`. Esto reinicia las posiciones de eventos dinamicos (choques de helicopteros, convoyes). El servidor genera nuevas ubicaciones de eventos en el proximo inicio.

---

## Estrategia de copias de seguridad

Los datos de persistencia son irremplazables una vez perdidos. Sigue estas practicas:

- **Haz copias de seguridad mientras esta detenido.** Copia toda la carpeta `storage_1/` mientras el servidor no esta corriendo. Copiar durante la ejecucion arriesga capturar un estado parcial o corrupto.
- **Programa copias de seguridad antes de reinicios.** Si ejecutas reinicios automaticos (cada 4-6 horas), agrega un paso de copia de seguridad a tu script de reinicio que copie `storage_1/` antes de que el proceso del servidor inicie.
- **Manten multiples generaciones.** Rota las copias de seguridad para que tengas al menos 3 copias recientes. Si tu ultima copia de seguridad esta corrupta, puedes volver a una anterior.
- **Almacena fuera de la maquina.** Copia las copias de seguridad a un disco separado o almacenamiento en la nube. Una falla de disco en la maquina del servidor se lleva tus copias de seguridad si estan en el mismo disco.

Un script de copia de seguridad minimo (se ejecuta antes del inicio del servidor):

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Errores comunes

Estos aparecen repetidamente en comunidades de administradores de servidores:

| Error | Que sucede | Prevencion |
|---------|-------------|------------|
| Eliminar `storage_1/` mientras el servidor esta corriendo | Corrupcion de datos. El servidor escribe a archivos que ya no existen, causando crasheos o estado parcial en el proximo inicio. | Siempre detiene el servidor primero. |
| No hacer copia de seguridad antes de un borrado | Si accidentalmente eliminas la carpeta equivocada o el borrado sale mal, no hay recuperacion. | Haz copia de seguridad de `storage_1/` antes de cada borrado. |
| Confundir reinicio de clima con borrado completo | Eliminar `events.xy` solo reinicia las posiciones de eventos dinamicos. No reinicia loot, bases ni jugadores. | Conoce que archivos controlan que (ver la tabla de directorio arriba). |
| Bandera no refrescada a tiempo | Despues de 40 dias (FlagRefreshMaxDuration), la bandera expira y todas las partes de base adjuntas se vuelven elegibles para limpieza. Los jugadores pierden toda su base. | Recuerda a los jugadores el intervalo de refresco. Baja FlagRefreshMaxDuration en servidores de poca poblacion. |
| Editar globals.xml mientras el servidor esta corriendo | Los cambios no se aplican hasta el reinicio. Peor aun, el servidor puede sobrescribir tus ediciones al apagarse. | Edita archivos de configuracion solo mientras el servidor esta detenido. |

---

[Inicio](../README.md) | [<< Anterior: Spawn de Jugadores](06-player-spawning.md) | [Siguiente: Ajuste de Rendimiento >>](08-performance.md)
