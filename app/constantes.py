from warnings import warn

RESULTATS_PAR_PAGE = 6
# variable qui définit le nombre de résultats par page (utilisée pour l'index et la recherche simple)

SECRET_KEY = "JE SUIS UN SECRET !"
# variable utilisée comme clé cryptographique, qui permet de générer des sigantures ou tokens

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)


class _TEST:
	# comme la classe débute par _, cela signifie qu'elle ne devrait pas être appelée directement
    SECRET_KEY = SECRET_KEY
    # configuration du secret
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    # configuration de la base de données test
    # chemin qui indique où chercher la BDD: chemin absolu vers le fichier db.sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    # configuration du secret
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'
    # configuration de la base de données production
    # chemin qui indique où chercher la BDD: chemin absolu vers le fichier db.sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False

CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
    # les deux classes sont regroupées dans un dictionnaire afin de pouvoir les appeler facilement
}
