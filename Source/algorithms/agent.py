from pysat.solvers import Solver
from pysat.formula import CNF


class Agent:
    def __init__(self, map_size=4):
        self.x = 0
        self.y = 0
        self.health = 100
        self.map_size = map_size
        self.knowledge_base = CNF()
        self.healing_potion = 0
        self.point = 0
        self.direction = "right"
        self.action = []
        # initialize the knowledge base with the starting position as safe
        self.knowledge_base.append([self.pos_literal(0, 0, "safe")])

    def pos_literal(self, y, x, prop):
        # Assign positive literals for propositions at (y, x)
        return self.encode(y, x, prop)

    def neg_literal(self, y, x, prop):
        # Assign negative literals for propositions at (y, x)
        return -self.encode(y, x, prop)

    # Vi CNF va SAT solver yeu cau cac menh de la so nguyen unique, ta can encode thanh so nguyen va tao ham bat ki de no unique
    def encode(self, y, x, prop):
        # Encode a unique number for each proposition
        # For simplicity, encode as x * size + y with offsets for each proposition
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
                    self.knowledge_base.append([self.pos_literal(ay, ax, "Pit")])
                if cell[y][x].is_stench:
                    self.knowledge_base.append([self.pos_literal(ay, ax, "Wumpus")])
                if cell[y][x].is_whiff:
                    self.knowledge_base.append(
                        [self.pos_literal(ay, ax, "Poisonous Gas")]
                    )
                if cell[y][x].is_glow:
                    self.knowledge_base.append(
                        [self.pos_literal(ay, ax, "Healing Potions")]
                    )

    def check_Pit(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, "Pit")])
            return not solver.solve()

    def check_Wumpus(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, "Wumpus")])
            return not solver.solve()

    def check_Poisonous_Gas(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, "Poisonous Gas")])
            return not solver.solve()

    def check_Healing_Potions(self, y, x):
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            solver.add_clause([self.neg_literal(y, x, "Healing Potions")])
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
