
# Kart-Engine v2.3

from constants import GameState, GRID_ROWS, GRID_COLS, TILE_SIZE
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.race_coordinator import RaceCoordinator
from model.race_config import get_race_config


class GameModel:
    """
    Partie MVC : Modèle.

    Gère les données et la logique du jeu :
    les circuits, les deux voitures et la progression de la course.
    """

    def __init__(self, start_col=7, start_row=1):
        """
        Initialise le modèle avec le menu principal.

        Les voitures et le circuit seront créés
        lorsque le joueur démarre une course.
        """
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None

        # Positions de départ des voitures.
        self.start_col = start_col
        self.start_row = start_row

        # Une voiture indépendante pour chaque joueur.
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

        # Sélection du circuit dans le menu.
        self.circuit_list = [
            "Circuit Simple",
            "Circuit Complexe"
        ]
        self.selected_circuit_idx = 0

        # Gestion des checkpoints, des tours et du vainqueur.
        self.race_coordinator: RaceCoordinator | None = None

    def load_circuit(self) -> None:
        """
        Appel : Depuis GameController, après le choix du circuit.

        Crée la grille, les deux voitures et initialise
        automatiquement les règles de la course.
        """
        if self.selected_circuit_idx == 0:
            grid = [
                [
                    RoadTile(
                        col=col_idx,
                        row=row_idx,
                        tile_type="road"
                    )
                    for col_idx in range(GRID_COLS)
                ]
                for row_idx in range(GRID_ROWS)
            ]
        else:
            grid = [
                [
                    RoadTile(
                        col=col_idx,
                        row=row_idx,
                        tile_type="grass"
                    )
                    for col_idx in range(GRID_COLS)
                ]
                for row_idx in range(GRID_ROWS)
            ]

        # Création du circuit.
        self.circuit = Circuit(grid=grid)

        # Création des voitures des deux joueurs.
        self.spawn_car()

        # Lecture des checkpoints et de la ligne d'arrivée.
        race_config = get_race_config()

        # Initialisation automatique de la course.
        self.configure_race(
            checkpoints=race_config["checkpoints"],
            finish_position=race_config["finish_position"],
            laps_to_win=race_config["laps_to_win"]
        )

    def spawn_car(self) -> None:
        """
        Appel : Depuis load_circuit().

        Crée deux voitures à des positions différentes.
        Le joueur 2 commence une ligne plus bas.
        """
        self.car = Car(self.start_col, self.start_row)
        self.car2 = Car(self.start_col, self.start_row + 1)

        # Chaque voiture possède sa propre position de sécurité.
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

        Initialise RaceCoordinator avec les positions
        des checkpoints et de la ligne d'arrivée.

        Chaque joueur possède sa propre progression.
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

    def update(self) -> None:
        """
        Appel : Depuis GameController.update(), à chaque frame.

        Met à jour séparément les deux voitures.
        Vérifie aussi leur progression dans la course.
        """
        if self.state != GameState.RACING:
            return

        if self.circuit is None:
            return

        # Mise à jour de la voiture du joueur 1.
        if self.car is not None:
            self._update_car("player1", self.car)

        # Mise à jour de la voiture du joueur 2.
        if self.car2 is not None:
            self._update_car("player2", self.car2)

    def _update_car(self, player, car) -> None:
        """
        Appel : Depuis update(), pour chaque voiture.

        Applique la physique du terrain, déplace la voiture
        et enregistre les checkpoints franchis.

        Les deux joueurs sont traités indépendamment.
        """
        # Position actuelle dans la grille.
        car_col = int(car.x // TILE_SIZE)
        car_row = int(car.y // TILE_SIZE)

        # Récupération du terrain sous la voiture.
        current_tile = self.circuit.get_tile(
            car_col,
            car_row
        )

        # Si la voiture est hors du circuit, on la replace.
        if (
            current_tile is None
            or current_tile.tile_type == "empty"
        ):
            car.x, car.y = self.last_safe_positions[player]
            car.speed = 0.0
            return

        # Application des propriétés physiques du terrain.
        car.grip_factor = current_tile.grip
        car.traction_factor = current_tile.traction_factor
        car.drift_threshold = current_tile.drift_threshold
        car.drift_friction = current_tile.drift_friction

        # Sauvegarde de la dernière position sûre.
        self.last_safe_positions[player] = (
            car.x,
            car.y
        )

        if player == "player1":
            self.last_safe_x = car.x
            self.last_safe_y = car.y

        # Déplacement physique de la voiture.
        car.update_position()

        # Nouvelle position dans la grille.
        new_col = int(car.x // TILE_SIZE)
        new_row = int(car.y // TILE_SIZE)

        new_tile = self.circuit.get_tile(
            new_col,
            new_row
        )

        # Empêche la voiture de rester hors du circuit.
        if (
            new_tile is None
            or new_tile.tile_type == "empty"
        ):
            car.x, car.y = self.last_safe_positions[player]
            car.speed = 0.0
            return

        # Enregistre le passage sur les checkpoints
        # et vérifie le franchissement de l'arrivée.
        if self.race_coordinator is not None:
            self.race_coordinator.update_player_tile(
                player,
                (new_col, new_row)
            )
