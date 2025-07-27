# Overall goal: Implement a 3d rendering library to display the already written cube logic. Arrow keys to rotate the view.
# Current task: Implement a 3d rendering library to display cube. No rotation yet.

from ursina import *
from PIL import Image

app = Ursina()

corner_dict = { # Create entities for each corner of the cube. Unfinished - the coordinates make it look like a 2x2 cube
    'WBO': Entity(model='CornerWBO', texture='CornerWBO', position=(-1, 1, 1)),
    'WGR': Entity(model='CornerWGR', texture='CornerWGR', position=(1, 1, -1)),
    'WOG': Entity(model='CornerWOG', texture='CornerWOG', position=(-1, 1, -1)),
    'WRB': Entity(model='CornerWRB', texture='CornerWRB', position=(1, 1, 1)),
    'YBR': Entity(model='CornerYBR', texture='CornerYBR', position=(1, -1, 1)),
    'YGO': Entity(model='CornerYGO', texture='CornerYGO', position=(-1, -1, -1)),
    'YOB': Entity(model='CornerYOB', texture='CornerYOB', position=(-1, -1, 1)),
    'YRG': Entity(model='CornerYRG', texture='CornerYRG', position=(1, -1, -1)),
}

EditorCamera()
app.run()