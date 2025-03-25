from __future__ import annotations

import builtins
from typing import Any, Protocol, runtime_checkable

from ..abc.types import ConfigTypeBase
from ..._hycore.utils import InstanceDict


@runtime_checkable
class Item(Protocol):
    value: ConfigItemInstance
    key_instance: Any


class ConfigItemInstance:
    def __init__(self, type: ConfigTypeBase, attr, key, default, parent: 'ConfigItem' = None):
        self.key, self.attr = key, attr
        self.type = type
        self._value = None
        self.default = default

        self.parent = parent

    def sync(self):
        self.key, self.attr, self.type, self.default = (
            self.parent.key, self.parent.attr, self.parent.type, self.parent.default)

    def set(self, value):
        self.validate(value, error=True)
        self._value = value

    def validate(self, value, error=False):
        res = self.type.validate(value)
        if not res and error:
            raise TypeError(f"{type(value)} is not a valid type")
        return res

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.set(value)


class ConfigItem:
    def __init__(self, type: type | ConfigTypeBase, default: Any, *, key = None):
        self.default = default

        self.attr = None
        self.key = key

        if isinstance(type, ConfigTypeBase):
            self.type = type
        else:
            self.type = type()

        self.validate(default)

        if not isinstance(type, builtins.type):
            raise TypeError("type must be a ItemType")

        self._instances = InstanceDict()

    def validate(self, value):
        if not self.type.validate(value):
            raise TypeError(f"{type(value)} is not a valid type")

    def _get_instance(self, ins) -> Item:
        if ins not in self._instances:
            self._instances[ins] = ConfigItemInstance(self.type, self.attr, self.key, self.default, self)
        return self._instances[ins]

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._get_instance(instance).value.value

    def __set__(self, instance, value):
        item = self._get_instance(instance).value  # dict_item.value
        old, new = item.value, value

        item.set(value)
        instance.on_change(self.attr, old, new)

    def from_instance(self, instance) -> 'ConfigItemInstance':
        item_instance = self._get_instance(instance).value
        return item_instance
