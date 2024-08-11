import os
import time
from colorama import Fore, Back, Style, init

# Initialize colorama for colored output in terminal
init(autoreset=True)


class WumpusWorldUI:
    """
    A class to handle the User Interface for the Wumpus World game.
    It displays the game map, logs actions, and saves the result to a file.
    """

    def __init__(self, program, agent):
        """
        Initializes the WumpusWorldUI with the provided program and agent.

        :param program: The current state of the Wumpus World.
        :param agent: The agent exploring the Wumpus World.
        """
        self.program = program
        self.agent = agent
        self.actions = []  # List to store actions taken by the agent
        self.path = []  # List to store the path taken by the agent

    def display_map(self):
        """
        Displays the current state of the Wumpus World map in the terminal.
        Clears the screen before displaying the map.
        """
        # Clear the terminal screen
        os.system("cls" if os.name == "nt" else "clear")

        print("Wumpus World")
        print("============\n")

        # Iterate over each cell in the map
        for row in self.program.cells:
            for cell in row:
                cell_display = " "

                # Determine the cell's display based on its elements
                if "W" in cell.element:
                    cell_display = Fore.RED + "W"  # Wumpus in red
                elif "P" in cell.element:
                    cell_display = Fore.YELLOW + "P"  # Pit in yellow
                elif "G" in cell.element:
                    cell_display = Fore.GREEN + "G"  # Gold in green
                elif "H_P" in cell.element:
                    cell_display = Fore.CYAN + "H"  # Healing Potion in cyan
                elif "P_G" in cell.element:
                    cell_display = Fore.MAGENTA + "G"  # Poison Gas in magenta
                elif "A" in cell.element:
                    cell_display = Fore.WHITE + "A"  # Agent in white

                # Collect percepts for the current cell
                percept_display = []
                if cell.is_stench:
                    percept_display.append(Fore.RED + "S")  # Stench in red
                if cell.is_breeze:
                    percept_display.append(Fore.YELLOW + "B")  # Breeze in yellow
                if cell.is_whiff:
                    percept_display.append(Fore.MAGENTA + "W")  # Whiff in magenta
                if cell.is_glow:
                    percept_display.append(Fore.CYAN + "G")  # Glow in cyan

                # Combine percepts into a single string
                percept_str = "".join(percept_display)

                # Print cell with its percepts
                print(f"[{cell_display}{percept_str}]", end=" ")
            print()
        print("\n")

    def log_action(self, action):
        """
        Logs the agent's action with its current position and records the path.

        :param action: The action taken by the agent.
        """
        y, x = self.agent.get_current_cell()  # Get the current cell of the agent
        self.actions.append(f"({y + 1},{x + 1}): {action}")  # Append action to the log
        self.path.append((y + 1, x + 1))  # Record the agent's position in the path

    def save_result(self, file_name="output/result1.txt"):
        """
        Saves the result of the game to a specified file.

        :param file_name: The name of the file where results will be saved.
        """
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        # Write actions to the specified file
        with open(file_name, "w") as file:
            file.write("Actions:\n")
            for action in self.actions:
                file.write(action + "\n")

            file.write("\nPath:\n")
            for y, x in self.path:
                file.write(f"({y},{x})\n")

        print(f"Result saved to {file_name}")

    def game_loop(self):
        """
        Main game loop where the agent autonomously explores the Wumpus World.
        The loop continues until the game ends.
        """
        game_over = False
        while not game_over:
            self.display_map()  # Display the current state of the map

            # Debugging statement
            print("Getting next action...")

            # Get the next action from the agent
            action = self.agent.get_action(self.program)

            # Debugging statement
            print(f"Action: {action}")

            self.log_action(action)  # Log the action taken by the agent

            # Perform the action in the game world
            self.agent.perform_action(action, self.program)

            # Debugging statement
            print("Action performed, checking game state...")

            # Check if the game has ended based on the agent's state
            if self.agent.is_dead() or self.agent.has_exited():
                game_over = True

            # Pause briefly to enhance user experience
            time.sleep(1)

        self.display_map()  # Display the final state of the map
        self.save_result()  # Save the result of the game
