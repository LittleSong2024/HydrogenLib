from ._block_parser import \
    BlockParser

from ._syntax_parser import \
    SyntaxParser

from ._types import \
    Block

from ..Lexer import \
    Lexer


class Parser:

    def __init__(self):
        self._lexer = Lexer()
        self._block_parser = BlockParser()
        self._syntax_parser = SyntaxParser()
        self.tokens = None
        self.block = None
        self.ast = None

    def parse(self, source_code):
        self.tokens = self._lexer.lex(source_code)
        self.block = self._block_parser.parse(self.tokens)
        self.ast = self._syntax_parser.parse(self.block)
