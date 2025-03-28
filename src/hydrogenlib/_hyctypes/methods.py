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

    def __call__(self, *args, **kwargs):
        if self.target is None:
            raise TypeError("CFunction target is None")
        return self.target(*args, **kwargs)


