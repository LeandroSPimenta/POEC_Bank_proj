import base64
import logging

# import mysql.connector
import os
import re

from datetime import datetime, timedelta
from time import time
import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

# from modules.bdd import connexion_bdd, envoi_requete, fermeture
from configs.config import DATABASE
from webapp import db, login

logging.basicConfig(
    filename="connexion.log",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)
# logging.config.fileConfig(fname='../configs/log.conf', disable_existing_loggers=False)
# Récupère le logger spécifié dans le fichier
# logger = logging.getLogger(__name__)

app = current_app


class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    nom = db.Column(db.String(40), index=True, unique=False)
    prenom = db.Column(db.String(40), index=True, unique=False)
    email = db.Column(db.String(40), index=True, unique=True)
    _password = db.Column("password", db.String(100))
    discriminator = db.Column("type", db.String(50))
    __mapper_args__ = {"polymorphic_on": discriminator}

    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    @hybrid_property
    def password(self):
        """Return the hashed user password."""
        return self._password

    @password.setter
    def password(self, password):
        """Salt/Hash and save the user's new password."""
        self._password = generate_password_hash(password)

    @password.getter
    def password(self):
        """Return the hashed user password."""
        return self._password

    def __repr__(self):
        return "<Utilisateur {}>".format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = password

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
                "reset_password"
            ]
        except:
            return
        return Utilisateur.query.get(id)

    @staticmethod
    def get_exp_token(token):
        try:
            exp = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
                "exp"
            ]
        except:
            return
        return exp

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Utilisateur.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def afficher(self):
        return {
            "id": self.id,
            "username": self.username,
            "Nom": self.nom,
            "Prénom": self.prenom,
            "e-mail": self.email,
            # 'password' : self.password,
            "discriminator": self.discriminator,
        }

    def data_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "discriminator": self.discriminator,
        }


@login.user_loader
def load_user(id):
    return Utilisateur.query.get(int(id))
