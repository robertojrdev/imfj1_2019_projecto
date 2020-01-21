from vector3 import vector3

class Triangle:
    def __init__(self, v1, v2, v3, color = None, depth = 0):
        self.vertices = [v1,v2,v3]
        self.color = color
        self.depth = depth

        edge1 = v2 - v1
        edge2 = v3 - v2
        self.normal = vector3.cross_product(edge1, edge2).normalized()

    def __lt__(self, other):
        return self.depth > other.depth

    def get_center(self):
        return (self.vertices[0] + self.vertices[1] + self.vertices[2]) / 3
