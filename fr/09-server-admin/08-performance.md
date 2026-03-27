# Chapter 9.8 : Optimisation des performances

[Accueil](../README.md) | [<< Précédent : Persistance](07-persistence.md) | [Suivant : Contrôle d'accès >>](09-access-control.md)

---

> **Résumé :** Les performances du serveur DayZ se résument à trois facteurs : le nombre d'objets, les événements dynamiques, et la charge des mods/joueurs. Ce chapitre couvre les paramètres spécifiques qui comptent, comment diagnostiquer les problèmes, et quel matériel aide réellement -- le tout basé sur des données réelles de la communauté provenant de plus de 400 rapports Discord de baisses de FPS, lag et désynchronisation.

---

## Table des matières

- [Ce qui affecte les performances du serveur](#ce-qui-affecte-les-performances-du-serveur)
- [Réglage de globals.xml](#réglage-de-globalsxml)
- [Réglage de l'économie pour les performances](#réglage-de-léconomie-pour-les-performances)
- [Journalisation de cfgeconomycore.xml](#journalisation-de-cfgeconomycorexml)
- [Paramètres de performance de serverDZ.cfg](#paramètres-de-performance-de-serverdzcfg)
- [Impact des mods sur les performances](#impact-des-mods-sur-les-performances)
- [Recommandations matérielles](#recommandations-matérielles)
- [Surveiller la santé du serveur](#surveiller-la-santé-du-serveur)
- [Erreurs de performance courantes](#erreurs-de-performance-courantes)

---

## Ce qui affecte les performances du serveur

D'après les données communautaires (plus de 400 mentions Discord de FPS/performance/lag/désync), les trois plus grands facteurs de performance sont :

1. **Nombre d'objets** -- des valeurs `nominal` élevées dans `types.xml` signifient que l'Économie Centrale suit et traite plus d'objets à chaque cycle. C'est systématiquement la cause numéro un du lag côté serveur.
2. **Apparition d'événements** -- trop d'événements dynamiques actifs (véhicules, animaux, crashs d'hélicoptères) dans `events.xml` consomment des cycles d'apparition/nettoyage et des emplacements d'entités.
3. **Nombre de joueurs + nombre de mods** -- chaque joueur connecté génère des mises à jour d'entités, et chaque mod ajoute des classes de script que le moteur doit compiler et exécuter à chaque tick.

La boucle de jeu du serveur fonctionne à un taux fixe de 30 FPS. Quand le serveur ne peut pas maintenir 30 FPS, les joueurs subissent de la désynchronisation -- téléportations, ramassages d'objets retardés et échecs de détection des hits. En dessous de 15 FPS serveur, le jeu devient injouable.

---

## Réglage de globals.xml

Voici les valeurs vanilla par défaut pour les paramètres qui affectent directement les performances :

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### Ce que chaque valeur contrôle

| Paramètre | Défaut | Effet sur les performances |
|-----------|--------|---------------------------|
| `ZombieMaxCount` | 1000 | Plafond pour le total d'infectés sur le serveur. Chaque zombie fait tourner le pathfinding IA. Réduire à 500-700 améliore sensiblement les FPS serveur sur les serveurs peuplés. |
| `AnimalMaxCount` | 200 | Plafond pour les animaux. Les animaux ont une IA plus simple que les zombies mais consomment quand même du temps de tick. Réduisez à 100 si vous constatez des problèmes de FPS. |
| `ZoneSpawnDist` | 300 | Distance en mètres à laquelle les zones de zombies s'activent autour des joueurs. Réduire à 200 signifie moins de zones simultanément actives. |
| `SpawnInitial` | 1200 | Nombre d'objets que le CE fait apparaître au premier démarrage. Des valeurs plus élevées signifient un chargement initial plus long. N'affecte pas les performances en régime permanent. |
| `CleanupLifetimeDefault` | 45 | Temps de nettoyage par défaut en secondes pour les objets sans durée de vie spécifique. Des valeurs plus basses signifient des cycles de nettoyage plus rapides mais un traitement CE plus fréquent. |

**Profil de performance recommandé** (pour les serveurs en difficulté au-dessus de 40 joueurs) :

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Réglage de l'économie pour les performances

L'Économie Centrale fonctionne en boucle continue, vérifiant chaque type d'objet par rapport à ses cibles `nominal`/`min`. Plus de types d'objets avec des nominaux élevés signifie plus de travail par cycle.

### Réduire les valeurs nominales

Chaque objet dans `types.xml` avec `nominal > 0` est suivi par le CE. Si vous avez 2000 types d'objets avec un nominal moyen de 20, le CE gère 40 000 objets. Réduisez les nominaux sur l'ensemble pour diminuer ce nombre :

- Objets civils courants : réduire de 15-40 à 10-25
- Armes : garder bas (le vanilla est déjà à 2-10)
- Variantes de vêtements : envisagez de désactiver les variantes de couleur dont vous n'avez pas besoin (`nominal=0`)

### Réduire les événements dynamiques

Dans `events.xml`, chaque événement actif fait apparaître et surveille des groupes d'entités. Réduisez le `nominal` des événements de véhicules et d'animaux, ou mettez `<active>0</active>` sur les événements dont vous n'avez pas besoin.

### Utiliser le mode veille

Quand aucun joueur n'est connecté, le CE peut se mettre en pause :

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` signifie que le serveur entre en mode veille 60 secondes après la déconnexion du dernier joueur. `IdleModeStartup=1` signifie que le serveur démarre en mode veille et n'active le CE que lorsque le premier joueur se connecte. Cela empêche le serveur de tourner dans des cycles d'apparition à vide.

### Régler le taux de réapparition

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Ces paramètres contrôlent combien d'objets et de types d'objets le CE traite par cycle. Des valeurs plus basses réduisent la charge CE par tick mais ralentissent la réapparition du loot. Les valeurs vanilla par défaut ci-dessus sont déjà conservatrices.

---

## Journalisation de cfgeconomycore.xml

Activez temporairement les logs de diagnostic du CE pour mesurer les temps de cycle et identifier les goulots d'étranglement. Dans votre `cfgeconomycore.xml` :

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Pour diagnostiquer les performances, mettez `log_ce_statistics` à `"true"`. Cela produit des timings de cycle CE dans le log RPT du serveur. Cherchez les lignes montrant combien de temps chaque cycle CE prend -- si les cycles dépassent 1000 ms, l'économie est surchargée.

Mettez `log_ce_lootspawn` et `log_ce_lootcleanup` à `"true"` pour voir quels types d'objets apparaissent et sont nettoyés le plus fréquemment. Ce sont vos candidats pour la réduction du nominal.

**Désactivez la journalisation après le diagnostic.** Les écritures de log elles-mêmes consomment des E/S et peuvent aggraver les performances si elles restent activées en permanence.

---

## Paramètres de performance de serverDZ.cfg

Le fichier de configuration principal du serveur a des options limitées liées aux performances :

| Paramètre | Effet |
|-----------|-------|
| `maxPlayers` | Réduisez si le serveur peine. Chaque joueur génère du trafic réseau et des mises à jour d'entités. Passer de 60 à 40 joueurs peut récupérer 5-10 FPS serveur. |
| `instanceId` | Détermine le chemin de `storage_1/`. Pas un paramètre de performance, mais si votre stockage est sur un disque lent, cela affecte les E/S de persistance. |

**Ce que vous ne pouvez pas changer :** le taux de tick du serveur est fixé à 30 FPS. Il n'y a aucun paramètre pour l'augmenter ou le diminuer. Si le serveur ne peut pas maintenir 30 FPS, il tourne simplement plus lentement.

---

## Impact des mods sur les performances

Chaque mod ajoute des classes de script que le moteur compile au démarrage et exécute à chaque tick. L'impact varie considérablement selon la qualité du mod :

- **Mods de contenu uniquement** (armes, vêtements, bâtiments) ajoutent des types d'objets mais un minimum de charge script. Leur coût est dans le suivi CE, pas le traitement par tick.
- **Mods à scripts lourds** avec des boucles `OnUpdate()` ou `OnTick()` exécutent du code à chaque frame serveur. Des boucles mal optimisées dans ces mods sont la cause la plus courante de lag lié aux mods.
- **Mods de trading/économie** qui maintiennent de grands inventaires ajoutent des objets persistants que le moteur doit suivre.

### Lignes directrices

- Ajoutez les mods progressivement. Testez les FPS serveur après chaque ajout, pas après en avoir ajouté 10 d'un coup.
- Surveillez les FPS serveur avec les outils admin ou la sortie du log RPT après l'ajout de nouveaux mods.
- Si un mod cause des problèmes, vérifiez son code source pour des opérations coûteuses par frame.

Consensus communautaire : "Les objets (types) et l'apparition d'événements sont les plus exigeants -- les mods qui ajoutent des milliers d'entrées types.xml font plus de mal que les mods qui ajoutent des scripts complexes."

---

## Recommandations matérielles

La logique de jeu du serveur DayZ est **mono-thread**. Les CPU multi-cœurs aident avec la surcharge OS et les E/S réseau, mais la boucle de jeu principale tourne sur un seul cœur.

| Composant | Recommandation | Pourquoi |
|-----------|---------------|----------|
| **CPU** | Les meilleures performances mono-thread possibles. AMD 5600X ou mieux. | La boucle de jeu est mono-thread. La fréquence d'horloge et l'IPC comptent plus que le nombre de cœurs. |
| **RAM** | 8 Go minimum, 12-16 Go pour les serveurs fortement moddés | Les mods et les grandes cartes consomment de la mémoire. En manquer cause des saccades. |
| **Stockage** | SSD requis | Les E/S de persistance de `storage_1/` sont constantes. Un HDD cause des micro-freezes pendant les cycles de sauvegarde. |
| **Réseau** | 100 Mbps+ avec faible latence | La bande passante compte moins que la stabilité du ping pour la prévention de la désynchronisation. |

Conseil communautaire : "OVH offre un bon rapport qualité-prix -- environ 60 USD pour une machine dédiée 5600X qui gère les serveurs moddés de 60 joueurs."

Évitez l'hébergement partagé/VPS pour les serveurs peuplés. Le problème du voisin bruyant sur du matériel partagé cause des baisses de FPS imprévisibles impossibles à diagnostiquer de votre côté.

---

## Surveiller la santé du serveur

### FPS du serveur

Vérifiez le log RPT pour les lignes contenant les FPS serveur. Un serveur sain maintient 30 FPS de manière constante. Seuils d'alerte :

| FPS serveur | Statut |
|-------------|--------|
| 25-30 | Normal. Des fluctuations mineures sont attendues pendant les combats intenses ou les redémarrages. |
| 15-25 | Dégradé. Les joueurs remarquent la désynchronisation sur les interactions d'objets et les combats. |
| En dessous de 15 | Critique. Téléportations, actions échouées, détection des hits cassée. |

### Avertissements de cycle CE

Avec `log_ce_statistics` activé, surveillez les temps de cycle CE. La norme est en dessous de 500 ms. Si les cycles dépassent régulièrement 1000 ms, votre économie est trop lourde.

### Croissance du stockage

Surveillez la taille de `storage_1/`. Une croissance non contrôlée indique un gonflement de la persistance -- trop d'objets placés, tentes ou caches qui s'accumulent. Des wipes de serveur réguliers ou la réduction de `FlagRefreshMaxDuration` dans `globals.xml` aident à contrôler cela.

### Rapports des joueurs

Les rapports de désynchronisation des joueurs sont votre indicateur temps réel le plus fiable. Si plusieurs joueurs signalent des téléportations simultanément, les FPS serveur sont tombés en dessous de 15.

---

## Erreurs de performance courantes

### Valeurs nominales trop élevées

Mettre chaque objet à `nominal=50` parce que "plus de loot c'est fun" crée des dizaines de milliers d'objets suivis. Le CE passe tout son cycle à gérer les objets au lieu de faire tourner le jeu. Commencez avec les nominaux vanilla et augmentez sélectivement.

### Trop d'événements de véhicules

Les véhicules sont des entités coûteuses avec simulation physique, suivi des attachements et persistance. Le vanilla fait apparaître environ 50 véhicules au total. Les serveurs avec 150+ véhicules constatent une perte de FPS significative.

### Exécuter 30+ mods sans tester

Chaque mod est correct isolément. L'effet cumulé de 30+ mods -- des milliers de types supplémentaires, des dizaines de scripts par frame, et une pression mémoire accrue -- peut faire baisser les FPS serveur de 50% ou plus. Ajoutez les mods par lots de 3-5 et testez après chaque lot.

### Ne jamais redémarrer le serveur

Certains mods ont des fuites mémoire qui s'accumulent avec le temps. Programmez des redémarrages automatiques toutes les 4-6 heures. La plupart des panneaux d'hébergement de serveurs supportent cela. Même les mods bien écrits bénéficient de redémarrages périodiques car la fragmentation mémoire du moteur augmente au fil des longues sessions.

### Ignorer le gonflement du stockage

Un dossier `storage_1/` qui atteint plusieurs gigaoctets ralentit chaque cycle de persistance. Faites un wipe ou réduisez-le périodiquement, surtout si vous autorisez la construction de bases sans limites de dégradation.

### Journalisation laissée activée

La journalisation de diagnostic CE, la journalisation de débogage des scripts, et la journalisation des outils admin écrivent toutes sur le disque à chaque tick. Activez-les pour le diagnostic, puis désactivez-les. Une journalisation verbeuse permanente sur un serveur occupé peut coûter 1-2 FPS à elle seule.

---

[Accueil](../README.md) | [<< Précédent : Persistance](07-persistence.md) | [Suivant : Contrôle d'accès >>](09-access-control.md)
