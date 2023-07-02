import random
import pygame as pg
import pygame.gfxdraw as gfx
from settings import *

# MapRenderer class, responsible for drawing the map, player, vertices, and linedefs
class MapRenderer:
  def __init__(self, engine):
    self.engine = engine  # Reference to the main engine
    self.screen = engine.screen  # Screen object from the engine
    self.wad_data = engine.wad_data  # WAD data from the engine
    self.vertexes = self.wad_data.vertexes  # Vertex data from the WAD file
    self.linedefs = self.wad_data.linedefs  # Linedef data from the WAD file
    # Get map bounds for use in remapping
    self.x_min, self.x_max, self.y_min, self.y_max = self.get_map_bounds()
    # Remap vertex positions to fit the screen
    self.vertexes = [pg.math.Vector2(self.remap_x(v.x), self.remap_y(v.y))
                     for v in self.vertexes]

  # Placeholder draw method, draws nothing at the moment
  def draw(self):
    pass
    # The below methods would draw linedefs and the player position if uncommented
    # self.draw_linedefs()
    # self.draw_player_pos()

  # Draw vertical lines at specified x-coordinates with a color depending on the sub_sector_id
  def draw_vlines(self, x1, x2, sub_sector_id):
    color = self.get_color(sub_sector_id)  # Get a color based on the sub_sector_id
    pg.draw.line(self.engine.screen, color, (x1, 0), (x1, HEIGHT), 3)  # Draw line at x1
    pg.draw.line(self.engine.screen, color, (x2, 0), (x2, HEIGHT), 3)  # Draw line at x2

  # Draw a segment with a color depending on the sub_sector_id
  def draw_seg(self, seg, sub_sector_id):
    # Get the vertices for the segment
    v1 = self.vertexes[seg.start_vertex_id]
    v2 = self.vertexes[seg.end_vertex_id]
    pg.draw.line(self.engine.screen, 'green', v1, v2, 4)  # Draw the line
    # The below line would color the segment based on the sub_sector_id if uncommented
    # pg.draw.line(self.engine.screen, self.get_color(sub_sector_id), v1, v2, 4)

  # Draw linedefs in red
  def draw_linedefs(self):
    for line in self.linedefs:
      p1 = self.vertexes[line.start_vertex_id]
      p2 = self.vertexes[line.end_vertex_id]
      pg.draw.line(self.engine.screen, 'red', p1, p2, 2)

  # Draw the player position and field of view
  def draw_player_pos(self):
    pos = self.engine.player.pos  # Get player position
    x = self.remap_x(pos.x)  # Remap x position
    y = self.remap_y (pos.y)  # Remap y position
    self.draw_fov(px=x, py=y)  # Draw field of view
    pg.draw.circle(self.engine.screen, 'orange', (x, y), 10)  # Draw player position as orange circle

  def draw_fov(self, px, py):
    # Get the player's position and angle from the engine
    x, y = self.engine.player.pos
    angle = -self.engine.player.angle + 90

    # Compute the sine and cosine of the player's FOV
    sin_a1 = math.sin(math.radians(angle - H_FOV))
    cos_a1 = math.cos(math.radians(angle - H_FOV))
    sin_a2 = math.sin(math.radians(angle + H_FOV))
    cos_a2 = math.cos(math.radians(angle + H_FOV))
    len_ray = HEIGHT

    # Calculate the endpoints of the FOV lines and remap them to fit the screen
    x1, y1 = self.remap_x(x + len_ray * sin_a1), self.remap_y(y + len_ray * cos_a1)
    x2, y2 = self.remap_x(x + len_ray * sin_a2), self.remap_y(y + len_ray * cos_a2)

    # Draw the FOV lines on the screen in yellow
    pg.draw.line(self.engine.screen, 'yellow', (px, py), (x1, y1), 4)
    pg.draw.line(self.engine.screen, 'yellow', (px, py), (x2, y2), 4)


  def get_color(self, seed):
    random.seed(seed)  # Set the random seed to ensure reproducible results
    rnd = random.randrange  # Alias for the randrange function for brevity
    rng = 100, 256  # Define the range of possible color values
    return rnd(*rng), rnd(*rng), rnd(*rng)  # Return a randomly generated color

  def draw_bbox(self, bbox, color):
    # Remap the bounding box coordinates to the screen
    x, y = self.remap_x(bbox.left), self.remap_y(bbox.top)
    w, h = self.remap_x(bbox.right) - x, self.remap_y(bbox.bottom) - y

    # Draw the bounding box on the screen in the specified color
    pg.draw.rect(self.engine.screen, color, (x, y, w, h), 2)

  def draw_node(self, node_id):
    # Get the node data from the engine
    node = self.engine.wad_data.nodes[node_id]

    # Draw the bounding boxes for the front and back of the node
    bbox_front = node.bbox['front']
    bbox_back = node.bbox['back']
    self.draw_bbox(bbox=bbox_front, color='green')
    self.draw_bbox(bbox=bbox_back, color='red')

    # Draw the partition line for the node
    x1, y1 = self.remap_x(node.x_partition), self.remap_y(node.y_partition)
    x2 = self.remap_x(node.x_partition + node.dx_partition)
    y2 = self.remap_y(node.y_partition + node.dy_partition)
    pg.draw.line(self.engine.screen, 'blue', (x1, y1), (x2, y2), 4)

  def remap_x(self, n, out_min=30, out_max=WIDTH-30):
    # This method remaps the given x-coordinate (n) from the game map range to the screen range.
    # It also makes sure the x-coordinate stays within the screen bounds by clamping the input between the min and max x-coordinates of the map.
    return (max(self.x_min, min(n, self.x_max)) - self.x_min) * (
      out_max - out_min) / (self.x_max - self.x_min) + out_min

  def remap_y(self, n, out_min=30, out_max=HEIGHT-30):
    # This method does the same thing as remap_x, but for y-coordinates.
    # Note the subtraction from HEIGHT at the beginning. This is because pygame's y-coordinates start at the top of the screen, not the bottom.
    return HEIGHT - (max(self.y_min, min(n, self.y_max)) - self.y_min) * (
      out_max - out_min) / (self.y_max - self.y_min) - out_min

  def get_map_bounds(self):
    # This method returns the bounding box of the game map by finding the smallest and largest x and y coordinates from the list of vertexes.
    # The coordinates are sorted first to find the min and max values.
    x_sorted = sorted(self.vertexes, key=lambda v: v.x)
    x_min, x_max = x_sorted[0].x, x_sorted[-1].x
    y_sorted = sorted(self.vertexes, key=lambda v: v.y)
    y_min, y_max = y_sorted[0].y, y_sorted[-1].y
    return x_min, x_max, y_min, y_max

  def draw_vertexes(self):
    # This method draws all the vertexes of the game map on the screen.
    # Each vertex is represented by a white circle.
    for v in self.vertexes:
      pg.draw.circle(self.engine.screen, 'white', (v.x, v.y), 4)
