import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Color variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = "#480113"
BLACK = (0, 0, 0)
GREY = "#808080"
DARKBLUE = "#054569"
LIGHTBLUE = "#8ecae6"
MIDBLUE = "#219ebc"
OATYELLOW = "#f1e3bc"
HONEYYELLOW = "#ffb703"
ORANGE = "#fb8500"

default_width = 1366
default_height = 768
max_width = pygame.display.Info().current_w
max_height = pygame.display.Info().current_w
fullscreen_flag = False
screen = pygame.display.set_mode((default_width, default_height))
running = True
fps = 60
font = pygame.font.SysFont("comicsans", 30)
default_node_size = 100


grid = [100,100]

class Button:
    def __init__(self, text, btn_color="#ced7e0", btn_highlight="#9ccddc", btn_shadow="#054569", btn_textSize=30, btn_textColor="#062c43", cb=None):
        #Core attributes 
        self.btn_attributes = [btn_color, btn_highlight, btn_shadow]
        self.pressed = False		                                               
        self.gui_font = pygame.font.Font(None,btn_textSize)
        self.top_color = self.btn_attributes[0]        		
        self.bottom_color = self.btn_attributes[2]
        self.text = text
        self.callback = cb

        #text
        self.text_surf = self.gui_font.render(text,True,btn_textColor)

    def draw(self, screen, width, height, pos, elevation):
        # Okay
        self.elevation = elevation        
        self.original_y_pos = pos[1]                		                

        # top rectangle 
        self.top_rect = pygame.Rect(pos, (width,height))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos, (width,height))		        

        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.elevation         

        self.bottom_rect.midtop = self.top_rect.midtop        
        self.bottom_rect.y = self.original_y_pos
        self.check_click(screen)                       

    def check_click(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.btn_attributes[1]			

            if pygame.mouse.get_pressed()[0]:                
                self.top_rect.y = self.original_y_pos
                self.pressed = True                
            else:            
                self.top_rect.y = self.original_y_pos - self.elevation
                if self.pressed == True:					                                                          
                    if self.callback != None:
                        self.callback()                    
                    self.pressed = False                    
        else:            
            self.top_rect.y = self.original_y_pos - self.elevation
            self.top_color = self.btn_attributes[0]
        self.text_rect.center = self.top_rect.center
        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)


def debug(info, x=10, y=10):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, "Red")
    debug_rect = debug_surf.get_rect(topleft=(x,y))
    pygame.draw.rect(display_surf, "Black", debug_rect)
    display_surf.blit(debug_surf, debug_rect)

def debugImg(img, x=10, y=10):
    display_surf = pygame.display.get_surface()
    if img:
        debug_surf = img
        debug_rect = debug_surf.get_rect(topleft=(x,y))
    else:
        debug_rect = pygame.Rect((x,y), (60,60))
        pygame.draw.rect(display_surf, "Black", debug_rect)        
    display_surf.blit(debug_surf, debug_rect)