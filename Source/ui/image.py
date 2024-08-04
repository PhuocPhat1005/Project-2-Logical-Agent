import pygame
from constants import *

def showGameBackground(screen):
    #https://www.craghoppers.com/the-journal/8-facts-about-the-rocky-mountain-region/
    background = pygame.image.load('ui/assets/game_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))

def showMenuBackground(screen):
    #https://wallpapersafari.com/w/nLIPZf/download
    background = pygame.image.load('ui/assets/menu_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))
