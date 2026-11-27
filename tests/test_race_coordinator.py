
# Kart-Engine v2.3

import unittest
from model.race_coordinator import RaceCoordinator


class TestRaceCoordinator(unittest.TestCase):
    """Vérifie les règles principales de la course."""

    def setUp(self):
        """Crée une course avec deux checkpoints et deux tours."""
        self.race = RaceCoordinator(
            checkpoints=[(2, 1), (4, 1)],
            finish_position=(6, 1),
            laps_to_win=2
        )

    def test_arrivee_sans_checkpoints(self):
        """L'arrivée seule ne valide pas un tour."""
        self.race.update_player_tile("player1", (6, 1))
        self.assertEqual(self.race.laps["player1"], 0)

    def test_tour_complet(self):
        """Tous les checkpoints permettent de valider un tour."""
        for case in ((2, 1), (4, 1), (6, 1)):
            self.race.update_player_tile("player1", case)

        self.assertEqual(self.race.laps["player1"], 1)

    def test_pas_de_double_comptage(self):
        """Rester sur l'arrivée ne compte pas deux tours."""
        for case in ((2, 1), (4, 1), (6, 1), (6, 1)):
            self.race.update_player_tile("player1", case)

        self.assertEqual(self.race.laps["player1"], 1)

    def test_joueurs_independants(self):
        """Les checkpoints sont propres à chaque joueur."""
        for case in ((2, 1), (4, 1), (6, 1)):
            self.race.update_player_tile("player1", case)

        self.race.update_player_tile("player2", (6, 1))

        self.assertEqual(self.race.laps["player1"], 1)
        self.assertEqual(self.race.laps["player2"], 0)

    def test_vainqueur(self):
        """Le joueur qui termine les deux tours gagne."""
        for case in (
            (2, 1), (4, 1), (6, 1),
            (2, 1), (4, 1), (6, 1)
        ):
            self.race.update_player_tile("player2", case)

        self.assertEqual(self.race.laps["player2"], 2)
        self.assertEqual(self.race.winner, "player2")


if __name__ == "__main__":
    unittest.main()
