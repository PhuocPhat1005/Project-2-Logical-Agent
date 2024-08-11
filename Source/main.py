from algorithms.program import Program
from algorithms.agent import Agent
from utils.test import WumpusWorldUI
from utils.util import Object, Action
from algorithms.directions import Directions


def main():
    program = Program(file_path="input/map1.txt")
    agent = Agent(map_size=program.map_size)

    # ui = WumpusWorldUI(program, agent)
    # ui.game_loop()
    program.display_map_test()
    print("hahahaha")
    action = Action.MOVE_FORWARD
    agent.perform_action(action, program)
    print("Point: ", agent.point)
    print("hihihihi")


if __name__ == "__main__":
    main()
