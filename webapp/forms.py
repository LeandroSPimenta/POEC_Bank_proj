from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField("Utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    remember_me = BooleanField("Se rappeler de moi")
    submit = SubmitField("Me connecter")


class SignupForm(FlaskForm):
    username = StringField("Utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    password_bis = PasswordField(
        "Confirmation du mot de passe", validators=[DataRequired()]
    )
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("M'inscrire")


class CommentForm(FlaskForm):
    body = StringField("Text", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("Poster")
