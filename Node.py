import pygame
class Node:
    """
    id of the Node is it's index in a 2D grid array starting from (0,0)
    """
    def __init__(self,x,y,size,id:tuple,world,grid_color = (163, 175, 204),grid_width = 1):
        self.x = x
        self.y = y
        self.size = size
        self.grid_color = grid_color
        self.grid_width = grid_width
        self.id = id
        self._world = world
        self.isGoalNode = False
        self.isStartNode = False
        self.isBlock = False
    def draw_node(self, world):
        self.pgObj = pygame.draw.rect(self._world.win, self.grid_color, pygame.Rect((self.x, self.y, self.size,self.size)), self.grid_width)
    def pos(self):
        if self.pgObj is None:
            raise AttributeError("Node is not yet drawn")
        else:
            return self.pgObj.center
    
    def __str__(self):
        return "<Node id="+str(self.id)+">"
    def add_color(self,color:tuple):
        self.pgObj = pygame.draw.rect(self._world.win,color,self.pgObj)

class StartNode:
    def __init__(self,id:tuple,world,color:tuple = (3, 3, 66)):
        self.id = id
        self._font = pygame.font.SysFont('Arial', 25)
        self._world = world
        self._color = color
        if self._world.available_nodes is not None:
            try:
                self._node = self._world.available_nodes[self.id[0]][self.id[1]]
            except IndexError as e:
                print(e,id)
        else:
            raise ValueError("No nodes avalaible, available_nodes are not initialised!")
        self.pos = self._node.pos()
        self.draw_node()
    def _setLabel(self,label:str,color):
        if self._world.available_nodes is not None:
            self._node = self._world.available_nodes[self.id[0]][self.id[1]]
        else:
            raise ValueError("No nodes avalaible, available_nodes are not initialised!")
        pos = self._node.x,self._node.y
        self._world.win.blit(self._font.render(label, True, color), pos)
    def draw_node(self):
        if self._world.available_nodes is not None:
            try:
                self._node = self._world.available_nodes[self.id[0]][self.id[1]]
            except IndexError as e:
                print(e,id)
        else:
            raise ValueError("No nodes avalaible, available_nodes are not initialised!")
        self._node.isStartNode = True
        self.pgObj = pygame.draw.circle(self._world.win, self._color, self.pos,int(self._node.size/2))
    
    def moveTo(self,new_location:tuple,playGround,speed:int=10):
        print("Moving ",self.id,"->",new_location)
        new_node_loc = self._world.available_nodes[new_location[0]][new_location[1]].pos()
        x_dist,y_dist = new_node_loc[0] - self.pos[0],new_node_loc[1] - self.pos[1]
        playGround.drawScenary()
        while x_dist!=0 or y_dist!=0:
            x,y = 0,0
            if x_dist>0:
                x = 1
            else:
                x = -1
            if y_dist>0:
                y = 1
            else:
                y = -1
            pos = (self.pos[0]+x,self.pos[1]+y)
            self.pgObj = pygame.draw.circle(self._world.win, self._color, pos,int(self._node.size/2))
            self.pos = pos
            playGround.drawScenary()
            x_dist,y_dist = new_node_loc[0] - self.pos[0],new_node_loc[1] - self.pos[1]
            pygame.time.delay(speed)
        self.id = new_location

class GoalNode:
    def __init__(self,id,goal_img_src:str,world):
        self.id = id
        self._world = world
        self._image = pygame.image.load(goal_img_src)
    def draw_node(self):
        if self._world.available_nodes is not None:
            try:
                self._node = self._world.available_nodes[self.id[0]][self.id[1]]
            except IndexError as e:
                print(e,id)
        else:
            raise ValueError("No nodes avalaible, available_nodes are not initialised!")
        self._image = pygame.transform.scale(self._image, (self._node.size, self._node.size))
        self._world.win.blit(self._image, (self._node.x,self._node.y))
        self._node.isGoalNode = True
    def getPos(self)->tuple:
        return self._node.pos()
    
