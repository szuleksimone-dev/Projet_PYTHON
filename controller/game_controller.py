
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
        """
        Initialise les éléments nécessaires au jeu.
        """
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        self.clock = pygame.time.Clock()

        # Modèle : données et physique des deux voitures.
        self.model = GameModel()

        # Vue : affichage du jeu.
        self.view = GameView(self.screen)

        # Commandes clavier des deux joueurs.
        self.input_handler = InputHandler()

        self.running = True

    def run(self) -> None:
        """
        Exécute la boucle principale du jeu.
        """
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
        """
        Gère les commandes du menu principal.
        """
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
            self.model.selected_circuit_idx = (
                self.model.selected_circuit_idx + 1
            ) % nb_circuits

        elif key == pygame.K_LEFT or key == pygame.K_UP:
            self.model.selected_circuit_idx = (
                self.model.selected_circuit_idx - 1
            ) % nb_circuits

        elif key == pygame.K_RETURN:
            # Charge le circuit et démarre une nouvelle course.
            self.model.load_circuit()
            self.model.state = GameState.RACING

        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self) -> None:
        """
        Appel : À chaque frame de la boucle principale.

        Lit les commandes des deux joueurs et les applique
        à leurs voitures pendant la course.

        Après la victoire d'un joueur, les commandes
        ne sont plus appliquées.
        """
        # Les voitures ne bougent que pendant une course.
        if self.model.state != GameState.RACING:
            return

        # Vérifie si un joueur a déjà gagné.
        race = getattr(self.model, "race_coordinator", None)

        if race is not None and race.winner is not None:
            # La course est terminée :
            # aucune nouvelle commande n'est appliquée.
            return

        # Lecture des commandes des deux joueurs.
        inputs = self.input_handler.get_inputs()

        # Le joueur 1 contrôle la première voiture.
        if self.model.car is not None:
            self.apply_input(
                self.model.car,
                inputs["player1"]
            )

        # Le joueur 2 contrôle la deuxième voiture.
        if self.model.car2 is not None:
            self.apply_input(
                self.model.car2,
                inputs["player2"]
            )

        # Mise à jour de la physique des deux voitures.
        # Le modèle vérifie aussi la victoire.
        self.model.update()

    def apply_input(self, car, player_input: dict) -> None:
        """
        Applique les commandes d'un joueur à sa voiture.

        Cette méthode est commune aux deux joueurs :
        seule la voiture et les commandes changent.
        """
        if player_input["accelerate"]:
            car.accelerate()

        if player_input["reverse"]:
            # Ralentit la voiture puis permet de reculer.
            car.reverse()

        if player_input["steer_left"]:
            car.steer_left()

        if player_input["steer_right"]:
            car.steer_right()

        # L'action use_item sera connectée plus tard
        # si le système d'objets est ajouté.

    def render(self) -> None:
        """
        Demande à la vue d'afficher le jeu.
        """
        self.view.draw(self.model)

    def quit(self) -> None:
        """
        Ferme la fenêtre et arrête le programme.
        """
        self.running = False
        pygame.quit()
        sys.exit()
