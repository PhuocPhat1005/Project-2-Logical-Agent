from algorithms.knowledge_base import KnowledgeBase
from utils.util import Action
from algorithms.directions import Directions
from algorithms.program import Program


# Agent class definition
class Agent:
    def __init__(self, map_size=10):
        self.x = 0  # chi so cot hien tai cua agent
        self.y = 0  # chi so hang hien tai cua agent
        self.current_hp = 100  # luong mau default
        self.map_size = map_size  # kich thuoc map hien tai
        self.knowledge_base = KnowledgeBase()  # Assuming KnowledgeBase class exists
        self.healing_potion = 0  # so luong healing potion dang nam giu hien tai
        self.point = 0  # so diem hien tai cua agent
        self.has_gold = False  # cho biet agent do co grab duoc gola chua
        self.killing_wumpus = False
        self.is_alive = True  # cho bien agent do con song ko (do bi an boi wumpus hay bi het mau hay bi roi xuong ho)
        self.explored_cells = (
            set()
        )  # Set to store explored cells => luu tru cac cell da duoc kham pha roi
        self.safe_cells = (
            set()
        )  # Set to store safe cells => cho biet cac cells ma agent di qua ma safe
        self.direction = (
            Directions.UP
        )  # Initialize with UP direction => set up huong dau tien cua agent la huong len.

        # Initial safe position (0, 0)
        self.knowledge_base.add_clause([self.pos_literal(0, 0, "SAFE")])
        self.safe_cells.add((0, 0))  # luon set up cell (0, 0) luon an toan
        self.explored_cells.add((0, 0))  # add cell(0,0) into the explored set

    # Method to generate a positive literal for a property at position (y, x)
    def pos_literal(self, y, x, prop):
        return self.encode(y, x, prop)

    # Method to generate a negative literal for a property at position (y, x)
    def neg_literal(self, y, x, prop):
        return -self.encode(y, x, prop)

    # Method to encode a property at position (y, x) as an integer
    def encode(self, y, x, prop):
        # Mapping of property names to unique offsets
        prop_offset = {
            "B": 1,
            "S": 2,
            "W_H": 3,
            "G_L": 4,
            "S_C": 5,
            "P": 6,
            "W": 7,
            "P_G": 8,
            "H_P": 9,
        }
        # Encoding based on x, y, and property offset
        return (
            x * self.map_size * len(prop_offset)
            + y * len(prop_offset)
            + prop_offset[prop]
        )

    # Method to get adjacent cells of a given position (y, x)
    def get_adjacent_cells(self, y, x):
        adjacent = []
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]  # Relative directions: up, down, left, right
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.map_size and 0 <= ny < self.map_size:
                adjacent.append((ny, nx))  # Add adjacent cells within map bounds
        return adjacent

    def perceive_current_cell(self, program):
        """Perceive the current cell and update the knowledge base."""
        cell = program.cells[self.y][self.x]  # Get the current cell from the program
        self.add_observation(
            self.y, self.x, cell
        )  # Add observations based on current cell properties
        neighbors = self.get_adjacent_cells(self.y, self.x)  # Get neighboring cells
        self.update_safe_cells(neighbors)  # Update the safe cells set

    # Method to add observations about a cell's properties
    def add_observation(self, y, x, cell):
        adj_cells = self.get_adjacent_cells(y, x)
        for ay, ax in adj_cells:
            if not cell.is_safe:  # If the current cell is not safe
                if (
                    cell.is_breeze
                ):  # If there's a breeze, infer the presence of a Pit in adjacent cells
                    self.knowledge_base.add_clause([self.pos_literal(ay, ax, "P")])
                if (
                    cell.is_stench
                ):  # If there's a stench, infer the presence of a Wumpus in adjacent cells
                    self.knowledge_base.add_clause([self.pos_literal(ay, ax, "W")])
                if (
                    cell.is_whiff
                ):  # If there's a whiff, infer the presence of Poisonous Gas in adjacent cells
                    self.knowledge_base.add_clause([self.pos_literal(ay, ax, "P_G")])
                if (
                    cell.is_glow
                ):  # If there's a glow, infer the presence of Healing Potions in adjacent cells
                    self.knowledge_base.add_clause([self.pos_literal(ay, ax, "H_P")])

    # Method to update the set of safe cells based on the knowledge base
    def update_safe_cells(self, neighbors):
        """Update the set of safe cells based on the knowledge base."""
        for ny, nx in neighbors:
            if self.check_safety(ny, nx):  # Check if neighboring cells are safe
                self.safe_cells.add((ny, nx))

    # Method to check if a cell is safe by ensuring it doesn't have dangerous elements
    def check_safety(self, y, x):
        return not any(
            [
                self.check_Pit(y, x),
                self.check_Wumpus(y, x),
                self.check_Poisonous_Gas(y, x),
            ]
        )

    # Method to check if a cell contains a Pit using the knowledge base
    def check_Pit(self, y, x):
        clause = [self.neg_literal(y, x, "P")]  # Check for absence of Pit
        return not self.knowledge_base.infer(clause)

    # Method to check if a cell contains a Wumpus using the knowledge base
    def check_Wumpus(self, y, x):
        clause = [self.neg_literal(y, x, "W")]
        return not self.knowledge_base.infer(clause)

    # Method to check if a cell contains Poisonous Gas using the knowledge base
    def check_Poisonous_Gas(self, y, x):
        clause = [self.neg_literal(y, x, "P_G")]
        return not self.knowledge_base.infer(clause)

    # Method to check if a cell contains Healing Potions using the knowledge base
    def check_Healing_Potions(self, y, x):
        clause = [self.neg_literal(y, x, "H_P")]
        return not self.knowledge_base.infer(clause)

    # Method to perform an action based on the agent's decision
    def perform_action(self, action, program, target=None):
        if action == Action.MOVE_FORWARD:
            self.move_forward(program)
        elif action == Action.TURN_LEFT:
            self.turn_left()
        elif action == Action.TURN_RIGHT:
            self.turn_right()
        elif action == Action.GRAB:
            self.grab(program)
        elif action == Action.SHOOT:
            self.shoot(target, program)
        elif action == Action.CLIMB:
            self.climb()
        elif action == Action.HEAL:
            self.heal()

    # Method to move the agent forward in the current direction
    def move_forward(self, program):
        dx, dy = Directions.get_movement_vector(self.direction)
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < self.map_size and 0 <= new_y < self.map_size:
            self.x, self.y = new_x, new_y
            self.point -= 10
            self.explored_cells.add((self.y, self.x))
            self.perceive_current_cell(program)

    # Method to turn the agent left
    def turn_left(self):
        self.direction = Directions.turn_left(self.direction)
        self.point -= 10

    # Method to turn the agent right
    def turn_right(self):
        self.direction = Directions.turn_right(self.direction)
        self.point -= 10

    # Method to grab gold or healing potions in the current cell
    def grab(self, program):
        cell = program.cells[self.y][self.x]
        if "G" in cell.element:  # Check if gold ("G") is in the current cell
            self.has_gold = True  # Mark the gold as grabbed
            self.point += 5000  # add points for grabbing gold
        if (
            "H_P" in cell.element
        ):  # check if the healing potion ("H_P") is in the current cell
            self.healing_potion += 1  # Update the number of healing potion
            cell.element.remove("H_P")  # Remove the healing potion from the cell
            self.point -= 10  # deduct points for grabbing healing potion

    # Method to shoot an arrow at a target cell
    def shoot(self, target, program):
        self.point -= 100  # deduct points for a shooting
        if self.check_Wumpus(
            target[0], target[1]
        ):  # Check if there's a Wumpus at the target cell.
            program.cells[target[0]][
                target[1]
            ].set_scream()  # Set the scream in the cell where Wumpus is shot
            self.update_map_after_wumpus_killed(
                target[0], target[1], program
            )  # update map after Wumpus is killed.

    # Method to climb out of the cave and end the game if the agent has gold.
    def climb(self):
        if (
            self.x == 0 and self.y == 0 and self.has_gold
        ):  # Check if the agent is at the starting position with the gold.
            self.point += 10
            print(
                f"Agent exits the cave with {self.point} points."
            )  # print the final score.
            self.is_alive = False  # mark the agent as no longer active (GAME OVER)

    # Method to heal the agent if it has a healing potion
    def heal(self):
        if self.healing_potion > 0:  # Check if the agent has any healing potions
            self.current_hp = min(
                self.current_hp + 25, 100
            )  # Restore the health points, up to a maximum of 100.
            self.healing_potion -= 1  # decrease the number of healing potions
            self.point -= 10  # deduct points for using a healing potion

    # DFS method to explore the map based on current knowledge

    def dfs(self, program):
        """Perform a DFS to explore the map based on current knowledge."""
        self.perceive_current_cell(program)  # Perceive the current cell at the start
        frontier = [(self.y, self.x)]  # Initialize the frontier with the current cell
        path = []  # Initialize an empty path
        self.explored_cells.add((self.y, self.x))  # Mark the starting cell as explored

        while frontier:  # While there are cells to explore
            current_y, current_x = frontier.pop()  # Pop the last cell from the frontier
            self.y, self.x = current_y, current_x  # Update agent's current position
            self.perceive_current_cell(program)  # Perceive the current cell again

            directions = self.get_movement_directions()

            for dy, dx in directions:
                ny, nx = current_y + dy, current_x + dx
                if (ny, nx) not in self.explored_cells and self.is_within_bounds(
                    nx, ny
                ):
                    if (ny, nx) in self.safe_cells:
                        frontier.append((ny, nx))  # Add the safe cell to the frontier
                        direction = (dy, dx)  # Store the direction
                        path.append(
                            (direction, (ny, nx))
                        )  # Append the direction and cell to the path
                        self.explored_cells.add((ny, nx))  # Mark this cell as explored
                        # Move the agent to this new cell
                        self.y, self.x = nx, ny
                    else:
                        self.handle_danger(
                            ny, nx, program
                        )  # Handle dangerous cells (e.g., shoot Wumpus)

        return path

    # Method to get the current cell's position
    def get_current_cell(self):
        return self.y, self.x

    # Method to check if a position is within map bounds
    def is_within_bounds(self, x, y):
        return 0 <= x < self.map_size and 0 <= y < self.map_size

    # Method to get possible movement directions based on the current direction
    def get_movement_directions(self):
        if self.direction == Directions.RIGHT:
            return [(1, 0), (0, -1), (0, 1), (-1, 0)]
        elif self.direction == Directions.LEFT:
            return [(-1, 0), (0, 1), (0, -1), (1, 0)]
        elif self.direction == Directions.UP:
            return [(0, -1), (-1, 0), (1, 0), (0, 1)]
        elif self.direction == Directions.DOWN:
            return [(0, 1), (1, 0), (-1, 0), (0, -1)]
        return []

    # Method to handle perceived dangers in a cell and update the knowledge base
    def handle_danger(self, ny, nx, program):
        """Handle perceived dangers and update the knowledge base accordingly."""
        cell = program.cells[ny][nx]  # Get the cell at the given position
        if self.check_Wumpus(ny, nx):  # Check if there's a Wumpus in the cells
            self.point -= 100  # Deduct points for encountering a Wumpus
            self.action.append(
                (Action.SHOOT, (ny, nx))
            )  # Add the shoot action to the agent's actions
            self.point -= 100  # Deduct points for shooting
            if "W" in cell.element:  # If the Wumpus is present in the cell
                cell.set_scream()  # Set scream in the cell where Wumpus is shot
                self.update_map_after_wumpus_killed(
                    ny, nx, program
                )  # Update map after Wumpus is killed
        elif self.check_Poisonous_Gas(
            ny, nx
        ):  # Check if there's Poisonous Gas in the cell
            self.current_hp -= 0.25 * self.current_hp  # Reduce health points by 25%
            if (
                self.current_hp <= 0 and self.healing_potion > 0
            ):  # If health points drop to 0 and there are healing potions
                self.healing_potion -= 1  # Use a healing potion
                self.current_hp = 0.25 * self.current_hp  # Restore 25% of health points
        if self.check_Healing_Potions(
            ny, nx
        ):  # Check if there are Healing Potions in the cell
            self.healing_potion += 1  # Increase the number of healing potions
            self.point += 10

    # Method to update the map after killing a Wumpus
    def update_map_after_wumpus_killed(self, y, x, program):
        adj_cells = self.get_adjacent_cells(y, x)  # Get adjacent cells of the Wumpus
        for ay, ax in adj_cells:
            if (
                "S" in program.cells[ay][ax].element
            ):  # If stench is present in adjacent cells
                program.cells[ay][ax].element.remove("S")

    # Helper method to return to the starting position after exploration
    def return_to_start(self, path):
        while path:
            action, _ = path.pop()
            self.perform_action(Action.TURN_LEFT)  # Adjust direction to move back
            self.perform_action(action)

    # Helper method to get valid movement directions
    def get_movement_directions(self):
        return Directions.get_possible_movements(self.direction)

    # Helper method to check if a position is within map bounds
    def is_within_bounds(self, x, y):
        return 0 <= x < self.map_size and 0 <= y < self.map_size

    def get_action(self, program):
        current_cell = program.cells[self.y][self.x]
        if self.current_hp <= 0:
            print("Loser !!!")
            return None
        if "G" in current_cell.element:
            return Action.GRAB
        if "H_P" in current_cell.element:
            return Action.GRAB
        if "W" in current_cell.element:
            return Action.SHOOT

    def is_dead(self):
        return not self.is_alive

    def has_exited(self):
        return self.has_gold and self.x == 0 and self.y == 0
