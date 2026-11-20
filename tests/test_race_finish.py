
# Kart-Engine v2.3

import unittest
from unittest.mock import Mock, patch

from constants import GameState
from model.game_model import GameModel
from controller.game_controller import GameController


class TestRaceFinish(unittest.TestCase):
    """
    Tests de la fin de course.

    Vérifie la victoire, l'arrêt des voitures
    et le blocage des commandes après la course.
    """

    def setUp(self):
        """
        Prépare une nouvelle course avant chaque test.
        """
        self.model = GameModel()
        self.model.load_circuit()
        self.model.state = GameState.RACING

    def test_winner_after_all_laps(self):
        """
        Le joueur gagne après tous les tours prévus.
        """
        race = self.model.race_coordinator

        for _ in range(race.laps_to_win):
            for checkpoint in race.checkpoints:
                race.update_player_tile(
                    "player1",
                    checkpoint
                )

            race.update_player_tile(
                "player1",
                race.finish_position
            )

        self.assertEqual(race.winner, "player1")
        self.assertTrue(self.model.is_race_finished())

    def test_both_cars_stop_after_victory(self):
        """
        Les deux voitures s'arrêtent après la victoire.
        """
        self.model.car.speed = 5.0
        self.model.car2.speed = 3.0

        position1 = (self.model.car.x, self.model.car.y)
        position2 = (self.model.car2.x, self.model.car2.y)

        # Simule une victoire déjà enregistrée.
        self.model.race_coordinator.winner = "player1"

        self.model.update()

        self.assertEqual(self.model.car.speed, 0.0)
        self.assertEqual(self.model.car2.speed, 0.0)

        self.assertEqual(
            (self.model.car.x, self.model.car.y),
            position1
        )
        self.assertEqual(
            (self.model.car2.x, self.model.car2.y),
            position2
        )

    def test_player2_does_not_move_after_player1_wins(self):
        """
        Si le joueur 1 gagne pendant une frame,
        le joueur 2 n'est plus mis à jour.
        """
        def simulate_update(player, car):
            if player == "player1":
                self.model.race_coordinator.winner = "player1"

        with patch.object(
            self.model,
            "_update_car",
            side_effect=simulate_update
        ) as mocked_update:

            self.model.update()

            self.assertEqual(mocked_update.call_count, 1)
            self.assertEqual(
                mocked_update.call_args.args[0],
                "player1"
            )

    def test_controller_ignores_inputs_after_victory(self):
        """
        Le contrôleur ne lit plus les commandes
        lorsque la course est terminée.
        """
        self.model.race_coordinator.winner = "player2"

        # Crée un contrôleur sans ouvrir une fenêtre Pygame.
        controller = GameController.__new__(GameController)
        controller.model = self.model
        controller.input_handler = Mock()

        with patch.object(self.model, "update") as mocked_update:
            controller.update()

            controller.input_handler.get_inputs.assert_not_called()
            mocked_update.assert_not_called()


if __name__ == "__main__":
    unittest.main()
