from warnings import warn

SECRET_KEY = "JE SUIS UN SECRET !"
# variable utilisée comme clé cryptographique, qui permet de générer des sigantures ou tokens

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
