import pygame, sys
from pygame.locals import *
#from ui.constants import *
from constants import *
from choice import *
from credit import *
from image import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
title = pygame.display.set_caption('Logical Agent - Wumpus World')

#def showWumpusWorld():
def showMenu():
    showMenuBackground(screen)
    choose_option = None
    menuChoice = ['Run Input', 'Credit', 'Exit']
    menu = Choice(screen, menuChoice, 'Logical Agent - Wumpus World')
    credit = Credit(screen)
    inputChoice = ['Input 01', 'Input 02', 'Input 03', 'Input 04', 'Input 05']
    inputMenu = Choice(screen, inputChoice, '')

    while True:
        is_up = False
        is_down = False
        is_left = False
        is_enter = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and is_down == False and is_up == False and is_left == False and is_enter == False:
                    is_down = True
                elif event.key == pygame.K_UP and is_down == False and is_up == False and is_left == False and is_enter == False:
                    is_up = True
                elif event.key == pygame.K_LEFT and is_down == False and is_up == False and is_left == False and is_enter == False:
                    is_left = True
                elif (event.key == pygame.K_RETURN or event.key == K_KP_ENTER) and is_down == False and is_up == False and is_left == False and is_enter == False:
                    is_enter = True
        
        if choose_option is None:
            menu.display_menu(is_up, is_down, is_enter)
            choose_option = menu.get_option_result()
        else:
            if choose_option == 0:
                choose_option = None
                pass
            if choose_option == 1:
                credit.display_credit(is_left)
                choose_option = credit.get_back_to()
            if choose_option == 2:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

#(base) D:\HCMUS\Co so AI\CSC14003 - Introduction to AI\Proj2\Project-2-Logical-Agent\Source>
#day la main ui, chua ket noi voi main toan chuong trinh
showMenu()