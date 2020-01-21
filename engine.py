#the scripts can import entire engine or it's classes through here like "from engine import color, vector3, component...."

import pygame
from color import color
from vector3 import vector3
from component import Component
from transform import Transform
from object_behaviour import ObjectBehaviour
from game_object import GameObject
from application import Application
from scene import Scene
from triangle import Triangle
from input import Input
from key import Key
from mesh_renderer import MeshRenderer
from mesh import Mesh
from material import Material
from camera import Camera
from point_light import PointLight
from quaternion import *