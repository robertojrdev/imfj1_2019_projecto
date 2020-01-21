from transform import Transform
from application import Application
from component import Component

class GameObject():
    def __init__(self, name = "Object"):
        self.name = name
        self.transform = None
        self.components = []
        self.transform = Transform(self)
        Application.scene.add_object(self)

    def add_component(self, comp):
        if(issubclass(comp, Component) == False):
            print("THIS IS NOT A COMPONENT")
            return
            
        newComp = comp(self)
        self.components.append(newComp)
        return newComp

    def get_component(self, comp):
        for o in self.components:
            if issubclass(type(o), comp):
                return o
        return
