from .type_hints import as_ctype


class ArrayType:
    def __init__(self, tp, length=0):
        self.__ctype__ = as_ctype(tp) * length
        self.__length__ = length

    def __call__(self, *args, **kwargs):
        return self.__ctype__(*args, **kwargs)  # 这里直接返回 ctypes.Array 对象
        # 不是我不想重写自己的Array,而是这个重写实在没有意义
        # ctypes 其他地方手感不好,但它的Array确实挑不出什么毛病

