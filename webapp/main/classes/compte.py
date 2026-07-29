from datetime import datetime

import modules.bdd as bdd
from webapp import db


class Compte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rib = db.Column(db.String(20), index=True, unique=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    solde = db.Column(db.Float, default=0)
    titulaire_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    discriminator = db.Column("type", db.String(50))
    __mapper_args__ = {"polymorphic_on": discriminator}
    operations = db.relationship(
        "Operation",
        backref="compte_src",
        lazy="dynamic",
        foreign_keys="Operation.compte_id",
    )
    virements = db.relationship(
        "Operation",
        backref="compte_bis",
        lazy="dynamic",
        foreign_keys="Operation.compte_bis_id",
    )
    # modifier virements vers virements_recus

    # def __init__(self, data_compte):
    #    self.rib, self.proprietaire, self.date_creation, self.solde, self.type = data_compte
    #    self.__class__.cnx, self.cursor = None, None

    def depot(self, somme, cnx=None):
        pass

    def __repr__(self):
        return "<Compte {}>".format(self.id)

    def format_name(self):
        name = str(self.titulaire.nom) + " " + str(self.titulaire.prenom)
        if self.discriminator == "compte_courant":
            name += " (Compte Courant)"
        else:
            name += " (Compte Épargne)"
        return name
