import pygame

class Label:
    """
    Label to add on pygame screens
    """
    def __init__(self,color:tuple,size:int,pos:tuple):
        """
        color:tuple
            color of the label in (r,g,b) format
        size:int
            size of the label
        pos:tuple
            (x,y) coordinates for the position of label
        """
        self._color = color
        self._size = size
        self._font = pygame.font.SysFont("Arial", self._size)
        self._pos = pos
        self._text = ""
    def draw_label(self,screen):
        """
        Draws the label on the pygame screen
        """
        text = self._font.render(self._text,True, self._color)
        text_rect = text.get_rect(center = self._pos)
        screen.blit(text, text_rect)
    def setValue(self,text):
        """
        Set the value for label
        """
        self._text = text
class Button:
    """
    Button elements for pygame screen

    Method
    ------
    draw_button(screen)
        draws button element on pygame screen
        screen: pygame screen
    
    isClicked(pos)
        Returns true if pos is a collidePos for the pygame rect element
    """
    def __init__(self,pos:tuple,size:tuple,bgColor:tuple,color:tuple,label:str="Button",labelSize:float=0.5,fill_value:int = 100):
        """
        pos:tuple
            (x,y) coordinates for the position of button
        size:tuple
            (width,height) of the button
        bgColor:tuple
            background color for the  button
        color:tuple
            color of the button label
        label:str
            label of the button
        labelSize:int
            size of the label
        fill_value:int
            fill value for pygame rect
        size:

        """
        self._pos = pos
        self.size = size
        self._color = color
        self._fontSize = int(size[1]*labelSize)
        self._label = label
        self._font = pygame.font.SysFont(None, self._fontSize)
        self._bgColor = bgColor
        self._fill_value = fill_value
        

    def draw_button(self,screen):
        """
        Draws the button on pygame screen
        """
        pos = self._pos+self.size
        self.pgObj = pygame.draw.rect(screen, self._bgColor, pygame.Rect(pos),self._fill_value, 3)
        labelLength = self._fontSize*len(self._label)
        text = self._font.render(self._label, True, self._color)
        text_rect = text.get_rect(center = self.pgObj.center)
        screen.blit(text, text_rect)
    def isClicked(self,pos)->bool:
        """
        Returns true if the click is made on button
        """
        if self.pgObj.collidepoint(pos):
            return True
        else:
            return False