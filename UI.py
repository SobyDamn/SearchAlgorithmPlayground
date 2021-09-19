import pygame as pg
from config import BLACK

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
LABEL_COLOR = BLACK


class InputBox:

    def __init__(self, x, y, w, h,label = "LABEL", text=''):
        self.rect = pg.Rect(x, y, w, h)

        self.color = COLOR_INACTIVE
        self._text = text
        self._FONT = pg.font.Font(None, int(h*0.90))
        self.txt_surface = self._FONT.render(text, True, self.color)
        self.active = False
        self._label = label #Label above a input box

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            print(event.type)
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self._text)
                    self._text = ''
                elif event.key == pg.K_BACKSPACE:
                    self._text = self._text[:-1]
                else:
                    self._text += event.unicode
                # Re-render the text.
                self.txt_surface = self._FONT.render(self._text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def getText(self):
        return self.text
    def isSelected(self,pos):
        """
        Method returns true if pos is collided with the current label
        """
        if self.rect.collidepoint(pos):
            return True
        else:
            return False
    def draw(self, screen):
        #Blit the label
        text = self._FONT.render(self._label, True, LABEL_COLOR)
        x,y = self.rect.center
        y = y-int(self.rect.h)
        text_rect = text.get_rect(center = (x,y))
        screen.blit(text, text_rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self,world,pos,size,bgColor,color,label="Button",labelSize:float=0.5):
        self._world = world
        self._pos = pos
        self.size = size
        self._color = color
        self._fontSize = int(size[1]*labelSize)
        self._label = label
        self._font = pg.font.SysFont('Arial', self._fontSize)
        self._bgColor = bgColor
        

    def draw_node(self):
        pos = self._pos+self.size
        self.pgObj = pg.draw.rect(self._world.win, self._bgColor, pg.Rect(pos),  100, 3)
        labelLength = self._fontSize*len(self._label)
        text = self._font.render(self._label, True, self._color)
        text_rect = text.get_rect(center = self.pgObj.center)
        self._world.win.blit(text, text_rect)
