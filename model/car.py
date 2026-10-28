import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_MAX_REVERSE_SPEED, CAR_BRAKE
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
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        """
        Appel : Depuis GameController.apply_input() à chaque frame si la touche avancer est maintenue.
        Partie MVC : Modèle.
        Ce qu'il fait : Applique une accélération longitudinale positive en augmentant la vitesse.
        """
        self.speed += CAR_ACCELERATION

    def update_position(self) -> None:
        """
        Appel : Depuis GameModel.update() à chaque frame de course.
        Partie MVC : Modèle.
        Ce qu'il fait : Modifie les coordonnées de la voiture sur l'axe Y en fonction de la vitesse actuelle.
        """
        self.y += self.speed

    def reverse(self) -> None:
        self.speed = max(-CAR_MAX_REVERSE_SPEED, self.speed - CAR_ACCELERATION)
        """
        Appel : Depuis GameController.apply_input() si la touche reculer est maintenue.
        Partie MVC : Modèle.
        Ce qu'il fait : Diminue la vitesse pour reculer. Utilise max() pour empêcher la voiture 
        de reculer de plus en plus vite à l'infini (limite à CAR_MAX_REVERSE_SPEED).
        """
    
    def brake(self) -> None:
        self.speed = max(0.0, self.speed - CAR_BRAKE)
        """
        Appel : Depuis GameController.apply_input() si la touche de freinage est maintenue.
        Partie MVC : Modèle.
        Ce qu'il fait : Réduit la vitesse positive jusqu'à l'arrêt. Utilise max() pour 
        garantir que la vitesse ne devienne pas négative (la voiture s'arrête bien à 0.0).
        """

    def build_sprite(self) -> pygame.Surface:
        """
        Appel : Depuis le constructeur __init__().
        Partie MVC : Modèle (bien que cela utilise pygame, spécifique à la Vue).
        Ce qu'il fait : Crée le rectangle rouge avec des bords arrondis représentant la voiture.
        """
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
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
