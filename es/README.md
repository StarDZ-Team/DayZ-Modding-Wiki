# Guia Completa de Modding para DayZ

> La documentacion mas completa sobre modding de DayZ disponible. Desde cero hasta mod publicado.

[![English](https://flagsapi.com/US/flat/48.png)](../en/README.md) [![Portugues](https://flagsapi.com/BR/flat/48.png)](../pt/README.md) [![Espanol](https://flagsapi.com/ES/flat/48.png)](README.md)

---

## Tabla de Contenidos

### Parte 1: Lenguaje Enforce Script
Aprende el lenguaje de scripting de DayZ desde la base.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [1.1](01-enforce-script/01-variables-types.md) | Variables y Tipos | Completado |
| [1.2](01-enforce-script/02-arrays-maps-sets.md) | Arrays, Maps y Sets | Completado |
| [1.3](01-enforce-script/03-classes-inheritance.md) | Clases y Herencia | Completado |
| [1.4](01-enforce-script/04-modded-classes.md) | Clases Modded | Completado |
| [1.5](01-enforce-script/05-control-flow.md) | Flujo de Control | Completado |
| [1.6](01-enforce-script/06-strings.md) | Operaciones con Strings | Completado |
| [1.7](01-enforce-script/07-math-vectors.md) | Matematicas y Vectores | Completado |
| [1.8](01-enforce-script/08-memory-management.md) | Gestion de Memoria | Completado |
| [1.9](01-enforce-script/09-casting-reflection.md) | Casting y Reflexion | Completado |
| [1.10](01-enforce-script/10-enums-preprocessor.md) | Enums y Preprocesador | Completado |
| [1.11](01-enforce-script/11-error-handling.md) | Manejo de Errores | Completado |
| [1.12](01-enforce-script/12-gotchas.md) | Lo que NO Existe | Completado |

### Parte 2: Estructura de Mods
Comprende como se organizan los mods de DayZ.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [2.1](02-mod-structure/01-five-layers.md) | La Jerarquia de 5 Capas de Scripts | Completado |
| [2.2](02-mod-structure/02-config-cpp.md) | config.cpp a Fondo | Completado |
| [2.3](02-mod-structure/03-mod-cpp.md) | mod.cpp y Workshop | Completado |
| [2.4](02-mod-structure/04-minimum-viable-mod.md) | Tu Primer Mod | Completado |
| [2.5](02-mod-structure/05-file-organization.md) | Organizacion de Archivos | Completado |

### Parte 3: Sistema de GUI y Layouts
Construye interfaces de usuario para DayZ.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [3.1](03-gui-system/01-widget-types.md) | Tipos de Widgets | Completado |
| [3.2](03-gui-system/02-layout-files.md) | Formato de Archivos Layout | Completado |
| [3.3](03-gui-system/03-sizing-positioning.md) | Dimensionamiento y Posicionamiento | Completado |
| [3.4](03-gui-system/04-containers.md) | Widgets Contenedores | Completado |
| [3.5](03-gui-system/05-programmatic-widgets.md) | Creacion Programatica | Completado |
| [3.6](03-gui-system/06-event-handling.md) | Manejo de Eventos | Completado |
| [3.7](03-gui-system/07-styles-fonts.md) | Estilos, Fuentes e Imagenes | Completado |

### Parte 4: Formatos de Archivo y Herramientas
Trabajando con el pipeline de assets de DayZ.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [4.1](04-file-formats/01-textures.md) | Texturas (.paa, .edds, .tga) | Completado |
| [4.2](04-file-formats/02-models.md) | Modelos 3D (.p3d) | Completado |
| [4.3](04-file-formats/03-materials.md) | Materiales (.rvmat) | Completado |
| [4.4](04-file-formats/04-audio.md) | Audio (.ogg, .wss) | Completado |
| [4.5](04-file-formats/05-dayz-tools.md) | Flujo de Trabajo con DayZ Tools | Completado |
| [4.6](04-file-formats/06-pbo-packing.md) | Empaquetado PBO | Completado |

### Parte 5: Archivos de Configuracion
Archivos de configuracion esenciales para cada mod.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [5.1](05-config-files/01-stringtable.md) | stringtable.csv (13 Idiomas) | Completado |
| [5.2](05-config-files/02-inputs-xml.md) | Inputs.xml (Atajos de Teclado) | Completado |
| [5.3](05-config-files/03-credits-json.md) | Credits.json | Completado |
| [5.4](05-config-files/04-imagesets.md) | Formato ImageSet | Completado |

### Parte 6: Referencia de API del Motor
APIs del motor DayZ para desarrolladores de mods.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [6.1](06-engine-api/01-entity-system.md) | Sistema de Entidades | Completado |
| [6.2](06-engine-api/02-vehicles.md) | Sistema de Vehiculos | Completado |
| [6.3](06-engine-api/03-weather.md) | Sistema de Clima | Completado |
| [6.4](06-engine-api/04-cameras.md) | Sistema de Camaras | Completado |
| [6.5](06-engine-api/05-ppe.md) | Efectos de Post-Procesado | Completado |
| [6.6](06-engine-api/06-notifications.md) | Sistema de Notificaciones | Completado |
| [6.7](06-engine-api/07-timers.md) | Timers y CallQueue | Completado |
| [6.8](06-engine-api/08-file-io.md) | E/S de Archivos y JSON | Completado |
| [6.9](06-engine-api/09-networking.md) | Redes y RPC | Completado |
| [6.10](06-engine-api/10-central-economy.md) | Economia Central | Completado |

### Parte 7: Patrones y Mejores Practicas
Patrones probados en produccion de mods profesionales.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [7.1](07-patterns/01-singletons.md) | Patron Singleton | Completado |
| [7.2](07-patterns/02-module-systems.md) | Sistemas de Modulos/Plugins | Completado |
| [7.3](07-patterns/03-rpc-patterns.md) | Comunicacion RPC | Completado |
| [7.4](07-patterns/04-config-persistence.md) | Persistencia de Configuracion | Completado |
| [7.5](07-patterns/05-permissions.md) | Sistemas de Permisos | Completado |
| [7.6](07-patterns/06-events.md) | Arquitectura Basada en Eventos | Completado |
| [7.7](07-patterns/07-performance.md) | Optimizacion de Rendimiento | Completado |

### Parte 8: Tutoriales
Guias paso a paso.

| Capitulo | Tema | Estado |
|----------|------|--------|
| [8.1](08-tutorials/01-first-mod.md) | Tu Primer Mod (Hello World) | Completado |
| [8.2](08-tutorials/02-custom-item.md) | Creando un Item Personalizado | Completado |
| [8.3](08-tutorials/03-admin-panel.md) | Construyendo un Panel de Admin | Completado |
| [8.4](08-tutorials/04-chat-commands.md) | Agregando Comandos de Chat | Completado |

---

## Referencia Rapida

- [Hoja de Referencia de Enforce Script](cheatsheet.md)
- [Referencia de Tipos de Widget](03-gui-system/01-widget-types.md)
- [Errores Comunes](01-enforce-script/12-gotchas.md)

---

## Creditos

- **Bohemia Interactive** -- Motor DayZ y muestras oficiales
- **Jacob_Mango** -- Community Framework y Community Online Tools
- **InclementDab** -- Dabs Framework y DayZ Editor
- **DaOne & GravityWolf** -- VPP Admin Tools
- **DayZ Expansion Team** -- Scripts de Expansion
- **Equipo MyMod** -- Compilacion y documentacion

## Licencia

Esta documentacion esta licenciada bajo [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Los ejemplos de codigo estan licenciados bajo [MIT](https://opensource.org/licenses/MIT).
