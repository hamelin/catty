from types import SimpleNamespace as SN
from typing import *  # noqa

import pytest

from catty.words import St, top, peer, alt
from . import check_reduce


def test_resolve_simple():
    check_reduce([8, [7, top]], [[7, 8]])


def test_resolve_complex():
    check_reduce(
        [2, 3, 4, 5, (78, (St[1], 55), {"p": 67, "q": [St[2]]})],
        [2, (78, (4, 55), {"p": 67, "q": [3]})]
    )


def test_resolve_consume_to_deepest_reference():
    check_reduce(
        [23, 1, 2, 3, 4, [alt]],
        [23, 1, [2]]
    )


def test_resolve_repeat():
    check_reduce(
        [23, 1, 2, 3, {"a": peer, "b": peer, "c": peer}],
        [23, 1, {"a": 2, "b": 2, "c": 2}]
    )


def test_resolve_equiv_literals():
    check_reduce(
        [23, 1, 2, 3, [St[0], top, St[1], peer, St[2], alt]],
        [23, [3, 3, 2, 2, 1, 1]]
    )


def test_bare():
    check_reduce(
        [23, 1, 2, 3, St[2]],
        [23, 1]
    )


def test_slice():
    check_reduce(
        [23, 1, 2, 3, St[0:3]],
        [23, [1, 2, 3]]
    )


def test_slice_interval3():
    check_reduce(
        [23, 1, 2, 3, 4, 5, 6, 7, 8, 9, St[1:7:3]],
        [23, 1, 2, [5, 8]]
    )
    check_reduce(
        [23, 1, 2, 3, 4, 5, 6, 7, 8, 9, St[2:7:3]],
        [23, 1, 2, [4, 7]]
    )


def test_slice_interval4():
    check_reduce(
        [23, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, St[1:9:4]],
        [23, 1, 2, 3, [7, 11]]
    )
    check_reduce(
        [23, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, St[2:9:4]],
        [23, 1, 2, 3, [6, 10]]
    )
    check_reduce(
        [23, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, St[3:9:4]],
        [23, 1, 2, 3, [5, 9]]
    )
    check_reduce(
        [23, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, St[:9:4]],
        [23, 1, 2, 3, [4, 8, 12]]
    )


@pytest.fixture
def root() -> SN:
    r = SN()
    r.asdf = SN()
    r.asdf.qwer = "HEY"
    r.heyhey = "hoho"
    return r


def test_subref_attr(root):
    check_reduce([root, top.heyhey], ["hoho"])


def test_subref_attrs(root):
    check_reduce([root, top.asdf.qwer], ["HEY"])


def test_subref_item():
    check_reduce([["asdf", "qwer"], top[1], top[2:]], ["er"])
    check_reduce([["asdf", "qwer"], top[1][2:]], ["er"])


def test_subref_mixed(root):
    check_reduce(
        [["asdf", root, "zxcv"], top[1:][0].heyhey[2:]],
        ["ho"]
    )
