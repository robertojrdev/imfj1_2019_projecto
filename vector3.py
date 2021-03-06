import math
from mathf import *
import numpy as np

class InvalidOperationException(Exception):
    def __init__(self, op, type1, type2):
        self.op = op
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        return "Invalid operation (" + self.op + ") between " + str(self.type1) + " and " + str(self.type2)

class vector3:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __add__(self, v):
        if (isinstance(v, vector3)):
            return vector3(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            raise(InvalidOperationException("add", type(self), type(v)))

    def __sub__(self, v):
        if (isinstance(v, vector3)):
            return vector3(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            raise(InvalidOperationException("sub", type(self), type(v)))

    def __mul__(self, v):
        if (isinstance(v, (int, float))):
            return vector3(self.x * v, self.y * v, self.z * v)
        else:
            raise(InvalidOperationException("mult", type(self), type(v)))

    def __truediv__(self, v):
        if (isinstance(v, (int, float))):
            return vector3(self.x / v, self.y / v, self.z / v)
        else:
            raise(InvalidOperationException("mult", type(self), type(v)))

    def __eq__(self, v):
        if (isinstance(v, vector3)):
            return (((self - v).magnitude()) < 0.0001)
        else:
            raise(InvalidOperationException("eq", type(self), type(v)))

    def __ne__(self, v):
        if (isinstance(v, vector3)):
            return (((self - v).magnitude()) > 0.0001)
        else:
            raise(InvalidOperationException("neq", type(self), type(v)))

    def __isub__(self, v):
        return self - v

    def __iadd__(self, v):
        return self + v

    def __imul__(self, v):
        return self * v

    def __idiv__(self, v):
        return self / v

    def __neg__(self):
        return vector3(-self.x, -self.y, -self.z)

    def magnitude(self):
        return math.sqrt(self.dot(self))

    def magnitude_squared(self):
        return self.dot(self)

    def dot(self, v):
        if (isinstance(v, vector3)):
            return self.x * v.x + self.y * v.y + self.z * v.z
        else:
            raise(InvalidOperationException("dot", type(self), type(v)))

    def cross(self, v):
        if (isinstance(v, vector3)):
            return vector3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)
        else:
            raise(InvalidOperationException("dot", type(self), type(v)))

    def normalize(self):
        mag = self.magnitude()
        if mag > 0.0001:
            d = 1.0 / mag
            self.x *= d
            self.y *= d
            self.z *= d
        else:
            self.x = 0
            self.y = 0
            self.z = 0

    def normalized(self):
        mag = self.magnitude()
        if mag > 0.0001:
            d = 1.0 / self.magnitude()
            return vector3(self.x * d, self.y * d, self.z * d)
        else:
            return vector3()

    def to_np3(self):
        return np.array([self.x, self.y, self.z])

    def to_np4(self, w = 1):
        return np.array([self.x, self.y, self.z, w])

    @staticmethod
    def one():
        return vector3(1,1,1)
    @staticmethod
    def right():
        return vector3(1,0,0)
    @staticmethod
    def up():
        return vector3(0,1,0)
    @staticmethod
    def forward():
        return vector3(0,0,1)
    @staticmethod
    def scale(v1, v2):
        return vector3(v1.x * v2.x, v1.y * v2.y, v1.z * v2.z)
    @staticmethod
    def multiply_matrix(v, m):
        return vector3.from_matrix(v.to_np4() @ m)
    @staticmethod
    def lerp(a, b, t):
        c = vector3()
        c.x = lerp(a.x, b.x, t)
        c.y = lerp(a.y, b.y, t)
        c.z = lerp(a.z, b.z, t)
        return c

    @staticmethod
    def from_np3(n):
        return vector3(n[0], n[1], n[2])

    @staticmethod
    def from_np4(v):
        return vector3(v[0], v[1], v[2])

    @staticmethod
    def from_matrix(v):
        return vector3(v[0] / v[3], v[1] / v[3], v[2] / v[3])

    @staticmethod
    def dot_product(v1, v2):
        return v1.dot(v2)

    @staticmethod
    def cross_product(v1, v2):
        return v1.cross(v2)

