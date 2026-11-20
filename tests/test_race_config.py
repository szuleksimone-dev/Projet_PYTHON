
# Kart-Engine v2.3

import unittest
from unittest.mock import Mock

from constants import GameState, TILE_SIZE
from model.game_model import GameModel
from model.race_config import get_race_config


class TestRaceConfig(unittest.TestCase):
    """
    Vérifie la configuration automatique de la course.

    Les checkpoints, les tours et le vainqueur
    doivent être gérés pour les deux joueurs.
    """

    def test_configuration_automatique(self):
        """
        Vérifie que load_circuit() initialise
        automatiquement RaceCoordinator.
        """
        model = GameModel()

        # Avant le chargement, aucune course n'existe.
        self.assertIsNone(model.race_coordinator)

        # Le circuit initialise les règles de course.
        model.load_circuit()

        race = model.race_coordinator
        config = get_race_config()

        self.assertIsNotNone(race)
        self.assertEqual(
            race.checkpoints,
            set(config["checkpoints"])
        )
        self.assertEqual(
            race.finish_position,
            config["finish_position"]
        )
        self.assertEqual(
            race.laps_to_win,
            config["laps_to_win"]
        )

    def test_nouvelle_course(self):
        """
        Vérifie qu'une nouvelle course remet
        les tours et le vainqueur à zéro.
        """
        model = GameModel()
        model.load_circuit()

        # Simulation d'une ancienne progression.
        model.race_coordinator.laps["player1"] = 2
        model.race_coordinator.winner = "player1"

        # Chargement d'une nouvelle course.
        model.load_circuit()

        self.assertEqual(
            model.race_coordinator.laps["player1"],
            0
        )
        self.assertEqual(
            model.race_coordinator.laps["player2"],
            0
        )
        self.assertIsNone(
            model.race_coordinator.winner
        )

    def test_checkpoint_deux_joueurs(self):
        """
        Vérifie que les deux voitures peuvent valider
        un checkpoint pendant GameModel.update().
        """
        model = GameModel()
        model.load_circuit()
        model.state = GameState.RACING

        # Premier checkpoint du circuit d'essai.
        checkpoint = get_race_config()["checkpoints"][0]
        col, row = checkpoint

        def aller_au_checkpoint(voiture):
            """
            Simule l'arrivée d'une voiture
            sur la case du checkpoint.
            """
            voiture.x = (col + 0.5) * TILE_SIZE
            voiture.y = (row + 0.5) * TILE_SIZE

        # On remplace uniquement le mouvement physique
        # pour tester la logique de course.
        model.car.update_position = Mock(
            side_effect=lambda: aller_au_checkpoint(model.car)
        )

        model.car2.update_position = Mock(
            side_effect=lambda: aller_au_checkpoint(model.car2)
        )

        # Mise à jour réelle du modèle.
        model.update()

        # Chaque joueur valide son checkpoint.
        self.assertIn(
            checkpoint,
            model.race_coordinator.visited["player1"]
        )

        self.assertIn(
            checkpoint,
            model.race_coordinator.visited["player2"]
        )


if __name__ == "__main__":
    unittest.main()
