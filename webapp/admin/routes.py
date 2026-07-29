import time

from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash

from webapp import db
from webapp.admin import bp
from flask_login import current_user, login_user, logout_user
from webapp.main.classes.utilisateur import Utilisateur
from webapp.admin.forms import ConseillerCreationForm
from webapp.main.requetes import inserer
from webapp.auth.email import send_password_reset_email

from webapp.main.classes.conseiller import Conseiller


@bp.route("/creerConseiller", methods=["GET", "POST"])
@bp.endpoint("creerConseiller")
# @roles_required('admin')
def creerConseiller():
    form = ConseillerCreationForm()
    if form.validate_on_submit():
        if form.password.data == form.password_bis.data:
            data = {
                form.username.name: form.username.data,
                form.date_debut.name: form.date_debut.data,
                form.date_fin.name: form.date_fin.data,
                form.password.name: generate_password_hash(form.password.data),
            }
            print(data)
            u = Conseiller(**data)
            insertion = inserer(u)
            if insertion == -1:
                flash("l'utilisateur existe déjà !")
            elif not insertion:
                flash("Erreur dans la base de donnée !")
            else:
                flash("Un Conseiller a été Créé")
                return redirect(url_for("main.index"))
        else:
            form.password_bis.errors.append("Mot de passe non confirmé !")
    return render_template(
        "admin/creerConseiller.html",
        title="creation consieller",
        user=current_user,
        form=form,
    )
