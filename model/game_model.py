
# Kart-Engine v2.3

from constants import GameState, GRID_ROWS, GRID_COLS, TILE_SIZE
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.race_coordinator import RaceCoordinator


class GameModel:
    """
    Partie MVC : Modèle.

    Gère les données et la logique du jeu :
    les circuits, les deux voitures et la progression de la course.
    """

    def __init__(self, start_col=7, start_row=1):
        """
        Initialise le modèle avec le menu principal.
        Les voitures seront créées au chargement du circuit.
        """
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None

        # Positions de départ.
        self.start_col = start_col
        self.start_row = start_row

        # Une voiture indépendante pour chaque joueur.
        # self.car garde son ancien nom pour la compatibilité.
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

        # Compatibilité avec le code précédent.
        self.last_safe_x, self.last_safe_y = (
            self.last_safe_positions["player1"]
        )

        # Sélection du circuit.
        self.circuit_list = ["Circuit Simple", "Circuit Complexe"]
        self.selected_circuit_idx = 0

        # Gestion des checkpoints, des tours et du vainqueur.
        self.race_coordinator: RaceCoordinator | None = None

    def load_circuit(self) -> None:
        """
        Appel : Depuis GameController après la sélection du circuit.

        Construit le circuit et crée les deux voitures.
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

        self.circuit = Circuit(grid=grid)

        # Une nouvelle course repart de zéro.
        self.race_coordinator = None

        self.spawn_car()

    def spawn_car(self) -> None:
        """
        Appel : Depuis load_circuit().

        Crée deux voitures à des positions différentes.
        Le joueur 2 démarre une ligne plus bas.
        """
        self.car = Car(self.start_col, self.start_row)
        self.car2 = Car(self.start_col, self.start_row + 1)

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
        Appel : Après load_circuit(), lorsque les positions
        des checkpoints et de l'arrivée sont connues.

        Initialise la progression des deux joueurs.
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

        Met à jour séparément la physique des deux voitures
        et leur progression dans la course.
        """
        if self.state != GameState.RACING or self.circuit is None:
            return

        if self.car is not None:
            self._update_car("player1", self.car)

        if self.car2 is not None:
            self._update_car("player2", self.car2)

    def _update_car(self, player, car) -> None:
        """
        Appel : Depuis update(), pour chaque voiture.

        Applique les propriétés du terrain, déplace la voiture
        et vérifie les checkpoints.

        Chaque joueur possède sa propre position de sécurité.
        """
        # Position actuelle dans la grille.
        car_col = int(car.x // TILE_SIZE)
        car_row = int(car.y // TILE_SIZE)

        current_tile = self.circuit.get_tile(car_col, car_row)

        # Si la voiture est hors de la piste, on la replace.
        if current_tile is None or current_tile.tile_type == "empty":
            car.x, car.y = self.last_safe_positions[player]
            car.speed = 0.0
            return

        # Propriétés physiques du terrain actuel.
        car.grip_factor = current_tile.grip
        car.traction_factor = current_tile.traction_factor
        car.drift_threshold = current_tile.drift_threshold
        car.drift_friction = current_tile.drift_friction

        # Sauvegarde de la position avant le déplacement.
        self.last_safe_positions[player] = (car.x, car.y)

        if player == "player1":
            self.last_safe_x = car.x
            self.last_safe_y = car.y

        # Déplacement de la voiture.
        car.update_position()

        # Vérification de la nouvelle position.
        new_col = int(car.x // TILE_SIZE)
        new_row = int(car.y // TILE_SIZE)

        new_tile = self.circuit.get_tile(new_col, new_row)

        # Empêche la voiture de sortir du circuit.
        if new_tile is None or new_tile.tile_type == "empty":
            car.x, car.y = self.last_safe_positions[player]
            car.speed = 0.0
            return

        # Enregistre la progression du bon joueur.
        if self.race_coordinator is not None:
            self.race_coordinator.update_player_tile(
                player,
                (new_col, new_row)
            )
