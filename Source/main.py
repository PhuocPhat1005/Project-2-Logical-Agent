# from pysat.solvers import Solver
# from pysat.formula import CNF
from pysat.solvers import Solver
from pysat.formula import CNF
class Cell:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.value = -1
        self.element = []
        self.visited = False
        self.is_breeze = False
        self.is_stench = False
        self.is_whiff = False
        self.is_glow = False
        self.is_scream = False
        self.is_safe = False
        self.direction = None

class Program:
    def __init__(self, file_path):
        self.map_size = 0
        self.tmp_map = []
        self.file_path = file_path
        self.cells = []
        self.read_map()
        
    def read_map(self):
        """Reads the map from the input file."""
        with open(self.file_path, 'r') as file:
            # First line contains the size of the map
            self.map_size = int(file.readline().strip())
            
            # Next lines contain the map strings
            for _ in range(self.map_size):
                line = file.readline().strip()
                # Split by '.' to get rooms, then split each room by ','
                row = [cell.split(',') for cell in line.split('.')]
                self.tmp_map.append(row)
                
        for y in range(self.map_size):
            self.cells.append([])  # Correct initialization of a row
            for x in range(self.map_size):
                self.cells[y].append(Cell(y, x))  # Append cell to current row
                self.cells[y][x].element = self.tmp_map[y][x]
                
        self.tmp_map[0][0] = 'A'
        self.cells[0][0].safe = True
        self.cells[0][0].direction = 'right'
        
        self.update_map_info()

    def update_per_cell(self, y, x, elements):
        if 'W' in elements:
            self.add_stench(y, x)
        if 'H_P' in elements:
            self.add_glow(y, x)
        if 'P_G' in elements:
            self.add_whiff(y, x)
        elif 'P' in elements:
            self.add_breeze(y, x)
    
    def update_map_info(self):
        """Updates the map with Stench, Breeze, Whiff, and Glow."""
        # Iterate through each cell in the map
        for i in range(self.map_size):
            for j in range(self.map_size):
                elements = self.tmp_map[i][j]
                self.update_per_cell(i, j, elements)

                    
    def remove_element(self, y, x, element):
        self.cells[y][x].element.remove(element)
        if self.cells[y][x].element == []:
            self.cells[y][x].element.append('-')
            
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.map_size - 1 and 0 <= ny <= self.map_size - 1:
                if element == 'Wumpus':
                    self.cells[ny][nx].is_stench = False
                # elif element == 'Pit':
                #     self.cells[ny][nx].is_breeze = False
                # elif element == 'Poisonous Gas':
                #     self.cells[ny][nx].is_whiff = False
                elif element == 'Healing Potions':
                    self.cells[ny][nx].is_glow = False
                    
        self.update_per_cell(y, x, self.cells[y][x].element)
        
    def add_stench(self, y, x):
        """Adds stench to adjacent rooms of a Wumpus."""
        self.add_to_adjacent(y, x, 'Wumpus')

    def add_breeze(self, y, x):
        """Adds breeze to adjacent rooms of a Pit."""
        self.add_to_adjacent(y, x, 'Pit')

    def add_whiff(self, y, x):
        """Adds whiff to adjacent rooms of Poisonous Gas."""
        self.add_to_adjacent(y, x, 'Poisonous Gas')

    def add_glow(self, y, x):
        """Adds glow to adjacent rooms of Healing Potions."""
        self.add_to_adjacent(y, x, 'Healing Potions')

    def add_to_adjacent(self, y, x, object_name):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.map_size - 1 and 0 <= ny <= self.map_size - 1:
                if object_name == 'Wumpus':
                    self.cells[ny][nx].is_stench = True
                elif object_name == 'Pit':
                    self.cells[ny][nx].is_breeze = True
                elif object_name == 'Poisonous Gas':
                    self.cells[ny][nx].is_whiff = True
                elif object_name == 'Healing Potions':
                    self.cells[ny][nx].is_glow = True

    def display_map_test(self):
        print('Type: [element, stench, breeze, whiff, glow]')
        """Displays the map with all information."""
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.cells[i][j]
                print(f'[',cell.element, cell.is_stench, cell.is_breeze, cell.is_whiff, cell.is_glow, ']', end=' ')
            print()

class Agent:
    def __init__(self, map_size=4):
        self.x = 0
        self.y = 0
        self.health = 100
        self.map_size = map_size
        self.knowledge_base = CNF()
        self.healing_potion = 0
        self.point = 0
        self.direction = 'right'
        self.action = []
        #initialize the knowledge base with the starting position as safe
        self.knowledge_base.append([self.pos_literal(0, 0, 'safe')])

    def pos_literal(self, y, x, prop):
        # Assign positive literals for propositions at (y, x)
        return self.encode(y, x, prop)

    def neg_literal(self, y, x, prop):
        # Assign negative literals for propositions at (y, x)
        return -self.encode(y, x, prop)
    
    #Vi CNF va SAT solver yeu cau cac menh de la so nguyen unique, ta can encode thanh so nguyen va tao ham bat ki de no unique
    def encode(self, y, x, prop):
        # Encode a unique number for each proposition
        # For simplicity, encode as x * size + y with offsets for each proposition
        prop_offset = {'safe' : 1, 'breeze' : 2, 'stench' : 3, 'whiff' : 4, 'glow' : 5, 'scream' : 6}
        return x * self.map_size * len(prop_offset) + y * len(prop_offset) + prop_offset[prop]
    
    def get_adjacent_cells(self, y, x):
        # Get all valid adjacent cells
        adjacent = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.size - 1 and 0 <= ny <= self.size - 1:
                adjacent.append((ny, nx))
        return adjacent
    
    def add_observation(self, y, x, cell):
        adj_cells = self.get_adjacent_cells(y, x)
        for ay, ax in adj_cells:
            if not cell[ay][ax].is_safe:
                if cell[y][x].is_breeze:
                    self.knowledge_base.append([self.pos_literal(ay, ax, 'Pit')])
                if cell[y][x].is_stench:
                    self.knowledge_base.append([self.pos_literal(ay, ax, 'Wumpus')])
                if cell[y][x].is_whiff:
                    self.knowledge_base.append([self.pos_literal(ay, ax, 'Poisonous Gas')])
                if cell[y][x].is_glow:
                    self.knowledge_base.append([self.pos_literal(ay, ax, 'Healing Potions')])
            
    def check_Pit(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, 'Pit')])
            return not solver.solve()
    
    def check_Wumpus(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, 'Wumpus')])
            return not solver.solve()
    
    def check_Poisonous_Gas(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, 'Poisonous Gas')])
            return not solver.solve()
    
    def check_Healing_Potions(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, 'Healing Potions')])
            return not solver.solve()
        
    # def dfs(self, program):
        
        # start_cell = program.cells[0][0]
        # frontier = [start_cell]
        # while frontier:
        #     current_cell = frontier.pop() #pop the last element (stack)
        #     program.cells[current_cell.y][current_cell.x].visited = True
        #     self.add_observation(current_cell.y, current_cell.x, program.cells)

        #     if self.direction == 'right':
        #         directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]#right, up, down, left
        #     elif self.direction == 'left':
        #         directions = [(-1, 0), (0, 1), (0, -1), (1, 0)]#left, down, up, right
        #     elif self.direction == 'up':
        #         directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]#up, left, right, down
        #     elif self.direction == 'down':
        #         directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]#down, right, left, up
                
        #     # i = 0 -> go forward direction
        #     # i = 1 -> turn left direction
        #     # i = 2 -> turn right direction
        #     # i = 3 -> backward direction
            
        #     for dy, dx, i in enumerate(directions):
        #         nx, ny = current_cell.x + dx, current_cell.y + dy
        #         if 0 <= nx <= program.map_size - 1 and 0 <= ny <= program.map_size - 1:
        #             if program.cells[ny][nx].visited:
        #                 continue
                    
        #             if self.check_Pit(ny, nx):
        #                 continue
        #             elif self.check_Wumpus(ny, nx):
        #                 self.point -= i * 10
        #                 self.action.append({'cell ': (ny, nx), 'action': 'shoot'})
        #                 self.point -= 100
        #                 if 'Wumpus' in program.cells[ny][nx].element:
        #                     program.cells[ny][nx].is_scream = True
                            
        #                 pass
        #             elif self.check_Poisonous_Gas(ny, nx):
        #                 new_h = self.health - 25
        #                 if new_h <= 0:
        #                     if self.healing_potion > 0:
        #                         self.healing_potion -= 1
        #                         new_h = 25
        #                     else:
        #                         continue     
        #                 self.health = new_h
        #                 pass
                    
        #             if self.check_Healing_Potions(ny, nx):
        #                 pass
                    
        # tracepath
        # return path

def main():
    program = Program('input/input1.txt')
    program.display_map_test()
    agent = Agent(program.map_size)
    
if __name__ == '__main__':
    main()