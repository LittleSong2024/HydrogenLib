from ....data_structures import Stack
from .token import Token


def _calc_indent_length(indent):
    value = indent
    return value.count('\t') * 4 + value.count(' ')


def _process_tokens(tokens: list[Token]):
    i = 0
    length = len(tokens)
    while i < length:
        length = len(tokens)
        if tokens[i].type == 'NEWLINE':
            if i + 1 < length and tokens[i + 1].type == 'NEWLINE':
                tokens.insert(i + 1, Token(
                    'WS', ''
                ))
                # i += 1
            if i + 1 < length and tokens[i + 1].type == 'WS':
                # if i+2 < length and tokens[i+2].type == 'NEWLINE':
                #     tokens.pop(i)
                #     tokens.pop(i+1)
                #     tokens.pop(i+2)
                #     i += 2
                #     continue
                ws = tokens[i + 1]
                tokens[i + 1] = Token(
                    'INDENT', _calc_indent_length(ws.value),
                    tokens[i].lineno, tokens[i].colno, tokens[i].offset + ws.offset
                )
                i += 1

        i += 1


def _process_indent(tokens: list[Token]) -> list[Token]:
    processed_tokens = []
    indent_stack = Stack([0])  # Use a stack to keep track of indentation levels

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
    i = len(tokens) - 1
    while i >= 0:
        if tokens[i].type == 'NEWLINE':
            tokens.pop(i)
        else:
            break
        i -= 1
