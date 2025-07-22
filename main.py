# Overall goal: create a 3d visualization of a 3x3x3 Rubik's Cube in Python
# Current task: Test the newly implemented (i.e., untested) turn functions
# TODO in future: Implement the 'M', 'E', and 'S' turns, which are middle slice turns

# Config

test_mode = True

# Code

class Cube:
    def __init__(self):
        # Initialize a 3x3x3 cube with each face having a unique color
        # White top, green front initially
        self.cube = {
            'U': [['W'] * 3 for _ in range(3)],  # Up face (White)
            'D': [['Y'] * 3 for _ in range(3)],  # Down face (Yellow)
            'F': [['G'] * 3 for _ in range(3)],  # Front face (Green)
            'B': [['B'] * 3 for _ in range(3)],  # Back face (Blue)
            'L': [['O'] * 3 for _ in range(3)],  # Left face (Orange)
            'R': [['R'] * 3 for _ in range(3)],  # Right face (Red)
        }

    def print_state(self):
        # Print the current state of the cube
        for face in ['U', 'L', 'F', 'R', 'B', 'D']:
            print(f'{face} face: ')
            for row in self.cube[face]:
                print(row)
    
    def get_cubestring(self):
        # Return a string representation of the cube's state, for a solved cube this would be 'WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY'
        # Each face goes top left to top right then middle left to middle right then bottom left to bottom right
        # Order of faces: U, L, F, R, B, D
        string_representation = ''
        for face in ['U', 'L', 'F', 'R', 'B', 'D']:
            for row in self.cube[face]:
                string_representation += ''.join(row)

        return string_representation
    
    def set_cubestring(self, cubestring):
        # Set the cube's state from a string representation
        if len(cubestring) != 54:
            raise ValueError("Cubestring must be exactly 54 characters long.")
        
        faces = ['U', 'L', 'F', 'R', 'B', 'D']
        index = 0
        for face in faces:
            for i in range(3):
                self.cube[face][i] = list(cubestring[index:index + 3])
                index += 3

    def turn(self, command):
        # Perform a turn on the cube based on the command
        # I strongly considered using a dictionary that would allow for a more compact implementation, but I think this is more readable and more importantly, more easily debuggable
        print(f'Turning {command}')
        if command == 'R':
            # Three steps, as I see it. 1: the parts of the pieces affected not on the R face, 2: the R face's corners, 3: the R face's edges.
            # Step 1: Move the U face's right column to the B face's left column, the B face's left column to the D face's right column, and the D face's right column to the F face's right column.
            for i in range(3):
                temp = self.cube['D'][i][2]
                self.cube['D'][i][2] = self.cube['B'][2-i][0]
                self.cube['B'][2-i][0] = self.cube['U'][i][2]
                self.cube['U'][i][2] = self.cube['F'][i][2]
                self.cube['F'][i][2] = temp

            # Step 2: Rotate the R face's corners
            temp = self.cube['R'][0][0]
            self.cube['R'][0][0] = self.cube['R'][2][0]
            self.cube['R'][2][0] = self.cube['R'][2][2]
            self.cube['R'][2][2] = self.cube['R'][0][2]
            self.cube['R'][0][2] = temp

            # Step 3: Rotate the R face's edges
            temp = self.cube['R'][0][1] 
            self.cube['R'][0][1] = self.cube['R'][1][0]
            self.cube['R'][1][0] = self.cube['R'][2][1]
            self.cube['R'][2][1] = self.cube['R'][1][2]
            self.cube['R'][1][2] = temp
        elif command == 'L':
            # Now I'm going to do the same thing for the L face, and see if there are patterns, then hopefully generalize to all turns
            # Step 1: Move the U face's left column to the F face's left column, the F face's left column to the D face's left column, and the D face's left column to the B face's right column.
            for i in range(3):
                temp = self.cube['D'][i][0]
                self.cube['D'][i][0] = self.cube['F'][i][0]
                self.cube['F'][i][0] = self.cube['U'][i][0]
                self.cube['U'][i][0] = self.cube['B'][2-i][2]
                self.cube['B'][2-i][2] = temp

            # Step 2: Rotate the L face's corners
            temp = self.cube['L'][0][0]
            self.cube['L'][0][0] = self.cube['L'][2][0]
            self.cube['L'][2][0] = self.cube['L'][2][2]
            self.cube['L'][2][2] = self.cube['L'][0][2]
            self.cube['L'][0][2] = temp

            # Step 3: Rotate the L face's edges
            temp = self.cube['L'][0][1]
            self.cube['L'][0][1] = self.cube['L'][1][0]
            self.cube['L'][1][0] = self.cube['L'][2][1]
            self.cube['L'][2][1] = self.cube['L'][1][2]
            self.cube['L'][1][2] = temp
        elif command == 'U':
            # Step 1: Move the F face's top row to the L face's top row, the L face's top row to the B face's top row, and the B face's top row to the R face's top row.
            for i in range(3):
                temp = self.cube['L'][0][i]
                self.cube['L'][0][i] = self.cube['F'][0][i]
                self.cube['F'][0][i] = self.cube['R'][0][i]
                self.cube['R'][0][i] = self.cube['B'][0][2-i]
                self.cube['B'][0][2-i] = temp

            # Step 2: Rotate the U face's corners
            temp = self.cube['U'][0][0]
            self.cube['U'][0][0] = self.cube['U'][2][0]
            self.cube['U'][2][0] = self.cube['U'][2][2]
            self.cube['U'][2][2] = self.cube['U'][0][2]
            self.cube['U'][0][2] = temp

            # Step 3: Rotate the U face's edges
            temp = self.cube['U'][0][1]
            self.cube['U'][0][1] = self.cube['U'][1][0]
            self.cube['U'][1][0] = self.cube['U'][2][1]
            self.cube['U'][2][1] = self.cube['U'][1][2]
            self.cube['U'][1][2] = temp
        elif command == 'D':
            # Step 1: Move the F face's bottom row to the R face's bottom row, the R face's bottom row to the B face's bottom row, and the B face's bottom row to the L face's bottom row.
            for i in range(3):
                temp = self.cube['F'][2][i]
                self.cube['F'][2][i] = self.cube['R'][2][i]
                self.cube['R'][2][i] = self.cube['B'][2][i]
                self.cube['B'][2][i] = self.cube['L'][2][i]
                self.cube['L'][2][i] = temp

            # Step 2: Rotate the D face's corners
            temp = self.cube['D'][0][0]
            self.cube['D'][0][0] = self.cube['D'][2][0]
            self.cube['D'][2][0] = self.cube['D'][2][2]
            self.cube['D'][2][2] = self.cube['D'][0][2]
            self.cube['D'][0][2] = temp

            # Step 3: Rotate the D face's edges
            temp = self.cube['D'][0][1]
            self.cube['D'][0][1] = self.cube['D'][1][0]
            self.cube['D'][1][0] = self.cube['D'][2][1]
            self.cube['D'][2][1] = self.cube['D'][1][2]
            self.cube['D'][1][2] = temp
        elif command == 'F':
            # Step 1: Move the U face's bottom row to the R face's left column, the R face's left column to the D face's top row, and the D face's top row to the L face's right column.
            for i in range(3):
                temp = self.cube['U'][2][i]
                self.cube['U'][2][i] = self.cube['L'][i][2]
                self.cube['L'][i][2] = self.cube['D'][0][i]
                self.cube['D'][0][i] = self.cube['R'][2-i][0]
                self.cube['R'][2-i][0] = temp

            # Step 2: Rotate the F face's corners
            temp = self.cube['F'][0][0]
            self.cube['F'][0][0] = self.cube['F'][2][0]
            self.cube['F'][2][0] = self.cube['F'][2][2]
            self.cube['F'][2][2] = self.cube['F'][0][2]
            self.cube['F'][0][2] = temp

            # Step 3: Rotate the F face's edges
            temp = self.cube['F'][0][1]
            self.cube['F'][0][1] = self.cube['F'][1][0]
            self.cube['F'][1][0] = self.cube['F'][2][1]
            self.cube['F'][2][1] = self.cube['F'][1][2]
            self.cube['F'][1][2] = temp
        elif command == 'B':
            # Step 1: Move the U face's top row to the L face's left column, the L face's left column to the D face's bottom row, and the D face's bottom row to the R face's right column.
            for i in range(3):
                temp = self.cube['U'][0][i]
                self.cube['U'][0][i] = self.cube['R'][i][2]
                self.cube['R'][i][2] = self.cube['D'][2][2-i]
                self.cube['D'][2][2-i] = self.cube['L'][2-i][0]
                self.cube['L'][2-i][0] = temp

            # Step 2: Rotate the B face's corners
            temp = self.cube['B'][0][0]
            self.cube['B'][0][0] = self.cube['B'][2][0]
            self.cube['B'][2][0] = self.cube['B'][2][2]
            self.cube['B'][2][2] = self.cube['B'][0][2]
            self.cube['B'][0][2] = temp

            # Step 3: Rotate the B face's edges
            temp = self.cube['B'][0][1]
            self.cube['B'][0][1] = self.cube['B'][1][0]
            self.cube['B'][1][0] = self.cube['B'][2][1]
            self.cube['B'][2][1] = self.cube['B'][1][2]
            self.cube['B'][1][2] = temp

def test_cube_turn_r_basic():
    cur_cube = Cube()
    original_cubestring = cur_cube.get_cubestring()
    print(original_cubestring)
    cur_cube.turn('R')
    final_cubestring = cur_cube.get_cubestring()
    print(final_cubestring)
    assert final_cubestring == 'WWGWWGWWGOOOOOOOOOGGYGGYGGYRRRRRRRRRWBBWBBWBBYYBYYBYYB'
    print("Basic test passed.")

def test_cube_turn_r_adv():
    cubestring_of_solved_cube_turned_u = 'WWWWWWWWWGGGOOOOOORRRGGGGGGBBBRRRRRROOOBBBBBBYYYYYYYYY'
    cur_cube = Cube()
    cur_cube.set_cubestring(cubestring_of_solved_cube_turned_u)
    print(cur_cube.get_cubestring())
    cur_cube.turn('R')
    print(cur_cube.get_cubestring())
    cur_cube.turn('R')
    print(cur_cube.get_cubestring())
    assert cur_cube.get_cubestring() == 'WWYWWYWWYGGGOOOOOORRBGGBGGORRRRRRBBBGOOGBBRBBYYWYYWYYW'
    print("Advanced test phase 1 passed.")
    cur_cube.turn('R')
    cur_cube.turn('R')
    print(cur_cube.get_cubestring())
    assert cur_cube.get_cubestring() == cubestring_of_solved_cube_turned_u
    print("Advanced test phase 2 passed.")

def test_cube_turn_l_basic():
    cur_cube = Cube()
    original_cubestring = cur_cube.get_cubestring()
    print(original_cubestring)
    cur_cube.turn('L')
    final_cubestring = cur_cube.get_cubestring()
    print(final_cubestring)
    assert final_cubestring == 'BWWBWWBWWOOOOOOOOOWGGWGGWGGRRRRRRRRRBBYBBYBBYGYYGYYGYY'
    print("Basic test passed.")

if __name__ == "__main__" and test_mode == True:
    #test_cube_turn_r_basic()
    #test_cube_turn_r_adv()
    test_cube_turn_l_basic()