from algorithms.program import Program
from algorithms.agent import Agent
from utils.test import WumpusWorldUI
from utils.util import Object, Action
from algorithms.directions import Directions


def print_path(trace, actions):
    with open("output/result1.txt", "w") as f:
        for i, (pos, action) in enumerate(zip(trace, actions)):
            output = f"({pos[0]},{pos[1]}): {action.name.lower()}"
            print(output)
            f.write(output + "\n")


def main():
    program = Program(file_path="input/map1.txt")
    agent = Agent(map_size=program.map_size)

    trace = []
    actions = []

    while True:
        action = agent.get_action(program)
        if action is None:
            break
        actions.append(action)
        trace.append((agent.y, agent.x))

    print_path(trace, actions)


if __name__ == "__main__":
    main()
