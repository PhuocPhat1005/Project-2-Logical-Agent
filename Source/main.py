from algorithms.program import Program
from algorithms.agent import Agent
from algorithms.knowledge_base import KnowledgeBase
from algorithms.cell import Cell


def main():
    program = Program("input/map1.txt")
    program.display_map_test()
    # agent = Agent(map_size=program.map_size)
    # Example usage:
    # Initialize the grid with cells
    # Create a new knowledge base
    # kb = KnowledgeBase()

    # # Add some clauses to the knowledge base
    # kb.add_clause([1, -2])  # Clause: x1 ∨ ¬x2
    # kb.add_clause([-1, 2])  # Clause: ¬x1 ∨ x2

    # # Define some clauses to infer
    # not_alpha = [
    #     [-1, -2]
    # ]  # Clauses to check if they are implied by the knowledge base (¬x1 ∨ ¬x2)

    # # Perform inference
    # is_implied = kb.infer(not_alpha)

    # # Output result
    # print(
    #     f"Is the clause {not_alpha} implied by the knowledge base? {'Yes' if is_implied else 'No'}"
    # )
    # grid = [[Cell(y, x) for x in range(4)] for y in range(4)]

    # # Example cell updates to simulate a Wumpus World scenario
    # grid[1][1].set_breeze()  # Breeze at (1, 1), indicating a pit nearby
    # grid[2][2].set_stench()  # Stench at (2, 2), indicating a Wumpus nearby

    # # Create an agent and perform DFS
    # agent = Agent(map_size=4)
    # path = agent.dfs(grid)
    # print(path)


if __name__ == "__main__":
    main()
