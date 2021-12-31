from operator import add
from typing import *  # noqa

from catty import reduce


def test_reduce_empty():
    assert reduce([]) == []


def test_reduce_constants():
    assert reduce([0]) == [0]
    assert reduce([1, None, "asdf"]) == [1, None, "asdf"]


def test_reduce_complexes():
    assert reduce((1, [4, 90, [None]], {"a": 90, "b": 12}, (3,))) == [
        1,
        [4, 90, [None]],
        {"a": 90, "b": 12},
        (3,)
    ]


def test_operation_simple():
    assert reduce([-3, 1, 3, add]) == [-3, 4]


def test_operation_simple2():
    assert reduce([1, 3, add, 2, add, 8]) == [6, 8]


def test_no_input():
    def thousand() -> int:
        return 1000

    assert reduce([None, 3, thousand, 8]) == [None, 3, 1000, 8]


def test_quote():
    assert reduce([-3, 1, 3, [add]]) == [-3, 1, 3, [add]]
