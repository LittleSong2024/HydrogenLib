from .builtin_conditions import *
from ...basic_methods import *
from ...abstract import AbstractMarker


class Condition:
    def __init__(self, condition: AbstractCondition, on_true=None, on_false=None):
        self._condition = condition
        self._on_true = on_true
        self._on_false = on_false

    def generate(self, owner, **kwargs):
        result = self._condition.run(owner, **kwargs)
        if result:
            return generate(self._on_true, owner, **kwargs)
        else:
            return generate(self._on_false, owner, **kwargs)

    def restore(self, owner, value, **kwargs):
        result = self._condition.run(owner, **kwargs)
        if result:
            return restore(self._on_true, value, owner, **kwargs)
        else:
            return restore(self._on_false, value, owner, **kwargs)


class Conditions(AbstractMarker):
    def __init__(self, *conditions: tuple[AbstractCondition, AbstractMarker]):
        self._conditions = conditions

    def generate(self, owner, **kwargs):
        for condition, marker in self._conditions:
            result = condition.run(owner, **kwargs)
            if result:
                return generate(marker, owner, **kwargs)
        return None

