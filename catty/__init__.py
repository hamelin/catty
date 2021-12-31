import inspect as ins
from typing import *


def reduce(program: Iterable) -> Sequence:
    stack: List = []
    for word in program:
        if hasattr(word, "__call__"):
            sig = ins.signature(word)
            num_args = len([
                p
                for p in sig.parameters.values()
                if (
                    p.kind in {
                        ins.Parameter.POSITIONAL_ONLY,
                        ins.Parameter.POSITIONAL_OR_KEYWORD
                    } and p.default is ins.Parameter.empty
                )
            ])
            if num_args == 0:
                args = []
            else:
                args = stack[-num_args:]
                del stack[-num_args:]
            stack.append(word(*args))
        else:
            stack.append(word)
    return stack
