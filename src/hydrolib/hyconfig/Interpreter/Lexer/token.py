import re
from typing import Union, Any


class Token:
    def __init__(
            self,
            type_: str, value: Union[re.Match, Any],
            lineno: int = 0, colno: int = 0, offset: int = 0
    ):
        self.type = type_
        self.lineno = lineno
        self.colno = colno
        self.offset = offset

        if isinstance(value, re.Match):
            self.match = value
            self.value: Union[str, int] = value.group()
        else:
            self.value: Union[str, int] = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        elif isinstance(other, tuple):
            return self.type == other[0] and self.value == other[1]
        else:
            return False

    @property
    def t(self):
        """
        获取Token的类型
        """
        return self.type

    @property
    def v(self):
        """
        获取Token的值
        """
        return self.value

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(str(self.value))

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.type},\t{repr(self.value)},\t{self.lineno}:{self.colno}-{self.offset}>"
