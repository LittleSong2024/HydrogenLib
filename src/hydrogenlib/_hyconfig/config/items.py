from __future__ import annotations
import builtins
from typing import Any, Protocol, runtime_checkable

from ..abc.types import ConfigType
from ..._hycore.utils import InstanceDict


@runtime_checkable
class IDict_Item(Protocol):
    value: ConfigItemInstance
    ins: Any


class ConfigItemInstance:
    def __init__(self, type, attr, key, default, parent: 'ConfigItem' = None):
        self.key, self.attr = key, attr
        self.type = type
        self.default = default
        self.instance = type(default)

        self.parent = parent

    def sync(self):
        self.key, self.attr, self.type, self.default = (
            self.parent.key, self.parent.attr, self.parent.type, self.parent.default)

    def set(self, value):
        self.instance.set(value)

    def get(self):
        return self.instance.get()

    def validate(self, value, error=False):
        res = self.type.validate(value)
        if not res and error:
            raise TypeError(f"{type(value)} is not a valid type")
        return res

    @property
    def value(self):
        return self.get()


class ConfigItem:
    def __init__(self, key, *, type: type[ConfigType], default: Any):
        self.type = type
        self.default = default

        self.attr = None
        self.key = key

        self.validate(default)

        if not isinstance(type, builtins.type):
            raise TypeError("type must be a ItemType")

        self._instances = InstanceDict()

    def validate(self, value):
        if not self.type.validate(value):
            raise TypeError(f"{type(value)} is not a valid type")

    def _instance(self, ins) -> IDict_Item:
        if ins not in self._instances:
            self._instances[ins] = ConfigItemInstance(self.type, self.attr, self.key, self.default, self)
        return self._instances[ins]

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._instance(instance).value.get()

    def __set__(self, instance, value):
        item = self._instance(instance).value  # idict_item.value

        old, new = item.value, value

        item.set(value)

        instance.on_change(self.attr, old, new)

    def from_instance(self, instance) -> 'ConfigItemInstance':
        item_instance = self._instance(instance).value
        return item_instance
