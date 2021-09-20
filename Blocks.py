import pygame
from config import NODE_BORDER_COLOR,SELECTED_NODE_COLOR
import math
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
        self._isHighlighted = False #Highlighting the blocks
    def draw_block(self,screen):
        self.pgObj = pygame.draw.rect(screen, self.grid_color, pygame.Rect((self.x, self.y, self.size,self.size)), self.grid_width)
        if self._isHighlighted:
            pygame.draw.rect(screen,self.grid_color,pygame.Rect((self.x+2, self.y+2, self.size-4,self.size-4)))
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

    def getWorld(self):
        """
        Returns the world in which the block is created
        """
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

COLOR_ACTIVE = pygame.Color('dodgerblue2')
class Node(Block):
    """
    A node is a type of block that is important to the world
    """
    def __init__(self, block:Block,label,colorOutline,colorNode,outlineWidth:int=2,specialNodeStatus:bool = False):
        super().__init__(block.x,block.y,block.size,block.id,block.getWorld(),block.grid_color,block.grid_width)

        self._label = label
        self._colorOutline = colorOutline
        self._colorNode = colorNode
        self._defaultOutlineColor = colorOutline
        self.pos = block.pos()
        self._font = pygame.font.Font(None, int(self.size*0.80))
        self.txt_surface = self._font.render(label, True, self._colorOutline)
        self._outlineWidth = outlineWidth
        self._oldLabel = None #Label before editing happened
        self._active = False #A node is active when it's selected
        self._specialNodeStatus = specialNodeStatus #Tells whether the node is special or not, Goal and Start nodes must be special
        self._isSelected = False
        #Send information to world about each node created
        self.getWorld().add_node(self)

        self._neighbourNodes = [] #Neighbour nodes that are connected with an edge

    def draw_block(self,screen):
        pygame.draw.circle(screen, self._colorNode, self.pos,int(self.size/2))
        outlineColor = SELECTED_NODE_COLOR if self._isSelected else self._colorOutline
        self.pgObj = pygame.draw.circle(screen, outlineColor, self.pos,int(self.size/2),self._outlineWidth)
        self.set_label(self._label,screen)
    def set_label(self,label,screen):
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
        self._colorNode = color
    def get_label(self):
        return self._label
    def setLocation(self,block:Block):
        """
        A location in grid is defined by the block
        Set location to a particular block position
        """
        self.pos = block.pos()
        self.id = block.id
    def handle_event(self, event):
        """
        Function handles the event
        Allows to edit the label of node using keypress
        Once deleted function returns False
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the node rect.
            if self.pgObj.collidepoint(event.pos):
                print("Use your keyboard to add/edit label to the node\n Press DELETE to remove the node")
                # Toggle the active variable.
                self._active = not self._active
                if self._active:
                    self._oldLabel = self._label
            else:
                self._active = False
            
            #Change the label to new value after checking validity
            if not self._active and (self._oldLabel is not None and self._oldLabel != self._label):
                #Try saving the new label
                self._saveNewLabel(self._oldLabel) #Discarding if no valid
                self._oldLabel = None
            # Change the current color of the input box.
            self._colorOutline = COLOR_ACTIVE if self._active else self._defaultOutlineColor
        
        if event.type == pygame.KEYDOWN:
            if self._active:
                if event.key == pygame.K_RETURN:
                    self._saveNewLabel(self._oldLabel) #Discarding if no valid
                    self._active = False
                    self._colorOutline = self._defaultOutlineColor
                elif event.key == pygame.K_BACKSPACE:
                    self._label = self._label[:-1]
                elif event.key == pygame.K_DELETE:
                    #delete the node
                    if not self._specialNodeStatus:
                        print("Deleted {}".format(self))
                        self.getWorld().remove_node(self.id)
                        return False
                    else:
                        print("Special node delete Permission Denied!\nNOTE: Special nodes like Start and Goal can't be deleted")
                else:
                    self._label += event.unicode
                # Re-render the text.
                self.txt_surface = self._font.render(self._label, True, self._colorOutline)
        return True
    def _saveNewLabel(self,oldLabel):
            """
            Function saves the label only if the new label is valid else switch back to old label
            """
            #Label is already saved check whether we want to discard it or not
            #Deal with empty label
            if len(self._label)==0:
                print("Node must have a label to identify!")
                self._label = oldLabel
                return False
            #Deal with duplicate labels
            if self._label in self.getWorld().getNodes().values():
                print("Duplicate labels are not allowed!")
                self._label = oldLabel
                return False
            print("Label changed from {} to {}".format(oldLabel,self._label))
    
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
    """
    def __init__(self,nodeStart:Node,nodeEnd:Node,weight = 0,edgeColor = NODE_BORDER_COLOR,edgeWidth = 3):
        self._edgeColor = edgeColor
        self._defaultEdgeColor = edgeColor
        self._edgeWidth = edgeWidth
        self._weight = weight
        self._weightLabel = str(weight)
        self._nodeStart = nodeStart #Start of the edge
        self._nodeEnd = nodeEnd #End of the edge
        self._world = nodeStart.getWorld() #Fix-ME Find alternate for updating the world about the edge created

        ##Inform the world that edge is created
        self._world.add_edge(self)

        #Inform the nodes that edge is created
        self._nodeStart.add_neighbour(self._nodeEnd) #Add neighbours
        self._nodeEnd.add_neighbour(self._nodeStart) #Add neighbour

        self._font = pygame.font.Font(None, int(self._nodeStart.size*0.80))
        self.txt_surface = self._font.render(self._weightLabel, True, self._edgeColor)

        self._active = False #An edge is active if selected
        self._oldWeight = None
    
    def handle_event(self, event):
        """
        Function handles the event
        Allows to set weight or delete an Edge
        Once an edge deleted function returns False
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the edge rect.
            if self.collidePoint(event.pos):
                print("Use your keyboard to add/edit weight of the edge\nPress DELETE to remove the edge")
                # Toggle the active variable.
                self._active = not self._active
                if self._active:
                    self._oldWeight = self._weightLabel
            else:
                self._active = False
            
            #Change the label to new value after checking validity
            if not self._active and (self._oldWeight is not None and self._oldWeight != self._weightLabel):
                #Try saving the new label
                self._saveNewLabel(self._oldWeight) #Discarding if not valid
                self._oldWeight = None
            # Change the current color of the input box.
            self._edgeColor = COLOR_ACTIVE if self._active else self._defaultEdgeColor
        
        if event.type == pygame.KEYDOWN:
            if self._active:
                if event.key == pygame.K_RETURN:
                    self._saveNewLabel(self._oldWeight) #Discarding if no valid
                    self._active = False
                    self._edgeColor = self._defaultEdgeColor
                elif event.key == pygame.K_BACKSPACE:
                    self._weightLabel = self._weightLabel[:-1]
                elif event.key == pygame.K_DELETE:
                    #delete the node
                    print("Deleted {}".format(self))
                    self._world.remove_edge(self)
                    return False
                else:
                    self._weightLabel += event.unicode
                # Re-render the text.
                self.txt_surface = self._font.render(self._weightLabel, True, self._edgeColor)
        return True
    def _saveNewLabel(self,oldLabel):
        """
        Discard the value if it's invalid else saves the value
        """
        #Deal with empty string
        if len(self._weightLabel)==0:
            print("Edge must contain a weight")
            self._weightLabel = oldLabel
            return False
        try:
            weight = int(self._weightLabel)
            self._weightLabel = str(weight)
            self._weight = weight
            print("{} new weight - {}".format(self,self._weightLabel))
            return True
        except ValueError:
            print("Edge weight value must be an integer")
            self._weightLabel = oldLabel
            return False
    
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
        return self._weight

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

        
    def __str__(self):
        return "<Edge {} - {}>".format(self._nodeStart.get_label(),self._nodeEnd.get_label())
