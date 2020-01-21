from component import Component

class ObjectBehaviour(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.awake()

    def awake(self):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass

    def on_pre_render(self):
        pass

    def on_render(self):
        pass

    def on_destroy(self):
        pass
