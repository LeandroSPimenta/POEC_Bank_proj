import time

from flask import render_template, flash, redirect, url_for, request, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from webapp import db
from webapp.auth import bp
from webapp.auth.forms import *
from flask_login import current_user, login_user, logout_user
from flask_babel import lazy_gettext as _l
from webapp.main.classes.utilisateur import Utilisateur
from webapp.main.classes.client import Client
from webapp.main.classes.conseiller import Conseiller
from webapp.main.classes.demande import Demande
from webapp.main.requetes import inserer
from webapp.auth.email import send_password_reset_email


def redirect_by_role(user):
    if user.discriminator == "client":
        return redirect(url_for("client.index"))
    elif user.discriminator == "conseiller":
        return redirect(url_for("conseiller.gerer_demandes"))
    else:
        return redirect(url_for("admin.index"))


@bp.route("/login", methods=["GET", "POST"])
@bp.endpoint("login")
def login():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_l("Login ou mot de passe invalide"))
            return redirect(url_for("auth.login"))

        if user.discriminator == "client":
            user = Client.query.get(user.id)
        elif user.discriminator == "conseiller":
            user = Conseiller.query.get(user.id)
        login_user(user, remember=form.remember_me.data)
        return redirect_by_role(user)
        # return redirect(url_for('main.index'))
    return render_template("auth/login.html", title=_l("Authentification"), form=form)


@bp.route("/logout")
@bp.endpoint("logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/signup", methods=["GET", "POST"])
@bp.endpoint("signup")
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        # fichier = request.files['inputFile']
        data = {
            form.prenom.name: form.prenom.data,
            form.nom.name: form.nom.data,
            form.username.name: form.username.data,
            # form.password.name: generate_password_hash(form.password.data),
            form.email.name: form.email.data,
            form.adresse.name: form.adresse.data,
            form.tel.name: form.tel.data,
            form.revenu_mensuel.name: form.revenu_mensuel.data,
            # form.piece_id.name: fichier.read()
        }
        # Création d'un objet demande

        demande = Demande(**data)

        # Uploading Files to a Database in Flask
        # https://www.youtube.com/watch?v=TLgVEBuQURA
        piece_id = request.files["pieceIdUp"]
        just_salaire = request.files["justSalaireUp"]
        just_domicile = request.files["justDomicileUp"]
        demande.piece_id = piece_id.read()
        demande.just_salaire = just_salaire.read()
        demande.just_domicile = just_domicile.read()

        insertion = inserer(demande)

        if insertion == -1:
            flash(_l("Demande déjà effectuée."))
        elif not insertion:
            flash(_l("Erreur dans la base de données."))
        else:
            # return render_template('auth/signup_confirmation.html', title='Confirmation')
            return redirect(url_for("auth.signup_confirmation"))
            # return render_template('auth/upload.html', title='Upload', form=form)
            # f = request.files['inputFile']
            # if form_data.validate_on_submit()
            #     db.session.add(form_data)
            #     db.session.commit()
            #     return render_template('auth/signup_confirmation.html', title='Confirmation')
    return render_template("auth/signup.html", title="Inscription", form=form)


@bp.route("/signup_confirmation", methods=["GET", "POST"])
@bp.endpoint("signup_confirmation")
def signup_confirmation():
    return render_template(
        "auth/signup_confirmation.html", title=_l("Confirmation de demande")
    )


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_l("Consultez votre e-mail et suivez les instructions"))
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html", form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = Utilisateur.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_l("Votre mot de passe a été réinitialisé."))
        return redirect(url_for("auth.login"))
    exp = int(Utilisateur.get_exp_token(token) - time.time())
    return render_template("auth/reset_password.html", form=form, exp=exp)


# @bp.route('/first_password/<token>', methods=['GET', 'POST'])
# def first_password(token):
#     return redirect('auth/first_password.html')
