from typing import Union

from . import _bitmap


class Bitmap(_bitmap.Bitmap):
    def __init__(self, size: int = 1):
        super().__init__(size)

    @property
    def size(self) -> int:
        return self._C_get_size()

    def set(self, index: int, value: Union[bool, int]):
        return self._C_set_bit(index, value)

    def get(self, index: int) -> bool:
        return self._C_get_bit(index)

    def __iter__(self):
        for i in range(self.size * 8):
            yield self.get(i)

    def to_bytes(self):
        return self._C_to_bytes()

    def byte_at(self, index):
        return self._C_byte_at(index)

    def __getitem__(self, index: int) -> bool:
        return self.get(index)

    def __setitem__(self, index: int, value: Union[bool, int]):
        return self.set(index, value)

    def __len__(self):
        return self.size * 8

    def __str__(self):
        return self.to_bytes().hex()

    __repr__ = __str__
