from engine import *
from scripts.cube_script import *
from scripts.camera_controller import *
from scripts.plane_controller import *

# Create a camera - when a camera is created it becomes the active camera in the active scene
camObj = GameObject("camera")
camera = camObj.add_component(Camera)
camera.setup(False)
light = camObj.add_component(PointLight)
light.range = 20

planeObj = GameObject("light")
light = planeObj.add_component(PointLight)
# light.range = 100
planeObj.add_component(PlaneController)
planeObj.transform.position = vector3(0,0,0)
plane_renderer = planeObj.add_component(MeshRenderer)
plane_renderer.mesh = Mesh.from_obj("ship.obj")
plane_renderer.material = Material(color(1,1,1,1), "TestMaterial1")

camera.transform.parent = planeObj.transform
camera.transform.position = vector3(0,0.1,-1)

#First Cube
obj1 = GameObject("TestObject")
pos1 = vector3(0, 0, 5)
obj1.transform.position = pos1
obj1.transform.scale = vector3(1,1,1)
obj1_renderer = obj1.add_component(MeshRenderer)
obj1_renderer.mesh = Mesh.create_cube((1, 1, 1))
obj1_renderer.material = Material(color(1,0,0,1), "TestMaterial1")
obj1.add_component(Cube)

#Second Cube
obj2 = GameObject("TestObject")
obj2.transform.position = vector3(0,.75,0)
obj2.transform.scale = vector3(.5,.5,.5)
obj2_renderer = obj2.add_component(MeshRenderer)
obj2_renderer.mesh = Mesh.create_cube((1, 1, 1))
obj2_renderer.material = Material(color(0,1,0,1), "TestMaterial1")
obj2.transform.parent = obj1.transform

#Third cube
obj3 = GameObject("TestObject")
obj3.transform.position = vector3(0,.75,0)
obj3.transform.scale = vector3(.5,.5,.5)
obj3_renderer = obj3.add_component(MeshRenderer)
obj3_renderer.mesh = Mesh.create_cube((1, 1, 1))
obj3_renderer.material = Material(color(0,0,1,1), "TestMaterial1")
obj3.transform.parent = obj2.transform
