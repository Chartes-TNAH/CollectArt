from flask import render_template, url_for
# importation de render_template (pour relier les templates aux routes) et d'url_for (pour construire des URL vers les
# fonctions et les pages html
from ..app import app
# importation de la variable app qui instancie l'application


# | ROUTES POUR LES ERREURS COURANTES |

@app.errorhandler(401)
def not_found_error(error):
    """
    Route qui permet de en cas d'erreur 401 (accès non autorisé) de renvoyer vers la page 401.html
    :return: template 401.html
    :rtype: template
    """
    return render_template('error/401.html'), 401


@app.errorhandler(404)
def not_found_error(error):
    """
    Route qui permet de en cas d'erreur 404 (page introuvable) de renvoyer vers la page 404.html
    :return: template 404.html
    :rtype: template
    """
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Route qui permet de en cas d'erreur 500 (erreur de serveur interne) de renvoyer vers la page 500.html
    :return: template 500.html
    :rtype: template
    """
    return render_template('error/500.html'), 500
