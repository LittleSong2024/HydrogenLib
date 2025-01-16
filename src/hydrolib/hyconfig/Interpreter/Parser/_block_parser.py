from ._types import Block
from ....data_structures import Stack
from ....type_func.Dict import ConstDict

bracket_map = ConstDict(
    {
        '(': ')',
        '[': ']',
        '{': '}',
    }
)


class BracketTracker:
    def __init__(self):
        self._s = Stack()

    def trace(self, char):
        if char in bracket_map.keys():
            self._s.push(char)
        elif char in bracket_map.values():
            top = self._s.at_top
            if bracket_map[top] != char:
                raise SyntaxError(f"Bracket mismatch. (Except '{bracket_map[top]}', but got '{char}')")
            self._s.pop()

    def stack_length(self):
        return self._s.size()

    def matched(self):
        return self._s.is_empty()


class BlockParser:
    def __init__(self):
        self.tokens = None

    def __parse_to_blocks(self):
        stack = Stack([Block()])
        tracker = BracketTracker()
        for token in self.tokens:
            if token.type in ['LP', 'RP']:
                tracker.trace(token.v)
            if token.type == 'INDENT' and tracker.matched():
                new_block = Block()
                if stack.at_top:
                    stack.at_top.addChild(new_block)
                stack.push(new_block)
            elif token.type == 'DEDENT' and tracker.matched():
                stack.pop()
            else:
                if stack.at_top:
                    stack.at_top.addChild(token)
                else:
                    stack.push(Block([token]))
        return stack.at_top

    def parse(self, tokens):
        self.tokens = tokens
        return self.__parse_to_blocks()
