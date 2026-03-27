# Chapter 9.9 : Contrôle d'accès

[Accueil](../README.md) | [<< Précédent : Optimisation des performances](08-performance.md) | [Suivant : Gestion des mods >>](10-mod-management.md)

---

> **Résumé :** Configurez qui peut se connecter à votre serveur DayZ, comment fonctionnent les bans, comment activer l'administration à distance, et comment la vérification des signatures de mods empêche le contenu non autorisé. Ce chapitre couvre tous les mécanismes de contrôle d'accès disponibles pour un opérateur de serveur.

---

## Table des matières

- [Accès admin via serverDZ.cfg](#accès-admin-via-serverdzcfg)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [Anti-triche BattlEye](#anti-triche-battleye)
- [RCON (Console distante)](#rcon-console-distante)
- [Vérification des signatures](#vérification-des-signatures)
- [Le répertoire keys/](#le-répertoire-keys)
- [Outils d'administration en jeu](#outils-dadministration-en-jeu)
- [Erreurs courantes](#erreurs-courantes)

---

## Accès admin via serverDZ.cfg

Le paramètre `passwordAdmin` dans **serverDZ.cfg** définit le mot de passe admin pour votre serveur :

```cpp
passwordAdmin = "YourSecretPassword";
```

Vous utilisez ce mot de passe de deux façons :

1. **En jeu** -- ouvrez le chat et tapez `#login YourSecretPassword` pour obtenir les privilèges admin pour cette session.
2. **RCON** -- connectez-vous avec un client RCON BattlEye en utilisant ce mot de passe (voir la section RCON ci-dessous).

Gardez le mot de passe admin long et unique. Quiconque le possède a le contrôle total du serveur en fonctionnement.

---

## ban.txt

Le fichier **ban.txt** se trouve dans votre répertoire de profil serveur (le chemin défini avec `-profiles=`). Il contient un SteamID64 par ligne :

```
76561198012345678
76561198087654321
```

- Chaque ligne est un SteamID64 brut à 17 chiffres -- pas de noms, pas de commentaires, pas de mots de passe.
- Les joueurs dont le SteamID apparaît dans ce fichier se voient refuser la connexion.
- Vous pouvez modifier le fichier pendant que le serveur tourne ; les changements prennent effet à la prochaine tentative de connexion.

---

## whitelist.txt

Le fichier **whitelist.txt** se trouve dans le même répertoire de profil. Lorsque vous activez la liste blanche, seuls les SteamID listés dans ce fichier peuvent se connecter :

```
76561198012345678
76561198087654321
```

Le format est identique à **ban.txt** -- un SteamID64 par ligne, rien d'autre.

La liste blanche est utile pour les communautés privées, les serveurs de test, ou les événements où vous avez besoin d'une liste de joueurs contrôlée.

---

## Anti-triche BattlEye

BattlEye est le système anti-triche intégré à DayZ. Ses fichiers se trouvent dans le dossier `BattlEye/` à l'intérieur de votre répertoire serveur :

| Fichier | Objectif |
|---------|----------|
| **BEServer_x64.dll** | Le binaire du moteur anti-triche BattlEye |
| **beserver_x64.cfg** | Fichier de configuration (port RCON, mot de passe RCON) |
| **bans.txt** | Bans spécifiques à BattlEye (basés sur les GUID, pas les SteamID) |

BattlEye est activé par défaut. Vous lancez le serveur avec `DayZServer_x64.exe` et BattlEye se charge automatiquement. Pour le désactiver explicitement (non recommandé en production), utilisez le paramètre de lancement `-noBE`.

Le fichier **bans.txt** dans le dossier `BattlEye/` utilise les GUID BattlEye, qui sont différents des SteamID64. Les bans émis via RCON ou les commandes BattlEye sont écrits automatiquement dans ce fichier.

---

## RCON (Console distante)

Le RCON BattlEye vous permet d'administrer le serveur à distance sans être en jeu. Configurez-le dans `BattlEye/beserver_x64.cfg` :

```
RConPassword yourpassword
RConPort 2306
```

Le port RCON par défaut est votre port de jeu plus 4. Si votre serveur tourne sur le port `2302`, le RCON utilise par défaut `2306`.

### Commandes RCON disponibles

| Commande | Effet |
|----------|-------|
| `kick <joueur> [raison]` | Expulser un joueur du serveur |
| `ban <joueur> [minutes] [raison]` | Bannir un joueur (écrit dans le bans.txt de BattlEye) |
| `say -1 <message>` | Diffuser un message à tous les joueurs |
| `#shutdown` | Arrêt propre du serveur |
| `#lock` | Verrouiller le serveur (pas de nouvelles connexions) |
| `#unlock` | Déverrouiller le serveur |
| `players` | Lister les joueurs connectés |

Vous vous connectez au RCON en utilisant un client RCON BattlEye (plusieurs outils gratuits existent). La connexion nécessite l'IP, le port RCON, et le mot de passe de **beserver_x64.cfg**.

---

## Vérification des signatures

Le paramètre `verifySignatures` dans **serverDZ.cfg** contrôle si le serveur vérifie les signatures des mods :

```cpp
verifySignatures = 2;
```

| Valeur | Comportement |
|--------|-------------|
| `0` | Désactivé -- n'importe qui peut rejoindre avec n'importe quels mods, pas de vérification de signature |
| `2` | Vérification complète -- les clients doivent avoir des signatures valides pour tous les mods chargés (par défaut) |

Utilisez toujours `verifySignatures = 2` sur les serveurs de production. Le mettre à `0` permet aux joueurs de rejoindre avec des mods modifiés ou non signés, ce qui est un risque de sécurité sérieux.

---

## Le répertoire keys/

Le répertoire `keys/` à la racine de votre serveur contient les fichiers **.bikey**. Chaque `.bikey` correspond à un mod et indique au serveur "les signatures de ce mod sont approuvées."

Quand `verifySignatures = 2` :

1. Le serveur vérifie chaque mod que le client qui se connecte a chargé.
2. Pour chaque mod, le serveur cherche un `.bikey` correspondant dans `keys/`.
3. Si une clé correspondante est manquante, le joueur est expulsé.

Chaque mod que vous installez sur le serveur est livré avec un fichier `.bikey` (généralement dans le sous-dossier `Keys/` ou `Key/` du mod). Vous copiez ce fichier dans le répertoire `keys/` de votre serveur.

```
DayZServer/
├── keys/
│   ├── dayz.bikey              ← vanilla (toujours présent)
│   ├── MyMod.bikey             ← copié depuis @MyMod/Keys/
│   └── AnotherMod.bikey        ← copié depuis @AnotherMod/Keys/
```

Si vous ajoutez un nouveau mod et oubliez de copier son `.bikey`, chaque joueur utilisant ce mod est expulsé à la connexion.

---

## Outils d'administration en jeu

Une fois connecté avec `#login <mot_de_passe>` dans le chat, vous avez accès aux outils admin :

- **Liste des joueurs** -- voir tous les joueurs connectés avec leurs SteamIDs.
- **Kick/ban** -- supprimer ou bannir des joueurs directement depuis la liste.
- **Téléportation** -- utiliser la carte admin pour se téléporter à n'importe quelle position.
- **Log admin** -- log côté serveur des actions des joueurs (kills, connexions, déconnexions) écrit dans les fichiers `*.ADM` du répertoire de profil.
- **Caméra libre** -- se détacher de votre personnage et voler autour de la carte.

Ces outils sont intégrés au jeu vanilla. Des mods tiers (comme Community Online Tools) étendent considérablement les capacités d'administration.

---

## Erreurs courantes

Ce sont les problèmes que les opérateurs de serveurs rencontrent le plus souvent :

| Erreur | Symptôme | Solution |
|--------|----------|---------|
| `.bikey` manquant dans `keys/` | Les joueurs sont expulsés à la connexion avec une erreur de signature | Copiez le fichier `.bikey` du mod dans le répertoire `keys/` de votre serveur |
| Mettre des noms ou mots de passe dans **ban.txt** | Les bans ne fonctionnent pas ; erreurs aléatoires | Utilisez uniquement des valeurs SteamID64 brutes, une par ligne |
| Conflit de port RCON | Le client RCON ne peut pas se connecter | Assurez-vous que le port RCON n'est pas utilisé par un autre service ; vérifiez les règles du pare-feu |
| `verifySignatures = 0` en production | N'importe qui peut rejoindre avec des mods falsifiés | Mettez à `2` sur tout serveur public |
| Oublier d'ouvrir le port RCON dans le pare-feu | Le client RCON timeout | Ouvrez le port UDP RCON (par défaut 2306) dans votre pare-feu |
| Modifier **bans.txt** dans `BattlEye/` avec des SteamIDs | Les bans ne fonctionnent pas | Le **bans.txt** de BattlEye utilise des GUID, pas des SteamIDs ; utilisez **ban.txt** dans le répertoire de profil pour les bans par SteamID |

---

[Accueil](../README.md) | [<< Précédent : Optimisation des performances](08-performance.md) | [Suivant : Gestion des mods >>](10-mod-management.md)
