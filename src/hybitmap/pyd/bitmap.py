from typing import Iterable, Union

from . import hybitmap as _bitmap


class Bitmap(_bitmap.Bitmap):
    def __init__(self, size_or_bits: Union[int, Iterable[bool]]):
        super().__init__(size_or_bits)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.size})'

    def set_bit(self, index: int, value: bool):
        self._C_set_bit(index, value)

    def get_bit(self, index: int):
        self._C_get_bit(index)

    @property
    def size(self):
        return self._C_get_size()

    @property
    def bytes(self):
        return self._C_to_bytes()

    def byte(self, index):
        return self._C_byte_at(index)

    def bbyte(self, byte_index):
        return self._C_byte_at(byte_index * 8)

    __str__ = __repr__
