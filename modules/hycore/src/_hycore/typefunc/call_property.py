class call_property:
    """
    类似内置的 ``@property`` 装饰器, 但是使用了另一种设置和获取值的方法

    读取: ``.property()``

    写入: ``.property(value)``

    删除: ``del .property``

    除了读取值的逻辑与 ``@property`` 装饰器不同, 写入和删除都可以沿用 ``@property`` 的逻辑

    比如: ``.property(value)`` 等同于 ``.property = value``

    """
    def __init__(self, fget, fset=None, fdel=None):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel

    def getter(self, fget):
        if not callable(fget):
            raise TypeError("fget must be callable")

        self._fget = fget

    def setter(self, fset):
        if not callable(fset):
            raise TypeError("fset must be callable")

        self._fset = fset

    def deleter(self, fdel):
        if not callable(fdel):
            raise TypeError("fdel must be callable")

        self._fdel = fdel

    def __get__(self, instance, owner):
        if instance is None:
            return self

        def wrapper(*args):
            if args:
                self._fset(instance, *args)
            else:
                return self._fget(instance)

        return wrapper

    def __set__(self, instance, value):
        self._fset(instance, value)

    def __delete__(self, instance):
        self._fdel(instance)
