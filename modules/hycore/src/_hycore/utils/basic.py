from ..decorators import singleton_decorator


class Char(int):

    def __str__(self):
        return chr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


@singleton_decorator
class _Null:
    ...


null = _Null()
inf = float('inf')
