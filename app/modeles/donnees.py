from flask import url_for
# importation de url_for (pour construire des URL vers les fonctions et les pages html) depuis flask

from .. app import db
# importation de la BDD


class Collection(db.Model):
    __tablename__ = "collection"
    collection_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    collection_name = db.Column(db.Text, nullable=False)
    collection_collector_name = db.Column(db.Text, nullable=False)
    collection_collector_firstname = db.Column(db.Text)
    collection_collector_date = db.Column(db.Text)
    collection_collector_bio = db.Column(db.Text)
    authorships_collection = db.relationship("Authorship_collection", back_populates="collection_collection")
    work = db.relationship("Work", backref="collection", cascade="all, delete, delete-orphan")
    # cascade permet d'appliquer l'action exercée sur l'objet parent à ses enfants (ici la suppression), elle est précisée au 
    # niveau de la relation one to many
    # delete-orphan indique que l'objet enfant doit suivre son parent dans tous les cas et être supprimé une fois qu'il n'est 
    # plus associé au parent (c'est-à-dire quand il n'a plus de clé étrangère)

    def get_id(self):
        """
        Retourne l'id de l'objet actuellement utilisé
        :return: ID de la collection
        :rtype: int
        """
        return(self.collection_id)

    @staticmethod
    def add_collection(name, collector_name, collector_firstname, collector_date, collector_bio):
        """
        Fonction qui permet d'ajouter une nouvelle collection dans la BDD
        :param name: nom de la collection (str)
        :param collector_name: nom de famille du/de la collectionneur·euse (str)
        :param collector_firstname: prénom du/de la collectionneur·euse (str)
        :param collector_date: date·s du/de la collectionneur·euse (str)
        :param collector_bio: petite biographie du/de la collectionneur·euse (str)
        :return: Booléen
        """
        errors = []
        # création d'une liste vide pour y stocker les erreurs

        if not name:
            errors.append("veuillez renseigner le nom de la collection.")
        if not collector_name:
            errors.append("veuillez renseigner le nom de famille du/de la collectionneur·euse.")
        if not collector_firstname:
            errors.append("veuillez renseigner le prénom du/de la collectionneur·euse")
        if not collector_date:
            errors.append("veuillez renseigner les dates du/de la collectionneur·euse, si elles sont inconnues indiquer: dates inconnues")
        # vérification que les champs sont bien renseignés (des indications dans le message d'erreur permettent de compléter 
	# les données si elles sont inconnues)

        if len(errors) > 0:
            return False, errors
        # Si il y a au moins une erreur, cela retourne false

        new_collection = Collection(
            collection_name=name,
            collection_collector_name=collector_name,
            collection_collector_firstname=collector_firstname,
            collection_collector_date=collector_date,
            collection_collector_bio=collector_bio)
        # ajout d'une nouvelle entrée collection dans la table collection avec les champs correspondant aux paramètres du 
	# modèle

        try:
            db.session.add(new_collection)
	    # ajout de la collection à la BDD
            db.session.commit()
            return True, new_collection

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def update_collection(collection_id, name, collector_name, collector_firstname, collector_date, collector_bio):
        """
        Fonction qui permet de modifier une collection de la BDD
        :param collection_id: id de la collection (int)
        :param name: nom de la collection (str)
        :param collector_name: nom de famille du/de la collectionneur·euse (str)
        :param collector_firstname: prénom du/de la collectionneur·euse (str)
        :param collector_date: date·s du/de la collectionneur·euse (str)
        :param collector_bio: petite biographie du/de la collectionneur·euse (str)
        :return: Booléen
        """
        errors=[]
        if not name:
            errors.append("veuillez renseigner le nom de la collection")
        if not collector_name:
            errors.append("veuillez renseigner le nom de famille du/de la collectionneur·euse")
        if not collector_firstname:
            errors.append("veuillez renseigner le prénom du/de la collectionneur·euse")
        if not collector_date:
            errors.append("veuillez renseigner les dates du/de la collectionneur·euse, si elles sont inconnues indiquer: dates inconnues")

        if len(errors) > 0:
            return False, errors

        update_collection = Collection.query.get(collection_id)
        # récupération d'une collection dans la BDD

        if update_collection.collection_name == name \
            and update_collection.collection_collector_name == collector_name \
            and update_collection.collection_collector_firstname == collector_firstname \
            and update_collection.collection_collector_date == collector_date \
            and update_collection.collection_collector_bio == collector_bio:
            errors.append("Aucune modification n'a été réalisée")
        # vérification qu'au moins un champ est modifié

        if len(errors) > 0:
            return False, errors
        
        else:
            update_collection.collection_name=name
            update_collection.collection_collector_name=collector_name
            update_collection.collection_collector_firstname=collector_firstname
            update_collection.collection_collector_date=collector_date
            update_collection.collection_collector_bio=collector_bio
        # mise à jour de la collection

        try:
            db.session.add(update_collection)
	    # ajout des modifications à la BDD
            db.session.commit()
            return True, update_collection

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_collection(collection_id):
        """
        Fonction qui supprime une collection
        :param collection_id: id de la collection (int)
        :return: Booléen
        """
        delete_collection = Collection.query.get(collection_id)
	# récupération d'une collection dans la BDD

        try:
            db.session.delete(delete_collection)
	    # suppression de la collection de la BDD
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


class Work(db.Model):
    __tablename__ = "work"
    work_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    work_title = db.Column(db.Text, nullable=False)
    work_author = db.Column(db.Text)
    work_date = db.Column(db.Text)
    work_medium = db.Column(db.Text, db.ForeignKey("mediums.label"), nullable=False)
    work_dimensions = db.Column(db.Text)
    work_image_lien = db.Column(db.Text)
    work_collection_id = db.Column(db.Integer, db.ForeignKey('collection.collection_id'))
    authorships_work = db.relationship("Authorship_work", back_populates="work_work")

    def get_id(self):
        """
        Retourne l'id de l'objet actuellement utilisé
        :return: ID de l'oeuvre
        :rtype: int
        """
        return(self.work_id)

    @staticmethod
    def add_work(title, author, date, medium, dimensions, image, collection_id):
        """
        Fonction qui permet d'ajouter une nouvelle oeuvre dans la BDD
        :param title: titre de l'oeuvre (str)
        :param author: nom de l'auteur de l'oeuvre, c'est-à-dire de l'artiste (str)
        :param date: date de création de l'oeuvre (str)
        :param medium: "peinture", "sculpture", "gravure", "dessin", "objet d'art" ou "photographie"(str)
        :param dimensions: dimensions de l'oeuvre (str)
	:param image: lien de l'image (str)
	:param collection_id: id (int)
        :return: Booléen
        """
        errors = []
        if not title:
            errors.append("veuillez renseigner le titre de l'oeuvre")
        if not author:
            errors.append("veuillez renseigner l'autheur de l'oeuvre")
        if not date:
            errors.append("veuillez renseigner la date de création de l'oeuvre, si elle est inconnue, indiquer: n.d.")
        if not medium:
            errors.append("veuillez renseigner la technique de l'oeuvre")
        if not dimensions:
            errors.append("veuillez renseigner les dimensions de l'oeuvre, si elles sont inconnues indiquer: dimensions inconnues")
         
        if len(errors) > 0:
            return False, errors

        new_work = Work(
		work_title=title,
		work_author=author,
		work_date=date,
		work_medium=medium,
		work_dimensions=dimensions,
		work_image_lien=image,
		work_collection_id=collection_id)

        try:
        	db.session.add(new_work)
        	db.session.commit()
        	return True, new_work

        except Exception as erreur:
        	return False, [str(erreur)]

    @staticmethod
    def update_work (work_id, title, author, date, medium, dimensions, image):
        """ 
        Fonction qui permet de modifier les informations de la notice d'une oeuvre
        :param work_id: id de l'oeuvre (int)
        :param title: titre de l'oeuvre (str)
        :param author: nom de l'auteur de l'oeuvre, c'est-à-dire de l'artiste (str)
        :param date: date de création de l'oeuvre (str)
        :param medium: "peinture", "sculpture", "gravure", "dessin", "objet d'art" ou "photographie"(str)
        :param dimensions: dimensions de l'oeuvre (str)
	:param image: lien de l'image (str)
        :return: Booléen
        """
        errors=[]
        if not title:
            errors.append("veuillez renseigner le titre de l'oeuvre")
        if not author:
            errors.append("veuillez renseigner l'autheur de l'oeuvre")
        if not date:
            errors.append("veuillez renseigner la date de création de l'oeuvre, si elle est inconnue, indiquer: n.d.")
        if not medium:
            errors.append("veuillez renseigner la technique de l'oeuvre")
        if not dimensions:
            errors.append("veuillez renseigner les dimensions de l'oeuvre, si elles sont inconnues indiquer: dimensions inconnues")

        if len(errors) > 0:
            return False, errors

        update_work = Work.query.get(work_id)

        if update_work.work_title == title \
           and update_work.work_author == author \
           and update_work.work_date == date \
           and update_work.work_medium == medium \
           and update_work.work_dimensions == dimensions \
           and update_work.work_image_lien == image:
           errors.append("Aucune modification n'a été réalisée")

        if len(errors) > 0:
            return False, errors
        
        else:
            update_work.work_title=title
            update_work.work_author=author
            update_work.work_date=date
            update_work.work_medium=medium
            update_work.work_dimensions=dimensions
            update_work.work_image_lien=image

        try:
            db.session.add(update_work)
            db.session.commit()
            return True, update_work

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_work(work_id):
        """
        Fonction qui supprime la notice d'une oeuvre et ses données 
        :param work_id: id de l'oeuvre (int)
        :return: Booléen
        """
        delete_work = Work.query.get(work_id)

        try:
            db.session.delete(delete_work)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


class Mediums(db.Model):
	label = db.Column(db.Text, unique=True, nullable=False, primary_key=True)


class Authorship_collection(db.Model):
    __tablename__ = "authorship_collection"
    authorship_collection_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_collection_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    authorship_collection_collection_id = db.Column(db.Integer, db.ForeignKey("collection.collection_id"))
    user_collection = db.relationship("User", back_populates="author_collection")
    collection_collection = db.relationship("Collection", back_populates="authorships_collection")

     
class Authorship_work(db.Model):
    __tablename__ = "authorship_work"
    authorship_work_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_work_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    authorship_work_work_id = db.Column(db.Integer, db.ForeignKey("work.work_id"))
    user_work = db.relationship("User", back_populates="author_work")
    work_work = db.relationship("Work", back_populates="authorships_work")

