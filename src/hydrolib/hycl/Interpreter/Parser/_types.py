from typing import Union

from src.hydrolib.hycl.Interpreter.Lexer import Token


class Pos:
    def __init__(self, index_ls):
        self._index_ls = index_ls  # type: list[int]

    def move_out(self):
        self._index_ls.pop()

    def move_in(self, index=0):
        self._index_ls.append(index)

    @property
    def root(self):
        return type(self)(self._index_ls[0])

    def __getitem__(self, item):
        return self._index_ls[item]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._index_ls == other._index_ls
        elif isinstance(other, list):
            return self._index_ls == other
        return False

    def __len__(self):
        return len(self._index_ls)

    def __iter__(self):
        yield from self._index_ls


class Block:
    def __init__(self, tokens: list[Union[Token, 'Block']] = None):
        self.children = tokens if tokens is not None else []

    def empty(self):
        return len(self.children) == 0

    def addChild(self, node):
        self.children.append(node)

    def sort(self):
        i = 0
        while i < len(self.children):
            if isinstance(self.children[i], Block):
                if self.children[i].empty():
                    self.children.pop(i)
                    i -= 1
                else:
                    self.children[i].sort()
            else:
                if self.children[i].type in {'WS', 'INDENT', 'DEDENT'}:
                    self.children.pop(i)
                    i -= 1
            i += 1

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)

    def __bool__(self):
        return True

    def __setitem__(self, key, value):
        self.children[key] = value
