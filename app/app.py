from flask import Flask
# importation de Flask depuis le module flask
from flask_sqlalchemy import SQLAlchemy
# importation de SQLAlchemy, qui permet d'interagir avec la BDD SQL
from flask_login import LoginManager
# importation de flask_login qui permet de gérer les sessions utilisateur·rice·s
import os
# importation du module os, qui permet de communiquer avec le système d'exploitation
from .constantes import SECRET_KEY


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# stockage du chemin absolu du fichier qui comprend le code
templates = os.path.join(chemin_actuel, "templates")
# stockage du chemin vers les templates tout en faisant une jointure adaptée à l'OS grâce à os.path.join()
statics = os.path.join(chemin_actuel, "static")
# stockage du chemin vers les statics tout en faisant une jointure adaptée à l'OS 


app = Flask(__name__, 
	template_folder=templates,
	static_folder=statics
	)
# instanciation de l'application
# __name__ est une variable Python prédéfinie qui prend le nom du module dans lequel elle est utilisée
# définition des dossiers contenant les templates et les statics

app.config['SECRET_KEY'] = SECRET_KEY
# configuration du secret, utile pour gérer les sessions utilisateur·rice·s ou des éléments de sécurité avancée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
# lien avec la BDD sqlite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# configuration de la BDD

db = SQLAlchemy(app)
# initiation de l'objet SQLAlchemy en lui fournissant l'application comme variable et en le stockant dans la variable db
login = LoginManager(app)
# mise en place de la gestion des utilisateur·rice·s

from .routes import generic, error
# importation des routes (routes générales, erreurs) depuis le dossier routes
