# Kart-Engine v2.3

from constants import GameState, TILE_SIZE
from model.car import Car
from model.circuit_maps import CIRCUIT_1, CIRCUIT_2
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.race_coordinator import RaceCoordinator
from model.race_config import get_race_config
from model.special_blocks import SpecialBlocks


class GameModel:
    """
    Partie MVC : Modèle.

    Gère les données et la logique du jeu :
    les circuits, les deux voitures, les checkpoints,
    les tours et les blocs spéciaux.
    """

    def __init__(self, start_col=7, start_row=1):
        """
        Initialise le modèle avec le menu principal.

        Le circuit et les voitures sont créés
        au moment du lancement d'une course.
        """
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None

        # Positions de départ par défaut.
        self.start_col = start_col
        self.start_row = start_row

        # Une voiture pour chaque joueur.
        self.car: Car | None = None
        self.car2: Car | None = None

        # Dernières positions sûres des deux voitures.
        self.last_safe_positions = {
            "player1": (
                start_col * TILE_SIZE + TILE_SIZE // 2,
                start_row * TILE_SIZE + TILE_SIZE // 2
            ),
            "player2": (
                start_col * TILE_SIZE + TILE_SIZE // 2,
                (start_row + 1) * TILE_SIZE + TILE_SIZE // 2
            )
        }

        # Compatibilité avec l'ancien code du joueur 1.
        self.last_safe_x, self.last_safe_y = (
            self.last_safe_positions["player1"]
        )

        # Sélection du circuit.
        self.circuit_list = [
            "Circuit Simple",
            "Circuit Complexe"
        ]
        self.selected_circuit_idx = 0

        # Logique des tours et de la victoire.
        self.race_coordinator: RaceCoordinator | None = None

        # Gestion des boosts et des blocs de départ.
        self.special_blocks: SpecialBlocks | None = None

    def load_circuit(self) -> None:
        """
        Appel : Depuis GameController.

        Crée le circuit, configure les blocs spéciaux,
        place les deux voitures et prépare la course.
        """
        # Choix de la carte créée par un autre membre du groupe.
        if self.selected_circuit_idx == 0:
            level_map = CIRCUIT_1
        else:
            level_map = CIRCUIT_2

        # Convertit chaque lettre en un objet RoadTile.
        terrain_types = {
            "R": "road",
            "G": "grass",
            "I": "ice",
            "T": "terre",
            "F": "fence"
        }

        grid = []
        for row_idx, row_str in enumerate(level_map):
            row_tiles = []
            for col_idx, symbol in enumerate(row_str):
                tile_type = terrain_types[symbol]
                row_tiles.append(
                    RoadTile(
                        col=col_idx,
                        row=row_idx,
                        tile_type=tile_type
                    )
                )
            grid.append(row_tiles)

        # Création du circuit.
        self.circuit = Circuit(grid=grid)

        # Lecture des paramètres provisoires de la course.
        race_config = get_race_config()

        # Création des blocs spéciaux.
        # Les positions pourront changer avec le level design.
        self.special_blocks = SpecialBlocks(
            boost_positions=race_config["boost_positions"],
            start_positions={
                "player1": (
                    self.start_col,
                    self.start_row
                ),
                "player2": (
                    self.start_col,
                    self.start_row + 1
                )
            }
        )

        # Place les voitures sur leurs blocs de départ.
        self.spawn_car()

        # Initialise les checkpoints, les tours et l'arrivée.
        self.configure_race(
            checkpoints=race_config["checkpoints"],
            finish_position=race_config["finish_position"],
            laps_to_win=race_config["laps_to_win"]
        )

    def spawn_car(self) -> None:
        """
        Appel : Depuis load_circuit().

        Crée les voitures sur les blocs de départ.

        Si les blocs spéciaux ne sont pas encore chargés,
        utilise les positions de départ par défaut.
        """
        start1 = (
            self.start_col,
            self.start_row
        )

        start2 = (
            self.start_col,
            self.start_row + 1
        )

        # Récupère les positions des blocs de départ.
        if self.special_blocks is not None:
            start1 = self.special_blocks.get_start_position(
                "player1"
            )
            start2 = self.special_blocks.get_start_position(
                "player2"
            )

        # Création des voitures.
        self.car = Car(*start1)
        self.car2 = Car(*start2)

        # Initialise les positions de sécurité.
        self.last_safe_positions = {
            "player1": (self.car.x, self.car.y),
            "player2": (self.car2.x, self.car2.y)
        }

        self.last_safe_x = self.car.x
        self.last_safe_y = self.car.y

    def configure_race(
        self, checkpoints, finish_position, laps_to_win=3
    ) -> None:
        """
        Appel : Depuis load_circuit().

        Initialise les checkpoints, la ligne d'arrivée
        et le nombre de tours nécessaires pour gagner.
        """
        if self.circuit is None:
            raise ValueError(
                "Le circuit doit être chargé avant la course."
            )

        self.race_coordinator = RaceCoordinator(
            checkpoints=checkpoints,
            finish_position=finish_position,
            laps_to_win=laps_to_win
        )

    def is_race_finished(self) -> bool:
        """
        Retourne True si un joueur a gagné.

        Le contrôleur et la vue peuvent utiliser
        cette information.
        """
        return (
            self.race_coordinator is not None
            and self.race_coordinator.winner is not None
        )

    def _stop_cars(self) -> None:
        """
        Arrête les deux voitures après une victoire.
        """
        for car in (self.car, self.car2):
            if car is not None:
                car.speed = 0.0

    def update(self) -> None:
        """
        Appel : Depuis GameController.update().

        Met à jour les voitures pendant la course.
        Arrête immédiatement la course si un joueur gagne.
        """
        if self.state != GameState.RACING:
            return

        if self.circuit is None:
            return

        # Aucune voiture ne bouge après la victoire.
        if self.is_race_finished():
            self._stop_cars()
            return

        # Mise à jour du joueur 1.
        if self.car is not None:
            self._update_car("player1", self.car)

            if self.is_race_finished():
                self._stop_cars()
                return

        # Mise à jour du joueur 2.
        if self.car2 is not None:
            self._update_car("player2", self.car2)

            if self.is_race_finished():
                self._stop_cars()
                return

    def _update_car(self, player, car) -> None:
        """
        Appel : Depuis update(), pour chaque voiture.

        Applique la physique du terrain, déplace la voiture
        et vérifie les boosts ainsi que les checkpoints.
        """
        # Position actuelle de la voiture dans la grille.
        car_col = int(car.x // TILE_SIZE)
        car_row = int(car.y // TILE_SIZE)

        current_tile = self.circuit.get_tile(
            car_col,
            car_row
        )

        # Une barrière ou le vide n'est pas traversable.
        if (
            current_tile is None
            or current_tile.tile_type in ("empty", "fence")
        ):
            car.x, car.y = self.last_safe_positions[player]
            car.speed = 0.0
            return

        # Propriétés physiques du terrain.
        car.grip_factor = current_tile.grip
        car.traction_factor = current_tile.traction_factor
        car.drift_threshold = current_tile.drift_threshold
        car.drift_friction = current_tile.drift_friction

        # Sauvegarde de la position sûre.
        self.last_safe_positions[player] = (
            car.x,
            car.y
        )

        if player == "player1":
            self.last_safe_x = car.x
            self.last_safe_y = car.y

        # Déplacement de la voiture.
        car.update_position()

        # Nouvelle position dans la grille.
        new_col = int(car.x // TILE_SIZE)
        new_row = int(car.y // TILE_SIZE)

        new_tile = self.circuit.get_tile(
            new_col,
            new_row
        )

        # Collision avec une barrière ou sortie de la carte.
        # Chaque voiture revient à sa propre position sûre.
        if (
            new_tile is None
            or new_tile.tile_type in ("empty", "fence")
        ):
            car.x, car.y = self.last_safe_positions[player]
            car.speed = 0.0
            return

        new_position = (new_col, new_row)

        # Vérifie les cases de boost.
        # Le boost est appliqué à l'entrée sur la case.
        if self.special_blocks is not None:
            self.special_blocks.update_player(
                player,
                new_position,
                car
            )

        # Vérifie les checkpoints et les tours.
        if self.race_coordinator is not None:
            self.race_coordinator.update_player_tile(
                player,
                new_position
            )