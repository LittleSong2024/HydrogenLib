from abc import ABC, abstractmethod
from typing import Any


class ConfigType(ABC):
    value: Any

    def dump(self):  # 将配置项的数据导出到后端
        # 大多数时候不需要重写
        return self.value

    @abstractmethod
    def load(self, data):  # 将后端返回的配置数据加载到配置项中
        ...  # 应该解决数据类型转换的问题

    @classmethod
    @abstractmethod
    def type_check(cls, init_value):
        ...

    @classmethod
    def check_exit(cls, expr, msg):  # 给 .type_check() 用的
        if not expr:
            raise Exception(f"{cls.__name__}: {msg}")

    def __init__(self, value, parent=None):
        self.set(value)
        self.parent = parent

    def set(self, value):
        self.type_check(value)
        self.value = value

    def get(self):
        return self.value





