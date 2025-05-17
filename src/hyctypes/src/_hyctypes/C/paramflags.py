class _ParamFlags:
    INPUT = 1
    OUTPUT = 2
    OPTIONAL = 4
    PTR = 8

    def __call__(self, flags, name, default=0):
        return flags, name, default


ParamFlags = _ParamFlags()
