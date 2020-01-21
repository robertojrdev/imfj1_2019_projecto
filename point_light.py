from object_behaviour import ObjectBehaviour
from application import Application
from vector3 import vector3
from mathf import inverse_lerp

class PointLight(ObjectBehaviour):
    def awake(self):
        self.range = 5
        self.intensity = 1
        Application.lights_buffer.append(self)

    def calculate_intensity(self, position, normal):
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
