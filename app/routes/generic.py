from flask import render_template, url_for, request, flash, redirect
# importation de render_template, request, flash et redirect depuis le module flask
from flask_login import current_user, login_user, logout_user, login_required
# importation de current_user, login_user, logout_user et login_required pour gérer les sessions 
# utilisateur·rice·s
from sqlalchemy import or_
# importation de l'opérateur OR depuis SQLAlchemy

from ..app import app, db, login
# importation de l'application, de la BDD et de login pour gérer les utilisateur·rice·s
from ..constantes import RESULTATS_PAR_PAGE
# importation de la variable RESULTATS_PAR_PAGE utilisée pour les routes recherche et index
from ..modeles.donnees import Collection, Work, Mediums
# importation des classes Collection, Work et Mediums du fichier données.py
from ..modeles.utilisateurs import User
# importation de la classe User du fichier utilisateurs.py



# ROUTES GENERALES

@app.route("/")
def accueil():
    """
    Route permettant d'afficher la page d'accueil
    :return: template accueil.html
    :rtype: template
    """
    collections = Collection.query.all()
    return render_template("pages/accueil.html", nom="CollectArt", collections=collections)
    
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
    Route permettant d'afficher les données d'une collection
    :param collection_id: clé primaire d'une collection dans la table Collection
    :return: template collection.html
    :rtype: template
    """
    unique_collection = Collection.query.get(collection_id)
    work = unique_collection.work
    return render_template("pages/collection.html", nom="CollectArt", collection=unique_collection, work=work)

@app.route("/collection/oeuvre/<int:work_id>")
def oeuvre(work_id):
    """
    Route permettant d'afficher les données d'une oeuvre
    :param work_id: clé primaire d'une oeuvre dans la table Work
    :return: template collection.html
    :rtype: template
    """
    unique_work = Work.query.get(work_id)
    return render_template("pages/oeuvre.html", nom="CollectArt", work=unique_work)

@app.route("/recherche")
def recherche():
    """
    Route permettant de faire de la recherche plein-texte
    :return: template resultats.html
    :rtype: template
    """
    keyword = request.args.get("keyword", None)
    # stockage dans la variable mot-clef une liste contenant la valeur du mot-clé rentré par 
    # l'utilisateur.
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    results = [] 
    # On crée une liste vide de résultat
    title = "Recherche"

    if keyword :
    # Si un mot-clé est rentré dans la barre de recherche, on requête les tables de la BDD pour 
    # vérifier s'il y a des correspondances. Le résultat est stocké dans la liste résults = []
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
            ).order_by(Collection.collection_name.asc()).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
        title = "Résultat(s) de la recherche : " + keyword + "."

    return render_template("pages/resultats.html", results=results, title=title, keyword=keyword)

@app.route("/index")
def index():
    """ 
    Route qui affiche la liste des collectionneur·euse·s (Nom, prenom) de la base
    :return: template resultats.html
    :rtype: template
    """
    title="Index"
    # vérification que la base de données n'est pas vide : 
    collector = Collection.query.all()
 
    if len(collector) == 0:
        return render_template("pages/index.html", collector=collector, title=title)
    else : 
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

        # creation de la pagination avec la methode .paginate qui remplace le .all dans la requête sur la base
        collector = Collection.query.order_by(Collection.collection_collector_name
            ).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
        return render_template("pages/index.html", collector=collector, title=title)



# ROUTES INTERFACE UTILISATEUR·RICE

@app.route("/edit-collection", methods=["GET", "POST"])
@login_required
def edit_collection():
    """
    Route permettant à un·e utilisateur·rice d'éditer les données d'une collection
    :return: template edit_collection.html
    :rtype: template
    """
    if request.method == "POST":
        status, data = Collection.add_collection(
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
            return render_template("pages/edit-collection.html")
    else:
        return render_template("pages/edit-collection.html", nom="CollectArt")

@app.route("/update-collection/<int:collection_id>", methods=["POST", "GET"])
@login_required
def update_collection(collection_id):
    """ 
    Route permettant de modifier les données d'une collection
    :param collection_id: ID de la collection récupérée depuis la page notice
    :return: template update-collection.html
    :rtype: template
    """
    
    if request.method == "GET":
        updateCollection = Collection.query.get(collection_id)
        return render_template("pages/update-collection.html", updateCollection=updateCollection)
        # renvoie sur la page html les éléments de l'objet collection correspondant à l'identifiant de la route

    # on récupère les données du formulaire modifié
    else:
        status, data = Collection.update_collection(
            collection_id=collection_id,
            name=request.form.get("name", None),
            collector_name=request.form.get("collector_name", None),
            collector_firstname=request.form.get("collector_firstname", None),
            collector_date=request.form.get("collector_date", None),
            collector_bio=request.form.get("collector_bio", None)
        )

        if status is True:
            flash("Modification réussie !", "success")
            return redirect("/collections")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(data), "danger")
            updateCollection = Collection.query.get(collection_id)
            return render_template("pages/update-collection.html", updateCollection=updateCollection)

@app.route("/delete-collection/<int:collection_id>", methods=["POST", "GET"])
@login_required
def delete_collection(collection_id):
    """ 
    Route pour supprimer une oeuvre dans la base
    :param work_id : ID de l'oeuvre
    """
    deleteCollection = Collection.query.get(collection_id)

    if request.method == "POST":
        status, data = Collection.delete_collection(
            collection_id=collection_id, 
            name=request.args.get("name", None),
            collector_name=request.args.get("collector_name", None),
            collector_firstname=request.args.get("collector_firstname", None),
            collector_date=request.args.get("collector_date", None),
            collector_bio=request.args.get("collector_bio", None))

        if status is True:
            flash("Suppression réussie !", "success")
            return redirect("/collections")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(data), "error")
            return redirect("pages/delete-work.html")
    else:
        return render_template("pages/delete-collection.html", deleteCollection=deleteCollection)


@app.route("/collection/<int:collection_id>/edit-work", methods=["GET", "POST"])
@login_required
def edit_work(collection_id):
    """
    Route permettant à un·e utilisateur·rice d'éditer les données d'une oeuvre
    :return: template collection_edit.html
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
            return redirect("/collection/<int:collection_id>/edit-work.html")
        else:
            flash("L'ajout d'une nouvelle oeuvre a échoué pour les raisons suivantes : " + ", ".join(data), "error") 
            return render_template("pages/edit-work.html")
    else:
        return render_template("pages/edit-work.html", nom="CollectArt", collection=unique_collection, mediums=mediums)

@app.route("/delete-work/<int:work_id>", methods=["POST", "GET"])
@login_required
def delete_work(work_id):
    """ 
    Route pour supprimer une oeuvre dans la base
    :param work_id : ID de l'oeuvre
    """
    deleteWork = Work.query.get(work_id)

    if request.method == "POST":
        status, data = Work.delete_work(
            work_id=work_id, 
            title=request.args.get("title", None),
            author=request.args.get("author", None),
            date=request.args.get("date", None),
            medium=request.args.get("medium", None),
            dimensions=request.args.get("dimensions", None),
            image=request.args.get("image", None))
        # on récupère les données de la notice 

        if status is True:
            flash("Suppression réussie !", "success")
            return redirect("/collections")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(data), "error")
            return redirect("pages/delete-work.html")
    else:
        return render_template("pages/delete-work.html", deleteWork=deleteWork)

# AJOUTER MODIFICATION D'UNE COLLECTION + MODIFICATION D'UNE OEUVRE



# ROUTES POUR LA GESTION DES UTILISATEUR·RICE·S

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """
    Route permettant de gérer les inscriptions utilisateur·rice·s
    :return: template inscription.html
    :rtype: template
    """
    if request.method == "POST":
    # Si le formulaire est envoyé, on passe en méthode POST
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
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """
    Route permettant de gérer les connexions
    :return: template connexion.html
    :rtype: template
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté·e", "info")
        return redirect("/")

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
    return render_template("pages/connexion.html")
login.login_view = "connexion"

@app.route("/deconnexion")
def deconnexion():
    """
    Route permettant de gérer les déconnexions
    :return: template accueil.html
    :rtype: template
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté·e", "info")
    return redirect("/")

