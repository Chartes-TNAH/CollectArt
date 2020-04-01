from flask import render_template
from ..app import app

# routes pour les erreurs

@app.errorhandler(401)
def not_found_error(error):
    return render_template('error/401.html'), 401


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error/500.html'), 500