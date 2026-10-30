import pygame
from constants import TILE_SIZE


class RoadTile:

    def __init__(self, col: int, row: int, tile_type: str = "road"):
        self.col = col
        self.row = row
        self.tile_type = tile_type
        # Définition du grip selon le type de terrain
        if self.tile_type == "ice":
            self.grip = 0.03  # Glissade extrême
        elif self.tile_type == "grass":
            self.grip = 0.08  # Adhérence moyenne
        else:
            self.grip = 0.20  # Route normale (grip élevé)
        self.sprite: pygame.Surface | None = None

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        # Couleur différente selon le type pour tester visuellement 
        if self.tile_type == "ice":
            surface.fill((200, 220, 255))  # Bleu glacier
        elif self.tile_type == "grass":
            surface.fill((50, 150, 50))    # Vert herbe
        else:
            surface.fill((80, 80, 90))     # Gris route
        pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite
