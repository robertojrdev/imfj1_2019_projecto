# Introdução à Matemática e Física Para Videojogos I - Final Project

### PyEngine
Roberto Gomes
a21700491

![alt text](https://github.com/robertojrdev/imfj1_2019_projecto/raw/master/Screenshot/title.png "Sample application")

This is the result of the final project for "Introdução à Matemática e Física Para Videojogos I" course, on the [Licenciatura em Videojogos][lv] da
[Universidade Lusófona de Humanidades e Tecnologias][ULHT] in Lisbon.

The engine was built using:
* Python 3.6
* Pygame (https://www.pygame.org/news)
* Numpy (https://numpy.org/devdocs/user/quickstart.html)
* Numpy-quaternion (https://pypi.org/project/numpy-quaternion/)

There is a sample application that can be run by using:
`py.exe main.py` or `python main.py` or `python3.6 main.py`, depending on your Python installation.
 
## Assignment

In short, the assignment for the course is as follows:
* Build a "Viewer" application. That application has to feature the following functionality:
  - Display a 3d object. Control of the visualization has to be done using keys.
  - Create a model other than a cube for this display.
* Build a "FPS-like" application.
  - Create an environment where the player can roam using standard FPS controls.
  - Implement backface culling.
  - Implement filled geometry, replacing the wireframe
  - Stop objects that are behind the camera from being renderered
  - Implement very simple point lighting.
  - Implement shading based on the light.
      
## Results

All requirements were fulfilled and the project was successfully completed. The base goals served well for a better understanding of the mathematical concepts involved, mainly matrices transformations and quaternion usage.

To complete this work I based in Unity Engine structure to create a similar workflow, utilizing concepts of GameObjects, Transforms, Components, Scenes, MonoBehaviour, and coroutines. Even though these concepts were very simplified the idea is there.

## Structure

The core of the engine is the application.py script, the main loop is here. It needs to be initialized from outside. When it is done it will start pygame and make sure everything is ready to start. You can pass a scene file to be started, it's not necessary though and can be made later on.
After that the loop must be started, it is done manually by calling run().

At this point, the engine is running (or should be...) and a Scene to hold all game objects is created.

There are two different concepts of scenes. One refer to the file containing all game objects to be loaded and their scripts, you can load multiple of them at the same time, their objects will simply be added to the game. The other is the application scene which will hold all game objects instantiated, the application can have only one of this.

The GameObjects have a Transform and are basically containers of Components. You cannot instantiate them if the application is not running, and once you instantiate them they will be added to the application scene automatically.

At the main loop the there are a few stages:
 * Uptade Inputs
 * Update
 * On Pre Render
 * On Render
 * Flip Render Buffer
 * Delta Time

These stages control the flow of the application and Behaviour Objects respond to them. Every Object Behaviour added to objects in the application scene will receive Update, OnPreRender, and OnRender messages.

ObjectBehaviour is how scripts are added to GameObjects adding behavior to them. you must simply create a class that derives from ObjectBehaviour and override the message functions to do it. Most of the time it will be the Update.

To start rendering things on the screen you must have a Camera, it is a Component, and must be attached to a GameObject. The application scene can have multiple cameras, but only one of them will render to screen. Every time you add a new camera to the scene it will become the new active camera.

To display an object in 3D you must have a MeshRenderer in the GameObject, and add a Mesh to it by importing a .obj file or creating a primitive, both using the Mesh class.

Without any light source the screen will be black, so you must add them to the scene. You do it by adding a PointLight to a GameObject.

To use keyboard or mouse inputs you must use Input class, it is updated every frame and has functions to check the state of the keys.



## Installation of required modules

To run the sample application, you'll have to install all the used modules:

* `pip install pygame`
* `pip install numpy`
* `pip install numpy-quaternion`

Although not needed, to avoid some warnings on application startup, you can install two additional modules:

* `pip install numba`
* `pip install scipy`

If pip is not available on the command line, you can try to invoke it through the module interface on Python:

* `python -m pip install <name of package>`

There might be some issues with installing numpy and numpy-quaternion, due to a C compiler not being available in the path.
If that happens, you can try download a binary version of the library (called a wheel) and install it manually.

You can download the wheels for Numpy from `https://pypi.org/project/numpy/#files`. Choose the appropriate version for your OS and Python version (cp36 for Python 3.6, cp37 for Python 3.7, etc). For example, 64-bit Windows 10 for Python 3.6 is the file `numpy-1.17.4-cp35-cp35m-win_amd64.whl`.

For numpy-quaternion, you can get the files from `https://www.lfd.uci.edu/~gohlke/pythonlibs/`. Same naming scheme is used, so the file for 64-bit Windows 10 for Python 3.6 is the file `numpy_quaternion‑2019.12.12‑cp36‑cp36m‑win_amd64.whl`.

To install a wheel manually, you just have to run the command: `pip install <wheel name>` or `python -m pip install <wheel name>` from the directory where the wheel was downloaded to.

## Licenses

All code in this repo is made available through the [GPLv3] license.
The text and all the other files are made available through the 
[CC BY-NC-SA 4.0] license.

## Metadata

* Autor: [Roberto Gomes][]
* Modified document from: [original][]

[Roberto Gomes]:https://github.com/robertojrdev
[original]:https://github.com/VideojogosLusofona/imfj1_2019_projecto
[GPLv3]:https://www.gnu.org/licenses/gpl-3.0.en.html
[CC BY-NC-SA 4.0]:https://creativecommons.org/licenses/by-nc-sa/4.0/