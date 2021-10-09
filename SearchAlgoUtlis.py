from SearchAlgoPlayground import Node
def MoveGen(N:Node,AvailableNodes:list)->list:
    """
    Returns list of possible move from a given node
    """
    possibleMove = []
    n = len(AvailableNodes)
    if n==0:
        return []
    m = len(AvailableNodes[0])
    x,y = N.id
    movements = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)] #possible direction to move
    for move_x,move_y in movements:
        if (x+move_x >=0 and x+move_x<n) and (y+move_y>=0 and y+move_y<m):
            node = AvailableNodes[x+move_x][y+move_y]
            if not node.isBlock:
                possibleMove.append(node)
    return possibleMove

def MakePairs(nodeList:list,parent:Node)->list:
    """
    Function creates a list of tuples where each tuples contains (n,p) where n is node and p is parent given as parameter
    """
    if not nodeList:
        return []
    else:
        return [(nodeList[0],parent)]+MakePairs(nodeList[1:],parent)
def RemoveSeen(nodeList:list,OPEN:list,CLOSED:list)->list:
    """
    Removes node from nodeList if it occured in any of the OPEN or CLOSED list of nodePairs
    """
    if not nodeList:
        return []
    else:
        node = nodeList[0] #Take head
        if OccursIn(node,OPEN) or OccursIn(node,CLOSED):
            return RemoveSeen(nodeList[1:],OPEN,CLOSED) #Check with the rest of the nodeList
        else:
            return [node]+RemoveSeen(nodeList[1:],OPEN,CLOSED) #Make a list and further check with the rest of the nodeList

def OccursIn(node:Node,nodePairs:list)->bool:
    """
    Returns true if the node is in the given nodePairs list else false
    each nodePair is (n,p) i.e. n is the node and p is the parent
    """
    if len(nodePairs)==0:
        return False
    #Check if the head of the list contains a node equals to the node we're looking
    elif node == nodePairs[0][0]:
        return True
    else:
        return OccursIn(node,nodePairs[1:]) #Shrink the list and call the function

def ReconstructPath(nodePair:tuple,CLOSED:list):
    def SkipTo(parent,nodePairs):
        if parent == nodePairs[0][0]:
            return nodePairs
        else:
            return SkipTo(parent,nodePairs[1:])
    
    (node,parent) = nodePair
    path = [node]
    while parent is not None:
        path = path + [parent]
        CLOSED = SkipTo(parent,CLOSED)
        (_,parent) = CLOSED[0]
    return path
