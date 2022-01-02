from contextlib import contextmanager
import inspect as ins
from operator import add, sub, gt
import sys
from typing import *  # noqa

import pytest

from catty import reduce
from catty.words import Word, apply, fork, over, tuck


@contextmanager
def limit_recursion_low() -> Iterator:
    depth_here = len(ins.getouterframes(ins.currentframe()))
    limit_recursion = sys.getrecursionlimit()
    sys.setrecursionlimit(depth_here + 50)
    try:
        yield
    finally:
        sys.setrecursionlimit(limit_recursion)


def test_function_python_finite_recursion():
    def adder_py(n: int, t: int = 0) -> int:
        if n <= 0:
            return t
        return adder_py(n - 1, t + n)

    with limit_recursion_low():
        with pytest.raises(RecursionError):
            total = adder_py(100)
            assert total == 101 * 100 / 2
            pytest.fail("Should fail on recursion excess")


adder_catty = Word(
    over, 0, gt,
    [over, 1, sub, tuck, add, apply.adder_catty],
    [],
    fork
)


def test_quote_catty_arbitrary_recursion():
    with limit_recursion_low():
        _, total = reduce([100, 0, adder_catty])
        assert total == 101 * 100 / 2
