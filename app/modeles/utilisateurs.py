from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import or_

from .. app import db, login

class User(UserMixin, db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    author_collection = db.relationship("Authorship_collection", back_populates="user_collection")
    author_work = db.relationship("Authorship_work", back_populates="user_work")

    def get_id(self):
        return(self.user_id)

    @staticmethod
    def identification(login, motdepasse):
        """ 
        Identifie un utilisateur·rice. Si cela fonctionne, renvoie les données de l'utilisateur·rice.
        :param login: Login de l'utilisateur·rice
        :param motdepasse: Mot de passe envoyé par l'utilisateur·rice
        :returns: Si réussite, données de l'utilisateur·rice. Sinon None
        :rtype: User or None
        """
        user = User.query.filter(User.user_login == login).first()
        if user and check_password_hash(user.user_password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse):
        """ 
        Crée un compte utilisateur·rice. Retourne un tuple (booléen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur
        Sinon, elle renvoie True suivi de la donnée enregistrée
        :param login: Login de l'utilisateur·rice
        :param email: Email de l'utilisateur·rice
        :param nom: Nom de l'utilisateur·rice
        :param motdepasse: Mot de passe de l'utilisateur·rice (Minimum 6 caractères)
        :return: tuple
        """
        erreurs = []
        if not login:
            erreurs.append("Le login fourni est vide")
        if not email:
            erreurs.append("L'email fourni est vide")
        if not nom:
            erreurs.append("Le nom fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court")

        # On vérifie que personne n'a utilisé cet email ou ce login
        uniques = User.query.filter(or_
            (User.user_email == email, User.user_login == login)
        ).count()
        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà utilisés")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # On crée un utilisateur·rice
        user = User(
            user_nom=nom,
            user_login=login,
            user_email=email,
            user_password=generate_password_hash(motdepasse)
            )

        try:
            # On ajoute l'utilisateur·rice à la BDD
            db.session.add(user)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur·rice
            return True, user
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        """
        Retourne l'id de l'objet actuellement utilisé
        :returns: ID de l'utilisateur·rice
        :rtype: int
        """
        return(self.user_id)


@login.user_loader
def trouver_utilisateur_via_id(identifiant):
    return User.query.get(int(identifiant))	