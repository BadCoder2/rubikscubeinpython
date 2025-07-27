# Overall goal: Implement a 3d rendering library to display the already written cube logic.
# TODO, NEXT UP: Fix CornerWOG and CornerWGR models/textures using the wrong green color.

from ursina import *
from cube import Cube as LogicalCube

# Config/constants

possible_turns = ['R', 'L', 'U', 'D', 'F', 'B']

coposdict = {
    'ULB': (-2, 2, 2),
    'UFR': (2, 2, -2),
    'UFL': (-2, 2, -2),
    'URB': (2, 2, 2),
    'DBR': (2, -2, 2),
    'DGL': (-2, -2, -2),
    'DFL': (-2, -2, 2),
    'DGR': (2, -2, -2),
}
edposdict = {
    'UB': (0, 2, 2),
    'UF': (0, 2, -2),
    'UL': (-2, 2, 0),
    'UR': (2, 2, 0),
    'BL': (-2, 0, 2),
    'FL': (-2, 0, -2),
    'BR': (2, 0, 2),
    'FR': (2, 0, -2),
    'DB': (0, -2, 2),
    'DF': (0, -2, -2),
    'DL': (-2, -2, 0),
    'DR': (2, -2, 0),
}
ceposdict = {
    'B': (0, 0, 2),
    'F': (0, 0, -2),
    'L': (-2, 0, 0),
    'R': (2, 0, 0),
    'U': (0, 2, 0),
    'D': (0, -2, 0),
}

# Start doing stuff

app = Ursina()

corner_dict = { # Create entities for each corner of the cube. Unfinished - the coordinates make it look like a 2x2 cube
    'WBO': Entity(model='CornerWBO', texture='CornerWBO', position=coposdict['ULB']),
    'WGR': Entity(model='CornerWGR', texture='CornerWGR', position=coposdict['UFR']),
    'WOG': Entity(model='CornerWOG', texture='CornerWOG', position=coposdict['UFL']),
    'WRB': Entity(model='CornerWRB', texture='CornerWRB', position=coposdict['URB']),
    'YBR': Entity(model='CornerYBR', texture='CornerYBR', position=coposdict['DBR']),
    'YGO': Entity(model='CornerYGO', texture='CornerYGO', position=coposdict['DGL']),
    'YOB': Entity(model='CornerYOB', texture='CornerYOB', position=coposdict['DFL']),
    'YRG': Entity(model='CornerYRG', texture='CornerYRG', position=coposdict['DGR']),
}
edge_dict = {
    'WB': Entity(model='EdgeWB', texture='EdgeWB', position=edposdict['UB']),
    'WG': Entity(model='EdgeWG', texture='EdgeWG', position=edposdict['UF']),
    'WO': Entity(model='EdgeWO', texture='EdgeWO', position=edposdict['UL']),
    'WR': Entity(model='EdgeWR', texture='EdgeWR', position=edposdict['UR']),
    'OB': Entity(model='EdgeOB', texture='EdgeOB', position=edposdict['BL']),
    'OG': Entity(model='EdgeOG', texture='EdgeOG', position=edposdict['FL']),
    'RB': Entity(model='EdgeRB', texture='EdgeRB', position=edposdict['BR']),
    'RG': Entity(model='EdgeRG', texture='EdgeRG', position=edposdict['FR']),
    'YB': Entity(model='EdgeYB', texture='EdgeYB', position=edposdict['DB']),
    'YG': Entity(model='EdgeYG', texture='EdgeYG', position=edposdict['DF']),
    'YO': Entity(model='EdgeYO', texture='EdgeYO', position=edposdict['DL']),
    'YR': Entity(model='EdgeYR', texture='EdgeYR', position=edposdict['DR']),
}
center_dict = {
    'B': Entity(model='CenterB', texture='CenterB', position=ceposdict['B']),
    'G': Entity(model='CenterG', texture='CenterG', position=ceposdict['F']),
    'O': Entity(model='CenterO', texture='CenterO', position=ceposdict['L']),
    'R': Entity(model='CenterR', texture='CenterR', position=ceposdict['R']),
    'W': Entity(model='CenterW', texture='CenterW', position=ceposdict['U']),
    'Y': Entity(model='CenterY', texture='CenterY', position=ceposdict['D']),
}

def input(key):
    if key in possible_turns:
        LogicalCube.turn(key)

EditorCamera()

while True:
    app.step()