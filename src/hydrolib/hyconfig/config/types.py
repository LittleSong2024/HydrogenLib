from typing import Sequence

from ..abc.types import ConfigType
from ...type_func import literal_eval


class IntType(ConfigType):
    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, int), "init_value is not a int")

    def load(self, data):
        self.set(int(data))


class StringType(ConfigType):

    def load(self, data):
        self.set(str(data))

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, str), "init_value is not a str")


class FloatType(ConfigType):

    def load(self, data):
        self.set(float(data))

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, float), "init_value is not a float")


class BooleanType(ConfigType):

    def load(self, data):
        self.set(bool(data))

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, bool), "init_value is not a bool")


class ListType(ConfigType):

    def load(self, data):
        self.set(list(data))

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, Sequence), "init_value is not a sequence")


class TupleType(ConfigType):

    def load(self, data):
        self.set(tuple(data))

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, tuple), "init_value is not a tuple")


class DictType(ConfigType):

    def load(self, data):
        self.set(data)

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, dict), "init_value is not a dict")


class SetType(ConfigType):

    def load(self, data):
        self.set(set(data))

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, set), "init_value is not a set")


class BytesType(ConfigType):

    def load(self, data):
        self.set(literal_eval(data))

    def dump(self):
        return str(self.value)  # 有些后端不支持bytes

    @classmethod
    def type_check(cls, init_value):
        cls.check_exit(isinstance(init_value, bytes), "init_value is not a bytes")
