import weakref
from collections import UserDict
from typing import Any, Union


class InstanceDictItem:
    def __init__(self, key_instance, value, parent: 'InstanceDict' = None):
        self.key_weakref = weakref.proxy(key_instance, self.delete_callback)
        self.value = value
        self.parent = parent

    @property
    def key(self):
        return self.key_weakref()

    def delete_callback(self, object):
        self.parent.delete(object)


class InstanceDict(UserDict):
    def __init__(self, dct=None):
        super().__init__()
        if isinstance(dct, InstanceDict):
            for k, v in dct.items():
                self._set(k, v)

    def _to_key(self, value):
        return id(value)

    def _get(self, key):
        return super().__getitem__(key)

    def _set(self, key, value):
        super().__setitem__(self._to_key(key), InstanceDictItem(key, value, self))

    def get(self, k, id_key=False, default=None) -> Union[InstanceDictItem, Any]:
        if not id_key:  # 如果 k 不作为 id 传入
            k = self._to_key(k)

        if k not in self:  # 如果 k 不位于字典中
            return default  # 返回默认值

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
        return self._get(self._to_key(key)).value

    def __setitem__(self, key, value):
        self._set(key, value)

    def __delitem__(self, key):
        super().__delitem__(self._to_key(key))

    def __contains__(self, item):
        return super().__contains__(self._to_key(item))

    def __iter__(self):
        for v in super().values():
            yield v.key, v.value
