import typing

if typing.TYPE_CHECKING:
    from .type_realities import *
    from .impls import Pointer as _Pointer, Ref as _Ref


type Pointer[T] = T | PointerType[T] | _Pointer | ArrayType | int | None
type Ref[T] = T | RefType[T] | None
type Array[T, N=None] = typing.Sequence[T] | ArrayType
type ProtoType[RT, *AT] = typing.Callable[[*AT], RT]
