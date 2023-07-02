# Import the necessary libraries and modules
import pygame as pg
import sys
from wad_data import WADData
from settings import *
from map_renderer import MapRenderer
from player import Player
from bsp import BSP
from seg_handler import SegHandler
from view_renderer import ViewRenderer

# DoomEngine class. This is the main engine of the game.
class DoomEngine:
  def __init__(self, wad_path='./resources/wad/DOOM1.WAD'):
    self.wad_path = wad_path  # Path to the WAD file.
    self.screen = pg.display.set_mode(WIN_RES, pg.SCALED)  # Pygame display surface.
    self.framebuffer = pg.surfarray.array3d(self.screen)  # Access pixel data directly.
    self.clock = pg.time.Clock()  # Pygame Clock object to track time.
    self.running = True  # Main game loop flag.
    self.dt = 1 / 60  # Delta time for each frame.
    self.on_init()  # Initialize the engine.

  # Method to initialize the game engine and all other components.
  def on_init(self):
    self.wad_data = WADData(self, map_name='E1M1')  # Load the WAD data.
    self.map_renderer = MapRenderer(self)  # Initialize the map renderer.
    self.player = Player(self)  # Initialize the player.
    self.bsp = BSP(self)  # Initialize the BSP tree.
    self.seg_handler = SegHandler(self)  # Initialize the segment handler.
    self.view_renderer = ViewRenderer(self)  # Initialize the view renderer.

  # Method to update the game state.
  def update(self):
    self.player.update()  # Update player state.
    self.seg_handler.update()  # Update segment handler state.
    self.bsp.update()  # Update BSP state.
    self.dt = self.clock.tick()  # Update the clock.
    pg.display.set_caption("Josue's Doom Engine: " + f'{self.clock.get_fps() :.1f}')  # Update the display caption with the current FPS.

  # Method to draw to the screen.
  def draw(self):
    pg.surfarray.blit_array(self.screen, self.framebuffer)  # Copy pixel data to the display surface.
    self.view_renderer.draw_sprite()  # Draw sprites.
    pg.display.flip()  # Update the display.

  # Method to check and handle Pygame events.
  def check_events(self):
    for e in pg.event.get():
      if e.type == pg.QUIT:  # If the QUIT event is triggered, end the game.
        self.running = False
        pg.quit()
        sys.exit()

  # Main game loop.
  def run(self):
    while self.running:  # Continue as long as the game is running.
      self.check_events()  # Check and handle events.
      self.update()  # Update game state.
      self.draw()  # Draw to the screen.

if __name__ == '__main__':  # If the script is run directly, initialize the DoomEngine and start the game.
  doom = DoomEngine()
  doom.run()
