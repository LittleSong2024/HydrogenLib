from inspect import Parameter, Signature
from types import UnionType
from typing import get_origin, Union, get_args, List, Set, Deque, FrozenSet, Sequence, Tuple, Dict, Optional

from .._hycore.type_func import literal_eval


def _match_type(arg, param_type):
    if isinstance(param_type, Parameter):
        param_type = param_type.annotation

    if isinstance(param_type, str):
        param_type = literal_eval(param_type, globals=globals(), locals=locals(), builtins=True, no_eval=False)

    origin = get_origin(param_type)

    if origin is Union:
        types = get_args(param_type)
        matches = [_match_type(arg, t) for t in types]
        return sum(matches) / len(types)

    elif origin in (List, Set, Deque, FrozenSet, Sequence):  # TODO: Not finished
        inner_types = get_args(param_type)
        if not inner_types:
            return 1  # No specific type specified, assume match
        inner_type = inner_types[0]
        if isinstance(arg, origin):  # 如果arg是序列类型之一
            return sum(_match_type(item, inner_type) for item in arg) / len(arg) if arg else 1
        else:
            return 0

    elif origin is Tuple:
        inner_types = get_args(param_type)
        if not inner_types:
            return 1  # No specific type specified, assume match
        if isinstance(arg, tuple):  # 如果arg是元组
            return sum(_match_type(item, inner_type) for item, inner_type in zip(arg, inner_types)) / len(
                arg) if arg else 1
        else:
            return 0

    elif origin is Dict:
        kt, vt = get_args(param_type)
        if isinstance(arg, dict):  # 如果arg是字典
            return sum(
                (_match_type(v, vt) + _match_type(k, kt)) / 2
                for k, v in arg.items()) / len(arg) if arg else 1
        else:
            return 0
    else:
        return 1 if isinstance(arg, param_type) else 0


def _get_match_degree(signature: Signature, args, kwargs, instance_method=False):
    match_degrees = 0
    # print(args, kwargs)
    try:
        bound_args = signature.bind(*args, **kwargs)
    except TypeError as e:
        # print('Bind Error:', e, "signature:", signature)
        return 0

    for index, (param_name, arg) in enumerate(bound_args.arguments.items()):
        if instance_method and index == 0:
            continue
        param = signature.parameters[param_name]
        match_degrees += _match_type(arg, param.annotation)

    length = len(bound_args.arguments) - int(bool(instance_method))

    # print("Match Degrees:", match_degrees, "Length:", length)

    return match_degrees / length if match_degrees else 0  # 匹配程度


def count_possible_types(type_hint):
    # if type_hint is type:
    #     return 1
    # print("Type:", type_hint)
    origin = get_origin(type_hint)

    if origin in (Union, UnionType):
        # 如果是Union类型，递归计算每个成员的可能类型数量
        return sum(count_possible_types(arg) for arg in get_args(type_hint))
    elif origin is List:
        # 如果是List类型，递归计算元素类型的可能类型数量
        element_type = get_args(type_hint)[0]
        return count_possible_types(element_type)
    elif origin is Tuple:
        # 如果是Tuple类型，递归计算每个元素类型的可能类型数量
        return sum(count_possible_types(arg) for arg in get_args(type_hint))
    elif origin is Optional:
        # 如果是Optional类型，递归计算内部类型的可能类型数量，并加上None
        return count_possible_types(get_args(type_hint)[0]) + 1
    else:
        # 基本类型或其他类型，返回1
        return 1
