import sys

from .namespace import _register_overload, overloads
from .overload_function import OverloadFunction
from .._hycore.data_structures import Heap


# TODO: 完成模块


def _get_module_globals(module_name):
    try:
        module = sys.modules[module_name]
        return module.__dict__
    except KeyError:
        return {}


def overload(func):
    func = OverloadFunction(func)
    if func.qualname in overloads:
        overloads[func.qualname].append(func)
    else:
        overloads[func.qualname] = Heap([func], True)

    return _register_overload(func).callable


