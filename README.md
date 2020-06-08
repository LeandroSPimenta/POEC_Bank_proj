# POEC_Bank_proj


## Descriptif 

Un outil de gestion bancaire bilingue avec 4 profils d'utilisateur :
- Admin
- Client
- Conseiller
- Anonyme (sans compte ou non connecté)

L'anonyme peut :
- convertir des devises
- demander la création d'un compte (en fournissant des pièces justificatives en pdf et avec la réception d'un e-mail de confirmation)

Le client peut, dans son espace personalisé :
- Consulter ses soldes
- Recevoir et réaliser des virements
- Retirer de l'argent

L'administrateur peut :
- créer des comptes "conseiller" via un formulaire
- supprimer des comptes "conseiller"
- attribuer des demandes de création de compte à un conseiller

Le conseiller peut :
- visualiser les demandes de création de compte
- afficher les pièces justificatives
- accepter ou refuser des demandes de création de compte
- accéder aux informations des clients qui lui ont été attribués automatiquements lors de l'acceptation d'une demande de création de compte

Ce projet a été réalisé par Leandro Silva Pimenta, Sadia Ingrachen et Victor Daubié en 2 sprints, 10 jours au total, à la fin d'une formation de 3 mois sur le développement en langage Python à la société Global Knowledge.


### Installation:

Avec Python3 installé, commencer par créer un environnement virtuel. La procédure est expliquée ici :
https://docs.python.org/fr/3/library/venv.html

Ensuite, dans l'environnement virtuel, installé les dépendances :
`pip install -r requirements.txt`

Si vous lancez l'application pour la première fois, initialisez la base de données :
```
flask db init
flask db migrate -m "first commit"
flask db upgrade
```

Pour lancer l'application :
```
flask run
```
