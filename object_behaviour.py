from component import Component

class ObjectBehaviour(Component):
    """ObjectBehaviour is the base class from which every PyEngine script derives.\n
    You can override all of its methods but not the constructor(__init__), instead use awake()
    """
    def __init__(self, game_object):
        super().__init__(game_object)
        self.awake()

    def awake(self):
        """Called when the object is created
        """
        pass

    def start(self):
        """TODO
        """
        pass

    def update(self, delta_time):
        """Called every frame
        
        Arguments:
            delta_time {float} -- time since the last update
        """
        pass

    def on_pre_render(self):
        """Called right before the render
        """
        pass

    def on_render(self):
        """Called during the render
        """
        pass

    def on_destroy(self):
        """TODO
        """
        pass
