from typing import Any, Union
from collections import UserDict
import weakref


class IDict_Item:
    def __init__(self, ins, value, parent: 'InstanceDict' = None):
        self.ins = ins
        self._value = weakref.proxy(value, self.delete)
        self.parent = parent

    def delete(self, object):
        self.parent.delete(object)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = weakref.proxy(value, self.delete)


class InstanceDict(UserDict):
    def __init__(self, dct=None):
        super().__init__()
        if dct:
            for k, v in dct._instances():
                self._set(k, v)

    def _to_key(self, value):
        return id(value)

    def _get(self, key):
        return super().__getitem__(key)

    def _set(self, key, value):
        super().__setitem__(id(key), IDict_Item(key, value))

    def get(self, k, id_key=False, default=None, item=False) -> Union[IDict_Item, Any]:
        if not id_key:  # 如果 k 不作为 id 传入
            k = self._to_key(k)

        if k not in self:  # 如果 k 不位于字典中
            return default  # 返回默认值

        if item:  # 返回 IDict_Item
            return self._get(k)
        else:  # 返回 value
            return self._get(k).value

    def set(self, k, v):
        self._set(k, v)

    def delete(self, key):
        del self[self._to_key(key)]

    def pop(self, key, id_key=False):
        if not id_key:
            key = self._to_key(key)

        return super().pop(key)

    def __getitem__(self, key):
        return self._get(self._to_key(key))

    def __setitem__(self, key, value):
        self._set(key, value)

    def __delitem__(self, key):
        super().__delitem__(self._to_key(key))
        
    def __contains__(self, item):
        return super().__contains__(self._to_key(item))
