import pygame, sys
from pygame.locals import *
#from constants import *
from ui.constants import *
from ui.choice import *
from ui.credit import *
from ui.image import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
title = pygame.display.set_caption('Logical Agent - Wumpus World')

def showWumpusWorld(choose_map_result, map):
    print('here')
    print(choose_map_result)
    
    M1 = Map(screen, map)
    showGameBackground(screen, level=choose_map_result)
    M1.showUnknownBoard()
    I1 = Info(screen, level=choose_map_result)
    I1.showLeftBar(choose_map_result, point=0, HP=100, H_Ps=0)
    I1.showNoti(0)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                    return
        pygame.display.update()

def showAgentMove(choose_map_result, map, path, level):
    I2 = Info(screen, level=level)
    M2 = Map(screen, map)
    # pos-y, pos-x, direction, point, HP, Healing Potion(s)
    # path = [
    #     (0, 0, 0, 0, 100, 0),
    #     (1, 0, 0, -10, 100, 0),
    #     (1, 0, 1, -20, 100, 0),
    #     (1, 1, 1, -30, 100, 0),
    #     (1, 1, 1, 4970, 100, 0),
    #     (1, 1, 2, 4960, 100, 0),
    #     (1, 1, 3, 4950, 100, 0),
    #     (1, 0, 3, 4940, 100, 0),
    #     (1, 0, 2, 4930, 100, 0),
    #     (0, 0, 2, 4920, 100, 0)
    # ]
    I2.showNoti(1)
    isMoving = True
    drirection = 1 # mod = 0: down, 1: right, 2: up, 3: left
    time_wait_1 = 1000
    time_wait_2 = 50
    while True:
        if isMoving:
            y_shoot, x_shoot = -1, -1
            for _ in range(len(path)):
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                            return
                if _ > 0:
                    M2.showPath(path[_-1][0][0], path[_-1][0][1])
                    if path[_][1] == 'Turn Left':
                        drirection = M2.turnLeft(drirection)
                    elif path[_][1] == 'Turn Right':
                        drirection = M2.turnRight(drirection)
                if path[_][1] == 'Grab Gold':
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.returnH())
                    M2.showGold(path[_][0][0], path[_][0][1], M2.returnH())
                    pygame.display.flip()
                    pygame.time.wait(time_wait_1)
                    M2.deleteGold(path, _)
                if path[_][1] == 'Grab Heal':
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.returnH())
                    M2.showHealingPotion(path[_][0][0], path[_][0][1], M2.returnH())
                    pygame.display.flip()
                    pygame.time.wait(time_wait_1)
                    M2.deleteHealingPotion(path, _) 
                M2.showPath(path[_][0][0], path[_][0][1])
                M2.showAgent(path[_][0][0], path[_][0][1], M2.returnH())
                if path[_][1] == 'Shoot' and (_==0 or path[_][0] != path[_-1][0]):
                    y_shoot, x_shoot = M2.agentShoot(path, _, drirection)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_1)
                I2.showLeftBar(choose_map_result, path[_][2], path[_][3], path[_][4])
                pygame.display.flip()
                pygame.time.wait(time_wait_2)
            I2.showNoti(2)
            pygame.display.flip()
            isMoving = False
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                        return


def showMenu():
    showMenuBackground(screen)
    choose_option = None
    menuChoice = ['Run Map', 'Credit', 'Exit']
    menu = Choice(screen, menuChoice, 'Logical Agent - Wumpus World')
    credit = Credit(screen)
    map_choose_option = None
    mapChoice = ['Map 01', 'Map 02', 'Map 03', 'Map 04', 'Map 05']
    mapMenu = Choice(screen, mapChoice, '')
    mapChoice_2 = ['Map 06', 'Map 07', 'Map 08', 'Map 09', 'Map 10']
    mapMenu_2 = Choice(screen, mapChoice_2, '')

    while True:
        is_up = False
        is_down = False
        is_left = False
        is_right = False
        is_enter = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_down = True
                elif event.key == pygame.K_UP and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_up = True
                elif event.key == pygame.K_LEFT and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_left = True
                elif event.key == pygame.K_RIGHT and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_right = True
                elif (event.key == pygame.K_RETURN or event.key == K_KP_ENTER) and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_enter = True
        
        if choose_option is None:
            menu.display_option(is_up, is_down, is_left, is_right, is_enter)
            choose_option = menu.get_option_result()
        else:
            if choose_option == 0:
                if map_choose_option is None:                    
                    mapMenu.display_option(is_up, is_down, is_left, is_right, is_enter)
                    map_choose_option = mapMenu.get_option_result()
                else:
                    return map_choose_option
                if is_left:
                    choose_option = mapMenu.get_back_to(None, 0)
                if is_right:
                    choose_option = mapMenu.get_next_to(-1, 0)
            if choose_option == 1:
                credit.display_credit(is_left)
                choose_option = credit.get_back_to()
            if choose_option == 2:
                pygame.quit()
                sys.exit()
            if choose_option == -1: # input page 2
                if map_choose_option is None:                    
                    mapMenu_2.display_option(is_up, is_down, is_left, is_right, is_enter, can_next=False)
                    map_choose_option = mapMenu_2.get_option_result()
                else:
                    return map_choose_option + 5
                if is_left:
                    choose_option = mapMenu_2.get_back_to(0, -1)
        pygame.display.update()

#(base) D:\HCMUS\Co so AI\CSC14003 - Introduction to AI\Proj2\Project-2-Logical-Agent\Source>
#day la main ui, chua ket noi voi main toan chuong trinh
#[element, stench, breeze, whiff, glow, scream]
# [ ['-'] True True False False ] [ ['W', 'P', 'G'] False False False False ] [ ['-'] True True False False ] [ ['-'] False False False False ]
# [ ['-'] False False False False ] [ ['G'] True True False False ] [ ['P'] False False False False ] [ ['-'] False True False False ]
# [ ['-'] False False False False ] [ ['-'] False False False False ] [ ['-'] False True False False ] [ ['-'] False True False False ]
# [ ['-'] False False False False ] [ ['-'] False False False False ] [ ['-'] False True False False ] [ ['P'] False False False False ]
def mainUI():
    choose_map_result = showMenu()
    map = [ [ [ ['A'], True, False, False, False ], [ ['W', 'G'], False, False, False, False ], [ ['-'], True, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['G'], True, True, False, False ], [ ['P'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['P'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['G'], True, True, False, False ], [ ['P'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['P'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['G'], True, True, False, False ], [ ['P'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ],
            [ [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['P'], False, False, False, False ], [ ['-'], False, True, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ], [ ['-'], False, False, False, False ] ] ]
    showWumpusWorld(choose_map_result, map)
    #showAgentMove(choose_map_result, map)

# while True:
#     mainUI()