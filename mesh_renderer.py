import math
from object_behaviour import ObjectBehaviour
from mesh import Mesh
from triangle import Triangle
from application import Application
from material import Material
from color import color
from vector3 import vector3


class MeshRenderer(ObjectBehaviour):
    """Prepare meshes to be renderered
    """
    def awake(self):
        self.material = Material(color(1,1,1,1), "mat")
        self.mesh = Mesh()
        self.debug_mode = False
        self.cull_by_distance = True

    def on_pre_render(self):
        world_matrix = self.transform.get_matrix()
        tris = []

        if ((self.material != None) and (self.mesh)):
            
            #distance culling
            if(self.cull_by_distance):
                direction_from_camera = self.transform.position - Application.scene.camera.transform.position
                dist = direction_from_camera.magnitude()
                if(dist >= Application.scene.camera.culling_distance):
                    return

            #display each side with a different color (DEBUG)
            if(self.debug_mode == True):
                colors = [(1,0,0),(0,1,0),(0,0,1),(.5,.5,0),(.5,0,.5),(0,.5,.5)]
                i = 0

            #Apply transform matrix transformation to triangles
            for triangle in self.mesh.tris:
                tpoly = []
                for v in triangle.vertices:
                    transformed = vector3.multiply_matrix(v, world_matrix)
                    tpoly.append(transformed)

                t = Triangle(tpoly[0], tpoly[1], tpoly[2])
                center = t.get_center()

                #calculate lights
                if(self.debug_mode == False):
                    light_intensity = .05
                    for light in Application.lights_buffer:
                        light_intensity += light.calculate_intensity(center, t.normal)
                    
                    if(light_intensity > 1):
                        light_intensity = 1

                    t.color = self.material.color * light_intensity
                else:
                    j = colors[math.floor(i / 2)]
                    t.color = color(j[0],j[1],j[2],1)
                    i += 1

                tris.append(t)

        #add triangle to buffer
        Application.add_triangle_to_buffer(tris)
    