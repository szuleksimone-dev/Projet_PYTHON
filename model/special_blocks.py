
# Kart-Engine v2.3


class SpecialBlocks:
    """
    Partie MVC : Modèle - Logique de course.

    Gère les cases spéciales du circuit :
    les blocs de départ et les zones de boost.

    Les positions sont données par la configuration
    du circuit, sans modifier la physique de Car.
    """

    def __init__(
        self,
        boost_positions,
        start_positions,
        boost_amount=2.0,
        max_boost_speed=9.0
    ):
        """
        Initialise les blocs spéciaux.

        boost_positions : cases qui donnent un boost.
        start_positions : case de départ de chaque joueur.

        Les valeurs du boost sont provisoires.
        """
        self.boost_positions = set(boost_positions)
        self.start_positions = dict(start_positions)

        self.boost_amount = boost_amount
        self.max_boost_speed = max_boost_speed

        # Dernière case visitée par chaque joueur.
        self.last_positions = {
            player: None
            for player in self.start_positions
        }

    def get_start_position(self, player):
        """
        Retourne la case de départ d'un joueur.
        """
        if player not in self.start_positions:
            raise ValueError("Joueur inconnu.")

        return self.start_positions[player]

    def update_player(self, player, position, car):
        """
        Vérifie si le joueur entre sur une case de boost.

        Le boost est déclenché une seule fois
        à l'entrée sur la case.

        Retourne True si un boost est appliqué.
        """
        if player not in self.last_positions:
            raise ValueError("Joueur inconnu.")

        # Pas de nouvel effet si la voiture reste
        # sur la même case.
        if self.last_positions[player] == position:
            return False

        self.last_positions[player] = position

        # Une case normale ne donne aucun boost.
        if position not in self.boost_positions:
            return False

        # Pas de boost si la voiture recule.
        if car.speed < 0:
            return False

        # Augmente la vitesse sans dépasser la limite.
        car.speed = min(
            self.max_boost_speed,
            car.speed + self.boost_amount
        )

        return True
