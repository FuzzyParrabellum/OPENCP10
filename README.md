# OPENCP10

**Présentation**

Cette API Django REST nommée apisoftdesk permet à une communauté d'utilisateurs de remonter et de suivre des problèmes lors du développement d'un projet.
Elle est constituée de deux applications, apisoftdesk qui contient la base de l'api (settings, urls etc.) et Troubleshootapp qui contient les modèles, 
views, serializers, etc.
Pour l'utiliser, il est nécessaire de consulter la collection postman associée https://documenter.getpostman.com/view/16689486/VUr1HYTP qui indique comment 
créer des utilisateurs, se connecter, créer des projets, des problèmes ou des commentaires une fois que le serveur de l'application est lancé..

**Instructions d'Installation**

Tout d'abord, téléchargez ces différents fichiers dans un dossier que vous choisirez. Créez ensuite dans ce dossier un environnement virtuel nommé : env

Par ex avec la commande : **python -m venv env**

(La version de python utilisée pour créer cette application est la 3.9.2)

Activez l'environnement virtuel avec la commande : **source env/bin/activate**

Utilisez la commande dans un éditeur de commande : **pip install -r /path/to/requirements.txt** où /path/to/requirements.txt est le chemin d'accès 
vers le fichier requirements.txt fourni dans ce repository

Vous pourrez ensuite lancer l'application apisoftdesk en local avec la commande : **python apisoftdesk/manage.py runserver** et commencer à utiliser l'API
via les endpoints et les paramètres définis par la collection postman associée.

