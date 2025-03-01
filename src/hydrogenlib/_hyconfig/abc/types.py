from abc import ABC, abstractmethod
from typing import Any


class ConfigType(ABC):
    value: Any

    def dump(self):  # 将配置项的数据导出到后端
        # 大多数时候不需要重写
        return self.value

    @abstractmethod
    def transform(self, data):  # 将后端返回的配置数据加载到配置项中
        ...  # 应该解决数据类型转换的问题

    @classmethod
    @abstractmethod
    def validate(cls, value) -> bool:  # 检查类型是否符合
        ...


    def __init__(self, value, parent=None):
        self.set(value)
        self.parent = parent

    def set(self, value):
        self.validate(value)
        self.value = value

    def get(self):
        return self.value





