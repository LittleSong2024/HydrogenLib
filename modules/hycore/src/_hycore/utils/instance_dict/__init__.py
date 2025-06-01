import weakref
from collections import UserDict
from typing import Any

from .events import *


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

    def to_key(self, value):
        return id(value)

    def _get(self, key) -> InstanceDictItem:
        return super().__getitem__(key)

    def _set(self, key, value) -> None:
        #
        super().__setitem__(key, InstanceDictItem(key, value, self))

    def _pop(self, key):
        return super().pop(key)

    def _delete(self, key) -> None:
        super().__delitem__(key)

    def get(self, k, id=False, default=None) -> Any:
        """
        从 实例字典 中获取值
        :param k: 键
        :param id: 传入的 k 参数是否是一个 id 值
        :param default: 返回的默认值
        """
        if not id:  # 如果 k 不作为 id 传入
            k = self.to_key(k)  # 转换为 id

        if k not in self:  # 如果 k 不位于字典中
            return default  # 返回默认值

        value = self._get(k)

        event = GetEvent(value.key, value.value)
        self.get_event(event)

        return event.result  # 找到项, 返回字典值

    def set(self, k, v, id=False):
        """
        设置 实例字典 的值
        :param k: 键
        :param v: 值
        :param id: 传入的是否是一个 id 值
        """
        if not id:
            k = self.to_key(k)

        self.set_event(  # 触发事件
            SetEvent(super().get(k, None), v))

        self._set(self.to_key(k), v)

    def delete(self, key, id=False):
        """
        删除一个 实例字典 项
        :param key: 键
        :param id: 传入的键是否是一个 id 值
        """
        if not id:
            key = self.to_key(key)

        self._delete(key)

    def pop(self, key, id=False):
        """
        弹出一个 实例字典 项
        :param key: 键
        :param id: 传入的键是否是一个 id 值
        :return: Any
        """
        if not id:
            key_id = self.to_key(key)

        self.delete_event(DeleteEvent(key, self._get(key_id)))

        return self._pop(key_id)

    def __getitem__(self, key):
        return self._get(self.to_key(key)).value

    def __setitem__(self, key, value):
        self._set(key, value)

    def __delitem__(self, key):
        super().__delitem__(self.to_key(key))

    def __contains__(self, item):
        return super().__contains__(self.to_key(item))

    def __iter__(self):
        for v in super().values():
            yield v.key, v.value

    # 拓展

    def delete_event(self, e: DeleteEvent):
        ...

    def set_event(self, e: SetEvent):
        ...

    def get_event(self, e: GetEvent):
        ...
