# Chapter 9.1 : Installation du serveur et premier lancement

[Accueil](../README.md) | **Installation du serveur** | [Suivant : Structure des répertoires >>](02-directory-structure.md)

---

> **Résumé :** Installez un serveur dédié DayZ Standalone à partir de zéro avec SteamCMD, lancez-le avec une configuration minimale, vérifiez qu'il apparaît dans le navigateur de serveurs, et connectez-vous en tant que joueur. Ce chapitre couvre tout, des exigences matérielles à la résolution des problèmes les plus courants au premier lancement.

---

## Table des matières

- [Prérequis](#prérequis)
- [Installer SteamCMD](#installer-steamcmd)
- [Installer le serveur DayZ](#installer-le-serveur-dayz)
- [Répertoire après installation](#répertoire-après-installation)
- [Premier lancement avec une configuration minimale](#premier-lancement-avec-une-configuration-minimale)
- [Vérifier que le serveur fonctionne](#vérifier-que-le-serveur-fonctionne)
- [Se connecter en tant que joueur](#se-connecter-en-tant-que-joueur)
- [Problèmes courants au premier lancement](#problèmes-courants-au-premier-lancement)

---

## Prérequis

### Matériel

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| CPU | 4 cœurs, 2.4 GHz | 6+ cœurs, 3.5 GHz |
| RAM | 8 Go | 16 Go |
| Disque | 20 Go SSD | 40 Go NVMe SSD |
| Réseau | 10 Mbps en upload | 50+ Mbps en upload |
| OS | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

Le serveur DayZ est mono-thread pour la logique de jeu. La fréquence d'horloge compte plus que le nombre de cœurs.

### Logiciels

- **SteamCMD** -- le client Steam en ligne de commande pour installer les serveurs dédiés
- **Visual C++ Redistributable 2019** (Windows) -- requis par `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- généralement déjà présent
- Ports **2302-2305 UDP** redirigés sur votre routeur/pare-feu

---

## Installer SteamCMD

### Windows

1. Téléchargez SteamCMD depuis https://developer.valvesoftware.com/wiki/SteamCMD
2. Extrayez `steamcmd.exe` dans un dossier permanent, par ex. `C:\SteamCMD\`
3. Lancez `steamcmd.exe` une fois -- il se mettra à jour automatiquement

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## Installer le serveur DayZ

L'App ID Steam du serveur DayZ est **223350**. Vous pouvez l'installer sans vous connecter à un compte Steam possédant DayZ.

### Installation en une ligne (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Installation en une ligne (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Script de mise à jour

Créez un script que vous pouvez relancer à chaque patch :

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Mise à jour terminée.
pause
```

Le flag `validate` vérifie chaque fichier pour détecter les corruptions. Pour une installation neuve, attendez-vous à un téléchargement de 2-3 Go.

---

## Répertoire après installation

Après l'installation, la racine du serveur ressemble à ceci :

```
DayZServer/
  DayZServer_x64.exe        # L'exécutable du serveur
  serverDZ.cfg               # Configuration principale du serveur
  dayzsetting.xml            # Paramètres de rendu/vidéo (non pertinents pour un serveur dédié)
  addons/                    # Fichiers PBO vanilla (ai.pbo, animals.pbo, etc.)
  battleye/                  # Anti-triche BattlEye (BEServer_x64.dll)
  dta/                       # Données moteur principales (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Clés de signature (dayz.bikey pour le vanilla)
  logs/                      # Logs moteur (connexion, contenu, audio)
  mpmissions/                # Dossiers de missions
    dayzOffline.chernarusplus/   # Mission Chernarus
    dayzOffline.enoch/           # Mission Livonia (DLC)
    dayzOffline.sakhal/          # Mission Sakhal (DLC)
  profiles/                  # Sortie runtime : logs RPT, logs de scripts, base de données joueurs
  ban.txt                    # Liste des joueurs bannis (Steam64 IDs)
  whitelist.txt              # Joueurs en liste blanche (Steam64 IDs)
  steam_appid.txt            # Contient "221100"
```

Points clés :
- **Vous modifiez** `serverDZ.cfg` et les fichiers dans `mpmissions/`.
- **Vous ne modifiez jamais** les fichiers dans `addons/` ou `dta/` -- ils sont écrasés à chaque mise à jour.
- **Les PBO de mods** vont dans la racine du serveur ou un sous-dossier (traité dans un chapitre ultérieur).
- **`profiles/`** est créé au premier lancement et contient vos logs de scripts et dumps de crash.

---

## Premier lancement avec une configuration minimale

### Étape 1 : Modifier serverDZ.cfg

Ouvrez `serverDZ.cfg` dans un éditeur de texte. Pour un premier test, utilisez la configuration la plus simple possible :

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### Étape 2 : Lancer le serveur

Ouvrez une invite de commandes dans le répertoire du serveur et exécutez :

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Flag | Objectif |
|------|----------|
| `-config=serverDZ.cfg` | Chemin vers le fichier de configuration |
| `-port=2302` | Port principal du jeu (utilise aussi 2303-2305) |
| `-profiles=profiles` | Dossier de sortie pour les logs et données joueurs |
| `-dologs` | Activer les logs du serveur |
| `-adminlog` | Journaliser les actions admin |
| `-netlog` | Journaliser les événements réseau |
| `-freezecheck` | Redémarrage automatique en cas de détection de gel |

### Étape 3 : Attendre l'initialisation

Le serveur met 30 à 90 secondes pour démarrer complètement. Surveillez la sortie console. Lorsque vous voyez une ligne comme :

```
BattlEye Server: Initialized (v1.xxx)
```

...le serveur est prêt à recevoir des connexions.

---

## Vérifier que le serveur fonctionne

### Méthode 1 : Log de scripts

Vérifiez dans `profiles/` la présence d'un fichier nommé comme `script_YYYY-MM-DD_HH-MM-SS.log`. Ouvrez-le et cherchez :

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Ces lignes confirment que l'économie s'est initialisée et que la mission a été chargée.

### Méthode 2 : Fichier RPT

Le fichier `.RPT` dans `profiles/` affiche la sortie au niveau moteur. Cherchez :

```
Dedicated host created.
BattlEye Server: Initialized
```

### Méthode 3 : Navigateur de serveurs Steam

Ouvrez Steam, allez dans **Vue > Serveurs de jeu > Favoris**, cliquez sur **Ajouter un serveur**, entrez `127.0.0.1:2302` (ou votre IP publique), et cliquez sur **Rechercher des jeux à cette adresse**. Si le serveur apparaît, il fonctionne et est accessible.

### Méthode 4 : Port de requête

Utilisez un outil externe comme https://www.battlemetrics.com/ ou le package npm `gamedig` pour interroger le port 27016 (port de requête Steam = port du jeu + 24714).

---

## Se connecter en tant que joueur

### Depuis la même machine

1. Lancez DayZ (pas DayZ Server -- le client de jeu normal)
2. Ouvrez le **Navigateur de serveurs**
3. Allez dans l'onglet **LAN** ou l'onglet **Favoris**
4. Ajoutez `127.0.0.1:2302` aux favoris
5. Cliquez sur **Connexion**

Si vous exécutez le client et le serveur sur la même machine, utilisez `DayZDiag_x64.exe` (le client de diagnostic) au lieu du client normal. Lancez avec :

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### Depuis une autre machine

Utilisez l'**IP publique** ou l'**IP LAN** de votre serveur selon que le client est ou non sur le même réseau. Les ports 2302-2305 UDP doivent être redirigés.

---

## Problèmes courants au premier lancement

### Le serveur démarre mais se ferme immédiatement

**Cause :** Visual C++ Redistributable manquant ou erreur de syntaxe dans `serverDZ.cfg`.

**Solution :** Installez VC++ Redist 2019 (x64). Vérifiez `serverDZ.cfg` pour les points-virgules manquants -- chaque ligne de paramètre doit se terminer par `;`.

### "BattlEye initialization failed"

**Cause :** Le dossier `battleye/` est manquant ou l'antivirus bloque `BEServer_x64.dll`.

**Solution :** Revalidez les fichiers du serveur via SteamCMD. Ajoutez une exception antivirus pour l'ensemble du dossier du serveur.

### Le serveur fonctionne mais n'apparaît pas dans le navigateur

**Cause :** Ports non redirigés, ou le pare-feu Windows bloque l'exécutable.

**Solution :**
1. Ajoutez une règle entrante dans le pare-feu Windows pour `DayZServer_x64.exe` (autoriser tout UDP)
2. Redirigez les ports **2302-2305 UDP** sur votre routeur
3. Vérifiez avec un outil de test de ports externe que le port 2302 UDP est ouvert sur votre IP publique

### "Version Mismatch" lors de la connexion

**Cause :** Le serveur et le client sont sur des versions différentes.

**Solution :** Mettez les deux à jour. Exécutez la commande de mise à jour SteamCMD pour le serveur. Le client se met à jour automatiquement via Steam.

### Pas de loot

**Cause :** Le fichier `init.c` est manquant ou le Hive n'a pas réussi à s'initialiser.

**Solution :** Vérifiez que `mpmissions/dayzOffline.chernarusplus/init.c` existe et contient `CreateHive()`. Vérifiez le log de scripts pour les erreurs.

### Le serveur utilise 100% d'un cœur CPU

C'est normal. Le serveur DayZ est mono-thread. N'exécutez pas plusieurs instances de serveur sur le même cœur -- utilisez l'affinité processeur ou des machines séparées.

### Les joueurs apparaissent en corbeaux / bloqués au chargement

**Cause :** Le template de mission dans `serverDZ.cfg` ne correspond pas à un dossier existant dans `mpmissions/`.

**Solution :** Vérifiez la valeur du template. Elle doit correspondre exactement à un nom de dossier :

```cpp
template = "dayzOffline.chernarusplus";  // Doit correspondre au nom du dossier dans mpmissions/
```

---

**[Accueil](../README.md)** | **Suivant :** [Structure des répertoires >>](02-directory-structure.md)
