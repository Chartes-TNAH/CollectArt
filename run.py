from app.app import app
# importation de la variable app (l'application) depuis le package app (variable définie dans le fichier app.py)

if __name__ == "__main__":
	app.run(debug=True)
# app.run() lance l'application
# le mode debug permet de lancer un débogueur pendant le développement de l'application
