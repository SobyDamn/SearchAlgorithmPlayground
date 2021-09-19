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
    def draw_block(self,screen):
        self.pgObj = pygame.draw.rect(screen, self.grid_color, pygame.Rect((self.x, self.y, self.size,self.size)), self.grid_width)
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
    def add_color(self,color:tuple):
        """
        Changing color of a block
        """
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

COLOR_ACTIVE = pygame.Color('dodgerblue2')
class Node(Block):
    """
    A node is a type of block that is important to the world
    """
    def __init__(self, block:Block,label,colorOutline,colorNode,outlineWidth:int=2,specialNodeStatus:bool = False):
        self._label = label
        self._colorOutline = colorOutline
        self._colorNode = colorNode
        self._defaultOutlineColor = colorOutline
        self.pos = block.pos()
        super().__init__(block.x,block.y,block.size,block.id,block.getWorld(),block.grid_color,block.grid_width)
        #Send information to world about each node created
        self.getWorld().add_node(self)
        self._font = pygame.font.Font(None, int(self.size*0.80))
        self.txt_surface = self._font.render(label, True, self._colorOutline)
        self._outlineWidth = outlineWidth
        self._oldLabel = None #Label before editing happened
        self._active = False #A node is active when it's selected
        self._specialNodeStatus = specialNodeStatus #Tells whether the node is special or not, Goal and Start nodes must be special
    def draw_block(self,screen):
        pygame.draw.circle(screen, self._colorNode, self.pos,int(self.size/2))
        self.pgObj = pygame.draw.circle(screen, self._colorOutline, self.pos,int(self.size/2),self._outlineWidth)
        self.set_label(self._label,screen)
    def set_label(self,label,screen):
        """
        Set the label for the node
        """
        self._label = label
        text = self._font.render(self._label, True, self._colorOutline)
        text_rect = text.get_rect(center = self.pgObj.center)
        screen.blit(text, text_rect)
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
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.pgObj.collidepoint(event.pos):
                print("Use your keyboard to add/edit label to the node")
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
                    print("New Label for {}: {}".format(self.id,self._label))
                    self._active = False
                    self._colorOutline = self._defaultOutlineColor
                elif event.key == pygame.K_BACKSPACE:
                    self._label = self._label[:-1]
                elif event.key == pygame.K_DELETE:
                    #delete the node
                    if not self._specialNodeStatus:
                        print("Deleted {}".format(self))
                        self.getWorld().remove_node(self.id)
                    else:
                        print("Special node delete Permission Denied!\nNOTE: Special nodes like Start and Goal can't be deleted")
                else:
                    self._label += event.unicode
                # Re-render the text.
                self.txt_surface = self._font.render(self._label, True, self._colorOutline)
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

    def __str__(self):
        return "<Node label = "+ self._label+" id = "+str(self.id)+">"