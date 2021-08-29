from Node import *
from SearchAlgoUtlis import *
from config import *
def bfs(sNode:StartNode,gNode:GoalNode,AllNode:list,PG):
    ALGORITHM_TITLE = "Breadth First Search"
    print("Running",ALGORITHM_TITLE)
    pygame.display.set_caption(TITLE+" "+ALGORITHM_TITLE)
    S = sNode.getNode()
    G = gNode.getNode()
    OPEN = [(S,None)] #Starting with S and it's parent as None
    CLOSED = [] #Empty

    #Till we have node to suspect keep looking
    while OPEN:
        nodePair = OPEN[0]
        (N,_) = nodePair
        if gNode.testNode(N):
            path = ReconstructPath(nodePair,CLOSED)
            #Show node movement
            moveToGoal(sNode,path,PG)
            return path
        else:
            CLOSED = [nodePair] + CLOSED
            neighbours = MoveGen(N,AllNode)
            newNodes = RemoveSeen(neighbours,OPEN,CLOSED)
            highlighNodes(newNodes,PG)
            newPairs = MakePairs(newNodes,N)
            OPEN = OPEN[1:] + newPairs
    return []


def highlighNodes(nodesList:list,PG):
    """
    Highlighting the nodes
    """
    for node in nodesList:
        pygame.time.delay(10)
        PG.drawScenary()
        node.highlight(True)

def moveToGoal(S:StartNode,path:list,PG):
    for node in path[::-1]:
        S.moveTo(node.id,PG,5)