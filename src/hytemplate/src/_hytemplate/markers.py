from .abstract import AbstractMarker, generate
from .._hycore.type_func import get_attr_by_path, set_attr_by_path


class Attribute(AbstractMarker):
    def __init__(self, attr, obj=None):
        self.attr_path = attr
        self.obj = obj

    def generate(self, countainer, **kwargs):
        obj = generate(self.obj or countainer, countainer, **kwargs)
        return get_attr_by_path(obj, self.attr_path)

    def restore(self, countainer, value, **kwargs):
        obj = generate(self.obj or countainer, countainer, **kwargs)
        set_attr_by_path(obj, self.attr_path, value)


class KWValue(AbstractMarker):
    def __init__(self, kwarg_name):
        self.kwarg_name = kwarg_name

    def generate(self, countainer, **kwargs):
        return kwargs[self.kwarg_name]


class StaticCall(AbstractMarker):
    """
    Call function with given arguments and kwargs
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def generate(self, countainer, **kwargs):
        return self.func(*self.args, **self.kwargs)


class DynamicCall(AbstractMarker):
    """
    Call function with given arguments and kwargs, but the function, arguments and kwargs can be dynamic
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def generate(self, countainer, **kwargs):
        func = generate(self.func, countainer, **kwargs)
        args = (generate(i, countainer, **kwargs)
                for i in self.args)
        kwargs = {k: generate(v, countainer, **kwargs)
                  for k, v in self.kwargs.items()}
        return func(*args, **kwargs)



