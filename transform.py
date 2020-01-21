from vector3 import *
from quaternion import *

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
            q = quaternion()
            local = self.local_rotation
            q.x = local.x
            q.y = local.y
            q.z = local.z
            q.w = local.w
            return q

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
        return vector3.from_np3(rotate_vectors(self.rotation, vector3.up().to_np3()))

    def get_right(self):
        return vector3.from_np3(rotate_vectors(self.rotation, vector3.right().to_np3()))

    def get_forward(self):
        return vector3.from_np3(rotate_vectors(self.rotation, vector3.forward().to_np3()))

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
        rotation_matrix[0][1] = qrot[1][0]
        rotation_matrix[0][2] = qrot[2][0]
        rotation_matrix[1][0] = qrot[0][1]
        rotation_matrix[1][1] = qrot[1][1]
        rotation_matrix[1][2] = qrot[2][1]
        rotation_matrix[2][0] = qrot[0][2]
        rotation_matrix[2][1] = qrot[1][2]
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
