
# Kart-Engine v2.3

import unittest

from constants import GameState, TILE_SIZE
from model.game_model import GameModel


class TestCompleteRace(unittest.TestCase):
    """
    Tests d'une course complète.

    Vérifie la progression des joueurs
    depuis les checkpoints jusqu'à la victoire.
    """

    def setUp(self):
        """
        Prépare une nouvelle course avec deux joueurs.
        """
        self.model = GameModel()
        self.model.load_circuit()
        self.model.state = GameState.RACING

    def move_to_tile(self, player, position):
        """
        Place une voiture sur une case du circuit.

        Cette méthode simule le passage sur une case
        sans utiliser les commandes du clavier.
        """
        if player == "player1":
            car = self.model.car
        else:
            car = self.model.car2

        col, row = position

        car.x = col * TILE_SIZE + TILE_SIZE // 2
        car.y = row * TILE_SIZE + TILE_SIZE // 2
        car.speed = 0.0

        # Le modèle vérifie les checkpoints et l'arrivée.
        self.model.update()

    def complete_lap(self, player):
        """
        Simule le passage sur tous les checkpoints
        puis sur la ligne d'arrivée.
        """
        race = self.model.race_coordinator

        for checkpoint in race.checkpoints:
            self.move_to_tile(player, checkpoint)

        self.move_to_tile(player, race.finish_position)

    def test_incomplete_lap(self):
        """
        Un tour incomplet ne doit pas être compté.
        """
        race = self.model.race_coordinator

        # Le joueur passe seulement sur un checkpoint.
        checkpoint = next(iter(race.checkpoints))
        self.move_to_tile("player1", checkpoint)

        # Puis il traverse la ligne d'arrivée.
        self.move_to_tile(
            "player1",
            race.finish_position
        )

        self.assertEqual(race.laps["player1"], 0)
        self.assertIsNone(race.winner)

    def test_player1_wins_complete_race(self):
        """
        Le joueur 1 gagne après trois tours complets.
        """
        race = self.model.race_coordinator

        for _ in range(race.laps_to_win):
            self.complete_lap("player1")

        self.assertEqual(
            race.laps["player1"],
            race.laps_to_win
        )
        self.assertEqual(race.winner, "player1")
        self.assertTrue(self.model.is_race_finished())

    def test_player2_wins_complete_race(self):
        """
        Le joueur 2 peut aussi gagner indépendamment.
        """
        race = self.model.race_coordinator

        # Le joueur 1 termine seulement un tour.
        self.complete_lap("player1")

        # Le joueur 2 termine tous les tours.
        for _ in range(race.laps_to_win):
            self.complete_lap("player2")

        self.assertEqual(race.laps["player1"], 1)
        self.assertEqual(
            race.laps["player2"],
            race.laps_to_win
        )
        self.assertEqual(race.winner, "player2")


if __name__ == "__main__":
    unittest.main()
