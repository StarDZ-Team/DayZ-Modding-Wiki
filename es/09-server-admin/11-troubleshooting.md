# Capitulo 9.11: Solucion de Problemas del Servidor

[Inicio](../README.md) | [<< Anterior: Gestion de Mods](10-mod-management.md) | [Siguiente: Temas Avanzados >>](12-advanced.md)

---

> **Resumen:** Diagnostica y soluciona los problemas de servidor DayZ mas comunes -- fallos de inicio, problemas de conexion, crasheos, spawning de loot y vehiculos, persistencia y rendimiento. Cada solucion aqui proviene de patrones de fallo reales a traves de miles de reportes de la comunidad.

---

## Tabla de Contenidos

- [El servidor no inicia](#el-servidor-no-inicia)
- [Los jugadores no pueden conectarse](#los-jugadores-no-pueden-conectarse)
- [Crasheos y punteros nulos](#crasheos-y-punteros-nulos)
- [El loot no spawnea](#el-loot-no-spawnea)
- [Los vehiculos no spawnean](#los-vehiculos-no-spawnean)
- [Problemas de persistencia](#problemas-de-persistencia)
- [Problemas de rendimiento](#problemas-de-rendimiento)
- [Lectura de archivos de log](#lectura-de-archivos-de-log)
- [Lista de verificacion de diagnostico rapido](#lista-de-verificacion-de-diagnostico-rapido)

---

## El servidor no inicia

### Archivos DLL faltantes

Si `DayZServer_x64.exe` crashea inmediatamente con un error de DLL faltante, instala el ultimo **Visual C++ Redistributable for Visual Studio 2019** (x64) desde el sitio oficial de Microsoft y reinicia.

### Puerto ya en uso

Otra instancia de DayZ u otra aplicacion esta ocupando el puerto 2302. Verifica con `netstat -ano | findstr 2302` (Windows) o `ss -tulnp | grep 2302` (Linux). Termina el proceso en conflicto o cambia tu puerto con `-port=2402`.

### Carpeta de mision faltante

El servidor espera `mpmissions/<template>/` donde el nombre de la carpeta coincida exactamente con el valor de `template` en **serverDZ.cfg**. Para Chernarus, eso es `mpmissions/dayzOffline.chernarusplus/` y debe contener al menos **init.c**.

### serverDZ.cfg invalido

Un solo punto y coma faltante o un tipo de comilla incorrecto previene el inicio silenciosamente. Presta atencion a:

- `;` faltante al final de lineas de valores
- Comillas tipograficas en lugar de comillas rectas
- Bloque `{};` faltante alrededor de entradas de clase

### Archivos de mod faltantes

Cada ruta en `-mod=@CF;@VPPAdminTools;@MyMod` debe existir relativa a la raiz del servidor y contener una carpeta **addons/** con archivos `.pbo`. Una sola ruta incorrecta previene el inicio.

---

## Los jugadores no pueden conectarse

### Redireccion de puertos

DayZ requiere estos puertos redirigidos y abiertos en tu firewall:

| Puerto | Protocolo | Proposito |
|------|----------|---------|
| 2302 | UDP | Trafico del juego |
| 2303 | UDP | Red de Steam |
| 2304 | UDP | Consulta de Steam (interno) |
| 27016 | UDP | Consulta del navegador de servidores de Steam |

Si cambiaste el puerto base con `-port=`, todos los demas puertos se desplazan con el mismo offset.

### Bloqueo del firewall

Agrega **DayZServer_x64.exe** a las excepciones de tu firewall del SO. En Windows: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. En Linux, abre los puertos con `ufw` o `iptables`.

### Desajuste de mods

Los clientes deben tener exactamente las mismas versiones de mods que el servidor. Si un jugador ve "Mod mismatch", alguno de los dos lados tiene una version desactualizada. Actualiza ambos cuando cualquier mod reciba una actualizacion del Workshop.

### Archivos .bikey faltantes

Cada archivo `.bikey` de cada mod debe estar en el directorio `keys/` del servidor. Sin el, BattlEye rechaza los PBOs firmados del cliente. Mira dentro de la carpeta `keys/` o `key/` de cada mod.

### Servidor lleno

Verifica `maxPlayers` en **serverDZ.cfg** (predeterminado 60).

---

## Crasheos y punteros nulos

### Acceso a puntero nulo

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- el error de script mas comun. Un mod esta llamando a un metodo en un objeto eliminado o no inicializado. Esto es un bug del mod, no una mala configuracion del servidor. Reportalo al autor del mod con el log RPT completo.

### Encontrar errores de script

Busca en el log RPT `SCRIPT (E)`. El nombre de clase y metodo en el error te dice que mod es responsable. Ubicaciones del RPT:

- **Servidor:** directorio `$profiles/` (o raiz del servidor si no se establecio `-profiles=`)
- **Cliente:** `%localappdata%\DayZ\`

### Crash al reiniciar

Si el servidor crashea en cada reinicio, **storage_1/** puede estar corrupto. Detiene el servidor, haz copia de seguridad de `storage_1/`, elimina `storage_1/data/events.bin`, y reinicia. Si eso falla, elimina todo el directorio `storage_1/` (borra toda la persistencia).

### Crash despues de actualizar un mod

Revierte a la version anterior del mod. Revisa el registro de cambios del Workshop en busca de cambios incompatibles -- clases renombradas, configuraciones removidas y formatos de RPC cambiados son causas comunes.

---

## El loot no spawnea

### types.xml no registrado

Los items definidos en **types.xml** no spawnearan a menos que el archivo este registrado en **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Si usas un archivo de types personalizado (por ejemplo, **types_custom.xml**), agrega una entrada `<file>` separada para el.

### Etiquetas de category, usage o value incorrectas

Cada etiqueta `<category>`, `<usage>` y `<value>` en tu types.xml debe coincidir con un nombre definido en **cfglimitsdefinition.xml**. Un error tipografico como `usage name="Military"` (M mayuscula) cuando la definicion dice `military` (minuscula) previene silenciosamente que el item spawnee.

### Nominal puesto en cero

Si `nominal` es `0`, la CE nunca spawneara ese item. Esto es intencional para items que solo deben existir via crafteo, eventos o colocacion de admin. Si quieres que el item spawnee naturalmente, pon `nominal` en al menos `1`.

### Posiciones de grupo de mapa faltantes

Los items necesitan posiciones de spawn validas dentro de edificios. Si un item personalizado no tiene posiciones de grupo de mapa coincidentes (definidas en **mapgroupproto.xml**), la CE no tiene donde colocarlo. Asigna el item a categorias y usages que ya tengan posiciones validas en el mapa.

---

## Los vehiculos no spawnean

Los vehiculos usan el sistema de eventos, **no** types.xml.

### Configuracion de events.xml

Los spawns de vehiculos se definen en **events.xml**:

```xml
<event name="VehicleOffroadHatchback">
    <nominal>8</nominal>
    <min>5</min>
    <max>8</max>
    <lifetime>3888000</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="1" min="1" type="OffroadHatchback"/>
    </children>
</event>
```

### Posiciones de spawn faltantes

Los eventos de vehiculos con `<position>fixed</position>` requieren entradas en **cfgeventspawns.xml**. Sin coordenadas definidas, el evento no tiene donde colocar el vehiculo.

### Evento desactivado

Si `<active>0</active>`, el evento esta completamente deshabilitado. Ponlo en `1`.

### Vehiculos danados bloqueando slots

Si `remove_damaged="0"`, los vehiculos destruidos permanecen en el mundo para siempre y ocupan slots de spawn. Pon `remove_damaged="1"` para que la CE limpie los destrozos y spawnee reemplazos.

---

## Problemas de persistencia

### Bases desapareciendo

Las banderas de territorio deben ser refrescadas antes de que su temporizador expire. El `FlagRefreshFrequency` predeterminado es `432000` segundos (5 dias). Si ningun jugador interactua con la bandera dentro de esa ventana, la bandera y todos los objetos dentro de su radio son eliminados.

Verifica el valor en **globals.xml**:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Aumenta este valor en servidores de poca poblacion donde los jugadores inician sesion con menos frecuencia.

### Items desapareciendo despues del reinicio

Cada item tiene un `lifetime` en **types.xml** (segundos). Cuando expira sin interaccion del jugador, la CE lo remueve. Referencia: `3888000` = 45 dias, `604800` = 7 dias, `14400` = 4 horas. Los items dentro de contenedores heredan el lifetime del contenedor.

### storage_1/ creciendo demasiado

Si tu directorio `storage_1/` crece mas alla de varios cientos de MB, tu economia esta produciendo demasiados items. Reduce los valores de `nominal` en tu types.xml, especialmente para items de alto conteo como comida, ropa y municion. Un archivo de persistencia inflado causa tiempos de reinicio mas largos.

### Datos de jugadores perdidos

Los inventarios y posiciones de jugadores se almacenan en `storage_1/players/`. Si este directorio es eliminado o corrompido, todos los jugadores spawnean nuevos. Haz copias de seguridad de `storage_1/` regularmente.

---

## Problemas de rendimiento

### FPS del servidor cayendo

Los servidores DayZ apuntan a 30+ FPS para jugabilidad fluida. Causas comunes de FPS bajo del servidor:

- **Demasiados zombis** -- reduce `ZombieMaxCount` en **globals.xml** (predeterminado 800, prueba 400-600)
- **Demasiados animales** -- reduce `AnimalMaxCount` (predeterminado 200, prueba 100)
- **Exceso de loot** -- baja los valores de `nominal` en tu types.xml
- **Demasiados objetos de base** -- bases grandes con cientos de items estresan la persistencia
- **Mods pesados en scripts** -- algunos mods ejecutan logica costosa por frame

### Desync

Los jugadores que experimentan rubber-banding, acciones retrasadas o zombis invisibles son sintomas de desync. Esto casi siempre significa que los FPS del servidor han caido por debajo de 15. Soluciona el problema de rendimiento subyacente en lugar de buscar una configuracion especifica para el desync.

### Tiempos de reinicio largos

El tiempo de reinicio es directamente proporcional al tamano de `storage_1/`. Si los reinicios toman mas de 2-3 minutos, tienes demasiados objetos persistentes. Reduce los valores nominales del loot y establece lifetimes apropiados.

---

## Lectura de archivos de log

### Ubicacion del RPT del servidor

El archivo RPT esta en `$profiles/` (si se lanzo con `-profiles=`) o en la raiz del servidor. Patron de nombre de archivo: `DayZServer_x64_<fecha>_<hora>.RPT`.

### Que buscar

| Termino de busqueda | Significado |
|-------------|---------|
| `SCRIPT (E)` | Error de script -- un mod tiene un bug |
| `[ERROR]` | Error a nivel del motor |
| `ErrorMessage` | Error fatal que puede causar apagado |
| `Cannot open` | Archivo faltante (PBO, config, mision) |
| `Crash` | Crash a nivel de aplicacion |

### Logs de BattlEye

Los logs de BattlEye estan en el directorio `BattlEye/` dentro de la raiz de tu servidor. Estos muestran eventos de expulsion y baneo. Si los jugadores reportan ser expulsados inesperadamente, revisa aqui primero.

---

## Lista de verificacion de diagnostico rapido

Cuando algo sale mal, trabaja a traves de esta lista en orden:

```
1. Revisa el RPT del servidor en busca de lineas SCRIPT (E) y [ERROR]
2. Verifica que cada ruta de -mod= existe y contiene addons/*.pbo
3. Verifica que todos los archivos .bikey estan copiados a keys/
4. Revisa serverDZ.cfg en busca de errores de sintaxis (punto y coma faltantes)
5. Verifica la redireccion de puertos: 2302 UDP + 27016 UDP
6. Verifica que la carpeta de mision coincida con el valor de template en serverDZ.cfg
7. Revisa storage_1/ en busca de corrupcion (elimina events.bin si es necesario)
8. Prueba con cero mods primero, luego agrega mods uno a la vez
```

El paso 8 es la tecnica mas poderosa. Si el servidor funciona vanilla pero se rompe con mods, puedes aislar el mod problematico a traves de busqueda binaria -- agrega la mitad de tus mods, prueba, luego reduce.

---

[Inicio](../README.md) | [<< Anterior: Gestion de Mods](10-mod-management.md) | [Siguiente: Temas Avanzados >>](12-advanced.md)
