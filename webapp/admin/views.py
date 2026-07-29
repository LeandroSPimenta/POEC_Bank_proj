from flask import url_for, request
from flask_admin import AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from flask_login import current_user
from werkzeug.utils import redirect

from webapp.main.classes.conseiller import Conseiller
from webapp.main.classes.demande import Demande


class GestiBankModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.discriminator == "admin"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login", next=request.url))


class DemandeModelView(GestiBankModelView):
    can_create = False
    can_edit = False
    can_delete = False
    form_columns = ["mon_conseiller"]
    column_exclude_list = ("password", "piece_id", "just_salaire", "just_domicile")
    column_editable_list = ("mon_conseiller",)
    column_sortable_list = (("mon_conseiller", "mon_conseiller.nom"),)
    can_view_details = True


class ConseillerModelView(GestiBankModelView):
    can_edit = False
    column_exclude_list = ("discriminator", "_password", "token", "token_expiration")
    form_columns = [
        "username",
        "password",
        "nom",
        "prenom",
        "email",
        "date_debut",
        "date_fin",
    ]
    column_editable_list = (
        "username",
        "nom",
        "prenom",
        "email",
        "date_debut",
        "date_fin",
    )
    can_view_details = True


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.discriminator == "admin"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login", next=request.url))


class HomeMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated
