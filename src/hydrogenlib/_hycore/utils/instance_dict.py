from typing import Any, Union
from collections import UserDict


class IDict_Item:
    def __init__(self, ins, value):
        self.ins = ins
        self.value = value


class InstanceDict(UserDict):
    def __init__(self, dct=None):
        super().__init__()
        if dct:
            for k, v in dct._instances():
                self._set(k, v)

    def _get(self, key):
        return super().__getitem__(key)

    def _set(self, key, value):
        super().__setitem__(id(key), IDict_Item(key, value))

    def get(self, k, id_key=False, default=None, item=False) -> Union[IDict_Item, Any]:
        if not id_key:  # 如果 k 不作为 id 传入
            k = id(k)  # 转换为 id

        if k not in self:  # 如果 k 不位于字典中
            return default  # 返回默认值

        if item:  # 返回 IDict_Item
            return self._get(k)
        else:  # 返回 value
            return self._get(k).value

    def set(self, k, v):
        self._set(k, v)

    def delete(self, key):
        del self[id(key)]

    def pop(self, key, id_key=False):
        if not id_key:
            key = id(key)

        return super().pop(key)

    def __getitem__(self, key):
        return self._get(id(key))

    def __setitem__(self, key, value):
        self._set(key, value)

    def __delitem__(self, key):
        super().__delitem__(id(key))
        
    def __contains__(self, item):
        return super().__contains__(id(item))
