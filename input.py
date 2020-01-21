import pygame
from vector3 import vector3
from key import Key

class Input:
    keys = []
    mouse_buttons = []
    mouse_pos = vector3(0,0,0)
    mouse_delta = vector3(0,0,0)

    @staticmethod
    def update(evt):
        #update up and down values from previous update
        for k in Input.keys:
            k.update()

        for b in Input.mouse_buttons:
            b.update()

        # reset mouse motion
        Input.mouse_delta = vector3()

        #read the new events
        for e in evt:
            if(e.type == pygame.KEYDOWN or e.type == pygame.KEYUP):
                Input.update_key(e.key, e.type)
            elif(e.type == pygame.MOUSEMOTION):
                pos = pygame.mouse.get_pos()
                delta = pygame.mouse.get_rel()
                Input.mouse_pos = vector3(pos[0], pos[0], 0)
                Input.mouse_delta = vector3(delta[0], delta[0], 0)
            # elif(e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP):
            #     self.update_mouse_button()

    # KEYBOARD
    @staticmethod
    def update_key(key, state):
        for k in Input.keys:
            if k.key == key:
                k.update(state)
                return
        
        k = Input.add_key(key)
        k.update(state)
        
    @staticmethod
    def add_key(key):
        k = Key(key)
        Input.keys.append(k)
        return k

    @staticmethod
    def get_key(key):
        for k in Input.keys:
            if k.key == key:
                return k.holding
        return False

    @staticmethod
    def get_key_down(key):
        for k in Input.keys:
            if k.key == key:
                return k.down
        return False

    @staticmethod
    def get_key_up(key):
        for k in Input.keys:
            if k.key == key:
                return k.up
        return False
    
    # MOUSE
    @staticmethod
    def update_mouse_button(button, state):
        for b in Input.mouse_buttons:
            if b.key == button:
                b.update(state)
                return
        
        b = Input.add_mouse_button(button)
        b.update(state)

    @staticmethod
    def add_mouse_button(button):
        b = Key(button)
        Input.mouse_buttons.append(b)
        return b

    @staticmethod
    def get_mouse_button(button):
        for b in Input.mouse_buttons:
            if b.key == button:
                return b.holding
        return False

    @staticmethod
    def get_mouse_button_down(button):
        for b in Input.mouse_buttons:
            if b.key == button:
                return b.down
        return False

    @staticmethod
    def get_mouse_button_up(button):
        for b in Input.mouse_buttons:
            if b.key == button:
                return b.up
        return False
