# Overall goal: Implement a 3d rendering library to display the already written cube logic.
# TODO: Test corner movement with stuff other than R, also actually rotate the corners so you dont see the inside of the cube
# TODO later: Fix specific error case of first turning D then turning F raising an error

from ursina import *
from cube import LogicalCube

# Config/constants/setup

possible_turns = ['r', 'l', 'u', 'd', 'f', 'b']
last_cubestring = ''

coposdict = {
    'ULB': (-2, 2, 2),
    'UFR': (2, 2, -2),
    'UFL': (-2, 2, -2),
    'URB': (2, 2, 2),
    'DBR': (2, -2, 2),
    'DFL': (-2, -2, -2),
    'DBL': (-2, -2, 2),
    'DFR': (2, -2, -2),
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

corner_locations_in_cubestring_dict = { # Always in order of the following (consider only the applicable): U, L, F, R, B, D. AKA ascending order of the cubestring.
    'ULB': (0, 9, 38),
    'UFR': (8, 20, 27),
    'UFL': (6, 11, 18),
    'URB': (2, 29, 36),
    'DBR': (35, 42, 53),
    'DFL': (17, 24, 45),
    'DBL': (15, 44, 51),
    'DFR': (26, 33, 47)
}
default_position_dict = {
    'WOB': 'ULB',
    'WGR': 'UFR',
    'WOG': 'UFL',
    'WRB': 'URB',
    'RBY': 'DBR',
    'OGY': 'DFL',
    'OBY': 'DBL',
    'GRY': 'DFR'
}

# Start doing stuff

app = Ursina()
log_cube_instance = LogicalCube()

corner_dict = { # Create entities for each corner of the cube. The names of the files are whatever I decided at the time, whereas the variable names are named in order of W, O, G, R, B, Y
    'WOB': Entity(model='CornerWBO', texture='CornerWBO', position=coposdict['ULB']),
    'WGR': Entity(model='CornerWGR', texture='CornerWGR', position=coposdict['UFR']),
    'WOG': Entity(model='CornerWOG', texture='CornerWOG', position=coposdict['UFL']),
    'WRB': Entity(model='CornerWRB', texture='CornerWRB', position=coposdict['URB']),
    'RBY': Entity(model='CornerYBR', texture='CornerYBR', position=coposdict['DBR']),
    'OGY': Entity(model='CornerYGO', texture='CornerYGO', position=coposdict['DFL']),
    'OBY': Entity(model='CornerYOB', texture='CornerYOB', position=coposdict['DBL']),
    'GRY': Entity(model='CornerYRG', texture='CornerYRG', position=coposdict['DFR']),
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
        log_cube_instance.turn(key.upper())

EditorCamera()

if __name__ == '__main__':
    rundirectly = True
else:
    rundirectly = False

while rundirectly:
    cur_cubestring = log_cube_instance.get_cubestring()
    if cur_cubestring != last_cubestring:
        
        # Update the displayed cube based on the current cubestring
        print(f'Current cubestring: {cur_cubestring}, last cubestring: {last_cubestring}')

        # Update corner positions
        for key, posincs in corner_locations_in_cubestring_dict.items():
            colorcornerunsorted = ''.join([cur_cubestring[loc] for loc in posincs])
            # Sort the color corner string to match the order in corner_dict
            colorcorner = ''.join(sorted(colorcornerunsorted, key=lambda x: 'WOGRBY'.index(x)))
            corner_dict[colorcorner].position = coposdict[key]
            print(f'Unsorted corner: {colorcornerunsorted}, sorted corner: {colorcorner}')

        # TODO: Update edge positions
        # TODO: Update center positions
        # TODO: Update corner rotations
        # TODO: Update edge rotations
        # TODO: Update center rotations
        last_cubestring = cur_cubestring
    app.step()