WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.08
CAR_WIDTH = 50
CAR_HEIGHT = 30
CAR_BRAKE = 0.08      
CAR_MAX_REVERSE_SPEED = 2.0 
CAR_TURN_SPEED = 3.0
CAR_FRICTION = 0.99 # Multiplicateur (1.0 = aucune friction, 0.9 = friction très forte)


class GameState:
    MENU = "menu"
    RACING = "racing"
    CIRCUIT_SELECTION="circuit_selection"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
