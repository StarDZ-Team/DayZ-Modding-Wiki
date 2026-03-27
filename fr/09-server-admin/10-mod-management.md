# Chapter 9.10 : Gestion des mods

[Accueil](../README.md) | [<< Précédent : Contrôle d'accès](09-access-control.md) | [Suivant : Dépannage >>](11-troubleshooting.md)

---

> **Résumé :** Installez, configurez et maintenez des mods tiers sur un serveur dédié DayZ. Couvre les paramètres de lancement, les téléchargements Workshop, les clés de signature, l'ordre de chargement, les mods serveur uniquement vs requis par le client, les mises à jour, et les erreurs les plus courantes qui causent des crashs ou des kicks de joueurs.

---

## Table des matières

- [Comment les mods se chargent](#comment-les-mods-se-chargent)
- [Format des paramètres de lancement](#format-des-paramètres-de-lancement)
- [Installation des mods Workshop](#installation-des-mods-workshop)
- [Clés de mod (.bikey)](#clés-de-mod-bikey)
- [Ordre de chargement et dépendances](#ordre-de-chargement-et-dépendances)
- [Mods serveur uniquement vs requis par le client](#mods-serveur-uniquement-vs-requis-par-le-client)
- [Mettre à jour les mods](#mettre-à-jour-les-mods)
- [Dépannage des conflits de mods](#dépannage-des-conflits-de-mods)
- [Erreurs courantes](#erreurs-courantes)

---

## Comment les mods se chargent

DayZ charge les mods via le paramètre de lancement `-mod=`. Chaque entrée est un chemin vers un dossier contenant des fichiers PBO et un `config.cpp`. Le moteur lit chaque PBO dans chaque dossier de mod, enregistre ses classes et scripts, puis passe au mod suivant dans la liste.

Le serveur et le client doivent avoir les mêmes mods dans `-mod=`. Si le serveur liste `@CF;@MyMod` et que le client n'a que `@CF`, la connexion échoue avec une erreur de signature. Les mods serveur uniquement placés dans `-servermod=` sont l'exception -- les clients n'en ont jamais besoin.

---

## Format des paramètres de lancement

Une commande de lancement typique de serveur moddé :

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Paramètre | Objectif |
|-----------|----------|
| `-mod=` | Mods requis à la fois par le serveur et tous les clients qui se connectent |
| `-servermod=` | Mods serveur uniquement (les clients n'en ont pas besoin) |

Règles :
- Les chemins sont **séparés par des points-virgules** sans espaces autour
- Chaque chemin est relatif au répertoire racine du serveur (par ex. `@CF` signifie `<racine_serveur>/@CF/`)
- Vous pouvez utiliser des chemins absolus : `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **L'ordre compte** -- les dépendances doivent apparaître avant les mods qui en ont besoin

---

## Installation des mods Workshop

### Étape 1 : Télécharger le mod

Utilisez SteamCMD avec l'App ID du **client** DayZ (221100) et l'ID Workshop du mod :

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

Les fichiers téléchargés se trouvent dans :

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Étape 2 : Créer un lien symbolique ou copier

Les dossiers Workshop utilisent des ID numériques, inutilisables dans `-mod=`. Créez un lien symbolique nommé (recommandé) ou copiez le dossier :

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Utiliser une jonction signifie que les mises à jour via SteamCMD s'appliquent automatiquement -- pas besoin de recopier.

### Étape 3 : Copier le .bikey

Voir la section suivante.

---

## Clés de mod (.bikey)

Chaque mod signé est livré avec un dossier `keys/` contenant un ou plusieurs fichiers `.bikey`. Ces fichiers indiquent à BattlEye quelles signatures PBO accepter.

1. Ouvrez le dossier du mod (par ex. `@CF/keys/`)
2. Copiez chaque fichier `.bikey` dans le répertoire `keys/` à la racine du serveur

```
DayZServer/
  keys/
    dayz.bikey              # Vanilla -- toujours présent
    cf.bikey                # Copié depuis @CF/keys/
    vpp_admintools.bikey    # Copié depuis @VPPAdminTools/keys/
```

Sans la bonne clé, tout joueur utilisant ce mod reçoit : **"Player kicked: Modified data"**.

---

## Ordre de chargement et dépendances

Les mods se chargent de gauche à droite dans le paramètre `-mod=`. Le `config.cpp` d'un mod déclare ses dépendances :

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Si `MyMod` nécessite `CF`, alors `@CF` doit apparaître **avant** `@MyMod` dans le paramètre de lancement :

```
-mod=@CF;@MyMod          ✓ correct
-mod=@MyMod;@CF          ✗ crash ou classes manquantes
```

**Schéma d'ordre de chargement général :**

1. **Mods framework** -- CF, Community-Online-Tools
2. **Mods bibliothèque** -- BuilderItems, tout pack d'assets partagés
3. **Mods de fonctionnalités** -- ajouts de cartes, armes, véhicules
4. **Mods dépendants** -- tout ce qui liste les précédents comme `requiredAddons`

En cas de doute, consultez la page Workshop du mod ou sa documentation. La plupart des auteurs de mods publient l'ordre de chargement requis.

---

## Mods serveur uniquement vs requis par le client

| Paramètre | Qui en a besoin | Exemples typiques |
|-----------|----------------|-------------------|
| `-mod=` | Serveur + tous les clients | Armes, véhicules, cartes, mods UI, vêtements |
| `-servermod=` | Serveur uniquement | Gestionnaires d'économie, outils de journalisation, backends admin, scripts de planification |

La règle est simple : si un mod contient **des scripts côté client, des layouts, des textures ou des modèles**, il doit aller dans `-mod=`. S'il n'exécute que de la logique côté serveur sans assets que le client touche, utilisez `-servermod=`.

Mettre un mod serveur uniquement dans `-mod=` force chaque joueur à le télécharger. Mettre un mod requis par le client dans `-servermod=` cause des textures manquantes, une UI cassée, ou des erreurs de script côté client.

---

## Mettre à jour les mods

### Procédure

1. **Arrêtez le serveur** -- mettre à jour des fichiers pendant que le serveur tourne peut corrompre les PBO
2. **Re-téléchargez** via SteamCMD :
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Copiez les fichiers .bikey mis à jour** -- les auteurs de mods font parfois une rotation de leurs clés de signature. Copiez toujours le `.bikey` frais du dossier `keys/` du mod vers le répertoire `keys/` du serveur
4. **Redémarrez le serveur**

Si vous avez utilisé des liens symboliques (jonctions), l'étape 2 met à jour les fichiers du mod sur place. Si vous avez copié les fichiers manuellement, vous devez les copier à nouveau.

### Mises à jour côté client

Les joueurs abonnés au mod sur Steam Workshop reçoivent les mises à jour automatiquement. Si vous mettez à jour un mod sur le serveur et qu'un joueur a l'ancienne version, il reçoit une erreur de signature et ne peut pas se connecter tant que son client n'est pas mis à jour.

---

## Dépannage des conflits de mods

### Vérifier le log RPT

Ouvrez le dernier fichier `.RPT` dans `profiles/`. Cherchez :

- **"Cannot register"** -- une collision de nom de classe entre deux mods
- **"Missing addons"** -- une dépendance n'est pas chargée (mauvais ordre de chargement ou mod manquant)
- **"Signature verification failed"** -- divergence `.bikey` ou clé manquante

### Vérifier le log de scripts

Ouvrez le dernier `script_*.log` dans `profiles/`. Cherchez :

- Lignes **"SCRIPT (E)"** -- erreurs de script, souvent causées par l'ordre de chargement ou une divergence de version
- **"Definition of variable ... already exists"** -- deux mods définissent la même classe

### Isoler le problème

Quand vous avez beaucoup de mods et que quelque chose casse, testez progressivement :

1. Commencez avec uniquement les mods framework (`@CF`)
2. Ajoutez un mod à la fois
3. Lancez et vérifiez les logs après chaque ajout
4. Le mod qui cause les erreurs est le coupable

### Deux mods modifiant la même classe

Si deux mods utilisent tous les deux `modded class PlayerBase`, celui chargé **en dernier** (le plus à droite dans `-mod=`) gagne. Son appel `super` chaîne vers la version de l'autre mod. Cela fonctionne généralement, mais si un mod surcharge une méthode sans appeler `super`, les modifications de l'autre mod sont perdues.

---

## Erreurs courantes

**Mauvais ordre de chargement.** Le serveur crash ou journalise "Missing addons" parce qu'une dépendance n'était pas encore chargée. Solution : déplacez le mod dépendance plus tôt dans la liste `-mod=`.

**Oublier `-servermod=` pour les mods serveur uniquement.** Les joueurs sont forcés de télécharger un mod dont ils n'ont pas besoin. Solution : déplacez les mods serveur uniquement de `-mod=` vers `-servermod=`.

**Ne pas mettre à jour les fichiers `.bikey` après une mise à jour de mod.** Les joueurs sont expulsés avec "Modified data" parce que la clé du serveur ne correspond pas aux nouvelles signatures PBO du mod. Solution : copiez toujours les fichiers `.bikey` lors de la mise à jour des mods.

**Rempaquetage des PBO de mods.** Rempaqueter les fichiers PBO d'un mod casse sa signature numérique, cause des kicks BattlEye pour chaque joueur, et viole les conditions de la plupart des auteurs de mods. Ne rempaquetiez jamais un mod que vous n'avez pas créé.

**Mélanger les chemins Workshop avec les chemins locaux.** Utiliser le chemin numérique brut du Workshop pour certains mods et des dossiers nommés pour d'autres cause de la confusion lors des mises à jour. Choisissez une approche -- les liens symboliques sont les plus propres.

**Espaces dans les chemins de mods.** Un chemin comme `-mod=@My Mod` casse le parsing. Renommez les dossiers de mods pour éviter les espaces, ou entourez l'intégralité du paramètre de guillemets : `-mod="@My Mod;@CF"`.

**Mod obsolète sur le serveur, mis à jour sur le client (ou inversement).** La divergence de version empêche la connexion. Gardez les versions serveur et Workshop synchronisées. Mettez à jour tous les mods et le serveur en même temps.

---

[Accueil](../README.md) | [<< Précédent : Contrôle d'accès](09-access-control.md) | [Suivant : Dépannage >>](11-troubleshooting.md)
