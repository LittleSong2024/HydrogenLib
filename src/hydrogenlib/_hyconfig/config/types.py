from typing import Sequence

from ..abc.types import ConfigType
from ..._hycore.type_func import literal_eval


class IntType(ConfigType):
    @classmethod
    def validate(cls, value):
        return isinstance(value, int)

    def transform(self, data):
        self.set(int(data))


class StringType(ConfigType):

    def transform(self, data):
        self.set(str(data))

    @classmethod
    def validate(cls, value):
        return isinstance(value, str)


class FloatType(ConfigType):

    def transform(self, data):
        self.set(float(data))

    @classmethod
    def validate(cls, value):
        return isinstance(value, float),


class BooleanType(ConfigType):

    def transform(self, data):
        self.set(bool(data))

    @classmethod
    def validate(cls, value):
        return isinstance(value, bool)


class ListType(ConfigType):

    def transform(self, data):
        self.set(list(data))

    @classmethod
    def validate(cls, value):
        return isinstance(value, Sequence)


class TupleType(ConfigType):

    def transform(self, data):
        self.set(tuple(data))

    @classmethod
    def validate(cls, value):
        return isinstance(value, tuple)


class DictType(ConfigType):

    def transform(self, data):
        self.set(data)

    @classmethod
    def validate(cls, value):
        return isinstance(value, dict)


class SetType(ConfigType):

    def transform(self, data):
        self.set(set(data))

    @classmethod
    def validate(cls, value):
        return isinstance(value, set)


class BytesType(ConfigType):

    def transform(self, data):
        self.set(literal_eval(data))

    def dump(self):
        return str(self.value)  # 有些后端不支持bytes

    @classmethod
    def validate(cls, value):
        return isinstance(value, bytes)
