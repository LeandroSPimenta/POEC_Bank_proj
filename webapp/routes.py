import os
from flask import render_template, flash, redirect, url_for, escape, request
from werkzeug.security import generate_password_hash

# from modules import requete_bdd
from webapp import app
from webapp.forms import LoginForm, SignupForm, CommentForm
from flask_login import current_user, login_user, logout_user, login_required

# from webapp.models import User, Post
# from webapp.tests_models import select_all, inserer


@app.route("/")
@app.route("/index")
@app.endpoint("index")
# @login_required
def index():
    return render_template("index.html", title="Page d'accueil")


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Authentification", form=form)
