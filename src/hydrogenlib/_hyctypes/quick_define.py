from collections import OrderedDict
from enum import Enum

from .._hycore.type_func import literal_eval


# 一个经典的函数原型格式
# HANDLE CreateFileMappingA(
#   [in]           HANDLE                hFile,
#   [in, optional] LPSECURITY_ATTRIBUTES lpFileMappingAttributes,
#   [in]           DWORD                 flProtect,
#   [in]           DWORD                 dwMaximumSizeHigh,
#   [in]           DWORD                 dwMaximumSizeLow,
#   [in, optional] LPCSTR                lpName
# );

# 现在,让我们来实现一个解析器来处理这类函数原型


class Empty: ...


class Flags_Const(Enum):
    IN = 0x1
    OUT = 0x2
    INOUT = 0x4
    OPTIONAL = 0x8
    REF = 0x10


def _parse_parameter_methodA(string, globals, locals):
    """
    方法1
    用于解析类似于 [<flags>] <type> <name> 的参数格式
    """
    flags = 0
    type_ = None
    name = None

    string = string.strip()  # 去除头尾空格
    string = string.removesuffix(',')  # 去除尾部逗号
    right_bracket = string.find(']')
    if right_bracket != -1:
        # 提取标志, 然后去除方括号, 分割标志, 最后去除空格
        flags_list = list(map(lambda x: x.strip(), string[:right_bracket].strip('[] ').split(',')))
        # 解析还原标志
        for flag in flags_list:
            flag = flag.upper()
            if flag in Flags_Const.__members__:
                flags |= getattr(Flags_Const, flag).value
            else:
                raise ValueError(f'Unknown flag: {flag}')

    else:
        raise ValueError('No right bracket found', string)

    string = string[right_bracket + 1:]  # 去除标志部分
    str_type, str_name, *error = string.split()  # 分割出类型和名称

    if len(error):
        raise ValueError('Invalid parameter format')

    type_ = literal_eval(str_type, globals, locals)
    name = str_name.strip()

    return name, type_, flags


def _parse_parameter_methodB(string, globals, locals):
    """
    解析类似于 <type> <name> C定义风格的参数格式
    """
    string = string.strip(' ,')
    type_, name = string.split(maxsplit=1)
    type_ = literal_eval(type_, globals, locals)
    return name, type_, 0


class Parameter:

    def __init__(self, name, type, flags):
        self.name = name
        self.type = type
        self.flags = flags

        self._s_type = None

    def has_flag(self, value):
        return self.flags & value

    @classmethod
    def from_string(cls, string: str, globals=None, locals=None):
        for i in [_parse_parameter_methodA, _parse_parameter_methodB]:
            try:
                name, type_, flags = i(string, globals, locals)
                return cls(name, type_, flags)
            except ValueError:
                pass


class Function:
    def __init__(self, name, return_type, parameters):
        self.name = name  # type: str
        self.return_type = return_type
        self.parameters = parameters  # type: OrderedDict[str, Parameter]

    @classmethod
    def from_string(cls, string: str, globals=None, locals=None):
        parameters = OrderedDict()

        string = string.strip().removesuffix(';')  # 去除头尾空格及分号
        first_whitespace = string.find(' ')  # 寻找第一个空格, 它往往存在于返回类型和函数名之间
        if first_whitespace != -1:
            whitespace_ = string[:first_whitespace]
            print(whitespace_)
            return_type = literal_eval(whitespace_, globals, locals)  # 解析返回类型
            left, right = string[first_whitespace + 1:].split('(', 1)
            name = left.strip()
            for line in right.split('\n'):
                line = line.strip()
                if line and not line.startswith(')'):
                    param = Parameter.from_string(line, globals, locals)
                    parameters[param.name] = param

            self = cls(name, return_type, parameters)
            return self

        else:
            raise ValueError('Invalid function format')

    def generate_c_signature(self, target):
        target.argtypes = self.argtypes
        target.restype = self.restype
        return target

    @property
    def argtypes(self):
        return [i.type for i in self.parameters.values()]

    @property
    def restype(self):
        return self.return_type


def generate_c_signature(target, function: Function):
    target.argtypes = function.argtypes
    target.restype = function.restype
    return target
