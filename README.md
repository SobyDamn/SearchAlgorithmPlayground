# Search Algorithm Playground


Search Algorithm Playground is a python package to work with graph related algorithm, mainly dealing with different Artificial Intelligence Search alorithms.
The tool provides an user interface to work with the graphs and visualise the effect of algorithm on the graph while giving the freedom to programmer to make adjustments in the way they wants.
It also provides a way to save the graph in json format hence enabling the programmers to share the files and use different algorithm on same graph with ease.

> Currently supports only undirected graphs 

<br>

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0) [![Generic badge](https://img.shields.io/badge/python-3.6+-<COLOR>.svg)](https://www.python.org/downloads/)

<br>

## Table of Contents

- [Installation](#installation)
- [How to use?](#how-to-use)
- [Documentation](#documentation)

<br>


## Installation
```Some Installation steps```

## How to use?
```Basic example with screenshot```

## Documentation

### Classes

- [PlayGround](#playground)
- [World](#world)
- [Block](#block)
- [Node](#node)
- [Edge](#edge)

## PlayGround
---
PlayGround class represents the ground which which consists of the world of blocks on which the graph is displayed or modified. 
PlayGround class provide controls on the elements in the world like Edge and Nodes.

    Attribute
    ---------
    world: World
        World class object on which playground is available

    Parameter
    ---------
    world : World
        a World class object on which the nodes/edges are drawn
        The screen size of the world determines the screensize of the playground window (default None).

    saveToFile : str
        name of the file with which the world(or graph) will be saved(file will be saved in json format) when the 'Save Work' button is pressed (default None).

    weighted : bool
        whether the edges that will be drawn on playround is weighted or not (default False).

    startNode : Node
        a node object of Node class which will be set as start node for the graph.
        NOTE: startNode is a special node which cannot be deleted from the playground(default None)
        if no value is provided then top left block contains the start node 'S'

    goalNode : Node
        a node object of Node class which will be set as start node for the graph.
        NOTE: goalNode is a special node which cannot be deleted from the playground(default None)
        if no value is provided then bottom right block contains the goal node 'G'

    blocks_dimension : tuple
        blocks_dimension represents number of blocks that will be generated in the world if world object is given as None(default (23,21))
        e.g (23,21) represents 23 rows and 21 columns

    block_size : int
        size of each block i.e. one side of the squared block (default 30)
        
    Methods
    -------
    fromfilename(filename:str)
        a classmethod which returns PlayGround class object initialised from values given in filename and returns the object
        filename: a json file name to which previously a playround is saved into

    onStart(func)
        Sets function to be executed when the start button is clicked
        func: function which will be executed when start is pressed
    
    delay(millisecond:int)
        Delays the program for given milliseconds
        Uses pygame.time.delay method
        Once the controls are taken away no other control would work on playground except exit
        NOTE: Using this delay function would allow to reflect changes on playground in delay mode better than instantaneous

    MoveGen(node:Node)
        Returns all the neighbours(in sorted order according to the label) of a node i.e. all the nodes which has edge between the given node
        node: A Node class object

    get_edge(nodeStart:Node,nodeEnd:Node)->Edge
        Returns an Edge class object between the node nodeStart and nodeEnd, if no edge exists returns None
        nodeStart: A Node class object
        nodeEnd: A Node class object

    getGoalNode()->Node
        Returns Node class object which is currenty set as a goal node for the playground

    getSartNode()->Node
        Returns Node class object which is currenty set as a start node for the playground

    setGoalNode(node:Node)
        Sets the given node as goal node for the PlayGround
        node: A Node class object

    setStartNode(node:Node)
        Sets the given node as goal node for the PlayGround
        node: A Node class object
    
    getScreen()
        Returns a pygame window object which is the surface on which the elements are being drawn
        Useful in case more extra elements are needed to be drawn on the playground
    
    add_node(node: Node)
        Adds node to the world
        NOTE: node available in the world will be displayed on the playground screen

    add_edge(edge: Edge)
        Adds edge to the world
        NOTE: edge available in the world will be displayed on the playground screen
    
    remove_edge(edge:Edge)
        Removes edge from the world
    
    remove_node(node:Node)
        Removed node from the world
        
    saveWork(filename:str=None)
        Saves the playground with the given filename
        if no filename is provided, then playground will be saved with arbitrary filename

    showInfoText(text:str)
        To display informational texts on the playground right above the start button
        text: text to be displayed on the playground infoText area

    to_dict()->dict
        Returns Playrgound attributes as dictionary

    setTitle(title:str)
        Sets the title of the playground window
    
    run()
        runs the playground as an active window on which the frames are drawn

## World

---
A World class represents the world for the playground which is responsible for Maintaining Node,Edge and Block of the playground

    Parameters
    ----------
    blocks_dimension : tuple
        blocks_dimension represents number of blocks that will be generated in the world
        e.g (23,21) represents 23 rows and 21 columns

    block_size : int
        size of each block i.e. one side of the squared block
    
    bottom_panel_size:int
        height of the bottom panel on which buttons and other UI element will be drawn
        min allowed 180

    grid_width:int
        Width of the grids

    background_color:tuple
        A rgb value type of the form (r,g,b) to set color for the background of the world default (255,255,255)
        
    gird_color:tuple
        A rgb value type of the form (r,g,b) to set color for the blocks border of the world default (232, 232, 232)

    margin:int
        Margin from the edges of the playground window, minimum value allowed is 10, default 10

    Methods
    -------
    fromdict(datadict:dict)
        A classmethod to create World class object from a dictionary
        NOTE:The dictionary must be of the same form returned by to_dict() method of the class

    create_grids()
        Generates grids if not generated in the world, if the gird is already availbale then it redraws them

    add_node(node:Node)
        Adds nodes to the world
        NOTE: To make the node visible on playground window it must be include in the world

    remove_node(node:Node)
        Removes nodes from the world
        NOTE: If nodes are not available in the world it will no longer visible on playground window

    update_node_loc(node:Node,newBlock:Block)
        Updates the location of the node to newBlock location and removes it from previous block
        node:Node - A Node class object which needs to be updated
        newBlock:Block - A Block class object to which the node is require to move to

    getEdges()->dict
        Returns all the available edges in the world as dictionary with key as the node pairs ids
        e.g ((1,1),(1,5)) is the key for an edge between the node with id (1,1) and (1,5)
        NOTE: The id represents position in the 2D matrix of the block

    add_edge(e:Edge)
        Adds edge to the world, edge added to the world will be visible on Playground window
        NOTE: Edges are added with the key of the end node ids e.g. ((1,1),(1,5)) is the key for an edge between the node with id (1,1) and (1,5)

    remove_edge(e:Edge)
        Removes the edge from the world. The edge removed from the world will no longer be visible on the Playground window

    getEdge(startNodeID:tuple,endNodeID:tuple)->Edge
        Returns edge between startNodeID and endNodeID if there exists an edge else returns None
        startNodeID:tuple - id of the node which has edge with the other node we're looking for
        endNodeID:tuple - id of the node which has edge with the other node we're looking for
    
    getNodes()->dict
        Returns the dictionary of all the nodes available in the world
        Key of is the id of the node
    
    getNode(key:tuple)->Node
        Returns node with given key, returns None if the node doesn't exists
        key:tuple - id of the node we are looking for,  location in the grid or 2D array.

    getBlock(id)->Block
        Returns block at the given id.
        id:tuple - Index Location in 2D matrix

    to_dict()->dict
        returns the object details with all attribute and values as dictionary


## Block
---
Block defines the world tiles. Blocks represents the world in 2-Dimensional array format.


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

## Node
---
A node is a type of block that is important to the world 
Node class inherits the Block class.

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


## Edge
---

An edge class represents an edge between 2 nodes

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