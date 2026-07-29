from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import TextArea
from flask_babel import lazy_gettext as _l


class CommentForm(FlaskForm):
    body = StringField(_l("Text"), widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField(_l("Poster"))
