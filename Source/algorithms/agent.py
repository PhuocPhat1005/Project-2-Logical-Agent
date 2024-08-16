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
        self.knowledge_base.add_clause([self.neg_literal(0, 0, Object.PIT.value)])
        self.knowledge_base.add_clause([self.neg_literal(0, 0, Object.WUMPUS.value)])
        self.knowledge_base.add_clause(
            [self.neg_literal(0, 0, Object.HEALING_POTIONS.value)]
        )
        self.knowledge_base.add_clause(
            [self.neg_literal(0, 0, Object.POISONOUS_GAS.value)]
        )
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
            Object.BREEZE.value: 1,  # breeze
            Object.STENCH.value: 2,  # stench
            Object.WHIFF.value: 3,  # whiff
            Object.GLOW.value: 4,  # glow
            Object.SCREAM.value: 5,  # scream
            Object.PIT.value: 6,  # pit
            Object.WUMPUS.value: 7,  # wumpus
            Object.POISONOUS_GAS.value: 8,  # poisonous gas
            Object.HEALING_POTIONS.value: 9,  # healing potion
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
            (-1, 0),  # up
            (1, 0),  # down
            (0, -1),  # left
            (0, 1),  # right
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
        print("Adjacent cells: ", adj_cells)

        # Nếu có gió nhẹ, suy luận rằng có hố ở các ô liền kề
        if cell.is_breeze:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause(
                    [self.pos_literal(ay, ax, Object.PIT.value)]
                )

        # Nếu có mùi hôi, suy luận rằng có Wumpus ở các ô liền kề
        if cell.is_stench:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause(
                    [self.pos_literal(ay, ax, Object.WUMPUS.value)]
                )

        # Nếu có mùi khí độc, suy luận rằng có khí độc ở các ô liền kề
        if cell.is_whiff:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause(
                    [self.pos_literal(ay, ax, Object.POISONOUS_GAS.value)]
                )

        # Nếu có ánh sáng, suy luận rằng có bình chữa bệnh ở các ô liền kề
        if cell.is_glow:
            for ay, ax in adj_cells:
                self.knowledge_base.add_clause(
                    [self.pos_literal(ay, ax, Object.HEALING_POTIONS.value)]
                )

    # Method to update the set of safe cells based on the knowledge base
    def update_safe_cells(self, neighbors):
        """
        Update the set of safe cells based on the knowledge base.

        Muc dich: cap nhat tap hop cac o co an toan (safe_cells) bang cach kiem tra tung o lien ke trong danh sach neighbors

        """
        for ny, nx in neighbors:
            if self.check_safety(ny, nx):  # Check if neighboring cells are safe
                self.safe_cells.add((ny, nx))

    def check_safety(self, y, x):
        """
        Kiểm tra xem một ô có an toàn không bằng cách đảm bảo rằng nó không chứa các yếu tố nguy hiểm.

        Args:
            y (int): Tọa độ dòng (row) của ô cần kiểm tra.
            x (int): Tọa độ cột (column) của ô cần kiểm tra.

        Returns:
            bool: Trả về True nếu ô không chứa hố (Pit), Wumpus, hoặc khí độc (Poisonous Gas),
                và do đó được coi là an toàn. Ngược lại, trả về False nếu ô có bất kỳ yếu tố
                nguy hiểm nào.
        """
        return not any(
            [
                self.check_Pit(y, x),
                self.check_Wumpus(y, x),
                self.check_Poisonous_Gas(y, x),
            ]
        )

    # Method to check if a cell contains a Pit using the knowledge base
    def check_Pit(self, y, x):
        """
        Kiểm tra xem ô tại tọa độ (y, x) có chứa hố (Pit) hay không.

        Args:
            y (int): Tọa độ hàng của ô cần kiểm tra.
            x (int): Tọa độ cột của ô cần kiểm tra.

        Returns:
            bool: Trả về True nếu cơ sở tri thức có thể suy luận rằng ô này có chứa hố (Pit),
                ngược lại trả về False.
        """
        clause = [
            self.pos_literal(y, x, Object.PIT.value)
        ]  # Kiểm tra sự hiện diện của hố tại ô này
        return self.knowledge_base.infer(clause)

    # Method to check if a cell contains a Wumpus using the knowledge base
    def check_Wumpus(self, y, x):
        """Check if a cell contains a Wumpus using the knowledge base.

        Args:
            y (int): The y-coordinate of the cell.
            x (int): The x-coordinate of the cell.

        Returns:
            bool: True if the cell contains a Wumpus, False otherwise.
        """
        clause = [self.pos_literal(y, x, Object.WUMPUS.value)]
        return self.knowledge_base.infer(clause)

    # Method to check if a cell contains Poisonous Gas using the knowledge base
    def check_Poisonous_Gas(self, y, x):
        """Check if a cell contains Poisonous Gas using the knowledge base.

        Args:
            y (int): The y-coordinate of the cell.
            x (int): The x-coordinate of the cell.

        Returns:
            bool: True if the cell contains Poisonous Gas, False otherwise.
        """
        clause = [self.pos_literal(y, x, Object.POISONOUS_GAS.value)]
        return self.knowledge_base.infer(clause)

    # Method to check if a cell contains Healing Potions using the knowledge base
    def check_Healing_Potions(self, y, x):
        """Check if a cell contains Healing Potions using the knowledge base.

        Args:
            y (int): The y-coordinate of the cell.
            x (int): The x-coordinate of the cell.

        Returns:
            bool: True if the cell contains Healing Potions, False otherwise.
        """
        clause = [self.pos_literal(y, x, Object.HEALING_POTIONS.value)]
        return self.knowledge_base.infer(clause)

    # Method to perform an action based on the agent's decision
    def perform_action(self, action, program, target=None):
        """
        Thực hiện một hành động dựa trên quyết định của agent.

        Args:
            action (Action): Hành động mà agent sẽ thực hiện.
                             Có thể là một trong các hành động được định nghĩa trong enum Action.
            program (Program): Đối tượng Program, quản lý trạng thái của bản đồ và trò chơi.
            target (tuple, optional): Tọa độ mục tiêu (ny, nx) cho hành động, ví dụ như khi bắn Wumpus.
                                      Mặc định là None.

        Returns:
            bool: Trả về True nếu hành động được thực hiện thành công, ngược lại trả về False.
        """
        print("brruhhhhh")
        # Kiểm tra nếu hành động là di chuyển về phía trước
        if action == Action.MOVE_FORWARD:
            # Thực hiện di chuyển về phía trước và kiểm tra xem nó có thành công không
            print("move forward")
            if self.move_forward(program):
                print("move forward")
                return True
        # Kiểm tra nếu hành động là quay sang trái
        elif action == Action.TURN_LEFT:
            print("turn left")
            self.turn_left()
            return True
        # Kiểm tra nếu hành động là quay sang phải
        elif action == Action.TURN_RIGHT:
            print("turn right")
            self.turn_right()
            return True
        # Kiểm tra nếu hành động là nhặt đồ vật
        elif action == Action.GRAB:
            print("grab")
            self.grab(program)
            return True
        # Kiểm tra nếu hành động là bắn
        elif action == Action.SHOOT:
            print("shoot")
            self.shoot(target, program)
            return True
        # Kiểm tra nếu hành động là leo lên (thoát ra khỏi hang)
        elif action == Action.CLIMB:
            print("climb")
            self.climb()
            return True
        # Kiểm tra nếu hành động là hồi máu
        elif action == Action.HEAL:
            print("heal")
            self.heal()
            return True
        # Nếu không có hành động nào khớp, trả về
        print("hello")
        return False

    # Helper method to check if a position is within map bounds
    def is_within_bounds(self, x, y):
        return 0 <= x < self.map_size and 0 <= y < self.map_size

    # Method to move the agent forward in the current direction
    def move_forward(self, program):
        """
        Di chuyển agent về phía trước theo hướng hiện tại.

        Phương thức này tính toán vị trí tiếp theo của tác tử dựa trên hướng hiện tại của nó.
        Nếu ô tiếp theo nằm trong giới hạn của bản đồ và được đánh dấu là an toàn, tác tử
        sẽ di chuyển đến ô đó, cập nhật điểm số và cảm nhận môi trường mới.

        :param program: Đối tượng chương trình chịu trách nhiệm xử lý trạng thái của môi trường.
        :return: Trả về True nếu tác tử di chuyển thành công; False nếu không.
        """
        # Lấy vector di chuyển (dx, dy) dựa trên hướng hiện tại của tác tử.
        # Vector này cho biết ta cần di chuyển bao nhiêu theo hướng x và y.
        dy, dx = Directions.get_movement_vector(self.direction)
        # Tính toán tọa độ mới (new_x, new_y) nơi tác tử sẽ di chuyển đến.
        new_y, new_x = self.y + dy, self.x + dx
        # Kiểm tra xem vị trí mới có nằm trong giới hạn của bản đồ không.
        if self.is_within_bounds(new_x, new_y):
            # Kiểm tra xem vị trí mới có phải là ô an toàn đã biết không.
            if (new_y, new_x) in self.safe_cells:
                # Cập nhật vị trí của agent sang tọa độ mới.
                self.x, self.y = new_x, new_y
                # Trừ 10 điểm từ điểm số của agent cho hành động di chuyển.
                self.point -= 10
                # Thêm vị trí mới vào tập hợp các ô đã khám phá.
                self.explored_cells.add((self.y, self.x))
                # Cảm nhận môi trường hiện tại của ô và cập nhật cơ sở tri thức của agent.
                self.perceive_current_cell(program)
                # Trả về True, báo hiệu agent đã di chuyển thành công.
                return True
            else:
                # In ra thông báo báo hiệu không thể di chuyển do ô không an toàn.
                print("Cannot move to an unsafe cell!")
        print("Error: Can not move !!!")
        # Trả về False nếu việc di chuyển không thành công (nằm ngoài giới hạn hoặc không an toàn).
        return False

    # Method to turn the agent left
    def turn_left(self):
        """
        Quay trái: Thay đổi hướng của agent về phía bên trái theo hướng hiện tại.

        Phương thức này điều chỉnh hướng của agent theo chiều kim đồng hồ, sau đó cập nhật
        điểm số của tác tử với một hình phạt cho hành động quay.

        :return: None
        """
        # Thay đổi hướng của tác tử sang trái dựa trên hướng hiện tại.
        self.direction = Directions.turn_left(self.direction)
        print("Turn left: ", self.direction)
        # Trừ 10 điểm từ điểm số của tác tử cho hành động quay trái.
        self.point -= 10

    # Method to turn the agent right
    def turn_right(self):
        """
        Quay phai: Thay đổi hướng của agent về phía bên phai theo hướng hiện tại.

        Phương thức này điều chỉnh hướng của agent theo chiều kim đồng hồ, sau đó cập nhật
        điểm số của tác tử với một hình phạt cho hành động quay.

        :return: None
        """
        self.direction = Directions.turn_right(self.direction)
        print("Turn right: ", self.direction)
        self.point -= 10

    # Method to grab gold or healing potions in the current cell
    def grab(self, program):
        """
        Phương thức để agent nhặt vàng hoặc bình thuốc hồi phục trong ô hiện tại.

        :param program: Đối tượng chương trình, chứa thông tin về các ô trên bản đồ.
        """
        cell = program.cells[self.y][
            self.x
        ]  # Lấy thông tin của ô hiện tại nơi agent đang đứng
        if (
            Object.GOLD.value in cell.element
        ):  # Check if gold ("G") is in the current cell
            self.has_gold = True  # Mark the gold as grabbed
            self.point += 5000  # add points for grabbing gold
            cell.element.remove(Object.GOLD)
            print(f"Gold grabbed at ({self.y}, {self.x})")
        if (
            Object.HEALING_POTIONS.value in cell.element
        ):  # check if the healing potion ("H_P") is in the current cell
            self.healing_potion += 1  # Update the number of healing potion
            cell.element.remove(
                Object.HEALING_POTIONS.value
            )  # Remove the healing potion from the cell
            self.point -= 10  # deduct points for grabbing healing potion
            cell.remove_glow()
            print(f"Healing potion grabbed at ({self.y}, {self.x}) !!!")
        else:
            self.point -= 10
            print("Nothing to grab here !!!")

    # Method to shoot an arrow at a target cell
    def shoot(self, program):
        dy, dx = Directions.get_movement_vector(self.direction)
        arrow_x, arrow_y = self.x + dx, self.y + dy

        # Loop to move the arrow until it hits a wall or target
        while self.is_within_bounds(arrow_x, arrow_y):
            if (
                Object.WUMPUS.value in program.cells[arrow_y][arrow_x].element
            ):  # If arrow hits the Wumpus
                program.cells[arrow_y][arrow_x].element.remove(
                    Object.WUMPUS.value
                )  # Remove Wumpus
                self.killing_wumpus = True  # Mark the Wumpus as killed
                # Add a clause to the knowledge base that the Wumpus is dead
                self.knowledge_base.add_clause(
                    [self.neg_literal(arrow_y, arrow_x, Object.WUMPUS.value)]
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
            self.x == 0 and self.y == 0 and self.has_gold == True
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
        trace_path = []  # To store the complete path of the agent's movement
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
                        trace_path.append((direction, (ny, nx)))  # Track the movement
                        self.explored_cells.add((ny, nx))  # Mark this cell as explored

                    else:
                        self.handle_danger(
                            ny, nx, program
                        )  # Handle dangerous cells (e.g., shoot Wumpus)

            # Check if the agent has returned to the starting position or died
            if self.current_hp <= 0 or (self.y == 0 and self.x == 0 and self.has_gold):
                break

        return path, trace_path

    # Method to handle perceived dangers in a cell and update the knowledge base
    def handle_danger(self, ny, nx, program):
        """Handle perceived dangers and update the knowledge base accordingly."""
        cell = program.cells[ny][nx]  # Get the cell at the given position
        if self.check_Wumpus(ny, nx):  # Check if there's a Wumpus in the cells
            print(f"Encountered Wumpus at ({ny}, {nx})")
            self.point -= 10000  # Deduct points for encountering a Wumpus
            self.shoot((ny, nx), program)
            if (
                Object.WUMPUS.value in cell.element
            ):  # If the Wumpus is present in the cell
                print("Wumpus shot!")
                cell.set_scream()  # Set scream in the cell where Wumpus is shot
                self.update_map_after_wumpus_killed(
                    ny, nx, program
                )  # Update map after Wumpus is killed
        elif self.check_Poisonous_Gas(
            ny, nx
        ):  # Check if there's Poisonous Gas in the cell
            print(f"Encountered Poisonous Gas at ({ny}, {nx})")
            self.current_hp -= 0.25 * self.current_hp  # Reduce health points by 25%
        if self.check_Healing_Potions(ny, nx):
            print(f"Found Healing Potion at ({ny}, {nx})")
            self.grab(program)

    # Method to update the map after killing a Wumpus
    def update_map_after_wumpus_killed(self, y, x, program):
        adj_cells = self.get_adjacent_cells(y, x)  # Get adjacent cells of the Wumpus
        for ay, ax in adj_cells:
            if (
                Object.STENCH.value in program.cells[ay][ax].element
            ):  # If stench is present in adjacent cells
                program.cells[ay][ax].element.remove(Object.STENCH.value)

    def get_action(self, program):
        # Check for termination conditions
        if self.current_hp <= 0:
            print("Loser !!!")
            return None

        current_cell = program.cells[self.y][self.x]

        # Check for immediate actions
        if Object.GOLD.value in current_cell.element:
            return Action.GRAB
        if Object.HEALING_POTIONS.value in current_cell.element:
            return Action.GRAB
        if Object.WUMPUS.value in current_cell.element:
            return Action.SHOOT

        # Use DFS to find the next move
        path, trace_path = self.dfs(program)
        if path:
            direction, (ny, nx) = path[0]
            movement_action = self.determine_movement_action(direction)
            self.update_agent_state(direction, (ny, nx), program)
            return movement_action

        # If no path is found, return to start or explore unexplored cells
        if self.has_gold:
            return (
                Action.CLIMB
                if (self.y == 0 and self.x == 0)
                else self.return_to_start(trace_path)
            )

        return None

    def return_to_start(self, path):
        """Return the agent to the starting position (0,0)."""
        start_position = (0, 0)
        reversed_path = []

        # Trace back from the current position to the start
        current_position = (self.y, self.x)

        # Build a reverse path from the current position to the start
        while current_position != start_position:
            for direction, (ny, nx) in path:
                if (ny, nx) == current_position:
                    reversed_path.append(
                        ((-direction[0], -direction[1]), (self.y, self.x))
                    )
                    current_position = (self.y - direction[1], self.x - direction[0])
                    break

        return reversed_path

    def update_agent_state(self, direction, new_position, program):
        """Update the agent's state after performing an action."""
        # Update the agent's position
        self.y, self.x = new_position

        # Optionally, update the agent's direction if it was changed
        if direction == (-1, 0):  # Moving UP
            self.direction = Directions.UP
        elif direction == (1, 0):  # Moving DOWN
            self.direction = Directions.DOWN
        elif direction == (0, -1):  # Moving LEFT
            self.direction = Directions.LEFT
        elif direction == (0, 1):  # Moving RIGHT
            self.direction = Directions.RIGHT

        # Optionally, update other relevant states or the knowledge base
        self.perceive_current_cell(
            program
        )  # Re-perceive the new cell to update knowledge

    def determine_movement_action(self, direction):
        """Determine the action needed based on the current and target direction."""
        if direction == (-1, 0):  # UP
            if self.direction == Directions.UP:
                return Action.MOVE_FORWARD
            elif self.direction == Directions.LEFT:
                return Action.TURN_RIGHT
            elif self.direction == Directions.RIGHT:
                return Action.TURN_LEFT
            else:  # DOWN
                return Action.TURN_LEFT

        elif direction == (1, 0):  # DOWN
            if self.direction == Directions.DOWN:
                return Action.MOVE_FORWARD
            elif self.direction == Directions.LEFT:
                return Action.TURN_LEFT
            elif self.direction == Directions.RIGHT:
                return Action.TURN_RIGHT
            else:  # UP
                return Action.TURN_RIGHT

        elif direction == (0, -1):  # LEFT
            if self.direction == Directions.LEFT:
                return Action.MOVE_FORWARD
            elif self.direction == Directions.UP:
                return Action.TURN_LEFT
            elif self.direction == Directions.DOWN:
                return Action.TURN_RIGHT
            else:  # RIGHT
                return Action.TURN_RIGHT

        elif direction == (0, 1):  # RIGHT
            if self.direction == Directions.RIGHT:
                return Action.MOVE_FORWARD
            elif self.direction == Directions.UP:
                return Action.TURN_RIGHT
            elif self.direction == Directions.DOWN:
                return Action.TURN_LEFT
            else:  # LEFT
                return Action.TURN_LEFT

        return None

    def is_dead(self):
        return not self.is_alive

    def has_exited(self):
        return self.has_gold and self.x == 0 and self.y == 0
