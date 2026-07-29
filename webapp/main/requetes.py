from sqlalchemy import exc
from webapp.main.classes.utilisateur import db


def inserer(objet):
    db.session.add(objet)
    try:
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        print(e)
        return -1
    except exc.SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return None
    return objet


def select_all(classe):
    return classe.query.all()


def delete_database_data(*args):
    for table in args:
        for elem in select_all(table):
            db.session.delete(elem)
    db.session.commit()
