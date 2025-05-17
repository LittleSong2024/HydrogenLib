from abc import ABC, abstractmethod
from io import IOBase
from typing import Generator


class FileInfo(ABC):
    @property
    @abstractmethod
    def size(self): ...

    @property
    @abstractmethod
    def name(self): ...

    @property
    @abstractmethod
    def path(self): ...

    @property
    @abstractmethod
    def mode(self): ...

    @property
    def inode(self): ...

    @property
    def birthday(self): ...

    @property
    def last_access(self): ...

    @property
    def last_modified(self): ...

    @property
    def device(self): ...

    @property
    def nlink(self): ...

    @property
    def uid(self): ...

    @property
    def gid(self): ...


class FileSystem(ABC):
    @abstractmethod
    def mkfile(self, file) -> None: ...

    @abstractmethod
    def mkdir(self, path) -> None: ...

    @abstractmethod
    def mkdirs(self, path) -> None: ...

    @abstractmethod
    def read(self, file, mode='r'): ...

    @abstractmethod
    def remove(self, file) -> None: ...

    @abstractmethod
    def rmdir(self, path): ...

    @abstractmethod
    def rmdirs(self, path): ...

    @abstractmethod
    def write(self, file, mode='w'): ...

    @abstractmethod
    def open(self, file, mode, encoding=None) -> IOBase: ...

    @abstractmethod
    def listdir(self, path) -> Generator[FileInfo, None, None]: ...

    @abstractmethod
    def close(self): ...
