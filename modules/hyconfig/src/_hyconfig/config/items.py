from __future__ import annotations

import builtins
import typing
from typing import Protocol, runtime_checkable

from ..abc.model import AbstractModel
from ..abc.types import ConfigTypeBase
from _hycore.better_descriptor import *

if typing.TYPE_CHECKING:
    from .container import HyConfig


@runtime_checkable
class Item(Protocol):
    value: ConfigItemInstance
    key_instance: Any


class ConfigItemInstance(DescriptorInstance):
    key: str
    type: ConfigTypeBase
    default: Any

    def __init__(self):
        super().__init__()

    def __dspt_init__(self, inst, owner, name, dspt: 'ConfigItem'):
        self.parent = dspt
        self.inst = inst
        self.key = dspt.key

    @property
    def model(self):
        return self.parent.model

    def set(self, v):
        self.validate(v, error=True)
        self.model.set(self.key, v)

    def get(self):
        return self.model.get(self.key)

    def validate(self, v, error=False):
        res = self.type.validate(v)
        if not res and error:
            raise TypeError(f"{type(v)} is not a valid type")
        return res

    @property
    def value(self):
        return self.get()

    @value.setter
    def value(self, value):
        self.set(value)

    def __dspt_get__(self, inst, owner, parent) -> Any:
        return self.value

    def __dspt_set__(self, inst, value, parent):
        self.value = value

    def __dspt_del__(self, inst, parent):
        self.value = self.default


class ConfigItem(Descriptor):
    def __init__(self, type: type | ConfigTypeBase, default: Any, *, key=None, model=None):
        super().__init__()
        self.default = default
        self.key = key
        self.model = model  # type: None | AbstractModel

        if isinstance(type, ConfigTypeBase):
            self.type = type
        else:
            self.type = type()

        if not self.type.validate(default):
            raise TypeError("default value is not a valid type")

        if not isinstance(type, builtins.type):
            raise TypeError("type must be a ItemType")

    def __dspt_init__(self, name, owner):
        self.key = self.key or name

    def __dspt_get__(self, inst, owner: 'HyConfig') -> Any:
        self.model = owner.__cfgbackend__.get_model()
        return super().__dspt_get__(inst, owner)

    def __dspt_new__(self) -> ConfigItemInstance:
        return ConfigItemInstance()
