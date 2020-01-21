import traceback
import time
import pygame
from scene import Scene
from triangle import Triangle
from input import Input

class Application:
    """Runs the application
    """
    screen = None
    scene = None
    triangles_buffer = []
    lights_buffer = []

    @staticmethod
    def init(scene, res_x = 640, res_y = 480):
        """Initialize application
        
        Arguments:
            scene {string} -- scene name, the scene must be in the subfolder scenes and the string passed here should not contain ".py"
        
        Keyword Arguments:
            res_x {int} -- screen width (default: {640})
            res_y {int} -- screen height (default: {480})
        """
        # Initialize pygame, with the default parameters
        pygame.init()

        # Create a window and a display surface
        Application.screen = pygame.display.set_mode((res_x, res_y))

        # Set scene
        Application.load_scene(scene)

    @staticmethod
    def load_scene(scene):
        """Run a python script which instantiate objects
        it does not unload previous scenes, instead load the new scene on top, it means you can use it to load packs of objects
        
        Arguments:
            scene {string} -- scene name, the scene must be in the subfolder scenes and the string passed here should not contain ".py" 
        """
        Application.scene = Scene(scene)
        exec(open("scenes/" + scene + ".py").read())
        
    @staticmethod
    def add_triangle_to_buffer(triangle):
        """Add triangles triangles to be rendered in this frame,
        the buffer is cleared after update is called
        
        Arguments:
            triangle {Triangle} -- Triangle to be rendered
        """
        if(isinstance(triangle, list)):
            Application.triangles_buffer.extend(triangle)
        elif(isinstance(triangle, Triangle)):
            Application.triangles_buffer.append(triangle)

    @staticmethod
    def run():
        """Start application loop
        """

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
                    try:
                        c.update(delta_time)
                    except Exception:
                        traceback.print_exc(10)

            # Call on_pre_render
            for o in Application.scene.objects:
                for c in o.components:
                    try:
                        c.on_pre_render()
                    except Exception:
                        traceback.print_exc(10)

            # Call on_render
            for o in Application.scene.objects:
                for c in o.components:
                    try:
                        c.on_render()
                    except Exception:
                        traceback.print_exc(10)

            Application.triangles_buffer.clear()

            # Render Scene
            # Application.scene.render()

            # Swaps the back and front buffer, effectively displaying what we rendered
            pygame.display.flip()

            # Updates the timer, so we we know how long has it been since the last frame
            delta_time = time.time() - prev_time
            prev_time = time.time()

            pygame.display.set_caption("Ganda game - fps: " + str(int(1/delta_time)))