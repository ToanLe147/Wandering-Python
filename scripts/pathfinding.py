

class node():
    def __init__(self) -> None:
        self.neighbors = []
        self.previous = None
        self.START = False
        self.GOAL = False        
        self.weight = 0 if self.START else self.update_weight()
        self.distance = 0 if self.START else 1e6
    
    def update_weight(self, weight=1):
        self.weight = weight
            

class Path_Finder():
    def __init__(self) -> None:        
        self.shortest_path = []
    
    def set_goal(self, goal):
        self.goal_node = goal
    
    def set_starting_point(self, starting_point):
        self.starting_point = starting_point
    
    def Dijkstra_finder(self):
        pass
    
    def Astar_finder(self):
        pass