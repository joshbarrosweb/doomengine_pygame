from settings import *
from pygame.math import Vector2 as vec2
import pygame as pg

class Player:
  def __init__(self, engine):
    # The Player class is initialized with an engine, which holds data related to the game's state.
    # The player's position and orientation (angle) are initialized from a "thing" in the game data.

    self.engine = engine
    self.thing = engine.wad_data.things[0]
    self.pos = self.thing.pos
    self.angle = self.thing.angle
    self.height = PLAYER_HEIGHT
    self.floor_height = 0
    self.z_velocity = 0
    self.DIAGONAL_MOVE_CORRECTION = 1 / math.sqrt(2)

  def update(self):
    # This function updates the player's height and controls on each frame.

    self.get_height()
    self.control()

  def get_height(self):
    # This function updates the player's height.
    # The player's height changes depending on their movement and any changes to the floor height.

    self.height = self.engine.bsp.get_sub_sector_height() + PLAYER_HEIGHT

    if self.height < self.floor_height + PLAYER_HEIGHT:
      self.height += 0.4 * (self.floor_height + PLAYER_HEIGHT - self.height)
      self.z_velocity = 0
    else:
      self.z_velocity -= 0.9
      self.height += max(-15.0, self.z_velocity)

  def control(self):
    # This function handles player's control inputs (keyboard events).
    # The speed of the player is scaled by the time passed since the last frame to ensure smooth movement.
    # Rotation is handled by the left and right arrow keys, and movement is handled by the WASD keys.
    # If the player is moving diagonally, the movement vector is corrected to ensure the player doesn't move faster diagonally.

    speed = PLAYER_SPEED * self.engine.dt
    rot_speed = PLAYER_ROT_SPEED * self.engine.dt

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
      self.angle += rot_speed
    if keys[pg.K_RIGHT]:
      self.angle -= rot_speed

    inc = vec2(0)
    if keys[pg.K_a]:
      inc += vec2(0, speed)
    if keys[pg.K_d]:
      inc += vec2(0, -speed)
    if keys[pg.K_w]:
      inc += vec2(speed, 0)
    if keys[pg.K_s]:
      inc += vec2(-speed, 0)

    if inc.x and inc.y:
      inc *= self.DIAGONAL_MOVE_CORRECTION

    inc.rotate_ip(self.angle)
    self.pos += inc
