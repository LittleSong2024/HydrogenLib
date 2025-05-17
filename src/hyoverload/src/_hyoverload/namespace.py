from .._hycore.data_structures import Heap

overloads = {}  # type: dict[str, Heap]
overload_temp = {}  # type: dict[str, dict[tuple[type, ...], 'OverloadFunctionCallable']]
overload_funcs = {}  # type: dict[str, 'OverloadFunctionCallable']


def _register_overload(function_callable):
    name = function_callable.qualname
    if name not in overload_funcs:
        overload_funcs[name] = function_callable
    return _get_registered(name)


def _get_registered(qualname):
    return overload_funcs[qualname]


def _add_to_temp(qualname, types):
    if qualname not in overload_temp:
        overload_temp[qualname] = dict()
    overload_temp[qualname][types] = _get_registered(qualname)


def _check_temp(qualname, args):
    if qualname not in overload_temp:
        return False

    for types in overload_temp[qualname]:
        if len(types) != len(args):
            continue
        for arg, type_ in zip(args, types):
            if not isinstance(arg, type_):
                return False


def get_func_overloads(func):
    return overloads[func.qualname]
