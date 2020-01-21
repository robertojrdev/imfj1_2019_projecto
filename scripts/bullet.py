from engine import ObjectBehaviour, MeshRenderer, Mesh, Material, color

class Bullet(ObjectBehaviour):
    """ Create a 0.1f size cube and move it forward indefintally
    """
    def awake(self):
        renderer = self.game_object.add_component(MeshRenderer)
        renderer.mesh = Mesh.create_cube((0.1,0.1,0.1))
        renderer.material = Material(color(0,0,1,1), "TestMaterial1")

    def update(self, delta_time):
        self.transform.position = self.transform.position + self.transform.forward * delta_time * 20