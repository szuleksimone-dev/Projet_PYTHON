
# Kart-Engine v2.3

"""
Configuration provisoire de la course.

Les positions sont données en coordonnées de grille :
(colonne, ligne).

Ces positions seront adaptées au circuit définitif.
"""

# Nombre de tours nécessaires pour gagner.
LAPS_TO_WIN = 3

# Position de la ligne d'arrivée.
# Elle correspond aussi au départ du joueur 1.
FINISH_POSITION = (7, 1)

# Points de passage obligatoires du circuit d'essai.
CHECKPOINTS = [
    (12, 3),
    (12, 8),
    (3, 8),
    (3, 3)
]


def get_race_config():
    """
    Retourne les paramètres nécessaires à RaceCoordinator.

    Appel : Depuis GameModel.load_circuit().

    Les checkpoints et la ligne d'arrivée sont séparés
    des propriétés physiques du terrain.
    """
    return {
        "checkpoints": CHECKPOINTS.copy(),
        "finish_position": FINISH_POSITION,
        "laps_to_win": LAPS_TO_WIN
    }
