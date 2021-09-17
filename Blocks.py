import pygame
class Block:
    """
    Block defines the world tiles
    id of the Block is it's index in a 2D grid array starting from (0,0)
    """
    def __init__(self,x,y,size,id:tuple,world,grid_color = (163, 175, 204),grid_width = 1):
        self.x = x
        self.y = y
        self.size = size
        self.grid_color = grid_color
        self.grid_width = grid_width
        self.id = id
        self._world = world
        self._hasNode = False #Tells whether there is a node over the block
        self.pyObj = None #pyGame object
    def draw_block(self):
        self.pgObj = pygame.draw.rect(self._world.win, self.grid_color, pygame.Rect((self.x, self.y, self.size,self.size)), self.grid_width)
    def pos(self):
        if self.pgObj is None:
            raise AttributeError("Block is not yet drawn")
        else:
            return self.pgObj.center
    
    def __str__(self):
        return "<Block id="+str(self.id)+">"
    def add_color(self,color:tuple):
        self.pgObj = pygame.draw.rect(self._world.win,color,pygame.Rect((self.x-1, self.y-1, self.size-1,self.size-1)))
    def getWorld(self):
        return self._world

    def setHasNode(self,val:bool):
        """
        Function sets the value whether the block has node or not
        """
        self._hasNode = val
    def hasNode(self)->bool:
        """
        Returns true if the block has a node over it
        """
        return self._hasNode


class Node(Block):
    """
    A node is a type of block that is important to the world
    """
    def __init__(self, block:Block,label,colorOutline,colorNode):
        self._label = label
        self._colorOutline = colorOutline
        self._colorNode = colorNode
        #Send information to world about each node created
        self.pos = block.pos()
        super().__init__(block.x,block.y,block.size,block.id,block.getWorld(),block.grid_color,block.grid_width)
        self.getWorld().add_node(self)
        self._font = pygame.font.SysFont('Arial', int(self.size*0.5))
    
    def draw_block(self):
        pygame.draw.circle(self.getWorld().win, self._colorNode, self.pos,int(self.size/2))
        self.pgObj = pygame.draw.circle(self.getWorld().win, self._colorOutline, self.pos,int(self.size/2),2)
        self.set_label(self._label)
    def set_label(self,label):
        #labelLength = self._fontSize*len(self._label)
        text = self._font.render(self._label, True, self._colorOutline)
        text_rect = text.get_rect(center = self.pgObj.center)
        self.getWorld().win.blit(text, text_rect)
    def setLocation(self,block:Block):
        self.pos = block.pos()
        self.id = block.id
    
    def __str__(self):
        return "<Node label = "+ self._label+" id = "+str(self.id)+">"