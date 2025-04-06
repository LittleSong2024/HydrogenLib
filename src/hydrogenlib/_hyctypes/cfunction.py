from .._hycore.type_func import Function


class CFunction(Function):
    def __init__(self, func, dll=None, target=None):
        super().__init__(func)
        self.dll = dll
        self.target = target

    def generate_c_signature(self, target):
        argtypes = []

        for param in self.signature.parameters.values():
            argtypes.append(param.annotation)

        restype = self.signature.return_annotation

        target.argtypes = argtypes
        target.restype = restype

        return CFunction(self, dll=self.dll, target=target)  # copy a new instance

    def _sort_args(self, args, kwargs):
        arguments = self.signature.bind(*args, **kwargs).arguments
        for param in self.signature.parameters.values():
            if param.name not in arguments:
                if param.default is not param.empty:
                    yield param.default
                else:
                    raise TypeError(f"Missing argument {param.name}")
            else:
                yield arguments[param.name]

    def __call__(self, *args, **kwargs):
        if self.target is None:
            raise TypeError("CFunction target is None")
        sorted_args = list(self._sort_args(args, kwargs))
        return self.target(*sorted_args)
        # return self.target(*args, **kwargs)

    def __get__(self, instance, owner):
        return lambda *args, **kwargs: self.__call__(instance, *args, **kwargs)


