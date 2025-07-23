import typing

if typing.TYPE_CHECKING:
    from .type_realities import *

else:
    PointerType = \
        ArrayType = \
        RefType = None

type Pointer[T] = T | PointerType | ArrayType | int | None
type Ref[T] = T | RefType[T] | None
type Array[T, N=None] = typing.Sequence[T] | ArrayType
type ProtoType[RT, *AT] = typing.Callable[[*AT], RT]
