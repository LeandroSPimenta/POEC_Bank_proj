import unittest
from modules.bdd import connexion_bdd, envoi_requete, fermeture
from configs.config import DATABASE_TEST
from webapp.main.classes.utilisateur import Utilisateur
from webapp.main.classes.admin import Admin


class TestUtilisateur(unittest.TestCase):
    connexion = None
    cursor = None

    @classmethod
    def setUpClass(cls):
        TestUtilisateur.connexion = connexion_bdd(database=DATABASE_TEST)
        TestUtilisateur.cursor = TestUtilisateur.connexion.cursor()

    def setUp(self) -> None:
        req = """
        CREATE TABLE `utilisateur` (
            `username` varchar(20) PRIMARY KEY NOT NULL,
            `password` LONGTEXT DEFAULT NULL,
            `nom` varchar(30) DEFAULT NULL,
            `prenom` varchar(20) DEFAULT NULL,
            `email` varchar(50) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        envoi_requete(TestUtilisateur.cursor, req)
        req = """
        INSERT INTO `utilisateur` (`username`,`password`,`nom`, `prenom`, `email`) VALUES
('admin', password('admin'), 'Smith', 'John', 'john.smith@domain.com');"""
        envoi_requete(TestUtilisateur.cursor, req)

    def tearDown(self) -> None:
        req = "DROP TABLE utilisateur"
        envoi_requete(TestUtilisateur.cursor, req)

    @classmethod
    def tearDownClass(cls):
        fermeture(TestUtilisateur.connexion, TestUtilisateur.cursor)

    def test_connexion_utilisateur(self):
        donnees_test = (
            "admin",
            "*4ACFE3202A5FF5CF467898FC58AAB1D615029441",
            "Smith",
            "John",
            "john.smith@domain.com",
        )
        user = Utilisateur()
        result = user.connexion("admin", "admin", TestUtilisateur.connexion)
        # self.assertTupleEqual(result, donnees_test)
        self.assertIsInstance(result, Admin)
