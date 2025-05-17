from inspect import BoundArguments


class Temp:
    def __init__(self):
        self._tmp = {}

    def update(self, args: BoundArguments, value):
        self._tmp[args] = value

    def check(self, args: BoundArguments):
        return args in self._tmp

    def get(self, args: BoundArguments):
        return self._tmp[args]
