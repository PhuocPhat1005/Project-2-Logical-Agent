from algorithms.knowledge_base import KnowledgeBase
from utils.util import Action


class Agent:
    def __init__(self, map_size=10):
        self.x = 0
        self.y = 0
        self.current_hp = 100
        self.map_size = map_size
        self.knowledge_base = KnowledgeBase()
        self.healing_potion = 0
        self.point = 0
        self.direction = "right"
        self.action = []
        self.knowledge_base.add_clause([self.pos_literal(0, 0, "safe")])

    def pos_literal(self, y, x, prop):
        return self.encode(y, x, prop)

    def neg_literal(self, y, x, prop):
        return -self.encode(y, x, prop)

    def encode(self, y, x, prop):
        prop_offset = {
            "safe": 1,
            "breeze": 2,
            "stench": 3,
            "whiff": 4,
            "glow": 5,
            "scream": 6,
        }
        return (
            x * self.map_size * len(prop_offset)
            + y * len(prop_offset)
            + prop_offset[prop]
        )

    def get_adjacent_cells(self, y, x):
        adjacent = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.map_size and 0 <= ny < self.map_size:
                adjacent.append((ny, nx))
        return adjacent

    def add_observation(self, y, x, cell):
        adj_cells = self.get_adjacent_cells(y, x)
        for ay, ax in adj_cells:
            if not cell[ay][ax].is_safe:
                if cell[y][x].is_breeze:
                    self.knowledge_base.add_clause([self.pos_literal(ay, ax, "Pit")])
                if cell[y][x].is_stench:
                    self.knowledge_base.add_clause([self.pos_literal(ay, ax, "Wumpus")])
                if cell[y][x].is_whiff:
                    self.knowledge_base.add_clause(
                        [self.pos_literal(ay, ax, "Poisonous Gas")]
                    )
                if cell[y][x].is_glow:
                    self.knowledge_base.add_clause(
                        [self.pos_literal(ay, ax, "Healing Potions")]
                    )

    def check_Pit(self, y, x):
        # Infer whether there is a pit at (y, x) using the knowledge base
        clause = [self.neg_literal(y, x, "Pit")]
        return not self.knowledge_base.infer(clause)

    def check_Wumpus(self, y, x):
        # Infer whether there is a Wumpus at (y, x) using the knowledge base
        clause = [self.neg_literal(y, x, "Wumpus")]
        return not self.knowledge_base.infer(clause)

    def check_Poisonous_Gas(self, y, x):
        # Infer whether there is poisonous gas at (y, x) using the knowledge base
        clause = [self.neg_literal(y, x, "Poisonous Gas")]
        return not self.knowledge_base.infer(clause)

    def check_Healing_Potions(self, y, x):
        clause = [self.neg_literal(y, x, "Healing Potions")]
        return not self.knowledge_base.infer(clause)

    def dfs(self, program):
        start_cell = program.cells[0][0]
        frontier = [start_cell]
        path = []

        while frontier:
            current_cell = frontier.pop()
            program.cells[current_cell.y][current_cell.x].set_discovery()
            self.add_observation(current_cell.y, current_cell.x, program.cells)

            if self.direction == "right":
                directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]
            elif self.direction == "left":
                directions = [(-1, 0), (0, 1), (0, -1), (1, 0)]
            elif self.direction == "up":
                directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
            elif self.direction == "down":
                directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

            for dy, dx, i in enumerate(directions):
                nx, ny = current_cell.x + dx, current_cell.y + dy
                if 0 <= nx < program.map_size and 0 <= ny < program.map_size:
                    if program.cells[ny][nx].get_discovery():
                        continue

                    if self.check_Pit(ny, nx):
                        continue
                    elif self.check_Wumpus(ny, nx):
                        self.point -= 100
                        self.action.append((Action.SHOOT, (ny, nx)))
                        self.point -= 100
                        if "Wumpus" in program.cells[ny][nx].element:
                            program.cells[ny][nx].set_scream()

                    elif self.check_Poisonous_Gas(ny, nx):
                        self.current_hp -= 25
                        if self.current_hp <= 0:
                            if self.healing_potion > 0:
                                self.healing_potion -= 1
                                self.current_hp = 25
                            else:
                                continue

                    if self.check_Healing_Potions(ny, nx):
                        self.healing_potion += 1
                        self.point += 5000

                    frontier.append(program.cells[ny][nx])
                    path.append((Action.MOVE_FORWARD, (ny, nx)))

        return path
