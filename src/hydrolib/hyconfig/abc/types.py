from abc import ABC, abstractmethod
from typing import Any


class ConfigType(ABC):
    value: Any

    def dump(self):  # 将配置项的数据导出到后端
        return self.value

    @abstractmethod
    def load(self, data):  # 将后端返回的配置数据加载到配置项中
        ...  # 应该解决数据类型转换的问题

    @classmethod
    @abstractmethod
    def type_check(cls, init_value):
        ...

    @staticmethod
    def error(type, msg):
        raise Exception(f"{type}: {msg}")

    def __init__(self, value, parent=None):
        self.set(value)
        self.parent = parent

    def set(self, value):
        self.type_check(value)
        self.value = value





