from flask import render_template, url_for, request, flash, redirect
# importation de render_template (relie les templates aux routes), url_for (permet de construire des url vers les 
# fonctions et les pages html), request (permet d'importer types d'objets et de les utiliser comme insinstance), 
# flash (envoie des messages flash) et redirect (permet de rediriger vers l'url d'une autre route) depuis le module flask
from flask_login import current_user, login_user, logout_user, login_required
# importation de current_user (utilisateur courant), login_user (connexion), logout_user (déconnexion) et login_required 
# (accès limité) pour gérer les sessions utilisateur·rice·s
from sqlalchemy import or_
# importation de l'opérateur OR depuis SQLAlchemy pour faire du requêtage

from ..app import app, db, login
# importation de la variable app, de la BDD et de login pour gérer les utilisateur·rice·s
from ..constantes import RESULTATS_PAR_PAGE
# importation de la variable RESULTATS_PAR_PAGE utilisée pour les routes recherche et index
from ..modeles.donnees import Collection, Work, Mediums
# importation des classes Collection, Work et Mediums du fichier données.py
from ..modeles.utilisateurs import User
# importation de la classe User du fichier utilisateurs.py



# | ROUTES GENERALES |

@app.route("/")
def accueil():
    """
    Route permettant d'afficher la page d'accueil
    :return: template accueil.html
    :rtype: template
    """
    collections = Collection.query.all()
    return render_template("pages/accueil.html", nom="CollectArt", collections=collections)
    # La fonction render_template prend comme premier argument le chemin du template et en deuxième des arguments nommés, qui
    # peuvent ensuite être réutilisés en tant que variables dans les templates.

    
@app.route("/collections")
def collections():
    """
    Route permettant d'afficher les différentes collections de la base de données
    :return: template collections.html
    :rtype: template
    """
    collections = Collection.query.order_by(Collection.collection_name.desc())
    return render_template("pages/collections.html", nom="CollectArt", collections=collections)


@app.route("/collection/<int:collection_id>")
def collection(collection_id):
    """
    Route permettant d'afficher les données d'une collection et les oeuvres qui y sont associées
    :param collection_id: clé primaire d'une collection (int)
    :return: template collection.html
    :rtype: template
    """
    unique_collection = Collection.query.get(collection_id)
    work = unique_collection.work
    return render_template("pages/collection.html", nom="CollectArt", collection=unique_collection, work=work)


@app.route("/collection/oeuvre/<int:work_id>")
def oeuvre(work_id):
    """
    Route permettant d'afficher la notice d'une oeuvre
    :param work_id: clé primaire d'une oeuvre (int)
    :return: template oeuvre.html
    :rtype: template
    """
    unique_work = Work.query.get(work_id)
    return render_template("pages/oeuvre.html", nom="CollectArt", work=unique_work)


@app.route("/recherche")
def recherche():
    """
    Route permettant de faire de la recherche plein-texte et d'afficher une liste de résultats
    :return: template resultats.html
    :rtype: template
    """
    keyword = request.args.get("keyword", None)
    # stockage dans la variable keywork une liste contenant la valeur du mot-clé rentré par l'utilisateur·rice
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    # si le numéro de la page est une chaîne de caractères composée uniquement de chiffres, on la recaste en integer
    # sinon, le numéro de la page est égal à 1

    results = [] 
    # On crée une liste vide de résultats
    title = "Recherche"

    if keyword :
    # Si un mot-clé est rentré dans la barre de recherche, on requête les tables de la BDD pour vérifier s'il y a des 
    # correspondances. Le résultat est stocké dans la liste résults = []
        results = Collection.query.filter(
            or_(
                Collection.collection_name.like("%{}%".format(keyword)),
                Collection.collection_collector_name.like("%{}%".format(keyword)),
                Collection.collection_collector_firstname.like("%{}%".format(keyword)),
                Collection.collection_collector_date.like("%{}%".format(keyword)),
                Collection.collection_collector_bio.like("%{}%".format(keyword)),
                Collection.work.any((Work.work_title).like("%{}%".format(keyword))),
                Collection.work.any((Work.work_author).like("%{}%".format(keyword))), 
                Collection.work.any((Work.work_date).like("%{}%".format(keyword))),
                Collection.work.any((Work.work_medium).like("%{}%".format(keyword))),
                )
                # on requête la table collection et la table work grâce à la commande any (au moins un des critères est true)
            ).order_by(Collection.collection_name.asc()).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
            # creation de la pagination avec la methode .paginate qui remplace le .all dans la requête sur la base
        title = "Résultat(s) de la recherche : " + keyword + "."

    return render_template("pages/resultats.html", nom="CollectArt", results=results, title=title, keyword=keyword)


@app.route("/index")
def index():
    """ 
    Route qui affiche la liste des collectionneur·euse·s (ordonnée par nom) de la base
    :return: template index.html
    :rtype: template
    """
    title="Index"
    collector = Collection.query.all()
    
    if len(collector) == 0:
        return render_template("pages/index.html", nom="CollectArt", collector=collector, title=title)
    else : 
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1
        
        collector = Collection.query.order_by(
                Collection.collection_collector_name
            ).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
        return render_template("pages/index.html", nom="CollectArt", collector=collector, title=title)



# | ROUTES INTERFACE UTILISATEUR·RICE |

@app.route("/edit-collection", methods=["GET", "POST"])
@login_required
def edit_collection():
    """
    Route permettant à un·e utilisateur·rice de créer une nouvelle collection
    :return: redirection ou template edit_collection.html
    :rtype: template
    """
    if request.method == "POST":
    # si le formulaire est envoyé, on passe en méthode POST
        status, data = Collection.add_collection(
        # on applique la fonction add_collection définie dans le fichier données.py
            name=request.form.get("name", None),
            collector_name=request.form.get("collector_name", None),
            collector_firstname=request.form.get("collector_firstname", None),
            collector_date=request.form.get("collector_date", None),
            collector_bio=request.form.get("collector_bio", None)
            )

        if status is True:
            flash("Création d'une nouvelle collection réussie !", "success")
            return redirect("/collections")
        else:
            flash("La création d'une nouvelle collection a échoué pour les raisons suivantes : " + ", ".join(data), "error") 
            return render_template("pages/edit-collection.html", nom="CollectArt")
    else:
        return render_template("pages/edit-collection.html", nom="CollectArt")


@app.route("/update-collection/<int:collection_id>", methods=["POST", "GET"])
@login_required
def update_collection(collection_id):
    """ 
    Route permettant de modifier les données d'une collection
    :param collection_id: ID de la collection récupérée depuis la page collection
    :return: redirection ou template update-collection.html
    :rtype: template
    """
    
    if request.method == "GET":
        updateCollection = Collection.query.get(collection_id)
        return render_template("pages/update-collection.html", nom="CollectArt", updateCollection=updateCollection)
        # si on est en méthode GET, on renvoie sur la page html les éléments de l'objet collection correspondant à l'id 
        # de la route
 
    else:
        status, data = Collection.update_collection(
            collection_id=collection_id,
            name=request.form.get("name", None),
            collector_name=request.form.get("collector_name", None),
            collector_firstname=request.form.get("collector_firstname", None),
            collector_date=request.form.get("collector_date", None),
            collector_bio=request.form.get("collector_bio", None)
        )
        # sinon, on récupère les données du formulaire à modifier et on les modifie grâce à la fonction update_collection

        if status is True:
            flash("Modification réussie !", "success")
            return redirect("/collections")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(data), "danger")
            updateCollection = Collection.query.get(collection_id)
            return render_template("pages/update-collection.html", nom="CollectArt", updateCollection=updateCollection)


@app.route("/delete-collection/<int:collection_id>", methods=["POST", "GET"])
@login_required
def delete_collection(collection_id):
    """ 
    Route permettant de supprimer une collection et ses données
    :param collection_id : ID de la collection
    :return: redirection ou template delete-collection.html 
    :rtype: template
    """
    deleteCollection = Collection.query.get(collection_id)
    works = deleteCollection.work
    # on cherche les oeuvres liées à la collection

    if request.method == "POST":
        status = Collection.delete_collection(
            collection_id=collection_id
        )
        # si le formulaire a été envoyé, on passe en méthode POST et on récupère la notice puis on applique la méthode 
        # delete_collection
        
        if status is True:
            flash("Suppression réussie !", "success")
            return redirect("/collections")
        else:
            flash("La suppression a échouée...", "error")
            return redirect("/collections")
    else:
        return render_template("pages/delete-collection.html", nom="CollectArt", deleteCollection=deleteCollection)


@app.route("/collection/<int:collection_id>/edit-work", methods=["GET", "POST"])
@login_required
def edit_work(collection_id):
    """
    Route permettant à un·e utilisateur·rice de créer la notice d'une nouvelle oeuvre et de l'ajouter à une collection
    :param collection_id: ID de la collection récupérée depuis la page collection
    :return: redirection ou template edit-work.html
    :rtype: template
    """

    mediums = Mediums.query.all()
    unique_collection = Collection.query.get(collection_id)
    
    if request.method == "POST":
        status, data = Work.add_work(
            title=request.form.get("title", None),
            author=request.form.get("author", None),
            date=request.form.get("date", None),
            medium=request.form.get("medium", None),
            dimensions=request.form.get("dimensions", None),
            image=request.form.get("image", None),
            collection_id=collection_id
            )

        if status is True:
            flash("Vous venez d'ajouter une nouvelle oeuvre à votre collection !", "success")
            return redirect("/collections")
        else:
            flash("L'ajout d'une nouvelle oeuvre a échoué pour les raisons suivantes : " + ", ".join(data), "error") 
            return render_template("pages/edit-work.html", nom="CollectArt", collection=unique_collection, mediums=mediums)
    else:
        return render_template("pages/edit-work.html", nom="CollectArt", collection=unique_collection, mediums=mediums)


@app.route("/update-work/<int:work_id>", methods=["POST", "GET"])
@login_required
def update_work(work_id):
    """ 
    Route permettant de modifier les données d'une collection
    :param work_id: ID de l'oeuvre récupérée depuis la page oeuvre
    :return: redirection ou template update-work.html
    :rtype: template
    """
    
    if request.method == "GET":
        updateWork = Work.query.get(work_id)
        return render_template("pages/update-work.html", updateWork=updateWork)

    else:
        status, data = Work.update_work(
            work_id=work_id,
            title=request.form.get("title", None),
            author=request.form.get("author", None),
            date=request.form.get("date", None),
            medium=request.form.get("medium", None),
            dimensions=request.form.get("dimensions", None),
            image=request.form.get("image", None)
            )

        if status is True:
            flash("Modification réussie !", "success")
            return redirect("/collections")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(data), "danger")
            updateWork = Work.query.get(work_id)
            return render_template("pages/update-work.html", nom="CollectArt", updateWork=updateWork)


@app.route("/delete-work/<int:work_id>", methods=["POST", "GET"])
@login_required
def delete_work(work_id):
    """ 
    Route pour supprimer une oeuvre et ses données dans la base
    :param work_id : ID de l'oeuvre
    :return: redirection ou template delete-work.html
    :rtype: template
    """
    deleteWork = Work.query.get(work_id)

    if request.method == "POST":
        status = Work.delete_work(
            work_id=work_id
        )

        if status is True:
            flash("Suppression réussie !", "success")
            return redirect("/collections")
        else:
            flash("La suppresion a échouée...", "error")
            return redirect("/collections")
    else:
        return render_template("pages/delete-work.html", deleteWork=deleteWork)



# | ROUTES POUR LA GESTION DES UTILISATEUR·RICE·S |

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """
    Route permettant de gérer les inscriptions utilisateur·rice·s
    :return: redirection ou template inscription.html
    :rtype: template
    """
    if request.method == "POST":
        status, data = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            name=request.form.get("name", None),
            password=request.form.get("password", None)
            )
        
        if status is True:
            flash("Inscription réussie ! Vous pouvez désormais vous connecter", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées dans les champs suivants : " + ", ".join(data), "error")
            return render_template("pages/inscription.html", nom="CollectArt")
    else:
        return render_template("pages/inscription.html", nom="CollectArt")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """
    Route permettant de gérer les connexions
    :return: reidrection ou template connexion.html
    :rtype: template
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté·e", "info")
        return redirect("/")
        # si l'utilisateur·rice est déjà connecté·e, il/elle est redirigé·e vers la page d'accueil

    if request.method == "POST":
        user = User.identification(
            login=request.form.get("login", None), 
            password=request.form.get("password", None)
        )

        if user:
            flash("Connexion réussie !", "success")
            login_user(user)
            return redirect("/")
        else:
            flash("Nom d'utilisateur·rice ou mot de passe incorrect", "error")
    return render_template("pages/connexion.html", nom="CollectArt")
login.login_view = "connexion"


@app.route("/deconnexion")
def deconnexion():
    """
    Route permettant de gérer les déconnexions
    :return: redirection vers l'accueil
    :rtype: template
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté·e", "info")
    return redirect("/")
