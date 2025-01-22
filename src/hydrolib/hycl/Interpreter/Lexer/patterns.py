from ....re_plus import Literal, Re, BaseRe

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
COMMA = Literal(',')
PERIOD = Literal('.')
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
TokenPatterns = [
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

    ("STR", multiSTR),
    ("STR", STR),
    ("STR", sSTR),

    ("LP", LP),
    ("RP", RP),

    ("COMMA", COMMA),
    ("PERIOD", PERIOD),

    ("WS", WHITESPACE),
    # ("UNKNOWN", ANY),
]  # type: list[tuple[str, BaseRe]]
