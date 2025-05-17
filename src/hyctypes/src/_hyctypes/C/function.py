from .prototype import Prototype


class Function:
    def __init__(self, func, dll=None):
        self._func = Function(func)
        self._callable = None
        self._prototype = Prototype.from_function(self._func)

        self._dll = dll

        if self._dll is not None:
            self._dll = dll
            self._prototype.call_standard = dll.conv
            self.connect(dll)  # 连接dll

    @classmethod
    def define(cls, dll):
        def wrapper(func):
            return cls(func, dll)

        return wrapper

    @property
    def func(self):
        return self._func

    def connect(self, dll):
        """
        将函数原型与dll连接
        """
        self._callable = dll.register(self._prototype)

    def __call__(self, *args, **kwargs):
        return self._callable(*args, **kwargs)
