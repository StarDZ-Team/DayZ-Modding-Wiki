# Chapter 9.11 : Dépannage du serveur

[Accueil](../README.md) | [<< Précédent : Gestion des mods](10-mod-management.md) | [Suivant : Sujets avancés >>](12-advanced.md)

---

> **Résumé :** Diagnostiquez et corrigez les problèmes de serveur DayZ les plus courants -- échecs de démarrage, problèmes de connexion, crashs, apparition du loot et des véhicules, persistance et performances. Chaque solution présentée ici provient de schémas d'erreurs réels à travers des milliers de rapports communautaires.

---

## Table des matières

- [Le serveur ne démarre pas](#le-serveur-ne-démarre-pas)
- [Les joueurs ne peuvent pas se connecter](#les-joueurs-ne-peuvent-pas-se-connecter)
- [Crashs et pointeurs nuls](#crashs-et-pointeurs-nuls)
- [Le loot n'apparaît pas](#le-loot-napparaît-pas)
- [Les véhicules n'apparaissent pas](#les-véhicules-napparaissent-pas)
- [Problèmes de persistance](#problèmes-de-persistance)
- [Problèmes de performance](#problèmes-de-performance)
- [Lecture des fichiers de log](#lecture-des-fichiers-de-log)
- [Checklist de diagnostic rapide](#checklist-de-diagnostic-rapide)

---

## Le serveur ne démarre pas

### Fichiers DLL manquants

Si `DayZServer_x64.exe` crash immédiatement avec une erreur de DLL manquante, installez la dernière version de **Visual C++ Redistributable for Visual Studio 2019** (x64) depuis le site officiel de Microsoft et redémarrez.

### Port déjà utilisé

Une autre instance DayZ ou une application occupe le port 2302. Vérifiez avec `netstat -ano | findstr 2302` (Windows) ou `ss -tulnp | grep 2302` (Linux). Arrêtez le processus en conflit ou changez votre port avec `-port=2402`.

### Dossier de mission manquant

Le serveur s'attend à `mpmissions/<template>/` où le nom du dossier correspond exactement à la valeur `template` dans **serverDZ.cfg**. Pour Chernarus, c'est `mpmissions/dayzOffline.chernarusplus/` et il doit contenir au minimum **init.c**.

### serverDZ.cfg invalide

Un seul point-virgule manquant ou un mauvais type de guillemet empêche silencieusement le démarrage. Surveillez :

- `;` manquant en fin de lignes de valeurs
- Guillemets typographiques au lieu de guillemets droits
- Bloc `{};` manquant autour des entrées de classe

### Fichiers de mod manquants

Chaque chemin dans `-mod=@CF;@VPPAdminTools;@MyMod` doit exister relativement à la racine du serveur et contenir un dossier **addons/** avec des fichiers `.pbo`. Un seul mauvais chemin empêche le démarrage.

---

## Les joueurs ne peuvent pas se connecter

### Redirection de ports

DayZ nécessite ces ports redirigés et ouverts dans votre pare-feu :

| Port | Protocole | Objectif |
|------|-----------|----------|
| 2302 | UDP | Trafic de jeu |
| 2303 | UDP | Réseau Steam |
| 2304 | UDP | Requête Steam (interne) |
| 27016 | UDP | Requête navigateur de serveurs Steam |

Si vous avez changé le port de base avec `-port=`, tous les autres ports se décalent du même offset.

### Blocage par le pare-feu

Ajoutez **DayZServer_x64.exe** aux exceptions de votre pare-feu OS. Sur Windows : `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. Sur Linux, ouvrez les ports avec `ufw` ou `iptables`.

### Divergence de mods

Les clients doivent avoir exactement les mêmes versions de mods que le serveur. Si un joueur voit "Mod mismatch", l'un des deux côtés a une version obsolète. Mettez les deux à jour quand un mod reçoit une mise à jour Workshop.

### Fichiers .bikey manquants

Le fichier `.bikey` de chaque mod doit être dans le répertoire `keys/` du serveur. Sans lui, BattlEye rejette les PBO signés du client. Regardez dans le dossier `keys/` ou `key/` de chaque mod.

### Serveur complet

Vérifiez `maxPlayers` dans **serverDZ.cfg** (par défaut 60).

---

## Crashs et pointeurs nuls

### Accès à un pointeur nul

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- l'erreur de script la plus courante. Un mod appelle une méthode sur un objet supprimé ou non initialisé. C'est un bug du mod, pas une mauvaise configuration du serveur. Signalez-le à l'auteur du mod avec le log RPT complet.

### Trouver les erreurs de script

Cherchez `SCRIPT (E)` dans le log RPT. Le nom de la classe et de la méthode dans l'erreur vous indique quel mod est responsable. Emplacements des RPT :

- **Serveur :** répertoire `$profiles/` (ou racine du serveur si aucun `-profiles=` n'est défini)
- **Client :** `%localappdata%\DayZ\`

### Crash au redémarrage

Si le serveur crash à chaque redémarrage, **storage_1/** peut être corrompu. Arrêtez le serveur, sauvegardez `storage_1/`, supprimez `storage_1/data/events.bin`, et redémarrez. Si cela échoue, supprimez l'intégralité du répertoire `storage_1/` (efface toute la persistance).

### Crash après une mise à jour de mod

Revenez à la version précédente du mod. Vérifiez le changelog du Workshop pour les changements cassants -- classes renommées, configs supprimées et formats RPC modifiés sont des causes courantes.

---

## Le loot n'apparaît pas

### types.xml non enregistré

Les objets définis dans **types.xml** n'apparaîtront pas si le fichier n'est pas enregistré dans **cfgeconomycore.xml** :

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Si vous utilisez un fichier types personnalisé (par ex. **types_custom.xml**), ajoutez une entrée `<file>` séparée pour lui.

### Mauvais tags de catégorie, d'usage ou de valeur

Chaque tag `<category>`, `<usage>`, et `<value>` dans votre types.xml doit correspondre à un nom défini dans **cfglimitsdefinition.xml**. Une faute de frappe comme `usage name="Military"` (M majuscule) quand la définition dit `military` (minuscule) empêche silencieusement l'objet d'apparaître.

### Nominal à zéro

Si `nominal` est `0`, le CE ne fera jamais apparaître cet objet. C'est intentionnel pour les objets qui ne doivent exister que via l'artisanat, les événements ou le placement admin. Si vous voulez que l'objet apparaisse naturellement, mettez `nominal` à au moins `1`.

### Positions de groupe de carte manquantes

Les objets ont besoin de positions d'apparition valides à l'intérieur des bâtiments. Si un objet personnalisé n'a pas de positions de groupe de carte correspondantes (définies dans **mapgroupproto.xml**), le CE n'a nulle part où le placer. Assignez l'objet à des catégories et usages qui ont déjà des positions valides sur la carte.

---

## Les véhicules n'apparaissent pas

Les véhicules utilisent le système d'événements, **pas** types.xml.

### Configuration de events.xml

Les apparitions de véhicules sont définies dans **events.xml** :

```xml
<event name="VehicleOffroadHatchback">
    <nominal>8</nominal>
    <min>5</min>
    <max>8</max>
    <lifetime>3888000</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="1" min="1" type="OffroadHatchback"/>
    </children>
</event>
```

### Positions d'apparition manquantes

Les événements de véhicules avec `<position>fixed</position>` nécessitent des entrées dans **cfgeventspawns.xml**. Sans coordonnées définies, l'événement n'a nulle part où placer le véhicule.

### Événement désactivé

Si `<active>0</active>`, l'événement est complètement désactivé. Mettez-le à `1`.

### Les véhicules endommagés bloquent les emplacements

Si `remove_damaged="0"`, les véhicules détruits restent dans le monde indéfiniment et occupent les emplacements d'apparition. Mettez `remove_damaged="1"` pour que le CE nettoie les épaves et fasse apparaître des remplacements.

---

## Problèmes de persistance

### Les bases disparaissent

Les drapeaux de territoire doivent être rafraîchis avant l'expiration de leur timer. La valeur par défaut de `FlagRefreshFrequency` est `432000` secondes (5 jours). Si aucun joueur n'interagit avec le drapeau dans ce délai, le drapeau et tous les objets dans son rayon sont supprimés.

Vérifiez la valeur dans **globals.xml** :

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Augmentez cette valeur sur les serveurs à faible population où les joueurs se connectent moins fréquemment.

### Les objets disparaissent après un redémarrage

Chaque objet a une `lifetime` dans **types.xml** (en secondes). Quand elle expire sans interaction joueur, le CE le supprime. Référence : `3888000` = 45 jours, `604800` = 7 jours, `14400` = 4 heures. Les objets dans des conteneurs héritent de la durée de vie du conteneur.

### storage_1/ devient trop volumineux

Si votre répertoire `storage_1/` dépasse plusieurs centaines de Mo, votre économie produit trop d'objets. Réduisez les valeurs `nominal` dans votre types.xml, surtout pour les objets à compteur élevé comme la nourriture, les vêtements et les munitions. Un fichier de persistance gonflé cause des temps de redémarrage plus longs.

### Données joueurs perdues

Les inventaires et positions des joueurs sont stockés dans `storage_1/players/`. Si ce répertoire est supprimé ou corrompu, tous les joueurs apparaissent en nouveau. Sauvegardez `storage_1/` régulièrement.

---

## Problèmes de performance

### Baisse des FPS serveur

Les serveurs DayZ visent 30+ FPS pour un gameplay fluide. Causes courantes de FPS serveur bas :

- **Trop de zombies** -- réduisez `ZombieMaxCount` dans **globals.xml** (par défaut 800, essayez 400-600)
- **Trop d'animaux** -- réduisez `AnimalMaxCount` (par défaut 200, essayez 100)
- **Excès de loot** -- réduisez les valeurs `nominal` dans votre types.xml
- **Trop d'objets de base** -- les grandes bases avec des centaines d'objets sollicitent la persistance
- **Mods à scripts lourds** -- certains mods exécutent une logique coûteuse par frame

### Désynchronisation

Les joueurs qui subissent des téléportations, des actions retardées ou des zombies invisibles sont des symptômes de désynchronisation. Cela signifie presque toujours que les FPS serveur sont tombés en dessous de 15. Corrigez le problème de performance sous-jacent plutôt que de chercher un paramètre spécifique à la désynchronisation.

### Temps de redémarrage longs

Le temps de redémarrage est directement proportionnel à la taille de `storage_1/`. Si les redémarrages prennent plus de 2-3 minutes, vous avez trop d'objets persistants. Réduisez les valeurs nominales du loot et définissez des durées de vie appropriées.

---

## Lecture des fichiers de log

### Emplacement du RPT serveur

Le fichier RPT se trouve dans `$profiles/` (si lancé avec `-profiles=`) ou la racine du serveur. Modèle de nom de fichier : `DayZServer_x64_<date>_<heure>.RPT`.

### Que chercher

| Terme de recherche | Signification |
|--------------------|---------------|
| `SCRIPT (E)` | Erreur de script -- un mod a un bug |
| `[ERROR]` | Erreur au niveau moteur |
| `ErrorMessage` | Erreur fatale pouvant causer l'arrêt |
| `Cannot open` | Fichier manquant (PBO, config, mission) |
| `Crash` | Crash au niveau application |

### Logs BattlEye

Les logs BattlEye se trouvent dans le répertoire `BattlEye/` à la racine de votre serveur. Ils montrent les événements de kick et de ban. Si des joueurs signalent être expulsés de façon inattendue, vérifiez ici en premier.

---

## Checklist de diagnostic rapide

Quand quelque chose ne va pas, parcourez cette liste dans l'ordre :

```
1. Vérifier le RPT serveur pour les lignes SCRIPT (E) et [ERROR]
2. Vérifier que chaque chemin -mod= existe et contient addons/*.pbo
3. Vérifier que tous les fichiers .bikey sont copiés dans keys/
4. Vérifier serverDZ.cfg pour les erreurs de syntaxe (points-virgules manquants)
5. Vérifier la redirection de ports : 2302 UDP + 27016 UDP
6. Vérifier que le dossier de mission correspond à la valeur template dans serverDZ.cfg
7. Vérifier storage_1/ pour la corruption (supprimer events.bin si nécessaire)
8. Tester avec zéro mod d'abord, puis ajouter les mods un par un
```

L'étape 8 est la technique la plus puissante. Si le serveur fonctionne en vanilla mais casse avec des mods, vous pouvez isoler le mod problématique par recherche binaire -- ajoutez la moitié de vos mods, testez, puis affinez.

---

[Accueil](../README.md) | [<< Précédent : Gestion des mods](10-mod-management.md) | [Suivant : Sujets avancés >>](12-advanced.md)
