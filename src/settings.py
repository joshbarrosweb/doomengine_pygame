import math
from pygame.math import Vector2 as vec2

# DOOM's original resolution was 320x200 pixels.
DOOM_RES = DOOM_W, DOOM_H = 320, 200

# Scale factor to apply to the original resolution.
SCALE = 5

# Calculating the game's window resolution after applying the scale factor.
WIN_RES = WIDTH, HEIGHT = int(DOOM_W * SCALE), int(DOOM_H * SCALE)

# Calculating half-width and half-height of the window for easy reference.
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

# Field of View (FOV) is set to 90 degrees.
FOV = 90.0
# Half of the FOV for calculations.
H_FOV = FOV / 2

# Defining the speed at which the player can move.
PLAYER_SPEED = 0.3
# The speed at which the player can rotate.
PLAYER_ROT_SPEED = 0.12
# The height of the player. This could be used when calculating camera and player's eye level.
PLAYER_HEIGHT = 41

# The distance from the player to the screen.
# It's calculated using half the width of the screen and the tangent of half the field of view.
# It's used in calculating the projection of 3D world to 2D screen.
SCREEN_DIST = H_WIDTH / math.tan(math.radians(H_FOV))

# Key color used for transparency or other effects, similar to green screen.
COLOR_KEY = (152, 0, 136)
