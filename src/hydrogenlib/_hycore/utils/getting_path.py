class GettingPath:
    def __init__(self, path):
        if not self.check(path):
            raise ValueError(f"Path {path} is not valid")

        self.path = path

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

    def iter_path(self):
        return self.path

    def touch(self, obj):
        cur = obj
        for next in self.iter_path():
            cur = self.getnext(cur, next)
        return cur
