from algorithms.program import Program
from algorithms.agent import Agent
from utils.test import WumpusWorldUI


def main():
    program = Program(file_path="input/map1.txt")
    agent = Agent(map_size=program.map_size)

    ui = WumpusWorldUI(program, agent)
    ui.game_loop()


if __name__ == "__main__":
    main()
