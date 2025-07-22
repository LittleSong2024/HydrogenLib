from typing import Callable, Any

from .lz_data import LazyData
from ...better_descriptor import (Descriptor, DescriptorInstance)


class LazyFieldInstance(DescriptorInstance):
    _lazydata = None

    def __dspt_init__(self, inst, owner, name, dspt):
        self._lazydata = LazyData(dspt.loader, inst)

    def __dspt_get__(self, instance, owner, parent) -> Any:
        return self._lazydata.get(instance)  # 传递实例


class LazyField(Descriptor):
    def __init__(self, loader: Callable):
        super().__init__()
        self.loader = loader

    def __dspt_new__(self, inst) -> DescriptorInstance:
        return LazyFieldInstance()
