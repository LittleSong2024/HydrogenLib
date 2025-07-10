from . import get_attr_by_path as _gabp, set_attr_by_path as _sabp, del_attr_by_path as _dabp
import enum as _enum
from typing import Callable, Any


class aliasmode(int, _enum.Enum):
    read = 0
    write = 1
    read_write = 2


class alias:
    """
    声明属性别名

    class myclass:
        a = ...

        b = alias['a'](mode=alias.mode.read)  # 这将创建一个只读的别名
        c = alias['a'](mode=alias.mode.write)  # 这将创建一个只写的别名
        d = alias['a'](mode=alias.mode.read_write)  # 这将创建一个可同时读写的别名

        # 当然这些声明方式都可以用原始的 alias(name, mode, classvar_enabled) 来代替

    你也可以自定义钩子

    class myclass:
        a = ...
        a_alias = alias['a'](mode=alias.mode.read_write)

        @a_alias.getter
        def a_alias(self, value):
            return value  # value 是当前属性的值,你可以进行修改,然后返回修改后的值

        @a_alias.setter
        def a_alias(self, value):
            return value  # 这时的 value 是即将修改的值,如果不进行干涉,需要直接返回

        @a_alias.deleter
        def a_alias(self):
            # raise AttributeError(...)  # 如果你想中断 delete 操作,你只能通过抛出异常的方式
            pass


    是不是觉得这些功能太简单了
    实际上,属性别名可以应用到嵌套的属性中
    比如:

    class myclass:
        a = otherclass()
        b = alias['a.xxx.xxx'](mode=alias.mode.read_write)

    这时候对 b 操作

    obj = myclass()
    obj.b  # 等同于 obj.a.xxx.xxx
    obj.b = ... # 等同于 obj.a.xxx.xxx = ...

    别名也可以应用在 class var 上,这要求开启 classvar_enabled, 但因为 Python 描述符本身的限制, class var 模式仅可读
    当你尝试以 class var 的形式为一个 alias 赋值时,会发生与你预期不同的事: alias 对象被覆盖
    如果不开启 classvar_enabled 那么任何以 class var 形式获取的别名都将返回 alias 对象本身

    class myclass:
        a = ...
        b = alias['a'](mode=alias.mode.read, classvar_enabled=True)

    myclass.b  # 等同于 myclass.a

    """
    mode = aliasmode

    def __init__(self, attr_path, mode=aliasmode.read, classvar_enabled=False):
        self.path = attr_path
        self.mode = mode
        self.cve = classvar_enabled

        self._get = lambda self, x: x
        self._set = lambda self, v: v
        self._del = lambda self: None

    def __class_getitem__(cls, item):
        return cls(item)

    def __call__(self, *, mode=None, classvar_enabled=None):
        if mode is not None:
            self.mode = mode
        if classvar_enabled is not None:
            self.cve = classvar_enabled

    def getter(self, fnc: Callable[[Any, Any], Any]):
        self._get = fnc
        return self

    def setter(self, fnc: Callable[[Any, Any], Any]):
        self._set = fnc
        return self

    def deleter(self, fnc: Callable[[Any], Any]):
        self._del = fnc
        return self

    def __get__(self, instance, owner):
        if instance is None:
            if self.cve:
                instance = owner
            else:
                return self
        if self.mode in {aliasmode.read_write, aliasmode.read}:
            return self._get(instance, _gabp(instance, self.path))
        raise PermissionError("Can't read alias")

    def __set__(self, instance, value):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            _sabp(instance, self.path, self._set(instance, value))
            return  # 抽象,没加return
        raise PermissionError("Can't write alias")

    def __delete__(self, instance):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            self._del(instance)
            _dabp(instance, self.path)
        raise PermissionError("Can't delete alias")
