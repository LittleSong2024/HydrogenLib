class Array:
    def __init__(self, tp, length=1, *value):
        self.__ctype__ = tp * length
        self.__cdata__ = self.__ctype__(*value)
