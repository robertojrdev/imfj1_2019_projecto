from object_behaviour import ObjectBehaviour
from application import Application
from vector3 import vector3
from mathf import inverse_lerp

class PointLight(ObjectBehaviour):
    """A simple point light, has only range and intensity
    """
    def awake(self):
        self.range = 5
        self.intensity = 1
        Application.lights_buffer.append(self)

    def calculate_intensity(self, position, normal):
        """Calculate light intensity on a surface
        
        Arguments:
            position {vector3} -- [point position]
            normal {vector3} -- [surface normal]
        
        Returns:
            [float] -- [value from 0 - 1]
        """

        direction = self.transform.position - position
        dist = direction.magnitude()
        if(dist > self.range):
            return 0

        intensity = vector3.dot_product(normal.normalized(), direction.normalized())
        intensity *= inverse_lerp(self.range, 0, dist)

        if(intensity < 0):
            return 0
        else: 
            return intensity
