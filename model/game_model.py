from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:
    """
    Partie MVC : Modèle.
    Gère les données et la logique globale du jeu (état, circuit, voitures).
    """

    def __init__(self):
        """Initialise le modèle avec l'état sur le Menu, sans circuit ni voiture."""
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        #--- POUR LA SELECTION DE CIRCUIT ---
        self.circuit_list = ["Circuit Simple", "Circuit Complexe"]
        self.selected_circuit_idx = 0

    def load_circuit(self) -> None:
        """
        Appel : Depuis le contrôleur (handle_menu_key) quand on quitte le menu.
        Partie MVC : Modèle.
        Ce qu'il fait : Génère la grille du circuit et fait apparaître la voiture.
        """
        if self.selected_circuit_idx == 0:
            # Circuit 1
            grid = [[RoadTile(col=col_idx, row=row_idx) for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
        else:
            # Circuit 2 
            grid = [[RoadTile(col=col_idx, row=row_idx) for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        """
        Appel : Depuis load_circuit().
        Partie MVC : Modèle.
        Ce qu'il fait : Instancie la voiture du joueur à une position de départ fixe.
        """
        self.car = Car(7, 1)

    def update(self) -> None:
        """
        Appel : Depuis update() du GameController à chaque frame.
        Partie MVC : Modèle.
        Ce qu'il fait : Met à jour la physique globale du jeu. Si la course est en cours, 
        calcule la nouvelle position de la voiture.
        """
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()
