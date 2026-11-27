
# Kart-Engine v2.3

import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from constants import GameState
from controller.game_controller import GameController
from model.game_model import GameModel


class TestTwoPlayers(unittest.TestCase):
    """
    Vérifie le fonctionnement des deux voitures.

    Chaque joueur doit posséder sa propre voiture
    et utiliser ses propres commandes.
    """

    def test_deux_voitures_au_depart(self):
        """
        Vérifie que le circuit crée deux voitures
        indépendantes à des positions différentes.
        """
        model = GameModel()
        model.load_circuit()

        self.assertIsNotNone(model.car)
        self.assertIsNotNone(model.car2)

        # Les deux joueurs ne partagent pas le même objet.
        self.assertIsNot(model.car, model.car2)

        # Les voitures ne commencent pas au même endroit.
        position1 = (model.car.x, model.car.y)
        position2 = (model.car2.x, model.car2.y)

        self.assertNotEqual(position1, position2)

    def test_mouvement_independant(self):
        """
        Vérifie que le déplacement du joueur 1
        ne déplace pas la voiture du joueur 2.
        """
        model = GameModel()
        model.load_circuit()
        model.state = GameState.RACING

        position1 = (model.car.x, model.car.y)
        position2 = (model.car2.x, model.car2.y)

        # Seul le joueur 1 accélère.
        model.car.accelerate()

        # Mise à jour des deux voitures.
        model.update()

        # La première voiture avance.
        self.assertNotEqual(
            (model.car.x, model.car.y),
            position1
        )

        # La deuxième voiture reste immobile.
        self.assertEqual(
            (model.car2.x, model.car2.y),
            position2
        )

    def test_commandes_separees(self):
        """
        Vérifie que le contrôleur transmet
        les commandes à la bonne voiture.
        """
        voiture1 = Mock()
        voiture2 = Mock()

        # Modèle simulé pour tester le contrôleur.
        modele = SimpleNamespace(
            state=GameState.RACING,
            car=voiture1,
            car2=voiture2,
            update=Mock()
        )

        # Le joueur 1 accélère.
        commandes1 = {
            "accelerate": True,
            "reverse": False,
            "steer_left": False,
            "steer_right": False,
            "use_item": False
        }

        # Le joueur 2 tourne à droite.
        commandes2 = {
            "accelerate": False,
            "reverse": False,
            "steer_left": False,
            "steer_right": True,
            "use_item": False
        }

        # Crée un contrôleur sans ouvrir de fenêtre.
        controleur = GameController.__new__(GameController)
        controleur.model = modele
        controleur.input_handler = Mock()

        controleur.input_handler.get_inputs.return_value = {
            "player1": commandes1,
            "player2": commandes2
        }

        # Exécute la vraie méthode du contrôleur.
        controleur.update()

        # Le joueur 1 accélère uniquement sa voiture.
        voiture1.accelerate.assert_called_once_with()
        voiture1.steer_right.assert_not_called()

        # Le joueur 2 tourne uniquement sa voiture.
        voiture2.steer_right.assert_called_once_with()
        voiture2.accelerate.assert_not_called()

        # Le modèle est mis à jour une seule fois.
        modele.update.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
