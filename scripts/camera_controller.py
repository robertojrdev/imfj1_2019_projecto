import pygame
from engine import ObjectBehaviour, Input, Transform
from vector3 import *
from quaternion import *
from scripts.bullet import *

class CameraController(ObjectBehaviour):
    def update(self, delta_time):
        mov_dir = vector3()
        if(Input.get_key(pygame.K_d)):
            mov_dir.x += 1
        if(Input.get_key(pygame.K_a)):
            mov_dir.x -= 1
        if(Input.get_key(pygame.K_PAGEUP)):
            mov_dir.y += 1
        if(Input.get_key(pygame.K_PAGEDOWN)):
            mov_dir.y -= 1
        if(Input.get_key(pygame.K_w)):
            mov_dir.z += 1
        if(Input.get_key(pygame.K_s)):
            mov_dir.z -= 1

        # mov_dir = from_np3(rotate_vectors(self.transform.rotation, mov_dir.to_np3()))
        # mov_dir.normalize()
        self.transform.position += mov_dir * delta_time

        if(Input.get_key_down(pygame.K_p)):
            bullet = GameObject("bullet")
            bullet.transform.position = self.transform.position
            bullet.transform.rotation = self.transform.rotation
            bullet.add_component(Bullet)
        