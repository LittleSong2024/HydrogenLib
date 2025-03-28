import ctypes


def get_annotation(cls, name):
    if name in cls.__annotations__:
        return cls.__annotations__[name]
    bases = cls.__bases__
    for base in bases:
        return get_annotation(base, name)


#
#
class HyStructure(ctypes.Structure):
    _fields_ = []
    _order_ = None

    c_struct = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._order_:
            fields = []
            for field in cls._order_:
                fields.append((field, get_annotation(cls, field)))
            cls._fields_ = fields

        else:
            cls._fields_.extend([*map(tuple, cls.__annotations__.items())])

        cls.c_struct = type(
            cls.__name__,
            (ctypes.Structure,),
            {
                '_fields_': cls._fields_
            }
        )
        # cls._type_ = cls.__structure__._type_

    def __new__(cls, **kwargs):
        self = cls.c_struct()
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

