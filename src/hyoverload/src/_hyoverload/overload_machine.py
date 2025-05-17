from .type_checker import MultiSignatureMatcher
from .._hycore.type_func import Function
from .._hycore.utils import InstanceDict


# @Descriptor
class OverloadMachine:
    def __init__(self):
        self.multi_matcher = MultiSignatureMatcher([])
        self.mapping = InstanceDict()

    def overload(self, __func):
        func = Function(__func)
        matcher = self.multi_matcher.add(func.signature)
        self.mapping[matcher] = func

    def call(self, args, kwargs):
        best_matcher = self.multi_matcher.match((self, ) + args, kwargs)[0]
        func = self.mapping[best_matcher]
        return func(*args, **kwargs)

    def __get__(self, instance, owner):
        return lambda *args, **kwargs: self.call(args, kwargs)


