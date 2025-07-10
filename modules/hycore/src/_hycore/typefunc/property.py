from . import get_attr_by_path as _gabp, set_attr_by_path as _sabp, del_attr_by_path as _dabp
import enum as _enum
from typing import Callable, Any


class aliasmode(int, _enum.Enum):
    read = 0
    write = 1
    read_write = 2


class alias:
    mode = aliasmode

    def __init__(self, attr_path, mode=aliasmode.read, classvar_enabled=False):
        self.path = attr_path
        self.mode = mode
        self.cve = classvar_enabled

        self._get = lambda self, x: x
        self._set = lambda self, v: v
        self._del = lambda self: None

    def getter(self, fnc: Callable[[Any, Any], Any]):
        self._get = fnc

    def setter(self, fnc: Callable[[Any, Any], Any]):
        self._set = fnc

    def deleter(self, fnc: Callable[[Any], Any]):
        self._del = fnc

    def __get__(self, instance, owner):
        if instance is None:
            if self.cve:
                instance = owner
            else:
                return self
        if self.mode in {aliasmode.read_write, aliasmode.read}:
            return self._get(instance, _gabp(instance, self.path))
        raise PermissionError("Can't read alias")

    def __set__(self, instance, value):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            _sabp(instance, self.path, self._set(instance, value))
            return  # 抽象,没加return
        raise PermissionError("Can't write alias")

    def __delete__(self, instance):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            self._del(instance)
            _dabp(instance, self.path)
        raise PermissionError("Can't delete alias")
