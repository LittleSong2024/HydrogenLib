from __future__ import annotations

import builtins
from typing import Protocol, runtime_checkable

from ..abc.types import ConfigTypeBase
from ..._hycore.better_descriptor import *


@runtime_checkable
class Item(Protocol):
    value: ConfigItemInstance
    key_instance: Any


class ConfigItemInstance(BetterDescriptorInstance):
    key: str
    attr: str
    type: ConfigTypeBase
    default: Any

    _value = None

    def __init__(self, parent: 'ConfigItem' = None):
        super().__init__()
        self.parent = parent
        self.sync()

    def sync(self):
        self.key, self.type, self.default = (
            self.parent.key, self.parent.type, self.parent.default)

    def set(self, v):
        self.validate(v, error=True)
        self._value = v

    def validate(self, v, error=False):
        res = self.type.validate(v)
        if not res and error:
            raise TypeError(f"{type(v)} is not a valid type")
        return res

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.set(value)

    def __better_get__(self, instance, owner, parent) -> Any:
        return self.value

    def __better_set__(self, instance, value, parent):
        self.set(value)

    def __better_del__(self, instance, parent):
        self.value = self.default


class ConfigItem(BetterDescriptor, type=ConfigItemInstance):
    def __init__(self, type: type | ConfigTypeBase, default: Any, *, key=None):
        super().__init__()
        self.default = default
        self.key = key

        if isinstance(type, ConfigTypeBase):
            self.type = type
        else:
            self.type = type()

        if not self.type.validate(default):
            raise TypeError("default value is not a valid type")

        if not isinstance(type, builtins.type):
            raise TypeError("type must be a ItemType")

    def __better_new__(self) -> "BetterDescriptorInstance":
        return ConfigItemInstance(self)

    def from_instance(self, instance) -> ConfigItemInstance:
        return self.get_instance_by_instance(instance)
