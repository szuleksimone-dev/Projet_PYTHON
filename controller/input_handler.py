
# Kart-Engine v2.3

import pygame


# Touches utilisées par le joueur 1.
# Z/W pour avancer, S pour reculer ou freiner,
# Q/A pour tourner à gauche et D pour tourner à droite.
MAPPING_P1 = {
    pygame.K_z: "accelerate",
    pygame.K_w: "accelerate",
    pygame.K_s: "reverse",
    pygame.K_q: "steer_left",
    pygame.K_a: "steer_left",
    pygame.K_d: "steer_right",
    pygame.K_SPACE: "use_item"
}

# Touches utilisées par le joueur 2.
# Les flèches servent à conduire et Entrée à utiliser un objet.
MAPPING_P2 = {
    pygame.K_UP: "accelerate",
    pygame.K_DOWN: "reverse",
    pygame.K_LEFT: "steer_left",
    pygame.K_RIGHT: "steer_right",
    pygame.K_RETURN: "use_item"
}


class InputHandler:
    """
    Partie MVC : Contrôleur.

    Lit les touches du clavier pour les deux joueurs.
    Transforme les touches appuyées en actions compréhensibles
    par le contrôleur du jeu.
    """

    def __init__(self):
        """
        Initialise les commandes des deux joueurs.
        Chaque joueur possède son propre dictionnaire de touches.
        """
        self.mapping_p1 = MAPPING_P1
        self.mapping_p2 = MAPPING_P2

    def get_player_inputs(self, mapping: dict) -> dict:
        """
        Lit le clavier et renvoie les actions d'un joueur.

        Une action vaut True si sa touche est maintenue,
        et False dans le cas contraire.
        """
        keys = pygame.key.get_pressed()

        # Toutes les actions sont désactivées au départ.
        actions = {action: False for action in mapping.values()}

        # On active les actions correspondant aux touches appuyées.
        for key, action in mapping.items():
            if keys[key]:
                actions[action] = True

        return actions

    def get_inputs(self) -> dict:
        """
        Renvoie séparément les commandes des deux joueurs.

        Le contrôleur pourra ensuite appliquer les commandes
        de chaque joueur à sa propre voiture.
        """
        return {
            "player1": self.get_player_inputs(self.mapping_p1),
            "player2": self.get_player_inputs(self.mapping_p2)
        }
