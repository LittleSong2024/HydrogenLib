from _hycore.typefunc import get_attr_by_path, set_attr_by_path
from .dict_template import DictTemplateMarker
from .list_template import ListTemplate
from ..basic_methods import *


class Attribute(AbstractMarker):
    def __init__(self, attr, obj=None, restorable=True):
        self.attr_path = attr
        self.obj = obj
        self.restorable = restorable

    def generate(self, context):
        obj = self.obj or context.root
        return get_attr_by_path(obj, self.attr_path)

    def restore(self, context: RestorationContext):
        if not self.restorable:
            return
        obj = self.obj or context.root
        set_attr_by_path(obj, self.attr_path, context.value)


class Argument(AbstractMarker):
    def __init__(self, argument):
        self.argument = argument

    def generate(self, context: GenerationContext):
        return context.arguments.get(self.argument)


class StaticCall(AbstractMarker):
    """
    Call function with given arguments and kwargs
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def generate(self, context: GenerationContext):
        return self.func(*self.args, **self.kwargs)


class DynamicCall(AbstractMarker):
    """
    Call function with given arguments and kwargs, but the function, arguments and kwargs can be dynamic
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def generate(self, context: GenerationContext):
        func = generate(self.func, context, parent=self)
        args = (generate(i, context, parent=self)
                for i in self.args)
        kwargs = {k: generate(v, context, parent=self)
                  for k, v in self.kwargs.items()}
        return func(*args, **kwargs)
