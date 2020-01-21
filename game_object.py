from transform import Transform
from application import Application
from component import Component

class GameObject():
    """Base class for all entities in the scenes
    """
    def __init__(self, name = "Object"):
        self.name = name
        self.transform = None
        self.components = []
        self.transform = Transform(self)
        Application.scene.add_object(self) #On create object it will be automatically added to the active scene

    def add_component(self, comp):
        """Add a component to the GameObject
        
        Arguments:
            comp {Component} -- The component to be added

        Returns:
            Component -- return the same component added
        """
        if(issubclass(comp, Component) == False):
            print("THIS IS NOT A COMPONENT")
            return
            
        newComp = comp(self)
        self.components.append(newComp)
        return newComp

    def get_component(self, comp):
        """Search for a component of type
        
        Arguments:
            comp {Component} -- Type
        
        Returns:
            if a component is found it will be returned, otherwise return null
        """
        for o in self.components:
            if issubclass(type(o), comp):
                return o
        return
