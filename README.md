# DataScientest_Projet3
Projet n°3 - Base de données

## Choix de la base de données

En terme de données, j'ai opté pour les données concernant les vins. J'ai porté mon dévolu sur cette données car elle présentait un potentiel pour produire une base de données relationnelle "classique

En terme de données de données, j'ai opté pourPostgreSQL (le script est  cependant potentiellement compa).



## L'intégration des données et la modélisation de la base

Le script integration.sql est contient l'ensemble des commandes pour intégrer le fichier CSV Source dans une table PostgreSQL. L'intégration s'effectue de manière brute dans un 1er temps. 
Ensuite, les commandes SQL permettent de construire une base de données relationnelle. 


## L'API FastAPI

L'API a été développé avec FastAPI. 
Le fichier main.py contient le script. 

Dans le script, les paramètres de connexion, nom d'utilisateur et mot de passe sont à adapter. 

Je n'ai intégrer d'authentification à l'API

Pour l'executer : 

uvicorn main:app --reload

puis localhost:8000

La documentation de l'API est acessible à l'URL : http://localhost:8000/docs


L'API contient l'accès à toutes les listes ainsi que 3 fonctions de recherche, deux fonctions d'ajout de Vin et de Pays. 



