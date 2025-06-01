class GettingPath:
    def __init__(self, path):
        if not self.check(path):
            raise ValueError(f"Path {path} is not valid")

        self.path = path

    @property
    def parent(self):
        """
        Get parent object
        """
        return GettingPath(self.path[:-1])

    @property
    def name(self):
        """
        Get name of object
        """
        return self.path[-1]

    def check(self, path):
        """
        Check if path is valid
        """
        return True

    def getnext(self, current, next):
        """
        Get next object from current object
        """
        return getattr(current, next)

    def setnext(self, current, next, value):
        """
        Set next object from current object
        """
        setattr(current, next, value)

    def iter_path(self):
        return self.path

    def touch(self, obj):
        cur = obj
        for next in self.iter_path():
            cur = self.getnext(cur, next)
        return cur

    def set(self, obj):
        cur = obj
        for next in self.iter_path()[:-1:]:
            cur = self.getnext(cur, next)
        self.setnext(cur, self.iter_path()[-1], obj)
