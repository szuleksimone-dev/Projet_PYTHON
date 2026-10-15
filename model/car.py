import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_MAX_REVERSE_SPEED, CAR_BRAKE
)


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION

    def update_position(self) -> None:
        self.y += self.speed

    def reverse(self) -> None:
        self.speed = max(-CAR_MAX_REVERSE_SPEED, self.speed - CAR_ACCELERATION)
        """Nouvelle methode implémentée : on utilise un max() pour que la voiture ne recule pas de plus en plus vite à l'infini"""
    
    def brake(self) -> None:
        self.speed = max(0.0, self.speed - CAR_BRAKE)
        """Nouvelle methode implémentée : on utilise un max() pour que la voiture ne recule pas  à l'infini et s'arrête bien"""

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
