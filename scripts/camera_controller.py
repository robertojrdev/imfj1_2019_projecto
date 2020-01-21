import pygame
from engine import ObjectBehaviour, Input, vector3, rotate_vectors, from_rotation_vector

class CameraController(ObjectBehaviour):
    def update(self, delta_time):
        
        #get direction
        mov_dir = vector3()
        if(Input.get_key(pygame.K_d)): #right
            mov_dir.x += 1
        if(Input.get_key(pygame.K_a)): #left
            mov_dir.x -= 1
        if(Input.get_key(pygame.K_PAGEUP) or Input.get_key(pygame.K_e)): #up
            mov_dir.y += 1
        if(Input.get_key(pygame.K_PAGEDOWN) or Input.get_key(pygame.K_q)): #down
            mov_dir.y -= 1
        if(Input.get_key(pygame.K_w)): #fwrd
            mov_dir.z += 1
        if(Input.get_key(pygame.K_s)): #backward
            mov_dir.z -= 1

        #rotate direction vector by camera rotation, normalize and apply transformation scaled by delta_time
        mov_dir = vector3.from_np3(rotate_vectors(self.transform.rotation, mov_dir.to_np3()))
        mov_dir.normalize()
        self.transform.position += mov_dir * delta_time

        #get rotation from inputs
        pitch = vector3()
        yaw = vector3()
        if(Input.get_key(pygame.K_RIGHT)):
            yaw.y += 1
        if(Input.get_key(pygame.K_LEFT)):
            yaw.y -= 1
        if(Input.get_key(pygame.K_UP)):
            pitch.x += 1
        if(Input.get_key(pygame.K_DOWN)):
            pitch.x -= 1

        #get quaternion from pitch and yaw scaled by delta_time
        pitch *= delta_time
        pitch = from_rotation_vector(pitch.to_np3())
        
        yaw *= delta_time
        yaw = from_rotation_vector(yaw.to_np3())

        #apply pitch and then yaw
        rot = self.transform.rotation
        rot *= pitch
        rot = yaw * rot #specifically in this order to rotate over the world Y axis instead of camera axis (unity like :D)
        self.transform.rotation = rot
        