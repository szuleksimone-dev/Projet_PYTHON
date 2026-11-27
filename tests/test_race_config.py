# Kart-Engine v2.3

import unittest
from unittest.mock import Mock

from constants import GameState, TILE_SIZE
from model.game_model import GameModel
from model.race_config import get_race_config
from model.race_coordinator import RaceCoordinator


class TestRaceConfig(unittest.TestCase):
    """
    Vérifie la configuration automatique de la course.

    Teste aussi les checkpoints dans l'ordre
    et la progression indépendante des deux joueurs.
    """

    def test_configuration_automatique(self):
        """
        Vérifie que load_circuit() initialise
        correctement les paramètres de la course.
        """
        model = GameModel()
        model.load_circuit()

        config = get_race_config()
        race = model.race_coordinator

        self.assertIsNotNone(race)

        # Une liste conserve l'ordre des checkpoints.
        self.assertEqual(
            race.checkpoints,
            list(config["checkpoints"])
        )

        self.assertEqual(
            race.finish_position,
            config["finish_position"]
        )

        self.assertEqual(
            race.laps_to_win,
            config["laps_to_win"]
        )

        # Les deux joueurs commencent au premier checkpoint.
        self.assertEqual(
            race.next_checkpoint_index["player1"],
            0
        )

        self.assertEqual(
            race.next_checkpoint_index["player2"],
            0
        )

    def test_nouvelle_course(self):
        """
        Vérifie qu'une nouvelle course remet
        les tours, les checkpoints et le vainqueur à zéro.
        """
        model = GameModel()
        model.load_circuit()

        # Simulation d'une ancienne progression.
        model.race_coordinator.laps["player1"] = 2
        model.race_coordinator.winner = "player1"

        model.race_coordinator.next_checkpoint_index["player1"] = 2

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

        self.assertEqual(
            model.race_coordinator.next_checkpoint_index["player1"],
            0
        )

        self.assertIsNone(
            model.race_coordinator.winner
        )

    def test_checkpoint_deux_joueurs(self):
        """
        Vérifie que les deux voitures peuvent valider
        le premier checkpoint pendant GameModel.update().
        """
        model = GameModel()
        model.load_circuit()
        model.state = GameState.RACING

        # Premier checkpoint du circuit.
        checkpoint = get_race_config()["checkpoints"][0]
        col, row = checkpoint

        def aller_au_checkpoint(voiture):
            """
            Simule l'arrivée d'une voiture
            sur la case du checkpoint.
            """
            voiture.x = (col + 0.5) * TILE_SIZE
            voiture.y = (row + 0.5) * TILE_SIZE

        # Remplace uniquement le mouvement physique
        # pour tester la logique de course.
        model.car.update_position = Mock(
            side_effect=lambda: aller_au_checkpoint(model.car)
        )

        model.car2.update_position = Mock(
            side_effect=lambda: aller_au_checkpoint(model.car2)
        )

        # Mise à jour du modèle.
        model.update()

        # Chaque joueur valide CP1.
        self.assertIn(
            checkpoint,
            model.race_coordinator.visited["player1"]
        )

        self.assertIn(
            checkpoint,
            model.race_coordinator.visited["player2"]
        )

        # Les deux joueurs attendent maintenant CP2.
        self.assertEqual(
            model.race_coordinator.next_checkpoint_index["player1"],
            1
        )

        self.assertEqual(
            model.race_coordinator.next_checkpoint_index["player2"],
            1
        )

    def test_checkpoints_mauvais_ordre(self):
        """
        Vérifie qu'un checkpoint ne peut pas
        être validé avant les précédents.
        """
        config = get_race_config()

        race = RaceCoordinator(
            checkpoints=config["checkpoints"],
            finish_position=config["finish_position"],
            laps_to_win=config["laps_to_win"]
        )

        cp1, cp2, cp3, cp4 = config["checkpoints"]

        # Le joueur essaie CP3 avant CP1.
        race.update_player_tile("player1", cp3)

        # Aucun checkpoint n'est validé.
        self.assertEqual(
            race.next_checkpoint_index["player1"],
            0
        )

        self.assertEqual(
            race.visited["player1"],
            set()
        )

        # Le joueur valide CP1.
        race.update_player_tile("player1", cp1)

        self.assertEqual(
            race.next_checkpoint_index["player1"],
            1
        )

        # Il essaie CP4 sans passer par CP2.
        race.update_player_tile("player1", cp4)

        # CP4 est ignoré : le prochain reste CP2.
        self.assertEqual(
            race.next_checkpoint_index["player1"],
            1
        )

        # Le passage sur la ligne d'arrivée
        # ne valide pas un tour incomplet.
        race.update_player_tile(
            "player1",
            config["finish_position"]
        )

        self.assertEqual(
            race.laps["player1"],
            0
        )

    def test_checkpoints_bon_ordre(self):
        """
        Vérifie que CP1, CP2, CP3 et CP4
        doivent être franchis dans cet ordre
        avant de valider un tour.
        """
        config = get_race_config()

        race = RaceCoordinator(
            checkpoints=config["checkpoints"],
            finish_position=config["finish_position"],
            laps_to_win=config["laps_to_win"]
        )

        checkpoints = config["checkpoints"]

        # Le joueur franchit les checkpoints
        # dans le bon ordre.
        for index, checkpoint in enumerate(checkpoints):
            race.update_player_tile("player1", checkpoint)

            self.assertEqual(
                race.next_checkpoint_index["player1"],
                index + 1
            )

        # Passage sur la ligne d'arrivée.
        race.update_player_tile(
            "player1",
            config["finish_position"]
        )

        # Un tour est validé.
        self.assertEqual(
            race.laps["player1"],
            1
        )

        # Le joueur doit recommencer par CP1.
        self.assertEqual(
            race.next_checkpoint_index["player1"],
            0
        )

        self.assertEqual(
            race.visited["player1"],
            set()
        )

        # L'autre joueur n'a pas progressé.
        self.assertEqual(
            race.laps["player2"],
            0
        )

        self.assertEqual(
            race.next_checkpoint_index["player2"],
            0
        )


if __name__ == "__main__":
    unittest.main()