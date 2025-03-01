from abc import ABC, abstractmethod
from typing import Any


class ConfigType(ABC):
    value: Any  # 配置项的值
    types: Any  # 配置项值的类型

    parent: Any
    backend: 'BackendABC'

    def __init_subclass__(cls, *, types=None):
        cls.types = types

    def __init__(self, value, parent=None, backend=None):
        self.set(value)
        self.parent = parent
        self.backend = backend

    def transform(self):  # 将配置项的值转换为后端可识别的配置数据
        ...

    @abstractmethod
    def load(self, value):  # 将后端返回的配置数据加载到配置项中
        return value

    @classmethod
    @abstractmethod
    def validate(cls, value) -> bool:  # 检查类型是否符合
        ...

    def set(self, value):
        self.validate(value)
        self.value = value

    def get(self):
        return self.value


from .backend import BackendABC


