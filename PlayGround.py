import pygame 
from World import World
from Node import *
from config import *
class PlayGround:
    def __init__(self,world:World,goalNode:GoalNode = None,startNode:StartNode = None):
        self.world = world
        self.isClicked = False
        self.goalNode = goalNode
        self.startNode = startNode
    def getNode(self,pos)->Node:
        nodes = self.world.available_nodes
        if not nodes:
            raise ValueError("Nodes are not initialised")
        else:
            for row in nodes:
                for node in row:
                    if node.pgObj.collidepoint(pos):
                        return node

    def selectNode(self,pos):
        node = self.getNode(pos)
        if node is not None:
            node.add_color(GRID_COLOR)
            sNode.moveTo(node.id,self,5)
                
    def _makeBlockNode(self,node:Node):
        if not node.isGoalNode and not node.isStartNode:
            node.add_color(BLOCK_COLOR)
            node.isBlock = True
            return True
        else:
            return False
    def eventHandler(self,event):
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
sNode =StartNode((0,15),world,BLUE)
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