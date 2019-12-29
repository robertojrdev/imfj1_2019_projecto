from engine import *

class Cube(ObjectBehaviour):
    def awake(self):
        self.counter = 0

    def update(self, delta_time, input):
        self.counter += delta_time
        if input.get_key(pygame.K_SPACE):
            self.counter += delta_time
            x = math.sin(self.counter)
            y = math.cos(self.counter * .5)
            z = 5 + math.cos(self.counter)
            self.transform.position = vector3(x,y,z)
            self.transform.rotation = self.transform.rotation * from_rotation_vector((0,math.radians(20 * delta_time),0))
            self.transform.rotation = self.transform.rotation * from_rotation_vector((math.radians(20 * delta_time),0,0))

