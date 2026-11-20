
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
    les circuits, les deux voitures et la progression
    de la course jusqu'à la victoire.
    """

    def __init__(self, start_col=7, start_row=1):
        """
        Initialise le modèle avec le menu principal.

        Les voitures et le circuit sont créés
        au moment du lancement d'une course.
        """
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None

        # Positions de départ des deux joueurs.
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

        # Sélection du circuit.
        self.circuit_list = [
            "Circuit Simple",
            "Circuit Complexe"
        ]
        self.selected_circuit_idx = 0

        # Gestion des checkpoints, des tours et du vainqueur.
        self.race_coordinator: RaceCoordinator | None = None

    def load_circuit(self) -> None:
        """
        Appel : Depuis GameController après le choix du circuit.

        Crée la grille, les deux voitures et initialise
        les règles d'une nouvelle course.
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

        # Création des deux voitures.
        self.spawn_car()

        # Configuration automatique de la nouvelle course.
        race_config = get_race_config()

        self.configure_race(
            checkpoints=race_config["checkpoints"],
            finish_position=race_config["finish_position"],
            laps_to_win=race_config["laps_to_win"]
        )

    def spawn_car(self) -> None:
        """
        Appel : Depuis load_circuit().

        Crée les deux voitures à des positions différentes.
        Le joueur 2 commence une ligne plus bas.
        """
        self.car = Car(self.start_col, self.start_row)
        self.car2 = Car(self.start_col, self.start_row + 1)

        # Chaque voiture possède sa position de sécurité.
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
        Indique si un joueur a gagné.

        Cette information peut être utilisée
        par le contrôleur et par la vue.
        """
        return (
            self.race_coordinator is not None
            and self.race_coordinator.winner is not None
        )

    def _stop_cars(self) -> None:
        """
        Arrête immédiatement les deux voitures.

        Appel : Depuis update() quand un joueur gagne.
        """
        for car in (self.car, self.car2):
            if car is not None:
                car.speed = 0.0

    def update(self) -> None:
        """
        Appel : Depuis GameController.update(), à chaque frame.

        Met à jour les deux voitures pendant la course.
        Dès qu'un joueur gagne, arrête les deux voitures
        et empêche les déplacements suivants.
        """
        if self.state != GameState.RACING:
            return

        if self.circuit is None:
            return

        # Si la course est déjà terminée, aucun déplacement.
        if self.is_race_finished():
            self._stop_cars()
            return

        # Mise à jour du joueur 1.
        if self.car is not None:
            self._update_car("player1", self.car)

            # La victoire du joueur 1 arrête immédiatement la course.
            if self.is_race_finished():
                self._stop_cars()
                return

        # Mise à jour du joueur 2.
        if self.car2 is not None:
            self._update_car("player2", self.car2)

            # La victoire du joueur 2 arrête également la course.
            if self.is_race_finished():
                self._stop_cars()
                return

    def _update_car(self, player, car) -> None:
        """
        Appel : Depuis update(), pour chaque voiture.

        Applique les propriétés du terrain,
        déplace la voiture et vérifie sa progression.

        Chaque joueur possède sa propre position sûre.
        """
        # Position actuelle de la voiture dans la grille.
        car_col = int(car.x // TILE_SIZE)
        car_row = int(car.y // TILE_SIZE)

        # Terrain situé sous la voiture.
        current_tile = self.circuit.get_tile(
            car_col,
            car_row
        )

        # Sortie de piste : retour à la dernière position sûre.
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

        # Vérifie si la voiture est sortie du circuit.
        if (
            new_tile is None
            or new_tile.tile_type == "empty"
        ):
            car.x, car.y = self.last_safe_positions[player]
            car.speed = 0.0
            return

        # Enregistre les checkpoints et les tours du joueur.
        if self.race_coordinator is not None:
            self.race_coordinator.update_player_tile(
                player,
                (new_col, new_row)
            )
