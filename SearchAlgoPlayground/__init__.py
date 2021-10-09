import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from .Blocks import Block
from .Edge import Edge
from .Node import Node
from .PlayGround import PlayGround
from .World import World
from .config import config
from .UI import *