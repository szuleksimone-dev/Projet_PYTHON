from constants import GameState, GRID_ROWS, GRID_COLS, TILE_SIZE
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.circuit_maps import CIRCUIT_1, CIRCUIT_2


class GameModel:
    """
    Partie MVC : Modèle.
    Gère les données et la logique globale du jeu (état, circuit, voitures).
    """

    def __init__(self,start_col=7, start_row=1):
        """Initialise le modèle avec l'état sur le Menu, sans circuit ni voiture."""
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None
        self.last_safe_x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.last_safe_y = start_row * TILE_SIZE + TILE_SIZE // 2
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
            level_map = CIRCUIT_1
        else :
            level_map = CIRCUIT_2

        grid = []
        for row_idx, row_str in enumerate(level_map):
            row_tiles = []
            for col_idx, char in enumerate(row_str):
                # On traduit la lettre en type de terrain
                if char == 'I':
                    t_type = "ice"
                elif char == 'G':
                    t_type = "grass"
                elif char == 'T':
                    t_type = "terre"
                elif char == 'F':
                    t_type = "fence"
                else:
                    t_type = "road"

                row_tiles.append(
                    RoadTile(col=col_idx, row=row_idx, tile_type=t_type)
                )
            grid.append(row_tiles)

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
        
        if current_tile is None or current_tile.tile_type == "empty":
            # Hors de la grille : Téléportation immédiate, vitesse à 0 et on stoppe net
            self.car.x = self.last_safe_x
            self.car.y = self.last_safe_y
            self.car.speed = 0.0
            return  # On sort de la fonction pour éviter que la voiture ne bouge à nouveau dans la même frame

        else:
            # Si on est sur une tuile valide, on applique les propriétés physiques
            self.car.grip_factor = current_tile.grip
            self.car.traction_factor = current_tile.traction_factor
            self.car.drift_threshold = current_tile.drift_threshold
            self.car.drift_friction = current_tile.drift_friction
            
            # Et on sauvegarde ce point comme le dernier point sain
            self.last_safe_x = self.car.x
            self.last_safe_y = self.car.y

        # Mettre à jour la position physique de la voiture
        self.car.update_position()

        # Vérifier la collision avec une barrière après le déplacement
        new_col = int(self.car.x // TILE_SIZE)
        new_row = int(self.car.y // TILE_SIZE)
        new_tile = self.circuit.get_tile(new_col, new_row)

        if new_tile is not None and new_tile.tile_type == "fence":
            # Revenir à la position précédente et arrêter la voiture
            self.car.x = self.last_safe_x
            self.car.y = self.last_safe_y
            self.car.speed = 0.0
