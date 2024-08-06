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

def showWumpusWorld(choose_input_result, map):
    M1 = Map(screen, map)
    showGameBackground(screen)
    M1.showBoard()
    I1 = Info(screen)
    I1.showInputInfo(choose_input_result)
    I1.showPoint()
    I1.showHP()
    I1.showNoti()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                    return
        pygame.display.update()

def showMenu():
    showMenuBackground(screen)
    choose_option = None
    menuChoice = ['Run Input', 'Credit', 'Exit']
    menu = Choice(screen, menuChoice, 'Logical Agent - Wumpus World')
    credit = Credit(screen)
    input_choose_option = None
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
            menu.display_option(is_up, is_down, is_left, is_enter)
            choose_option = menu.get_option_result()
        else:
            if choose_option == 0:
                if input_choose_option is None:
                    inputMenu.display_option(is_up, is_down, is_left, is_enter)
                    input_choose_option = inputMenu.get_option_result()
                else:
                    return input_choose_option
                choose_option = inputMenu.get_back_to()
            if choose_option == 1:
                credit.display_credit(is_left)
                choose_option = credit.get_back_to()
            if choose_option == 2:
                pygame.quit()
                sys.exit()
        pygame.display.update()

#(base) D:\HCMUS\Co so AI\CSC14003 - Introduction to AI\Proj2\Project-2-Logical-Agent\Source>
#day la main ui, chua ket noi voi main toan chuong trinh

# [ ['A'] True False False False ] [ ['W'] False False False False ] [ Empty True True False False ] [ Empty False False False False ]
# [ Empty False False False False ] [ ['G'] True True False False ] [ ['P'] False False False False ] [ Empty False True False False ] 
# [ Empty False False False False ] [ Empty False False False False ] [ Empty False True False False ] [ Empty False True False False ]
# [ Empty False False False False ] [ Empty False False False False ] [ Empty False True False False ] [ ['P'] False False False False ]
def mainUI():
    choose_input_result = showMenu()
    map = [ [ [ 'A', True, False, False, False ], [ 'W', False, False, False, False ], [ '-', True, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ 'G', True, True, False, False ], [ 'P', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, True, False, False ], [ 'P', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ 'G', True, True, False, False ], [ 'P', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, True, False, False ], [ 'P', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ 'G', True, True, False, False ], [ 'P', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ],
            [ [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, True, False, False ], [ 'P', False, False, False, False ], [ '-', False, True, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ], [ '-', False, False, False, False ] ] ]
    showWumpusWorld(choose_input_result, map)

while True:
    mainUI()