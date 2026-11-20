
# Kart-Engine v2.3

"""
Configuration provisoire de la course.

Les positions seront adaptées aux circuits
définitifs créés par le membre 3.
"""

# Nombre de tours nécessaires pour gagner.
LAPS_TO_WIN = 3

# Position de la ligne d'arrivée.
FINISH_POSITION = (7, 1)

# Positions provisoires des checkpoints.
CHECKPOINTS = [
    (12, 3),
    (12, 8),
    (3, 8),
    (3, 3)
]

# Positions provisoires des blocs de boost.
BOOST_POSITIONS = [
    (5, 3),
    (10, 7)
]


def get_race_config():
    """
    Retourne les paramètres de la course.

    Une copie des listes évite de modifier
    la configuration originale.
    """
    return {
        "checkpoints": CHECKPOINTS.copy(),
        "finish_position": FINISH_POSITION,
        "laps_to_win": LAPS_TO_WIN,
        "boost_positions": BOOST_POSITIONS.copy()
    }
