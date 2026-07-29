import mysql.connector
import configs.config

# from mysql.connector import Error
from configs.config import DATABASE


def connexion_bdd(user="root", password="", host="127.0.0.1", database=DATABASE):
    try:
        print("connexion")
        cnx = mysql.connector.connection.MySQLConnection(
            user=user, password=password, host=host, database=database
        )
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Il y a un problème avec votre user name ou password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("La base n’existe pas")
        else:
            print(err)
    else:
        print("je suis connecté à la bdd")
        cnx.autocommit = True  # commit automatiquement à chaque create|insert|update
        return cnx


def envoi_requete(cursor, requete, donnees=None):
    try:
        if not donnees:
            cursor.execute(requete)
        elif isinstance(donnees, tuple):
            cursor.execute(requete, donnees)
        elif isinstance(donnees, list) and all(
            isinstance(element, tuple) for element in donnees
        ):
            cursor.executemany(requete, donnees)
        else:
            print("format de données incompatible")
    except mysql.connector.errors.IntegrityError:
        print("Données déjà dans la bdd")
        raise


def fermeture(connexion, cursor):
    cursor.close()
    connexion.close()
