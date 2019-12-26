import pygame
from vector3 import *
from quaternion import *
from material import *

class Component:
    def __init__(self, game_object):
        self.game_object = game_object
        self.transform = game_object.transform

class Transform:
    def __init__(self, game_object):
        self.game_object = game_object
        self.local_position = vector3()
        self.local_rotation = quaternion(1, 0, 0, 0)
        self.local_scale = vector3.one()
        self._parent = None
        self.children = []

    # PROPERTIES
    def get_position(self):
        if(self._parent):
            translated_position = rotate_vectors(self._parent.rotation, self.local_position.to_np3())
            translated_position = from_np3(translated_position)
            scaled_position = vector3.scale(self._parent.scale, translated_position)
            return self._parent.position + scaled_position
        else:
            return self.local_position

    def set_position(self, value):
        self.local_position = value

    def get_rotation(self):
        if(self._parent):
            return self.local_rotation * self._parent.rotation
        else:
            return self.local_rotation

    def set_rotation(self, value):
        self.local_rotation = value

    def get_scale(self):
        if(self._parent):
            return vector3.scale(self.local_scale, self._parent.scale)
        else:
            return self.local_scale

    def set_scale(self, value):
        self.local_scale = value

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        if(parent == self):
            print("A TRANSFORM CANNOT BE THE PARENT OF ITSELF")
            return

        if(issubclass(type(parent), Transform) == False):
            print("YOU NEED TO PASS A TRANSFORM AS ARGUMENT")
            return

        if(self._parent != None):
            self._parent.children.remove(self)

        self._parent = parent
        self._parent.children.append(self)

    def get_up(self):
        return from_np3(rotate_vectors(self.rotation, vector3.up().to_np3()))

    parent = property(get_parent, set_parent)
    rotation = property(get_rotation, set_rotation)
    position = property(get_position, set_position)
    scale = property(get_scale, set_scale)
    up = property(get_up)

    def get_matrix(self):
        return Transform.get_prs_matrix(self.position, self.rotation, self.scale)

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

class ObjectBehaviour(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.awake()

    def awake(self):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass

    def on_destroy(self):
        pass

class GameObject():
    def __init__(self, name = "Object"):
        self.name = name
        self.transform = None
        self.components = []
        self.transform = Transform(self)

    def add_component(self, comp):
        if(issubclass(comp, Component) == False):
            print("THIS IS NOT A COMPONENT")
            return
            
        newComp = comp(Component(self))
        self.components.append(newComp)
        return newComp

    def get_component(self, comp):
        for o in self.components:
            if issubclass(type(o), comp):
                return o
        return

class MeshRenderer(ObjectBehaviour):
    def awake(self):
        self.material = Material(color(1,1,1,1), "mat")
        self.mesh = Mesh()

    def render(self, screen, clip_matrix, camera_position):
        world_matrix = self.transform.get_matrix()
        # mesh_matrix = world_matrix @ clip_matrix

        light = vector3(1,1,1).normalized()

        if ((self.material != None) and (self.mesh)):
            clr = self.material.color

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

                facingCameraDot = dot_product(normal, direction.normalized())

                if(facingCameraDot < 0):
                    for v in tpoly:
                        vout = v.to_np4() @ clip_matrix
                        projected = from_np4(vout)

                        projected.x += screen.get_width() * 0.5
                        projected.y = screen.get_height() * 0.5 - projected.y
                        
                        ppoly.append(( projected.x,  projected.y))

                    c = color.lerp(color(0,0,0,0), clr, -facingCameraDot)

                    pygame.draw.polygon(screen, c.tuple3(), ppoly, 0)
                    pygame.draw.polygon(screen, self.material.color.tuple3(), ppoly, self.material.line_width)

class Scene:
    def __init__(self, name):
        self.name = name
        self.camera = None
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self, screen):
        camera_matrix = self.camera.get_camera_matrix()
        projection_matrix = self.camera.get_projection_matrix()

        clip_matrix = camera_matrix @ projection_matrix

        for obj in self.objects:
            renderer = obj.get_component(MeshRenderer)
            if (renderer):
                renderer.render(screen, clip_matrix, self.camera.transform.position)

class Camera(ObjectBehaviour):
    def setup(self, ortho, res_x, res_y, fov = 33):
        self.ortho = ortho
        self.res_x = res_x
        self.res_y = res_y
        self.fov = math.radians(fov)

    def get_projection_matrix(self):
        self.proj_matrix = np.zeros((4, 4))
        if (self.ortho):
            self.proj_matrix[0,0] = self.res_x * 0.5
            self.proj_matrix[1,1] = self.res_y * 0.5
            self.proj_matrix[3,0] = 0
            self.proj_matrix[3,1] = 0
            self.proj_matrix[3,3] = 1
        else:
            t = math.tan(self.fov)
            a = self.res_y / self.res_x
            self.proj_matrix[0,0] = 0.5 * self.res_x / t
            self.proj_matrix[1,1] = 0.5 * self.res_y / (a * t)
            self.proj_matrix[2,3] = 1
            self.proj_matrix[3,0] = 0
            self.proj_matrix[3,1] = 0

        return self.proj_matrix

    def get_camera_matrix(self):
        return Transform.get_prs_matrix(-self.transform.position, self.transform.rotation.inverse(), vector3(1,1,1))

class Mesh:
    def __init__(self, name = "UnknownMesh"):
        self.name = name
        self.polygons = []

    def offset(self, v):
        new_polys = []
        for poly in self.polygons:
            new_poly = []
            for p in poly:
                new_poly.append(p + v)
            new_polys.append(new_poly)

        self.polygons = new_polys

    def render(self, screen, matrix, material):
        c = material.color.tuple3()        

        for poly in self.polygons:
            tpoly = []
            spoly = []
            for v in poly:
                vout = v.to_np4()
                vout = vout @ matrix
                transformed = from_np4(vout)

                transformed.x += screen.get_width() * 0.5
                transformed.y = screen.get_height() * 0.5 - transformed.y
                
                tpoly.append(( transformed.x,  transformed.y))

            pygame.draw.polygon(screen, c, tpoly, material.line_width)


    @staticmethod
    def create_cube(size, mesh = None):
        if (mesh == None):
            mesh = Mesh("UnknownCube")

        Mesh.create_quad(vector3( size[0] * 0.5, 0, 0), vector3(0, -size[1] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)
        Mesh.create_quad(vector3(-size[0] * 0.5, 0, 0), vector3(0,  size[1] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)

        Mesh.create_quad(vector3(0,  size[1] * 0.5, 0), vector3(size[0] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)
        Mesh.create_quad(vector3(0, -size[1] * 0.5, 0), vector3(-size[0] * 0.5, 0), vector3(0, 0, size[2] * 0.5), mesh)

        Mesh.create_quad(vector3(0, 0,  size[2] * 0.5), vector3(-size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)
        Mesh.create_quad(vector3(0, 0, -size[2] * 0.5), vector3( size[0] * 0.5, 0), vector3(0, size[1] * 0.5, 0), mesh)

        return mesh

    @staticmethod
    def create_quad(origin, axis0, axis1, mesh):
        if (mesh == None):
            mesh = Mesh("UnknownQuad")

        poly = []
        poly.append(origin + axis0 + axis1)
        poly.append(origin + axis0 - axis1)
        poly.append(origin - axis0 - axis1)
        poly.append(origin - axis0 + axis1)

        mesh.polygons.append(poly)

        return mesh
    
