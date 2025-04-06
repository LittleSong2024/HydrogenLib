import ctypes


def get_annotation(cls, name):
    if name in cls.__annotations__:
        return cls.__annotations__[name]
    bases = cls.__bases__
    for base in bases:
        return get_annotation(base, name)


def _c__str__(self):
    msg = f"struct {self.__class__.__name__}: \n"
    field_fmt = f'<{self._length_}'
    length = 0
    for field, type in self._fields_:
        value = str(getattr(self, field))
        length = max(len(value), length)

        value_fmt = f'<{length}'

        msg += f"\t{format(field, field_fmt)} = {format(value, value_fmt)}  # type: {type.__name__}\n"
    return msg


def _c__repr__(self):
    dct = {field: getattr(self, field) for field, type in self._fields_}
    return f"{self.__class__.__name__}({', '.join([f'{field}={value}' for field, value in dct.items()])})"


def _c__getattr__(self, item):
    ls = []
    for field, type in self._fields_:
        if field.startswith(item):
            ls.append(field)

    if len(ls) == 1:
        return getattr(self, ls[0])
    else:
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")


class HyStructure(ctypes.Structure):
    _fields_ = []
    _order_ = None
    _length_ = 0

    c_struct = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        max_length = cls._length_
        if cls._order_:
            fields = []
            for field in cls._order_:
                max_length = max(max_length, len(field))
                fields.append((field, get_annotation(cls, field)))
            cls._fields_ = fields

        else:
            cls._fields_.extend([*map(tuple, cls.__annotations__.items())])
            for field, _ in cls.__annotations__.items():
                max_length = max(max_length, len(field))

        cls.c_struct = type(
            cls.__name__,
            (ctypes.Structure,),
            {
                '_fields_': cls._fields_,
                '_length_': max_length,
                '__str__': _c__str__,
                '__repr__': _c__repr__,
                '__getattr__': _c__getattr__,
            }
        )
        # cls._type_ = cls.__structure__._type_

    def __new__(cls, **kwargs):
        self = cls.c_struct()
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self
