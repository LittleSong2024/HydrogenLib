import os
from io import BytesIO
from typing import *
from typing import Union

from .data_structures import Stack


def read(file, mode='r'):
    """
    从文件读取数据，允许自定义模式
    """
    with open(file, mode) as f:
        return f.read()


def write(data, file, mode='w'):
    """
    向文件写入数据，允许自定义模式
    """
    with open(file, mode) as f:
        f.write(data)


def empty(file):
    """
    判断文件内容是否为空
    """
    with open(file) as f:
        d = f.read(1)
        if d == '':
            return True


def isspace(file):
    """
    判断文件内容是否为空白
    """
    d = read(file)
    return d.isspace()


class NeoIo:
    """
    新文件读写
    特点:
        1. 可复用
        2. 灵活,完全支持内置的IOAPI
        3. 快速获取文件信息
        4. 堆栈文件

    适用于普通文件操作，在常见桌面和服务器操作系统上表现良好。
    """

    def __init__(self):
        self._fd_ls = Stack()

    def __push_fd(self, fd):
        self._fd_ls.push(fd)

    @property
    def _top_fd(self):
        return self._fd_ls.at_top

    @classmethod
    def from_fd(cls, fd):
        ins = cls()
        ins.__push_fd(fd)
        return ins

    @classmethod
    def fopen(cls, file, mode='r', encoding=None, *args, **kwargs):
        fd = open(file, mode, encoding=encoding, *args, **kwargs)
        ins = cls.from_fd(fd)
        return ins

    def open(self, file, mode='r', encoding=None, *args, **kwargs):
        self.__push_fd(
            open(file, mode, encoding=encoding, *args, **kwargs))
        return self

    @property
    def opend(self):
        return self._top_fd.at_top is not None and not self._top_fd.closed

    @property
    def can_write(self):
        return self._top_fd.writable()

    @property
    def can_read(self):
        return self._top_fd.readable()

    @property
    def can_seek(self):
        return self._top_fd.seekable()

    @property
    def is_bytes_io(self):
        return isinstance(self._top_fd, BytesIO)

    @property
    def pos(self):
        return self._top_fd.tell()

    @property
    def fileno(self):
        return self._top_fd.fileno()

    @property
    def fstat(self):
        try:
            return os.fstat(self.fileno)
        except OSError:
            return None

    @property
    def size(self):
        return self.fstat.st_size

    def write(self, data: Union[bytes, str]):
        if self.can_write:
            self._top_fd.write(data)
        else:
            raise IOError("文件无法写入")

    def seek(self, offset, whence=0):
        self._top_fd.seek(offset, whence)

    def read(self, size=-1):
        if self.can_read:
            return self._top_fd.read(size)
        else:
            raise IOError("文件无法读取")

    def readline(self, size=-1):
        if self.can_read:
            return self._top_fd.readline(size)
        else:
            raise IOError("文件无法读取")

    def readlines(self, hint=-1):
        if self.can_read:
            return self._top_fd.readlines(hint)
        else:
            raise IOError("文件无法读取")

    def clear(self):
        """
        清除文件内容
        """
        self._top_fd.truncate(0)

    def flush(self):
        self._top_fd.flush()

    def close(self):
        if self._top_fd:
            self._top_fd.close()
            self._fd_ls.pop()
        else:
            raise IOError('未打开任何文件')

    def close_all(self):
        while self._fd_ls:
            self._fd_ls.pop().close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
