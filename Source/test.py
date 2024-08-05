from pysat.formula import CNF
from pysat.solvers import Solver

class WumpusWorld:
    def __init__(self, size):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.knowledge_base = CNF()
        self.init_knowledge()

    def init_knowledge(self):
        # Initial knowledge: the starting position (0, 0) is safe
        self.knowledge_base.append([self.pos_literal(0, 0, 'safe')])

    def pos_literal(self, x, y, prop):
        return self.encode(x, y, prop)

    def neg_literal(self, x, y, prop):
        return -self.encode(x, y, prop)

    def encode(self, x, y, prop):
        prop_offset = {'safe': 1, 'breeze': 2, 'pit': 3, 'stench': 4, 'wumpus': 5, 'Poisonous Gas': 6}
        return x * self.size * len(prop_offset) + y * len(prop_offset) + prop_offset[prop]

    def adjacent_cells(self, x, y):
        # Get all valid adjacent cells
        adjacent = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                adjacent.append((nx, ny))
        return adjacent

    def add_observation(self, x, y, observation):
        if observation == 'breeze':
            self.knowledge_base.append([self.pos_literal(x, y, 'breeze')])
            # If there's a breeze, at least one adjacent cell has a pit
            adj_cells = self.adjacent_cells(x, y)
            self.knowledge_base.append([self.pos_literal(ax, ay, 'pit') for ax, ay in adj_cells])
        elif observation == 'stench':
            self.knowledge_base.append([self.pos_literal(x, y, 'stench')])
            # Add stench handling similar to breeze if needed
        # Add other observations similarly

    def check_safe(self, y, x):
        # Check if (y, x) is safe using the knowledge base
        with Solver(bootstrap_with=self.knowledge_base) as solver:
            # Add clauses for checking if (y, x) is not safe
            solver.add_clause([self.pos_literal(y, x, 'pit')])
            solver.add_clause([self.pos_literal(y, x, 'wumpus')])
            solver.add_clause([self.pos_literal(y, x, 'Poisonous Gas')])

            # If any of these clauses are satisfied, the cell is not safe
            # Solve to check if the negation of the safe condition is satisfiable
            return not solver.solve()

    def move(self, x, y, observation):
        self.add_observation(x, y, observation)
        if self.check_safe(y, x):
            print(f"Moved to ({x}, {y}) safely!")
        else:
            print(f"Cannot move to ({x}, {y}), it's not safe!")

def main():
    world_size = 4
    game = WumpusWorld(world_size)

    # Example moves (simulated observations)
    game.move(0, 1, 'breeze')
    game.move(1, 0, 'stench')
    # Add more moves and logic

if __name__ == "__main__":
    main()
