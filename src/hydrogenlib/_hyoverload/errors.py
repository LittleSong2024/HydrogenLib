import inspect
import sys
import traceback
from inspect import Signature

import rich

from . import namespace as namespace


class OverloadError(Exception):
    def __init__(self, qual_name, tests=(), args=(), kwargs=None):
        self.qual_name = qual_name
        self.tests = tests
        self.msg = ''
        self.args = args
        self.kwargs = kwargs or {}

    @staticmethod
    def to_call_format(args, kwargs):
        ls = list(map(
            lambda x:
            type(x).__name__, args
        )) + \
             list(map(
                 lambda x:
                 f'{x[0]}={type(x[1]).__name__}', kwargs
             ))

        if len(ls) == 1:
            string = ls[0] + ','
        else:
            string = ', '.join(ls)
        return string

    @staticmethod
    def to_args_format(signature: Signature):
        params = signature.parameters
        string = ', '.join(
            list(map(str, params.values()))
        )
        return string

    @staticmethod
    def to_type_name(type_: inspect.Parameter):
        if type_.annotation is inspect.Parameter.empty:
            return 'Any'
        else:
            return str(type_.annotation.__name__)

    @staticmethod
    def __rich_to_string(string):
        console = rich.get_console()
        console.width = 200
        rich_string = console.render(string)
        result = ''
        for part in rich_string:
            result += str(part.text)
        return result

    def generate_error_msg(self):
        error_msg = ''

        def add_error_msg(string):
            nonlocal error_msg
            error_msg += self.__rich_to_string(string)

        add_error_msg(f'无法匹配重载类型\n')
        add_error_msg(f'[yellow]传入的实参:[/yellow] {self.to_call_format(self.args, self.kwargs)}')
        for test, func in zip(self.tests, namespace.overloads[self.qual_name]):
            add_error_msg(
                f'\t[yellow]尝试匹配: {func.signature} [/yellow]'
                f'匹配度为 [red]{str(test[0])}[/red]'
            )
        return error_msg

    def __str__(self):
        try:
            return self.generate_error_msg()
        except Exception as e:
            return str(e)


class OverloadRuntimeError(Exception):
    def __init__(self, qualname, called_overload, e, call_args, call_kwargs):
        self.qualname = qualname
        self.called_overload = called_overload
        self.e = e
        self.args = call_args
        self.kwargs = call_kwargs

    def __str__(self):
        return (f'\n以参数 ({OverloadError.to_call_format(self.args, self.kwargs)}) '
                f'调用 `{self.qualname}` '
                f'的重载 "{self.called_overload}" '
                f'时发生错误.'
                '\n\n详细信息:\n\n' +
                (''.join(traceback.format_exception(self.e)))
                )
