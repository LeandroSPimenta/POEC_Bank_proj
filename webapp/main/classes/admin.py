import logging

from webapp import db
from webapp.main.classes.utilisateur import Utilisateur


class Admin(Utilisateur):

    # logging.basicConfig(filename='../log/admin_connexion.log', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

    __tablename__ = "admin"
    __mapper_args__ = {"polymorphic_identity": "admin"}
    id = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), primary_key=True)

    def afficher(self):
        return super().afficher()


if __name__ == "__main__":
    # cons = Conseiller(data_user, data_conseiller)
    # admin.agents.append(cons)
    # return cons
    admin = Admin()
