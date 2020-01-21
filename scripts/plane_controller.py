import pygame
from engine import ObjectBehaviour, GameObject, Input, vector3, rotate_vectors, from_rotation_vector
from scripts.bullet import Bullet

class PlaneController(ObjectBehaviour):
    """Plane movement with WASD and Arrows, P shoot a bullet - Can be attached to any GameObject
    """
    def update(self, delta_time):
        #get movement input direction
        mov_dir = vector3()
        if(Input.get_key(pygame.K_d)):
            mov_dir.x += 1
        if(Input.get_key(pygame.K_a)):
            mov_dir.x -= 1
        if(Input.get_key(pygame.K_w)):
            mov_dir.z += 1
        if(Input.get_key(pygame.K_s)):
            mov_dir.z -= 1

        #apply object rotation to direction vector, normalize, scale and apply movement
        mov_dir = vector3.from_np3(rotate_vectors(self.transform.rotation, mov_dir.to_np3()))
        mov_dir.normalize()
        self.transform.position += mov_dir * delta_time * 1.5

        #get rotation input
        rot_dir = vector3()
        if(Input.get_key(pygame.K_RIGHT)):
            rot_dir.z -= 1
        if(Input.get_key(pygame.K_LEFT)):
            rot_dir.z += 1
        if(Input.get_key(pygame.K_UP)):
            rot_dir.x += 1
        if(Input.get_key(pygame.K_DOWN)):
            rot_dir.x -= 1

        # scale rotation, get a quaternion of it and apply it
        rot_dir *= delta_time * 1.5
        rot_dir = from_rotation_vector(rot_dir.to_np3())
        self.transform.rotation *= rot_dir

        #shoot a bullet
        if(Input.get_key_down(pygame.K_p)):
            bullet = GameObject("bullet")
            bullet.transform.position = self.transform.position
            bullet.transform.rotation = self.transform.rotation
            bullet.add_component(Bullet)
        