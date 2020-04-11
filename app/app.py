from flask import Flask
# importation de Flask depuis le module flask
from flask_sqlalchemy import SQLAlchemy
# importation de SQLAlchemy, qui permet d'interagir avec des bases de données SQL
from flask_login import LoginManager
# importation de flask_login qui permet de gérer les sessions utilisateur·rice·s
import os
# importation du module os, qui permet de communiquer avec le système d'exploitation
from .constantes import CONFIG


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# on stocke ici le chemin absolu du fichier qui comprend le code
templates = os.path.join(chemin_actuel, "templates")
# on stocke le chemin vers les templates tout en faisant une jointure adaptée à l'OS grâce à os.path.join()
statics = os.path.join(chemin_actuel, "static")
# on stocke le chemin vers les statics tout en faisant une jointure adaptée à l'OS 

db = SQLAlchemy()
# initiation de l'objet SQLAlchemy en le stockant dans la variable db
login = LoginManager()
# mise en place de la gestion des utilisateur·rice·s

app = Flask(__name__, 
	template_folder=templates,
	static_folder=statics
	)
# instanciation de l'application
# __name__ est une variable Python prédéfinie qui prend le nom du module dans lequel elle est utilisée
# définition des dossiers contenant les templates et les statics

from .routes import generic, error
# importation des routes (routes générales, erreurs) depuis le dossier routes

def config_app(config_name="production"):
    """ crée l'application """
    app.config.from_object(CONFIG[config_name])
    # configuration de l'app en appelant la constante CONFIG qui définit s'il s'agit de l'app test ou app de production
    # les configurations sont contenues dans le fichier constantes.py, où l'on retrouve la BDD associée

    # Set up extensions
    db.init_app(app)
    login.init_app(app)

    return app





