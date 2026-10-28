import pygame
from controller.game_controller import GameController


def main():
    """
    Appel : Au lancement du script.
    Partie MVC : Initialisation.
    Ce qu'il fait : Démarre pygame, configure la fenêtre, instancie le contrôleur et lance la boucle principale.
    """
    pygame.init()
    pygame.display.set_caption("Projet Python - Jeu de course 2D")

    controller = GameController()
    controller.run()

    pygame.quit()


if __name__ == "__main__":
    main()
