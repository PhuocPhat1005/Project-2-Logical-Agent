from algorithms.knowledge_base import KnowledgeBase
from utils.util import Action, Object
from algorithms.directions import Directions


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

        # Vị trí an toàn ban đầu (0, 0)
        self.knowledge_base.add_clause([self.neg_literal(0, 0, Object.PIT)])
        self.knowledge_base.add_clause([self.neg_literal(0, 0, Object.WUMPUS)])
        self.knowledge_base.add_clause([self.neg_literal(0, 0, Object.HEALING_POTIONS)])
        self.knowledge_base.add_clause([self.neg_literal(0, 0, Object.POISONOUS_GAS)])
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
            Object.BREEZE: 1,  # breeze
            Object.STENCH: 2,  # stench
            Object.WHIFF: 3,  # whiff
            Object.GLOW: 4,  # glow
            Object.SCREAM: 5,  # scream
            Object.PIT: 6,  # pit
            Object.WUMPUS: 7,  # wumpus
            Object.POISONOUS_GAS: 8,  # poisonous gas
            Object.HEALING_POTIONS: 9,  # healing potion
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

    # Phương thức thêm các quan sát về thuộc tính của một ô
    def add_observation(self, y, x, cell):
        adj_cells = self.get_adjacent_cells(y, x)

        # Nếu có gió nhẹ, suy luận rằng có hố ở các ô liền kề
        if cell.is_breeze:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause([self.pos_literal(ay, ax, Object.PIT)])

        # Nếu có mùi hôi, suy luận rằng có Wumpus ở các ô liền kề
        if cell.is_stench:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause(
                    [self.pos_literal(ay, ax, Object.WUMPUS)]
                )

        # Nếu có mùi khí độc, suy luận rằng có khí độc ở các ô liền kề
        if cell.is_whiff:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause(
                    [self.pos_literal(ay, ax, Object.POISONOUS_GAS)]
                )

        # Nếu có ánh sáng, suy luận rằng có bình chữa bệnh ở các ô liền kề
        if cell.is_glow:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause(
                    [self.pos_literal(ay, ax, Object.HEALING_POTIONS)]
                )

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
        clause = [self.neg_literal(y, x, Object.PIT)]  # Check for absence of Pit
        return not self.knowledge_base.infer(clause)

    # Method to check if a cell contains a Wumpus using the knowledge base
    def check_Wumpus(self, y, x):
        clause = [self.neg_literal(y, x, Object.WUMPUS)]
        return not self.knowledge_base.infer(clause)

    # Method to check if a cell contains Poisonous Gas using the knowledge base
    def check_Poisonous_Gas(self, y, x):
        clause = [self.neg_literal(y, x, Object.POISONOUS_GAS)]
        return not self.knowledge_base.infer(clause)

    # Method to check if a cell contains Healing Potions using the knowledge base
    def check_Healing_Potions(self, y, x):
        clause = [self.neg_literal(y, x, Object.HEALING_POTIONS)]
        return not self.knowledge_base.infer(clause)

    # Method to perform an action based on the agent's decision
    def perform_action(self, action, program, target=None):
        if action == Action.MOVE_FORWARD:
            if self.move_forward(program):
                return True
        elif action == Action.TURN_LEFT:
            self.turn_left()
            return True
        elif action == Action.TURN_RIGHT:
            self.turn_right()
            return True
        elif action == Action.GRAB:
            self.grab(program)
            return True
        elif action == Action.SHOOT:
            self.shoot(target, program)
            return True
        elif action == Action.CLIMB:
            self.climb()
            return True
        elif action == Action.HEAL:
            self.heal()
            return True
        return False

    # Method to move the agent forward in the current direction
    def move_forward(self, program):
        dx, dy = Directions.get_movement_vector(self.direction)
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < self.map_size and 0 <= new_y < self.map_size:
            if (new_y, new_x) in self.safe_cells:
                self.x, self.y = new_x, new_y
                self.point -= 10
                self.explored_cells.add((self.y, self.x))
                self.perceive_current_cell(program)
                return True
            else:
                print("Cannot move to an unsafe cell!")
        return False

    # Method to turn the agent left
    def turn_left(self):
        self.direction = Directions.turn_left(self.direction)
        print("Turn left: ", self.direction)
        self.point -= 10

    # Method to turn the agent right
    def turn_right(self):
        self.direction = Directions.turn_right(self.direction)
        print("Turn right: ", self.direction)
        self.point -= 10

    # Method to grab gold or healing potions in the current cell
    def grab(self, program):
        cell = program.cells[self.y][self.x]
        if Object.GOLD in cell.element:  # Check if gold ("G") is in the current cell
            self.has_gold = True  # Mark the gold as grabbed
            self.point += 5000  # add points for grabbing gold
            cell.element.remove(Object.GOLD)
            print(f"Gold grabbed at ({self.y}, {self.x})")
        if (
            Object.HEALING_POTIONS in cell.element
        ):  # check if the healing potion ("H_P") is in the current cell
            self.healing_potion += 1  # Update the number of healing potion
            cell.element.remove(
                Object.HEALING_POTIONS
            )  # Remove the healing potion from the cell
            self.point -= 10  # deduct points for grabbing healing potion
            cell.remove_glow()
            print(f"Healing potion grabbed at ({self.y}, {self.x}) !!!")
        else:
            print("Nothing to grab here !!!")

    # Method to shoot an arrow at a target cell
    def shoot(self, target, program):
        dx, dy = Directions.get_movement_vector(self.direction)
        arrow_x, arrow_y = self.x + dx, self.y + dy

        # Loop to move the arrow until it hits a wall or target
        while 0 <= arrow_x < self.map_size and 0 <= arrow_y < self.map_size:
            if (
                Object.WUMPUS in program.cells[arrow_y][arrow_x].element
            ):  # If arrow hits the Wumpus
                program.cells[arrow_y][arrow_x].element.remove(
                    Object.WUMPUS
                )  # Remove Wumpus
                self.killing_wumpus = True  # Mark the Wumpus as killed
                # Add a clause to the knowledge base that the Wumpus is dead
                self.knowledge_base.add_clause(
                    [self.neg_literal(arrow_y, arrow_x, Object.WUMPUS)]
                )
                print(f"Wumpus killed at ({arrow_y}, {arrow_x})")
                break
            arrow_x += dx
            arrow_y += dy
        self.point -= 10
        print("Arrow shoot !!!")

    # Method to climb out of the cave and end the game if the agent has gold.
    def climb(self):
        if (
            self.x == 0 and self.y == 0
        ):  # Check if the agent is at the starting position with the gold.
            self.point += 10
            print(
                f"Agent exits the cave with {self.point} points."
            )  # print the final score.
            self.is_alive = False  # mark the agent as no longer active (GAME OVER)
        else:
            print("You can only climb out at the starting position (0,0) !!!")

    # Method to heal the agent if it has a healing potion
    def heal(self):
        if self.healing_potion > 0:  # Check if the agent has any healing potions
            self.current_hp = min(
                self.current_hp + 25, 100
            )  # Restore the health points, up to a maximum of 100.
            self.healing_potion -= 1  # decrease the number of healing potions
            self.point -= 10  # deduct points for using a healing potion
            print("Agent healed !!!")
        else:
            print("No healing potion available !!!")

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

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

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
            self.point -= 10000  # Deduct points for encountering a Wumpus
            self.shoot((ny, nx), program)
            if Object.WUMPUS in cell.element:  # If the Wumpus is present in the cell
                cell.set_scream()  # Set scream in the cell where Wumpus is shot
                self.update_map_after_wumpus_killed(
                    ny, nx, program
                )  # Update map after Wumpus is killed
        elif self.check_Poisonous_Gas(
            ny, nx
        ):  # Check if there's Poisonous Gas in the cell
            self.current_hp -= 0.25 * self.current_hp  # Reduce health points by 25%
        if self.check_Healing_Potions(ny, nx):
            self.grab(program)

    # Method to update the map after killing a Wumpus
    def update_map_after_wumpus_killed(self, y, x, program):
        adj_cells = self.get_adjacent_cells(y, x)  # Get adjacent cells of the Wumpus
        for ay, ax in adj_cells:
            if (
                Object.STENCH in program.cells[ay][ax].element
            ):  # If stench is present in adjacent cells
                program.cells[ay][ax].element.remove(Object.STENCH)

    # Helper method to return to the starting position after exploration
    def return_to_start(self, path):
        while path:
            action, _ = path.pop()
            self.perform_action(Action.TURN_LEFT)  # Adjust direction to move back
            self.perform_action(action)

    # Helper method to get valid movement directions
    def get_movement_directions(self):
        return Directions.get_movement_vector(self.direction)

    # Helper method to check if a position is within map bounds
    def is_within_bounds(self, x, y):
        return 0 <= x < self.map_size and 0 <= y < self.map_size

    def get_action(self, program):
        # Check for termination conditions
        if self.current_hp <= 0:
            print("Loser !!!")
            return None

        current_cell = program.cells[self.y][self.x]

        # Check for immediate actions
        if Object.GOLD in current_cell.element:
            return Action.GRAB
        if Object.HEALING_POTIONS in current_cell.element:
            return Action.GRAB
        if Object.WUMPUS in current_cell.element:
            return Action.SHOOT

        # Use DFS to find the next move
        path = self.dfs(program)
        if path:
            direction, (ny, nx) = path[0]

            # Determine the correct action based on direction
            movement_vector = Directions.get_movement_vector(self.direction)
            dx, dy = movement_vector

            if direction == (-1, 0):  # UP
                if self.direction == Directions.UP:
                    print("The agent is move forward")
                    return Action.MOVE_FORWARD
                elif self.direction == Directions.LEFT:
                    print("The agent is turn right")
                    return Action.TURN_RIGHT
                elif self.direction == Directions.RIGHT:
                    print("The agent is turn left")
                    return Action.TURN_LEFT
                else:
                    return Action.TURN_LEFT  # if DOWN, turn left twice to go UP

            elif direction == (1, 0):  # DOWN
                if self.direction == Directions.DOWN:
                    return Action.MOVE_FORWARD
                elif self.direction == Directions.LEFT:
                    return Action.TURN_LEFT
                elif self.direction == Directions.RIGHT:
                    return Action.TURN_RIGHT
                else:
                    return Action.TURN_LEFT  # if UP, turn left twice to go DOWN

            elif direction == (0, -1):  # LEFT
                if self.direction == Directions.LEFT:
                    return Action.MOVE_FORWARD
                elif self.direction == Directions.UP:
                    return Action.TURN_LEFT
                elif self.direction == Directions.DOWN:
                    return Action.TURN_RIGHT
                else:
                    return Action.TURN_LEFT  # if RIGHT, turn left twice to go LEFT

            elif direction == (0, 1):  # RIGHT
                if self.direction == Directions.RIGHT:
                    return Action.MOVE_FORWARD
                elif self.direction == Directions.UP:
                    return Action.TURN_RIGHT
                elif self.direction == Directions.DOWN:
                    return Action.TURN_LEFT
                else:
                    return Action.TURN_LEFT  # if LEFT, turn left twice to go RIGHT

        # If no path is found, return to start or explore unexplored cells
        if self.has_gold:
            return (
                Action.CLIMB
                if (self.y == 0 and self.x == 0)
                else self.return_to_start(path)
            )

        return None

    def is_dead(self):
        return not self.is_alive

    def has_exited(self):
        return self.has_gold and self.x == 0 and self.y == 0
