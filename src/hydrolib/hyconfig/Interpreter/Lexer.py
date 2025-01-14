from collections import deque
from typing import Any, Union
from ...re_plus import *
from ...data_structures import Stack

# TODO: 词法分析器,Token新的参数


class Token:
    def __init__(
            self,
            type_: str, value: Union[re.Match, Any],
            lineno: int = 0, colno: int = 0, offset: int = 0
    ):
        self.type = type_
        self.lineno = lineno
        self.colno = colno
        self.offset = offset

        if isinstance(value, re.Match):
            self.match = value
            self.value: Union[str, int] = value.group()
        else:
            self.value: Union[str, int] = value

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(str(self.value))

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.type},\t{repr(self.value)},\t{self.lineno}:{self.colno}-{self.offset}>"


NEWLINE = Literal('\n')

IDENT = Re('[a-zA-Z_][a-zA-Z0-9_-]*')

WHITESPACE = Re(r'\s+')

IMPORT = Literal('import')
AS = Literal('as')
FROM = Literal('from')
PASS = Literal('pass')

LP = Re(r'[(\[{]')
RP = Re(r'[)\]}]')

LFILLTOKEN = Literal('{<')
RFILLTOKEN = Literal('>}')

SPLIT_CHAR = Re(r'[,.]')

ASSIGN = Literal('=')

INT = Re('-?[0-9]+')
eINT = Re(r'-?\d+e\d+')
jINT = Re(r'[+-]?[0-9]+j')

hINT = Re(r'0x[0-9a-fA-F]+')
bINT = Re(r'0b[01]+')
oINT = Re(r'0o[0-7]+')


STR = Re(r'"([^"\\]*(\\.[^"\\]*)*)"')
sSTR = Re(r"'([^'\\]*(\\.[^'\\]*)*)'")
multiSTR = Re(r'"""([^"]|"")*"""')


# 定义记号规则
TOKEN_PATTERNS = [
    ("NEWLINE", NEWLINE),
    # ("DEDENT", ...)  # 退缩记号,由后期添加

    ("KEYWORD", IMPORT),
    ("KEYWORD", AS),
    ("KEYWORD", FROM),
    ("KEYWORD", PASS),

    ("LFILL", LFILLTOKEN),
    ("RFILL", RFILLTOKEN),

    ("OPER", Re(r'((//)|[\+\-\*/^&\|%]|<<|>>)')),

    ("IDENT", IDENT),
    ("ASSIGN", ASSIGN),

    ("INT", INT),
    ("INT", eINT),
    ("INT", jINT),
    ("INT", oINT),
    ("INT", bINT),
    ("INT", hINT),

    ("STR", STR),
    ("STR", sSTR),
    ("STR", multiSTR),

    ("LP", LP),
    ("RP", RP),

    ("SPLIT_CHAR", SPLIT_CHAR),
    ("WS", WHITESPACE),
    # ("UNKNOWN", ANY),
]  # type: list[tuple[str, BaseRe]]


# "\""

def _lex(code):
    longer_match = None
    longer_token = None
    for token_type, pattern in TOKEN_PATTERNS:
        match = pattern.match(code)
        if match is None:
            # print(f"{token_type} not match")
            continue
        token = Token(token_type, match)
        return token
    # print(f"Longer Token: {longer_token}")
    # return longer_token


def _calc_indent_length(indent):
    value = indent
    return value.count('\t') * 4 + value.count(' ')


def _process_tokens(tokens: list[Token]):
    i = 0
    while i < len(tokens):
        if tokens[i].type == 'NEWLINE':
            if tokens[i+1].type == 'WS':
                ws = tokens[i+1]
                tokens.pop(i+1)
                tokens[i] = Token(
                    'INDENT', _calc_indent_length(ws.value),
                    tokens[i].lineno, tokens[i].colno, tokens[i].offset + ws.offset
                )
                i += 1

        i += 1


def _process_indent(tokens: list[Token]) -> list[Token]:
    processed_tokens = []
    indent_stack = Stack()  # Use a stack to keep track of indentation levels

    for i, token in enumerate(tokens):
        if token.type == 'INDENT':
            current_indent = token.value
            last_indent = indent_stack.at_top

            if current_indent > last_indent:
                # Increase indentation level
                indent_stack.push(current_indent)
                processed_tokens.append(
                    Token(
                        'INDENT', current_indent - last_indent, token.lineno, token.colno, token.offset))
            elif current_indent < last_indent:
                # Decrease indentation level
                while indent_stack and current_indent < indent_stack[-1]:
                    last_indent = indent_stack.pop()
                    processed_tokens.append(Token('DEDENT', last_indent - current_indent))

                if not indent_stack or current_indent != indent_stack[-1]:
                    raise IndentationError(f"Unexpected dedent at position {i}")
            else:
                # No change in indentation
                continue
        else:
            processed_tokens.append(token)

    # Handle any remaining dedents at the end of the file
    while len(indent_stack) > 1:
        last_indent = indent_stack.pop()
        processed_tokens.append(Token('DEDENT', last_indent - indent_stack[-1]))

    return processed_tokens


def _delete_whitespace(tokens: list[Token]):
    i = 0
    while i < len(tokens):
        if tokens[i].type == 'WS':
            tokens.pop(i)
        else:
            i += 1


def _token_strip(tokens: list[Token]):
    i = 0
    while i < len(tokens):
        if tokens[i].type == 'NEWLINE':
            tokens.pop(i)
        else:
            break
        i += 1
    i = len(tokens)-1
    while i >= 0:
        if tokens[i].type == 'NEWLINE':
            tokens.pop(i)
        else:
            break
        i -= 1


# 词法分析器
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
    # _process_tokens(tokens_lst)
    # _process_indent(tokens_lst)
    _delete_whitespace(tokens_lst)
    _token_strip(tokens_lst)

    return tokens_lst
