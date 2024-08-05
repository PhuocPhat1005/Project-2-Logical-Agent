from pysat.solvers import Solver
from pysat.formula import CNF
from algorithms.cell import Cell


class Program:
    def __init__(self, file_path):
        self.map_size = 0
        self.tmp_map = []
        self.file_path = file_path
        self.cells = []
        self.read_map()

    def read_map(self):
        """Reads the map from the input file."""
        with open(self.file_path, "r") as file:
            # First line contains the size of the map
            self.map_size = int(file.readline().strip())

            # Next lines contain the map strings
            for _ in range(self.map_size):
                line = file.readline().strip()
                # Split by '.' to get rooms, then split each room by ','
                row = [cell.split(",") for cell in line.split(".")]
                self.tmp_map.append(row)

        for y in range(self.map_size):
            self.cells.append([])  # Correct initialization of a row
            for x in range(self.map_size):
                self.cells[y].append(Cell(y, x))  # Append cell to current row
                self.cells[y][x].element = self.tmp_map[y][x]

        self.tmp_map[0][0] = "A"
        self.cells[0][0].safe = True
        self.cells[0][0].direction = "right"

        self.update_map_info()

    def update_per_cell(self, y, x, elements):
        if "W" in elements:
            self.add_stench(y, x)
        if "H_P" in elements:
            self.add_glow(y, x)
        if "P_G" in elements:
            self.add_whiff(y, x)
        elif "P" in elements:
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
            self.cells[y][x].element.append("-")

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.map_size - 1 and 0 <= ny <= self.map_size - 1:
                if element == "Wumpus":
                    self.cells[ny][nx].is_stench = False
                # elif element == 'Pit':
                #     self.cells[ny][nx].is_breeze = False
                # elif element == 'Poisonous Gas':
                #     self.cells[ny][nx].is_whiff = False
                elif element == "Healing Potions":
                    self.cells[ny][nx].is_glow = False

        self.update_per_cell(y, x, self.cells[y][x].element)

    def add_stench(self, y, x):
        """Adds stench to adjacent rooms of a Wumpus."""
        self.add_to_adjacent(y, x, "Wumpus")

    def add_breeze(self, y, x):
        """Adds breeze to adjacent rooms of a Pit."""
        self.add_to_adjacent(y, x, "Pit")

    def add_whiff(self, y, x):
        """Adds whiff to adjacent rooms of Poisonous Gas."""
        self.add_to_adjacent(y, x, "Poisonous Gas")

    def add_glow(self, y, x):
        """Adds glow to adjacent rooms of Healing Potions."""
        self.add_to_adjacent(y, x, "Healing Potions")

    def add_to_adjacent(self, y, x, object_name):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.map_size - 1 and 0 <= ny <= self.map_size - 1:
                if object_name == "Wumpus":
                    self.cells[ny][nx].is_stench = True
                elif object_name == "Pit":
                    self.cells[ny][nx].is_breeze = True
                elif object_name == "Poisonous Gas":
                    self.cells[ny][nx].is_whiff = True
                elif object_name == "Healing Potions":
                    self.cells[ny][nx].is_glow = True

    def display_map_test(self):
        print("Type: [element, stench, breeze, whiff, glow]")
        """Displays the map with all information."""
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.cells[i][j]
                print(
                    f"[",
                    cell.element,
                    cell.is_stench,
                    cell.is_breeze,
                    cell.is_whiff,
                    cell.is_glow,
                    "]",
                    end=" ",
                )
            print()
