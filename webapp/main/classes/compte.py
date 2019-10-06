from datetime import datetime

import modules.bdd as bdd
from webapp import db


class Compte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rib = db.Column(db.String(20), index=True, unique=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    solde = db.Column(db.Integer)
    titulaire_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    #def __init__(self, data_compte):
    #    self.rib, self.proprietaire, self.date_creation, self.solde, self.type = data_compte
    #    self.__class__.cnx, self.cursor = None, None

    def depot(self, somme, cnx=None):
        pass