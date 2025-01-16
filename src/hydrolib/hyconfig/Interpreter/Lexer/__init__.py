from collections import deque

from .token import Token

from .patterns import TokenPatterns
from .process import _process_tokens, _process_indent, _token_strip, _delete_whitespace, _calc_indent_length



# TODO: 词法分析器,Token新的参数


def _lex(code):
    for token_type, pattern in TokenPatterns:
        match = pattern.match(code)
        if match is None:
            # print(f"{token_type} not match")
            continue
        token = Token(token_type, match)
        return token
    # print(f"Longer Token: {longer_token}")
    # return longer_token


# 词法分析器
class Lexer:
    @staticmethod
    def lex(source_code):
        tokens = deque()
        while source_code:
            token = _lex(source_code)
            if token is None:
                current_code = source_code.split('\n')[0]
                raise SyntaxError(f"Invalid syntax: {current_code}")
            tokens.append(token)
            source_code = source_code[len(token):]
        tokens_lst = list(tokens)
        _token_strip(tokens_lst)
        _process_tokens(tokens_lst)
        tokens_lst = _process_indent(tokens_lst)
        _delete_whitespace(tokens_lst)

        return tokens_lst
