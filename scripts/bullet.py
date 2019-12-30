from engine import *

class Bullet(ObjectBehaviour):
    def awake(self):
        renderer = self.game_object.add_component(MeshRenderer)
        renderer.mesh = Mesh.create_cube((1,1,1))
        renderer.material = Material(color(0,0,1,1), "TestMaterial1")

    def update(self, delta_time):
        self.transform.position = self.transform.position + self.transform.forward * delta_time * 20