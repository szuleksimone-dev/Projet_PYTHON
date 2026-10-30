import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_MAX_REVERSE_SPEED, CAR_BRAKE, CAR_TURN_SPEED, CAR_FRICTION
)


class Car:
    """
    Partie MVC : Modèle.
    Ce qu'il fait : Représente une voiture de course avec ses attributs physiques 
    (position, vitesse, orientation) et sa dynamique de déplacement.
    """
    def __init__(self, start_col: int, start_row: int):
        """
        Appel : Depuis GameModel.spawn_car() lors du chargement du circuit.
        Partie MVC : Modèle.
        Ce qu'il fait : Initialise les coordonnées de départ de la voiture, 
        sa vitesse (à l'arrêt), son angle et construit son image (sprite).
        """
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0 # L'avant de la voiture 
        self.movement_angle: float = 0.0 # La vraie direction du déplacement (physique/drift)
        self.grip_factor = 0.05 # A MODIFIER avec valeur adaptée en fonction du terrain
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        """
        Appel : Depuis GameController.apply_input() à chaque frame si la touche avancer est maintenue.
        Partie MVC : Modèle.
        Ce qu'il fait : Applique une accélération longitudinale positive en augmentant la vitesse.
        """
        self.speed += CAR_ACCELERATION
    
    def steer_left(self) -> None:
        """Augmente l'angle de braquage (tourne à gauche)."""
        self.angle -= CAR_TURN_SPEED

    def steer_right(self) -> None:
        """Diminue l'angle de braquage (tourne à droite)."""
        self.angle += CAR_TURN_SPEED

    def update_position(self) -> None:
        """
        Appel : Depuis GameModel.update() à chaque frame de course.
        Partie MVC : Modèle.
        Ce qu'il fait : Modifie les coordonnées de la voiture en 2D avec formules trigonométriques et applique la friction de l'air.
        """
        # On applique la friction de l'air pour ralentir la voiture naturellement
        self.speed *= CAR_FRICTION
        # Pour éviter que l'ordinateur ne calcule des micro-vitesses infinies (ex: 0.0000001),
        # on force l'arrêt complet si la vitesse est minuscule.
        if abs(self.speed) < 0.01:
            self.speed = 0.0
        
        # Gestion du dérapage (Drift façon Trackmania)
        # Pour l'instant, on met une valeur fixe (ex: 0.15) -> Il faudra changer le grip en focntion du milieu
        angle_diff = self.angle - self.movement_angle
        # Sécurité mathématique pour éviter les bugs à 360 degrés
        angle_diff = (angle_diff + 180) % 360 - 180 
        
        self.movement_angle += angle_diff * self.grip_factor

        rad = math.radians(self.movement_angle)
        self.y += self.speed * math.sin(rad)
        self.x += self.speed * math.cos(rad)

    def reverse(self) -> None:
        """
        Appel : Depuis GameController.apply_input() si la touche reculer est maintenue.
        Partie MVC : Modèle.
        Ce qu'il fait : Diminue la vitesse pour reculer. Utilise max() pour empêcher la voiture 
        de reculer de plus en plus vite à l'infini (limite à CAR_MAX_REVERSE_SPEED).
        """
        self.speed = max(-CAR_MAX_REVERSE_SPEED, self.speed - CAR_ACCELERATION)
        
    
    def brake(self) -> None:
        """
        Appel : Depuis GameController.apply_input() si la touche de freinage est maintenue.
        Partie MVC : Modèle.
        Ce qu'il fait : Réduit la vitesse positive jusqu'à l'arrêt. Utilise max() pour 
        garantir que la vitesse ne devienne pas négative (la voiture s'arrête bien à 0.0).
        """
        if self.speed>0:
            self.speed = max(0.0, self.speed - CAR_BRAKE)
        elif self.speed<0:
            self.speed = min(0.0, self.speed + CAR_BRAKE)
       

    def build_sprite(self) -> pygame.Surface:
        """
        Appel : Depuis le constructeur __init__().
        Partie MVC : Modèle (bien que cela utilise pygame, spécifique à la Vue).
        Ce qu'il fait : Crée le rectangle rouge avec des bords arrondis représentant la voiture.
        """
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        # Le corps de la voiture (Rouge)
        pygame.draw.rect(surf, (255, 165, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        # Le pare-brise (Bleu clair) pour repérer l'avant
        pygame.draw.rect(surf, (0, 200, 255), (CAR_WIDTH - 8, 2, 8, CAR_HEIGHT - 4))
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """
        Appel : Depuis GameView.draw() (la Vue) à chaque frame.
        Partie MVC : Modèle vers Vue.
        Ce qu'il fait : Calcule la rotation de l'image de la voiture selon son angle actuel 
        et renvoie l'image tournée avec son rectangle de positionnement pour l'affichage.
        """
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
