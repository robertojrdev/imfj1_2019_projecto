# Import pygame into our program
# import pygame
# import pygame.freetype
import time

# from scene import *
# from object3d import *
# from mesh import *
# from material import *
# from color import *
from engine import *

# Define a main function, just to keep things nice and tidy
def main():
    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 640
    res_y = 480

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("TestScene")

    camObj = GameObject("camera")
    camera = camObj.add_component(Camera)
    camera.setup(False, res_x, res_y)

    scene.camera = camera

    # Moves the camera back 2 units
    # camObj.transform.position -= vector3(0,0,2)

    # Create a cube and place it in a scene, at position (0,0,0)
    # This cube has 1 unit of side, and is red
    obj1 = GameObject("TestObject")
    pos1 = vector3(0, 0, 5)
    obj1.transform.position = pos1
    obj1.transform.scale = vector3(1,1,1)
    obj1_renderer = obj1.add_component(MeshRenderer)
    obj1_renderer.mesh = Mesh.create_cube((1, 1, 1))
    obj1_renderer.material = Material(color(1,0,0,1), "TestMaterial1")
    scene.add_object(obj1)

    obj2 = GameObject("TestObject")
    obj2.transform.position = vector3(0,.75,0)
    obj2.transform.scale = vector3(.5,.5,.5)
    obj2_renderer = obj2.add_component(MeshRenderer)
    obj2_renderer.mesh = Mesh.create_cube((1, 1, 1))
    obj2_renderer.material = Material(color(0,1,0,1), "TestMaterial1")
    obj2.transform.parent = obj1.transform
    scene.add_object(obj2)

    obj3 = GameObject("TestObject")
    obj3.transform.position = vector3(0,.75,0)
    obj3.transform.scale = vector3(.5,.5,.5)
    obj3_renderer = obj3.add_component(MeshRenderer)
    obj3_renderer.mesh = Mesh.create_cube((1, 1, 1))
    obj3_renderer.material = Material(color(0,0,1,1), "TestMaterial1")
    obj3.transform.parent = obj2.transform
    scene.add_object(obj3)

    # Specify the rotation of the object. It will rotate 15 degrees around the axis given, 
    # every second
    angle = 50
    axis = vector3(1,0.7,0.2)
    axis = vector3(1,0,0)
    axis.normalize()

    axis2 = vector3(0,0,1)

    # Timer
    delta_time = 0
    prev_time = time.time()
    counter = 0
    timer = 0

    obj1.transform.rotation = obj1.transform.rotation * from_rotation_vector((math.radians(90),0,0))
    # obj2.transform.rotation = obj2.transform.rotation * from_rotation_vector((math.radians(90),0,0))
    # obj3.transform.rotation = obj3.transform.rotation * from_rotation_vector((math.radians(90),0,0))

    input = Input()

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

        input.update(evt)

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))

        # Rotates the object, considering the time passed (not linked to frame rate)
        # q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3())
        # obj1.transform.rotation = q * obj1.transform.rotation

        if input.get_key(pygame.K_SPACE):
            counter += delta_time
            x = math.sin(counter)
            y = math.cos(counter * .5)
            z = 5 + math.cos(counter)
            obj1.transform.position = vector3(x,y,z)
            obj1.transform.rotation = obj1.transform.rotation * from_rotation_vector((0,math.radians(20 * delta_time),0))
            obj1.transform.rotation = obj1.transform.rotation * from_rotation_vector((math.radians(20 * delta_time),0,0))

        dir = vector3()
        rot = vector3()

        if input.get_key(pygame.K_w):
            dir.z += 1
        if input.get_key(pygame.K_s):
            dir.z -= 1
        if input.get_key(pygame.K_a):
            dir.x -= 1
        if input.get_key(pygame.K_d):
            dir.x += 1
        if input.get_key(pygame.K_q):
            dir.y -= 1
        if input.get_key(pygame.K_e):
            dir.y += 1

        if input.get_key(pygame.K_UP):
            rot.x += 1
        if input.get_key(pygame.K_DOWN):
            rot.x -= 1
        if input.get_key(pygame.K_RIGHT):
            rot.y -= 1
        if input.get_key(pygame.K_LEFT):
            rot.y += 1

        camera.transform.position += from_np3(rotate_vectors(camera.transform.rotation, dir.to_np3())) * delta_time
        rot *= delta_time
        camera.transform.rotation = from_euler_angles(rot.to_np3()) * camera.transform.rotation

        # obj3.transform.position = obj1.transform.position + obj1.transform.up

        # obj2.transform.position = vector3(1,0,5 + math.sin(counter) * 5)
        # obj2.transform.rotation = obj2.transform.rotation * from_rotation_vector((0,math.radians(10 * delta_time),0))
        # obj2.transform.rotation = obj2.transform.rotation * from_rotation_vector((math.radians(10 * delta_time),0,0))

        # obj3.transform.position = vector3(-1,0,5 + math.sin(counter) * 5)
        # obj3.transform.rotation = obj3.transform.rotation * from_rotation_vector((0,math.radians(10 * delta_time),0))
        # obj3.transform.rotation = obj3.transform.rotation * from_rotation_vector((math.radians(10 * delta_time),0,0))

        # axis2 = from_np3(rotate_vectors(from_euler_angles((delta_time,0,0)), axis2.to_np3()))
        # obj1.transform.position = pos1 + axis2

        # obj2.transform.position = obj1.transform.up + obj1.transform.position

        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()
        timer += delta_time


# Run the main function
main()
