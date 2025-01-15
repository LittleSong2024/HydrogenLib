from typing import Union

from .Lexer import Token, Lexer
from ...data_structures import Stack

q_map = {
    '(': ')',
    '[': ']',
    '{': '}',
}


class Block:
    def __init__(self, tokens: list[Union[Token, 'Block']] = None):
        self.children = tokens if tokens is not None else []

    def addChild(self, node):
        self.children.append(node)

    def sort(self):
        i = 0
        while i < len(self.children):
            if isinstance(self.children[i], Block):
                self.children[i].sort()
            else:
                if self.children[i].type in {'WS', 'NEWLINE', 'INDENT', 'DEDENT'}:
                    self.children.pop(i)
                    i -= 1
            i += 1

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)

    def __setitem__(self, key, value):
        self.children[key] = value


class BlockParser:
    def __init__(self):
        self.lexer = None
        self.tokens = None
        self.pos = 0

        self.result = None

    def setLexer(self, lexer):
        self.lexer = lexer

    def setTokens(self, tokens):
        self.tokens = tokens

    def __parse_to_blocks(self):
        stack = Stack([Block()])
        qstack = Stack()
        for token in self.tokens:
            if token.type == 'LP':
                qstack.push(token)
            elif token.type == 'RP':
                if qstack.at_top:
                    data = qstack.pop()
                    if q_map[data.value] != token.value:
                        raise SyntaxError(f"Unexpected '{token.value}' at position {self.pos}")
                else:
                    raise SyntaxError(f"Unexpected ')' at position {self.pos}")
            if token.type == 'INDENT' and not qstack.at_top:
                new_block = Block()
                if stack.at_top:
                    stack.at_top.addChild(new_block)
                stack.push(new_block)
            elif token.type == 'DEDENT' and not qstack.at_top:
                stack.pop()
            else:
                if stack.at_top:
                    stack.at_top.addChild(token)
                else:
                    stack.push(Block([token]))
        self.result = stack.at_top

    def parse(self, source_code):
        if self.tokens is None:
            self.tokens = self.lexer.lex(source_code)
        self.__parse_to_blocks()
        return self.result


class SyntaxParser:
    class Pos:
        def __init__(self, index_ls):
            self._index_ls = index_ls

        def __iter__(self):
            for i in self._index_ls:
                yield i

    def __init__(self, _block_parser):
        Pos = self.Pos

        self.pos: Pos = None

        self.end = None
        self._block_parser = _block_parser
        self._pos_generator = self._pos_generator_func()

    def _pos_generator_func(self):
        stack = Stack([self._block_parser.result])
        index = Stack([0])
        while True:
            cr = stack.at_top
            i = index.at_top
            if isinstance(cr[i], Block):
                stack.push(cr[i])
                index.push(0)
            else:
                index.at_top += 1
                if index.at_top >= len(cr):
                    stack.pop()
                    index.pop()
                    if not stack.at_top:
                        break
                    continue
                yield self.Pos(index)

    def __getitem__(self, item: 'Pos'):
        current = self._block_parser.result
        for index in item:
            current = current.children[index]
        return current

    def next(self):
        try:
            self.pos = next(self._pos_generator)
            return self[self.pos]
        except StopIteration:
            self.end = True
            return None

    def current(self):
        return self[self.pos]

    def __p__template(self):
        start = ...
        yield start == ...  # 判断开头是否符合语法
        # 如果符合语法，则返回True,对于返回False的语法判断生成器,判断器会停止它

        # 语法判断主逻辑
        yield ...
        yield ...
        yield ...
        # 同样,如果返回False,则判断器会停止它
        # 当有一个生成器正常退出,判断器将会将它作为匹配语法输出
        # 判断器会运行直到有一个生成器正常退出,判断器将会将它作为匹配语法输出
        # 如果没有生成器正常退出,判断器将会返回None
        yield ...  # 最后返回语法匹配结果(AST节点)

    def _p_import(self):
        i = 0
        mode = 0
        start = self.current()
        # mode
        # 0: import `module`
        # 1: import `module` as `alias`
        yield start == 'import'

    def _p_from_import(self):
        i = 0




class Parser:

    def __init__(self):
        self._lexer = Lexer()
        self._block_parser = BlockParser()
        self.result = None

    def parse(self, source_code):
        self._block_parser.setLexer(self._lexer)
        self._block_parser.parse(source_code)

        self.result = self._block_parser.result
