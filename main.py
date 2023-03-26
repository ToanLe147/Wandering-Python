import pathfinding

from scripts.parameters import *


class menu():
    pass

    def get_screen_size(self):
        self.current_w = pygame.display.Info().current_w
        self.current_h = pygame.display.Info().current_h
        
        self.start_pos = (self.current_w//2, self.current_h//2)
        self.button_width = 250
        self.button_height = 40
        self.button_elevation = 5
        self.offset = (self.start_pos[1] + (len(self.button_list) * self.button_height)) // (len(self.button_list) + 1) if self.button_list else 50
        self.button_start_pos_initial = self.start_pos[1] - (len(self.button_list) * self.button_height) // 2
        
        panel_size = (self.button_width + 200, self.button_height*len(self.button_list) + self.offset*(len(self.button_list)-1) + 200)
        self.panel = pygame.Surface(panel_size)
        self.panel_rectangle = self.panel.get_rect(center = self.start_pos)        
        self.panel.fill(DARKJADE)
        self.panel.set_alpha(120)
        
        help_panel_size = (self.current_w, self.current_h // 4)
        self.help_panel = pygame.Surface(help_panel_size)
        self.help_panel.fill(GREY)
        self.help_panel.set_alpha(120)
    
    def draw_menu_panel(self, screen: pygame.SurfaceType):        
        if self.menu_reveal:            
            screen.blit(self.panel, self.panel_rectangle)
            self.DrawButton(screen)


class pathfinder():
    def __init__(self, matrix) -> None:
        self.matrix = matrix


class player():
    pass


if __name__ == "__main__":
    
    while running:
        for event in pygame.event.get():            
            if event.type == QUIT:
                running = False
        
        screen.fill(OATYELLOW)
        debug(f"{pygame.mouse.get_pos()}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        pygame.display.update()
        clock.tick(fps)
        
