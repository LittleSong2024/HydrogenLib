from typing import Optional

from ...type_func.LiteralEval import literal_eval as _lt_ev


def literal_eval(string, globals_: Optional[dict] = None, locals_: Optional[dict] = None, builtins: bool = False,
                 no_eval: bool = True):
    return _lt_ev(string, globals_, locals_, builtins, no_eval)
