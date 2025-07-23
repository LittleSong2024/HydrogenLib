from typing import Callable, Any

from .lz_data import LazyData
from ...better_descriptor import (Descriptor, DescriptorInstance)


class LazyFieldInstance(DescriptorInstance):
    _lazydata = None

    def __dspt_init__(self, inst, owner, name, dspt: 'LazyField'):
        self._lazydata = LazyData(dspt.loader(), inst)

    def __dspt_get__(self, instance, owner, parent: 'LazyField') -> Any:
        self._lazydata.update_callable(parent.loader())
        return self._lazydata.get(instance)  # 传递实例


class LazyField(Descriptor):
    def __init__(self, loader: Callable = None):
        super().__init__()
        self._loader = loader

    def loader(self, loader: Callable = None):
        if loader:
            self._loader = loader
            return self
        else:
            return self._loader

    def __dspt_new__(self, inst) -> DescriptorInstance:
        return LazyFieldInstance()
