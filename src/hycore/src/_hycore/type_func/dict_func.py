def is_sub_dict(dic1, dic2):
    # dic1 in dic2
    if tuple(dic1) <= tuple(dic2):
        for i in dic1:
            if i not in dic2 or dic1[i] != dic2[i]:
                return False
        return True
    else:
        return False


def is_parent_dict(dic1, dic2):
    # dic2 in dic1
    return is_sub_dict(dic2, dic1)


def is_key_sub(dic1, dic2):
    return tuple(dic1) <= tuple(dic2)


def is_key_parent(dic1, dic2):
    return tuple(dic2) <= tuple(dic1)


def dict_update(dic1, dic2):
    # update 将dic2 的值更新到 dic1
    for i in dic2:
        dic1[i] = dic2[i]
    return dic1


def dict_eupdate(dic1, dic2):
    for i in dic2:
        if i not in dic1:
            dic1[i] = dic2[i]
    return dic1


def dict_sort(dic1, dic2):
    """
    将dic1和dic2的键修改至相同（key），返回dic1
    当dic1.keys() == dic2.keys()，字典不会发生任何更改
    """
    # 将两部字典的键修改至相同
    for i in dic1:
        if i not in dic2:
            dic2[i] = dic1[i]
    for i in dic2:
        if i not in dic1:
            dic1[i] = dic2[i]
    return dic1


def get_pairs_by_value(dic, value, reverse=False):
    """
    通过值获取所以符合的键值对，结果以字符排序（默认升序），可以通过reverse参数控制

    :param dic: a dict type object
    :param value: a value of dict
    :param reverse: 控制升序降序，对于sort/sorted中的reverse参数
    """
    pairs = [(k, v) for k, v in dic._instances() if v == value]
    return sorted(pairs, key=lambda x: x[0], reverse=reverse)


class AttrDict:
    def __init__(self, **kwargs):
        object.__setattr__(self, "_dict", kwargs)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    @property
    def get_dict(self):
        return self._dict


from types import MappingProxyType


class ConstDict:
    def __init__(self, initial_dict=None):
        if initial_dict is None:
            initial_dict = {}
        self._data = MappingProxyType(initial_dict)

    def __getitem__(self, key):
        return self._data[key]

    def get(self, key, *, default=None):
        return self._data.get(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __repr__(self):
        return f"ConstDict({self._data})"
