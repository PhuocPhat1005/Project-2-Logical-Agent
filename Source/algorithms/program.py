from algorithms.cell import Cell
from utils.util import Action, Object
from algorithms.directions import Directions


class Program:
    """
    Class representing the Wumpus World program that handles the map, cell updates, and game logic.

    Attributes:
        map_size (int): The size of the map (NxN).
        tmp_map (list): Temporary storage for the map as a list of lists containing elements in each cell.
        file_path (str): Path to the file containing the map configuration.
        cells (list): A 2D list of Cell objects representing the Wumpus World grid.
    """

    def __init__(self, file_path):
        """
        Initializes the Program class with the provided file path.

        Args:
            file_path (str): The path to the map file.
        """
        self.map_size = 0  # Size of the map (NxN)
        self.tmp_map = []  # Temporary storage for map elements
        self.file_path = file_path  # File path for the map file
        self.cells = []  # 2D list to store Cell objects
        self.read_map()  # Read the map from the file and initialize the game world

    def read_map(self):
        """
        Reads the map from the input file and initializes the cells with elements.
        """
        with open(self.file_path, "r") as file:
            # Read the first line to get the size of the map
            self.map_size = int(file.readline().strip())

            # Read the map data line by line
            for _ in range(self.map_size):
                line = file.readline().strip()
                # Split the line by '.' to get rooms, then split each room by ','
                row = [cell.split(",") for cell in line.split(".")]  # Parse each row
                self.tmp_map.append(
                    row
                )  # Append the processed row to the temporary map

        # Initialize cells with positions and elements
        for y in range(self.map_size):
            self.cells.append([])  # Initialize a new row in cells
            for x in range(self.map_size):
                self.cells[y].append(
                    Cell(y, x)
                )  # Create a new Cell object for each position
                self.cells[y][x].element = self.tmp_map[y][
                    x
                ]  # Assign elements from the temporary map

        # Mark the starting position (0,0) as safe and set the initial direction to "right"
        self.tmp_map[0][0] = Object.AGENT.value
        self.cells[0][0].safe = True
        self.cells[0][0].direction = Directions.UP

        self.update_map_info()  # Update the map with stench, breeze, whiff, and glow

    def update_percepts(self, y, x, elements):
        """
        Updates the adjacent cells with stench, breeze, whiff, or glow based on the elements in the current cell.

        Args:
            y (int): The y-coordinate of the cell.
            x (int): The x-coordinate of the cell.
            elements (list): The elements present in the current cell.
        """
        if Object.WUMPUS.value in elements:  # If there's a Wumpus in the cell
            self.add_stench(y, x)  # Add stench to adjacent cells
        if (
            Object.HEALING_POTIONS.value in elements
        ):  # If there's a healing potion in the cell
            self.add_glow(y, x)  # Add glow to adjacent cells
        if (
            Object.POISONOUS_GAS.value in elements
        ):  # If there's poisonous gas in the cell
            self.add_whiff(y, x)  # Add whiff to adjacent cells
        elif Object.PIT.value in elements:  # If there's a pit in the cell
            self.add_breeze(y, x)  # Add breeze to adjacent cells

    def update_map_info(self):
        """
        Iterates through the map and updates the cells with information about stench, breeze, whiff, and glow.
        """
        # Iterate through each cell in the map
        for i in range(self.map_size):
            for j in range(self.map_size):
                elements = self.tmp_map[i][j]  # Get the elements in the current cell
                self.update_percepts(
                    i, j, elements
                )  # Update adjacent cells based on these elements

    def remove_elements(self, y, x, element):
        """
        Removes an element from the specified cell and updates the adjacent cells accordingly.

        Args:
            y (int): The y-coordinate of the cell.
            x (int): The x-coordinate of the cell.
            element (str): The element to be removed (e.g., "Wumpus", "Pit").
        """
        self.cells[y][x].element.remove(
            element
        )  # Remove the specified element from the cell
        if (
            self.cells[y][x].element == []
        ):  # If no elements are left, add a placeholder "-"
            self.cells[y][x].element.append("-")

        # Update the adjacent cells based on the removed element
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= self.map_size - 1 and 0 <= ny <= self.map_size - 1:
                if element == Object.WUMPUS.value:
                    self.cells[ny][
                        nx
                    ].remove_stench()  # Remove stench if Wumpus is removed
                elif element == Object.PIT.value:
                    self.cells[ny][
                        nx
                    ].remove_breeze()  # Remove breeze if Pit is removed
                elif element == Object.POISONOUS_GAS.value:
                    self.cells[ny][
                        nx
                    ].remove_whiff()  # Remove whiff if Poisonous Gas is removed
                elif element == Object.HEALING_POTIONS.value:
                    self.cells[ny][
                        nx
                    ].remove_glow()  # Remove glow if Healing Potion is removed

        # Re-update the current cell's adjacent cells
        self.update_per_cell(y, x, self.cells[y][x].element)

    def add_stench(self, y, x):
        """
        Adds stench to adjacent cells of a Wumpus.

        Args:
            y (int): The y-coordinate of the Wumpus cell.
            x (int): The x-coordinate of the Wumpus cell.
        """
        self.add_to_adjacent(y, x, "W")  # Add stench to adjacent cells

    def add_breeze(self, y, x):
        """
        Adds breeze to adjacent cells of a Pit.

        Args:
            y (int): The y-coordinate of the Pit cell.
            x (int): The x-coordinate of the Pit cell.
        """
        self.add_to_adjacent(y, x, "P")  # Add breeze to adjacent cells

    def add_whiff(self, y, x):
        """
        Adds whiff to adjacent cells of Poisonous Gas.

        Args:
            y (int): The y-coordinate of the Poisonous Gas cell.
            x (int): The x-coordinate of the Poisonous Gas cell.
        """
        self.add_to_adjacent(y, x, "P_G")  # Add whiff to adjacent cells

    def add_glow(self, y, x):
        """
        Adds glow to adjacent cells of Healing Potions.

        Args:
            y (int): The y-coordinate of the Healing Potions cell.
            x (int): The x-coordinate of the Healing Potions cell.
        """
        self.add_to_adjacent(y, x, "H_P")  # Add glow to adjacent cells

    def add_to_adjacent(self, y, x, object_name):
        """
        Adds an effect (stench, breeze, whiff, glow) to adjacent cells based on the specified object.

        Args:
            y (int): The y-coordinate of the cell with the object.
            x (int): The x-coordinate of the cell with the object.
            object_name (str): The name of the object (e.g., "Wumpus", "Pit").
        """
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]  # Directions to adjacent cells (up, down, left, right)
        for dy, dx in directions:
            nx, ny = x + dx, y + dy  # Calculate the new coordinates
            if 0 <= nx <= self.map_size - 1 and 0 <= ny <= self.map_size - 1:
                # Add the corresponding effect to the adjacent cell
                if object_name == Object.WUMPUS.value:
                    self.cells[ny][nx].set_stench()  # Add stench
                elif object_name == Object.PIT.value:
                    self.cells[ny][nx].set_breeze()  # Add breeze
                elif object_name == Object.WHIFF.value:
                    self.cells[ny][nx].set_whiff()  # Add whiff
                elif object_name == Object.HEALING_POTIONS.value:
                    self.cells[ny][nx].set_glow()  # Add glow

    def display_map_test(self):
        """
        Displays the map with all information for testing purposes.
        """
        print("Type: [element, stench, breeze, whiff, glow]")  # Header for map display
        # Iterate through each row in the map
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.cells[i][j]  # Get the cell at the current position
                # Display the cell's elements and effects
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
            print()  # Move to the next line after each row

    def get_cell_info(self, y, x):
        return self.tmp_map[y][x]
