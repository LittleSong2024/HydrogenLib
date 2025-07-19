import enum
from dataclasses import dataclass
from typing import TypedDict

from _hycore.utils import InstanceMapping


class ExtraMode(str, enum.Enum):
    ignore = 'ignore'
    forbid = 'forbid'
    allow = 'allow'


class _FieldValidator(classmethod):
    name: str = ...

    def __init__(self, func, name):
        super().__init__(func)
        self.name = name


@dataclass
class ModelConfig:
    fields: InstanceMapping[str, 'Field'] = None


class Field:
    keyword_only = False

    @property
    def validator(self):
        return self._validator

    @validator.setter
    def validator(self, value):
        self._validator = value

    def has_default(self):
        return self.default is not None

    def __init__(self, name, type, default=None):
        self.name = name
        self.type = type
        self.default = default

        self._mapping = InstanceMapping()
        self._validator = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self._mapping.get(instance, self.default)

    def __set__(self, instance, value):
        self._mapping[instance] = self.validator(value) if self.validator else value


class BaseModelConfig(TypedDict):
    extra: ExtraMode
