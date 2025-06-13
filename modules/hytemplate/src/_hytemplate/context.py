from typing import Optional, Any

import attrs

from .abstract import AbstractMarker


@attrs.define(frozen=True)
class BaseContext:
    root: Optional[Any] = None  # 根对象
    parent: Optional[AbstractMarker] = None  # 父对象
    current: Optional[AbstractMarker] = None  # 当前对象
    globals: dict = None  # 全局变量
    locals: dict = None  # 局部变量, 只会在当前对象及其子对象中生效
    outs: dict = attrs.field(factory=dict)  # 当前对象的输出,它将出现在子对象的输入中
    ins: dict = attrs.field(factory=dict)  # 当前对象的输入, 来自上级对象
    arguments: dict = None  # 外部传入的 `kwargs` 参数

    def new(self, **kwargs):
        kwargs['ins'] = self.outs
        kwargs['outs'] = {}
        return attrs.evolve(self, **kwargs)


@attrs.define(frozen=True)
class GenerationContext(BaseContext):
    ...


@attrs.define(frozen=True)
class RestorationContext(BaseContext):
    value: Any = None
