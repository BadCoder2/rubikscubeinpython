# Overall goal: Implement a 3d rendering library to display the already written cube logic.
# TODO, NEXT UP: Fix CornerWOG and CornerWGR models/textures using the wrong green color.

from ursina import *

app = Ursina()

corner_dict = { # Create entities for each corner of the cube. Unfinished - the coordinates make it look like a 2x2 cube
    'WBO': Entity(model='CornerWBO', texture='CornerWBO', position=(-2, 2, 2)),
    'WGR': Entity(model='CornerWGR', texture='CornerWGR', position=(2, 2, -2)),
    'WOG': Entity(model='CornerWOG', texture='CornerWOG', position=(-2, 2, -2)),
    'WRB': Entity(model='CornerWRB', texture='CornerWRB', position=(2, 2, 2)),
    'YBR': Entity(model='CornerYBR', texture='CornerYBR', position=(2, -2, 2)),
    'YGO': Entity(model='CornerYGO', texture='CornerYGO', position=(-2, -2, -2)),
    'YOB': Entity(model='CornerYOB', texture='CornerYOB', position=(-2, -2, 2)),
    'YRG': Entity(model='CornerYRG', texture='CornerYRG', position=(2, -2, -2)),
}
edge_dict = {
    'WB': Entity(model='EdgeWB', texture='EdgeWB', position=(0, 2, 2)),
    'WG': Entity(model='EdgeWG', texture='EdgeWG', position=(0, 2, -2)),
    'WO': Entity(model='EdgeWO', texture='EdgeWO', position=(-2, 2, 0)),
    'WR': Entity(model='EdgeWR', texture='EdgeWR', position=(2, 2, 0)),
    'OB': Entity(model='EdgeOB', texture='EdgeOB', position=(-2, 0, 2)),
    'OG': Entity(model='EdgeOG', texture='EdgeOG', position=(-2, 0, -2)),
    'RB': Entity(model='EdgeRB', texture='EdgeRB', position=(2, 0, 2)),
    'RG': Entity(model='EdgeRG', texture='EdgeRG', position=(2, 0, -2)),
    'YB': Entity(model='EdgeYB', texture='EdgeYB', position=(0, -2, 2)),
    'YG': Entity(model='EdgeYG', texture='EdgeYG', position=(0, -2, -2)),
    'YO': Entity(model='EdgeYO', texture='EdgeYO', position=(-2, -2, 0)),
    'YR': Entity(model='EdgeYR', texture='EdgeYR', position=(2, -2, 0)),
}
center_dict = {
    'B': Entity(model='CenterB', texture='CenterB', position=(0, 0, 2)),
    'G': Entity(model='CenterG', texture='CenterG', position=(0, 0, -2)),
    'O': Entity(model='CenterO', texture='CenterO', position=(-2, 0, 0)),
    'R': Entity(model='CenterR', texture='CenterR', position=(2, 0, 0)),
    'W': Entity(model='CenterW', texture='CenterW', position=(0, 2, 0)),
    'Y': Entity(model='CenterY', texture='CenterY', position=(0, -2, 0)),
}

EditorCamera()
while True:
    app.step()