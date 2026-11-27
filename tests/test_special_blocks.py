
# Kart-Engine v2.3

import unittest
from unittest.mock import Mock

from model.special_blocks import SpecialBlocks


class TestSpecialBlocks(unittest.TestCase):
    """
    Tests des blocs spéciaux du circuit.

    Vérifie les boosts et les positions de départ
    des deux joueurs.
    """

    def setUp(self):
        """
        Prépare les blocs spéciaux avant chaque test.
        """
        self.blocks = SpecialBlocks(
            boost_positions=[(5, 3), (10, 7)],
            start_positions={
                "player1": (7, 1),
                "player2": (7, 2)
            },
            boost_amount=2.0,
            max_boost_speed=9.0
        )

    def test_start_positions(self):
        """
        Chaque joueur possède sa propre case de départ.
        """
        self.assertEqual(
            self.blocks.get_start_position("player1"),
            (7, 1)
        )
        self.assertEqual(
            self.blocks.get_start_position("player2"),
            (7, 2)
        )

    def test_boost_on_entry(self):
        """
        Le boost augmente la vitesse à l'entrée
        sur une case spéciale.
        """
        car = Mock()
        car.speed = 3.0

        activated = self.blocks.update_player(
            "player1", (5, 3), car
        )

        self.assertTrue(activated)
        self.assertEqual(car.speed, 5.0)

    def test_no_repeated_boost_on_same_tile(self):
        """
        Rester sur la même case ne donne pas
        plusieurs boosts.
        """
        car = Mock()
        car.speed = 3.0

        self.blocks.update_player("player1", (5, 3), car)
        activated = self.blocks.update_player(
            "player1", (5, 3), car
        )

        self.assertFalse(activated)
        self.assertEqual(car.speed, 5.0)

    def test_boost_speed_limit(self):
        """
        La vitesse ne dépasse pas la limite du boost.
        """
        car = Mock()
        car.speed = 8.0

        self.blocks.update_player("player1", (5, 3), car)

        self.assertEqual(car.speed, 9.0)

    def test_players_are_independent(self):
        """
        Les deux joueurs peuvent activer
        le même boost séparément.
        """
        car1 = Mock()
        car1.speed = 2.0

        car2 = Mock()
        car2.speed = 4.0

        self.assertTrue(
            self.blocks.update_player("player1", (5, 3), car1)
        )
        self.assertTrue(
            self.blocks.update_player("player2", (5, 3), car2)
        )

        self.assertEqual(car1.speed, 4.0)
        self.assertEqual(car2.speed, 6.0)

    def test_no_boost_in_reverse(self):
        """
        Une voiture qui recule ne reçoit pas de boost.
        """
        car = Mock()
        car.speed = -2.0

        activated = self.blocks.update_player(
            "player1", (5, 3), car
        )

        self.assertFalse(activated)
        self.assertEqual(car.speed, -2.0)


if __name__ == "__main__":
    unittest.main()
