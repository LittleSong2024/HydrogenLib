from .winapi import CreateFileMapping

def _CreateFileMapping(name: str, size: int):
    return CreateFileMapping(
        win32con.INVALID_HANDLE_VALUE,
        None,
        win32con.PAGE_READWRITE,
        0,
        size,
        name
    )


def _OpenFileMapping(name: str):
    return win32api.OpenFileMapping(
        win32con.FILE_MAP_ALL_ACCESS,
        False,
        name
    )


def _MapViewOfBuffer(handle, size: int):
    return win32api.MapViewOfFile(
        handle,
        win32con.FILE_MAP_WRITE,
        0,
        0,
        size
    )


def _UnmapViewOfBuffer(buffer):
    return win32api.UnmapViewOfFile(buffer)


def _CloseHandle(handle):
    return win32api.CloseHandle(handle)


def _CopyMemory(src, dst, size: int):
    return win32api.CopyMemory(dst, src, size)


def global_memory_name(name: str):
    return f'Global\\{name}'


class SharedMemoryCreator:
    def __init__(self):
        self.size = None
        self.name = None

        self.hMapFile = None
        self.pBuf = None

    def create(self, name: str, size: int, __global: bool = True):
        self.name = name
        self.size = size
        if __global:
            self.name = global_memory_name(self.name)

        self.hMapFile = _CreateFileMapping(self.name, self.size)
        if self.hMapFile == 0:
            raise Exception('CreateFileMapping failed')
        self.pBuf = _MapViewOfBuffer(self.hMapFile, self.size)
        if self.pBuf == 0:
            raise Exception('MapViewOfFile failed')

    def write(self, data: bytes):
        if len(data) > self.size:
            raise OverflowError(f"{len(data)} is too long. (Only {self.size} bytes)")

        _CopyMemory(self.pBuf, data, len(data))

    def close(self):
        _UnmapViewOfBuffer(self.pBuf)
        _CloseHandle(self.hMapFile)

    def __del__(self):
        self.close()


class SharedMemoryReader:
    def __init__(self):
        self.name = None

        self.hMapFile = None
        self.pBuf = None

    def open(self, name: str, __global: bool = True):
        self.name = name
        if __global:
            self.name = global_memory_name(self.name)

        self.hMapFile = _OpenFileMapping(self.name, 0)
        if self.hMapFile == 0:
            raise Exception('CreateFileMapping failed')

        self.pBuf = _MapViewOfBuffer(self.hMapFile, 0)
        if self.pBuf == 0:
            raise Exception('MapViewOfFile failed')

    def read(self) -> bytes:
        return bytes(self.pBuf)

    def close(self):
        _UnmapViewOfBuffer(self.pBuf)
        _CloseHandle(self.hMapFile)



