from settings import *
import pygame

#initialise the button requirements
class button:
    def __init__(self, x, y, width, height, text = None, colour = (73,73,73), highlightedcolour = (189,189,189), function = None, params = None):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.colour = colour
        self.highlightedcolour = highlightedcolour
        self.function = function
        self.params = params
        self.highlighted = False
        self.width = width
        self.height = height

#provide an update when the mouse interacts with the button
    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

#places the button on the screen
    def draw(self, window):
        self.image.fill(self.highlightedcolour if self.highlighted else self.colour)
        if self.text:
            self.drawText(self.text)
        window.blit(self.image, self.pos)

#calls the function in passing buttons on our app_class
    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()

#draw text on button
    def drawText(self, text):
        font = pygame.font.SysFont("comicsansms", 20, bold = 1)
        text = font.render(text, False, (0,0,0))
        width, height = text.get_size()
        x = ((self.width - width)) // cellsize #text position
        y = ((self.width - height)) // cellsize #text position
        self.image.blit(text, (x, y))

