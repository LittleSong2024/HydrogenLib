def singleton_decorator(cls):
    cls._instance = None

    def new(cls):
        origin_new = cls.__new__
        if cls._instance is None:
            cls._instance = origin_new(cls)

        return cls._instance

    cls.__new__ = new

    return cls


def Instance(*args, **kwargs):
    def wrapper(cls):
        return cls(*args, **kwargs)

    return wrapper
