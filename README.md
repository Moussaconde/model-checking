# MODEL CHECKING
Binome : <b> Kodjo Godwin Leger KAVEGE </b> et <b> Moussa CONDE </b>


## Fonctionnalités Principales

Ce projet offre les fonctionnalités suivantes :

## Modélisation de l'Automate : 
La classe Automate permet de représenter un automate à partir d'un fichier .dot en extrayant les nœuds, les transitions et les propositions atomiques.

## Évaluation des Formules CTL : 
La classe CTL_Evaluateur permet d'évaluer les formules CTL sur l'automate en utilisant les règles de marquage et d'exploration.

## Vérification des Formules : 
Le fichier main.py fournit une interface pour charger un fichier *.ctl* spécifiant la liste des formules à vérifier et un fichier *.dot* décrivant l'automate, puis affiche les résultats de la vérification des formules.

Les parties bonus implémentées sont :

- L'implication (=>)
- Composition de A et E d’une part avec F, G, U et X d’autre part.
- Gestion de l'exécution de multiple formules 




## Preréquis avant utilisation 
Veuillez rendre exécutable ( `chmod +x init.sh` ) le fichier `init.sh` qui initialise l'environment d'exécution du programme.

Il va :

- faire l'installation de python3
- installer les packages python requis
- rendre le fichier main.py exécutable



## Exécution 

Veuillez activer l'environnement virtuel afin de prendre en compte les packages installés par pip. 

*Command <br>*
`source model_checking_env/bin/activate`

Comme mentioné dans le fichier du TP vous pouvez maintenant exécuter le programme

`./main.py chemin_formule_ctl chemin_fichier_dot`

quand vous aurez tout terminé vous pouvez exécuter ce fichier bash `destroy.sh`

Il supprimera :

- l'environnement virutel
- les packages python installés
