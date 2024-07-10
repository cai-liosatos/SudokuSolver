import pygame
from pygame.locals import *
#create button

class Button():
    def __init__(self, x, y, text, width, height):
        self.width = int(width)
        self.height = int(height)
        self.text = text
        self.font = pygame.font.Font(None, 52)
        self.image = pygame.transform.scale(self.font.render(self.text, True, pygame.Color("Black")), (self.width-10, self.height-10))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pygame.draw.rect(surface, [0, 0, 0], [self.rect.x, self.rect.y, self.width, self.height], width=2)
        #get mouse pos
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        
        surface.blit(self.image, (self.rect.x+5, self.rect.y+5))    
        return action