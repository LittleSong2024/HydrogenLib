
from base64 import b64encode, b64decode

from ..abc.types import ConfigTypeBase, ConfigTypeMapping


class IntType(ConfigTypeBase, type=int): ...


class StringType(ConfigTypeBase, type=str): ...


class FloatType(ConfigTypeBase, type=float): ...


class BooleanType(ConfigTypeBase, type=bool): ...


class ListType(ConfigTypeBase, type=list): ...


class TupleType(ConfigTypeBase, type=tuple): ...


class DictType(ConfigTypeBase, type=dict): ...


class SetType(ConfigTypeBase, type=set): ...


class BytesType(ConfigTypeBase, types=bytes):
    def transform(self, value):
        if self.backend.support(bytes):
            return value
        else:
            return b64encode(value).decode()

    def load(self, value):
        if isinstance(value, str):
            return b64decode(value.encode())
        else:
            return value


builtin_type_mapping = m = ConfigTypeMapping()
m.add_types(IntType, StringType, FloatType, BooleanType, ListType, TupleType, DictType, SetType, BytesType)

