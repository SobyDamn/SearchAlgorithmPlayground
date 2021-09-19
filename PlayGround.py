import pygame 
from World import World
from Blocks import *
from config import *
from UI import *
from BreadthFirstSearch import bfs
from DepthFirstSearch import dfs




class PlayGround:
    def __init__(self,world:World):
        self.world = world
        self.isClicked = False
        self._running = False
        self._selectedNode = None #This is the node which is selected, will help in moving the nodes around
        #A Playground consist of a start node and a goal node always
        self._startNode = Node(self.world.getBlock((0,0)),'S',SPECIAL_NODE_BORDER_COLOR,SPECIAL_NODE_COLOR,3,True)
        self._goalNode = Node(self.world.getBlock((len(self.world.available_blocks)-1,len(self.world.available_blocks[0])-1)),'G',SPECIAL_NODE_BORDER_COLOR,SPECIAL_NODE_COLOR,3,True)
        self._isDragging = False #True when clicked and mouse is dragging

    
    def _createControls(self):
        """
        Generates button to control the playground
        """
        height = int(BOTTOM_PANEL_HEIGHT/3)
        width = int(height*2)
        pos_x = int((SCREEN_WIDTH-width)/2)
        pos_y = (SCREEN_HEIGHT+int((BOTTOM_PANEL_HEIGHT-height)/2))
        self.startButton = Button(self.world,(pos_x,pos_y),(width,height),BUTTON_COLOR_PRIMARY,GRAY,"Run")
        ##Secondary buttons
        height = int(BOTTOM_PANEL_HEIGHT/3.5)
        width = int(height*1.8)
        pos_x = int((width)/2)
        self.selectStartButton = Button(self.world,(pos_x,pos_y),(width,height),BUTTON_COLOR_SECONDARY,GRAY,"Select Start",0.3)
        pos_x = int(SCREEN_WIDTH - (width)/2) - width
        self.selectGoalButton = Button(self.world,(pos_x,pos_y),(width,height),BUTTON_COLOR_SECONDARY,GRAY,"Select Goal",0.3)



    def _drawButtons(self):
        self.startButton.draw_node()
        self.selectGoalButton.draw_node()
        self.selectStartButton.draw_node()

    def _genLabel(self):
        def _nextLabel(label = ""):
            """
            A utility function to genLabel
            Counting with alphabet system
            Generates next label 
            """
            revL = [char for char in label[::-1]]
            n = len(revL)
            if n==0:
                return 'A'
            found = False
            for i in range(0,n):
                nextChar = chr(ord(revL[i])+1)
                if(nextChar <= 'Z'):
                    found = True
                    revL[i] = nextChar
                    break
                else:
                    revL[i] = 'A'
            if not found:
                revL.append('A')
            return ''.join(revL[::-1])
        """
        Function generates a label for a node which is not already there in the grid
        """
        label = "A"
        while label in self.world.getNodes().values():
            label = _nextLabel(label)
        return label


    def _getClickedBlock(self,pos)->Block:
        """
        Click Handler, checks if the click is button node or simple node and manages accordingly
        """

        blocks = self.world.available_blocks
        if not blocks:
            raise ValueError("Blocks are not initialised")
        else:
            for row in blocks:
                for block in row:
                    if block.pgObj.collidepoint(pos):
                        return block
    def _dragNode(self,newBlock):
        if self.isClicked and self._selectedNode is not None and not newBlock.hasNode():
            self.world.remove_node(self._selectedNode.id) #Remove from old position
            self._selectedNode.setLocation(newBlock)
            self.world.add_node(self._selectedNode) #Add to new position
            print("Dragging to {}".format(newBlock))
    def _handleClicks(self,event):
        block = self._getClickedBlock(event.pos)
        if block is not None:
            self._dragNode(block)
            if not self._isDragging:
                if block.hasNode():
                    self._selectedNode = self.world.getNode(block.id)
                elif not block.hasNode():
                    self._selectedNode = Node(block,self._genLabel(),NODE_BORDER_COLOR,NODE_COLOR)
            print(block)
        else:
            #If the click is made somewhere outside a grid
            self._selectedNode = None
            pass


    def eventHandler(self,event):
        if self._selectedNode is not None:
            self._selectedNode.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handleClicks(event)
            self.isClicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.isClicked = False
        elif event.type == pygame.MOUSEMOTION:
            if self.isClicked:
                self._isDragging = True
                self._handleClicks(event)
            else:
                self._isDragging = False
    def drawScenary(self):
        self.world.create_grids()

        pygame.display.update()
pygame.init()
pygame.display.set_caption(TITLE)
world = World(SCREEN_SIZE,background,(10,10))
world.create_grids()

#node = Node(world.available_blocks[0][0],"A",NODE_BORDER_COLOR,NODE_COLOR)
#print(node)
running = True
PG = PlayGround(world)
clock = pygame.time.Clock()
while running:
    PG.drawScenary()
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False
        else:
            PG.eventHandler(event)
    clock.tick(60)
pygame.quit()