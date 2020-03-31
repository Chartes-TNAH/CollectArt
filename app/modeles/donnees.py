from flask import url_for
import datetime

from .. app import db

class Collection(db.Model):
    __tablename__ = "collection"
    collection_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    collection_name = db.Column(db.Text, nullable=False)
    collection_collector_name = db.Column(db.Text, nullable=False)
    collection_collector_firstname = db.Column(db.Text)
    collection_collector_date = db.Column(db.Text)
    collection_collector_bio = db.Column(db.Text)
    authorships_collection = db.relationship("Authorship_collection", back_populates="collection_collection")
    work = db.relationship("Work", backref="collection")

    def get_id(self):
        """
        Retourne l'id de l'objet actuellement utilisé
        :returns: ID de l'oeuvre
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
        :param collector_date: date(s) du/de la collectionneur·euse (str)
        :param collector_bio: petite biographie du/de la collectionneur·euse (str)
        :return:
        """
        errors = []
        if not name:
            errors.append("veuillez renseigner le nom de la collection.")
        if not collector_name:
            errors.append("veuillez renseigner le nom de famille du/de la collectionneur·euse.")
        if not collector_firstname:
            errors.append("veuillez renseigner le prénom du/de la collectionneur·euse")
        if not collector_date:
            errors.append("veuillez renseigner les dates du/de la collectionneur·euse, si elles sont inconnues indiquer: dates inconnues")
        if not collector_bio:
            errors.append("veuillez renseigner une petite biographie du/de la collectionneur·euse")

        # Si on a au moins une erreur, cela retourne faux
        if len(errors) > 0:
            return False, errors

        # ajout d'une nouvelle entrée collection dans la table collection avec les champs correspondant aux paramètres du modèle
        new_collection = Collection(
            collection_name=name,
            collection_collector_name=collector_name,
            collection_collector_firstname=collector_firstname,
            collection_collector_date=collector_date,
            collection_collector_bio=collector_bio)

        try:
            db.session.add(new_collection)
            db.session.commit()
            # ajout de l'oeuvre à la BDD

            return True, new_collection

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def update_collection (collection_id, name, collector_name, collector_firstname, collector_date, collector_bio):
        """
        Fonction qui permet d'ajouter une nouvelle collection dans la BDD
        :param collection_id: id de la collection (int)
        :param name: nom de la collection (str)
        :param collector_name: nom de famille du/de la collectionneur·euse (str)
        :param collector_firstname: prénom du/de la collectionneur·euse (str)
        :param collector_date: date(s) du/de la collectionneur·euse (str)
        :param collector_bio: petite biographie du/de la collectionneur·euse (str)
        :return:
        """
        errors=[]
        if not name:
            errors.append("veuillez renseigner le nom de la collection.")
        if not collector_name:
            errors.append("veuillez renseigner le nom de famille du/de la collectionneur·euse.")
        if not collector_firstname:
            errors.append("veuillez renseigner le prénom du/de la collectionneur·euse")
        if not collector_date:
            errors.append("veuillez renseigner les dates du/de la collectionneur·euse, si elles sont inconnues indiquer: dates inconnues")
        if not collector_bio:
            errors.append("veuillez renseigner une petite biographie du/de la collectionneur·euse")

        # Si on a au moins une erreur, cela retourne faux
        if len(errors) > 0:
            return False, errors

        collection = Collection.query.get(collection_id)
        # récupération d'une collection dans la BDD

        if collection.collection_name == name \
            and collection.collection_collector_name == collector_name \
            and collection.collection_collector_firstname == collector_firstname \
            and collection.collection_collector_date == collector_date \
            and collection.collection_collector_bio == collector_bio:
            erreurs.append("Aucune modification n'a été réalisée")
        # vérification qu'au moins un champ est modifié
        
        else:
            collection.collection_name == name
            collection.collection_collector_name == collector_name
            collection.collection_collector_firstname == collector_firstname
            collection.collection_collector_date == collector_date
            collection.collection_collector_bio == collector_bio
        # mise à jour de la collection

        try:
            db.session.add(collection)
            db.session.commit()
        # ajout des modifications à la BDD
            return True, collection

        except Exception as erreur:
            return False, [str(erreur)]

 #  @staticmethod
 #   def delete_collection(collection_id):
        """
        Fonction qui supprime une collection
        :param work_id: id de la collection
        :type work_id: int
        :returns :
        """
 #      collection = Collection.query.get(collection_id)
        # récupération de la notice de l'oeuvre

 #   try:
 #      db.session.delete(collection)
 #       db.session.commit()
        # suppression de l'oeuvre de la BDD
 #       return True

 #   except Exception as failed:
 #       print(failed)
 #       return False


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
        :returns: ID de l'oeuvre
        :rtype: int
        """
        return(self.work_id)

    @staticmethod
    def add_work(title, author, date, medium, dimensions, image):
        """
        Fonction qui permet d'ajouter une nouvelle oeuvre dans la BDD
        :param title: titre de l'oeuvre (str)
        :param author: nom de l'auteur de l'oeuvre, c'est-à-dire de l'artiste (str)
        :param date: date de création de l'oeuvre (str)
        :param medium: 'peinture', 'sculpture', 'gravure', 'dessin', "objet d'art" ou 'photographie'(str)
        :param dimensions: dimensions de l'oeuvre (str)
        :return:
        """
        errors = []
        if not title:
            errors.append("veuillez renseigner le titre de l'oeuvre.")
        if not author:
            errors.append("veuillez renseigner l'autheur de l'oeuvre.")
        if not date:
            errors.append("veuillez renseigner la date de création de l'oeuvre, si elle est inconnue, indiquer: n.d.")
        if not medium:
            errors.append("veuillez renseigner la technique de l'oeuvre.")
        if not dimensions:
            errors.append("veuillez renseigner les dimensions de l'oeuvre, si elles sont inconnues indiquer: dimensions inconnues.")

        # Si on a au moins une erreur, cela retourne faux
        if len(errors) > 0:
            return False, errors

        # ajout d'une nouvelle entrée oeuvre dans la table work avec les champs correspondant aux paramètres du modèle
        new_work = Work(work_title=title,
        	          work_author=author,
        	          work_date=date,
        	          work_medium=medium,
        	          work_dimensions=dimensions,
                      work_image_lien=image)

        try:
        	db.session.add(new_work)
        	db.session(commit)
        	# ajout de l'oeuvre à la BDD

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
        :param medium: 'peinture', 'sculpture', 'gravure', 'dessin', "objet d'art" ou 'photographie'(str)
        :param dimensions: dimensions de l'oeuvre (str)
        :return: Tuple (booléen, liste/objet).
        """
        errors=[]
        if not title:
            errors.append("veuillez renseigner le titre de l'oeuvre.")
        if not author:
            errors.append("veuillez renseigner l'autheur de l'oeuvre.")
        if not date:
            errors.append("veuillez renseigner la date de création de l'oeuvre, si elle est inconnue, indiquer: n.d.")
        if not medium:
            errors.append("veuillez renseigner la technique de l'oeuvre.")
        if not dimensions:
            errors.append("veuillez renseigner les dimensions de l'oeuvre, si elles sont inconnues indiquer: dimensions inconnues.")

        # Si on a au moins une erreur, cela retourne faux
        if len(errors) > 0:
            return False, errors

        oeuvre = Work.query.get(work_id)
        # récupération d'une oeuvre dans la BDD

        if oeuvre.work_title == title \
           and oeuvre.work_author == author \
           and oeuvre.work_date == date \
           and oeuvre.work_medium == medium \
           and oeuvre.work_dimensions == dimensions \
           and oeuvre.work_image_lien == image:
           erreurs.append("Aucune modification n'a été réalisée")
        # vérification qu'au moins un champ est modifié
        
        else:
            oeuvre.work_title == title
            oeuvre.work_author == author
            oeuvre.work_date == date
            oeuvre.work_medium == medium
            oeuvre.work_dimensions == dimensions
            oeuvre.work_image_lien == image
        # mise à jour de l'oeuvre

        try:
            db.session.add(oeuvre)
            db.session.commit()
        # ajout des modifications à la BDD
            return True, oeuvre

        except Exception as erreur:
            return False, [str(erreur)]

#    @staticmethod
#    def delete_work(work_id):
        """
        Fonction qui supprime la notice d'une oeuvre
        :param work_id: id de l'oeuvre
        :type work_id: int
        :returns :
        """
#        oeuvre = Work.query.get(work_id)
        # récupération de la notice de l'oeuvre

#    try:
#        db.session.delete(oeuvre)
#        db.session.commit()
    # suppression de l'oeuvre de la BDD
#        return True
#    except Exception as failed:
#        print(failed)
#        return False


class Mediums(db.Model):
	label = db.Column(db.Text, unique=True, nullable=False, primary_key=True)


class Authorship_collection(db.Model):
    __tablename__ = "authorship_collection"
    authorship_collection_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_collection_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    authorship_collection_collection_id = db.Column(db.Integer, db.ForeignKey("collection.collection_id"))
    authorship_collection_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_collection = db.relationship("User", back_populates="author_collection")
    collection_collection = db.relationship("Collection", back_populates="authorships_collection")

        
class Authorship_work(db.Model):
    __tablename__ = "authorship_work"
    authorship_work_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_work_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    authorship_work_work_id = db.Column(db.Integer, db.ForeignKey("work.work_id"))
    authorship_collection_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_work = db.relationship("User", back_populates="author_work")
    work_work = db.relationship("Work", back_populates="authorships_work")

