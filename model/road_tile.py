import pygame
from constants import TILE_SIZE


class RoadTile:

    def __init__(self, col: int, row: int, tile_type: str = "road"):
        self.col = col
        self.row = row
        self.tile_type = tile_type
        
        # Définition des propriétés physiques selon le type de terrain
        if self.tile_type == "ice":
            self.grip = 0.03               # Glissade latérale extrême (adhérence quasi nulle)
            self.traction_factor = 0.4     # Mauvaise motricité : patine beaucoup à l'accélération/freinage
            self.drift_threshold = 5.0     # Dérape instantanément (dès 5° d'écart)
            self.drift_friction = 0.995    # Conserve presque toute sa vitesse en dérapant (effet patinoire)
            
        elif self.tile_type == "grass":
            self.grip = 0.07               # Adhérence latérale faible
            self.traction_factor = 0.6     # Motricité moyenne
            self.drift_threshold = 18.0    # Dérape plus facilement que sur la route
            self.drift_friction = 0.986    # Freine un tout petit peu plus que la route en dérapant, mais reste fluide

        elif self.tile_type == "terre":
            self.grip = 0.05               # Glisse un peu (entre la glace et l'herbe, style rallye)
            self.traction_factor = 0.65    # Motricité correcte mais ça patine légèrement
            self.drift_threshold = 8.0     # Dérape très facilement au braquage
            self.drift_friction = 0.99     # Conserve très bien sa vitesse en glissade

        elif self.tile_type == "empty":
            self.grip = 0.0                
            self.traction_factor = 0.0     
            self.drift_threshold = 0.0     
            self.drift_friction = 0.0     

        else: # "road"
            self.grip = 0.20               # Très bonne adhérence latérale (accroche bien)
            self.traction_factor = 1.0     # 100% de l'accélération et du freinage
            self.drift_threshold = 15.0    # Difficile de déraper (nécessite un vrai coup de volant)
            self.drift_friction = 0.96     # Frottement de référence lors d'un dérapage sur bitume

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
        elif self.tile_type == "terre":
            surface.fill((140, 85, 45))    # Marron terre
        else:
            surface.fill((80, 80, 90))     # Gris route

        pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite
