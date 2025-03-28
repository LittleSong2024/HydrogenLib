from abc import ABC
from typing import Any, Union


class ConfigTypeBase(ABC):
    parent: Any  # 配置项的父级, 通常为ConfigContainer
    type: Any  # 配置项值的类型
    backend: 'AbstractBackend'  # 配置项的后端实例

    def __init_subclass__(cls, *, type=None, **kwargs):
        cls.type = type

    def transform(self, value):  # 将配置项的值转换为后端可识别的配置数据
        ...

    def load(self, value):  # 将后端返回的配置数据加载到配置项中
        return value

    def validate(self, value) -> bool:  # 检查类型是否符合
        return isinstance(value, self.type)


from .backend import AbstractBackend

_TypeType = Union[ConfigTypeBase, type[ConfigTypeBase]]


class ConfigTypeMapping:
    def __init__(self):
        self._mapping = {}

    def add_pair(self, key_type, value_type):
        self._mapping[key_type] = value_type

    def add_type(self, config_type: _TypeType):
        self.add_pair(config_type.type, config_type)

    def add_types(self, *config_types: _TypeType):
        for config_type in config_types:
            self.add_type(config_type)

    def remove_pair(self, key_type):
        return self._mapping.pop(key_type)

    def remove_pairs(self, *key_types):
        for key_type in key_types:
            self.remove_pair(key_type)

    def remove_type(self, config_type: _TypeType):
        return self.remove_pair(config_type.type)

    def get_type(self, config_type: _TypeType):
        return self.get_pair(config_type.type)

    def get_pair(self, key_type):
        return self._mapping.get(key_type)

    def exists(self, key_type):
        return key_type in self._mapping

    def exists_type(self, config_type: _TypeType):
        return self.exists(config_type.type)

    def __contains__(self, item):
        return self.exists(item)

    def __getitem__(self, item):
        return self.get_pair(item)

    def __setitem__(self, key, value):
        self.add_pair(key, value)

    def __delitem__(self, key):
        self.remove_pair(key)

    def __iter__(self):
        for k, v in self._mapping.items():
            yield k, v
