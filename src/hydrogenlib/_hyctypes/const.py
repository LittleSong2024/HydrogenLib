from typing import Literal


class _AutoDescriptor(object):
    import os as _os

    def __set_name__(self, owner, name):
        if self._os.name == 'nt':
            self.value = owner.STDCALL
        else:
            self.value = owner.CDECL

    def __get__(self, instance, owner) -> Literal[1, 2]:
        return self.value


class CallStandard:
    AUTO = _AutoDescriptor()
    STDCALL = 1
    CDECL = 2


if __name__ == '__main__':
    print(CallStandard.AUTO)
