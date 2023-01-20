from scripts.parameters import *


class app():
    def __init__(self) -> None:        
        self.update_display_elements()        
        self.draw_wall = False
        self.start_node = None
        self.draw_start = False
            
    def get_screen_size(self):
        self.current_w = pygame.display.Info().current_w
        self.current_h = pygame.display.Info().current_h
    
    def update_display_elements(self, node_size=default_node_size):
        self.get_screen_size()
        self.wall = []
        self.node_size = node_size
        self.x_padding = self.current_w % self.node_size / 2
        self.y_padding = self.current_h % self.node_size / 2
        # Setup grid storage
        self.grid_columes = self.current_w // self.node_size
        self.grid_rows = self.current_h // self.node_size        
        size = (self.node_size, self.node_size)
        self.grid = [ [Rect((self.x_padding + columne_index*self.node_size, self.y_padding + row_index*self.node_size), size) for row_index in range(self.grid_rows)] for columne_index in range(self.grid_columes) ]
        self.tgrid = [ [(self.x_padding + columne_index*self.node_size, self.y_padding + row_index*self.node_size) for row_index in range(self.grid_rows)] for columne_index in range(self.grid_columes) ]
        print(self.grid_rows, self.grid_columes)
        print(self.tgrid)
        
    
    def draw_borders(self, screen):
        pygame.draw.rect(screen, BLACK, Rect((0,0), (self.current_w, self.y_padding)))
        pygame.draw.rect(screen, BLACK, Rect((0,self.current_h - self.y_padding), (self.current_w, self.y_padding)))
        pygame.draw.rect(screen, BLACK, Rect((0,0), (self.x_padding, self.current_h)))
        pygame.draw.rect(screen, BLACK, Rect((self.current_w - self.x_padding,0), (self.x_padding, self.current_h)))
        ## Draw grid borders
        for index in range(self.grid_columes+1):
            pygame.draw.line(screen, WHITE, (self.x_padding + index*self.node_size, 0), (self.x_padding + index*self.node_size, self.current_h))
        for index in range(self.grid_rows+1):
            pygame.draw.line(screen, WHITE, (0, self.y_padding + index*self.node_size), (self.current_w, self.y_padding + index*self.node_size))    
    
    def draw_nodes(self, screen):        
        if self.start_node:
            row = self.start_node[0]
            colume = self.start_node[1]
            pygame.draw.rect(screen, ORANGE, self.grid[row][colume])            
        if self.draw_wall: 
            if pygame.mouse.get_pressed()[0]:
                selection = self.mouse_interact()
                if selection not in self.wall and len(selection) == 2:
                    self.wall.append(selection)
        if self.wall:
            for cell in self.wall:
                pygame.draw.rect(screen, BLACK, self.grid[cell[0]][cell[1]])
                
    def draw_start_node(self):        
        pass

    def mouse_interact(self):            
        mouse_pos_x = pygame.mouse.get_pos()[0]
        mouse_pos_y = pygame.mouse.get_pos()[1]
        result = []
                
        if mouse_pos_x > self.x_padding and mouse_pos_x < (self.current_w - self.x_padding):
            result.append(int(mouse_pos_x-self.x_padding) // self.node_size)
        if mouse_pos_y > self.y_padding and mouse_pos_y < (self.current_h - self.y_padding):
            result.append(int(mouse_pos_y-self.y_padding) // self.node_size)
        
        # print((mouse_pos_x, mouse_pos_y))
        # print(result)
        # print(self.tgrid[result[0]][result[1]])
        return result
   
# test = Button('Test')
# test.draw(screen, 250, 100, (400,500), 10)

if __name__ == '__main__':
    app = app()
    
    while running:                                
        draw_start = False            
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # if event.type == MOUSEBUTTONUP:
            #     app.start_node = app.mouse_interact()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    app.draw_wall = not app.draw_wall
                if event.key == K_f:
                    if not fullscreen_flag:                    
                        screen = pygame.display.set_mode((0,0), FULLSCREEN)
                    else:                    
                        screen = pygame.display.set_mode((default_width, default_height))
                    fullscreen_flag = not fullscreen_flag
                    app.update_display_elements()
        
        screen.fill(OATYELLOW)        
        app.draw_borders(screen)
        app.draw_nodes(screen)
        debug(f"{pygame.mouse.get_pos()}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        pygame.display.update()
        clock.tick(fps)    


