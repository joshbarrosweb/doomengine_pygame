from settings import *

# This class represents a Binary Space Partitioning (BSP) tree used in the game engine
# It's used to determine the drawing order of the game's polygons
class BSP:
  SUB_SECTOR_IDENTIFIER = 0x8000  # The identifier for sub sectors in the BSP tree

  # Initialize BSP
  def __init__(self, engine):
    self.engine = engine  # The game engine
    self.player = engine.player  # The player
    self.nodes = engine.wad_data.nodes  # The nodes in the BSP tree
    self.sub_sectors = engine.wad_data.sub_sectors  # The sub sectors in the BSP tree
    self.segs = engine.wad_data.segments  # The segments in the BSP tree
    self.root_node_id = len(self.nodes) - 1  # The root node of the BSP tree
    self.is_traverse_bsp = True  # Determines if we should traverse the BSP tree

  # Update the BSP traversal
  def update(self):
    self.is_traverse_bsp = True  # Reset traversal flag
    self.render_bsp_node(node_id=self.root_node_id)  # Start rendering from root node

  # Get the height of the sub sector
  def get_sub_sector_height(self):
    sub_sector_id = self.root_node_id

    # Find the sub sector by traversing the BSP tree
    while not sub_sector_id >= self.SUB_SECTOR_IDENTIFIER:
      node = self.nodes[sub_sector_id]

      # Determine if player is on the back side of the node
      is_on_back = self.is_on_back_side(node)
      if is_on_back:
        sub_sector_id = self.nodes[sub_sector_id].back_child_id
      else:
        sub_sector_id = self.nodes[sub_sector_id].front_child_id

    # Get the sub sector and return the floor height of the first segment
    sub_sector = self.sub_sectors[sub_sector_id - self.SUB_SECTOR_IDENTIFIER]
    seg = self.segs[sub_sector.first_seg_id]
    return seg.front_sector.floor_height

  # Convert an angle to the x position on screen
  @staticmethod
  def angle_to_x(angle):
    if angle > 0:
      x = SCREEN_DIST - math.tan(math.radians(angle)) * H_WIDTH
    else:
      x = -math.tan(math.radians(angle)) * H_WIDTH + SCREEN_DIST
    return int(x)

  # Add a segment to the field of view (FOV)
  def add_segment_to_fov(self, vertex1, vertex2):
    angle1 = self.point_to_angle(vertex1)
    angle2 = self.point_to_angle(vertex2)

    # Normalize the difference between angles
    span = self.norm(angle1 - angle2)

    if span >= 180.0:
      return False

    rw_angle1 = angle1

    angle1 -= self.player.angle
    angle2 -= self.player.angle

    span1 = self.norm(angle1 + H_FOV)

    if span1 > FOV:
      if span1 >= span + FOV:
        return False
      angle1 = H_FOV

    span2 = self.norm(H_FOV - angle2)
    if span2 > FOV:
      if span2 >= span + FOV:
        return False
      angle2 = -H_FOV

    x1 = self.angle_to_x(angle1)
    x2 = self.angle_to_x(angle2)

    return x1, x2, rw_angle1

  # Render a sub sector by adding each segment in the sub sector to the FOV
  def render_sub_sector(self, sub_sector_id):
    sub_sector = self.sub_sectors[sub_sector_id]

    for i in range(sub_sector.seg_count):
      seg = self.segs[sub_sector.first_seg_id + i]
      if result := self.add_segment_to_fov(seg.start_vertex, seg.end_vertex):
        self.engine.seg_handler.classify_segment(seg, *result)

  # Normalize an angle to a value between 0 and 360
  @staticmethod
  def norm(angle):
    return angle % 360

  # Check if a bounding box is within the player's FOV
  def check_bbox(self, bbox):
    # Get the corners of the bounding box
    a, b = vec2(bbox.left, bbox.bottom), vec2(bbox.left, bbox.top)
    c, d = vec2(bbox.right, bbox.top), vec2(bbox.right, bbox.bottom)

    # Set the sides of the bounding box that need to be checked
    # based on the player's position
    px, py = self.player.pos
    if px < bbox.left:
      if py > bbox.top:
        bbox_sides = (b, a), (c, b)
      elif py < bbox.bottom:
        bbox_sides = (b, a), (a, d)
      else:
        bbox_sides = (b, a),
    elif px > bbox.right:
      if py > bbox.top:
        bbox_sides = (c, b), (d, c)
      elif py < bbox.bottom:
        bbox_sides = (a, d), (d, c)
      else:
        bbox_sides = (d, c),
    else:
      if py > bbox.top:
        bbox_sides = (c, b),
      elif py < bbox.bottom:
        bbox_sides = (a, d),
      else:
        return True

    # Check if any of the sides of the bounding box are within the player's FOV
    for v1, v2 in bbox_sides:
      angle1 = self.point_to_angle(v1)
      angle2 = self.point_to_angle(v2)

      span = self.norm(angle1 - angle2)

      angle1 -= self.player.angle
      span1 = self.norm(angle1 + H_FOV)

      if span1 > FOV:
        if span1 >= span + FOV:
          continue
      return True
    return False

  # Get the angle between the player's position and a vertex
  def point_to_angle(self, vertex):
    delta = vertex - self.player.pos
    return math.degrees(math.atan2(delta.y, delta.x))

  # Render a BSP node by recursively rendering its children nodes
  # The rendering order is determined by the player's position relative to the node's partition line
  def render_bsp_node(self, node_id):
    if self.is_traverse_bsp:

      if node_id >= self.SUB_SECTOR_IDENTIFIER:
        sub_sector_id = node_id - self.SUB_SECTOR_IDENTIFIER
        self.render_sub_sector(sub_sector_id)
        return None

      node = self.nodes[node_id]

      # Determine if player is on the back side of the node
      is_on_back = self.is_on_back_side(node)

      if is_on_back:
        self.render_bsp_node(node.back_child_id)
        if self.check_bbox(node.bbox['front']):
          self.render_bsp_node(node.front_child_id)
      else:
        self.render_bsp_node(node.front_child_id)
        if self.check_bbox(node.bbox['back']):
          self.render_bsp_node(node.back_child_id)

  # Check if the player is on the back side of a node
  def is_on_back_side(self, node):
    dx = self.player.pos.x - node.x_partition
    dy = self.player.pos.y - node.y_partition
    return dx * node.dy_partition - dy * node.dx_partition <= 0
