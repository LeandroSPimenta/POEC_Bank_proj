from flask import Flask, request, session, current_app, url_for

from flask_babel import Babel
from flask_admin import Admin

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
mail = Mail()
babel = Babel()
admin_flask = Admin(name="Administration")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    # bootstrap.init_app(app)
    # moment.init_app(app)
    babel.init_app(app)
    admin_flask.init_app(app)

    # admin = Admin(app, name='Administration', index_view=views.MyAdminIndexView())

    # ... no changes to blueprint registration
    from webapp.auth import bp as auth_bp
    from webapp.main import bp as main_bp
    from webapp.admin import bp as admin_bp

    from webapp.client import bp as client_pb
    from webapp.api import bp as api_bp

    from webapp.conseiller import bp as conseiller_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_pb, url_prefix="/client")
    app.register_blueprint(conseiller_bp, url_prefix="/conseiller")

    app.register_blueprint(api_bp, url_prefix="/api")

    if not app.debug and not app.testing:
        # ... no changes to logging setup
        pass
    with app.app_context():
        # admin_flask.endpoint = 'bp_admin'
        admin_flask.index_view = views.MyAdminIndexView()
        admin_flask.template_mode = "bootstrap3"
        admin_flask.add_view(
            views.DemandeModelView(models.Demande, db.session, endpoint="demande_")
        )
        admin_flask.add_view(
            views.ConseillerModelView(
                models.Conseiller, db.session, endpoint="conseiller_"
            )
        )
        admin_flask.add_link(
            views.HomeMenuLink(name="Retour au site", category="", url="/index")
        )
        admin_flask.add_link(
            views.LogoutMenuLink(name="Logout", category="", url="/auth/logout")
        )

    app.__setattr__("allowed_file", allowed_file)

    return app


from webapp.main import models, filters
from webapp.admin import views


@babel.localeselector
def get_locale():
    if request.args.get("lang") in current_app.config["LANGUAGES"]:
        session["lang"] = request.args.get("lang")
    local_language = session.get(
        "lang", request.accept_languages.best_match(current_app.config["LANGUAGES"])
    )
    return local_language
