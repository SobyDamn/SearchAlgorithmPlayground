import pygame 
from World import World
from Blocks import *
from config import *
from BreadthFirstSearch import bfs
from DepthFirstSearch import dfs

class Button:
    def __init__(self,world,pos,size,bgColor,color,label="Button",labelSize:float=0.5):
        self._world = world
        self._pos = pos
        self.size = size
        self._color = color
        self._fontSize = int(size[1]*labelSize)
        self._label = label
        self._font = pygame.font.SysFont('Arial', self._fontSize)
        self._bgColor = bgColor

    def draw_node(self):
        pos = self._pos+self.size
        self.pgObj = pygame.draw.rect(self._world.win, self._bgColor, pygame.Rect(pos),  100, 3)
        labelLength = self._fontSize*len(self._label)
        text = self._font.render(self._label, True, self._color)
        text_rect = text.get_rect(center = self.pgObj.center)
        self._world.win.blit(text, text_rect)



class PlayGround:
    def __init__(self,world:World):
        self.world = world
        self.isClicked = False
        self._running = False
        self._selectedNode = None #This is the node which is selected, will help in moving the nodes around
        #A Playground consist of a start node and a goal node always
        self._startNode = Node(self.world.getBlock((0,0)),'S',SPECIAL_NODE_BORDER_COLOR,SPECIAL_NODE_COLOR,3)
        self._goalNode = Node(self.world.getBlock((len(self.world.available_blocks)-1,len(self.world.available_blocks[0])-1)),'G',SPECIAL_NODE_BORDER_COLOR,SPECIAL_NODE_COLOR,3)
        self._labelList = ["S","G"]

    
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

    def _nextLabel(self,label = ""):
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
    def _genLabel(self):
        """
        Function generates a label not in current label
        """
        label = "A"
        while label in self._labelList:
            label = self._nextLabel(label)
        self._labelList.append(label)
        return label


    def getClickedBlock(self,pos)->Block:
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
    def _handleClicks(self,pos):
        block = self.getClickedBlock(pos)
        if block is not None:
            self._dragNode(block)
            if block.hasNode() and self.isClicked:
                if self._selectedNode is None:
                    self._selectedNode = self.world.getNode(block.id)
            else:
                Node(block,self._genLabel(),NODE_BORDER_COLOR,NODE_COLOR)
                pass
            print(block)


    def eventHandler(self,event):
        if self._running:
            return #If algorithm is working jam the controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isClicked = True
            self._handleClicks(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.isClicked = False
            self._selectedNode = None
        elif event.type == pygame.MOUSEMOTION:
            if self.isClicked:
                self._handleClicks(event.pos)
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
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            PG.eventHandler(event)
    clock.tick(60)
pygame.quit()