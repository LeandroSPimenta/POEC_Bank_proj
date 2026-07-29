from webapp import db
from webapp.main.classes.compte import Compte
import modules.bdd as bdd


class CompteEpargne(Compte):
    __tablename__ = "compte_epargne"
    __mapper_args__ = {"polymorphic_identity": "compte_epargne"}
    id = db.Column(db.Integer, db.ForeignKey("compte.id"), primary_key=True)
    num_compte = db.Column(db.Integer, index=True, unique=True)
    taux_remuneration = db.Column(db.Float, default=0.02)
    seuil_remuneration = db.Column(db.Integer, default=1000)

    # def __init__(self, data_compte, data_compte_epargne):
    #    super().__init__(data_compte)
    #    self.num_compte, self.rib , self.plafond, self.seuil_remuneration = data_compte_epargne
    #    self.__class__.cnx, self.cursor = None, None

    def virement_epargne(self, montant_virement, cnx=None):
        pass

    def crediter(self, data_compte, data_compte_epargne, somme_versee, cnx=None):
        pass

    def remunerer(self, data_compte, data_compte_epargne, cnx=None):
        pass
