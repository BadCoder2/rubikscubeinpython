# Overall goal: Implement a 3d rendering library to display the already written cube logic.
# TODO: Fix specific error case of first turning D then turning F causing incorrect coloration (due to rotation, not position)

from ursina import *
from cube import LogicalCube

# Config/constants/setup

possible_turns = ['r', 'l', 'u', 'd', 'f', 'b']
last_cubestring = ''
uncomputed_turns = []

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
edge_locations_in_cubestring_dict = {
    'UB': (1, 37),
    'UF': (7, 19),
    'UL': (3, 10),
    'UR': (5, 28),
    'BL': (12, 41),
    'FL': (14, 21),
    'BR': (32, 39),
    'FR': (23, 30),
    'DB': (43, 52),
    'DF': (25, 46),
    'DL': (16, 48),
    'DR': (34, 50)
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
    'GR': Entity(model='EdgeRG', texture='EdgeRG', position=edposdict['FR']),
    'BY': Entity(model='EdgeYB', texture='EdgeYB', position=edposdict['DB']),
    'GY': Entity(model='EdgeYG', texture='EdgeYG', position=edposdict['DF']),
    'OY': Entity(model='EdgeYO', texture='EdgeYO', position=edposdict['DL']),
    'RY': Entity(model='EdgeYR', texture='EdgeYR', position=edposdict['DR']),
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
        uncomputed_turns.append(key)

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
        
        # Update edge positions
        for key, posincs in edge_locations_in_cubestring_dict.items():
            coloredgeunsorted = ''.join([cur_cubestring[i] for i in posincs])
            # Sort the color edge string to match the order in edge_dict
            coloredge = ''.join(sorted(coloredgeunsorted, key=lambda x: 'WOGRBY'.index(x)))
            edge_dict[coloredge].position = edposdict[key]
        
        # TODO: Update center positions

        last_cubestring = cur_cubestring
    if len(uncomputed_turns) > 0:
        # Update corner and edge rotations
        for turn in uncomputed_turns:
            if turn == 'r':
                # Check which corners are in the right face
                corner_tl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['UFR']])
                corner_tl_key = ''.join(sorted(corner_tl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_tr_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['URB']])
                corner_tr_key = ''.join(sorted(corner_tr_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_bl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DFR']])
                corner_bl_key = ''.join(sorted(corner_bl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_br_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DBR']])
                corner_br_key = ''.join(sorted(corner_br_key_us, key=lambda x: 'WOGRBY'.index(x)))
                # Rotate them
                corner_dict[corner_tl_key].rotation_x += 90
                corner_dict[corner_tr_key].rotation_x += 90
                corner_dict[corner_bl_key].rotation_x += 90
                corner_dict[corner_br_key].rotation_x += 90
                # Check which edges are in the right face
                edge_t_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UR']])
                edge_t_key = ''.join(sorted(edge_t_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_b_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DR']])
                edge_b_key = ''.join(sorted(edge_b_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_l_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['FR']])
                edge_l_key = ''.join(sorted(edge_l_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_r_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['BR']])
                edge_r_key = ''.join(sorted(edge_r_key_us, key=lambda x: 'WOGRBY'.index(x)))
                # Rotate them
                edge_dict[edge_t_key].rotation_x += 90
                edge_dict[edge_b_key].rotation_x += 90
                edge_dict[edge_l_key].rotation_x += 90
                edge_dict[edge_r_key].rotation_x += 90
            elif turn == 'l':
                corner_tl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['UFL']])
                corner_tl_key = ''.join(sorted(corner_tl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_tr_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['ULB']])
                corner_tr_key = ''.join(sorted(corner_tr_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_bl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DFL']])
                corner_bl_key = ''.join(sorted(corner_bl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_br_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DBL']])
                corner_br_key = ''.join(sorted(corner_br_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_dict[corner_tl_key].rotation_x -= 90
                corner_dict[corner_tr_key].rotation_x -= 90
                corner_dict[corner_bl_key].rotation_x -= 90
                corner_dict[corner_br_key].rotation_x -= 90
                edge_t_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UL']])
                edge_t_key = ''.join(sorted(edge_t_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_b_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DL']])
                edge_b_key = ''.join(sorted(edge_b_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_l_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['FL']])
                edge_l_key = ''.join(sorted(edge_l_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_r_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['BL']])
                edge_r_key = ''.join(sorted(edge_r_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_dict[edge_t_key].rotation_x -= 90
                edge_dict[edge_b_key].rotation_x -= 90
                edge_dict[edge_l_key].rotation_x -= 90
                edge_dict[edge_r_key].rotation_x -= 90
            elif turn == 'u':
                corner_tl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['ULB']])
                corner_tl_key = ''.join(sorted(corner_tl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_tr_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['UFR']])
                corner_tr_key = ''.join(sorted(corner_tr_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_bl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['UFL']])
                corner_bl_key = ''.join(sorted(corner_bl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_br_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['URB']])
                corner_br_key = ''.join(sorted(corner_br_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_dict[corner_tl_key].rotation_y += 90
                corner_dict[corner_tr_key].rotation_y += 90
                corner_dict[corner_bl_key].rotation_y += 90
                corner_dict[corner_br_key].rotation_y += 90
                edge_t_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UF']])
                edge_t_key = ''.join(sorted(edge_t_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_b_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UB']])
                edge_b_key = ''.join(sorted(edge_b_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_l_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UL']])
                edge_l_key = ''.join(sorted(edge_l_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_r_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UR']])
                edge_r_key = ''.join(sorted(edge_r_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_dict[edge_t_key].rotation_y += 90
                edge_dict[edge_b_key].rotation_y += 90
                edge_dict[edge_l_key].rotation_y += 90
                edge_dict[edge_r_key].rotation_y += 90
            elif turn == 'd':
                corner_tl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DBR']])
                corner_tl_key = ''.join(sorted(corner_tl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_tr_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DFR']])
                corner_tr_key = ''.join(sorted(corner_tr_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_bl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DBL']])
                corner_bl_key = ''.join(sorted(corner_bl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_br_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DFL']])
                corner_br_key = ''.join(sorted(corner_br_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_dict[corner_tl_key].rotation_y -= 90
                corner_dict[corner_tr_key].rotation_y -= 90
                corner_dict[corner_bl_key].rotation_y -= 90
                corner_dict[corner_br_key].rotation_y -= 90
                edge_t_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DF']])
                edge_t_key = ''.join(sorted(edge_t_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_b_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DB']])
                edge_b_key = ''.join(sorted(edge_b_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_l_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DL']])
                edge_l_key = ''.join(sorted(edge_l_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_r_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DR']])
                edge_r_key = ''.join(sorted(edge_r_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_dict[edge_t_key].rotation_y -= 90
                edge_dict[edge_b_key].rotation_y -= 90
                edge_dict[edge_l_key].rotation_y -= 90
                edge_dict[edge_r_key].rotation_y -= 90
            elif turn == 'f':
                corner_tl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['UFR']])
                corner_tl_key = ''.join(sorted(corner_tl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_tr_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DFR']])
                corner_tr_key = ''.join(sorted(corner_tr_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_bl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['UFL']])
                corner_bl_key = ''.join(sorted(corner_bl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_br_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DFL']])
                corner_br_key = ''.join(sorted(corner_br_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_dict[corner_tl_key].rotation_z += 90
                corner_dict[corner_tr_key].rotation_z += 90
                corner_dict[corner_bl_key].rotation_z += 90
                corner_dict[corner_br_key].rotation_z += 90
                edge_t_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UF']])
                edge_t_key = ''.join(sorted(edge_t_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_b_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DF']])
                edge_b_key = ''.join(sorted(edge_b_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_l_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['FR']])
                edge_l_key = ''.join(sorted(edge_l_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_r_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['FL']])
                edge_r_key = ''.join(sorted(edge_r_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_dict[edge_t_key].rotation_z += 90
                edge_dict[edge_b_key].rotation_z += 90
                edge_dict[edge_l_key].rotation_z += 90
                edge_dict[edge_r_key].rotation_z += 90
            elif turn == 'b':
                corner_tl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['ULB']])
                corner_tl_key = ''.join(sorted(corner_tl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_tr_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['URB']])
                corner_tr_key = ''.join(sorted(corner_tr_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_bl_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DBL']])
                corner_bl_key = ''.join(sorted(corner_bl_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_br_key_us = ''.join([cur_cubestring[i] for i in corner_locations_in_cubestring_dict['DBR']])
                corner_br_key = ''.join(sorted(corner_br_key_us, key=lambda x: 'WOGRBY'.index(x)))
                corner_dict[corner_tl_key].rotation_z -= 90
                corner_dict[corner_tr_key].rotation_z -= 90
                corner_dict[corner_bl_key].rotation_z -= 90
                corner_dict[corner_br_key].rotation_z -= 90
                edge_t_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['UB']])
                edge_t_key = ''.join(sorted(edge_t_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_b_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['DB']])
                edge_b_key = ''.join(sorted(edge_b_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_l_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['BL']])
                edge_l_key = ''.join(sorted(edge_l_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_r_key_us = ''.join([cur_cubestring[i] for i in edge_locations_in_cubestring_dict['BR']])
                edge_r_key = ''.join(sorted(edge_r_key_us, key=lambda x: 'WOGRBY'.index(x)))
                edge_dict[edge_t_key].rotation_z -= 90
                edge_dict[edge_b_key].rotation_z -= 90
                edge_dict[edge_l_key].rotation_z -= 90
                edge_dict[edge_r_key].rotation_z -= 90
        uncomputed_turns = []
        # TODO: Update center rotations
    app.step()