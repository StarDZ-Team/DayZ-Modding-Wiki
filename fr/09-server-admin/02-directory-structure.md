# Chapter 9.2 : Structure des répertoires et dossier de mission

[Accueil](../README.md) | [<< Précédent : Installation du serveur](01-server-setup.md) | **Structure des répertoires** | [Suivant : Référence serverDZ.cfg >>](03-server-cfg.md)

---

> **Résumé :** Un guide complet de chaque fichier et dossier dans le répertoire du serveur DayZ et le dossier de mission. Savoir ce que fait chaque fichier -- et lesquels peuvent être modifiés sans risque -- est essentiel avant de toucher à l'économie du loot ou d'ajouter des mods.

---

## Table des matières

- [Répertoire principal du serveur](#répertoire-principal-du-serveur)
- [Le dossier addons/](#le-dossier-addons)
- [Le dossier keys/](#le-dossier-keys)
- [Le dossier profiles/](#le-dossier-profiles)
- [Le dossier mpmissions/](#le-dossier-mpmissions)
- [Structure du dossier de mission](#structure-du-dossier-de-mission)
- [Le dossier db/ -- Cœur de l'économie](#le-dossier-db----cœur-de-léconomie)
- [Le dossier env/ -- Territoires animaux](#le-dossier-env----territoires-animaux)
- [Le dossier storage_1/ -- Persistance](#le-dossier-storage_1----persistance)
- [Fichiers principaux de la mission](#fichiers-principaux-de-la-mission)
- [Quels fichiers modifier vs ne pas toucher](#quels-fichiers-modifier-vs-ne-pas-toucher)

---

## Répertoire principal du serveur

```
DayZServer/
  DayZServer_x64.exe          # Exécutable du serveur
  serverDZ.cfg                 # Configuration principale du serveur (nom, mot de passe, mods, heure)
  dayzsetting.xml              # Paramètres de rendu (non pertinents pour les serveurs dédiés)
  ban.txt                      # Steam64 IDs bannis, un par ligne
  whitelist.txt                # Steam64 IDs en liste blanche, un par ligne
  steam_appid.txt              # Contient "221100" -- ne pas modifier
  dayz.gproj                   # Fichier projet Workbench -- ne pas modifier
  addons/                      # PBO de jeu vanilla
  battleye/                    # Fichiers anti-triche
  config/                      # Configuration Steam (config.vdf)
  dta/                         # PBO moteur principaux (scripts, GUI, graphiques)
  keys/                        # Clés de vérification de signature (fichiers .bikey)
  logs/                        # Logs au niveau moteur
  mpmissions/                  # Tous les dossiers de missions
  profiles/                    # Sortie runtime (logs de scripts, base de données joueurs, dumps de crash)
  server_manager/              # Utilitaires de gestion du serveur
```

---

## Le dossier addons/

Contient tout le contenu vanilla du jeu empaqueté sous forme de fichiers PBO. Chaque PBO possède un fichier de signature `.bisign` correspondant :

```
addons/
  ai.pbo                       # Scripts de comportement IA
  ai.pbo.dayz.bisign           # Signature pour ai.pbo
  animals.pbo                  # Définitions des animaux
  characters_backpacks.pbo     # Modèles/configs des sacs à dos
  characters_belts.pbo         # Modèles des ceintures
  weapons_firearms.pbo         # Modèles/configs des armes
  ... (100+ fichiers PBO)
```

**Ne modifiez jamais ces fichiers.** Ils sont écrasés à chaque mise à jour du serveur via SteamCMD. Les mods remplacent le comportement vanilla via le système de classes `modded`, pas en modifiant les PBO.

---

## Le dossier keys/

Contient les fichiers de clés publiques `.bikey` utilisés pour vérifier les signatures des mods :

```
keys/
  dayz.bikey                   # Clé de signature vanilla (toujours présente)
```

Lorsque vous ajoutez un mod, copiez son fichier `.bikey` dans ce dossier. Le serveur utilise `verifySignatures = 2` dans `serverDZ.cfg` pour rejeter tout PBO qui n'a pas de `.bikey` correspondant dans ce dossier.

Si un joueur charge un mod dont la clé n'est pas dans votre dossier `keys/`, il reçoit un kick **"Signature check failed"**.

---

## Le dossier profiles/

Créé au premier lancement du serveur. Contient la sortie runtime :

```
profiles/
  BattlEye/                              # Logs et bans BE
  DataCache/                             # Données en cache
  Users/                                 # Fichiers de préférences par joueur
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Log admin
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Rapport moteur (infos crash, avertissements)
  script_2026-03-08_11-34-35.log           # Log de scripts (votre outil de débogage principal)
```

Le **log de scripts** est le fichier le plus important ici. Chaque appel `Print()`, chaque erreur de script, et chaque message de chargement de mod y apparaît. Quand quelque chose ne fonctionne pas, c'est là que vous regardez en premier.

Les fichiers de log s'accumulent avec le temps. Les anciens logs ne sont pas automatiquement supprimés.

---

## Le dossier mpmissions/

Contient un sous-dossier par carte :

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (gratuit)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

Le format du nom de dossier est `<nomDeMission>.<nomDeTerrain>`. La valeur `template` dans `serverDZ.cfg` doit correspondre exactement à l'un de ces noms de dossier.

---

## Structure du dossier de mission

Le dossier de mission Chernarus (`mpmissions/dayzOffline.chernarusplus/`) contient :

```
dayzOffline.chernarusplus/
  init.c                         # Script du point d'entrée de la mission
  db/                            # Fichiers principaux de l'économie
  env/                           # Définitions des territoires animaux
  storage_1/                     # Données de persistance (joueurs, état du monde)
  cfgeconomycore.xml             # Classes racines de l'économie et paramètres de journalisation
  cfgenvironment.xml             # Liens vers les fichiers de territoires animaux
  cfgeventgroups.xml             # Définitions des groupes d'événements
  cfgeventspawns.xml             # Positions exactes d'apparition pour les événements (véhicules, etc.)
  cfgeffectarea.json             # Définitions des zones contaminées
  cfggameplay.json               # Réglages du gameplay (endurance, dégâts, construction)
  cfgignorelist.xml              # Objets exclus entièrement de l'économie
  cfglimitsdefinition.xml        # Définitions valides des tags catégorie/usage/valeur
  cfglimitsdefinitionuser.xml    # Définitions de tags personnalisés utilisateur
  cfgplayerspawnpoints.xml       # Emplacements d'apparition des nouveaux joueurs
  cfgrandompresets.xml           # Définitions réutilisables de pools de loot
  cfgspawnabletypes.xml          # Attachements pré-configurés et cargaison sur les entités apparues
  cfgundergroundtriggers.json    # Déclencheurs de zones souterraines
  cfgweather.xml                 # Configuration météo
  areaflags.map                  # Données de flags de zone (binaire)
  mapclusterproto.xml            # Définitions de prototypes de clusters de carte
  mapgroupcluster.xml            # Définitions de clusters de groupes de bâtiments
  mapgroupcluster01.xml          # Données de cluster (partie 1)
  mapgroupcluster02.xml          # Données de cluster (partie 2)
  mapgroupcluster03.xml          # Données de cluster (partie 3)
  mapgroupcluster04.xml          # Données de cluster (partie 4)
  mapgroupdirt.xml               # Positions de loot au sol/terre
  mapgrouppos.xml                # Positions des groupes de carte
  mapgroupproto.xml              # Définitions de prototypes pour les groupes de carte
```

---

## Le dossier db/ -- Cœur de l'économie

C'est le cœur de l'Économie Centrale. Cinq fichiers contrôlent ce qui apparaît, où et en quelle quantité :

```
db/
  types.xml        # LE fichier clé : définit les règles d'apparition de chaque objet
  globals.xml      # Paramètres globaux de l'économie (timers, limites, compteurs)
  events.xml       # Événements dynamiques (animaux, véhicules, hélicoptères)
  economy.xml      # Interrupteurs pour les sous-systèmes de l'économie (loot, animaux, véhicules)
  messages.xml     # Messages programmés du serveur aux joueurs
```

### types.xml

Définit les règles d'apparition de **chaque objet** du jeu. Avec environ 23 000 lignes, c'est de loin le plus grand fichier de l'économie. Chaque entrée spécifie combien de copies d'un objet doivent exister sur la carte, où il peut apparaître, et combien de temps il persiste. Voir le [Chapitre 9.4](04-loot-economy.md) pour une analyse approfondie.

### globals.xml

Paramètres globaux qui affectent l'ensemble de l'économie : nombre de zombies, nombre d'animaux, timers de nettoyage, plages de dégâts du loot, timing de réapparition. Il y a 33 paramètres au total. Voir le [Chapitre 9.4](04-loot-economy.md) pour la référence complète.

### events.xml

Définit les événements d'apparition dynamiques pour les animaux et véhicules. Chaque événement spécifie un nombre nominal, des contraintes d'apparition, et des variantes enfants. Par exemple, l'événement `VehicleCivilianSedan` fait apparaître 8 berlines sur la carte en 3 variantes de couleur.

### economy.xml

Interrupteurs principaux pour les sous-systèmes de l'économie :

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

| Flag | Signification |
|------|---------------|
| `init` | Faire apparaître les objets au premier démarrage du serveur |
| `load` | Charger l'état sauvegardé depuis la persistance |
| `respawn` | Permettre la réapparition des objets après nettoyage |
| `save` | Sauvegarder l'état dans les fichiers de persistance |

### messages.xml

Messages programmés diffusés à tous les joueurs. Prend en charge les minuteries de compte à rebours, les intervalles de répétition, les messages à la connexion, et les avertissements d'arrêt :

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

Utilisez `#name` pour le nom du serveur et `#tmin` pour le temps restant en minutes.

---

## Le dossier env/ -- Territoires animaux

Contient les fichiers XML qui définissent où chaque espèce animale peut apparaître :

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

Ces fichiers contiennent des centaines de points de coordonnées définissant les zones de territoire sur la carte. Ils sont référencés par `cfgenvironment.xml`. Vous avez rarement besoin de les modifier, sauf si vous souhaitez changer l'emplacement géographique d'apparition des animaux ou des zombies.

---

## Le dossier storage_1/ -- Persistance

Contient l'état persistant du serveur entre les redémarrages :

```
storage_1/
  players.db         # Base de données SQLite de tous les personnages joueurs
  spawnpoints.bin    # Données binaires des points d'apparition
  backup/            # Sauvegardes automatiques des données de persistance
  data/              # État du monde (objets placés, construction de bases, véhicules)
```

**Ne modifiez jamais `players.db` pendant que le serveur tourne.** C'est une base de données SQLite verrouillée par le processus serveur. Si vous devez effacer les personnages, arrêtez d'abord le serveur et supprimez ou renommez le fichier.

Pour effectuer un **wipe complet de la persistance**, arrêtez le serveur et supprimez l'intégralité du dossier `storage_1/`. Le serveur le recréera au prochain lancement avec un monde vierge.

Pour un **wipe partiel** (conserver les personnages, réinitialiser le loot) :
1. Arrêtez le serveur
2. Supprimez les fichiers dans `storage_1/data/` mais conservez `players.db`
3. Redémarrez

---

## Fichiers principaux de la mission

### cfgeconomycore.xml

Enregistre les classes racines pour l'économie et configure la journalisation du CE :

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

Définissez `log_ce_lootspawn` à `"true"` lors du débogage de problèmes d'apparition d'objets. Cela produit une sortie détaillée dans le log RPT montrant quels objets le CE essaie de faire apparaître et pourquoi ils réussissent ou échouent.

### cfglimitsdefinition.xml

Définit les valeurs valides pour les éléments `<category>`, `<usage>`, `<value>`, et `<tag>` utilisés dans `types.xml` :

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

Si vous utilisez un tag `<usage>` ou `<value>` dans `types.xml` qui n'est pas défini ici, l'objet n'apparaîtra pas silencieusement.

### cfgignorelist.xml

Les objets listés ici sont entièrement exclus de l'économie, même s'ils ont des entrées dans `types.xml` :

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

Ceci est utilisé pour les objets qui existent dans le code du jeu mais ne sont pas censés apparaître naturellement (objets inachevés, contenu obsolète, objets saisonniers hors saison).

### cfggameplay.json

Un fichier JSON qui remplace les paramètres de gameplay. Contrôle l'endurance, le mouvement, les dégâts de base, la météo, la température, l'obstruction des armes, la noyade, et plus encore. Ce fichier est optionnel -- s'il est absent, le serveur utilise les valeurs par défaut.

### cfgplayerspawnpoints.xml

Définit où les joueurs fraîchement apparus apparaissent sur la carte, avec des contraintes de distance par rapport aux infectés, autres joueurs et bâtiments.

### cfgeventspawns.xml

Contient les coordonnées exactes dans le monde où les événements (véhicules, crashs d'hélicoptères, etc.) peuvent apparaître. Chaque nom d'événement de `events.xml` possède une liste de positions valides :

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

L'attribut `a` est l'angle de rotation en degrés.

---

## Quels fichiers modifier vs ne pas toucher

| Fichier / Dossier | Modifiable ? | Notes |
|-------------------|:---:|-------|
| `serverDZ.cfg` | Oui | Configuration principale du serveur |
| `db/types.xml` | Oui | Règles d'apparition des objets -- votre modification la plus fréquente |
| `db/globals.xml` | Oui | Paramètres de réglage de l'économie |
| `db/events.xml` | Oui | Événements d'apparition véhicules/animaux |
| `db/economy.xml` | Oui | Interrupteurs des sous-systèmes de l'économie |
| `db/messages.xml` | Oui | Messages de diffusion du serveur |
| `cfggameplay.json` | Oui | Réglage du gameplay |
| `cfgspawnabletypes.xml` | Oui | Préréglages d'attachements/cargaison |
| `cfgrandompresets.xml` | Oui | Définitions des pools de loot |
| `cfglimitsdefinition.xml` | Oui | Ajouter des tags usage/valeur personnalisés |
| `cfgplayerspawnpoints.xml` | Oui | Emplacements d'apparition des joueurs |
| `cfgeventspawns.xml` | Oui | Coordonnées d'apparition des événements |
| `cfgignorelist.xml` | Oui | Exclure des objets de l'économie |
| `cfgweather.xml` | Oui | Schémas météorologiques |
| `cfgeffectarea.json` | Oui | Zones contaminées |
| `init.c` | Oui | Script d'entrée de la mission |
| `addons/` | **Non** | Écrasé lors des mises à jour |
| `dta/` | **Non** | Données moteur principales |
| `keys/` | Ajout uniquement | Copiez les fichiers `.bikey` des mods ici |
| `storage_1/` | Suppression uniquement | Persistance -- ne pas modifier manuellement |
| `battleye/` | **Non** | Anti-triche -- ne pas toucher |
| `mapgroup*.xml` | Avec précaution | Positions de loot des bâtiments -- modification avancée uniquement |

---

**Précédent :** [Installation du serveur](01-server-setup.md) | [Accueil](../README.md) | **Suivant :** [Référence serverDZ.cfg >>](03-server-cfg.md)
