
# Kart-Engine v2.3

import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:
    """
    Vue du jeu (basée sur pygame) : responsable de l'affichage graphique.
    Elle lit l'état du modèle à chaque frame pour dessiner le circuit
    et les voitures, sans jamais modifier les données du modèle.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        """
        Redessine l'intégralité de l'écran à chaque frame
        en se basant sur les positions et l'état du modèle.
        """
        self.screen.fill(COLOR_BG)

        if model.state == GameState.MENU:
            self._draw_menu(model)

        elif model.state == GameState.CIRCUIT_SELECTION:
            self._draw_circuit_selection(model)

        elif model.state == GameState.RACING:
            self._draw_racing(model)

        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT
        )
        self.screen.blit(
            title_surf,
            title_surf.get_rect(center=(cx, 160))
        )

        options = [
            ("JOUER (Enter)", GameState.RACING),
            ("QUITTER (Escape)", None)
        ]

        for i, (label, _) in enumerate(options):
            y = 320 + i * 80

            rect = pygame.Rect(cx - 140, y - 25, 280, 50)

            pygame.draw.rect(
                self.screen, COLOR_PANEL, rect, border_radius=8
            )
            pygame.draw.rect(
                self.screen,
                COLOR_PANEL_BORDER,
                rect,
                2,
                border_radius=8
            )

            text_surf = self.font.render(
                label,
                True,
                COLOR_ACCENT if i == 0 else COLOR_TEXT
            )
            self.screen.blit(
                text_surf,
                text_surf.get_rect(center=rect.center)
            )

    def _draw_circuit_selection(self, model: GameModel) -> None:
        """
        Affiche la liste des circuits
        et met en évidence celui sélectionné.
        """
        cx = WINDOW_WIDTH // 2

        # Titre de l'écran
        title_surf = self.font.render(
            "Sélectionnez un circuit",
            True,
            COLOR_ACCENT
        )
        self.screen.blit(
            title_surf,
            title_surf.get_rect(center=(cx, 160))
        )

        # Affichage de la liste des circuits
        for i, circuit_name in enumerate(model.circuit_list):
            y = 320 + i * 80

            rect = pygame.Rect(cx - 140, y - 25, 280, 50)

            # Le circuit sélectionné change de couleur.
            if i == model.selected_circuit_idx:
                bg_color = COLOR_ACCENT
                text_color = COLOR_BG
            else:
                bg_color = COLOR_PANEL
                text_color = COLOR_TEXT

            pygame.draw.rect(
                self.screen,
                bg_color,
                rect,
                border_radius=8
            )
            pygame.draw.rect(
                self.screen,
                COLOR_PANEL_BORDER,
                rect,
                2,
                border_radius=8
            )

            text_surf = self.font.render(
                circuit_name,
                True,
                text_color
            )
            self.screen.blit(
                text_surf,
                text_surf.get_rect(center=rect.center)
            )

        # Instructions en bas de l'écran
        instructions = self.font.render(
            "Flèches: Naviguer  |  Entrée: Valider  |  Échap: Retour",
            True,
            COLOR_TEXT
        )
        self.screen.blit(
            instructions,
            instructions.get_rect(
                center=(cx, WINDOW_HEIGHT - 50)
            )
        )

    def _draw_racing(self, model: GameModel) -> None:
        """
        Partie MVC : Vue.

        Appel : Depuis draw(), pendant la course.

        Affiche le circuit et les deux voitures.
        Chaque voiture possède sa propre position
        et sa propre orientation.
        """
        if model.circuit is None:
            return

        # Affichage du circuit.
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite,
                    (col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                )

        # Affichage des voitures des deux joueurs.
        for car in (model.car, model.car2):
            if car is not None:
                surf, rect = car.get_rotated_sprite()
                self.screen.blit(surf, rect)
