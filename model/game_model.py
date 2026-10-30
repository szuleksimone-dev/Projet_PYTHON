from constants import GameState, GRID_ROWS, GRID_COLS, TILE_SIZE
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
            grid = [
                [RoadTile(col=col_idx, row=row_idx, tile_type="road") for col_idx in range(GRID_COLS)] 
                for row_idx in range(GRID_ROWS)
            ]
        else:
            grid = [
                [RoadTile(col=col_idx, row=row_idx, tile_type="ice") for col_idx in range(GRID_COLS)] 
                for row_idx in range(GRID_ROWS)
            ]
        """level_map = [
                "RRRRRRRRRRRRRRRR",
                "RIIIRRRRRRRRRRRR",
                "RIIIRRRRRRRRRRRR",
                "RRRRRRGGGGGRRRRR",
                "RRRRRRGGGGGRRRRR",
                "RRRRRRRRRRRRRRRR",
                # ... (autant de lignes que GRID_ROWS, et de caractères que GRID_COLS)
            ]

            grid = []
            for row_idx, row_str in enumerate(level_map):
                row_tiles = []
                for col_idx, char in enumerate(row_str):
                    # On traduit la lettre en type de terrain
                    if char == 'I':
                        t_type = "ice"
                    elif char == 'G':
                        t_type = "grass"
                    else:
                        t_type = "road"
                    
                    row_tiles.append(RoadTile(col=col_idx, row=row_idx, tile_type=t_type))
                grid.append(row_tiles) -> POUR CIRCUIT ELABORE """
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
        # Trouver quelle tuile est sous les roues de la voiture
        # On convertit les coordonnées pixels (x, y) en coordonnées de grille (col, row)
        car_col = int(self.car.x // TILE_SIZE)
        car_row = int(self.car.y // TILE_SIZE)

        # Récupérer la tuile correspondante dans le circuit (si on est dans les limites)
        current_tile = self.circuit.get_tile(car_col, car_row)
        
        if current_tile:
            # Mettre à jour dynamiquement le grip de la voiture 
            self.car.grip_factor = current_tile.grip

        # Mettre à jour la position physique de la voiture
        self.car.update_position()
