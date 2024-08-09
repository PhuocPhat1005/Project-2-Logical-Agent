from enum import Enum, auto


class Object(Enum):
    EMPTY = "_"
    WUMPUS = "W"  # a monster that kills the agent if the end up in the same cell.
    PIT = "P"  # dangerous cells that agent falls into and dies.
    AGENT = "A"  # the agent moves around the grid trying to achieve its goals.
    GOLD = "G"  # the agent's goal is to find and retrive the gold.
    POISONOUS_GAS = "P_G"  # reduces the agent's health by 25% if entered.
    HEALING_POTIONS = "H_P"  # restores the agent's health by 25% when using.
    STENCH = "S"  # indicates an adjacent cell contains the Wumpus.
    BREEZE = "B"  # indicates an adjacent cell contains a pit.
    WHIFF = "W_H"  # indicates an adjacent cell contains poisonous gas.
    GLOW = "G_L"  # indicates an adjacent cell contains a healing potion.
    SCREAM = "S_C"  # heard if the Wumpus is killed.


class Action(Enum):
    MOVE_FORWARD = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    GRAB = auto()
    SHOOT = auto()
    CLIMB = auto()
    HEAL = auto()


class GameState(Enum):
    RUNNING = 1
    NOT_RUNNING = 2
