from _hyconfig.abc import AbstractModel
from _hycore.typefunc import alias


class ManagerBase:
    default: object

    def __init__(self):
        self.__data__ = {}

    def __setattr__(self, name, value):
        if isinstance(value, AbstractModel):
            self.__data__[name] = value
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        return self.__data__.get(name, self.default)

    def get(self, name):
        return self.__data__.get(name, self.default)

    def set(self, name, value):
        self.__data__[name] = value


class ModelManager(ManagerBase):
    models = alias['__data__'](mode=alias.mode.read_write)


class BackendManager(ManagerBase):
    backends = alias['__data__'](mode=alias.mode.read_write)

