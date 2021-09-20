import pygame
from Blocks import *


class World:
    def __init__(self,blocks_dimension:tuple,block_size:int,bottom_panel_size:int,grid_width:int = 1,background_color:tuple=(255,255,255),gird_color:tuple = ((232, 232, 232)),margin=10):
        """
        A world with a grid what a nice place to live in!
        blocks_dimension: dimension of the grid as (row,col)
        bottom_panel_size: size of the bottom pannel containing controls(min value allowed is 180)
        grid_width: width of the grid lines (default 1)
        background_color: Color of the background on which the world is drawn default as white
        block_size: size of each blocks (square)
        grid_color: color of the grid, default gray
        margin: margin between grid and corners(min value allowed is 10)
        """
        self._rows,self._cols = blocks_dimension
        self._background = background_color
        self.available_blocks = None
        self._margin = max(margin,10)
        self._screen_size = self._calc_screen_size(blocks_dimension,block_size,bottom_panel_size)
        self._width,self._height = self._screen_size[0],self._screen_size[1]
        self.win = pygame.display.set_mode((self._width,self._height))
        self._grid_width = grid_width
        self._block_size = block_size
        self._grid_color = gird_color
        self._blocksGenerated = False
        self._available_nodes = None #Type dictionary where block id is a key
        self._available_edges = None
        self.create_grids() #Initialise grid always as soon as world is created
    def _calc_screen_size(self,blocks_dimension,block_size,bottom_panel_size):
        """
        Returns size of the screen
        """
        screen_width = block_size*self._cols + 2*self._margin
        screen_height = block_size*self._rows + self._margin + max(bottom_panel_size,180)
        return (screen_width,screen_height)
    def create_grids(self):
        self.win.fill(self._background)
        """
        Create grid of blocks
        """
        if self._blocksGenerated:
            self.redraw_world()
            return #if blocks are generated no regenerating required just redraw
        
        total_cols = self._cols
        total_rows = self._rows
        start_x = self._margin
        start_y = self._margin
        for col in range(0,total_cols):
            cols = []
            for row in range(0,total_rows):
                x = start_x+self._block_size*col
                y = start_y+self._block_size*row
                id = (col,row)
                block = Block(x,y,self._block_size,id,self,self._grid_color,self._grid_width)
                block.draw_block(self.win)
                cols.append(block)
            if not self._blocksGenerated:
                self.add_blocks(cols)
        self._blocksGenerated = True
    def redraw_world(self):
        """
        Redraws frames of the world
        all the element on the world must be redrawn
        """
        if self.available_blocks is None:
            raise ValueError("Block are not available")
        else:
            for row in self.available_blocks:
                for block in row:
                    block.draw_block(self.win)
        #Draw edges
        if self._available_edges is not None:
            for edge in self._available_edges.values():
                edge.draw_edge(self.win)
        #Draw nodes
        if self._available_nodes is not None:
            for node in self._available_nodes.values():
                node.draw_block(self.win)
    def add_node(self,node:Node):
        """
        Add nodes to the world
        """
        #Dictionary is updated each time the node is moved in the grid
        if self._available_nodes is None:
            self._available_nodes = {}
        if not node.id in self._available_nodes:
            self._available_nodes[node.id] = node
        else:
            #print("{} already exists at thAT block location".format(node))
            pass

        #Now the block contains a node over it
        block = self.getBlock(node.id)
        block.setHasNode(True)
    
    def remove_node(self,id:tuple,forUpdate=False):
        """
        Deletes node with id as key from world
        """
        try:
            if not forUpdate:
                self._removeEdges(self._available_nodes[id])
            del self._available_nodes[id]
        except KeyError:
            print("World: Deleting a node which doesn't exists")

        #Now the block doesn't contains a node over it
        block = self.getBlock(id)
        block.setHasNode(False)
    def update_node_loc(self,node:Node,newBlock:Block):
        """
        Updates the location of a node to new block
        """
        #Deletes from last location and add to new location
        oldLoc = node.id #oldLoc id to update the edge dict
        self.remove_node(node.id,True)#remove from current block for update purpose
        node.setLocation(newBlock) #Update the location of the node
        self._updateEdges(node,oldLoc) #Update location in dictionary

        self.add_node(node) #Add updated location block
    def getEdges(self):
        """
        Returns list of edges
        """
        return self._available_edges
    def add_edge(self,e:Edge):
        """
        Add edge between two nodes
        """
        #FIX-ME Make it work for directed graph as well
        (node1_id,node2_id) = (e.getNodes()[0].id,e.getNodes()[1].id)
        key = tuple(sorted((node1_id,node2_id)))#The key of the edge is nodes in sorted ascending order
        if self._available_edges is None:
            self._available_edges = {}
        if not key in self._available_edges:
            self._available_edges[key] = e
        else:
            print("World: Edge between the nodes {} - {} already exists".format(e.getNodes()[0],e.getNodes()[1]))
            pass
    def remove_edge(self,edge:Edge):
        """
        Removes the edge
        """
        try:
            (sNode,eNode) = edge.getNodes()
            key = tuple(sorted((sNode.id,eNode.id)))#The key of the edge is nodes in sorted ascending order
            sNode.remove_neighbour(eNode)
            eNode.remove_neighbour(sNode)
            del self._available_edges[key] 
        except KeyError:
            print("World: Edge to be deleted Doesn't exists {}".format(key))
    def _removeEdges(self,node:Node):
        """
        Function removes all the edges from the given node
        """
        for endNode in node.get_neighbours():
            self.remove_edge(self.getEdge(node.id,endNode.id))
    def _updateEdges(self,node:Node,oldLoc:tuple):
        """
        Updates the edge for avaialable_edges
        """
        for endNode in node.get_neighbours():
            edge = self.getEdge(oldLoc,endNode.id)
            key = tuple(sorted((oldLoc,endNode.id)))#The key of the edge is nodes in sorted ascending order
            try:
                del self._available_edges[key]
                self.add_edge(edge)
            except KeyError:
                print("World: Error in updating the edge to world")
    
    def getEdge(self,startNodeID:tuple,endNodeID:tuple)->Edge:
        key = tuple(sorted((startNodeID,endNodeID)))
        return self._available_edges[key]
    def getNodes(self):
        """
        Returns available nodes in the world
        Dictionary of nodes id as key
        """
        return self._available_nodes
    def getNode(self,key):
        """
        key is tuple of location in the grid or 2D array
        Returns the node
        """
        return self._available_nodes[key]
    def getBlock(self,id):
        """
        Returns block associated with the id in the grid
        """
        x,y = id
        try:
            return self.available_blocks[x][y]
        except IndexError:
            raise("Provided 'id' doesn't contain any block")
    def add_blocks(self,col):
        """
        Method decides whether to add the row or not based on whether we have already added the node or not
        """
        if self.available_blocks is None:
            self.available_blocks = []
        self.available_blocks.append(col)
    def __str__(self):
        details =   "World Details\nScreen Size - "+str(self._width)+"x"+str(self._height)+"\n"+"Total Blocks - "+str(len(self.available_nodes))+"\n"
        return details

