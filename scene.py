
class Scene:
    """Holds all objects loaded in the application
    """
    def __init__(self, name):
        self.name = name
        self.camera = None
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)
   