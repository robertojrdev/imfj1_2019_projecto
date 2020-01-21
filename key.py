import pygame

class Key:
    """Represents a key state
    """
    def __init__(self, key):
        self.key = key
        self.down = False
        self.holding = False
        self.up = False

    def update(self, state = None):
        if(state == None):
            if(self.down == True):
                self.down = False
            if(self.up == True):
                self.up = False
        elif(state == pygame.KEYDOWN or state == pygame.MOUSEBUTTONDOWN):
            self.down = True
            self.holding = True
            self.up = False
        elif(state == pygame.KEYUP or state == pygame.MOUSEBUTTONUP):
            self.down = False
            self.holding = False
            self.up = True