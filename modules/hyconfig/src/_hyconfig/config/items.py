import dataclasses

from _hycore.utils import InstanceMapping
from _hycore.typefunc import iter_annotations


class ConfigItemMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls._mapping = InstanceMapping()

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if instance not in self._mapping:
            self._mapping[instance] = self()

        return self._mapping[instance]


class InlineConfig(metaclass=ConfigItemMeta):
    def __init_subclass__(cls, **kwargs):
        dataclasses.dataclass(cls)  # 使用 dataclasses 提供的功能实现结构体

