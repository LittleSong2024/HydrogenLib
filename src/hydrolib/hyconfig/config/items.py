import builtins
from typing import Any
from ..abc.types import ConfigType


class ConfigItemInstance:
    def __init__(self, type_instance: ConfigType, default_value):
        self.data = type_instance
        self.default = default_value


class ConfigItem:
    def __init__(self, key, *, type: type[ConfigType], default: Any):
        self.key = key
        self.type = type
        self.default = default

        if not isinstance(type, builtins.type):
            raise TypeError("type must be a ItemType")

        self.type.type_check(default)

        self.item = ConfigItemInstance(self.type(default), self.default)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.item.data.value

    def __set__(self, instance, value):
        self.type.type_check(value)
        self.item.data.set(value)
        from .container import ConfigContainer
        if isinstance(instance, ConfigContainer):
            instance.changeEvent(self.key)

