# MODEL CHECKING

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
