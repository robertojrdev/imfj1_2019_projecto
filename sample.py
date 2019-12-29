from engine import *
from scripts.cube_script import *

# Define a main function, just to keep things nice and tidy
def main():

    # Define all objects and it's initial configuration 
    # to start the application
    objs = []

    obj1 = GameObject("TestObject")
    pos1 = vector3(0, 0, 5)
    obj1.transform.position = pos1
    obj1.transform.scale = vector3(1,1,1)
    obj1_renderer = obj1.add_component(MeshRenderer)
    obj1_renderer.mesh = Mesh.create_cube((1, 1, 1))
    obj1_renderer.material = Material(color(1,0,0,1), "TestMaterial1")
    obj1.add_component(Cube)
    objs.append(obj1)

    obj2 = GameObject("TestObject")
    obj2.transform.position = vector3(0,.75,0)
    obj2.transform.scale = vector3(.5,.5,.5)
    obj2_renderer = obj2.add_component(MeshRenderer)
    obj2_renderer.mesh = Mesh.create_cube((1, 1, 1))
    obj2_renderer.material = Material(color(0,1,0,1), "TestMaterial1")
    obj2.transform.parent = obj1.transform
    objs.append(obj2)

    obj3 = GameObject("TestObject")
    obj3.transform.position = vector3(0,.75,0)
    obj3.transform.scale = vector3(.5,.5,.5)
    obj3_renderer = obj3.add_component(MeshRenderer)
    obj3_renderer.mesh = Mesh.create_cube((1, 1, 1))
    obj3_renderer.material = Material(color(0,0,1,1), "TestMaterial1")
    obj3.transform.parent = obj2.transform
    objs.append(obj3)

    Application(objs)
    return


# Run the main function
main()
