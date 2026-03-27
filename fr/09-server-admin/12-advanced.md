# Chapter 9.12 : Sujets avancés du serveur

[Accueil](../README.md) | [<< Précédent : Dépannage](11-troubleshooting.md) | [Accueil Partie 9](01-server-setup.md)

---

> **Résumé :** Fichiers de configuration avancés, configurations multi-cartes, fractionnement de l'économie, territoires animaux, événements dynamiques, contrôle météo, redémarrages automatisés et système de messages.

---

## Table des matières

- [cfggameplay.json en profondeur](#cfggameplayjson-en-profondeur)
- [Serveurs multi-cartes](#serveurs-multi-cartes)
- [Réglage personnalisé de l'économie](#réglage-personnalisé-de-léconomie)
- [cfgenvironment.xml et territoires animaux](#cfgenvironmentxml-et-territoires-animaux)
- [Événements dynamiques personnalisés](#événements-dynamiques-personnalisés)
- [Automatisation du redémarrage du serveur](#automatisation-du-redémarrage-du-serveur)
- [cfgweather.xml](#cfgweatherxml)
- [Système de messages](#système-de-messages)

---

## cfggameplay.json en profondeur

Le fichier **cfggameplay.json** se trouve dans votre dossier de mission et remplace les valeurs de gameplay codées en dur. Activez-le d'abord dans **serverDZ.cfg** :

```cpp
enableCfgGameplayFile = 1;
```

Structure vanilla :

```json
{
  "version": 123,
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false,
    "disableRespawnDialog": false,
    "disableRespawnInUnconsciousness": false
  },
  "PlayerData": {
    "disablePersonalLight": false,
    "StaminaData": {
      "sprintStaminaModifierErc": 1.0, "sprintStaminaModifierCro": 1.0,
      "staminaWeightLimitThreshold": 6000.0, "staminaMax": 100.0,
      "staminaKg": 0.3, "staminaMin": 0.0,
      "staminaDepletionSpeed": 1.0, "staminaRecoverySpeed": 1.0
    },
    "ShockHandlingData": {
      "shockRefillSpeedConscious": 5.0, "shockRefillSpeedUnconscious": 1.0,
      "allowRefillSpeedModifier": true
    },
    "MovementData": {
      "timeToSprint": 0.45, "timeToJog": 0.0,
      "rotationSpeedJog": 0.3, "rotationSpeedSprint": 0.15
    },
    "DrowningData": {
      "staminaDepletionSpeed": 10.0, "healthDepletionSpeed": 3.0,
      "shockDepletionSpeed": 10.0
    },
    "WeaponObstructionData": { "staticMode": 1, "dynamicMode": 1 }
  },
  "WorldsData": {
    "lightingConfig": 0, "objectSpawnersArr": [],
    "environmentMinTemps": [-3, -2, 0, 4, 9, 14, 18, 17, 13, 11, 9, 0],
    "environmentMaxTemps": [3, 5, 7, 14, 19, 24, 26, 25, 18, 14, 10, 5]
  },
  "BaseBuildingData": { "canBuildAnywhere": false, "canCraftAnywhere": false },
  "UIData": {
    "use3DMap": false,
    "HitIndicationData": {
      "hitDirectionOverrideEnabled": false, "hitDirectionBehaviour": 1,
      "hitDirectionStyle": 0, "hitDirectionIndicatorColorStr": "0xffbb0a1e",
      "hitDirectionMaxDuration": 2.0, "hitDirectionBreakPointRelative": 0.2,
      "hitDirectionScatter": 10.0, "hitIndicationPostProcessEnabled": true
    }
  }
}
```

- `version` -- doit correspondre à ce que votre binaire serveur attend. Ne le changez pas.
- `lightingConfig` -- `0` (par défaut) ou `1` (nuits plus lumineuses).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 valeurs, une par mois (jan-déc).
- `disablePersonalLight` -- supprime la faible lumière ambiante autour des nouveaux joueurs la nuit.
- `staminaMax` et les modificateurs de sprint contrôlent la distance que les joueurs peuvent parcourir en courant avant l'épuisement.
- `use3DMap` -- bascule la carte en jeu vers la variante 3D rendue du terrain.

---

## Serveurs multi-cartes

DayZ prend en charge plusieurs cartes via différents dossiers de mission dans `mpmissions/` :

| Carte | Dossier de mission |
|-------|-------------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Chaque carte a ses propres fichiers CE (`types.xml`, `events.xml`, etc.). Changez de carte via `template` dans **serverDZ.cfg** :

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Ou avec un paramètre de lancement : `-mission=mpmissions/dayzOffline.enoch`

Pour exécuter plusieurs cartes simultanément, utilisez des instances de serveur séparées avec leur propre configuration, répertoire de profil et plage de ports.

---

## Réglage personnalisé de l'économie

### Fractionnement de types.xml

Fractionnez les objets en plusieurs fichiers et enregistrez-les dans **cfgeconomycore.xml** :

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

Le serveur charge et fusionne tous les fichiers avec `type="types"`.

### Catégories et tags personnalisés

**cfglimitsdefinition.xml** définit les catégories/tags pour `types.xml` mais est écrasé lors des mises à jour. Utilisez plutôt **cfglimitsdefinitionuser.xml** :

```xml
<lists>
    <categories>
        <category name="custom_rare" />
    </categories>
    <tags>
        <tag name="custom_event" />
    </tags>
</lists>
```

---

## cfgenvironment.xml et territoires animaux

Le fichier **cfgenvironment.xml** dans votre dossier de mission pointe vers les fichiers de territoire dans le sous-répertoire `env/` :

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

Le dossier `env/` contient ces fichiers de territoires animaux :

| Fichier | Animaux |
|---------|---------|
| **bear_territories.xml** | Ours bruns |
| **wolf_territories.xml** | Meutes de loups |
| **fox_territories.xml** | Renards |
| **hare_territories.xml** | Lapins/lièvres |
| **hen_territories.xml** | Poulets |
| **pig_territories.xml** | Cochons |
| **red_deer_territories.xml** | Cerfs rouges |
| **roe_deer_territories.xml** | Chevreuils |
| **sheep_goat_territories.xml** | Moutons/chèvres |
| **wild_boar_territories.xml** | Sangliers |
| **cattle_territories.xml** | Vaches |

Une entrée de territoire définit des zones circulaires avec position et nombre d'animaux :

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- coordonnées du centre ; `r` -- rayon en mètres
- `dmin`, `dmax` -- nombre min/max d'animaux dans la zone
- `smin`, `smax` -- réservé (définir à `-1`)

---

## Événements dynamiques personnalisés

Les événements dynamiques (crashs d'hélicoptères, convois) sont définis dans **events.xml**. Pour créer un événement personnalisé :

**1. Définir l'événement** dans **events.xml** :

```xml
<event name="StaticMyCustomCrash">
    <nominal>3</nominal> <min>1</min> <max>5</max>
    <lifetime>1800</lifetime> <restock>600</restock>
    <saferadius>500</saferadius> <distanceradius>200</distanceradius> <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1" />
    <position>fixed</position> <limit>child</limit> <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_Mi8_Crashed" />
    </children>
</event>
```

**2. Ajouter des positions d'apparition** dans **cfgeventspawns.xml** :

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Ajouter des gardes infectés** (optionnel) -- ajoutez des éléments `<secondary type="ZmbM_PatrolNormal_Autumn" />` dans la définition de votre événement.

**4. Apparitions groupées** (optionnel) -- définissez des clusters dans **cfgeventgroups.xml** et référencez le nom du groupe dans votre événement.

---

## Automatisation du redémarrage du serveur

DayZ n'a pas de planificateur de redémarrage intégré. Utilisez l'automatisation au niveau du système d'exploitation.

### Windows

Créez **restart_server.bat** et exécutez-le via les Tâches planifiées de Windows toutes les 4-6 heures :

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Créez un script shell et ajoutez-le au cron (`0 */4 * * *`) :

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Sauvegardez toujours `storage_1/` avant chaque redémarrage. Une persistance corrompue lors de l'arrêt peut effacer les bases et véhicules des joueurs.

---

## cfgweather.xml

Le fichier **cfgweather.xml** dans votre dossier de mission contrôle les schémas météorologiques. Chaque carte est livrée avec ses propres valeurs par défaut :

Chaque phénomène a des valeurs `min`, `max`, `duration_min`, et `duration_max` (en secondes) :

| Phénomène | Min par défaut | Max par défaut | Notes |
|-----------|---------------|----------------|-------|
| `overcast` | 0.0 | 1.0 | Détermine la densité des nuages et la probabilité de pluie |
| `rain` | 0.0 | 1.0 | Ne se déclenche qu'au-dessus d'un seuil de couverture nuageuse. Mettez max à `0.0` pour supprimer la pluie |
| `fog` | 0.0 | 0.3 | Des valeurs au-dessus de `0.5` produisent une visibilité quasi nulle |
| `wind_magnitude` | 0.0 | 18.0 | Affecte la balistique et le mouvement des joueurs |

---

## Système de messages

Le fichier **db/messages.xml** dans votre dossier de mission contrôle les messages programmés du serveur et les avertissements d'arrêt :

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- minutes avant le déclenchement du message (pour les messages d'arrêt, minutes avant l'arrêt du serveur)
- `shutdown` -- `1` pour les messages de séquence d'arrêt, `0` pour les diffusions normales

Le système de messages ne redémarre pas le serveur. Il affiche uniquement des avertissements quand un programme de redémarrage est configuré en externe.

---

[Accueil](../README.md) | [<< Précédent : Dépannage](11-troubleshooting.md) | [Accueil Partie 9](01-server-setup.md)
