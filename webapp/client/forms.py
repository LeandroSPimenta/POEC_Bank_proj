from flask_wtf import FlaskForm
from flask_login import current_user
from flask_babel import lazy_gettext as _l

from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, AnyOf

from webapp.main.classes.compte import Compte


class CompteEpargneCreationForm(FlaskForm):
    titulaire_id = IntegerField(_l("titulaire"), validators=[DataRequired()])
    taux_remuneration = StringField(_l("Taux de rémuneration"), default=0.02)
    submit = SubmitField(_l("Creation"))


def compte_src_choices():
    user_accounts = current_user.comptes.all()
    choices = [(str(c.id), c.format_name()) for c in user_accounts]
    return choices


def compte_dest_choices():
    all_accounts = Compte.query.filter(Compte.titulaire_id != current_user.id).all()
    choices = [(str(c.id), c.format_name()) for c in all_accounts]
    return choices


class VirementForm(FlaskForm):
    # compte_src = IntegerField('Compte émetteur', validators=[DataRequired()])
    # compte_dest = IntegerField('Compte récepteur', validators=[DataRequired()])
    valeur = FloatField("Somme", validators=[DataRequired()])
    motif = StringField("Motif")
    submit = SubmitField("Effectuer le virement")
    compte_src = SelectField("Compte émetteur", default="")
    compte_dest = SelectField("Compte récepteur", default="")

    def __init__(self):
        super(VirementForm, self).__init__()
        compte_src_choix = compte_src_choices()
        compte_dest_choix = compte_dest_choices()
        self.compte_src.choices = compte_src_choix
        self.compte_src.validators = [AnyOf([c[0] for c in compte_src_choix])]
        self.compte_dest.choices = compte_dest_choix
        self.compte_dest.validators = [AnyOf([c[0] for c in compte_dest_choix])]
