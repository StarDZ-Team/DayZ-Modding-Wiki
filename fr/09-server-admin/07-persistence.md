# Chapter 9.7 : État du monde et persistance

[Accueil](../README.md) | [<< Précédent : Apparition des joueurs](06-player-spawning.md) | [Suivant : Optimisation des performances >>](08-performance.md)

La persistance de DayZ maintient le monde en vie entre les redémarrages. Comprendre son fonctionnement vous permet de gérer les bases, planifier les wipes et éviter la corruption des données.

## Table des matières

- [Comment fonctionne la persistance](#comment-fonctionne-la-persistance)
- [Le répertoire storage_1/](#le-répertoire-storage_1)
- [Paramètres de persistance de globals.xml](#paramètres-de-persistance-de-globalsxml)
- [Système de drapeaux de territoire](#système-de-drapeaux-de-territoire)
- [Objets Hoarder](#objets-hoarder)
- [Paramètres de persistance de cfggameplay.json](#paramètres-de-persistance-de-cfggameplayjson)
- [Procédures de wipe du serveur](#procédures-de-wipe-du-serveur)
- [Stratégie de sauvegarde](#stratégie-de-sauvegarde)
- [Erreurs courantes](#erreurs-courantes)

---

## Comment fonctionne la persistance

DayZ stocke l'état du monde dans le répertoire `storage_1/` à l'intérieur de votre dossier de profil serveur. Le cycle est simple :

1. Le serveur sauvegarde l'état du monde périodiquement (par défaut environ toutes les 30 minutes) et lors d'un arrêt propre.
2. Au redémarrage, le serveur lit `storage_1/` et restaure tous les objets persistants -- véhicules, bases, tentes, barils, inventaires des joueurs.
3. Les objets sans persistance (la plupart du loot au sol) sont régénérés par l'Économie Centrale à chaque redémarrage.

Si `storage_1/` n'existe pas au démarrage, le serveur crée un monde vierge sans données de joueurs et sans structures construites.

---

## Le répertoire storage_1/

Votre profil serveur contient `storage_1/` avec ces sous-répertoires et fichiers :

| Chemin | Contenu |
|--------|---------|
| `data/` | Fichiers binaires contenant les objets du monde -- pièces de base, objets placés, positions des véhicules |
| `players/` | Fichiers **.save** par joueur indexés par SteamID64. Chaque fichier stocke la position, l'inventaire, la santé, les effets de statut |
| `snapshot/` | Instantanés de l'état du monde utilisés pendant les opérations de sauvegarde |
| `events.bin` / `events.xy` | État des événements dynamiques -- suit les emplacements des crashs d'hélicoptères, positions de convois et autres événements apparus |

Le dossier `data/` constitue l'essentiel de la persistance. Il contient des données d'objets sérialisées que le serveur lit au démarrage pour reconstruire le monde.

---

## Paramètres de persistance de globals.xml

Le fichier **globals.xml** (dans votre dossier de mission) contrôle les timers de nettoyage et le comportement des drapeaux. Voici les valeurs liées à la persistance :

```xml
<!-- Rafraîchissement du drapeau de territoire -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 jours (secondes) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 jours (secondes) -->

<!-- Timers de nettoyage -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Nettoyage par défaut (secondes) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Corps de joueur mort : 1 heure -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Animal mort : 20 minutes -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Zombie mort : 5,5 minutes -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Objet ruiné : 5,5 minutes -->

<!-- Comportement de nettoyage -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Max d'objets nettoyés par cycle -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Pas de nettoyage dans un rayon de 100 m d'un joueur -->
```

La valeur `CleanupAvoidance` empêche le serveur de faire disparaître des objets proches des joueurs actifs. Si un corps mort se trouve à moins de 100 mètres de n'importe quel joueur, il reste en place jusqu'à ce que le joueur s'éloigne ou que le timer se réinitialise.

---

## Système de drapeaux de territoire

Les drapeaux de territoire sont le fondement de la persistance des bases dans DayZ. Voici comment les deux valeurs clés interagissent :

- **FlagRefreshFrequency** (`432000` secondes = 5 jours) -- À quelle fréquence vous devez interagir avec votre drapeau pour le maintenir actif. Approchez-vous du drapeau et utilisez l'action "Rafraîchir".
- **FlagRefreshMaxDuration** (`3456000` secondes = 40 jours) -- Le temps de protection accumulé maximum. Chaque rafraîchissement ajoute jusqu'à FlagRefreshFrequency de temps, mais le total ne peut pas dépasser ce plafond.

Quand le timer d'un drapeau expire :

1. Le drapeau lui-même devient éligible au nettoyage.
2. Toutes les pièces de construction de base attachées à ce drapeau perdent leur protection de persistance.
3. Au prochain cycle de nettoyage, les pièces non protégées commencent à disparaître.

Si vous réduisez FlagRefreshFrequency, les joueurs doivent visiter leurs bases plus souvent. Si vous augmentez FlagRefreshMaxDuration, les bases survivent plus longtemps entre les visites. Ajustez les deux valeurs ensemble pour correspondre au style de jeu de votre serveur.

---

## Objets Hoarder

Dans **cfgspawnabletypes.xml**, certains conteneurs sont marqués avec `<hoarder/>`. Cela les identifie comme des objets de cache qui comptent dans les limites de stockage par joueur de l'Économie Centrale.

Les objets hoarder vanilla sont :

| Objet | Type |
|-------|------|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Barils de stockage |
| CarTent, LargeTent, MediumTent, PartyTent | Tentes |
| SeaChest | Stockage sous-marin |
| SmallProtectorCase | Petit coffre verrouillable |
| UndergroundStash | Cache enterrée |
| WoodenCrate | Caisse artisanale |

Exemple de **cfgspawnabletypes.xml** :

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

Le serveur suit combien d'objets hoarder chaque joueur a placés. Quand la limite est atteinte, les nouveaux placements échouent ou l'objet le plus ancien disparaît (selon la configuration du serveur).

---

## Paramètres de persistance de cfggameplay.json

Le fichier **cfggameplay.json** dans votre dossier de mission contient des paramètres qui affectent la durabilité des bases et conteneurs :

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Paramètre | Défaut | Effet |
|-----------|--------|-------|
| `disableBaseDamage` | `false` | À `true`, les pièces de construction (murs, portails, tours de guet) ne peuvent pas être endommagées. Cela désactive effectivement le raid. |
| `disableContainerDamage` | `false` | À `true`, les conteneurs de stockage (tentes, barils, caisses) ne peuvent pas subir de dégâts. Les objets à l'intérieur restent en sécurité. |

Mettre les deux à `true` crée un serveur PvE où les bases et le stockage sont indestructibles. La plupart des serveurs PvP laissent les deux à `false`.

---

## Procédures de wipe du serveur

Vous avez quatre types de wipe, chacun ciblant une partie différente de `storage_1/`. **Arrêtez toujours le serveur avant d'effectuer tout wipe.**

### Wipe complet

Supprimez l'intégralité du dossier `storage_1/`. Le serveur crée un monde vierge au prochain démarrage. Toutes les bases, véhicules, tentes, données joueurs et états d'événements sont effacés.

### Wipe de l'économie (conserver les joueurs)

Supprimez `storage_1/data/` mais laissez `storage_1/players/` intact. Les joueurs conservent leurs personnages et inventaires, mais tous les objets placés (bases, tentes, barils, véhicules) sont supprimés.

### Wipe des joueurs (conserver le monde)

Supprimez `storage_1/players/`. Tous les personnages joueurs sont réinitialisés en apparitions fraîches. Les bases et objets placés restent dans le monde.

### Réinitialisation météo / événements

Supprimez `events.bin` ou `events.xy` de `storage_1/`. Cela réinitialise les positions des événements dynamiques (crashs d'hélicoptères, convois). Le serveur génère de nouveaux emplacements d'événements au prochain démarrage.

---

## Stratégie de sauvegarde

Les données de persistance sont irremplaçables une fois perdues. Suivez ces pratiques :

- **Sauvegardez à l'arrêt.** Copiez l'intégralité du dossier `storage_1/` pendant que le serveur ne tourne pas. Copier pendant l'exécution risque de capturer un état partiel ou corrompu.
- **Planifiez les sauvegardes avant les redémarrages.** Si vous exécutez des redémarrages automatiques (toutes les 4-6 heures), ajoutez une étape de sauvegarde à votre script de redémarrage qui copie `storage_1/` avant le démarrage du processus serveur.
- **Conservez plusieurs générations.** Faites tourner les sauvegardes pour en avoir au moins 3 récentes. Si votre dernière sauvegarde est corrompue, vous pouvez revenir à une plus ancienne.
- **Stockez hors machine.** Copiez les sauvegardes sur un disque séparé ou un stockage cloud. Une panne de disque sur la machine serveur emporte vos sauvegardes si elles sont sur le même disque.

Un script de sauvegarde minimal (s'exécute avant le démarrage du serveur) :

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Erreurs courantes

Ces problèmes reviennent régulièrement dans les communautés d'administrateurs de serveurs :

| Erreur | Conséquence | Prévention |
|--------|-------------|------------|
| Supprimer `storage_1/` pendant que le serveur tourne | Corruption des données. Le serveur écrit dans des fichiers qui n'existent plus, causant des crashs ou un état partiel au prochain démarrage. | Toujours arrêter le serveur d'abord. |
| Ne pas sauvegarder avant un wipe | Si vous supprimez accidentellement le mauvais dossier ou si le wipe tourne mal, il n'y a pas de récupération possible. | Sauvegarder `storage_1/` avant chaque wipe. |
| Confondre réinitialisation météo et wipe complet | Supprimer `events.xy` réinitialise uniquement les positions des événements dynamiques. Cela ne réinitialise pas le loot, les bases ou les joueurs. | Savoir quels fichiers contrôlent quoi (voir le tableau du répertoire ci-dessus). |
| Drapeau non rafraîchi à temps | Après 40 jours (FlagRefreshMaxDuration), le drapeau expire et toutes les pièces de base attachées deviennent éligibles au nettoyage. Les joueurs perdent toute leur base. | Rappeler aux joueurs l'intervalle de rafraîchissement. Réduire FlagRefreshMaxDuration sur les serveurs à faible population. |
| Modifier globals.xml pendant que le serveur tourne | Les changements ne sont pas pris en compte jusqu'au redémarrage. Pire, le serveur peut écraser vos modifications à l'arrêt. | Modifier les fichiers de configuration uniquement quand le serveur est arrêté. |

---

[Accueil](../README.md) | [<< Précédent : Apparition des joueurs](06-player-spawning.md) | [Suivant : Optimisation des performances >>](08-performance.md)
