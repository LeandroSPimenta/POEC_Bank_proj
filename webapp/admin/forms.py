from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    DateTimeField,
    DateField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from flask_babel import lazy_gettext as _l


class ConseillerCreationForm(FlaskForm):
    username = StringField(_l("Utilisateur"), validators=[DataRequired()])
    password = PasswordField(_l("Mot de passe"), validators=[DataRequired()])
    password_bis = PasswordField(
        _l("Confirmation du mot de passe"), validators=[DataRequired()]
    )
    date_debut = DateField(_l("Date d'entrée"), format="%d-%m-%Y")
    date_fin = DateField(
        _l("Date de sortie"), format="%d-%m-%Y", validators=[Optional()]
    )
    submit = SubmitField(_l("Création"))
