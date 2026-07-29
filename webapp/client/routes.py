import time

from flask import render_template, flash, redirect, url_for, escape, request
from werkzeug.security import generate_password_hash

from webapp import db
from webapp.client import bp

from flask_login import current_user, login_user, logout_user, login_required
from webapp.main.classes.compte_courant import CompteCourant
from webapp.main.classes.compte_epargne import CompteEpargne
from webapp.main.classes.compte import Compte
from webapp.main.classes.operation import Operation
from webapp.client.forms import CompteEpargneCreationForm, VirementForm
from webapp.admin.forms import ConseillerCreationForm
from webapp.main.requetes import inserer
from webapp.auth.email import send_password_reset_email
from webapp.main.classes.conseiller import Conseiller
from flask_babel import _, lazy_gettext as _l


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
@bp.endpoint("index")
@login_required
def index():
    if current_user.is_authenticated and current_user.discriminator == "client":
        if "open_ce" in request.full_path:
            if len(current_user.comptes.all()) == 1 and request.args.get("open_ce"):
                compte = CompteEpargne(titulaire_id=current_user.id)
                insertion = inserer(compte)
                if insertion:
                    return redirect(url_for("client.compteEpargne"))
        return render_template(
            "client/index.html",
            user=current_user,
            title=_l("Espace Client"),
            nb_comptes=len(current_user.comptes.all()),
        )
    redirect(url_for("main.index"))


@bp.route("/compteCourant", methods=["GET"])
@bp.endpoint("compteCourant")
@login_required
def compteCourant():
    if current_user.is_authenticated and current_user.discriminator == "client":
        compte = current_user.comptes.filter_by(discriminator="compte_courant").first()
        operations = None

        if compte.operations.all() is None:
            flash(_("Aucune opération n'a été effectuée sur ce compte"))
        else:
            operations = (
                compte.operations.union_all(compte.virements)
                .order_by(Operation.done_at.desc())
                .all()
            )
        return render_template(
            "client/compteCourant.html",
            user=current_user,
            compte=compte,
            title=_l("Compte Courant"),
            operations=operations,
        )
    redirect(url_for("main.index"))


@bp.route("/compteEpargne", methods=["GET"])
@bp.endpoint("compteEpargne")
@login_required
def compteEpargne():
    if current_user.is_authenticated and current_user.discriminator == "client":
        compte = current_user.comptes.filter_by(discriminator="compte_epargne").first()
        operations = None
        if compte.operations.all() is None:
            flash(_l("Aucune opération n a été effectuée sur ce compte"))
        else:
            operations = (
                compte.operations.union_all(compte.virements)
                .order_by(Operation.done_at.desc())
                .all()
            )
        return render_template(
            "client/compteEpargne.html",
            user=current_user,
            compte=compte,
            title=_l("Compte Épargne"),
            operations=operations,
        )
    redirect(url_for("main.index"))


@bp.route("/creerCompteEpargne", methods=["GET", "POST"])
@bp.endpoint("creer_compte_epargne")
def creer_compte_epargne():
    if current_user.is_authenticated and current_user.discriminator == "client":
        compte = CompteEpargne.query.filter_by(titulaire=current_user).first()
        # return redirect(url_for('main.index'))
        form = CompteEpargneCreationForm()
        if form.validate_on_submit():
            data = {
                form.titulaire_id.name: form.titulaire_id.data,
                form.taux_remuneration.name: form.taux_remuneration.data,
            }
            compte_e = CompteEpargne(**data)
            insertion = inserer(compte_e)
            if insertion:
                return redirect(url_for("client.compteEpargne"))
            # afficher le solde du compte epargne
            # rémuneration d'un compte et verser la rémunération dans

        return render_template(
            "client/creerCompteEpargne.html",
            user=current_user,
            compte=compte,
            title=_l("Création Compte Épargne"),
            form=form,
        )

    redirect(url_for("main.index"))


@bp.route("/virement", methods=["GET", "POST"])
@bp.endpoint("virement")
def virement():
    if current_user.is_authenticated and current_user.discriminator == "client":
        form = VirementForm()
        user_accounts = current_user.comptes.all()
        all_accounts = [
            filter(lambda x: x.titulaire_id != current_user.id, Compte.query.all())
        ]
        if form:
            print(form.compte_src.data)
        if form.validate_on_submit():
            data = {
                form.compte_src.name: form.compte_src.data,
                form.compte_dest.name: form.compte_dest.data,
                form.valeur.name: form.valeur.data,
                form.motif.name: form.motif.data,
            }
            compte = Compte.query.get(data["compte_src"])
            compte_dest = Compte.query.get(data["compte_dest"])
            if not (
                compte_dest is not None
                and compte is not None
                and compte.titulaire_id == current_user.id
                and compte_dest.id != compte.id
                and data["valeur"]
            ):
                flash(_l("Conditions pour un virement non remplies"))
            else:
                try:
                    valeur = float(data["valeur"])
                except (ValueError, TypeError):
                    flash(_l("Conditions pour un virement non remplies"))
                    return redirect(url_for("client.index"))
                else:
                    valeur = abs(valeur)
                    solde_temp = compte.solde - valeur
                    if solde_temp < 0:
                        if compte.discriminator == "compte_courant":
                            if not compte.autorisation_decouvert:
                                flash(
                                    _l("vous n'êtes pas autorisé à passer en découvert")
                                )
                                return redirect(url_for("client.index"))
                            elif solde_temp < (
                                0 - (compte.entree_moyenne * compte.taux_decouvert)
                            ):
                                flash(
                                    _l(
                                        "l'opération dépasserait votre seuil de découvert"
                                    )
                                )
                                return redirect(url_for("client.index"))
                        else:
                            flash(
                                _l(
                                    "L'operation demandée passerait le compte en négatif"
                                )
                            )
                            return redirect(url_for("client.index"))
                    compte.solde = solde_temp
                    compte_dest.solde += valeur
                    data_operation = {
                        "compte_id": compte.id,
                        "compte_bis_id": compte_dest.id,
                        "valeur": valeur,
                        "type_operation": "virement",
                    }
                    if data["motif"]:
                        data_operation.update({"label": data["motif"]})
                    operation = Operation(**data_operation)
                    # insertion = inserer(operation)
                    db.session.add(operation)
                    db.session.commit()
                    flash(_l("Virement effectué !"))
        return render_template(
            "client/virement.html",
            user=current_user,
            title=_l("Effectuer un Virement"),
            user_accounts=user_accounts,
            all_accounts=all_accounts,
            form=form,
        )
    redirect(url_for("main.index"))
