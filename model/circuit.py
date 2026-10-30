from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:
    """
    Représente le circuit de course sous forme d'une grille 2D de tuiles (RoadTile).
    Gère les dimensions de la carte et fournit des méthodes sécurisées
    pour interagir avec les différentes portions de terrain.
    """
    def __init__(self,  grid: list[list[RoadTile]]):
        """
        Initialise le circuit à partir d'une grille 2D préexistante.
        Args:
            grid: Une liste de listes d'objets RoadTile représentant la carte du jeu.
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        """
        Récupère de manière sécurisée la tuile située à des coordonnées de grille données.
        Retourne l'objet RoadTile correspondant, ou None si les coordonnées sortent des limites de la carte.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
