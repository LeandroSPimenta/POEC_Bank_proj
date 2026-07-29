import os

from flask import render_template, flash, url_for, escape, current_app

# from webapp import app
from webapp.main import bp
from webapp.main.forms import CommentForm
from flask_login import current_user, login_required
from webapp.main.classes.utilisateur import Utilisateur
from webapp.main.classes.demande import Demande
from webapp.main.requetes import select_all


@bp.route("/")
@bp.route("/index")
# @bp.endpoint('index')
# @login_required
def index():
    user = {"username": "Victor"}
    posts = [
        {"author": {"username": "Josh"}, "body": "Pas sympa le git avec PyCharm"},
        {
            "author": {"username": "Melanie"},
            "body": "Mais non, il suffit de bien le configurer",
        },
    ]
    bureau = os.listdir(os.path.abspath(os.path.dirname(__file__)))
    users = select_all(Utilisateur)
    demandes = select_all(Demande)
    return render_template(
        "main/index.html",
        # title="Page d'accueil",
        user=current_user,
        posts=posts,
        desktop=bureau,
        users=users,
        demandes=demandes,
        participants=[],
    )


@bp.route("/user/<username>")
@bp.endpoint("profile")
def profile(username):
    return "{}'s profile".format(escape(username))


if __name__ == "__main__":
    with bp.test_demande_context():
        print(url_for("main.index"))
        print(url_for("auth.login"))
