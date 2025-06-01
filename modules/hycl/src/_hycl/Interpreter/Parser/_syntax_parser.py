from abc import ABC, abstractmethod

from ._types import *
from ..Lexer import Token

# TODO: 完成递归语法解析
# TODO: 模块暂停开发


class ASTNode(ABC):
    children: list

    @abstractmethod
    def __init__(self, children: list, **kwargs):
        ...


class GeneratorManager:
    def __init__(self, generators: list, next_hook=None):
        self._generators = generators
        self._next_hook = next_hook

    def result(self):
        while True:
            i = 0
            res = False
            if self._next_hook:
                self._next_hook()
            while i < len(self._generators):
                try:
                    res = next(self._generators[i])
                except StopIteration:
                    if isinstance(res, ASTNode):
                        return res
                    else:
                        raise RuntimeError("Unexpected error")
                finally:
                    if res is False:
                        self._generators.pop(i)
                        i -= 1
                i += 1

            if len(self._generators) == 0:
                return None


def _pos_generator_wrap_func(block, index_ls):
    for i in range(len(block.children)):
        if isinstance(block.children[i], Block):
            yield from _pos_generator_wrap_func(block.children[i], index_ls + [i])
        else:
            yield index_ls + [i]


class SyntaxParser:

    def __init__(self):

        self._pos: Pos = None
        self._block: Block = None

        self.end = None
        self._pos_generator = None

    def _pos_generator_func(self):
        return _pos_generator_wrap_func(self._block, [])

    def __getitem__(self, item: 'Pos'):
        current = self._block
        try:
            for index in item:
                current = current.children[index]  # 获取下一层的节点
            return current
        except (AttributeError, TypeError, IndexError):  # 中途有不是Block的节点,返回None
            return None

    def next(self):
        try:
            self._pos = next(self._pos_generator)
            return self[self._pos]
        except StopIteration:
            self.end = True
            return None

    def current(self) -> Token:
        return self[self._pos]

    def __p__template(self):
        # 如果符合语法，则返回True,对于返回False的语法判断生成器,判断器会停止该生成器
        # 语法判断主逻辑,对于每一次返回,pos都会更新
        # 比如:
        yield self.current() == ...
        yield self.current().t == ...
        yield self.current().v == ...
        # 如果返回False,判断器会停止它
        # 当有一个生成器正常退出,判断器将会将它作为匹配语法输出
        # 判断器会运行直到有一个生成器正常退出,判断器将会将它作为匹配语法输出
        # 如果没有生成器正常退出,判断器将会返回None
        yield ...  # 返回AST节点

    def _p_import(self):
        """
        import_stat ::= 'import' IDENT ('.' IDENT)* ('as' IDENT)?
        """
        yield self.current() == 'import'
        yield self.current().t == 'IDENT'
        while True:
            if self.current() == 'as':
                yield True  # 处理当前标记
                yield self.current().t == 'IDENT'  # 判断下一个标记是否为正确的标识符
                yield self.current() == '\n'  # 保证语句结束
                break  # 跳出循环,使生成器正常退出
            yield self.current() == '.'
            yield self.current().t == 'IDENT'

    def _p_from_import(self):
        """
        from_import_stat ::= 'from' IDENT ('.' IDENT)* 'import' IDENT ('as' IDENT)?
        """
        yield self.current() == 'from'
        yield self.current().t == 'IDENT'
        while True:
            if self.current().t not in ['IDENT', 'PERIOD']:
                break
            yield self.current() == '.'
            yield self.current().t == 'IDENT'
        yield self.current() == 'import'
        yield self.current().t == 'IDENT'
        if self.current() == 'as':
            yield True
            yield self.current().t == 'IDENT'

    def _p_table_def(self):
        """
        tabledef_stat ::= '[' IDENT ('.' IDENT)* ']'
        """
        yield self.current() == '['
        yield self.current().t == 'IDENT'
        while True:
            if self.current().t not in ['IDENT', 'PERIOD']:
                yield self.current() == ']'
                return
            yield self.current() == '.'
            yield self.current().t == 'IDENT'

    def parse(self, block: Block):
        self._block = block
        self._pos_generator = self._pos_generator_func()
        syntax_match_funcs = [
            getattr(self, fc)
            for fc in dir(self)
            if fc.startswith('_p_')
        ]
        # print(syntax_match_funcs)
        # self.next()
        while True:
            gm = GeneratorManager([
                fc()
                for fc in syntax_match_funcs
            ], next_hook=self.next)
            res = gm.result()
            if res:
                print(res)
            if res is None and not self.end:
                raise SyntaxError(f"Cannot match any syntax.")
