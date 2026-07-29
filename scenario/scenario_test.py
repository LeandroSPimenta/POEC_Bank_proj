from webapp import db
from datetime import datetime
from webapp.main.models import *
from werkzeug.security import generate_password_hash as gph
from webapp.main.requetes import inserer, delete_database_data

data_cli = {
    "username": "Baltran",
    "password": "elpoto",
    "email": "daubie_vic@msn.com",
    "adresse": "10, rue de la liberté",
    "tel": "0123456789",
}

data_cli_2 = {
    "username": "Sadia",
    "password": "Sadia",
    "email": "sadia_ing@msn.com",
    "adresse": "12, rue de la liberté",
    "tel": "0123786589",
}

data_cli_3 = {
    "username": "Moez",
    "password": "Moez",
    "email": "moez_form@msn.com",
    "adresse": "9, rue de la liberté",
    "tel": "0123586589",
}

data_admin = {"username": "admin", "password": "admin", "email": "admin@gestibank.fr"}

data_conseiller = {"username": "Bob", "password": "bob", "email": "bob@bip.fr"}

data_demande = {
    "username": "Bernard",
    "password": "bernard",
    "email": "bern@bip.fr",
    "tel": "0147852369",
}
data_demande2 = {
    "username": "Jean",
    "password": "jean",
    "email": "abd@bip.fr",
    "tel": "0145879632",
}

data_compte_courant_1 = {
    "solde": "2600",
    "titulaire_id": "2",
    "autorisation_decouvert": False,
}
data_compte_courant_2 = {
    "solde": "1300",
    "titulaire_id": "3",
    "autorisation_decouvert": True,
}
data_compte_courant_3 = {
    "solde": "12000",
    "titulaire_id": "4",
    "autorisation_decouvert": True,
}

data_compte_epargne_1 = {"solde": "12600", "titulaire_id": "2"}


data_virement = {
    "valeur": 200,
    "compte_id": "2",
    "compte_bis_id": "1",
    "type_operation": "virement",
    "done_at": datetime(2015, 6, 5, 8, 10, 10, 10),
}
data_depot = {"valeur": 50, "compte_id": "2", "type_operation": "depot"}


delete_database_data(
    Client, Utilisateur, Demande, Conseiller, CompteCourant, CompteEpargne, Operation
)
populate = []
populate.append(Admin(**data_admin))
populate.append(Client(**data_cli))
populate.append(Client(**data_cli_2))
populate.append(Client(**data_cli_3))
populate.append(Conseiller(**data_conseiller))
populate.append(Demande(**data_demande))
populate.append(Demande(**data_demande2))
populate.append(Operation(**data_virement))
populate.append(Operation(**data_depot))
populate.append(CompteCourant(**data_compte_courant_1))
populate.append(CompteCourant(**data_compte_courant_2))
populate.append(CompteCourant(**data_compte_courant_3))
populate.append(CompteEpargne(**data_compte_epargne_1))


for obj in populate:
    inserer(obj)


client = Client.query.get(2)

print(client.username)
