# Chapter 9.5 : Apparition des véhicules et événements dynamiques

[Accueil](../README.md) | [<< Précédent : Économie du loot](04-loot-economy.md) | [Suivant : Apparition des joueurs >>](06-player-spawning.md)

---

> **Résumé :** Les véhicules et les événements dynamiques (crashs d'hélicoptères, convois, voitures de police) n'utilisent PAS `types.xml`. Ils utilisent un système séparé à trois fichiers : `events.xml` définit ce qui apparaît et en quelle quantité, `cfgeventspawns.xml` définit où, et `cfgeventgroups.xml` définit les formations groupées. Ce chapitre couvre les trois fichiers avec les valeurs vanilla réelles.

---

## Table des matières

- [Comment fonctionne l'apparition des véhicules](#comment-fonctionne-lapparition-des-véhicules)
- [Entrées de véhicules dans events.xml](#entrées-de-véhicules-dans-eventsxml)
- [Référence des champs d'événement véhicule](#référence-des-champs-dévénement-véhicule)
- [cfgeventspawns.xml -- Positions d'apparition](#cfgeventspawnsxml----positions-dapparition)
- [Événements de crash d'hélicoptère](#événements-de-crash-dhélicoptère)
- [Convoi militaire](#convoi-militaire)
- [Voiture de police](#voiture-de-police)
- [cfgeventgroups.xml -- Apparitions groupées](#cfgeventgroupsxml----apparitions-groupées)
- [Classe racine véhicule dans cfgeconomycore.xml](#classe-racine-véhicule-dans-cfgeconomycorexml)
- [Erreurs courantes](#erreurs-courantes)

---

## Comment fonctionne l'apparition des véhicules

Les véhicules ne sont **pas** définis dans `types.xml`. Si vous ajoutez une classe de véhicule à `types.xml`, il n'apparaîtra pas. Les véhicules utilisent un pipeline dédié à trois fichiers :

1. **`events.xml`** -- Définit chaque événement de véhicule : combien doivent exister sur la carte (nominal), quelles variantes peuvent apparaître (enfants), et les flags de comportement comme la durée de vie et le rayon de sécurité.

2. **`cfgeventspawns.xml`** -- Définit les positions physiques dans le monde où les événements de véhicule peuvent placer des entités. Chaque nom d'événement correspond à une liste d'entrées `<pos>` avec les coordonnées x, z et l'angle.

3. **`cfgeventgroups.xml`** -- Définit les apparitions groupées où plusieurs objets apparaissent ensemble avec des décalages de position relatifs (par ex. épaves de trains).

Le CE lit `events.xml`, choisit un événement qui a besoin d'apparaître, cherche les positions correspondantes dans `cfgeventspawns.xml`, en sélectionne une au hasard qui satisfait les contraintes `saferadius` et `distanceradius`, puis fait apparaître une entité enfant sélectionnée aléatoirement à cette position.

Les trois fichiers se trouvent dans `mpmissions/<votre_mission>/db/`.

---

## Entrées de véhicules dans events.xml

Chaque type de véhicule vanilla a sa propre entrée d'événement. Voici tous avec les valeurs réelles :

### Berline civile

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

### Tous les événements de véhicules vanilla

Tous les événements de véhicules utilisent la même structure que la Berline ci-dessus. Seules les valeurs diffèrent :

| Nom de l'événement | Nominal | Min | Max | Lifetime | Enfants (variantes) |
|--------------------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Variantes Hatchback02 |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Variantes Sedan02 |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | Variantes camion V3S |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- moins d'apparitions |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Bateaux -- compteur le plus élevé, durée de vie plus longue |

`VehicleOffroad02` a un nominal plus bas (3) que les autres véhicules terrestres (8). `VehicleBoat` a à la fois le nominal le plus élevé (22) et une durée de vie plus longue (600 vs 300).

---

## Référence des champs d'événement véhicule

### Champs au niveau de l'événement

| Champ | Type | Description |
|-------|------|-------------|
| `name` | string | Identifiant de l'événement. Doit correspondre à une entrée dans `cfgeventspawns.xml` quand `position="fixed"`. |
| `nominal` | int | Nombre cible d'instances actives de cet événement sur la carte. |
| `min` | int | Le CE tentera d'en faire apparaître davantage quand le compteur tombe en dessous. |
| `max` | int | Plafond absolu. Le CE ne dépassera jamais ce compteur. |
| `lifetime` | int | Secondes entre les vérifications de réapparition. Pour les véhicules, ce n'est PAS la durée de vie de persistance du véhicule -- c'est l'intervalle auquel le CE réévalue s'il faut apparaître ou nettoyer. |
| `restock` | int | Secondes minimum entre les tentatives de réapparition. 0 = prochain cycle. |
| `saferadius` | int | Distance minimum (mètres) de tout joueur pour que l'événement apparaisse. Empêche les véhicules d'apparaître devant les joueurs. |
| `distanceradius` | int | Distance minimum (mètres) entre deux instances du même événement. Empêche deux berlines d'apparaître l'une à côté de l'autre. |
| `cleanupradius` | int | Si un joueur est dans cette distance (mètres), l'entité de l'événement est protégée du nettoyage. |

### Flags

| Flag | Valeurs | Description |
|------|---------|-------------|
| `deletable` | 0, 1 | Si le CE peut supprimer cette entité d'événement. Les véhicules utilisent 0 (non supprimable par le CE). |
| `init_random` | 0, 1 | Randomiser les positions initiales à la première apparition. 0 = utiliser les positions fixes de `cfgeventspawns.xml`. |
| `remove_damaged` | 0, 1 | Supprimer l'entité quand elle devient ruinée. **Critique pour les véhicules** -- voir [Erreurs courantes](#erreurs-courantes). |

### Autres champs

| Champ | Valeurs | Description |
|-------|---------|-------------|
| `position` | `fixed`, `player` | `fixed` = apparaître aux positions de `cfgeventspawns.xml`. `player` = apparaître relativement aux positions des joueurs. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max appliqués par type d'enfant. `mixed` = min/max partagés entre tous les enfants. `custom` = comportement spécifique au moteur. |
| `active` | 0, 1 | Activer ou désactiver cet événement. 0 = l'événement est complètement ignoré. |

### Champs des enfants

| Attribut | Description |
|----------|-------------|
| `type` | Nom de classe de l'entité à faire apparaître. |
| `min` | Nombre minimum d'instances de cette variante. |
| `max` | Nombre maximum d'instances de cette variante. |
| `lootmin` | Nombre minimum d'objets de loot apparus à l'intérieur/autour de l'entité. 0 pour les véhicules (les pièces viennent de `cfgspawnabletypes.xml`). |
| `lootmax` | Nombre maximum d'objets de loot. Utilisé par les crashs d'hélicoptères et événements dynamiques, pas les véhicules. |

---

## cfgeventspawns.xml -- Positions d'apparition

Ce fichier associe les noms d'événements aux coordonnées du monde. Chaque bloc `<event>` contient une liste de positions d'apparition valides pour ce type d'événement. Quand le CE doit faire apparaître un véhicule, il choisit une position aléatoire de cette liste qui satisfait les contraintes `saferadius` et `distanceradius`.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... plus de positions ... -->
</event>
```

Chaque `<pos>` a trois attributs :

| Attribut | Description |
|----------|-------------|
| `x` | Coordonnée X du monde (position est-ouest sur la carte). |
| `z` | Coordonnée Z du monde (position nord-sud sur la carte). |
| `a` | Angle en degrés (0-360). La direction vers laquelle le véhicule est orienté à l'apparition. |

**Règles clés :**

- Si un événement n'a pas de bloc `<event>` correspondant dans `cfgeventspawns.xml`, il **n'apparaîtra pas** quelle que soit la configuration dans `events.xml`.
- Vous avez besoin d'au moins autant d'entrées `<pos>` que votre valeur `nominal`. Si vous définissez `nominal=8` mais n'avez que 3 positions, seulement 3 pourront apparaître.
- Les positions doivent être sur des routes ou un terrain plat. Une position à l'intérieur d'un bâtiment ou sur un terrain escarpé fera apparaître le véhicule enterré ou retourné.
- La valeur `a` (angle) détermine la direction du véhicule. Alignez-la avec la direction de la route pour des apparitions naturelles.

---

## Événements de crash d'hélicoptère

Les crashs d'hélicoptères sont des événements dynamiques qui font apparaître une épave avec du loot militaire et des infectés aux alentours. Ils utilisent le tag `<secondary>` pour définir les apparitions de zombies ambiants autour du site de crash.

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

### Différences clés avec les événements de véhicules

- **`<secondary>InfectedArmy</secondary>`** -- fait apparaître des zombies militaires autour du site de crash. Ce tag référence un groupe d'apparition d'infectés que le CE place aux environs.
- **`lootmin="10"` / `lootmax="15"`** -- l'épave apparaît avec 10-15 objets de loot d'événement dynamique. Ce sont des objets avec `deloot="1"` dans `types.xml` (équipement militaire, armes rares).
- **`lifetime=2100`** -- le crash persiste pendant 35 minutes avant que le CE le nettoie et en fasse apparaître un nouveau ailleurs.
- **`saferadius=1000`** -- les crashs n'apparaissent jamais à moins de 1 km d'un joueur.
- **`remove_damaged=0`** -- l'épave est déjà "endommagée" par définition, donc cela doit être à 0 sinon elle serait immédiatement nettoyée.

---

## Convoi militaire

Les convois militaires sont des groupes de véhicules épaves statiques qui apparaissent avec du loot militaire et des gardes infectés.

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

Les convois fonctionnent de manière identique aux crashs d'hélicoptères : le tag `<secondary>` fait apparaître `InfectedArmy` autour du site, et les objets de loot avec `deloot="1"` apparaissent sur les épaves. Avec `nominal=5`, jusqu'à 5 sites de convoi existent sur la carte simultanément. Chacun dure 1800 secondes (30 minutes) avant de se déplacer vers un nouvel emplacement.

---

## Voiture de police

Les événements de voitures de police font apparaître des véhicules de police épaves avec des infectés de type policier à proximité. Ils sont **désactivés par défaut**.

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

**`active=0`** signifie que cet événement est désactivé par défaut -- changez à `1` pour l'activer. Le tag `<secondary>InfectedPoliceHard</secondary>` fait apparaître des zombies policiers renforcés (plus résistants que les infectés standards). Avec `nominal=10` et `saferadius=500`, les voitures de police sont plus nombreuses mais moins précieuses que les crashs d'hélicoptères.

---

## cfgeventgroups.xml -- Apparitions groupées

Ce fichier définit les événements où plusieurs objets apparaissent ensemble avec des décalages de position relatifs. L'utilisation la plus courante est les trains abandonnés.

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

Le premier enfant est placé à la position de `cfgeventspawns.xml`. Les enfants suivants sont décalés par leurs valeurs `x`, `z`, `a` par rapport à cette origine. Dans cet exemple, les wagons sont espacés de 15 mètres le long de l'axe z.

Chaque `<child>` dans un groupe a :

| Attribut | Description |
|----------|-------------|
| `type` | Nom de classe de l'objet à faire apparaître. |
| `x` | Décalage en X en mètres depuis l'origine du groupe. |
| `z` | Décalage en Z en mètres depuis l'origine du groupe. |
| `a` | Décalage d'angle en degrés depuis l'origine du groupe. |

L'événement de groupe lui-même a toujours besoin d'une entrée correspondante dans `events.xml` pour contrôler les compteurs nominaux, la durée de vie et l'état actif.

---

## Classe racine véhicule dans cfgeconomycore.xml

Pour que le CE reconnaisse les véhicules comme des entités traçables, ils doivent avoir une déclaration de classe racine dans `cfgeconomycore.xml` :

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** est la classe de base pour tous les véhicules terrestres dans DayZ.
- **`BoatScript`** est la classe de base pour tous les bateaux.
- L'attribut `act="car"` indique au CE de traiter ces entités avec un comportement spécifique aux véhicules (persistance, apparition basée sur les événements).

Sans ces entrées de classe racine, le CE ne suivrait pas et ne gérerait pas les instances de véhicules. Si vous ajoutez un véhicule moddé qui hérite d'une classe de base différente, vous devrez peut-être ajouter sa classe racine ici.

---

## Erreurs courantes

Ce sont les problèmes d'apparition de véhicules les plus fréquents rencontrés par les administrateurs de serveur.

### Mettre les véhicules dans types.xml

**Problème :** Vous ajoutez `CivilianSedan` à `types.xml` avec un nominal de 10. Aucune berline n'apparaît.

**Solution :** Retirez le véhicule de `types.xml`. Ajoutez ou modifiez l'événement de véhicule dans `events.xml` avec les enfants appropriés, et assurez-vous que des positions d'apparition correspondantes existent dans `cfgeventspawns.xml`. Les véhicules utilisent le système d'événements, pas le système d'apparition d'objets.

### Pas de positions d'apparition correspondantes dans cfgeventspawns.xml

**Problème :** Vous créez un nouvel événement de véhicule dans `events.xml` mais le véhicule n'apparaît jamais.

**Solution :** Ajoutez un bloc `<event name="VotreNomDEvenement">` correspondant dans `cfgeventspawns.xml` avec suffisamment d'entrées `<pos>`. Le `name` de l'événement dans les deux fichiers doit correspondre exactement. Vous avez besoin d'au moins autant de positions que votre valeur `nominal`.

### Mettre remove_damaged=0 pour les véhicules conduisibles

**Problème :** Vous mettez `remove_damaged="0"` sur un événement de véhicule. Au fil du temps, le serveur se remplit de véhicules épaves qui ne disparaissent jamais, bloquant les positions d'apparition et dégradant les performances.

**Solution :** Gardez `remove_damaged="1"` pour tous les véhicules conduisibles (berlines, camions, hatchbacks, bateaux). Cela garantit que lorsqu'un véhicule est détruit, le CE le supprime et en fait apparaître un neuf. Ne mettez `remove_damaged="0"` que pour les objets épaves (crashs d'hélicoptères, convois) qui sont déjà endommagés de par leur conception.

### Oublier de mettre active=1

**Problème :** Vous configurez un événement de véhicule mais il n'apparaît jamais.

**Solution :** Vérifiez le tag `<active>`. S'il est à `0`, l'événement est désactivé. Certains événements vanilla comme `StaticPoliceCar` sont livrés avec `active=0`. Mettez-le à `1` pour activer l'apparition.

### Pas assez de positions d'apparition pour le nombre nominal

**Problème :** Vous mettez `nominal=15` pour un événement de véhicule mais seulement 6 positions existent dans `cfgeventspawns.xml`. Seulement 6 véhicules apparaissent.

**Solution :** Ajoutez plus d'entrées `<pos>`. En règle générale, incluez au moins 2-3x votre valeur nominale en positions pour donner au CE suffisamment d'options pour satisfaire les contraintes `saferadius` et `distanceradius`.

### Le véhicule apparaît à l'intérieur de bâtiments ou sous terre

**Problème :** Un véhicule apparaît clippé dans un bâtiment ou enterré dans le terrain.

**Solution :** Examinez les coordonnées `<pos>` dans `cfgeventspawns.xml`. Testez les positions en jeu en utilisant la téléportation admin avant de les ajouter au fichier. Les positions doivent être sur des routes plates ou un terrain dégagé, et l'angle (`a`) doit être aligné avec la direction de la route.

---

[Accueil](../README.md) | [<< Précédent : Économie du loot](04-loot-economy.md) | [Suivant : Apparition des joueurs >>](06-player-spawning.md)
