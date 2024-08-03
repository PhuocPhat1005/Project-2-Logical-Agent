class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.element = []
        self.visited = False
        self.is_safe = False
        self.is_breeze = False
        self.is_stench = False
        self.is_whiff = False
        self.is_glow = False
        self.is_scream = False

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
                # Split by dots to get rooms and add to map
                self.tmp_map.append(line.split('.'))
                
        for i in range(self.map_size):
            self.cells.append([])  # Correct initialization of a row
            for j in range(self.map_size):
                self.cells[i].append(Cell(i, j))  # Append cell to current row
        self.tmp_map[0][0] = 'A'
        self.update_map_info()

    def update_map_info(self):
        """Updates the map with Stench, Breeze, Whiff, and Glow."""
        # Iterate through each cell in the map
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.tmp_map[i][j]
                if cell != '-':
                    self.cells[i][j].element.append(cell)
                    
                # Update with Percepts
                if 'W' in cell:
                    self.add_stench(i, j)
                if 'H_P' in cell:
                    self.add_glow(i, j)
                if 'P_G' in cell:
                    self.add_whiff(i, j)
                elif 'P' in cell:
                    self.add_breeze(i, j)

    def add_stench(self, x, y):
        """Adds stench to adjacent rooms of a Wumpus."""
        self.add_to_adjacent(x, y, 'Wumpus')

    def add_breeze(self, x, y):
        """Adds breeze to adjacent rooms of a Pit."""
        self.add_to_adjacent(x, y, 'Pit')

    def add_whiff(self, x, y):
        """Adds whiff to adjacent rooms of Poisonous Gas."""
        self.add_to_adjacent(x, y, 'Poisonous Gas')

    def add_glow(self, x, y):
        """Adds glow to adjacent rooms of Healing Potions."""
        self.add_to_adjacent(x, y, 'Healing Potions')

    def add_to_adjacent(self, x, y, object_name):
        """Adds a symbol to adjacent cells if they're empty or don't already have it."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.map_size and 0 <= ny < self.map_size:
                if object_name == 'Wumpus':
                    self.cells[nx][ny].is_stench = True
                elif object_name == 'Pit':
                    self.cells[nx][ny].is_breeze = True
                elif object_name == 'Poisonous Gas':
                    self.cells[nx][ny].is_whiff = True
                elif object_name == 'Healing Potions':
                    self.cells[nx][ny].is_glow = True

    def display_map_test(self):
        print('Type: [element, stench, breeze, whiff, glow]')
        """Displays the map with all information."""
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.cells[i][j]
                print(f'[', cell.element if cell.element != [] else 'Empty', cell.is_stench, cell.is_breeze, cell.is_whiff, cell.is_glow, ']', end=' ')
            print()

# Example usage:
program = Program('input/input1.txt')
program.display_map_test()
