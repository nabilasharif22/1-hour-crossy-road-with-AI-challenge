# settings.py

# Screen dimensions
WIDTH = 600
HEIGHT = 600
FPS = 60

# Grid setup (The game moves in a grid-like pattern)
TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)   # Frog color
GRAY = (128, 128, 128)  # Road color
BLUE = (65, 105, 225)   # River color
RED = (200, 50, 50)     # Car color
BROWN = (139, 69, 19)   # Log color

# Game Areas (Y-coordinates for where road and river start)
# We calculate these based on tile size so they fit the grid
RIVER_TOP = 2 * TILE_SIZE
RIVER_BOTTOM = 7 * TILE_SIZE
ROAD_TOP = 8 * TILE_SIZE
ROAD_BOTTOM = 13 * TILE_SIZE