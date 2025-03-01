import builtins
from typing import Any

from ..abc.types import ConfigType
from ..._hycore.utils import InstanceDict, IDict_Item


class ConfigData:
    def __init__(self, type, value, default, parent: 'ConfigItem' = None):
        self.type: ConfigType = type
        self.value: Any = value
        self.default: Any = default
        self.parent = parent

    def tp_validate(self, value):
        return self.type.validate(value)

    def tp_transform(self):
        return self.type.transform()

    def tm_validate(self, value):
        return self.parent.validate(value)


class ConfigItem:
    def __init__(self, key, *, type: type[ConfigType], default: Any):
        self.attr = None
        self.key = key
        self.type = type
        self.default = default

        if not isinstance(type, builtins.type):
            raise TypeError("type must be a ItemType")

        self.validate(default)

        self._items = InstanceDict()

    def validate(self, value):
        if not self.type.validate(value):
            raise TypeError(f"{type(value)} is not a valid type")

    def _item(self, ins) -> IDict_Item:
        if ins not in self._items:
            self._items[ins] = self.type(self.default, self)
        return self._items[ins]

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._item(instance).value.value

    def __set__(self, instance, value):
        from .container import ConfigContainer  # 循环引用，只能这样写

        item = self._item(instance).value  # config_idct_item.value
        # print(type(item))
        old, new = item.value, value
        item.set(value)

        if isinstance(instance, ConfigContainer):
            instance.on_change(self.attr, old, new)

    def from_instance(self, instance) -> 'ConfigData':
        type_ins = self._item(instance).value

        data = ConfigData(self.type, type_ins.value, self.default, self)
        return data
