from . import get_attr_by_path as getattr, set_attr_by_path as setattr, del_attr_by_path as delattr
import enum as _enum
from typing import Callable, Any, Self


class aliasmode(int, _enum.Enum):
    read = 0
    write = 1
    read_write = 2


class alias:
    """
    声明属性别名
    """
    mode = aliasmode

    def __init__(self, attr_path, mode=aliasmode.read, classvar_enabled=False):
        self.path = str(attr_path)
        self.mode = mode
        self.cve = classvar_enabled

    def __str__(self):
        return self.path

    def __class_getitem__(cls, item) -> 'alias':
        return cls(item)

    def __getitem__(self, item):
        self.path += '.' + item
        return self

    def __call__(self, *, mode=None, classvar_enabled=None) -> Self:
        if mode is not None:
            self.mode = mode
        if classvar_enabled is not None:
            self.cve = classvar_enabled

        return self

    def __get__(self, instance, owner):
        if instance is None:
            if self.cve:
                instance = owner
            else:
                return self
        if self.mode in {aliasmode.read_write, aliasmode.read}:
            return getattr(instance, self.path)
        raise PermissionError("Can't read alias")

    def __set__(self, instance, value):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            setattr(instance, self.path, value)
            return
        raise PermissionError("Can't write alias")

    def __delete__(self, instance):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            delattr(instance, self.path)
        raise PermissionError("Can't delete alias")
