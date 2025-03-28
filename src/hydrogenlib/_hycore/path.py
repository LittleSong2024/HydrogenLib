import os
from os import PathLike
from pathlib import Path
from typing import Literal, Optional, Union


def path_to(*path):
    path = os.sep.join(path)
    return path


def isdir(path):
    return os.path.isdir(path)


def isfile(file):
    return os.path.isfile(file)


def path_exists(path):
    return os.path.exists(path)


def mkdir(path):
    os.mkdir(path)


def mkdirs(path):
    if isdir(path):
        return
    os.makedirs(path)


def rmdir(path):
    os.rmdir(path)


def remove(path):
    os.remove(path)


def rename_file(old, new):
    os.rename(old, new)


def mkfile(file, clear=True):
    if not isfile(file):
        directory = os.path.dirname(file)
        if directory:
            mkdirs(directory)
        open(file, "w").close()
    elif clear:
        open(file, "w").close()


def listdir(path):
    return os.listdir(path)


def scandir(path):
    for i in os.scandir(path):
        try:
            yield i
        except PermissionError:
            continue


def scandir_ls(path):
    return list(scandir(path))


def rmdirs(path):
    for i in scandir(path):
        if i.is_dir():
            rmdirs(i.path)
        else:
            remove(i.path)
    rmdir(path)


def rmfile(file):
    remove(file)


def abspath(path):
    return os.path.abspath(path)


def isabspath(path):
    return os.path.isabs(path)


def tree(folder) -> dict:
    f_dic = {folder: {}}
    now_dic = f_dic[folder]
    folder = path_to(folder)

    if isfile(folder):
        now_dic[folder] = os.path.getsize(folder)
    else:
        for i in scandir(folder):
            if i.is_dir():
                now_dic[i.path] = tree(i.path)
            else:
                now_dic[i.path] = os.path.getsize(i.path)
    return f_dic


class StringPath(str):
    def __init__(self, __dir=None):
        if __dir is None:
            self._path = None
        else:
            self._path = Path(__dir)

    def get_path(self) -> Path:
        return self._path

    def using(self, path):
        return self._path / path

    def absolute(self):
        return self.__class__(self._path.absolute())

    def as_uri(self):
        return self.__class__(self._path.as_uri())

    def as_posix(self):
        return self.__class__(self._path.as_posix())

    @property
    def anchor(self):
        return self.__class__(self._path.anchor)

    def chmod(self, mode, *, follow_symlinks=True):
        self._path.chmod(mode, follow_symlinks=follow_symlinks)

    @classmethod
    def cwd(cls):
        return cls(Path.cwd())

    @property
    def drive(self):
        return self._path.drive

    def exists(self, follow_symlinks=True):
        return self._path.exists(follow_symlinks=follow_symlinks)

    def expanduser(self):
        return self._path.expanduser()

    def glob(self, pattern, *, case_sensitive: Optional[bool] = None):
        return self._path.glob(pattern, case_sensitive=case_sensitive)

    def group(self):
        return self._path.group()

    def hardlink_to(self, target):
        self._path.hardlink_to(target)

    @classmethod
    def home(cls):
        return cls(Path.home())

    def is_absolute(self):
        return self._path.is_absolute()

    def is_block_device(self):
        return self._path.is_block_device()

    def is_char_device(self):
        return self._path.is_char_device()

    def is_dir(self):
        return self._path.is_dir()

    def is_fifo(self):
        return self._path.is_fifo()

    def is_file(self):
        return self._path.is_file()

    def is_junction(self):
        return self._path.is_junction()

    def is_mount(self):
        return self._path.is_mount()

    def is_relative_to(self, other, *_deprecated):
        return self._path.is_relative_to(other, *_deprecated)

    def is_reserved(self):
        return self._path.is_reserved()

    def is_socket(self):
        return self._path.is_socket()

    def is_symlink(self):
        return self._path.is_symlink()

    def iterdir(self):
        return self._path.iterdir()

    def joinpath(self, *args):
        return self.__class__(self._path.joinpath(*args))

    def lchmod(self, mode):
        self._path.lchmod(mode)

    def lstat(self):
        return self._path.lstat()

    def match(self, pattern, *, case_sensitive: Optional[bool] = None):
        return self._path.match(pattern, case_sensitive=case_sensitive)

    def mkdir(self, mode=0o777, parents=False, exist_ok=False):
        self._path.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)

    @property
    def name(self):
        return self._path.name

    def open(self,
             mode: Literal[
                 "r+", "+r", "rt+", "r+t", "+rt", "tr+", "t+r", "+tr", "w+", "+w", "wt+", "w+t", "+wt", "tw+", "t+w",
                 "+tw", "a+", "+a", "at+", "a+t", "+at", "ta+", "t+a", "+ta", "x+", "+x", "xt+", "x+t", "+xt", "tx+",
                 "t+x", "+tx", "w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx", "r", "rt", "tr", "U", "rU", "Ur",
                 "rtU", "rUt", "Urt", "trU", "tUr", "Utr"
             ] = "r",
             buffering: int = -1,
             encoding: Optional[str] = None,
             errors: Optional[str] = None,
             newline: Optional[str] = None):
        return self._path.open(
            mode=mode, buffering=buffering,
            encoding=encoding, errors=errors, newline=newline,
        )

    def open_with_neoio(self, io_instance = None, mode: str= 'r', encoding: str= None, create: bool = None, *args, **kwargs):
        if io_instance is None:
            from .file import NeoIO
            io_instance = NeoIO()

        return io_instance.open(self, mode, encoding, create=create, *args, **kwargs)

    def owner(self):
        return self._path.owner()

    @property
    def parents(self):
        return [self.__class__(pre) for pre in self._path.parents]

    @property
    def parts(self):
        return self._path.parts

    def read_bytes(self):
        return self._path.read_bytes()

    def read_text(self, encoding=None, errors=None):
        return self._path.read_text(encoding=encoding, errors=errors)

    def readlink(self):
        return self._path.readlink()

    def relative_to(self,
                    other: Union[str, PathLike[str]],
                    *_deprecated: Union[str, PathLike[str]],
                    walk_up: bool = False):
        return self.__class__(
            self._path.relative_to(
                other,
                *_deprecated,
                walk_up=walk_up
            )
        )

    def rename(self, target):
        self._path.rename(target)

    def path_replace(self, target):
        self._path.replace(target)

    def resolve(self, strict=False):
        return self.__class__(self._path.resolve(strict=strict))

    def rglob(self, pattern, *, case_sensitive: Optional[bool] = None):
        return self._path.rglob(pattern, case_sensitive=case_sensitive)

    def rmdir(self):
        self._path.rmdir()

    def root(self):
        return self._path.root

    def samefile(self, other_path):
        return self._path.samefile(other_path)

    def stat(self):
        return self._path.stat()

    @property
    def stem(self):
        return self._path.stem

    @property
    def suffix(self):
        return self._path.suffix

    @property
    def suffixes(self):
        return self._path.suffixes

    def symlink_to(self, target, target_is_directory=False):
        self._path.symlink_to(target, target_is_directory=target_is_directory)

    def touch(self, mode=0o666, exist_ok=True):
        self._path.touch(mode=mode, exist_ok=exist_ok)

    def unlink(self, missing_ok=False):
        self._path.unlink(missing_ok=missing_ok)

    def walk(self, topdown=True, onerror=None, followlinks=False):
        return self._path.walk(topdown, onerror, followlinks)

    def with_name(self, name):
        return self.__class__(self._path.with_name(name))

    def with_stem(self, stem):
        return self.__class__(self._path.with_stem(stem))

    def with_segments(self, *args):
        return self.__class__(self._path.with_segments(*args))

    def with_suffix(self, suffix: str):
        return self.__class__(self._path.with_suffix(suffix))

    def write_bytes(self, data):
        self._path.write_bytes(data)

    def write_text(self, data, encoding=None, errors=None, newline=None):
        self._path.write_text(data, encoding=encoding, errors=errors, newline=newline)

    @property
    def parent(self):
        return self.__class__(self._path.parent)

    def __truediv__(self, path):
        return self.__class__(self._path / path)

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._path})'
