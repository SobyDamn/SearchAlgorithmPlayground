# Search Algorithm Playground


Search Algorithm Playground is a python package to work with graph related algorithm, mainly dealing with different Artificial Intelligence Search alorithms.
The tool provides an user interface to work with the graphs and visualise the effect of algorithm on the graph while giving the freedom to programmer to make adjustments in the way they wants.
It also provides a way to save the graph in json format hence enabling the programmers to share the files and use different algorithm on same graph with ease.


> Currently supports only undirected graphs 

<br>

![AStarAlgoResult](/static/AStar_Sample_output.png)

<br>

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


<br>

## Table of Contents

- [Installation](#installation)
- [Controls](#controls)
- [Basic Use](#basic-use)
- [Documentation](#documentation)

<br>


# Installation

## Install from pip

```
pip install SearchAgoPlayground
```
## Manually install it

Copy the [repository](https://github.com/SobyDamn/SearchAlgorithmPlayground) in your system then do

```
python setup.py install
```

You can also copy/paste the SearchAlgoPlayground folder into your project

<br>

# Controls

## **Creating a node**
Double click on any empty block will create a node on it.

> NOTE: Single click highlights the selected block and info label area will display it's location in 2D Matrix.
<br>

![NodeCreate](/static/node_creator.gif)

<br>

## **Creating an edge between two nodes**
Clicking on a node single time selects the node for creating an edge with that.
<br>
Select one node, once selected select another node to create an edge between them.

![EdgeCreate](/static/edge_creator.gif)

<br>

## **Modify element mode**

Double click on any element makes it go in modify mode which allows the element to be deleted or edited.

To delete an edge double click on it and then press _DELETE_

![EdgeDelete](/static/edge_delete.gif)


To edit an edge weight double click and use keyboard to modify it's value, once done hit _ENTER_ or click anywhere else.

![EdgeWeightEdit](/static/edge_weight_edit.gif)


To delete a node double click on it and then hit _DELETE_ on keyboard

![DeleteNodeWithEdge](/static/delete_node_with_edge.gif)


To edit node label double click on a node and use keyboard to modify the label, once done hit _ENTER_ or click anywhere else.

> NOTE: Label of a node must be unique

![EditNodeLabel](/static/edit_node_label.gif)

<br>

## **Move nodes in the playground**

![NodeDrag](/static/node_drag.gif)


<br>

# Basic Use:

## simple PlayGround:
Creates PlayGround object with default values

```python
from SearchAlgoPlayground import PlayGround

pg = PlayGround() #Creating a playground object
pg.run() #run the playground
```

## Loading graph from file:

Method Used: [fromfilename()](#PlayGround.method.fromfilename)

> NOTE: The graph file here in below example _Graph.json_ must have been saved by the playground, i.e. saved by clicking **_Save Work_** button.

```python
from SearchAlgoPlayground import PlayGround

pg = PlayGround.fromfilename("Graph.json") #loading a playground from a file
pg.run() #run the playground
```

## Set filename to save your work into:

Parameter used: [saveToFile](#PlayGround.parameter.saveToFile)

```python
from SearchAlgoPlayground import PlayGround

pg = PlayGround(saveToFile = "MyWork.json") #Creating a playground object with name of the file provided where the work will be saved
pg.run() #run the playground
```

## PlayGround with weighted edge:

Parameter used: [weighted](#PlayGround.parameter.weighted)

```python
from SearchAlgoPlayground import PlayGround

pg = PlayGround(weighted=True) #Weighted playground
pg.run() #run the playground
```


## Setting up dimension for the world in playground:

Parameter used: [saveToFile](#PlayGround.parameter.saveToFile), [weighted](#PlayGround.parameter.weighted), [block_dimensions](#PlayGround.parameter.blocks_dimension)

```python
from SearchAlgoPlayground import PlayGround

#A weighted playground with a name of the file where work need to be saved given as MyWork.json
#block_dimension is dimension of 2D matrix (rows,cols) here both are 20
pg = PlayGround(saveToFile = "MyWork.json",weighted=True,blocks_dimension=(20,20))
pg.run() #run the playground
```

## Setting onStart event:
Method set as onStart will be executed once the Start button is clicked shown on playground.

Parameter used: [saveToFile](#PlayGround.parameter.saveToFile), [weighted](#PlayGround.parameter.weighted), [block_dimensions](#PlayGround.parameter.blocks_dimension)

Method used: [onStart()](#PlayGround.method.onStart)

```python
from SearchAlgoPlayground import PlayGround

#A weighted playground with a name of the file where work need to be saved given as MyWork.json
#block_dimension is dimension of 2D matrix (rows,cols) here both are 20
pg = PlayGround(saveToFile = "MyWork.json",weighted=True,blocks_dimension=(20,20))

##Sample function to be put as start for playground
def sayHello():
    print("Hello From Playground!")


pg.onStart(sayHello) #Setting method for on start click
pg.run() #run the playground
```

## Changing configuration for playground:
Changing values in configuration can modify the default values for PlayGround and world related to it.

```python
from SearchAlgoPlayground import PlayGround
from SearchAlgoPlayground import config
from SearchAlgoPlayground.config import YELLOW,PURPLE

config["BACKGROUND_COLOR"] = YELLOW #set background color as yellow
config["NODE_COLOR"] = PURPLE #set node color as purple

#A weighted playground with a name of the file where work need to be saved given as MyWork.json
#block_dimension is dimension of 2D matrix (rows,cols) here both are 20
pg = PlayGround(saveToFile = "MyWork.json",weighted=True,blocks_dimension=(20,20))

pg.run() #run the playground
```

Below are the given default values, or look into the file [config.py](https://github.com/SobyDamn/SearchAlgorithmPlayground/blob/master/SearchAlgoPlayground/config.py)

```python
config = {
    "TITLE":"Algo PlayGround",               #Title of the playground window
    "BLOCKS_DIMENSION":(21,23),              #ROWS,COLUMNS
    "BLOCK_SIZE":30,                         #Size of each block i.e. sides
    "BOTTOM_PANEL_HEIGHT":200,               #Size of bottom panel for control
    "MARGIN":15,                             #Margin between sides and the grid 
    "GRID_WIDTH":1,                          #Width of the boundary of the block
    "BACKGROUND_COLOR":WHITE,                #Color of the background of the world
    "GRID_COLOR":GRAY,                       #Block boundary color
    "HIGHLIGHT_COLOR":DARK_GRAY,             #Highlighting color
    "BUTTON_COLOR_PRIMARY":BROWN,            #Color for the button larger
    "BUTTON_COLOR_SECONDARY": PURPLE,        #color for the smaller button
    "INFO_LABEL_COLOR":DARK_GRAY,            #color for the info text
    "NODE_COLOR":GRAY,                       #color of the node
    "NODE_BORDER_COLOR":BLACK,               #color of the border of node
    "SPECIAL_NODE_BORDER_COLOR": DARK_PURPLE,#Special node border color
    "SPECIAL_NODE_COLOR":GREEN,              #special node color
    "SELECTED_NODE_COLOR" : RED,             #color of the node selected
    "ELEMENT_ACTIVE_COLOR":BLUE,             #Element selected by user is considered as active to the playground
    "MY_WORK_DIR": "MyGraph/"                #Directory in which the work is saved
}
```
<br>

> ## Check more implemented examples [here](#Link).

<br>

# Documentation

## Classes

- [PlayGround](#playground)
- [World](#world)
- [Block](#block)
- [Node](#node)
- [Edge](#edge)
- [Examples](#)

<br>

## PlayGround

PlayGround class represents the ground which which consists of the world of blocks on which the graph is displayed or modified. 
PlayGround class provide controls on the elements in the world like Edge and Nodes.


### Parameters
[world](#PlayGround.parameter.world), [saveToFile](#PlayGround.parameter.saveToFile), [weighted](#PlayGround.parameter.weighted), [startNode](#PlayGround.parameter.startNode), [goalNode](#PlayGround.parameter.goalNode), [block_dimensions](#PlayGround.parameter.blocks_dimension), [block_size](#PlayGround.parameter.block_size)
<br>

_**<h4 id="PlayGround.parameter.world">world : World</h4>**_
A World class object on which the nodes/edges are drawn
The screen size of the world determines the screensize of the playground window (default None).

_**<h4 id="PlayGround.parameter.saveToFile">saveToFile : str</h4>**_
name of the file with which the world(or graph) will be saved(file will be saved in json format) when the 'Save Work' button is pressed (default None).

_**<h4 id="PlayGround.parameter.weighted">weighted : bool</h4>**_
whether the edges that will be drawn on playround is weighted or not (default False).

_**<h4 id="PlayGround.parameter.startNode">startNode : Node</h4>**_
a node object of Node class which will be set as start node for the graph.
if no value is provided then top left block contains the start node 'S'
<br>
```NOTE: startNode is a special node which cannot be deleted from the playground(default None)```

_**<h4 id="PlayGround.parameter.goalNode">goalNode : Node</h4>**_
a node object of Node class which will be set as start node for the graph.
if no value is provided then bottom right block contains the goal node 'G'<br>
```NOTE: goalNode is a special node which cannot be deleted from the playground(default None)```

_**<h4 id="PlayGround.parameter.blocks_dimension">blocks_dimension : tuple</h4>**_
blocks_dimension represents number of blocks that will be generated in the world if world object is given as None(default (23,21))
<br>
e.g (23,21) represents 23 rows and 21 columns

**_<h4 id="PlayGround.parameter.block_size">block_size : int</h4>_**
size of each block i.e. one side of the squared block (default 30)

### Attribute
[world](#PlayGround.attribute.world)

_**<h4 id="PlayGround.attribute.world">world: World</h4>**_
World class object on which playground is available
        
### Methods
[fromfilename()](#PlayGround.method.fromfilename), [addUIElement()](#PlayGround.method.addUIElement), [removeUIElement()](#PlayGround.method.removeUIElement), [onStart()](#PlayGround.method.onStart), [delay()](#PlayGround.method.delay),[getAllNodes()](#PlayGround.method.getAllNodes),[getAllEges()](#PlayGround.method.getAllEges), [MoveGen()](#PlayGround.method.MoveGen), [get_edge()](#PlayGround.method.get_edge), [getGoalNode()](#PlayGround.method.getGoalNode), [getStartNode()](#PlayGround.method.getStartNode), [setGoalNode()](#PlayGround.method.setGoalNode), [setStartNode()](#PlayGround.method.setStartNode), [getScreen()](#PlayGround.method.getScreen), [add_node()](#PlayGround.method.MoveGen), [add_edge()](#PlayGround.method.add_edge), [remove_edge()](#PlayGround.method.remove_edge), [remove_node()](#PlayGround.method.remove_node), [saveWork()](#PlayGround.method.saveWork), [showInfoText()](#PlayGround.method.showInfoText),[get_dimension()](#PlayGround.method.get_dimension), [to_dict()](#PlayGround.method.to_dict)
<br>

_**<h4 id="PlayGround.method.fromfilename">fromfilename(filename:str)</h4>**_
a classmethod which returns PlayGround class object initialised from values given in filename and returns the object
<br>
_filename_: a json file name to which previously a playround is saved into

_**<h4 id="PlayGround.method.addUIElement">addUIElement(element)</h4>**_
Adds UI element to the playground
<br>
```NOTE: any UI element must contain draw() method which takes pygame screen as a parameter, the method will be called each time frame is drawn```

_**<h4 id="PlayGround.method.removeUIElement">removeUIElement(element)</h4>**_
Removes UI element from the playground

_**<h4 id="PlayGround.method.onStart">onStart(func)</h4>**_
Sets function to be executed when the start button is clicked
<br>
_func_: function which will be executed when start is pressed

_**<h4 id="PlayGround.method.delay">delay(millisecond:int)</h4>**_
Delays the program for given milliseconds
<br>
Uses pygame.time.delay method
<br>
Once the controls are taken away no other control would work on playground except exit
<br>
```NOTE: Using this delay function would allow to reflect changes on playground in delay mode better than instantaneous```

_**<h4 id="PlayGround.method.MoveGen">MoveGen(node:Node)</h4>**_
Returns all the neighbours(in sorted order according to the label) of a node i.e. all the nodes which has edge between the given node
<br>
_node_: A Node class object

_**<h4 id="PlayGround.method.get_edge">get_edge(nodeStart:Node,nodeEnd:Node)->Edge</h4>**_
Returns an Edge class object between the node nodeStart and nodeEnd, if no edge exists returns None
_nodeStart_: A Node class object
<br>
_nodeEnd_: A Node class object

_**<h4 id="PlayGround.method.getAllNodes">getAllNodes()->list</h4>**_
Returns all nodes available in the world as a list

_**<h4 id="PlayGround.method.getAllEdges">getAllEdges()->list</h4>**_
Returns list of all edges available in world

_**<h4 id="PlayGround.method.getGoalNode">getGoalNode()->Node</h4>**_
Returns Node class object which is currenty set as a goal node for the playground

_**<h4 id="PlayGround.method.getSartNode">getSartNode()->Node</h4>**_
Returns Node class object which is currenty set as a start node for the playground

_**<h4 id="PlayGround.method.setGoalNode">setGoalNode(node:Node)</h4>**_
Sets the given node as goal node for the PlayGround
_node_: A Node class object

_**<h4 id="PlayGround.method.setStartNode">setStartNode(node:Node)</h4>**_
Sets the given node as goal node for the PlayGround
<br>
_node_: A Node class object

_**<h4 id="PlayGround.method.getScreen">getScreen()</h4>**_
Returns a pygame window object which is the surface on which the elements are being drawn
<br>
Useful in case more extra elements are needed to be drawn on the playground

_**<h4 id="PlayGround.method.add_node">add_node(node: Node)</h4>**_
Adds node to the world
<br>
```NOTE: node available in the world will be displayed on the playground screen```

_**<h4 id="PlayGround.method.add_edge">add_edge(edge: Edge)</h4>**_
Adds edge to the world
<br>
```NOTE: edge available in the world will be displayed on the playground screen```

_**<h4 id="PlayGround.method.remove_edge">remove_edge(edge:Edge)</h4>**_
Removes edge from the world

_**<h4 id="PlayGround.method.remove_node">remove_node(node:Node)</h4>**_
Removed node from the world

_**<h4 id="PlayGround.method.saveWork">saveWork(filename:str=None)</h4>**_
Saves the playground with the given filename.
if no filename is provided, then playground will be saved with arbitrary filename

_**<h4 id="PlayGround.method.showInfoText">showInfoText(text:str)</h4>**_
To display informational texts on the playground right above the start button
<br>
_text_: text to be displayed on the playground infoText area

_**<h4 id="PlayGround.method.to_dict">to_dict()->dict</h4>**_
Returns Playrgound attributes as dictionary

_**<h4 id="PlayGround.method.setTitle">setTitle(title:str)</h4>**_
Sets the title of the playground window
<br>
_title_: a string value

_**<h4 id="PlayGround.method.run">run()</h4>**_
runs the playground as an active window on which the frames are drawn

---

## World

A World class represents the world for the playground which is responsible for Maintaining Node,Edge and Block of the playground

### Parameters
#### _**blocks_dimension : tuple**_
blocks_dimension represents number of blocks that will be generated in the world
e.g (23,21) represents 23 rows and 21 columns

#### _**block_size : int**_
size of each block i.e. one side of the squared block

#### _**bottom_panel_size:int**_
height of the bottom panel on which buttons and other UI element will be drawn
min allowed 180

#### _**grid_width:int**_
Width of the grids

#### _**background_color:tuple**_
A rgb value type of the form (r,g,b) to set color for the background of the world default (255,255,255)

#### _**gird_color:tuple**_
A rgb value type of the form (r,g,b) to set color for the blocks border of the world default (232, 232, 232)

#### _**margin:int**_
Margin from the edges of the playground window, minimum value allowed is 10, default 10

### Methods
[fromdict()](#fromdictdatadictdict), [create_grids()](#create_grids), [add_node()](#add_nodenode-node), [remove_node()](#remove_nodenodenode), [update_node_loc()](#update_node_locnodenodenewblockblock), [getEdges()](#getedges-dict), [add_edge()](#add_edgeedge-edge), [remove_edge()](#remove_edgeedgeedge), [getNodes()](#getnodes-dict), [getNode()](#getnodekeytuple-node), [getBlock()](#getblockid-block), [get_dimension()](#get_dimension-tuple), [to_dict()](#to_dict-dict)

#### _**fromdict(datadict:dict)**_
A classmethod to create World class object from a dictionary
<br>
```NOTE:The dictionary must be of the same form returned by to_dict() method of the class```

#### _**create_grids()**_
Generates grids if not generated in the world, if the gird is already availbale then it redraws them

#### _**add_node(node:Node)**_
Adds nodes to the world
<br>
```NOTE: To make the node visible on playground window it must be include in the world```

#### _**remove_node(node:Node)**_
Removes nodes from the world
<br>
```NOTE: If nodes are not available in the world it will no longer visible on playground window```

#### _**update_node_loc(node:Node,newBlock:Block)**_
Updates the location of the node to newBlock location and removes it from previous block.
_node:Node_ - A Node class object which needs to be updated
newBlock:Block - A Block class object to which the node is require to move to

#### _**getEdges()->dict**_
Returns all the available edges in the world as dictionary with key as the node pairs ids
e.g ((1,1),(1,5)) is the key for an edge between the node with id (1,1) and (1,5)
<br>
```NOTE: The id represents position in the 2D matrix of the block```

#### _**add_edge(e:Edge)**_
Adds edge to the world, edge added to the world will be visible on Playground window
<br>
```NOTE: Edges are added with the key of the end node ids e.g. ((1,1),(1,5)) is the key for an edge between the node with id (1,1) and (1,5)```

#### _**remove_edge(e:Edge)**_
Removes the edge from the world. The edge removed from the world will no longer be visible on the Playground window

#### _**getEdge(startNodeID:tuple,endNodeID:tuple)->Edge**_
Returns edge between startNodeID and endNodeID if there exists an edge else returns None
_startNodeID:tuple_ - id of the node which has edge with the other node we're looking for
_endNodeID:tuple_ - id of the node which has edge with the other node we're looking for

#### _**getNodes()->dict**_
Returns the dictionary of all the nodes available in the world
Key of is the id of the node

#### _**getNode(key:tuple)->Node**_
Returns node with given key, returns None if the node doesn't exists
_key:tuple _- id of the node we are looking for,  location in the grid or 2D array.

#### _**getBlock(id)->Block**_
Returns block at the given id.
id:tuple - Index Location in 2D matrix

#### _**get_dimension()->tuple**_
Returns dimension of the world as tuple of (rows,col)

#### _**to_dict()->dict**_
returns the object details with all attribute and values as dictionary

---

## Block

Block defines the world tiles. Blocks represents the world in 2-Dimensional array format.


### Attribute
#### _**x:int**_
x coordinate in the window plane of the block

#### _**y:int**_
y coordinate in the window plane of the block

#### _**size:int**_
size of the block, denotes one side of the square block

#### _**id:tuple**_
id represents position in the 2D matrix of the block
(x,y) where x is the row and y is the column

#### _**pgObj**_
pygame rect object


### Parameters

#### _**x:int**_
x coordinate in the window plane of the block

#### _**y:int**_
y coordinate in the window plane of the block

#### _**size:int**_
size of the block, denotes one side of the square block

#### _**id:tuple**_
id represents position in the 2D matrix of the block
(x,y) where x is the row and y is the column

#### _**gird_color:tuple**_
rgb color (r,g,b) value for the block boundary default ((163, 175, 204))

grid_width:int
width of the boundary default 1

### Methods

#### _**draw_block(screen)**_
draws the block on pygame window
screen: pygame window

#### _**highlight(val:bool)**_
highlights block with highlist color
val:bool - true to enable highlight

#### _**pos() -> tuple**_
returns the coordinate of the centre of the block on the pygame window

#### _**setHasNode(val:bool)**_
sets the value for the flag _hasNode to represent that a block contains a node

#### _**hasNode()->bool**_
returns true if block has node over it

#### _**to_dict()->dict**_
returns the object details with all attribute and values as dictionary

---
## Node

A node is a type of block that is important to the world 
Node class inherits the Block class.

### Parameters

#### _**block:Block**_
A Block class object on which the node will be drawn

#### _**label:str**_
Label of the node

#### _**colorOutline:tuple**_
A rgb value of the form (r,g,b) represents outline color of the node

#### _**colorNode:tuple**_
A rgb value of the form (r,g,b) represents color of the node

#### _**outlineWidth:int**_
Width of the outline of the node default 2

#### _**specialNodeStatus:bool**_
sets whether the node is special default is False
<br>
```NOTE: A special node must be present on playground all time, i.e. delete is not allowed```

### Attributes
#### _**x:int**_
x coordinate in the window plane of the block

#### _**y:int**_
y coordinate in the window plane of the block

#### _**size:int**_
size of the block, denotes one side of the square block

#### _**id:tuple**_
id represents position in the 2D matrix of the block
(x,y) where x is the row and y is the column

#### _**pgObj**_
pygame rect object

#### _**pos:tuple**_
coordinate in pygame window for center of the node

### Methods
[draw_block()](#draw_blockscreen), [highlight()](#highlightvalbool), [pos()](#pos---tuple), [setHasNode()](#sethasnodevalbool), [hasNode()](#hasnode-bool), [to_dict()](#to_dict-dict), [set_label()](#set_labellabelstrscreen), [selected()](#selectedvalbool), [set_color()](#set_colorcolortuple), [get_label()](#get_label-str), [setLocation()](#setlocationblockblock), [handle_event()](#handle_eventworldworldeventinfolabel), [add_neighbour()](#add_neighbournodenode), [remove_neighbour()](#remove_neighbournodenode), [get_neighbours()](#get_neighbour-list)

#### _**draw_block(screen)**_
draws the node on pygame window
screen: pygame window

#### _**highlight(val:bool)**_
highlights block with highlist color
val:bool - true to enable highlight

#### _**pos() -> tuple**_
returns the coordinate of the centre of the block on the pygame window

#### _**setHasNode(val:bool)**_
sets the value for the flag _hasNode to represent that a block contains a node

#### _**hasNode()->bool**_
returns true if block has node over it

#### _**to_dict()->dict**_
returns the object details with all attribute and values as dictionary

#### _**set_label(label:str,screen)**_
sets the label on the node
_screen_ - a pygame window
<br>
_label:str_ - a string value that'll be displayed on node

#### _**selected(val:bool)**_
sets isSelected flag value


#### _**set_color(color:tuple)**_
sets the color of the node
<br>
_color:tuple_ - A rgb value in the form (r,g,b)

#### _**get_label()->str**_
returns value of label of the node

#### _**setLocation(block:Block)**_
sets the location to the new block
block:Block - A Block class object
<br>
```NOTE: Location for nodes are defined by the block they resides on```

#### _**handle_event(world:World,event,infoLabel)**_
Internal method to handle the pygame events

#### _**add_neighbour(node:Node)**_
Adds the given node as neighbouring node if it's not already a neighbouring node, should be used when it has an edge with the given node
<br>
_node:Node_ - A Node class object

#### _**remove_neighbour(node:Node)**_
Removes the given node from neighbouring node if it's in neighbouring node
_node:Node_ - A Node class object

#### _**get_neighbour()->list**_
Returns list of neighbouring nodes(Node class objects) which is sorted in order with their label

---

## Edge


An edge class represents an edge between 2 nodes

### Parameters

#### _**nodeStart:Node**_
A Node class object which represents the starting node of the edge

#### _**nodeEnd:Node**_
A Node class object which represents the ending node of the edge

#### _**isWeighted:bool**_
Whether the edge drawn between the node has weight or not, default False

#### _**weight:int**_
Wieght of the edge, default 0

#### _**edgeColor:tuple**_
A rgb value of the form (r,g,b) which represents the color of the edge, default value _NODE_BORDER_COLOR_
<br>
_edgeWidth:int_
Width of the edge, default 3

### Attribute
#### _**pgObj**_
A pygame rect object

### Methods
[handle_event()](#handle_eventworldworldeventinfolabel), [set_color()](#set_colorcolortuple), [collidePoint()](#collidepointclickpointoffeset5), [draw_edge()](#draw_edgescreen), [getNodes()](#getnodekeytuple-node), [get_weight()](#get_weight-int), [to_dict()](#to_dict-dict)

#### _**handle_event(world:World,event,infoLabel)**_
Internal method to handle the pygame events

#### _**set_color(color:tuple)**_
Sets color of the edge
color:tuple - A rgb value of the form (r,g,b)

#### _**collidePoint(clickPoint,offeset=5)**_
Returns true if the given click point is inside the offset value on edge

#### _**draw_edge(screen)**_
Draws edge on the screen
screen - A pygame window

#### _**getNodes()->tuple**_
Returns the pair of node which the edge is connecting

#### _**get_weight()->int**_
Returns the weight of the edge

#### _**to_dict()->dict**_
Returns the object details its attributes and value as dictionary

---