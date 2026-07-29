from webapp import create_app, db, cli, mail
from webapp.main.models import *
from flask_mail import Message
from werkzeug.security import generate_password_hash as gph

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": Utilisateur,
        "Conseiller": Conseiller,
        "Client": Client,
        "Demande": Demande,
        "gph": gph,
        "Message": Message,
        "mail": mail,
        "Compte": Compte,
        "CompteCourant": CompteCourant,
        "CompteEpargne": CompteEpargne,
        "Operation": Operation,
    }
