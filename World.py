import pygame
from Blocks import *
from config import * 


class World:
    """
    A world with a grid what a nice place to live in!
    """
    def __init__(self,screen_size,background,margin=(0,0)):
        self.screen_size = screen_size
        self.background = background
        self.win = pygame.display.set_mode((screen_size[0],screen_size[1]+BOTTOM_PANEL_HEIGHT))
        self.available_blocks = None
        self.width,self.height = self.screen_size[0],self.screen_size[1]
        self.margin_x,self.margin_y = margin
        self.blocksGenerated = False
        self._available_nodes = None #Type dictionary where block id is a key
        self._available_edges = None
    def create_grids(self):
        self.win.fill(background)
        """
        Creating grids with margin
        Actual margin given is screen_width - totalGrid*NodeSize + margin
        y is positive in downward direction and x in right direction
        """
        if self.blocksGenerated:
            self.redraw_world()
            return #if blocks are generated no regenerating required just redraw
        
        total_cols = int((self.width-self.margin_x)/BLOCK_SIZE)
        total_rows = int((self.height-self.margin_y)/BLOCK_SIZE)
        start_x = int((self.margin_x + (self.width - total_cols*BLOCK_SIZE))/2)
        start_y = int((self.margin_y + (self.height - total_rows*BLOCK_SIZE))/2)
        for col in range(0,total_cols):
            cols = []
            for row in range(0,total_rows):
                x = start_x+BLOCK_SIZE*col
                y = start_y+BLOCK_SIZE*row
                id = (col,row)
                block = Block(x,y,BLOCK_SIZE,id,self,GRID_COLOR,GRID_WIDTH)
                block.draw_block(self.win)
                cols.append(block)
            if not self.blocksGenerated:
                self.add_blocks(cols)
        self.blocksGenerated = True
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
        self._available_nodes[node.id] = node

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
            print("Deleting a node which doesn't exists")

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
    def add_edge(self,e:Edge):
        """
        Add edge between two nodes
        """
        #FIX-ME Make it work for directed graph as well
        (node1_id,node2_id) = (e.getNodes()[0].id,e.getNodes()[1].id)
        key = tuple(sorted((node1_id,node2_id)))#The key of the edge is nodes in sorted ascending order
        if self._available_edges is None:
            self._available_edges = {}
        self._available_edges[key] = e
    def remove_edge(self,nodeStartID:tuple,nodeEndID:tuple):
        """
        Removes the edge between nodeStartID and nodeEndID
        ID is node if i.e. location in 2D grid
        """
        key = tuple(sorted((nodeStartID,nodeEndID)))#The key of the edge is nodes in sorted ascending order
        try:
            del self._available_edges[key] #Will also trigger destructor
        except KeyError:
            print("Edge to be deleted Doesn't exists")
    def _removeEdges(self,node:Node):
        """
        Function removes all the edges containing the given node
        """
        for endNode in node.get_neighbours():
            self.remove_edge(node.id,endNode.id)
    def _updateEdges(self,node:Node,oldLoc:tuple):
        """
        Updates the edge for avaialable_edges
        """
        for endNode in node.get_neighbours():
            edge = self.getEdge(oldLoc,endNode.id)
            self.remove_edge(oldLoc,endNode.id) #Remove the edge from the dict
            self.add_edge(edge)
    
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
        details =   "World Details\nScreen Size - "+str(self.width)+"x"+str(self.height)+"\n"+"Total Blocks - "+str(len(self.available_nodes))+"\n"
        return details

