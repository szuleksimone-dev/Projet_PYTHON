
# Kart-Engine v2.3


class RaceCoordinator:
    """
    Partie MVC : Modèle.

    Gère les checkpoints, les tours et le vainqueur.
    Chaque joueur possède sa propre progression.
    """

    def __init__(self, checkpoints, finish_position, laps_to_win=3):
        """
        Initialise les règles de la course.

        checkpoints : positions des points de passage.
        finish_position : position de la ligne d'arrivée.
        laps_to_win : nombre de tours pour gagner.
        """
        if laps_to_win < 1:
            raise ValueError("Le nombre de tours doit être positif.")

        self.checkpoints = set(checkpoints)
        self.finish_position = finish_position
        self.laps_to_win = laps_to_win

        # Nombre de tours de chaque joueur.
        self.laps = {"player1": 0, "player2": 0}

        # Checkpoints déjà validés pendant le tour actuel.
        self.visited = {"player1": set(), "player2": set()}

        # Dernière case visitée par chaque voiture.
        self.last_tile = {"player1": None, "player2": None}

        # Aucun joueur n'a gagné au début.
        self.winner = None

    def update_player_tile(self, player, position):
        """
        Vérifie la case dans laquelle entre un joueur.

        Un tour est validé si tous les checkpoints
        ont été visités avant la ligne d'arrivée.
        """
        if player not in self.laps:
            raise ValueError("Joueur inconnu.")

        # On arrête le comptage après la victoire.
        if self.winner is not None:
            return

        # Évite de compter plusieurs fois la même case.
        if self.last_tile[player] == position:
            return

        self.last_tile[player] = position

        # Enregistre le passage sur un checkpoint.
        if position in self.checkpoints:
            self.visited[player].add(position)

        # Vérifie le passage sur la ligne d'arrivée.
        if position == self.finish_position:

            # Tous les checkpoints sont obligatoires.
            if self.visited[player] == self.checkpoints:
                self.laps[player] += 1

                # Prépare le tour suivant.
                self.visited[player].clear()

                # Vérifie si le joueur a gagné.
                if self.laps[player] >= self.laps_to_win:
                    self.winner = player
