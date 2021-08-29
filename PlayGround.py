import pygame 
from World import World
from Node import *
from config import *
from BreadthFirstSearch import bfs

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
    def __init__(self,world:World,goalNode:GoalNode = None,startNode:StartNode = None):
        self.world = world
        self.isClicked = False
        self.goalNode = goalNode
        self.startNode = startNode
        self._createControls()
        self._selectGoalClick = False
        self._selectStartClick = False
        self._running = False
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
            
    def getClickedNode(self,pos)->Node:
        """
        Click Handler, checks if the click is button node or simple node and manages accordingly
        """
        if self.selectGoalButton.pgObj.collidepoint(pos):
            self._selectGoalClick = True
            self._selectStartClick = False
            print("Select a Goal node")
            return None
        elif self.selectStartButton.pgObj.collidepoint(pos):
            self._selectGoalClick = False
            self._selectStartClick = True
            print("Select a Start node")
            return None
        elif self.startButton.pgObj.collidepoint(pos):
            if not self._running:
                self._running = True
                self._runTask()
            return None
        nodes = self.world.available_nodes
        if not nodes:
            raise ValueError("Nodes are not initialised")
        else:
            for row in nodes:
                for node in row:
                    if node.pgObj.collidepoint(pos):
                        return node
        self._selectGoalClick = False
        self._selectStartClick = False
        print("Run or Select Blocks")

    def _runTask(self):
        """
        Task to run when clicked on Run
        """
        bfs(self.startNode,self.goalNode,self.world.available_nodes,self)
    def selectNode(self,pos):
        node = self.getClickedNode(pos)
        if node is not None:
            if self._selectGoalClick:
                self._setGoalNode(node)
            elif self._selectStartClick:
                self._setStartNode(node)
            else:
                self._makeBlockNode(node)
                
    def _makeBlockNode(self,node:Node):
        if not node.isGoalNode and not node.isStartNode:
            node.add_color(BLOCK_COLOR)
            node.isBlock = True

    def _setGoalNode(self,node):
        self._selectGoalClick = False
        self.goalNode.setGoalNode(node.id)
    
    def _setStartNode(self,node):
        self._selectStartClick = False
        self.startNode.setStartNode(node.id)
    def eventHandler(self,event):
        if self._running:
            return #If algorithm is working jam the controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isClicked = True
            self.selectNode(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.isClicked = False
        elif event.type == pygame.MOUSEMOTION:
            if self.isClicked:
                self.selectNode(event.pos)
    def drawScenary(self):
        self.world.create_grids()
        self._drawButtons()
        if self.goalNode is not None:
            self.goalNode.draw_node()
        if self.startNode is not None:
            self.startNode.draw_node()
        pygame.display.update()
pygame.init()
pygame.display.set_caption(TITLE)
world = World(SCREEN_SIZE,background,(10,10))
world.create_grids()
gNode = GoalNode((5,5),GOAL_IMG,world)
running = True
sNode =StartNode((0,15),world,START_NODE_COLOR)
PG = PlayGround(world,gNode,sNode)
#sNode.moveTo((15,0),PG)
#sNode.moveTo((5,5),PG)
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