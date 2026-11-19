
# Kart-Engine v2.3

import pygame
import sys

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """
    Partie MVC : Contrôleur.

    Gère les événements du clavier, les états du jeu
    et la boucle principale.

    Il fait le lien entre le modèle (logique du jeu)
    et la vue (affichage).
    """

    def __init__(self):
        """Initialise les éléments nécessaires au jeu."""
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        # Modèle : contient les données et la physique du jeu.
        self.model = GameModel()

        # Vue : affiche le jeu à l'écran.
        self.view = GameView(self.screen)

        # Gestion des commandes des deux joueurs.
        self.input_handler = InputHandler()

        self.running = True

    def run(self) -> None:
        """Exécute la boucle principale du jeu."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """
        Traite les événements ponctuels :
        fermeture de fenêtre et touches pressées.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """
        Transmet la touche pressée à la méthode
        correspondant à l'état actuel du jeu.
        """
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)

        elif state == GameState.CIRCUIT_SELECTION:
            self.handle_circuit_selection_key(key)

    def handle_menu_key(self, key: int) -> None:
        """Gère les commandes du menu principal."""
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECTION

        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_circuit_selection_key(self, key: int) -> None:
        """
        Permet de choisir un circuit avec les flèches.

        Entrée : confirmer le choix et démarrer la course.
        Échap : revenir au menu principal.
        """
        nb_circuits = len(self.model.circuit_list)

        if key == pygame.K_RIGHT or key == pygame.K_DOWN:
            # Sélection du circuit suivant.
            self.model.selected_circuit_idx = (
                self.model.selected_circuit_idx + 1
            ) % nb_circuits

        elif key == pygame.K_LEFT or key == pygame.K_UP:
            # Sélection du circuit précédent.
            self.model.selected_circuit_idx = (
                self.model.selected_circuit_idx - 1
            ) % nb_circuits

        elif key == pygame.K_RETURN:
            # Chargement du circuit et début de la course.
            self.model.load_circuit()
            self.model.state = GameState.RACING

        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self) -> None:
        """
        Met à jour le jeu pendant une course.

        Récupère les commandes des deux joueurs.
        Pour le moment, le modèle contient une seule voiture.
        Seules les commandes du joueur 1 sont appliquées.
        """
        if self.model.state != GameState.RACING:
            return

        # Lecture des commandes des deux joueurs.
        inputs = self.input_handler.get_inputs()

        # Récupération de la voiture actuelle.
        car = self.model.car

        if car is not None:
            # Le joueur 1 contrôle la voiture existante.
            self.apply_input(car, inputs["player1"])

        # Mise à jour de la physique de la voiture.
        self.model.update()

    def apply_input(self, car, player_input: dict) -> None:
        """
        Applique les commandes du joueur à sa voiture.

        Le contrôleur traduit les actions du clavier
        en appels aux méthodes de la classe Car.
        """
        if player_input["accelerate"]:
            car.accelerate()

        if player_input["reverse"]:
            # La commande de recul permet aussi de ralentir.
            car.reverse()

        if player_input["steer_left"]:
            car.steer_left()

        if player_input["steer_right"]:
            car.steer_right()

        # L'action use_item sera connectée quand
        # le système d'objets sera disponible.

    def render(self) -> None:
        """Demande à la vue d'afficher le jeu."""
        self.view.draw(self.model)

    def quit(self) -> None:
        """Ferme la fenêtre et arrête le programme."""
        self.running = False
        pygame.quit()
        sys.exit()
