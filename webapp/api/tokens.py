from flask import jsonify, g
from webapp import db
from webapp.api import bp
from webapp.api.auth import basic_auth, token_auth


@bp.route("/tokens", methods=["POST"])
@basic_auth.login_required
def get_token():
    """
    Obtenir un token d'accès à l'api
    test httpie:
    http --auth <username>:<password> POST http://localhost:5000/api/tokens
    :return: un token sous json
    """
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({"token": token})


@bp.route("/tokens", methods=["DELETE"])
@token_auth.login_required
def revoke_token():
    """
    test httpie:
    http DELETE http://localhost:5000/api/tokens \
    Authorization:"Bearer pC1Nu9wwyNt8VCj1trWilFdFI276AcbS"
    :return:
    """
    g.current_user.revoke_token()
    db.session.commit()
    return "", 204
