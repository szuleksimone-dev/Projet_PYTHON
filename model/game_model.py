
# Kart-Engine v2.3

from constants import GameState, GRID_ROWS, GRID_COLS, TILE_SIZE
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.race_coordinator import RaceCoordinator


class GameModel:
    """
    Partie MVC : Modèle.

    Gère les données et la logique globale du jeu :
    l'état du jeu, le circuit, la voiture et la course.
    """

    def __init__(self, start_col=7, start_row=1):
        """
        Initialise le modèle au menu principal.
        Aucun circuit ni aucune voiture n'est encore créé.
        """
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None

        # Dernière position sûre de la voiture.
        self.last_safe_x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.last_safe_y = start_row * TILE_SIZE + TILE_SIZE // 2

        # Sélection du circuit dans le menu.
        self.circuit_list = ["Circuit Simple", "Circuit Complexe"]
        self.selected_circuit_idx = 0

        # Gestion de la course, configurée après le chargement du circuit.
        self.race_coordinator: RaceCoordinator | None = None

    def load_circuit(self) -> None:
        """
        Appel : Depuis le contrôleur, après la sélection du circuit.

        Crée la grille du circuit et fait apparaître la voiture.
        """
        if self.selected_circuit_idx == 0:
            grid = [
                [
                    RoadTile(col=col_idx, row=row_idx, tile_type="road")
                    for col_idx in range(GRID_COLS)
                ]
                for row_idx in range(GRID_ROWS)
            ]
        else:
            grid = [
                [
                    RoadTile(col=col_idx, row=row_idx, tile_type="grass")
                    for col_idx in range(GRID_COLS)
                ]
                for row_idx in range(GRID_ROWS)
            ]

        # Exemple de carte plus élaborée pour une future version.
        """level_map = [
                "RRRRRRRRRRRRRRRR",
                "RIIIRRRRRRRRRRRR",
                "RIIIRRRRRRRRRRRR",
                "RRRRRRGGGGGRRRRR",
                "RRRRRRRRRRRRRRRR",
                # ... (autant de lignes que GRID_ROWS et GRID_COLS)
            ]

            grid = []
            for row_idx, row_str in enumerate(level_map):
                row_tiles = []
                for col_idx, char in enumerate(row_str):
                    if char == 'I':
                        t_type = "ice"
                    elif char == 'G':
                        t_type = "grass"
                    else:
                        t_type = "road"

                    row_tiles.append(
                        RoadTile(
                            col=col_idx,
                            row=row_idx,
                            tile_type=t_type
                        )
                    )
                grid.append(row_tiles)
        """

        self.circuit = Circuit(grid=grid)

        # Une nouvelle carte commence avec une nouvelle course.
        self.race_coordinator = None

        self.spawn_car()

    def spawn_car(self) -> None:
        """
        Appel : Depuis load_circuit().

        Crée la voiture du premier joueur.
        """
        self.car = Car(7, 1)

    def configure_race(self, checkpoints, finish_position, laps_to_win=3) -> None:
        """
        Appel : Après load_circuit(), quand les positions
        des checkpoints et de l'arrivée sont connues.

        Prépare la gestion des tours et du vainqueur.

        checkpoints : liste des cases (col, row).
        finish_position : case de la ligne d'arrivée.
        laps_to_win : nombre de tours nécessaires pour gagner.
        """
        if self.circuit is None:
            raise ValueError("Le circuit doit être chargé avant la course.")

        self.race_coordinator = RaceCoordinator(
            checkpoints=checkpoints,
            finish_position=finish_position,
            laps_to_win=laps_to_win
        )

    def update(self) -> None:
        """
        Appel : Depuis GameController.update(), à chaque frame.

        Met à jour la physique de la voiture et vérifie
        sa progression dans la course.
        """
        if (
            self.state != GameState.RACING
            or self.circuit is None
            or self.car is None
        ):
            return

        # Position actuelle de la voiture dans la grille.
        car_col = int(self.car.x // TILE_SIZE)
        car_row = int(self.car.y // TILE_SIZE)

        # Terrain situé sous la voiture avant son déplacement.
        current_tile = self.circuit.get_tile(car_col, car_row)

        if current_tile is None or current_tile.tile_type == "empty":
            # Hors de la piste : retour à la dernière position sûre.
            self.car.x = self.last_safe_x
            self.car.y = self.last_safe_y
            self.car.speed = 0.0
            return

        # Application des propriétés physiques du terrain.
        self.car.grip_factor = current_tile.grip
        self.car.traction_factor = current_tile.traction_factor
        self.car.drift_threshold = current_tile.drift_threshold
        self.car.drift_friction = current_tile.drift_friction

        # Sauvegarde de la dernière position sûre.
        self.last_safe_x = self.car.x
        self.last_safe_y = self.car.y

        # Déplacement physique de la voiture.
        self.car.update_position()

        # Vérification de la nouvelle case après le déplacement.
        new_col = int(self.car.x // TILE_SIZE)
        new_row = int(self.car.y // TILE_SIZE)

        new_tile = self.circuit.get_tile(new_col, new_row)

        # Un checkpoint ne compte que sur une case valide.
        if new_tile is None or new_tile.tile_type == "empty":
            return

        # Transmission de la position au gestionnaire de course.
        if self.race_coordinator is not None:
            self.race_coordinator.update_player_tile(
                "player1",
                (new_col, new_row)
            )
