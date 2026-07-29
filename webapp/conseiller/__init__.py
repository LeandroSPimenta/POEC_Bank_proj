from flask import Blueprint

bp = Blueprint("conseiller", __name__)

from webapp.conseiller import routes
