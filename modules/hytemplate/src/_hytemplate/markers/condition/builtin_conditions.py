from .abstract import AbstractCondition
from ...abstract import generate


class ComplexCondition(AbstractCondition):
    def __init__(self, a, b, cmp=lambda a, b: a == b):
        self._a, self._b = a, b
        self._cmp = cmp

    def run(self, template, **kwargs) -> bool:
        return self._cmp(
            generate(self._a, template, **kwargs),
            generate(self._b, template, **kwargs)
        )


def EqualCondition(a, b):
    return ComplexCondition(a, b)


def NotEqualCondition(a, b):
    return ComplexCondition(a, b, cmp=lambda a, b: a != b)


def GreaterThanCondition(a, b):
    return ComplexCondition(a, b, cmp=lambda a, b: a > b)


def LessThanCondition(a, b):
    return ComplexCondition(a, b, cmp=lambda a, b: a < b)


def GreaterThanOrEqualCondition(a, b):
    return ComplexCondition(a, b, cmp=lambda a, b: a >= b)


def LessThanOrEqualCondition(a, b):
    return ComplexCondition(a, b, cmp=lambda a, b: a <= b)


def ContainsCondition(a, b):
    return ComplexCondition(a, b, cmp=lambda a, b: a in b)


def NotContainsCondition(a, b):
    return ComplexCondition(a, b, cmp=lambda a, b: a not in b)


def CmpCondition(a, b, func):
    return ComplexCondition(a, b, lambda a, b: func(a, b))


class AllCondition(AbstractCondition):
    def __init__(self, *conditions):
        self._conditions = conditions

    def run(self, template, **kwargs) -> bool:
        for condition in self._conditions:
            if not condition.run(template, **kwargs):
                return False
        return True


class AnyCondition(AbstractCondition):
    def __init__(self, *conditions):
        self._conditions = conditions

    def run(self, template, **kwargs) -> bool:
        for condition in self._conditions:
            if condition.run(template, **kwargs):
                return True
        return False


class Not(AbstractCondition):
    def __init__(self, condition):
        self._condition = condition

    def run(self, template, **kwargs) -> bool:
        return not self._condition.run(template, **kwargs)
