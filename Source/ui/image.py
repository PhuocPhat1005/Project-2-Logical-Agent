import pygame, sys, copy
from pygame.locals import *
from ui.constants import *
from ui.text import *

def showGameBackground(screen, area=None, level=1):
    #https://wallpapercave.com/w/wp7326071
    #area: (pos_x, pos_y, width, height)
    background = pygame.image.load(f'ui/assets/game_background_{level % 5}.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    if area == None:
        screen.blit(background, (0, 0))
    else:
        screen.blit(background, (area[0], area[1]), area)

def showMenuBackground(screen):
    #https://wallpapersafari.com/w/nLIPZf/download
    background = pygame.image.load('ui/assets/menu_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))

class ImageElement:
    def __init__(self, screen, cell_side=60):
        self.screen = screen
        self.cell_side = cell_side
        self.cell_size = (self.cell_side, self.cell_side)
        self.empty_img = pygame.image.load('ui/assets/empty.png')
        self.empty_img = pygame.transform.scale(self.empty_img, self.cell_size)
        self.unknown_img = pygame.image.load('ui/assets/unknown.png')
        self.unknown_img = pygame.transform.scale(self.unknown_img, self.cell_size)
        #https://www.clipartmax.com/download/m2i8A0H7b1Z5d3Z5_miner-miner-png/
        self.agent_img = pygame.image.load('ui/assets/agent.png')
        self.agent_img = pygame.transform.scale(self.agent_img, self.cell_size)
        #https://pngtree.com/freepng/vector-of-png-bow-arrow_7258676.html
        self.shoot_img = pygame.image.load('ui/assets/shoot.png')
        self.shoot_img = pygame.transform.scale(self.shoot_img, self.cell_size)
        #https://www.hiclipart.com/free-transparent-background-png-clipart-iyjih
        self.gold_img = pygame.image.load('ui/assets/gold.png')
        self.gold_img = pygame.transform.scale(self.gold_img, self.cell_size)
        
        #https://yt3.googleusercontent.com/s_38Cu2ryXXDcK9fbfc9O-C23DZV1Lo8VgvDJbG_kRB7WctOofRD1gt-LNMGlJnx13-BaetK1w=s900-c-k-c0x00ffffff-no-rj
        self.wumpus_img = pygame.image.load('ui/assets/wumpus.png')
        self.wumpus_img = pygame.transform.scale(self.wumpus_img, self.cell_size)
        self.stench_img = pygame.image.load('ui/assets/stench.png')
        self.stench_img = pygame.transform.scale(self.stench_img, self.cell_size)
        self.scream_img = pygame.image.load('ui/assets/scream.png')
        self.scream_img = pygame.transform.scale(self.scream_img, self.cell_size)
        
        #https://www.pikpng.com/pngvi/mTJTmi_ground-clipart-crack-hole-in-ground-drawing-png-download/
        self.pit_img = pygame.image.load('ui/assets/pit.png')
        self.pit_img = pygame.transform.scale(self.pit_img, self.cell_size)
        self.breeze_img = pygame.image.load('ui/assets/breeze.png')
        self.breeze_img = pygame.transform.scale(self.breeze_img, self.cell_size)

        #https://en.ac-illust.com/clip-art/22263264/poisonous-gas
        self.poisonous_gas_img = pygame.image.load('ui/assets/poisonous_gas.png')
        self.poisonous_gas_img = pygame.transform.scale(self.poisonous_gas_img, self.cell_size)
        self.whiff_img = pygame.image.load('ui/assets/whiff.png')
        self.whiff_img = pygame.transform.scale(self.whiff_img, self.cell_size)

        #https://pngtree.com/freepng/potion-mysterious-magic-potion-bottle_6838219.html
        self.healing_potion_img = pygame.image.load('ui/assets/healing_potion.png')
        self.healing_potion_img = pygame.transform.scale(self.healing_potion_img, self.cell_size)
        self.glow_img = pygame.image.load('ui/assets/glow.png')
        self.glow_img = pygame.transform.scale(self.glow_img, self.cell_size)

    
    # Show images
    def showEmpty(self, i, j, h):
        self.screen.blit(self.empty_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showUnknown(self, i, j, h):
        self.screen.blit(self.unknown_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showAgent(self, i, j, h):
        self.screen.blit(self.agent_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showShoot(self, i, j, h):
        self.screen.blit(self.shoot_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showGold(self, i, j, h):
        self.screen.blit(self.gold_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showWumpus(self, i, j, h):
        self.screen.blit(self.wumpus_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showStench(self, i, j, h):
        self.screen.blit(self.stench_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showScream(self, i, j, h):
        self.screen.blit(self.scream_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showPoisonousGas(self, i, j, h):
        self.screen.blit(self.poisonous_gas_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showWhiff(self, i, j, h):
        self.screen.blit(self.whiff_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showHealingPotion(self, i, j, h):
        self.screen.blit(self.healing_potion_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showGlow(self, i, j, h):
        self.screen.blit(self.glow_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showPit(self, i, j, h):
        self.screen.blit(self.pit_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showBreeze(self, i, j, h):
        self.screen.blit(self.breeze_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def turnLeft(self, drirection):
        self.agent_img = pygame.transform.rotate(self.agent_img, 90)
        self.shoot_img = pygame.transform.rotate(self.shoot_img, 90)
        return drirection+1
    def turnRight(self, drirection):
        self.agent_img = pygame.transform.rotate(self.agent_img, -90)
        self.shoot_img = pygame.transform.rotate(self.shoot_img, -90)
        return drirection-1

class Map(ImageElement):
    def __init__(self, screen, map_data, cell_side=65):
        # Read and store map data
        self.map_data = copy.deepcopy(map_data)
        self.h = len(map_data)
        self.w = len(map_data[0])
        cell_side = 65
        if max(self.h, self.w) <= 5:
            cell_side = 120
        elif max(self.h, self.w) <= 10:
            cell_side = 65
        else:
            cell_side = 20
        super().__init__(screen, cell_side)
    
    def returnH(self):
        return self.h
    
    def updateMap(self, map_data):
        self.map_data = copy.deepcopy(map_data)
    
    def returnCellSide(self):
        return self.cell_side
    
    def agentShoot(self, path, now, drirection):
        y =  path[now][0][0]
        x =  path[now][0][1]
        # mod = 0: right, 1: up, 2: left, 3: down
        if drirection % 4 == 0:
            self.showShoot(y, x+1, self.h)
            return y, x+1
        elif drirection % 4 == 1:
            self.showShoot(y+1, x, self.h)
            return y+1, x
        elif drirection % 4 == 2:
            self.showShoot(y, x-1, self.h)
            return y, x-1
        elif drirection % 4 == 3:
            self.showShoot(y-1, x, self.h)
            return y-1, x
    def deleteGold(self, path, now):
        y =  path[now][0][0]
        x =  path[now][0][1]
        self.map_data[y][x][0].remove('G')
        # for _ in range(now+1):
        #     self.showPath(path[_][0][0], path[_][0][1])
    
    def deleteWumpus(self, path, now):
        y =  path[now][0][0]
        x =  path[now][0][1]
        self.map_data[y][x][0].remove('W')
        if y > 0:
            if y-1 > 0 and 'W' in self.map_data[y-2][x][0]:
                pass
            elif x-1 > 0 and 'W' in self.map_data[y-1][x-1][0]:
                pass
            elif x+1 < self.w-1 and 'W' in self.map_data[y-1][x+1][0]:
                pass
            else:
                self.map_data[y-1][x][1] = False
                self.map_data[y-1][x][5] = True
        if y < self.h-1:
            if y+1 < self.h-1 and 'W' in self.map_data[y+1][x][0]:
                pass
            elif x-1 > 0 and 'W' in self.map_data[y+1][x-1][0]:
                pass
            elif x+1 < self.w-1 and 'W' in self.map_data[y+1][x+1][0]:
                pass
            else:
                self.map_data[y+1][x][1] = False
                self.map_data[y+1][x][5] = True
        if x > 0:
            if x-1 > 0 and 'W' in self.map_data[y][x-2][0]:
                pass
            elif y-1 > 0 and 'W' in self.map_data[y-1][x-1][0]:
                pass
            elif y+1 < self.h-1 and 'W' in self.map_data[y+1][x-1][0]:
                pass
            else:
                self.map_data[y][x-1][1] = False
                self.map_data[y][x-1][5] = True
        if x < self.w-1:
            if x-1 > 0 and 'W' in self.map_data[y][x-2][0]:
                pass
            elif y-1 > 0 and 'W' in self.map_data[y-1][x-1][0]:
                pass
            elif y+1 < self.h-1 and 'W' in self.map_data[y+1][x-1][0]:
                pass
            else:
                self.map_data[y][x+1][1] = False
                self.map_data[y][x+1][5] = True
        for _ in range(now+1):
            self.showPath(path[_][0][0], path[_][0][1])
    
    def deleteHealingPotion(self, path, now):
        y =  path[now][0][0]
        x =  path[now][0][1]
        self.map_data[y][x][0].remove('H_P')
        if y > 0:
            if y-1 > 0 and 'H_P' in self.map_data[y-2][x][0]:
                pass
            elif x-1 > 0 and 'H_P' in self.map_data[y-1][x-1][0]:
                pass
            elif x+1 < self.w-1 and 'H_P' in self.map_data[y-1][x+1][0]:
                pass
            else:
                self.map_data[y-1][x][4] = False
        if y < self.h-1:
            if y+1 < self.h-1 and 'H_P' in self.map_data[y+1][x][0]:
                pass
            elif x-1 > 0 and 'H_P' in self.map_data[y+1][x-1][0]:
                pass
            elif x+1 < self.w-1 and 'H_P' in self.map_data[y+1][x+1][0]:
                pass
            else:
                self.map_data[y+1][x][4] = False
        if x > 0:
            if x-1 > 0 and 'H_P' in self.map_data[y][x-2][0]:
                pass
            elif y-1 > 0 and 'H_P' in self.map_data[y-1][x-1][0]:
                pass
            elif y+1 < self.h-1 and 'H_P' in self.map_data[y+1][x-1][0]:
                pass
            else:
                self.map_data[y][x-1][4] = False
        if x < self.w-1:
            if x+1 < self.w-1 and 'H_P' in self.map_data[y][x+1][0]:
                pass
            elif y-1 > 0 and 'H_P' in self.map_data[y-1][x-1][0]:
                pass
            elif y+1 < self.h-1 and 'H_P' in self.map_data[y+1][x-1][0]:
                pass
            else:
                self.map_data[y][x+1][4] = False
        for _ in range(now+1):
            self.showPath(path[_][0][0], path[_][0][1])
    
    def showUnknownBoard(self): # Show game board
        y = 0
        x = 0
        for y in range (0, self.h):
            for x in range (0, self.w):
                self.showUnknown(y, x, self.h)
    
    def showKnownBoard(self): # Show game board
        y = 0
        x = 0
        #[element, stench, breeze, whiff, glow]
        for y in range (0, self.h):
            for x in range (0, self.w):
                self.showEmpty(y, x, self.h)
                if 'A' in self.map_data[y][x][0]:
                    self.showAgent(y, x, self.h)
                if 'G' in self.map_data[y][x][0]:
                    self.showGold(y, x, self.h)
                if 'W' in self.map_data[y][x][0]:
                    self.showWumpus(y, x, self.h)
                if 'P' in self.map_data[y][x][0]:
                    self.showPit(y, x, self.h)
                if 'P_G' in self.map_data[y][x][0]:
                    self.showPoisonousGas(y, x, self.h)
                if 'H_P' in self.map_data[y][x][0]:
                    self.showHealingPotion(y, x, self.h)
                
                if self.map_data[y][x][1]:
                    self.showStench(y, x, self.h)
                if self.map_data[y][x][2]:
                    self.showBreeze(y, x, self.h)
                if self.map_data[y][x][3]:
                    self.showWhiff(y, x, self.h)
                if self.map_data[y][x][4]:
                    self.showGlow(y, x, self.h)
    
    def showPath(self, y, x): # Show agent move
        # y = 0
        # x = 0
        # #[element, stench, breeze, whiff, glow]
        # for y in range (0, self.h):
        #     for x in range (0, self.w):
        #         self.showEmpty(y, x, self.h)
        #         if 'A' in self.map_data[y][x][0]:
        #             self.showAgent(y, x, self.h)
        #         if 'G' in self.map_data[y][x][0]:
        #             self.showGold(y, x, self.h)
        #         if 'W' in self.map_data[y][x][0]:
        #             self.showWumpus(y, x, self.h)
        #         if 'P' in self.map_data[y][x][0]:
        #             self.showPit(y, x, self.h)
        #         if 'P_G' in self.map_data[y][x][0]:
        #             self.showPoisonousGas(y, x, self.h)
        #         if 'H_P' in self.map_data[y][x][0]:
        #             self.showHealingPotion(y, x, self.h)
                
        #         if self.map_data[y][x][1]:
        #             self.showStench(y, x, self.h)
        #         if self.map_data[y][x][2]:
        #             self.showBreeze(y, x, self.h)
        #         if self.map_data[y][x][3]:
        #             self.showWhiff(y, x, self.h)
        #         if self.map_data[y][x][4]:
        #             self.showGlow(y, x, self.h)
        #[element, stench, breeze, whiff, glow]
        self.showEmpty(y, x, self.h)
        if 'A' in self.map_data[y][x][0]:
            self.showAgent(y, x, self.h)
        if 'G' in self.map_data[y][x][0]:
            self.showGold(y, x, self.h)
        if 'W' in self.map_data[y][x][0]:
            self.showWumpus(y, x, self.h)
        if 'P' in self.map_data[y][x][0]:
            self.showPit(y, x, self.h)
        if 'P_G' in self.map_data[y][x][0]:
            self.showPoisonousGas(y, x, self.h)
        if 'H_P' in self.map_data[y][x][0]:
            self.showHealingPotion(y, x, self.h)
        
        if self.map_data[y][x][1]:
            self.showStench(y, x, self.h)
        if self.map_data[y][x][2]:
            self.showBreeze(y, x, self.h)
        if self.map_data[y][x][3]:
            self.showWhiff(y, x, self.h)
        if self.map_data[y][x][4]:
            self.showGlow(y, x, self.h)
        if self.map_data[y][x][5]:
            self.showScream(y, x, self.h)