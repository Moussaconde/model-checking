# MODEL CHECKING
Binome : Kodjo Godwin Leger KAVEGE et Moussa CONDE


## Fonctionnalités Principales

Ce projet offre les fonctionnalités suivantes :

## Modélisation de l'Automate : 
La classe Automate permet de représenter un automate à partir d'un fichier .dot en extrayant les nœuds, les transitions et les propositions atomiques.

## Évaluation des Formules CTL : 
La classe CTL_Evaluateur permet d'évaluer les formules CTL sur l'automate en utilisant les règles de marquage et d'exploration.

## Vérification des Formules : 
Le fichier main.py fournit une interface pour charger un fichier .ctl spécifiant la liste des formules à vérifier et un fichier .dot décrivant l'automate, puis affiche les résultats de la vérification des formules.

La partie bonus du projet n'as pas été traitée.



## Preréquis avant utilisation 
Veuillez rendre exécutable ( ` chmod +x init.sh ` ) le fichier `init.sh` qui initialise l'environment d'exécution du programme.

Il va :

- faire l'installation de python3
- installer les packages python requis
- rendre le fichier main.py exécutable
- Activer l'environnement virtuel
(`source model_checking_env/bin/activate`)



## Exécution 
Comme mentioné dans le fichier du TP vous pouvez exécuter le programme

`./main.py chemin_formule_ctl chemin_fichier_dot`

quand vous aurez tout terminé vous pouvez exécuter ce fichier bash `destroy.sh`

Il supprimera :

- l'environnement virutel
- retirer les packages python
