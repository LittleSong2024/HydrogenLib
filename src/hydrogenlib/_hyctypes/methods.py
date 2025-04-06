import ctypes as _ctypes


def copy_new(source):

    if not isinstance(source, (_ctypes.Union, _ctypes.Structure)):
        raise TypeError("source must be a ctypes Union or Structure")

    try:
        source_addr = _ctypes.addressof(source)
        source_cls = type(source)

        size = _ctypes.sizeof(source)

        target = source_cls()
        _ctypes.memmove(_ctypes.addressof(target), source_addr, size)

        return target
    except Exception as e:
        raise RuntimeError("Failed to copy ctypes Union or Structure") from e

