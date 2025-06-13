import inspect
import types

from .markers import DictTemplateMarker
from .basic_methods import *


def check_stack():
    frame = inspect.currentframe().f_back
    while (frame := frame.f_back) is not None:
        func_name = frame.f_code.co_name
        func = frame.f_globals.get(func_name, frame.f_locals.get(func_name))
        if isinstance(func, (types.MethodType, )):
            return func.__self__
    return None


class Template:
    """
    顶层模板类型
    储存模版通用数据,提供 API 填充模版
    """
    __root_template_type__ = DictTemplateMarker

    def __init__(self, template, **kwargs):
        self._template = self.__root_template_type__(template)
        self._globals = kwargs

    def fill(self, **kwargs):
        return generate(self._template, GenerationContext(
            root=self, globals=self._globals, arguments=kwargs
        ))

    def restore(self, value, **kwargs):
        return restore(self._template, value, RestorationContext(
            root=self, globals=self._globals, arguments=kwargs
        ))

    def __getattr__(self, item):
        if item in self._globals:
            return self._globals[item]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __init_subclass__(cls, **kwargs):
        rtt = kwargs.get("rtt", cls.__root_template_type__)  # root template type (RTT)
        cls.__root_template_type__ = rtt
