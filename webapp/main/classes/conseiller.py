from webapp import db
from webapp.main.classes.utilisateur import Utilisateur
from webapp.main.classes.demande import Demande
import datetime


class Conseiller(Utilisateur):
    # __tablename__ = 'conseiller'
    __mapper_args__ = {"polymorphic_identity": "conseiller"}
    id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), primary_key=True)
    date_debut = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    date_fin = db.Column(db.DateTime, index=True, default=None)
    demande = db.relationship(
        "Demande",
        backref="mon_conseiller",
        lazy="dynamic",
        foreign_keys="Demande.conseiller_id",
    )
    clients = db.relationship(
        "Client",
        backref="mon_conseiller",
        lazy="dynamic",
        foreign_keys="Client.conseiller_id",
    )

    def __repr__(self):
        return "<Conseiller {} {}>".format(self.nom, self.prenom)

    @classmethod
    def creer(cls, data_user, data_conseiller, role, cnx=None):
        pass

    def modifier(self, mle_agent, date_sortie, cnx=None):
        pass

    # def modifier(self, mle_agent, cnx=None):
    #    pass

    def supprimmer(self, cnx=None):
        pass


if __name__ == "__main__":
    pass
    # INSERT INTO `utilisa  teur` (`login`,`password`,`nom`, `prenom`, `email`) VALUES
    # ('ag1dupont', 'hhshdzyyds', 'dupont', 'jean' , 'pdupont@gmail.com');

    # cons = Conseiller((1, 'ag1dupont', '2000-12-04', None), ('ag1dupont', '2DF57C81EFE267B70AED6F85772E438ECAEE90A2', 'dupont', 'jean', 'pdupont@gmail.com'))
    # cons.modifier(1, '2018-05-20')
