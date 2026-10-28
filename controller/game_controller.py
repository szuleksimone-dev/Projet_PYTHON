import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """
    Partie MVC : Contrôleur.
    Ce qu'il fait : Gère la boucle de jeu principale et fait l'interface 
    entre les entrées clavier, la mise à jour du modèle et l'affichage.
    """

    def __init__(self):
        """
        Appel : Depuis main.py au lancement du jeu.
        Partie MVC : Contrôleur.
        Ce qu'il fait : Initialise la fenêtre d'affichage, l'horloge, le modèle, la vue et le gestionnaire d'entrées.
        """
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        """
        Appel : Depuis main.py après l'initialisation.
        Partie MVC : Contrôleur.
        Ce qu'il fait : Exécute la boucle principale du jeu (cadencée à 60 FPS).
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """
        Appel : Depuis run() à chaque frame.
        Partie MVC : Contrôleur.
        Ce qu'il fait : Lit les événements de pygame (fermeture de fenêtre, appui ponctuel sur une touche).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """
        Appel : Depuis handle_events() lorsqu'une touche est pressée (événement ponctuel).
        Partie MVC : Contrôleur.
        Ce qu'il fait : Vérifie l'état actuel du jeu et redirige la touche pressée 
        vers la méthode de gestion appropriée (ex: menu).
        """
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CIRCUIT_SELECTION:
            self.handle_circuit_selection_key(key)

    def handle_circuit_selection_key(self, key: int) -> None:
        """
        Appel : Depuis handle_keydown() si le jeu est sur l'écran de choix du circuit.
        Partie MVC : Contrôleur.
        Ce qu'il fait : Gère la sélection du circuit avec les flèches, valide avec Entrée, ou annule avec Échap.
        """
        # On récupère le nombre total de circuits pour ne pas dépasser
        nb_circuits = len(self.model.circuit_list)

        if key == pygame.K_RIGHT or key == pygame.K_DOWN:
            # On passe au circuit suivant (le modulo permet de boucler vers le 1er)
            self.model.selected_circuit_idx = (self.model.selected_circuit_idx + 1) % nb_circuits
            
        elif key == pygame.K_LEFT or key == pygame.K_UP:
            # On passe au circuit précédent
            self.model.selected_circuit_idx = (self.model.selected_circuit_idx - 1) % nb_circuits
            
        elif key == pygame.K_RETURN:
            # On a choisi notre circuit, on le charge et on lance la course !
            self.model.load_circuit()
            self.model.state = GameState.RACING
            
        elif key == pygame.K_ESCAPE:
            # On annule et on fait un retour en arrière vers le menu
            self.model.state = GameState.MENU

    def handle_menu_key(self, key: int) -> None:
        """
        Appel : Depuis handle_keydown() lorsque le jeu est sur l'écran de menu.
        Partie MVC : Contrôleur.
        Ce qu'il fait : Interprète les touches du menu (Entrée pour passer à la selection du circuit, 
        Échap pour quitter).
        """
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECTION
        elif key == pygame.K_ESCAPE:
            self.quit()

    def update(self) -> None:
        """
        Appel : Depuis la boucle principale run() à chaque frame.
        Partie MVC : Contrôleur.
        Ce qu'il fait : Récupère les entrées du joueur, les applique à la voiture, 
        puis demande au modèle de mettre à jour la physique globale du jeu.
        """
        if self.model.state != GameState.RACING:
            return

        p1_input = self.input_handler.get_inputs()
        car = self.model.car
        self.apply_input(car, p1_input)
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        """
        Appel : Depuis update().
        Partie MVC : Contrôleur vers Modèle.
        Ce qu'il fait : Traduit les entrées du dictionnaire player_input en appels 
        de méthodes spécifiques sur l'objet car (accelerate, reverse, brake).
        """
        if player_input['accelerate']:
            car.accelerate()
        if player_input["reverse"]:
            car.reverse()
        if player_input["brake"]:
            car.brake()
        
    def render(self) -> None:
        """
        Appel : Depuis la boucle principale run() à chaque frame.
        Partie MVC : Contrôleur vers Vue.
        Ce qu'il fait : Ordonne à la vue de dessiner l'état actuel du modèle.
        """
        self.view.draw(self.model)

    def quit(self) -> None:
        """Ferme proprement pygame et quitte le programme."""
        self.running = False
        pygame.quit()
        sys.exit()
