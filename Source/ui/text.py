import pygame
from constants import *
from image import showGameBackground

# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/

class Text_Display:
    def __init__(self, content='', font_type=FONT_TYPE, font_size=FONT_MEDIUM, text_color=WHITE_COLOR):
        self.content = content
        self.font_type = font_type
        self.font_size = font_size
        self.text_color = text_color
        self.text_content = ''
        self.font = pygame.font.Font(font_type, font_size)
        
    def get_text_position(self):
        text_position = self.text_content.get_rect()
        return text_position
    
    def show_text(self, color=None):
        if color is None:
            color = self.text_color
        self.text_content = self.font.render(self.content, True, color)
        return self.text_content
    
    def center_text(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        text_rect = self.text_content.get_rect(center=(width / 2, height / 2))
        return text_rect
    
    def write_text_content(self, content='', pos_x=0, pos_y=0, text_color=WHITE_COLOR, font_size=FONT_MEDIUM, is_center=False, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        text_obj = Text_Display(content, font_size=font_size, text_color=text_color)
        text_content = text_obj.show_text()
        text_pos = (pos_x, pos_y)
        if is_center:
            text_pos = text_obj.center_text(width, height)
        self.screen.blit(text_content, text_pos)
        

class Info(Text_Display):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.left_margin = 900
    
    def reShowInfo(self):
        area = (self.left_margin, 0, WINDOW_WIDTH-self.left_margin, WINDOW_HEIGHT)
        showGameBackground(self.screen, area)
    
    def showInputInfo(self, choose_input_result):
        self.write_text_content(f"Input 0{choose_input_result+1}", self.left_margin, 50)
    
    def showPoint(self, point=0):
        self.write_text_content(f"Point: {point}", self.left_margin, 200)
    def showHP(self, HP=100):
        self.write_text_content(f"HP: {HP}%", self.left_margin, 300)
    
    def showNoti(self):
        self.write_text_content(f"Press Enter to blabla", BOARD_APPEEAR_WIDTH, SHOW_NOTI)
    
    #def showFull()