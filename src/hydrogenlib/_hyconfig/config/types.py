from typing import Sequence

from ..abc.types import ConfigType


class IntType(ConfigType, types=int):
    def load(self, value):
        self.set(int(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, int)


class StringType(ConfigType, types=str):
    def load(self, value):
        self.set(str(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, str)


class FloatType(ConfigType, types=float):
    def load(self, value):
        self.set(float(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, float),


class BooleanType(ConfigType, types=bool):
    def load(self, value):
        self.set(bool(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, bool)


class ListType(ConfigType, types=list):
    def load(self, value):
        self.set(list(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, Sequence)


class TupleType(ConfigType, types=tuple):
    def load(self, value):
        self.set(tuple(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, tuple)


class DictType(ConfigType, types=dict):
    def load(self, value):
        self.set(dict(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, dict)


class SetType(ConfigType, types=set):
    def load(self, value):
        self.set(set(value))

    @classmethod
    def validate(cls, value):
        return isinstance(value, set)


class BytesType(ConfigType, types=bytes):
    def load(self, value):
        self.set(bytes(value))

    def transform(self):
        if self.backend.support(bytes):
            return self.value
        else:
            return list(self.value)

    @classmethod
    def validate(cls, value):
        return isinstance(value, bytes)
