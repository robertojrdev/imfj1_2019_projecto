
class Component:
    """Base class for everything attached to GameObjects.
    """
    def __init__(self, game_object):
        self.game_object = game_object
        self.transform = self.game_object.transform
