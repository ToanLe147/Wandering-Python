from scripts.parameters import *
from scripts.pathfinding import *
import asyncio

class app():
    def __init__(self) -> None:        
        self.update_display_elements()
        self.is_menu_on = False
        self.draw_obstacle = False
        self.start_node = None
        self.end_node = None
        self.draw_start = False
        self.draw_end = False
        # self.draw_path = False
        self.path = None
        self.path_drawing_index = 0
            
    def get_screen_size(self):
        self.current_w = pygame.display.Info().current_w
        self.current_h = pygame.display.Info().current_h
    
    # def find_path(self):        
    #     if self.start_node and self.end_node:
    #         self.path = astar(self.maze, self.start_node, self.end_node)
    #     print(self.path)
    
    def update_display_elements(self, node_size=default_node_size):
        self.get_screen_size()
        self.obstacle = []        
        self.node_size = node_size
        self.x_padding = self.current_w % self.node_size / 2
        self.y_padding = self.current_h % self.node_size / 2
        # Setup grid storage
        self.grid_columes = self.current_w // self.node_size
        self.grid_rows = self.current_h // self.node_size        
        size = (self.node_size, self.node_size)
        self.grid = [ [Rect((self.x_padding + columne_index*self.node_size, self.y_padding + row_index*self.node_size), size) for row_index in range(self.grid_rows)] for columne_index in range(self.grid_columes) ]
        self.maze = [ [0]*self.grid_rows for columne_index in range(self.grid_columes) ]
        # print(self.grid_rows, self.grid_columes)
        # print(self.maze)
        # print(self.grid.__len__(), self.maze.__len__())
    
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
        if not self.is_menu_on:            
            if self.draw_start:
                if pygame.mouse.get_pressed()[0]:
                    self.start_node = self.mouse_interact()
            if self.draw_end:
                if pygame.mouse.get_pressed()[0]:
                    self.end_node = self.mouse_interact()
            if self.draw_obstacle: 
                if pygame.mouse.get_pressed()[0]:
                    selection = self.mouse_interact()
                    if selection not in self.obstacle and len(selection) == 2:
                        self.obstacle.append(selection)
                if pygame.mouse.get_pressed()[2]:
                    selection = self.mouse_interact()
                    if selection in self.obstacle and len(selection) == 2:
                        self.obstacle.remove(selection)
        if self.obstacle:
            for cell in self.obstacle:
                pygame.draw.rect(screen, BLACK, self.grid[cell[0]][cell[1]])
        if self.start_node:
            if self.start_node in self.obstacle:
                self.obstacle.remove(self.start_node)
            row = self.start_node[0]
            colume = self.start_node[1]
            pygame.draw.rect(screen, ORANGE, self.grid[row][colume])
        if self.end_node:
            if self.end_node in self.obstacle:
                self.obstacle.remove(self.end_node)
            row = self.end_node[0]
            colume = self.end_node[1]
            pygame.draw.rect(screen, GREEN, self.grid[row][colume])
        if self.path:
            for index in range(int(self.path_drawing_index)):                
                cell = self.path[index]
                pygame.draw.rect(screen, DARKBLUE, self.grid[cell[0]][cell[1]])
            self.path_drawing_index = self.path_drawing_index + 10/fps if self.path_drawing_index < len(self.path) else len(self.path)

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
    
    def reset(self, reset_signal):        
        if reset_signal:
            self.obstacle = []
            self.start_node = None
            self.end_node = None            
            self.path = None
            self.path_drawing_index = 0
            self.maze = [ [0]*self.grid_rows for columne_index in range(self.grid_columes) ]
        return False  # toggle off the reset signal

class menu():
    def __init__(self) -> None:        
        self.button_list = {}
        self.get_screen_size()
                                         
        self.button_list["START"] = Button("PICK START", btn_highlight=GREEN, cb=[self.toggle_input, "START"])
        self.button_list["END"] = Button("PICK END", btn_highlight=RED, cb=[self.toggle_input, "END"])
        self.button_list["OBSTACLE"] = Button("DRAW OBSTACLE", cb=[self.toggle_input, "OBSTACLE"])        
        self.button_list["RESET"] = Button("RESET", cb=[self.reset])
        self.button_list["RESUME"] = Button("RESUME", cb=[self.resume])
        
        self.menu_reveal = False
        self.in_progress = None
        self.reset_signal = False
        self.draw_obstacles = False
        self.draw_start = False
        self.draw_end = False
        # self.draw_path = False
    
    def get_screen_size(self):
        self.current_w = pygame.display.Info().current_w
        self.current_h = pygame.display.Info().current_h
        
        self.start_pos = (self.current_w//4, self.current_h//4)
        self.button_width = 250
        self.button_height = 40
        self.button_elevation = 5
        self.offset = (self.start_pos[1] + (len(self.button_list) * self.button_height)) // (len(self.button_list) + 1) if self.button_list else 50
        
        panel_size = (self.button_width + 200, self.button_height*len(self.button_list) + self.offset*(len(self.button_list)-1) + 200)
        self.panel = pygame.Surface(panel_size)
        self.panel.fill(DARKJADE)
        self.panel.set_alpha(120)
        
        help_panel_size = (self.current_w, self.current_h // 4)
        self.help_panel = pygame.Surface(help_panel_size)
        self.help_panel.fill(GREY)
        self.help_panel.set_alpha(120)
    
    def DrawButton(self, screen):
        index = 0
        x = self.start_pos[0]
        for button in self.button_list:
            new_button_pos = (x, self.start_pos[1] + index * self.offset)
            if self.in_progress == button or not self.in_progress:
                self.button_list[button].draw(screen, self.button_width, self.button_height, new_button_pos, self.button_elevation)
            else:
                self.button_list[button].draw(screen, self.button_width, self.button_height, new_button_pos, self.button_elevation, True)
            index += 1
    
    def draw_menu_panel(self, screen):
        self.get_screen_size()
        if self.menu_reveal:            
            screen.blit(self.panel, (self.start_pos[0]-100,self.start_pos[1]-100))
            self.DrawButton(screen)
    
    def draw_help_panel(self, screen):
        self.get_screen_size()
        screen.blit(self.help_panel, (0, self.current_h // 4 * 3))        

    def toggle_input(self, input):
        if self.in_progress and self.in_progress != input:
            return
        if input == "START":
            self.draw_start = not self.draw_start            
            self.in_progress = input if self.draw_start else None
        if input == "END":
            self.draw_end = not self.draw_end
            self.in_progress = input if self.draw_end else None
        if input == "OBSTACLE":
            self.draw_obstacles = not self.draw_obstacles
            self.in_progress = input if self.draw_obstacles else None
    
    def toggle_menu(self):
        self.menu_reveal = not self.menu_reveal
        
    def confirm_button_callback(self):
        self.toggle_input(self.in_progress)
    
    def reset(self):
        self.reset_signal = True
    
    def resume(self):
        self.menu_reveal = not self.menu_reveal

async def main():
    global running, screen, app, menu
    app = app()
    menu = menu()
    while running:                                        
        for event in pygame.event.get():            
            if event.type == QUIT:
                running = False            
            if event.type == KEYDOWN:
                if event.key == K_a:
                    menu.toggle_input("START")
                if event.key == K_s:
                    menu.toggle_input("END")
                if event.key == K_d:
                    menu.toggle_input("OBSTACLE")
                if event.key == K_BACKSPACE:
                    menu.reset()
                if event.key == K_RETURN:
                    # menu.confirm_button_callback()
                    if app.start_node and app.end_node:
                        app.path = path_finder(app.maze, tuple(app.start_node), tuple(app.end_node), app.obstacle)                   
                    print("path \n", app.path)
                if event.key == K_ESCAPE:
                    menu.toggle_menu()
                if event.key == K_f:
                    if not fullscreen_flag:                    
                        screen = pygame.display.set_mode((0,0), FULLSCREEN)
                    else:                    
                        screen = pygame.display.set_mode((default_width, default_height))
                    fullscreen_flag = not fullscreen_flag
                    app.update_display_elements()
        # Update menu selection
        app.is_menu_on = menu.menu_reveal
        app.draw_obstacle = menu.draw_obstacles
        app.draw_start = menu.draw_start
        app.draw_end = menu.draw_end        
        menu.reset_signal = app.reset(menu.reset_signal)
        
        # Background
        screen.fill(OATYELLOW)        
        # Draw main section
        app.draw_borders(screen)
        app.draw_nodes(screen)
        # Draw menu section
        menu.draw_menu_panel(screen)
        # Draw help button
        # menu.draw_help_panel(screen)
        
        # debug(f"{pygame.mouse.get_pos()}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        
        debug(f"{menu.in_progress if menu.in_progress else ''}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        pygame.display.update()
        clock.tick(fps)
        await asyncio.sleep(0)


if __name__ == '__main__':    
    asyncio.run(main())
    


