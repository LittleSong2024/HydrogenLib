from inspect import get_annotations

from _hycore.typefunc import get_type_name
from .impls import *


class PointerType(AbstractCType, real=Pointer):
    def __init__(self, tp):
        """

        :param tp: 指针目标类型
        """
        self.tp = tp
        self.__real_ctype__ = ctypes.POINTER(as_ctype(tp))

    def __call__(self, obj):
        return Pointer(pointer(obj))

    def __convert_ctype__(self, obj):
        if isinstance(obj, Pointer):
            return obj.cast(self.tp)
        elif isinstance(obj, self.tp):
            return Pointer(pointer(obj))
        else:
            raise TypeError(f"Cannot convert {obj} as {self}")


class ArrayType(AbstractCType, real=Array):
    def __init__(self, tp, length=1):
        """

        :param tp: 数组元素类型
        :param length: 数组长度
        """
        self.tp = tp
        self.length = length
        self.__real_ctype__ = ctypes.POINTER(as_ctype(tp)) * length

    def __call__(self, *args):
        return Array(self.__real_ctype__(*args))

    def __convert_ctype__(self, obj):
        if isinstance(obj, Pointer):
            return
        elif hasattr(obj, '__iter__'):
            obj = tuple(obj)  # 先转换成开销小的元组类型
            length = len(obj)
            if length != self.length:
                # 将 obj 转换成 Array 时发生错误: 长度不匹配
                raise TypeError(f'Convert to Array failed: Length mismatch (except {self.length}, got {length})')
            return Array(self.__real_ctype__(*(as_cdata(x) for x in obj)))
        else:
            raise TypeError(f'Convert to Array failed: {obj} is not iterable')


class RefType(AbstractCType, real=Ref):
    def __init__(self, tp):
        """
        :param tp: 引用目标类型
        """
        self.tp = tp

    def __convert_ctype__(self, obj):
        return Ref(obj)

    def __call__(self, obj):
        return Ref(obj)


class AnonymousType(AbstractCType, real=object):
    def __init__(self, tp):
        self.__real_ctype__ = self.__real_type__ = tp


class _This:
    _i = None

    def __new__(cls, *args, **kwargs):
        if cls._i is None:
            cls._i = super().__new__(cls)

        return cls._i


This = _This()


class StructureType(AbstractCType, real=Structure):
    __struct_meta__ = None

    @staticmethod
    def config_structure(s, fields=None, anonymous=None, pack=None, align=None):
        fields = fields or getattr(s, '_fields_', None)
        anonymous = anonymous or getattr(s, '_anonymous_', None)
        pack = pack or getattr(s, '_pack_', None)
        align = align or getattr(s, '_align_', None)

        if fields is not None:
            s._fields_ = tuple(fields)
        if anonymous is not None:
            s._anonymous_ = tuple(anonymous)
        if pack is not None:
            s._pack_ = pack
        if align is not None:
            s._align_ = align

        return s

    @staticmethod
    def generate_structure_name(types, head='Structure'):
        return f"{head}_{''.join([get_type_name(tp).removeprefix('c_') for tp in types])}"

    def __init__(self, fields, anonymous, pack, align, metaclass=None):
        metaclass = metaclass or self.__struct_meta__ or ctypes.Structure
        self.__real_ctype__ = s = type(
            self.generate_structure_name(map(lambda x: x[1], fields)),
            (metaclass,), {}
        )

        final_fields = []
        final_anonymous = set(anonymous or ())
        for name, typ in fields:
            if isinstance(typ, AnonymousType):
                final_anonymous.add(name)

            final_fields.append((name, as_ctype(typ)))

        self.config_structure(
            s,
            fields=final_fields,
            anonymous=final_anonymous,
            pack=pack,
            align=align,
        )

    def set_real_type(self, tp):
        if not issubclass(tp, Structure):
            raise TypeError(f"{tp.__name__} is not a subclass of Structure")
        self.__real_type__ = tp

    def __convert_ctype__(self, obj):
        return self.__real_ctype__

    def __call__(self, *args, **kwargs):
        return self.__real_type__(
            self.__real_ctype__(*args, **kwargs)
        )

    @classmethod
    def define(cls, maybe_cls, *, pack=None, align=None, anonymous=None, meta=None):
        def decorator(ccls):
            # 提取 annotations
            fields = get_annotations(ccls).items()
            inst = cls(fields, pack=pack, align=align, anonymous=anonymous, metaclass=meta)
            inst.set_real_type(ccls)

            return inst

        if maybe_cls is None:
            return decorator

        else:
            return decorator(maybe_cls)


class UnionType(StructureType, real=Structure):  # 万能的 Structure!!!
    __struct_meta__ = ctypes.Union

# class Structure(ctypes.Structure):
#     def __str__(self):
#         head = f"struct {self.__class__.__name__}:\n"
#         body = ''
#         for field, type in self._fields_:
#             value = getattr(self, field)
#             body += f"\t{field} = {value}  # type: {type.__name__}\n"
#
#         return head + body
#
#     def __repr__(self):
#         field_dct = {
#             k: getattr(self, k) for k in self._fields_
#         }
#         return f"{self.__class__.__name__}({', '.join([f'{field}={value}' for field, value in field_dct.items()])})"
#
#
# def struct(maybe_cls=None, *, pack=None, align=None):
#     def decorator(cls):
#         if not issubclass(cls, ctypes.Structure):
#             raise TypeError(f"{cls.__name__} is not a subclass of Structure")
#
#         # 提取 annotations, 生成 fields
#         anonymous = []  # 记录匿名属性
#         fields = []
#
#         for name, type in cls.__annotations__.items():
#             if isinstance(type, AnonymousType):
#                 anonymous.append(name)
#
#             fields.append((name, as_ctype(type)))
#
#         # 配置结构体
#
#         if pack is not None:
#             cls._pack_ = pack
#
#         if align is not None:
#             cls._align_ = align
#
#         if anonymous:
#             cls._anonymous_ = anonymous
#
#         cls._fields_ = fields
#
#         return cls
#
#     if maybe_cls is None:
#         return decorator
#
#     return decorator(maybe_cls)
#
#
# union = struct
