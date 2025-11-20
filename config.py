"""Game configuration and constants"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Raycasting settings
FOV = 60  # Field of view in degrees
HALF_FOV = FOV / 2
NUM_RAYS = 400
MAX_DEPTH = 20
DELTA_ANGLE = FOV / NUM_RAYS

# Player settings
PLAYER_SPEED = 0.05
PLAYER_ROT_SPEED = 0.03
PLAYER_SIZE = 0.2

# Map settings
TILE_SIZE = 1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 20)
GREEN = (20, 220, 20)
BLUE = (20, 20, 220)
YELLOW = (220, 220, 20)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
ORANGE = (255, 140, 0)

# Wall colors based on distance
WALL_COLORS = [
    (100, 100, 100),  # Far
    (120, 120, 120),
    (140, 140, 140),
    (160, 160, 160),
    (180, 180, 180),  # Close
]

# Game settings
PLAYER_HEALTH = 100
WEAPON_DAMAGE = 25
WEAPON_FIRE_RATE = 0.5  # seconds between shots
ENEMY_HEALTH = 50
