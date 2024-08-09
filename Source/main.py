from algorithms.progam import Program
from algorithms.agent import Agent


def main():
    program = Program("input/map1.txt")
    program.display_map_test()
    agent = Agent(program.map_size)


if __name__ == "__main__":
    main()
