from settings import *
from pygame.math import Vector2 as vec2
import pygame as pg

class Player:
  def __init__(self, engine):
    self.engine = engine
    self.thing = engine.wad_data.things[0]
    self.pos = self.thing.pos
    self.angle = self.thing.angle
    self.height = PLAYER_HEIGHT
    self.DIAGONAL_MOVE_CORRECTION = 1 / math.sqrt(2)

  def update(self):
    self.get_height()
    self.control()

  def get_height(self):
    self.height = self.engine.bsp.get_sub_sector_height() + PLAYER_HEIGHT

  def control(self):
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
