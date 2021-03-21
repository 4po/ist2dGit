# 4poGit
Script Python qui commite et pousse les changements de manière agressive en utilisant Git.

## Ce qu'il fait (complet et fonctionnel)
* Tente de commiter toutes les x secondes si un changement a été fait.
 * Réglez la minuterie à 1 seconde pour obtenir des commits presque instantanés lors de la sauvegarde. Il ne fera aucune commande git s'il n'y a pas de changement, les fichiers sont surveillés.
 * Si plusieurs fichiers sont sauvegardés ensemble, ils se retrouveront dans le même commit. Bien qu'il soit possible de commiter chaque fichier modifié individuellement sur les événements de changement de fichier, ce qui serait excessif et inadapté à mes besoins.
* Tente de pousser toutes les y secondes si un commit a été fait (par le script, ne surveille pas les commits manuels).

## Travail en cours / développements proposés.
* Simple pulls.

## Ce qu'il ne fera pas
 * Utiliser SSH (complication inutile pour mes besoins).
 * Gérer plusieurs dépôts.
 * Utilisation de gitignore
  * Git l'utilisera toujours comme d'habitude, mais ce script tentera d'ajouter `add -A` lorsque les fichiers ignorés sont modifiés (bien que rien ne soit ajouté ou validé).
  * Ceci n'est un problème que si vous avez des fichiers ignorés rapidement modifiés, ce qui provoque un spam de `add -A'. Dans ce cas, essayez d'ajouter l'ignore à `ignore_patterns` dans le script.

## Pourquoi
 * J'utilise ceci pour sauvegarder et pousser automatiquement mon Zim-Wiki sur mon serveur Git.
 * Aussi utile pour récupérer du contenu non-commissionné supprimé impulsivement.

### Usage
### Avertissements
 * Le script ne pousse que sa propre branche.
 * Si vous autorisez le script à changer de branche, il continuera à partir de l'état de l'arbre de travail de la branche à partir de laquelle il change (pas une fusion normale, un remplacement total sur le même arbre).

### Configuration
Modifiez les chemins en haut du script :
 * Mettez `git_path` dans le chemin de votre git.
 * Mettez `repo_path` dans le chemin du dépôt que vous souhaitez autocommiter.
 * Mettez `ac_branch` à n'importe quel nom de branche que vous voulez pour les commits automatiques.

Modifiez les délais pour les adapter à vos besoins.

Editez `x.txt` en insérant votre nom d'utilisateur, mot de passe, hôte et dépôt. Vous pouvez aussi coder en dur les valeurs dans le script

Lancez le script dans une console (si vous voulez exécuter le script de manière cachée, vous devez éditer la partie pause du script).

### Exécution
Si le dépôt n'est pas déjà sur la branche `ac_branch`, le script se mettra en pause et demandera la permission de changer de branche. Le script restera en pause jusqu'à ce que la permission soit donnée.

L'extraction d'une autre branche provoquera une pause automatique du script. C'est une façon de permettre le travail manuel sur le référentiel. Le script ne reprendra pas jusqu'à ce qu'on lui dise de le faire. J'ai tendance à `merger --no-ff` sur ma branche master lorsque je crée des commits correctement nommés.


## Exigences
Construit et testé sur :
- WinPython 3.4 + Watchdog
- Windows 7
- git 1.9.5

## Participez
N'hésitez pas à faire des pull-request, fork, issue ou à me dire où mon code a besoin d'être amélioré, mon Python est loin d'être parfait.

## FAQ
 * Pourquoi pas de GitPython ?
  * J'ai décidé que ce serait un script super simple, je pensais qu'une autre bibliothèque pourrait compliquer les choses et cacher des détails simples de mise en œuvre.

