# Overall goal: create a 3d visualization of a 3x3x3 Rubik's Cube in Python
# Current task: Implement a way to store the state of the cube

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
        print(f'Turning {command}')
        if command == 'R':
            # Three steps, as I see it. 1: the parts of the pieces affected not on the R face, 2: the R face's corners, 3: the R face's edges.
            # Step 1: Move the U face's right column to the B face's right column, the B face's right column to the D face's right column, and the D face's right column to the F face's right column.
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

if __name__ == "__main__" and test_mode == True:
    #test_cube_turn_r_basic()
    test_cube_turn_r_adv()