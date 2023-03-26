import asyncio
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from scripts.parameters import *


class userInterface():
    def __init__(self) -> None:        
        self.button_list = {}
        self.get_screen_size()
                                         
        self.button_list["GO"] = Button("GO", btn_highlight=GREEN)
        self.button_list["RESET"] = Button("RESET")
        
        self.reset_signal = False        

    def get_screen_size(self):
        self.current_w = pygame.display.Info().current_w
        self.current_h = pygame.display.Info().current_h
                
        self.btn_config = btn_config(
            (self.current_w//2, self.current_h//2),
            250,
            40,
            5,            
        )
        self.btn_offset = (self.btn_config.pos[1] + (len(self.button_list) * self.btn_config.height)) // (len(self.button_list) + 1) if self.button_list else 50
                
        self.button_start_pos_initial = self.btn_config.pos[1] - (len(self.button_list) * self.btn_config.height) // 2
        
        panel_size = (self.btn_config.width + 200, self.btn_config.height*len(self.button_list) + self.btn_offset*(len(self.button_list)-1) + 200)
        self.panel = pygame.Surface(panel_size)
        self.panel_rectangle = self.panel.get_rect(center = self.btn_config.pos)        
        self.panel.fill(DARKJADE)
        self.panel.set_alpha(120)
        
        help_panel_size = (self.current_w, self.current_h // 4)
        self.help_panel = pygame.Surface(help_panel_size)
        self.help_panel.fill(GREY)
        self.help_panel.set_alpha(120)
    
    def draw_menu_panel(self, screen: pygame.SurfaceType):                      
        screen.blit(self.panel, self.panel_rectangle)
        self.DrawButton(screen)
    
    def drawGrid(self, screen: pygame.surface, node_size=default_node_size):
        x_padding = default_width % node_size / 2
        y_padding = default_height % node_size / 2
        columes = default_width // node_size
        rows = default_height // node_size        
        self.rect_maze = [
                            [Rect(
                                (x_padding + col_index*node_size, 
                                 y_padding + row_index*node_size), 
                                (node_size, node_size)) 
                             for row_index in range(rows)] 
                          for col_index in range(columes) 
                         ]
        self.maze = [ [0]*rows for _ in range(columes) ]        
        for a_rect_list in self.rect_maze:
            for a_rect in a_rect_list:                
                pygame.draw.rect(screen, WHITE, a_rect, 1)


class pathFinder():
    def __init__(self, matrix) -> None:
        self.matrix = matrix
        self.grid = Grid(self.matrix)


class player():
    pass


async def main():
    app = userInterface()
    running = True
    filled = False    
    while running:
        for event in pygame.event.get():            
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:                
                pos = (pygame.mouse.get_pos()[0]//default_node_size, 
                       pygame.mouse.get_pos()[1]//default_node_size)
                filled = True
        
        screen.fill(OATYELLOW)
        app.drawGrid(screen)
        if filled:
            pygame.draw.rect(screen, BLACK, app.rect_maze[pos[0]][pos[1]])            
        debug(f"{pygame.mouse.get_pos()[1]//default_node_size, pygame.mouse.get_pos()[0]//default_node_size}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])        
        pygame.display.update()
        clock.tick(fps)
        await asyncio.sleep(0)


if __name__ == '__main__':    
    asyncio.run(main())

