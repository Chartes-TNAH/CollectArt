from app.app import config_app
# importation de la focntion config_app (qui retourne l'application) depuis le package app (variable définie dans le 
# fichier app.py)

if __name__ == "__main__":
	app = config_app("production")
	app.run(debug=True)
# app.run() lance l'application
# le mode debug permet de lancer un débogueur pendant le développement de l'application
