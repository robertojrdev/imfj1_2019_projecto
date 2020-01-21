from vector3 import vector3
from triangle import Triangle

class Mesh:
    """A class that allows creating or modifying meshes from scripts.
    """
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
        """Create a unity cube scaled by size
        
        Arguments:
            size {float} -- size to scale
        
        Keyword Arguments:
            mesh {Mesh} -- mesh to add the triangles to (default: {None})
        
        Returns:
            Mesh -- a mesh with the given triangles
        """
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

    @staticmethod
    def from_obj(file_path, mesh = None):
        """Load a mesh from an .obj file
        
        Arguments:
            file_path {string} -- the path to the file
        
        Keyword Arguments:
            mesh {Mesh} -- mesh to assign the polygons (default: {None})
        
        Returns:
            Mesh -- a mesh with the loaded polygons
        """
        if (mesh == None):
            mesh = Mesh(file_path)
        vertices = []

        file = open(file_path, 'r')
        for line in file:
            if(line[0] == 'v'):
                elements = line.split()
                p1 = float(elements[1])
                p2 = float(elements[2])
                p3 = float(elements[3])
                vertices.append(vector3(p1,p2,p3))
            if(line[0] == 'f'):
                elements = line.split()
                v1 = int(elements[1]) - 1
                v2 = int(elements[2]) - 1
                v3 = int(elements[3]) - 1
                triangle = Triangle(vertices[v1],vertices[v2],vertices[v3])
                mesh.tris.append(triangle)

        return mesh
