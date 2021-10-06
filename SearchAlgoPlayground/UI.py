import pygame

class Label:
    def __init__(self,color,size,pos):
        self._color = color
        self._size = size
        self._font = pygame.font.SysFont("Arial", self._size)
        self._pos = pos
        self._text = ""
    def draw_label(self,screen):
        text = self._font.render(self._text,True, self._color)
        text_rect = text.get_rect(center = self._pos)
        screen.blit(text, text_rect)
    def setValue(self,text):
        """
        Set the value for label
        """
        self._text = text
class Button:
    def __init__(self,pos,size,bgColor,color,label="Button",labelSize:float=0.5,fill_value = 100):
        self._pos = pos
        self.size = size
        self._color = color
        self._fontSize = int(size[1]*labelSize)
        self._label = label
        self._font = pygame.font.SysFont(None, self._fontSize)
        self._bgColor = bgColor
        self._fill_value = fill_value
        

    def draw_button(self,screen):
        pos = self._pos+self.size
        self.pgObj = pygame.draw.rect(screen, self._bgColor, pygame.Rect(pos),self._fill_value, 3)
        labelLength = self._fontSize*len(self._label)
        text = self._font.render(self._label, True, self._color)
        text_rect = text.get_rect(center = self.pgObj.center)
        screen.blit(text, text_rect)
    def isClicked(self,collidePos):
        if self.pgObj.collidepoint(collidePos):
            return True
        else:
            return False