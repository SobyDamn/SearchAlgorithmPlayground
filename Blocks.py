import pygame
from config import NODE_BORDER_COLOR,SELECTED_NODE_COLOR
import math
class Block:
    """
    Block defines the world tiles
    ...

    Attribute
    ---------
    x:int
        x coordinate in the window plane of the block

    y:int
        y coordinate in the window plane of the block

    size:int
        size of the block, denotes one side of the square block
    
    id:tuple
        id represents position in the 2D matrix of the block
        (x,y) where x is the row and y is the column
    
    pgObj
        pygame rect object
    
    Methods
    -------
    draw_block(screen)
        draws the block on pygame window
        screen: pygame window

    highlight(val:bool)
        highlights block with highlist color
        val:bool - true to enable highlight
    
    pos() -> tuple
        returns the coordinate of the centre of the block on the pygame window
    
    setHasNode(val:bool)
        sets the value for the flag _hasNode to represent that a block contains a node
    
    hasNode()->bool
        returns true if block has node over it

    to_dict()->dict
        returns the object details with all attribute and values as dictionary

    """
    def __init__(self,x:int,y:int,size:int,id:tuple,grid_color:tuple = (163, 175, 204),grid_width:int = 1):
        """
        Parameters
        ---------
        x:int
            x coordinate in the window plane of the block

        y:int
            y coordinate in the window plane of the block

        size:int
            size of the block, denotes one side of the square block

        id:tuple
            id represents position in the 2D matrix of the block
            (x,y) where x is the row and y is the column

        gird_color:tuple
            rgb color (r,g,b) value for the block boundary default ((163, 175, 204))

        grid_width:int
            width of the boundary default 1
        """
        self.x = x
        self.y = y
        self.size = size
        self._grid_color = grid_color
        self._grid_width = grid_width
        self.id = id
        self._hasNode = False #Tells whether there is a node over the block
        self.pgObj = None #pyGame object
        self._isHighlighted = False #Highlighting the blocks
    def draw_block(self,screen):
        """
        Draws the block on the screen
        """
        self.pgObj = pygame.draw.rect(screen, self._grid_color, pygame.Rect((self.x, self.y, self.size,self.size)), self._grid_width)
        if self._isHighlighted:
            pygame.draw.rect(screen,self._grid_color,pygame.Rect((self.x+2, self.y+2, self.size-4,self.size-4)))
    def highlight(self,val:bool):
        """
        Highlight the block
        Useful to show which block is selected
        """
        self._isHighlighted = val
    def pos(self):
        """
        Returns Exact coordinates in 2D screen space
        """
        if self.pgObj is None:
            raise AttributeError("Block is not yet drawn")
        else:
            return self.pgObj.center
    
    def __str__(self):
        return "<Block id="+str(self.id)+">"

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
    def to_dict(self)->dict:
        """
        Returns the attributes and values as dictionary
        """
        block = {
            "x": self.x,
            "y":self.y,
            "id":self.id,
            "size":self.size,
            "gird_color":str(self._grid_color),
            "grid_width": self._grid_width,
            "hasNode": self._hasNode
        }
        return block

COLOR_ACTIVE = pygame.Color('dodgerblue2')
class Node(Block):
    """
    A node is a type of block that is important to the world 
    Node class inherits the Block class
    ...

    Attributes
    ----------
    x:int
        x coordinate in the window plane of the block

    y:int
        y coordinate in the window plane of the block

    size:int
        size of the block, denotes one side of the square block
    
    id:tuple
        id represents position in the 2D matrix of the block
        (x,y) where x is the row and y is the column
    
    pgObj
        pygame rect object
    
    pos:tuple
        coordinate in pygame window for center of the node

    Methods
    -------
    draw_block(screen)
        draws the node on pygame window
        screen: pygame window

    highlight(val:bool)
        highlights block with highlist color
        val:bool - true to enable highlight
    
    pos() -> tuple
        returns the coordinate of the centre of the block on the pygame window
    
    setHasNode(val:bool)
        sets the value for the flag _hasNode to represent that a block contains a node
    
    hasNode()->bool
        returns true if block has node over it

    to_dict()->dict
        returns the object details with all attribute and values as dictionary
    
    set_label(label:str,screen)
        sets the label on the node
        screen - a pygame window
        label:str - a string value that'll be displayed on node

    selected(val:bool)
        sets isSelected flag value

    set_color(color:tuple)
        sets the color of the node
        color:tuple - A rgb value in the form (r,g,b)
    
    get_label()->str
        returns value of label of the node

    setLocation(block:Block)
        sets the location to the new block
        block:Block - A Block class object
        NOTE: Location for nodes are defined by the block they resides on

    handle_event(world:World,event,infoLabel)
        Internal method to handle the pygame events
    
    add_neighbour(node:Node)
        Adds the given node as neighbouring node if it's not already a neighbouring node, should be used when it has an edge with the given node
        node:Node - A Node class object

    remove_neighbour(node:Node)
        Removes the given node from neighbouring node if it's in neighbouring node
        node:Node - A Node class object
    
    get_neighbour()->list
        Returns list of neighbouring nodes(Node class objects) which is sorted in order with their label
    

    """
    def __init__(self, block:Block,label:str,colorOutline:tuple,colorNode:tuple,outlineWidth:int=2,specialNodeStatus:bool = False):
        super().__init__(block.x,block.y,block.size,block.id,block._grid_color,block._grid_width)
        """
        Parameters
        -----------
        block:Block
            A Block class object on which the node will be drawn

        label:str
            Label of the node
        
        colorOutline:tuple
            A rgb value of the form (r,g,b) represents outline color of the node

        colorNode:tuple
            A rgb value of the form (r,g,b) represents color of the node

        outlineWidth:int
            Width of the outline of the node default 2

        specialNodeStatus:bool
            sets whether the node is special default is False
            NOTE: A special node must be present on playground all time, i.e. delete is not allowed

        """
        self._label = label
        self._colorOutline = colorOutline
        self._colorNode = colorNode
        self._defaultOutlineColor = colorOutline
        self.pos = block.pos()
        self._font = pygame.font.Font(None, int(self.size*0.80))
        self._txt_surface = self._font.render(label, True, self._colorOutline)
        self._outlineWidth = outlineWidth
        self._oldLabel = None #Label before editing happened
        self._active = False #A node is active when it's selected
        self._specialNodeStatus = specialNodeStatus #Tells whether the node is special or not, Goal and Start nodes must be special
        self._isSelected = False

        self._neighbourNodes = [] #Neighbour nodes that are connected with an edge

    def draw_block(self,screen):
        """
        Draws the node on the screen
        """
        pygame.draw.circle(screen, self._colorNode, self.pos,int(self.size/2))
        outlineColor = SELECTED_NODE_COLOR if self._isSelected and not self._active else self._colorOutline
        self.pgObj = pygame.draw.circle(screen, outlineColor, self.pos,int(self.size/2),self._outlineWidth)
        self.set_label(self._label,screen)
    def set_label(self,label:str,screen):
        """
        Set the label for the node
        """
        self._label = label
        text = self._font.render(self._label, True, self._colorOutline)
        text_rect = text.get_rect(center = self.pgObj.center)
        screen.blit(text, text_rect)

    def selected(self,val:bool):
        """
        Set the node selected 
        """
        self._isSelected = val
    
    def set_color(self,color:tuple):
        """
        Set the color for the node
        NOTE: Color is triplet of rgb i.e. (255,255,255)
        """
        if not self._specialNodeStatus:
            self._colorNode = color
    def get_label(self)->str:
        return self._label
    def setLocation(self,block:Block):
        """
        A location in grid is defined by the block
        Set location to a particular block position
        """
        self.pos = block.pos()
        self.id = block.id
    def handle_event(self,world, event,infoLabel):
        """
        Function handles the event happening in the world
        Allows to edit the label of node using keypress
        Once deleted function returns False
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the node rect.
            if self.pgObj.collidepoint(event.pos):
                helpText = "Use your keyboard to add/edit label to the node. Press DELETE to remove the node"
                #print(helpText)
                infoLabel.setValue(helpText)
                # Toggle the active variable.
                self._active = not self._active
                if self._active:
                    self._oldLabel = self._label
                else:
                    infoLabel.setValue(str(self))
                    self._isSelected = True
            else:
                self._active = False
            #Change the label to new value after checking validity
            if not self._active and (self._oldLabel is not None and self._oldLabel != self._label):
                #Try saving the new label
                self._saveNewLabel(self._oldLabel,world,infoLabel) #Discarding if no valid
                self._oldLabel = None
            # Change the current color of the input box.
            self._colorOutline = COLOR_ACTIVE if self._active else self._defaultOutlineColor
        
        if event.type == pygame.KEYDOWN:
            if self._active:
                if event.key == pygame.K_RETURN:
                    self._saveNewLabel(self._oldLabel,world,infoLabel) #Discarding if no valid
                    self._active = False
                    self._colorOutline = self._defaultOutlineColor
                elif event.key == pygame.K_BACKSPACE:
                    self._label = self._label[:-1]
                elif event.key == pygame.K_DELETE:
                    #delete the node
                    if not self._specialNodeStatus:
                        helpText = "Deleted {}".format(self)
                        #print(helpText)
                        infoLabel.setValue(helpText)
                        world.remove_node(self.id)
                        return False
                    else:
                        helpText = "Special node delete Permission Denied! NOTE: Special nodes like Start and Goal can't be deleted"
                        #print(helpText)
                        infoLabel.setValue(helpText)
                else:
                    self._label += event.unicode
                # Re-render the text.
                self._txt_surface = self._font.render(self._label, True, self._colorOutline)
        return True
    def _saveNewLabel(self,oldLabel,world,infoLabel):
            """
            Function saves the label only if the new label is valid else switch back to old label
            """
            #Label is already saved check whether we want to discard it or not
            #Deal with empty label
            if len(self._label)==0:
                helpText = "Node must have a label to identify!"
                #print(helpText)
                infoLabel.setValue(helpText)
                self._label = oldLabel
                return False
            #Deal with duplicate labels
            if self._label in world.getNodes().values():
                #print(helpText)
                infoLabel.setValue(helpText)
                self._label = oldLabel
                return False
            helpText = "Label changed from {} to {}".format(oldLabel,self._label)
            #print(helpText)
            infoLabel.setValue(helpText)
    
    def add_neighbour(self,node):
        """
        Adds a node as neighbour if it doesn't exists already
        """
        if node not in self._neighbourNodes:
            self._neighbourNodes.append(node)
    def remove_neighbour(self,node):
        """
        Remove the node from the neighbour if it exists
        """
        if node in self._neighbourNodes:
            self._neighbourNodes.remove(node)
    def get_neighbours(self)->list:
        """
        Returns list of neighbours in sorted order of the label
        """
        return sorted(self._neighbourNodes)
    def to_dict(self)->dict:
        """
        Returns the node parameters in dictionary format
        """
        node = {
            "block_id":str(self.id), #To initalise the parent
            "label":self._label,
            "colorOutline":str(self._defaultOutlineColor),
            "colorNode":str(self._colorNode),
            "pos":str(self.pos),
            "outlineWidth":self._outlineWidth,
            "specialNodeStatus":self._specialNodeStatus,
            #Edge updates the neighbour for the node need not to be included
        }
        return node
    def __eq__(self, label:str)->bool:
        """
        Equality between label of the node
        """
        #If the label is being edited check with oldLabel, this will help whether we want to discard the label or not
        if self._oldLabel is not None:
            if label==self._oldLabel:
                return True
            else:
                return False
        if label==self._label:
            return True
        else:
            return False
    def __lt__(self,value:str)->bool:
        """
        Label comparator
        """
        if self._label < value:
            return True
        else:
            return False
    
    def __gt__(self, value:str)->bool:
        """
        Label comparator
        """
        if self._label > value:
            return True
        else:
            return False

    def __ge__(self, value:str)->bool:
        """
        Label comparator
        """
        if self._label >= value:
            return True
        else:
            return False

    def __le__(self, value:str)->bool:
        """
        Label comparator
        """
        if self._label <= value:
            return True
        else:
            return False
    def __str__(self):
        return "<Node label = "+ self._label+" id = "+str(self.id)+">"



class Edge:
    """
    An edge class represents an edge between 2 nodes
    ...

    Attribute
    ---------
    pgObj
        A pygame rect object
    
    Methods
    -------
    handle_event(world:World,event,infoLabel)
        Internal method to handle the pygame events

    set_color(color:tuple)
        Sets color of the edge
        color:tuple - A rgb value of the form (r,g,b)
    
    collidePoint(clickPoint,offeset=5)
        Returns true if the given click point is inside the offset value on edge

    draw_edge(screen)
        Draws edge on the screen
        screen - A pygame window

    getNodes()->tuple
        Returns the pair of node which the edge is connecting

    get_weight()->int
        Returns the weight of the edge

    to_dict()->dict
        Returns the object details its attributes and value as dictionary

    """
    def __init__(self,nodeStart:Node,nodeEnd:Node,isWeighted:bool = False,weight = 0,edgeColor = NODE_BORDER_COLOR,edgeWidth = 3):
        """
        Parameters
        ----------
        nodeStart:Node
            A Node class object which represents the starting node of the edge

        nodeEnd:Node
            A Node class object which represents the ending node of the edge

        isWeighted:bool
            Whether the edge drawn between the node has weight or not, default False

        weight:int
            Wieght of the edge, default 0

        edgeColor:tuple
            A rgb value of the form (r,g,b) which represents the color of the edge, default value _NODE_BORDER_COLOR_
        
        edgeWidth:int
            Width of the edge, default 3
        """
        self._edgeColor = edgeColor
        self._defaultEdgeColor = edgeColor
        self._edgeWidth = edgeWidth
        self._weight = weight
        self._weightLabel = str(weight)
        self._nodeStart = nodeStart #Start of the edge
        self._nodeEnd = nodeEnd #End of the edge
        self._isWeighted = isWeighted

        #Inform the nodes that edge is created
        self._nodeStart.add_neighbour(self._nodeEnd) #Add neighbours
        self._nodeEnd.add_neighbour(self._nodeStart) #Add neighbour

        self._font = pygame.font.Font(None, int(min(30,self._nodeStart.size*0.80)))
        self._txt_surface = self._font.render(self._weightLabel, True, self._edgeColor)

        self._active = False #An edge is active if selected
        self._oldWeight = None
        self.pgObj = None
    
    def handle_event(self, world,event,infoLabel):
        """
        Function handles the event happening in the world with the node
        Allows to set weight or delete an Edge
        Once an edge deleted function returns False
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the edge rect.
            if self.collidePoint(event.pos):
                helpText = ""
                if self._isWeighted:
                    helpText +="Use your keyboard to add/edit weight of the edge"
                    #print(helpText)
                helpText += "Press DELETE to remove the edge"
                infoLabel.setValue(helpText)
                #print(helpText)
                # Toggle the active variable.
                self._active = not self._active
                if self._active:
                    self._oldWeight = self._weightLabel
                else:
                    infoLabel.setValue("")
            else:
                self._active = False
            
            #Change the label to new value after checking validity
            if not self._active and (self._oldWeight is not None and self._oldWeight != self._weightLabel):
                #Try saving the new label
                self._saveNewLabel(self._oldWeight,infoLabel) #Discarding if not valid
                self._oldWeight = None
            # Change the current color of the input box.
            self._edgeColor = COLOR_ACTIVE if self._active else self._defaultEdgeColor
        
        if event.type == pygame.KEYDOWN:
            if self._active:
                if event.key == pygame.K_RETURN:
                    self._saveNewLabel(self._oldWeight,infoLabel) #Discarding if no valid
                    self._active = False
                    self._edgeColor = self._defaultEdgeColor
                elif event.key == pygame.K_BACKSPACE:
                    self._weightLabel = self._weightLabel[:-1]
                elif event.key == pygame.K_DELETE:
                    #delete the node
                    helpText = "Deleted {}".format(self)
                    infoLabel.setValue(helpText)
                    #print(helpText)
                    world.remove_edge(self)
                    return False
                else:
                    self._weightLabel += event.unicode
                # Re-render the text.
                self._txt_surface = self._font.render(self._weightLabel, True, self._edgeColor)
        return True
    def _saveNewLabel(self,oldLabel,infoLabel):
        """
        Discard the value if it's invalid else saves the value
        """
        #Deal with empty string
        if len(self._weightLabel)==0:
            helpText = "Edge must contain a weight"
            infoLabel.setValue(helpText)
            #print(helpText)
            self._weightLabel = oldLabel
            return False
        try:
            weight = int(self._weightLabel)
            self._weightLabel = str(weight)
            self._weight = weight
            helpText = "{} new weight - {}".format(self,self._weightLabel)
            infoLabel.setValue(helpText)
            #print(helpText)
            return True
        except ValueError:
            helpText = "Edge weight value must be an integer"
            infoLabel.setValue(helpText)
            #print(helpText)
            self._weightLabel = oldLabel
            return False
    def set_color(self,color:tuple):
        """
        Sets the color of the edge
        """
        self._edgeColor = color
    def collidePoint(self,clickPoint,offset=5):
        """
        Returns true if the click point is inside offset limit of the edge
        """
        if self.pgObj.collidepoint(clickPoint) and self._distance_point_line(clickPoint) < offset:
            return True
        else:
            return False
    def _distance_point_line(self,pt):
        """
        Returns normal distance at which the point pt is clicked from the line
        """
        l1 = self._nodeStart.pos
        l2 = self._nodeEnd.pos
        NV = pygame.math.Vector2(l1[1] - l2[1], l2[0] - l1[0])
        LP = pygame.math.Vector2(l1)
        P = pygame.math.Vector2(pt)
        return abs(NV.normalize().dot(P -LP))

    def draw_edge(self,screen):
        self.pgObj = pygame.draw.line(screen,self._edgeColor,self._nodeStart.pos,self._nodeEnd.pos,self._edgeWidth)
        if self._isWeighted:
            #A weighted edge will have a label representing it's weight
            self._set_label(self._weightLabel,screen)

    def getNodes(self)->tuple:
        """
        Returns the nodes the edge is connecting
        """
        return (self._nodeStart,self._nodeEnd)

    def get_weight(self)->int:
        """
        Returns the weight of the edge
        """
        return self._weight if self._isWeighted else 0

    def _set_label(self,label,screen,offset = 0.4):
        """
        Sets the label of weight to the edge
        height above the edge the label is placed is offset*nodeSize
        """
        h = self._nodeEnd.size*offset
        xc,yc = self.pgObj.center
        x1,y1 = min(self._nodeStart.pos,self._nodeEnd.pos)
        dist_sq = (xc-x1)**2 + (yc-y1)**2
        mid_dist = math.sqrt(dist_sq)
        phi = math.atan((h)/mid_dist)
        theta = math.pi/2 if xc-x1==0 else math.atan((yc-y1)/(xc-x1))
        hyp = math.sqrt((h)**2 + (mid_dist)**2)
        (x,y) = (x1+int(hyp*math.cos(theta+phi)),y1+int(hyp*math.sin(theta+phi)))
        text = self._font.render(label, True, self._edgeColor)
        text_rect = text.get_rect(center = (x,y))
        screen.blit(text, text_rect)

    def to_dict(self)->dict:
        """
        Returns edge parameter and it's value as dictionary
        """
        edge = {
            "nodeStart":str(self._nodeStart.id),
            "nodeEnd":str(self._nodeEnd.id),
            "edgeColor":str(self._edgeColor),
            "edgeWidth":self._edgeWidth,
            "weight":self._weight,
            "isWeighted":self._isWeighted
        }
        return edge
    def __str__(self):
        return "<Edge {} - {}>".format(self._nodeStart.get_label(),self._nodeEnd.get_label())
