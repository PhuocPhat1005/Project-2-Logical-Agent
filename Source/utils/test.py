import os
import time
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)


class WumpusWorldUI:
    def __init__(self, program, agent):
        self.program = program
        self.agent = agent
        self.actions = []

    def display_map(self):
        """
        Displays the current state of the Wumpus World map.
        """
        os.system("cls" if os.name == "nt" else "clear")
        print("Wumpus World")
        print("============\n")
        for row in self.program.cells:
            for cell in row:
                cell_display = " "
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

                # Display percepts
                percept_display = []
                if cell.is_stench:
                    percept_display.append(Fore.RED + "S")
                if cell.is_breeze:
                    percept_display.append(Fore.YELLOW + "B")
                if cell.is_whiff:
                    percept_display.append(Fore.MAGENTA + "W")
                if cell.is_glow:
                    percept_display.append(Fore.CYAN + "G")

                percept_str = "".join(percept_display)
                print(f"[{cell_display}{percept_str}]", end=" ")
            print()
        print("\n")

    def log_action(self, action):
        """
        Logs the agent's action.
        """
        y, x = self.agent.get_current_cell()
        self.actions.append(f"({y + 1},{x + 1}): {action}")

    def save_result(self, file_name="output/result1.txt"):
        """
        Saves the result of the game to a file.
        """
        with open(file_name, "w") as file:
            for action in self.actions:
                file.write(action + "\n")
        print(f"Result saved to {file_name}")

    def game_loop(self):
        """
        Main game loop where the agent autonomously explores the Wumpus World.
        """
        game_over = False
        while not game_over:
            self.display_map()
            action = self.agent.get_action(
                self.program
            )  # Agent determines its next action
            self.log_action(action)
            self.agent.perform_action(action, self.program)  # Agent performs the action

            # Check game end conditions
            if self.agent.is_dead() or self.agent.has_exited():
                game_over = True

            time.sleep(1)  # Pause for effect

        self.display_map()
        self.save_result()
