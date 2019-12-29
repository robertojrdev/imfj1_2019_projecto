import pygame
import time
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
            return vector3.multiply_matrix(self.local_position, self.parent.get_matrix())
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

    def get_right(self):
        return from_np3(rotate_vectors(self.rotation, vector3.right().to_np3()))

    def get_forward(self):
        return from_np3(rotate_vectors(self.rotation, vector3.forward().to_np3()))

    parent = property(get_parent, set_parent)
    rotation = property(get_rotation, set_rotation)
    position = property(get_position, set_position)
    scale = property(get_scale, set_scale)
    up = property(get_up)
    right = property(get_right)
    forward = property(get_forward)

    def get_matrix(self):
        return Transform.get_prs_matrix(self.position, self.rotation, self.scale)

    @staticmethod
    def get_position_matrix(position):
        trans = np.identity(4)
        trans[3,0] = position.x
        trans[3,1] = position.y
        trans[3,2] = position.z
        return trans

    @staticmethod
    def get_rotation_matrix(rotation):
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
        return rotation_matrix

    @staticmethod
    def get_scale_matrix(scale):
        scale_matrix = np.identity(4)
        scale_matrix[0,0] = scale.x    
        scale_matrix[1,1] = scale.y
        scale_matrix[2,2] = scale.z 
        return scale_matrix

    @staticmethod
    def get_prs_matrix(position, rotation, scale):
        trans = Transform.get_position_matrix(position)
        rotation_matrix = Transform.get_rotation_matrix(rotation)
        scale_matrix = Transform.get_scale_matrix(scale)

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
        Application.scene.add_object(self)

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
        self.debug_mode = False

    def render(self, screen, clip_matrix, camera_position):
        world_matrix = self.transform.get_matrix()
        tris = []

        if ((self.material != None) and (self.mesh)):
            clr = self.material.color

            colors = [(1,0,0),(0,1,0),(0,0,1),(.5,.5,0),(.5,0,.5),(0,.5,.5)]
            i = 0

            for triangle in self.mesh.tris:
                tpoly = []
                for v in triangle.vertices:
                    transformed = vector3.multiply_matrix(v, world_matrix)
                    tpoly.append(transformed)

                edge1 = tpoly[1] - tpoly[0]
                edge2 = tpoly[2] - tpoly[1]
                normal = cross_product(edge1, edge2)

                center  = (tpoly[0] + tpoly[1] + tpoly[2]) / 3
                direction = center - camera_position

                facingCameraDot = dot_product(normal.normalized(), direction.normalized())

                if(facingCameraDot < 0):
                    c = clr * -facingCameraDot
                    j = colors[math.floor(i / 2)]
                    if(self.debug_mode):
                        c = color(j[0],j[1],j[2],1)
                        # c = color(j[0],j[1],j[2],1) * -facingCameraDot
                    tris.append(Triangle(tpoly[0], tpoly[1], tpoly[2], c, direction.magnitude()))

                i += 1
        return tris

class Scene:
    def __init__(self, name):
        self.name = name
        self.camera = None
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        if self.camera:
            self.camera.render(self.objects)
            
class Camera(ObjectBehaviour):
    def awake(self):
        Application.scene.camera = self
        self.background_color = color(.01,.01,.025)

    def setup(self, ortho, fov = 33):
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
        return Transform.get_prs_matrix(-self.transform.position, self.transform.rotation.inverse(), vector3(1,1,1))

    def render(self, objects):
        # Paint the background
        Application.screen.fill(self.background_color.tuple3())

        camera_matrix = self.get_camera_matrix()
        projection_matrix = self.get_projection_matrix()
        clip_matrix = camera_matrix @ projection_matrix

        triangles = []

        for obj in objects:
            renderer = obj.get_component(MeshRenderer)
            if (renderer):
                triangles.extend(renderer.render(Application.screen, projection_matrix, self.transform.position))

        triangles.sort()

        for t in triangles:
            proj_vert = []
            for v in t.vertices:
                projected = vector3.multiply_matrix(v, clip_matrix)

                projected.x = Application.screen.get_width() * 0.5 + projected.x
                projected.y = Application.screen.get_height() * 0.5 - projected.y
                
                proj_vert.append(( projected.x,  projected.y))
            
            pygame.draw.polygon(Application.screen, t.color.tuple3(), proj_vert, 0)
            pygame.draw.polygon(Application.screen, (10,10,10), proj_vert, 1)

class Mesh:
    def __init__(self, name = "UnknownMesh"):
        self.name = name
        self.tris = []

    def offset(self, v):
        new_polys = []
        for poly in self.tris:
            new_poly = []
            for p in poly:
                new_poly.append(p + v)
            new_polys.append(new_poly)

        self.tris = new_polys

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

        v1 = origin + axis0 + axis1
        v2 = origin + axis0 - axis1
        v3 = origin - axis0 - axis1
        v4 = origin - axis0 + axis1

        t1 = Triangle(v1, v2, v3)
        t2 = Triangle(v1, v3, v4)

        mesh.tris.append(t1)
        mesh.tris.append(t2)

        return mesh

class Triangle:
    def __init__(self, v1, v2, v3, color = None, depth = 0):
        self.vertices = [v1,v2,v3]
        self.color = color
        self.depth = depth

    def __lt__(self, other):
        return self.depth > other.depth

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

class Key:
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

class Application:
    screen = None
    scene = None


    def __init__(self, res_x = 640, res_y = 480):
        # Initialize pygame, with the default parameters
        pygame.init()

        # Create a window and a display surface
        Application.screen = pygame.display.set_mode((res_x, res_y))

        # Create a scene
        Application.scene = Scene("Main Scene")

    def init(self):
        # Timer
        delta_time = 0
        prev_time = time.time()

        # Game loop, runs forever
        while (True):
            # # Process OS events
            evt = pygame.event.get()
            for event in evt:
                # Checks if the user closed the window
                if (event.type == pygame.QUIT):
                    # Exits the application immediately
                    return
                elif (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        return

            Input.update(evt)

            # Call update
            for o in Application.scene.objects:
                for c in o.components:
                    c.update(delta_time)

            # Render Scene
            Application.scene.render()

            # Swaps the back and front buffer, effectively displaying what we rendered
            pygame.display.flip()

            # Updates the timer, so we we know how long has it been since the last frame
            delta_time = time.time() - prev_time
            prev_time = time.time()

