from .api_abc import API_ValueItem, transform
from ._hycore.type_func import get_attr_by_path


class Attr(API_ValueItem):
    def __init__(self, path):
        self.path = path

    def generate(self, api, **kwargs):
        return get_attr_by_path(self.path, api)


class Arg(API_ValueItem):
    def __init__(self, name, attr=None):
        self.name = name
        self.attr = attr

    def generate(self, api, **kwargs):
        obj = kwargs[self.name]
        if self.attr:
            return get_attr_by_path(self.attr, obj)
        else:
            return obj


class Call(API_ValueItem):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def generate(self, api, **kwargs):
        func = transform(self.func, api, **kwargs)

        args = []
        for arg in self.args:
            args.append(transform(arg, api, **kwargs))

        kwargs = {}
        for key, value in self.kwargs.items():
            kwargs[key] = transform(value, api, **kwargs)

        return func(*args, **kwargs)


class Format(API_ValueItem):
    def __init__(self, fmt, *args, **kwars):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwars

    def generate(self, api, **kwargs):
        fmt = transform(self.fmt, api, **kwargs)

        args = []
        for arg in self.args:
            args.append(transform(arg, api, **kwargs))

        kwargs = {}
        for key, value in self.kwargs.items():
            kwargs[key] = transform(value, api, **kwargs)

        return fmt.format(*args, **kwargs)


