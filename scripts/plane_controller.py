import pygame
from engine import ObjectBehaviour, Input, Transform
from vector3 import *
from quaternion import *
from scripts.bullet import *

class PlaneController(ObjectBehaviour):
    def update(self, delta_time):
        mov_dir = vector3()
        if(Input.get_key(pygame.K_d)):
            mov_dir.x += 1
        if(Input.get_key(pygame.K_a)):
            mov_dir.x -= 1
        if(Input.get_key(pygame.K_w)):
            mov_dir.z += 1
        if(Input.get_key(pygame.K_s)):
            mov_dir.z -= 1

        mov_dir = from_np3(rotate_vectors(self.transform.rotation, mov_dir.to_np3()))
        mov_dir.normalize()
        self.transform.position += mov_dir * delta_time * 1.5

        rot_dir = vector3()
        if(Input.get_key(pygame.K_RIGHT)):
            rot_dir.z -= 1
        if(Input.get_key(pygame.K_LEFT)):
            rot_dir.z += 1
        if(Input.get_key(pygame.K_UP)):
            rot_dir.x += 1
        if(Input.get_key(pygame.K_DOWN)):
            rot_dir.x -= 1

        # rot_dir.normalize()
        rot_dir *= delta_time * 1.5
        rot_dir = from_rotation_vector(rot_dir.to_np3())
        self.transform.rotation *= rot_dir

        if(Input.get_key_down(pygame.K_p)):
            bullet = GameObject("bullet")
            bullet.transform.position = self.transform.position
            bullet.transform.rotation = self.transform.rotation
            bullet.add_component(Bullet)
        