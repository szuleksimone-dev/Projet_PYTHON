# Kart-Engine v2.3


class RaceCoordinator:
    """
    Partie MVC : Modèle.

    Gère les checkpoints, les tours et le vainqueur.
    Les checkpoints doivent être validés dans l'ordre.
    Chaque joueur possède sa propre progression.
    """

    def __init__(self, checkpoints, finish_position, laps_to_win=3):
        """
        Initialise les règles de la course.

        checkpoints : liste ordonnée des points de passage.
        finish_position : position de la ligne d'arrivée.
        laps_to_win : nombre de tours nécessaires pour gagner.
        """
        if laps_to_win < 1:
            raise ValueError("Le nombre de tours doit être positif.")

        # Une liste conserve l'ordre des checkpoints.
        # Le premier élément correspond à CP1.
        self.checkpoints = list(checkpoints)

        self.finish_position = finish_position
        self.laps_to_win = laps_to_win

        # Nombre de tours de chaque joueur.
        self.laps = {
            "player1": 0,
            "player2": 0
        }

        # Checkpoints validés pendant le tour actuel.
        self.visited = {
            "player1": set(),
            "player2": set()
        }

        # Indice du prochain checkpoint attendu.
        # 0 = CP1, 1 = CP2, 2 = CP3, etc.
        self.next_checkpoint_index = {
            "player1": 0,
            "player2": 0
        }

        # Dernière case visitée par chaque voiture.
        self.last_tile = {
            "player1": None,
            "player2": None
        }

        # Aucun joueur n'a gagné au début.
        self.winner = None

    def update_player_tile(self, player, position):
        """
        Vérifie la case dans laquelle entre un joueur.

        Les checkpoints sont validés dans l'ordre :
        CP1, CP2, CP3, etc.

        Un tour est validé uniquement si tous les
        checkpoints ont été franchis dans le bon ordre
        avant le passage sur la ligne d'arrivée.
        """
        if player not in self.laps:
            raise ValueError("Joueur inconnu.")

        # Aucun comptage après la victoire.
        if self.winner is not None:
            return

        # Évite de traiter plusieurs fois la même case.
        if self.last_tile[player] == position:
            return

        self.last_tile[player] = position

        # Prochain checkpoint à valider.
        index = self.next_checkpoint_index[player]

        # Vérifie si des checkpoints restent à valider.
        if index < len(self.checkpoints):

            expected_checkpoint = self.checkpoints[index]

            # Seul le prochain checkpoint est accepté.
            if position == expected_checkpoint:

                self.visited[player].add(position)

                # Passe au checkpoint suivant.
                self.next_checkpoint_index[player] += 1

        # Vérifie le passage sur la ligne d'arrivée.
        if position == self.finish_position:

            # Tous les checkpoints doivent être validés.
            if (
                self.next_checkpoint_index[player]
                == len(self.checkpoints)
            ):
                # Un tour supplémentaire.
                self.laps[player] += 1

                # Prépare le tour suivant.
                self.visited[player].clear()
                self.next_checkpoint_index[player] = 0

                # Vérifie si le joueur a gagné.
                if self.laps[player] >= self.laps_to_win:
                    self.winner = player