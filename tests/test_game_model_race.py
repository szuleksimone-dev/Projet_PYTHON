
# Kart-Engine v2.3

import unittest
from unittest.mock import Mock

from constants import GameState, TILE_SIZE
from model.circuit import Circuit
from model.game_model import GameModel
from model.road_tile import RoadTile


class TestGameModelRace(unittest.TestCase):
    """
    Vérifie la connexion entre GameModel et RaceCoordinator.

    Les déplacements sont simulés pour tester la logique
    de course sans dépendre du clavier ou de la physique.
    """

    def setUp(self):
        """
        Appel : Avant chaque test.

        Crée un petit circuit de trois cases et
        prépare une voiture simulée.
        """
        self.model = GameModel()

        grid = [[
            RoadTile(col=0, row=0, tile_type="road"),
            RoadTile(col=1, row=0, tile_type="road"),
            RoadTile(col=2, row=0, tile_type="road")
        ]]

        self.model.circuit = Circuit(grid)

        # La voiture simulée commence sur la première case.
        self.model.car = Mock()
        self.model.car.x = TILE_SIZE / 2
        self.model.car.y = TILE_SIZE / 2
        self.model.car.speed = 0.0

        self.model.state = GameState.RACING

    def simuler_deplacement(self, colonne):
        """
        Simule un déplacement vers une case du circuit.

        Remplace seulement le calcul physique du mouvement.
        GameModel.update() reste réellement exécuté.
        """
        def avancer():
            self.model.car.x = (colonne + 0.5) * TILE_SIZE

        self.model.car.update_position.side_effect = avancer

    def test_checkpoint_et_arrivee(self):
        """
        Vérifie qu'un checkpoint suivi de l'arrivée
        valide un tour et désigne le vainqueur.
        """
        self.model.configure_race(
            checkpoints=[(1, 0)],
            finish_position=(2, 0),
            laps_to_win=1
        )

        # Premier déplacement : passage au checkpoint.
        self.simuler_deplacement(1)
        self.model.update()

        self.assertIn(
            (1, 0),
            self.model.race_coordinator.visited["player1"]
        )

        # Deuxième déplacement : passage à l'arrivée.
        self.simuler_deplacement(2)
        self.model.update()

        self.assertEqual(
            self.model.race_coordinator.laps["player1"],
            1
        )
        self.assertEqual(
            self.model.race_coordinator.winner,
            "player1"
        )

    def test_arrivee_sans_checkpoint(self):
        """
        Vérifie que traverser l'arrivée sans avoir
        visité le checkpoint ne valide aucun tour.
        """
        self.model.configure_race(
            checkpoints=[(1, 0)],
            finish_position=(2, 0),
            laps_to_win=1
        )

        # La voiture va directement à l'arrivée.
        self.simuler_deplacement(2)
        self.model.update()

        self.assertEqual(
            self.model.race_coordinator.laps["player1"],
            0
        )
        self.assertIsNone(
            self.model.race_coordinator.winner
        )

    def test_configuration_sans_circuit(self):
        """
        Vérifie qu'une course ne peut pas être
        configurée avant le chargement du circuit.
        """
        model = GameModel()

        with self.assertRaises(ValueError):
            model.configure_race(
                checkpoints=[(1, 0)],
                finish_position=(2, 0)
            )


if __name__ == "__main__":
    unittest.main()
