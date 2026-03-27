# Chapter 9.3 : Référence complète de serverDZ.cfg

[Accueil](../README.md) | [<< Précédent : Structure des répertoires](02-directory-structure.md) | **Référence serverDZ.cfg** | [Suivant : Économie du loot en profondeur >>](04-loot-economy.md)

---

> **Résumé :** Chaque paramètre de `serverDZ.cfg` documenté avec son objectif, ses valeurs valides et son comportement par défaut. Ce fichier contrôle l'identité du serveur, les paramètres réseau, les règles de gameplay, l'accélération du temps et la sélection de mission.

---

## Table des matières

- [Format du fichier](#format-du-fichier)
- [Identité du serveur](#identité-du-serveur)
- [Réseau et sécurité](#réseau-et-sécurité)
- [Règles de gameplay](#règles-de-gameplay)
- [Temps et météo](#temps-et-météo)
- [Performance et file de connexion](#performance-et-file-de-connexion)
- [Persistance et instance](#persistance-et-instance)
- [Sélection de la mission](#sélection-de-la-mission)
- [Exemple de fichier complet](#exemple-de-fichier-complet)
- [Paramètres de lancement qui remplacent la configuration](#paramètres-de-lancement-qui-remplacent-la-configuration)

---

## Format du fichier

`serverDZ.cfg` utilise le format de configuration Bohemia (similaire au C). Règles :

- Chaque assignation de paramètre se termine par un **point-virgule** `;`
- Les chaînes sont entourées de **guillemets doubles** `""`
- Les commentaires utilisent `//` pour une seule ligne
- Le bloc `class Missions` utilise des accolades `{}` et se termine par `};`
- Le fichier doit être encodé en UTF-8 ou ANSI -- pas de BOM

Un point-virgule manquant fera échouer silencieusement le serveur ou ignorer les paramètres suivants.

---

## Identité du serveur

```cpp
hostname = "My DayZ Server";         // Nom du serveur affiché dans le navigateur
password = "";                       // Mot de passe pour se connecter (vide = public)
passwordAdmin = "";                  // Mot de passe pour la connexion admin via la console en jeu
description = "";                    // Description affichée dans les détails du navigateur de serveurs
```

| Paramètre | Type | Défaut | Notes |
|-----------|------|--------|-------|
| `hostname` | string | `""` | Affiché dans le navigateur de serveurs. Maximum ~100 caractères. |
| `password` | string | `""` | Laissez vide pour un serveur public. Les joueurs doivent entrer ce mot de passe pour rejoindre. |
| `passwordAdmin` | string | `""` | Utilisé avec la commande `#login` en jeu. **Définissez-le sur chaque serveur.** |
| `description` | string | `""` | Les descriptions multi-lignes ne sont pas supportées. Restez concis. |

---

## Réseau et sécurité

```cpp
maxPlayers = 60;                     // Nombre maximum de places joueurs
verifySignatures = 2;                // Vérification des signatures PBO (seul 2 est supporté)
forceSameBuild = 1;                  // Exiger la même version client/serveur de l'exécutable
enableWhitelist = 0;                 // Activer/désactiver la liste blanche
disableVoN = 0;                      // Désactiver la voix sur réseau
vonCodecQuality = 20;               // Qualité audio VoN (0-30)
guaranteedUpdates = 1;               // Protocole réseau (toujours utiliser 1)
```

| Paramètre | Type | Valeurs valides | Défaut | Notes |
|-----------|------|----------------|--------|-------|
| `maxPlayers` | int | 1-60 | 60 | Affecte l'utilisation de la RAM. Chaque joueur ajoute ~50-100 Mo. |
| `verifySignatures` | int | 2 | 2 | Seule la valeur 2 est supportée. Vérifie les fichiers PBO par rapport aux clés `.bisign`. |
| `forceSameBuild` | int | 0, 1 | 1 | À 1, les clients doivent correspondre à la version exacte de l'exécutable du serveur. Toujours garder à 1. |
| `enableWhitelist` | int | 0, 1 | 0 | À 1, seuls les Steam64 IDs listés dans `whitelist.txt` peuvent se connecter. |
| `disableVoN` | int | 0, 1 | 0 | Mettez à 1 pour désactiver complètement le chat vocal en jeu. |
| `vonCodecQuality` | int | 0-30 | 20 | Des valeurs plus élevées signifient une meilleure qualité vocale mais plus de bande passante. 20 est un bon équilibre. |
| `guaranteedUpdates` | int | 1 | 1 | Paramètre du protocole réseau. Toujours utiliser 1. |

### Shard ID

```cpp
shardId = "123abc";                  // Six caractères alphanumériques pour les shards privés
```

| Paramètre | Type | Défaut | Notes |
|-----------|------|--------|-------|
| `shardId` | string | `""` | Utilisé pour les serveurs hive privés. Les joueurs sur des serveurs avec le même `shardId` partagent les données de personnage. Laissez vide pour un hive public. |

---

## Règles de gameplay

```cpp
disable3rdPerson = 0;               // Désactiver la caméra troisième personne
disableCrosshair = 0;               // Désactiver le réticule
disablePersonalLight = 1;           // Désactiver la lumière ambiante du joueur
lightingConfig = 0;                 // Luminosité nocturne (0 = plus lumineux, 1 = plus sombre)
```

| Paramètre | Type | Valeurs valides | Défaut | Notes |
|-----------|------|----------------|--------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | Mettez à 1 pour les serveurs première personne uniquement. C'est le paramètre "hardcore" le plus courant. |
| `disableCrosshair` | int | 0, 1 | 0 | Mettez à 1 pour supprimer le réticule. Souvent associé à `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | La "lumière personnelle" est un léger halo autour du joueur la nuit. La plupart des serveurs la désactivent (valeur 1) pour le réalisme. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = nuits plus lumineuses (clair de lune visible). 1 = nuits noires totales (nécessite lampe torche/NVG). |

---

## Temps et météo

```cpp
serverTime = "SystemTime";                 // Heure initiale
serverTimeAcceleration = 12;               // Multiplicateur de vitesse du temps (0-24)
serverNightTimeAcceleration = 1;           // Multiplicateur de vitesse du temps nocturne (0.1-64)
serverTimePersistent = 0;                  // Sauvegarder le temps entre les redémarrages
```

| Paramètre | Type | Valeurs valides | Défaut | Notes |
|-----------|------|----------------|--------|-------|
| `serverTime` | string | `"SystemTime"` ou `"YYYY/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` utilise l'horloge locale de la machine. Définissez une heure fixe comme `"2024/9/15/12/0"` pour un serveur en jour permanent. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Multiplicateur pour le temps en jeu. À 12, un cycle complet de 24 heures dure 2 heures réelles. À 1, le temps est réel. À 24, un jour complet passe en 1 heure. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Multiplié par `serverTimeAcceleration`. Avec une valeur de 4 et une accélération de 12, la nuit passe à une vitesse de 48x (nuits très courtes). |
| `serverTimePersistent` | int | 0, 1 | 0 | À 1, le serveur sauvegarde son horloge en jeu sur disque et reprend à partir de celle-ci après redémarrage. À 0, le temps revient à `serverTime` à chaque redémarrage. |

### Configurations temporelles courantes

**Toujours en journée :**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Cycle jour/nuit rapide (journées de 2 heures, nuits courtes) :**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Jour/nuit en temps réel :**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Performance et file de connexion

```cpp
loginQueueConcurrentPlayers = 5;     // Joueurs traités en même temps lors de la connexion
loginQueueMaxPlayers = 500;          // Taille maximale de la file de connexion
```

| Paramètre | Type | Défaut | Notes |
|-----------|------|--------|-------|
| `loginQueueConcurrentPlayers` | int | 5 | Combien de joueurs peuvent charger simultanément. Des valeurs plus basses réduisent les pics de charge serveur après un redémarrage. Augmentez à 10-15 si votre matériel est puissant et que les joueurs se plaignent des temps d'attente. |
| `loginQueueMaxPlayers` | int | 500 | Si ce nombre de joueurs est déjà en file d'attente, les nouvelles connexions sont refusées. 500 convient à la plupart des serveurs. |

---

## Persistance et instance

```cpp
instanceId = 1;                      // Identifiant d'instance du serveur
storageAutoFix = 1;                  // Réparation automatique des fichiers de persistance corrompus
```

| Paramètre | Type | Défaut | Notes |
|-----------|------|--------|-------|
| `instanceId` | int | 1 | Identifie l'instance du serveur. Les données de persistance sont stockées dans `storage_<instanceId>/`. Si vous exécutez plusieurs serveurs sur la même machine, donnez à chacun un `instanceId` différent. |
| `storageAutoFix` | int | 1 | À 1, le serveur vérifie les fichiers de persistance au démarrage et remplace ceux qui sont corrompus par des fichiers vides. Toujours laisser à 1. |

---

## Sélection de la mission

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

La valeur `template` doit correspondre exactement à un nom de dossier dans `mpmissions/`. Missions vanilla disponibles :

| Template | Carte | DLC requis |
|----------|-------|:---:|
| `dayzOffline.chernarusplus` | Chernarus | Non |
| `dayzOffline.enoch` | Livonia | Oui |
| `dayzOffline.sakhal` | Sakhal | Oui |

Les missions personnalisées (par ex. de mods ou cartes communautaires) utilisent leur propre nom de template. Le dossier doit exister dans `mpmissions/`.

---

## Exemple de fichier complet

Voici le `serverDZ.cfg` par défaut complet avec tous les paramètres :

```cpp
hostname = "EXAMPLE NAME";              // Nom du serveur
password = "";                          // Mot de passe pour se connecter au serveur
passwordAdmin = "";                     // Mot de passe pour devenir admin du serveur

description = "";                       // Description dans le navigateur de serveurs

enableWhitelist = 0;                    // Activer/désactiver la liste blanche (valeur 0-1)

maxPlayers = 60;                        // Nombre maximum de joueurs

verifySignatures = 2;                   // Vérifie les .pbo par rapport aux fichiers .bisign (seul 2 est supporté)
forceSameBuild = 1;                     // Exiger la même version client/serveur (valeur 0-1)

disableVoN = 0;                         // Activer/désactiver la voix sur réseau (valeur 0-1)
vonCodecQuality = 20;                   // Qualité du codec voix sur réseau (valeurs 0-30)

shardId = "123abc";                     // Six caractères alphanumériques pour shard privé

disable3rdPerson = 0;                   // Active/désactive la vue troisième personne (valeur 0-1)
disableCrosshair = 0;                   // Active/désactive le réticule (valeur 0-1)

disablePersonalLight = 1;              // Désactive la lumière personnelle pour tous les clients
lightingConfig = 0;                     // 0 pour nuits plus lumineuses, 1 pour nuits plus sombres

serverTime = "SystemTime";             // Heure initiale en jeu ("SystemTime" ou "YYYY/MM/DD/HH/MM")
serverTimeAcceleration = 12;           // Multiplicateur de vitesse du temps (0-24)
serverNightTimeAcceleration = 1;       // Multiplicateur de vitesse nocturne (0.1-64), aussi multiplié par serverTimeAcceleration
serverTimePersistent = 0;              // Sauvegarder le temps entre les redémarrages (valeur 0-1)

guaranteedUpdates = 1;                 // Protocole réseau (toujours utiliser 1)

loginQueueConcurrentPlayers = 5;       // Joueurs traités simultanément lors de la connexion
loginQueueMaxPlayers = 500;            // Taille maximale de la file de connexion

instanceId = 1;                        // ID d'instance du serveur (affecte le nommage du dossier de stockage)

storageAutoFix = 1;                    // Réparation automatique de la persistance corrompue (valeur 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Paramètres de lancement qui remplacent la configuration

Certains paramètres peuvent être remplacés via les paramètres de ligne de commande lors du lancement de `DayZServer_x64.exe` :

| Paramètre | Remplace | Exemple |
|-----------|----------|---------|
| `-config=` | Chemin du fichier de configuration | `-config=serverDZ.cfg` |
| `-port=` | Port du jeu | `-port=2302` |
| `-profiles=` | Répertoire de sortie des profils | `-profiles=profiles` |
| `-mod=` | Mods côté client (séparés par des points-virgules) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Mods serveur uniquement | `-servermod=@MyServerMod` |
| `-BEpath=` | Chemin de BattlEye | `-BEpath=battleye` |
| `-dologs` | Activer la journalisation | -- |
| `-adminlog` | Activer la journalisation admin | -- |
| `-netlog` | Activer la journalisation réseau | -- |
| `-freezecheck` | Redémarrage automatique en cas de gel | -- |
| `-cpuCount=` | Cœurs CPU à utiliser | `-cpuCount=4` |
| `-noFilePatching` | Désactiver le patching de fichiers | -- |

### Exemple de lancement complet

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Les mods sont chargés dans l'ordre spécifié dans `-mod=`. L'ordre des dépendances est important : si le Mod B nécessite le Mod A, listez le Mod A en premier.

---

**Précédent :** [Structure des répertoires](02-directory-structure.md) | [Accueil](../README.md) | **Suivant :** [Économie du loot en profondeur >>](04-loot-economy.md)
