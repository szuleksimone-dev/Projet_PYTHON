
# Kart-Engine v2.3

import unittest

from constants import GameState, TILE_SIZE
from model.game_model import GameModel


class TestBoostIntegration(unittest.TestCase):
    """
    Tests d'intégration des blocs spéciaux.

    Vérifie que les boosts et les blocs de départ
    fonctionnent dans le modèle du jeu.
    """

    def setUp(self):
        """
        Prépare un circuit avec deux voitures.
        """
        self.model = GameModel()
        self.model.load_circuit()
        self.model.state = GameState.RACING

    def test_boost_in_game_model(self):
        """
        Une voiture placée sur un boost
        reçoit une augmentation de vitesse.
        """
        car = self.model.car

        # Place la voiture au centre du premier boost.
        car.x = 5 * TILE_SIZE + TILE_SIZE // 2
        car.y = 3 * TILE_SIZE + TILE_SIZE // 2
        car.speed = 0.0

        # Le modèle vérifie la case de boost.
        self.model.update()

        self.assertEqual(car.speed, 2.0)

    def test_no_double_boost_in_game_model(self):
        """
        Le boost ne se répète pas si la voiture
        reste sur la même case.
        """
        car = self.model.car

        car.x = 5 * TILE_SIZE + TILE_SIZE // 2
        car.y = 3 * TILE_SIZE + TILE_SIZE // 2
        car.speed = 0.0

        # Premier passage : le boost est activé.
        self.model.update()
        self.assertEqual(car.speed, 2.0)

        # Deuxième frame : pas de nouveau boost.
        self.model.update()

        # La vitesse diminue légèrement avec la friction.
        self.assertLess(car.speed, 2.0)
        self.assertGreater(car.speed, 0.0)

    def test_start_blocks_in_game_model(self):
        """
        Les voitures sont créées sur leurs
        blocs de départ respectifs.
        """
        blocks = self.model.special_blocks

        start1 = blocks.get_start_position("player1")
        start2 = blocks.get_start_position("player2")

        self.assertEqual(start1, (7, 1))
        self.assertEqual(start2, (7, 2))

        self.assertEqual(
            self.model.car.x,
            start1[0] * TILE_SIZE + TILE_SIZE // 2
        )

        self.assertEqual(
            self.model.car.y,
            start1[1] * TILE_SIZE + TILE_SIZE // 2
        )

        self.assertEqual(
            self.model.car2.x,
            start2[0] * TILE_SIZE + TILE_SIZE // 2
        )

        self.assertEqual(
            self.model.car2.y,
            start2[1] * TILE_SIZE + TILE_SIZE // 2
        )


if __name__ == "__main__":
    unittest.main()
