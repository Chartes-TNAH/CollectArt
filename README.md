# CollectArt




CollectArt est une application web répertoriant des collections d'art d'hier et d'aujourd'hui, sous la forme d'une base de données collaborative. Elle a été créée par Caroline Corbières.


**Sur CollectArt, il est possible :**
  - de consulter des notices de collections d'art privées et des notices d'oeuvres.
  - de consulter l'index des collectionneur·euse·s.
  - de faire une recherche rapide parmi les collections.
  - pour les utilisateur·rice·s ayant un compte, de créer, modifier et supprimer des notices collections et oeuvres afin d'alimenter la base de données. 
  

**Développement du projet :** 

Ce projet a été développé grâce au langage de programmation python 3 et s’appuie sur une base de données. Le graphisme de l’application a été réalisé grâce à Bootstrap et s'appuie sur celui du projet [Digital Muret](https://digitalmuret.inha.fr/s/digital-muret/page/accueil) réalisé par l'INHA et placé sous licence CC BY 4.0. 

Les données tests utilisées pour l'application proviennent d'un des datasets sur des collectionneur·euse·s du siècle d'or néerlandais, mis en ligne sur le Github de la [Frick Collection](https://github.com/frickcollection) et placé sous licence CC0 1.0.


**Comment lancer CollectArt ?**

En local : 
  - Installer python3
  - Cloner ce repository : `git clone https://github.com/carolinecorbieres/CollectArt`
  - Installer puis activer un environnement virtuel: `virtualenv -p python3 env` puis `source env/bin/activate`
  - Installer les librairies nécessaires au fonctionnement de l’application (voir les [requirements](https://github.com/carolinecorbieres/CollectArt/blob/master/requirements.txt)): `pip install requirements.txt`
  - Lancer le fichier run.py: `python3 run.py`
