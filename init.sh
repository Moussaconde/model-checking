#!/bin/bash

# Mise à jour des informations sur les paquets
sudo apt update

# Installation de Python 3
sudo apt install python3

# Installation de Python 3
sudo apt install -y python3.10-venv

# Créer un environnement virtuel
python3 -m venv model_checking_env

# Activer l'environnement virtuel
source model_checking_env/bin/activate

# Installer les dépendances depuis le fichier requirements.txt
pip install -r requirements.txt

chmod +x main.py
