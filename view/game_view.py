
# Kart-Engine v2.3

import pygame

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT,
    COLOR_PANEL, COLOR_PANEL_BORDER, GameState
)

from model.game_model import GameModel


class GameView:
    """
    Partie MVC : Vue.

    Affiche le menu, les circuits, les checkpoints,
    la ligne d'arrivée et les deux voitures.

    La vue ne modifie pas les données du modèle.
    """

    def __init__(self, screen: pygame.Surface):
        """
        Initialise l'écran et les polices du jeu.
        """
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont(
            "Arial", 18, bold=True
        )

    def draw(self, model: GameModel) -> None:
        """
        Appel : Depuis GameController.render().

        Affiche l'écran selon l'état du jeu.
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
        """
        Affiche les options du menu principal.
        """
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
                self.screen, COLOR_PANEL,
                rect, border_radius=8
            )
            pygame.draw.rect(
                self.screen, COLOR_PANEL_BORDER,
                rect, 2, border_radius=8
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
        Affiche les circuits et met en évidence
        le circuit sélectionné.
        """
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Sélectionnez un circuit",
            True,
            COLOR_ACCENT
        )
        self.screen.blit(
            title_surf,
            title_surf.get_rect(center=(cx, 160))
        )

        for i, circuit_name in enumerate(model.circuit_list):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)

            if i == model.selected_circuit_idx:
                bg_color = COLOR_ACCENT
                text_color = COLOR_BG
            else:
                bg_color = COLOR_PANEL
                text_color = COLOR_TEXT

            pygame.draw.rect(
                self.screen, bg_color,
                rect, border_radius=8
            )
            pygame.draw.rect(
                self.screen, COLOR_PANEL_BORDER,
                rect, 2, border_radius=8
            )

            text_surf = self.font.render(
                circuit_name, True, text_color
            )
            self.screen.blit(
                text_surf,
                text_surf.get_rect(center=rect.center)
            )

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
        Appel : Depuis draw(), pendant la course.

        Affiche le terrain, les checkpoints,
        la ligne d'arrivée et les deux voitures.
        """
        if model.circuit is None:
            return

        # Dessine les cases du circuit.
        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite,
                    (col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                )

        # Dessine les points de passage et l'arrivée.
        self._draw_race_markers(model)

        # Dessine les deux voitures au-dessus du circuit.
        for car in (model.car, model.car2):
            if car is not None:
                surf, rect = car.get_rotated_sprite()
                self.screen.blit(surf, rect)

    def _draw_race_markers(self, model: GameModel) -> None:
        """
        Appel : Depuis _draw_racing().

        Dessine les checkpoints en jaune et
        la ligne d'arrivée en damier.

        Les positions viennent de RaceCoordinator.
        Cette méthode ne modifie pas les règles de course.
        """
        race = model.race_coordinator

        if race is None:
            return

        # Affichage des checkpoints.
        for col, row in race.checkpoints:
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            rect = pygame.Rect(
                x + 4, y + 4,
                TILE_SIZE - 8, TILE_SIZE - 8
            )

            # Contour jaune autour de chaque checkpoint.
            pygame.draw.rect(
                self.screen,
                (255, 220, 0),
                rect,
                4,
                border_radius=8
            )

            # Texte CP au centre de la case.
            label = self.small_font.render(
                "CP", True, (255, 220, 0)
            )
            self.screen.blit(
                label,
                label.get_rect(
                    center=(
                        x + TILE_SIZE // 2,
                        y + TILE_SIZE // 2
                    )
                )
            )

        # Affichage de la ligne d'arrivée.
        col, row = race.finish_position

        x = col * TILE_SIZE
        y = row * TILE_SIZE

        # Damier noir et blanc au centre de la case.
        case_size = TILE_SIZE // 8

        for line in range(2):
            for column in range(8):
                color = (
                    (255, 255, 255)
                    if (line + column) % 2 == 0
                    else (20, 20, 20)
                )

                square = pygame.Rect(
                    x + column * case_size,
                    y + TILE_SIZE // 2 - case_size
                    + line * case_size,
                    case_size,
                    case_size
                )

                pygame.draw.rect(
                    self.screen,
                    color,
                    square
                )

        # Contour blanc pour identifier l'arrivée.
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(x, y, TILE_SIZE, TILE_SIZE),
            3
        )
