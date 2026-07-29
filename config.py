import os

from sqlalchemy.pool import SingletonThreadPool

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "ma_cle_secrete"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "gestibank.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTION = {"poolclass": SingletonThreadPool}
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    LANGUAGES = ["fr", "en"]
    ALLOWED_EXTENSIONS = set(["pdf", "png", "jpg", "jpeg"])
    # UPLOAD_FOLDER = '/Desktop'
