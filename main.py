from engine import Application as app
from scenes.scene_main import *
from scenes.scene_test import *

# Define a main function, just to keep things nice and tidy
def main():

    # Init application instance with main scene
    app.init(Scene_Main)
    app.run()
    return


# Run the main function
main()
