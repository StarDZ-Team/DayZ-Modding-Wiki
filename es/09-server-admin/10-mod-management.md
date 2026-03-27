# Capitulo 9.10: Gestion de Mods

[Inicio](../README.md) | [<< Anterior: Control de Acceso](09-access-control.md) | [Siguiente: Solucion de Problemas >>](11-troubleshooting.md)

---

> **Resumen:** Instala, configura y mantiene mods de terceros en un servidor dedicado de DayZ. Cubre parametros de lanzamiento, descargas del Workshop, llaves de firma, orden de carga, mods solo de servidor vs requeridos por el cliente, actualizaciones y los errores mas comunes que causan crasheos o expulsiones de jugadores.

---

## Tabla de Contenidos

- [Como se cargan los mods](#como-se-cargan-los-mods)
- [Formato de parametros de lanzamiento](#formato-de-parametros-de-lanzamiento)
- [Instalacion de mods del Workshop](#instalacion-de-mods-del-workshop)
- [Llaves de mods (.bikey)](#llaves-de-mods-bikey)
- [Orden de carga y dependencias](#orden-de-carga-y-dependencias)
- [Mods solo de servidor vs requeridos por el cliente](#mods-solo-de-servidor-vs-requeridos-por-el-cliente)
- [Actualizacion de mods](#actualizacion-de-mods)
- [Solucion de conflictos de mods](#solucion-de-conflictos-de-mods)
- [Errores comunes](#errores-comunes)

---

## Como se cargan los mods

DayZ carga mods a traves del parametro de lanzamiento `-mod=`. Cada entrada es una ruta a una carpeta que contiene archivos PBO y un `config.cpp`. El motor lee cada PBO en cada carpeta de mod, registra sus clases y scripts, y luego continua al siguiente mod en la lista.

El servidor y el cliente deben tener los mismos mods en `-mod=`. Si el servidor lista `@CF;@MyMod` y el cliente solo tiene `@CF`, la conexion falla con un error de firma. Los mods solo de servidor colocados en `-servermod=` son la excepcion -- los clientes nunca necesitan esos.

---

## Formato de parametros de lanzamiento

Un comando tipico de lanzamiento de servidor con mods:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Parametro | Proposito |
|-----------|---------|
| `-mod=` | Mods requeridos tanto por el servidor como por todos los clientes que se conectan |
| `-servermod=` | Mods solo del servidor (los clientes no los necesitan) |

Reglas:
- Las rutas estan **separadas por punto y coma** sin espacios alrededor de los punto y coma
- Cada ruta es relativa al directorio raiz del servidor (por ejemplo, `@CF` significa `<raiz_servidor>/@CF/`)
- Puedes usar rutas absolutas: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **El orden importa** -- las dependencias deben aparecer antes de los mods que las necesitan

---

## Instalacion de mods del Workshop

### Paso 1: Descargar el mod

Usa SteamCMD con el App ID del **cliente** de DayZ (221100) y el ID del Workshop del mod:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

Los archivos descargados quedan en:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Paso 2: Crear un enlace simbolico o copia

Las carpetas del Workshop usan IDs numericos, que son inutilizables en `-mod=`. Crea un enlace simbolico con nombre (recomendado) o copia la carpeta:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Usar una junction significa que las actualizaciones via SteamCMD se aplican automaticamente -- no se requiere re-copiar.

### Paso 3: Copiar el .bikey

Ver la siguiente seccion.

---

## Llaves de mods (.bikey)

Cada mod firmado viene con una carpeta `keys/` que contiene uno o mas archivos `.bikey`. Estos archivos le dicen a BattlEye que firmas de PBO aceptar.

1. Abre la carpeta del mod (por ejemplo, `@CF/keys/`)
2. Copia cada archivo `.bikey` al directorio `keys/` de la raiz del servidor

```
DayZServer/
  keys/
    dayz.bikey              # Vanilla -- siempre presente
    cf.bikey                # Copiado de @CF/keys/
    vpp_admintools.bikey    # Copiado de @VPPAdminTools/keys/
```

Sin la llave correcta, cualquier jugador que ejecute ese mod recibe: **"Player kicked: Modified data"**.

---

## Orden de carga y dependencias

Los mods se cargan de izquierda a derecha en el parametro `-mod=`. El `config.cpp` de un mod declara sus dependencias:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Si `MyMod` requiere `CF`, entonces `@CF` debe aparecer **antes** de `@MyMod` en el parametro de lanzamiento:

```
-mod=@CF;@MyMod          ✓ correcto
-mod=@MyMod;@CF          ✗ crash o clases faltantes
```

**Patron general de orden de carga:**

1. **Mods de framework** -- CF, Community-Online-Tools
2. **Mods de libreria** -- BuilderItems, cualquier paquete de assets compartidos
3. **Mods de caracteristicas** -- adiciones de mapas, armas, vehiculos
4. **Mods dependientes** -- cualquier cosa que liste los anteriores como `requiredAddons`

Cuando tengas dudas, revisa la pagina del Workshop o la documentacion del mod. La mayoria de autores de mods publican el orden de carga requerido.

---

## Mods solo de servidor vs requeridos por el cliente

| Parametro | Quien lo necesita | Ejemplos tipicos |
|-----------|-------------|------------------|
| `-mod=` | Servidor + todos los clientes | Armas, vehiculos, mapas, mods de UI, ropa |
| `-servermod=` | Solo el servidor | Gestores de economia, herramientas de registro, backends de admin, scripts de programacion |

La regla es directa: si un mod contiene **cualquier** script del lado del cliente, layouts, texturas o modelos, debe ir en `-mod=`. Si solo ejecuta logica del lado del servidor sin assets que el cliente necesite, usa `-servermod=`.

Poner un mod solo de servidor en `-mod=` obliga a cada jugador a descargarlo. Poner un mod requerido por el cliente en `-servermod=` causa texturas faltantes, UI rota o errores de script en el cliente.

---

## Actualizacion de mods

### Procedimiento

1. **Detiene el servidor** -- actualizar archivos mientras el servidor esta corriendo puede corromper PBOs
2. **Re-descarga** via SteamCMD:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Copia los archivos .bikey actualizados** -- los autores de mods ocasionalmente rotan sus llaves de firma. Siempre copia el `.bikey` nuevo de la carpeta `keys/` del mod al directorio `keys/` del servidor
4. **Reinicia el servidor**

Si usaste enlaces simbolicos (junctions), el paso 2 actualiza los archivos del mod en su lugar. Si copiaste archivos manualmente, debes copiarlos de nuevo.

### Actualizaciones del lado del cliente

Los jugadores suscritos al mod en Steam Workshop reciben actualizaciones automaticamente. Si actualizas un mod en el servidor y un jugador tiene la version anterior, obtiene un error de firma y no puede conectarse hasta que su cliente se actualice.

---

## Solucion de conflictos de mods

### Revisar el log RPT

Abre el archivo `.RPT` mas reciente en `profiles/`. Busca:

- **"Cannot register"** -- una colision de nombre de clase entre dos mods
- **"Missing addons"** -- una dependencia no esta cargada (orden de carga incorrecto o mod faltante)
- **"Signature verification failed"** -- desajuste de `.bikey` o llave faltante

### Revisar el log de scripts

Abre el `script_*.log` mas reciente en `profiles/`. Busca:

- **"SCRIPT (E)"** -- errores de script, frecuentemente causados por orden de carga o desajuste de version
- **"Definition of variable ... already exists"** -- dos mods definen la misma clase

### Aislar el problema

Cuando tienes muchos mods y algo se rompe, prueba incrementalmente:

1. Empieza solo con mods de framework (`@CF`)
2. Agrega un mod a la vez
3. Lanza y revisa logs despues de cada adicion
4. El mod que causa errores es el culpable

### Dos mods editando la misma clase

Si dos mods usan `modded class PlayerBase`, el que se carga **ultimo** (mas a la derecha en `-mod=`) gana. Su llamada a `super` se encadena a la version del otro mod. Esto generalmente funciona, pero si un mod sobreescribe un metodo sin llamar a `super`, los cambios del otro mod se pierden.

---

## Errores comunes

**Orden de carga incorrecto.** El servidor crashea o registra "Missing addons" porque una dependencia no se cargo todavia. Solucion: mueve el mod de dependencia antes en la lista `-mod=`.

**Olvidar `-servermod=` para mods solo de servidor.** Los jugadores son obligados a descargar un mod que no necesitan. Solucion: mueve los mods solo de servidor de `-mod=` a `-servermod=`.

**No actualizar archivos `.bikey` despues de una actualizacion de mod.** Los jugadores son expulsados con "Modified data" porque la llave del servidor no coincide con las nuevas firmas de PBO del mod. Solucion: siempre re-copia los archivos `.bikey` al actualizar mods.

**Re-empaquetar PBOs de mods.** Re-empaquetar los archivos PBO de un mod rompe su firma digital, causa expulsiones de BattlEye para cada jugador y viola los terminos de la mayoria de autores de mods. Nunca re-empaques un mod que no creaste.

**Mezclar rutas del Workshop con rutas locales.** Usar la ruta numerica cruda del Workshop para algunos mods y carpetas con nombre para otros causa confusion al actualizar. Elige un enfoque -- los enlaces simbolicos son lo mas limpio.

**Espacios en rutas de mods.** Una ruta como `-mod=@My Mod` rompe el parseo. Renombra las carpetas de mods para evitar espacios, o encierra todo el parametro entre comillas: `-mod="@My Mod;@CF"`.

**Mod desactualizado en el servidor, actualizado en el cliente (o viceversa).** El desajuste de version impide la conexion. Manten las versiones del servidor y del Workshop sincronizadas. Actualiza todos los mods y el servidor al mismo tiempo.

---

[Inicio](../README.md) | [<< Anterior: Control de Acceso](09-access-control.md) | [Siguiente: Solucion de Problemas >>](11-troubleshooting.md)
