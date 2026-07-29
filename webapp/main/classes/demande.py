from webapp import db

# To convert the binary to pdf import:
import os, base64

# To convert back:
from io import BytesIO
from flask import send_file
from webapp.main.classes.utilisateur import Utilisateur


class Demande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), index=True, unique=False)
    prenom = db.Column(db.String(40), index=True, unique=False)
    email = db.Column(db.String(40), index=True, unique=True)
    username = db.Column(db.String(40), index=True, unique=True)
    password = db.Column(db.String(100))
    adresse = db.Column(db.String(100), index=False, unique=False, default="")
    tel = db.Column(db.String(20), unique=False, default="")
    revenu_mensuel = db.Column(db.Integer, index=False, default=0)
    # """Manquent (?) :
    # -> nombre d’enfants
    # -> situation matrimoniale
    # """
    piece_id = db.Column(db.LargeBinary, default=None)
    just_salaire = db.Column(db.LargeBinary, default=None)
    just_domicile = db.Column(db.LargeBinary, default=None)
    conseiller_id = db.Column(db.Integer, db.ForeignKey("conseiller.id"))

    def accepter(self):
        pass

    def afficher(self):
        return {
            "id": self.id,
            # 'username' : self.username,
            "Nom": self.nom,
            "Prénom": self.prenom,
            "e-mail": self.email,
            "Téléphone": self.tel,
            "Adresse": self.adresse,
            "Revenu mensuel": self.revenu_mensuel,
        }

    def data_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "tel": self.tel,
            "adresse": self.adresse,
            "revenu_mensuel": self.revenu_mensuel,
            "piece_id": self.piece_id,
            "just_salaire": self.just_salaire,
            "just_domicile": self.just_domicile,
            "conseiller_id": self.conseiller_id,
        }
