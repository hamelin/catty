from typing import *  # noqa

from catty import reduce


def test_reduce_empty():
    assert reduce([]) == ()


def test_reduce_constants():
    assert reduce([0]) == (0,)
    assert reduce([1, None, "asdf"]) == (1, None, "asdf")
