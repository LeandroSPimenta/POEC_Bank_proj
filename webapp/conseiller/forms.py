from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    DateTimeField,
    IntegerField,
)
from wtforms.validators import DataRequired, Email, EqualTo
from flask_babel import lazy_gettext as _l


class AcceptForm(FlaskForm):
    value = IntegerField("id", validators=[DataRequired()])
    action = StringField("action", validators=[DataRequired()])


class ClientCreationForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()])
    password = PasswordField(_l("Mot de passe"), validators=[DataRequired()])
    password_bis = PasswordField(
        _l("Confirmation du mot de passe"), validators=[DataRequired()]
    )
    date_debut = DateTimeField(_l("Date d'entrée"), validators=[DataRequired()])
    date_fin = DateTimeField(_l("Date de sortie"))
    submit = SubmitField(_l("Création"))
