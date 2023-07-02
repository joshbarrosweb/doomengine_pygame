# Class representing a texture map with fields like name, flags, dimensions, column direction, number of patches and the patch maps themselves
class TextureMap:
  __slots__ = [
    'name',
    'flags',
    'width',
    'height',
    'column_dir',
    'patch_count',
    'patch_maps'
  ]

# Class representing the header of a texture with fields like the count of textures, texture offset and texture data offset
class TextureHeader:
  __slots__ = [
    'texture_count',
    'texture_offset',
    'texture_data_offset'
  ]

# Class representing a patch map with fields like x and y offsets, index of the patch name, step direction and the color map
class PatchMap:
  __slots__ = [
    'x_offset',
    'y_offset',
    'p_name_index',
    'step_dir',
    'color_map'
  ]

# Class representing a column in a patch with fields like top delta, length, pre and post padding, and the actual data
class PatchColumn:
  __slots__ = [
    'top_delta',
    'length',
    'padding_pre',
    'data',
    'padding_post'
  ]

# Class representing the header of a patch with fields like dimensions, offsets from top left, and column offset
class PatchHeader:
  __slots__ = [
    'width',
    'height',
    'left_offset',
    'top_offset',
    'column_offset'
  ]

# Class representing a 'Thing' object with fields like position, angle, type, and flags
class Thing:
  __slots__ = [
    'pos',
    'angle',
    'type',
    'flags'
  ]

# Class representing a sector with fields like floor and ceiling heights, floor and ceiling textures, light level, type, and tag
class Sector:
  __slots__ = [
    'floor_height',
    'ceil_height',
    'floor_texture',
    'ceil_texture',
    'light_level',
    'type',
    'tag'
  ]

# Class representing a sidedef with fields like offsets, texture details, and sector id. Also maintains a reference to its associated sector
class Sidedef:
  __slots__ = [
    'x_offset',
    'y_offset',
    'upper_texture',
    'lower_texture',
    'middle_texture',
    'sector_id',
  ]

  __slots__ += ['sector']

# Class representing a segment with fields like start and end vertex ids, angle, linedef id, direction, and offset. Also maintains references to its vertices, linedef, and front and back sectors
class Seg:
  __slots__ = [
    'start_vertex_id',
    'end_vertex_id',
    'angle',
    'linedef_id',
    'direction',
    'offset'
  ]
  __slots__ += ['start_vertex', 'end_vertex', 'linedef', 'front_sector', 'back_sector']

# Class representing a linedef with fields like start and end vertex ids, flags, line type, sector tag, and front and back sidedef ids. Also maintains references to its front and back sidedefs
class Linedef:
  __slots__ = [
    'start_vertex_id',
    'end_vertex_id',
    'flags',
    'line_type',
    'sector_tag',
    'front_sidedef_id',
    'back_sidedef_id'
  ]
  __slots__ += ['front_sidedef', 'back_sidedef']

# Class representing a sub sector with fields like count of segments and id of the first segment
class SubSector:
  __slots__ = [
    'seg_count',
    'first_seg_id'
  ]

# Class representing a node in a BSP tree. Has fields like partition coordinates, partition deltas, bounding boxes and child node ids. Also contains a nested class BBox to represent a bounding box with fields for its edges
class Node:
  class BBox:
    __slots__ = ['top', 'bottom', 'left', 'right']

  __slots__ = [
    'x_partition',
    'y_partition',
    'dx_partition',
    'dy_partition',
    'bbox',
    'front_child_id',
    'back_child_id'
  ]

  # Initialize the node with bounding boxes for front and back sides
  def __init__(self):
    self.bbox = {'front': self.BBox(), 'back': self.BBox()}
