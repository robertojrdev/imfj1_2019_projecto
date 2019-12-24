import pygame
import numpy as np
from vector3 import *
from quaternion import *

class Object3d:
    def __init__(self, name):
        self.name = name
        self.position = vector3()
        self.rotation = quaternion(1,0,0,0)
        self.local_rotation = quaternion(1,0,0,0)
        self.scale = vector3(1,1,1)
        self.mesh = None
        self.material = None
        self.children = []

    def get_matrix(self):
        return Object3d.get_prs_matrix(self.position, self.rotation, self.scale)

    def render(self, screen, clip_matrix, camera_position):
        world_matrix = self.get_matrix()
        
        mesh_matrix = world_matrix @ clip_matrix

        if ((self.material != None) and (self.mesh)):
            # self.mesh.render(screen, mesh_matrix, self.material)
            c = self.material.color.tuple3()        

            for poly in self.mesh.polygons:
                tpoly = []
                ppoly = []
                for v in poly:
                    vout = v.to_np4()
                    vout = vout @ world_matrix
                    transformed = from_np4(vout)

                    tpoly.append(transformed)

                edge1 = tpoly[1] - tpoly[0]
                edge2 = tpoly[2] - tpoly[1]
                normal = cross_product(edge1, edge2)

                center  = (tpoly[0] + tpoly[1] + tpoly[2]) / 3
                direction = center - camera_position

                facingCameraDot = dot_product(normal, direction)

                if(facingCameraDot < 0):
                    for v in tpoly:
                        vout = v.to_np4() @ clip_matrix
                        projected = from_np4(vout)

                        projected.x += screen.get_width() * 0.5
                        projected.y = screen.get_height() * 0.5 - projected.y
                        
                        ppoly.append(( projected.x,  projected.y))

                    pygame.draw.polygon(screen, c, ppoly, self.material.line_width)

        for child in self.children:
            # child.rotation = child.local_rotation * self.rotation
            child.render(screen, mesh_matrix, camera_position)

    def add_child(self, obj):
        self.children.append(obj)

    @staticmethod
    def get_prs_matrix(position, rotation, scale):
        trans = np.identity(4)
        trans[3,0] = position.x
        trans[3,1] = position.y
        trans[3,2] = position.z    

        qrot  = as_rotation_matrix(rotation)
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

        scale_matrix = np.identity(4)
        scale_matrix[0,0] = scale.x    
        scale_matrix[1,1] = scale.y
        scale_matrix[2,2] = scale.z  

        return scale_matrix @ rotation_matrix @ trans
