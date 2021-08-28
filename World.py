import pygame
from Node import Node
from config import * 

class World:
    def __init__(self,screen_size,background,margin=(0,0)):
        self.screen_size = screen_size
        self.background = background
        self.win = pygame.display.set_mode((screen_size))
        self.available_nodes = None
        self.width,self.height = self.screen_size[0],self.screen_size[1]
        self.margin_x,self.margin_y = margin
        self.nodeGenerated = False
    def create_grids(self):
        self.win.fill(background)
        """
        Creating grids with margin
        Actual margin given is screen_width - totalGrid*NodeSize + margin
        y is positive in downward direction and x in right direction
        """
        if self.nodeGenerated:
            self.redraw_nodes()
            return #if nodes are generated no regenerating required just redraw
        
        total_cols = int((self.width-self.margin_x)/NODE_SIZE)
        total_rows = int((self.height-self.margin_y)/NODE_SIZE)
        start_x = int((self.margin_x + (self.width - total_cols*NODE_SIZE))/2)
        start_y = int((self.margin_y + (self.height - total_rows*NODE_SIZE))/2)
        for col in range(0,total_cols):
            cols = []
            for row in range(0,total_rows):
                x = start_x+NODE_SIZE*col
                y = start_y+NODE_SIZE*row
                id = (col,row)
                node = Node(x,y,NODE_SIZE,id,self,GRID_COLOR,GRID_WIDTH)
                node.draw_node(self)
                cols.append(node)
            if not self.nodeGenerated:
                self.add_nodes(cols)
        self.nodeGenerated = True
    def redraw_nodes(self):
        if self.available_nodes is None:
            raise ValueError("Nodes are not available")
        else:
            for row in self.available_nodes:
                for node in row:
                    node.draw_node(self)
                    if node.isBlock:
                        node.add_color(BLOCK_COLOR)
    def add_nodes(self,col):
        """
        Method decides whether to add the row or not based on whether we have already added the node or not
        """
        if self.available_nodes is None:
            self.available_nodes = []
        self.available_nodes.append(col)
    def __str__(self):
        details =   "World Details\nScreen Size - "+str(self.width)+"x"+str(self.height)+"\n"+"Total Nodes - "+str(len(self.available_nodes))+"\n"
        return details
