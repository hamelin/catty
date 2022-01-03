from operator import add, neg
from typing import *  # noqa

from catty import reduce
from catty.words import unquote, St
from . import check_reduce


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


def test_operation_unary():
    assert reduce([-3, neg, 8, neg]) == [3, -8]


def test_unquote_unravel():
    assert reduce([0, [1, 2], unquote]) == [0, 1, 2]


def test_unquote_apply():
    assert reduce([8, [8, add]]) == [8, [8, add]]
    assert reduce([8, [8, add], unquote]) == [16]


def test_reduce_resolution():
    assert reduce([8, [7, St.top]]) == [[7, 8]]


def test_resolve_complex():
    assert reduce([2, 3, 4, 5, (78, (St[1], 55), {"p": 67, "q": [St + 2]})]) == [
        2, (78, (4, 55), {"p": 67, "q": [3]})
    ]


def test_resolve_consume_to_deepest_reference():
    check_reduce(
        [23, 1, 2, 3, 4, [St.post]],
        [23, 1, [2]]
    )


def test_resolve_repeat():
    check_reduce(
        [23, 1, 2, 3, {"a": St[1], "b": St[1], "c": St[1]}],
        [23, 1, {"a": 2, "b": 2, "c": 2}]
    )


def test_resolve_equiv_index_add():
    check_reduce(
        [23, 1, 2, 3, [St[1], St + 1]],
        [23, 1, [2, 2]]
    )


def test_resolve_equiv_literals():
    check_reduce(
        [23, 1, 2, 3, [St[0], St.top, St[1], St.next, St[2], St.post]],
        [23, [3, 3, 2, 2, 1, 1]]
    )
