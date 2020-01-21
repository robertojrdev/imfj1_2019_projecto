import math
import bisect
import pygame
import numpy as np
from quaternion import *
from application import Application
from color import color
from object_behaviour import ObjectBehaviour
from vector3 import vector3

class Camera(ObjectBehaviour):
    """A camera used to see the world
    """
    def awake(self):
        Application.scene.camera = self
        self.background_color = color(.01,.01,.025)
        self.culling_distance = 15

    def setup(self, ortho, fov = 33):
        """Sutup
        
        Arguments:
            ortho {bool} -- true is ortho false is perspective
        
        Keyword Arguments:
            fov {float} -- field of view (default: {33})
        """
        self.ortho = ortho
        self.fov = math.radians(fov)
        self.near = 0.1
        self.far = 1000

    def get_projection_matrix(self):
        self.proj_matrix = np.zeros((4, 4))
        x = Application.screen.get_width()
        y = Application.screen.get_height()
        if (self.ortho):
            self.proj_matrix[0,0] = x * 0.5
            self.proj_matrix[1,1] = y * 0.5
            self.proj_matrix[3,0] = 0
            self.proj_matrix[3,1] = 0
            self.proj_matrix[3,3] = 1
        else:
            t = math.tan(self.fov)
            a = y / x
            self.proj_matrix[0,0] = 0.5 * x / t
            self.proj_matrix[1,1] = 0.5 * y / (a * t)
            self.proj_matrix[2,2] = self.far / (self.far - self.near)
            self.proj_matrix[2,3] = 1
            self.proj_matrix[3,0] = 0
            self.proj_matrix[3,2] = (-self.far * self.near) / (self.far - self.near)
            self.proj_matrix[3,3] = 0
            
            # self.proj_matrix[0,0] = 0.5 * x / t
            # self.proj_matrix[1,1] = 0.5 * y / (a * t)
            # self.proj_matrix[2,2] = 1
            # self.proj_matrix[2,3] = 1
            # self.proj_matrix[3,0] = 0
            # self.proj_matrix[3,1] = 0

        return self.proj_matrix

    def get_camera_matrix(self):
        pos = self.transform.position
        trans = np.identity(4)
        trans[3,0] = -pos.x
        trans[3,1] = -pos.y
        trans[3,2] = -pos.z    

        qrot  = as_rotation_matrix(self.transform.rotation)
        rotation_matrix = np.identity(4)
        rotation_matrix[0][0] = qrot[0][0]
        rotation_matrix[0][1] = qrot[0][1]
        rotation_matrix[0][2] = qrot[0][2]
        rotation_matrix[1][0] = qrot[1][0]
        rotation_matrix[1][1] = qrot[1][1]
        rotation_matrix[1][2] = qrot[1][2]
        rotation_matrix[2][0] = qrot[2][0]
        rotation_matrix[2][1] = qrot[2][1]
        rotation_matrix[2][2] = qrot[2][2]
        rotation_matrix[3,3] = 1

        return trans @ rotation_matrix

    def on_render(self):
        # Paint the background
        Application.screen.fill(self.background_color.tuple3())

        #get clip matrix
        camera_matrix = self.get_camera_matrix()
        projection_matrix = self.get_projection_matrix()
        clip_matrix = camera_matrix @ projection_matrix

        #prepare
        triangles = []
        cam_pos = self.transform.position
        cam_fwd = self.transform.forward.normalized()

        #get triangles from buffer to render
        for t in Application.triangles_buffer:
            center = t.get_center()
            direction = center - cam_pos
            dir_norm = direction.normalized()

            direction_dot = vector3.dot_product(cam_fwd, dir_norm)

            #only render the ones ahead of the camera
            if(direction_dot > 0.5):
                facing_camera_dot = vector3.dot_product(t.normal, dir_norm)
                #back-face culling
                if(facing_camera_dot < 0):
                    t.depth = direction.magnitude()
                    bisect.insort(triangles, t)

        #project triangles and draw them (transform from 3D to 2D to render in a flat screen)
        screen_w = Application.screen.get_width() * 0.5 
        screen_h = Application.screen.get_height() * 0.5
        for t in triangles:
            proj_vert = []
            for v in t.vertices:
                projected = vector3.multiply_matrix(v, clip_matrix)

                projected.x = screen_w + projected.x
                projected.y = screen_h  - projected.y
                
                proj_vert.append(( projected.x,  projected.y))
            
            pygame.draw.polygon(Application.screen, t.color.tuple3(), proj_vert, 0)
            # pygame.draw.polygon(Application.screen, (10,10,10), proj_vert, 1)
