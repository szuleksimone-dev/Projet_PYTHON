import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:   "reverse",
    pygame.K_SPACE:  "brake",
}
"""On associe deux touches vers des noms d'action puis les noms d'action vers les méthodes implémentées dans car.py """


class InputHandler:
    """
    Partie MVC : Contrôleur (Sous-module).
    Ce qu'il fait : Gère les entrées clavier en "continu" (touches maintenues enfoncées).
    Contrairement aux événements ponctuels gérés par handle_events() (comme naviguer dans un menu), 
    cette classe est conçue pour le pilotage : elle vérifie à chaque frame quelles touches 
    sont physiquement écrasées par les doigts du joueur.
    """

    def __init__(self):
        """
        Appel : Depuis l'initialisation du GameController.
        Ce qu'il fait : Récupère le dictionnaire MAPPING pour l'utiliser lors de la détection.
        """
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        """
        Appel : Depuis GameController.update() à chaque frame pendant la course.
        Ce qu'il fait : Prend une "photo" de tout le clavier avec pygame.key.get_pressed().
        Si la touche configurée dans le mapping est enfoncée à cet instant précis, 
        l'action correspondante passe à True dans le dictionnaire renvoyé.
        """
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
