from datetime import datetime

from webapp import db
from webapp.main.models import *
from werkzeug.security import generate_password_hash as gph
from webapp.main.requetes import inserer, delete_database_data

data_cli = {
    "username": "Baltran",
    "password": "elpoto",
    "email": "daubie_vic@msn.com",
    "conseiller_id": 2,
    "adresse": "10, rue de la liberté",
    "tel": "0123456789",
    "prenom": "Victor",
    "nom": "Daubié",
}
data_cli_2 = {
    "username": "Sadia",
    "password": "Sadia",
    "email": "sadia_ing@msn.com",
    "conseiller_id": 2,
    "adresse": "12, rue de la liberté",
    "tel": "0123786589",
    "prenom": "Sadia",
    "nom": "Anon",
}
data_cli_3 = {
    "username": "Moez",
    "password": "Moez",
    "email": "moez_form@msn.com",
    "conseiller_id": 3,
    "adresse": "9, rue de la liberté",
    "tel": "0123586589",
    "prenom": "Moez",
    "nom": "Ben Haj Hmida",
}
data_admin = {"username": "admin", "password": "admin", "email": "admin@gestibank.fr"}

data_conseiller = {
    "username": "Bob",
    "password": "bob",
    "email": "bob@bip.fr",
    "prenom": "Jean",
    "nom": "Durt",
}
data_conseiller_2 = {
    "username": "MadMax",
    "password": "wild",
    "email": "max@bip.fr",
    "prenom": "Max",
    "nom": "Luret",
}
data_conseiller_3 = {
    "username": "Pippo",
    "password": "pippo",
    "email": "pip@bip.fr",
    "prenom": "Fred",
    "nom": "Qwant",
}

data_demande = {
    "username": "Bernie",
    "email": "bern@bip.fr",
    "adresse": "12, rue de la liberté",
    "tel": "0147852369",
    "prenom": "Bernard",
    "nom": "Ledoy",
}
data_demande2 = {
    "username": "Jean",
    "email": "abd@bip.fr",
    "tel": "0145879632",
    "adresse": "12, rue de la liberté",
    "prenom": "Jean",
    "nom": "Friche",
}

data_compte_courant = {"solde": "2600", "titulaire_id": "5"}
data_compte_courant_2 = {"solde": "1300", "titulaire_id": "6"}
data_compte_courant_3 = {"solde": "20000", "titulaire_id": "7"}
data_compte_epargne = {"solde": "12600", "titulaire_id": "5"}

data_virement = {
    "valeur": 200,
    "compte_id": "2",
    "compte_bis_id": "1",
    "type_operation": "virement",
    "done_at": datetime(2015, 6, 5, 8, 10, 10, 10),
}
data_virement_2 = {
    "valeur": 200,
    "compte_id": "1",
    "compte_bis_id": "2",
    "type_operation": "virement",
}
data_depot = {"valeur": 50, "compte_id": "2", "type_operation": "depot"}

delete_database_data(
    Client, Utilisateur, Demande, Conseiller, CompteCourant, CompteEpargne, Operation
)
populate = []
populate.append(Admin(**data_admin))
populate.append(Conseiller(**data_conseiller))
populate.append(Conseiller(**data_conseiller_2))
populate.append(Conseiller(**data_conseiller_3))
populate.append(Client(**data_cli))
populate.append(Client(**data_cli_2))
populate.append(Client(**data_cli_3))
populate.append(Demande(**data_demande))
populate.append(Demande(**data_demande2))
populate.append(Operation(**data_virement))
populate.append(Operation(**data_virement_2))
populate.append(Operation(**data_depot))
populate.append(CompteCourant(**data_compte_courant))
populate.append(CompteCourant(**data_compte_courant_2))
populate.append(CompteEpargne(**data_compte_epargne))

for obj in populate:
    inserer(obj)

client = Client.query.get(5)

print(client.username)
compte = Compte.query.get(2)
operations = compte.operations.union_all(compte.virements)

for op in operations:
    print(op.afficher())
