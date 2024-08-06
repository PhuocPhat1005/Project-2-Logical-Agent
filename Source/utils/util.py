from enum import Enum, auto
import pygame


class Object(Enum):
    EMPTY = "_"
    WUMPUS = "W"
    PIT = "P"
    AGENT = "A"
    GOLD = "G"
    POISONOUS_GAS = "P_G"
    HEALING_POTIONS = "H_P"
    STENCH = "S"
    BREEZE = "B"
    WHIFF = "W_H"
    GLOW = "G_L"
    SCREAM = "S_C"
