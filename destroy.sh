#!/bin/bash

# Installation de Python 3
sudo apt uninstall -y python3.10-venv

# Créer un environnement virtuel
rm -fr venv model_checking_env
